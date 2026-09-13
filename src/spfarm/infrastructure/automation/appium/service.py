"""Lifecycle manager for isolated local Appium server processes."""

from __future__ import annotations

import contextlib
import os
import shutil
import socket
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Protocol

import requests


class ManagedProcess(Protocol):
    def poll(self) -> Optional[int]: ...

    def terminate(self) -> None: ...

    def kill(self) -> None: ...

    def wait(self, timeout: Optional[float] = None) -> int: ...


ProcessFactory = Callable[[list[str]], ManagedProcess]
StatusProbe = Callable[[str, float], bool]


def _start_process(args: list[str]) -> ManagedProcess:
    return subprocess.Popen(
        args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )


def _probe_status(server_url: str, timeout: float) -> bool:
    try:
        response = requests.get(f"{server_url}/status", timeout=timeout)
        return response.ok
    except requests.RequestException:
        return False


class PortAllocator:
    def __init__(self, start: int = 4723) -> None:
        self._next = start
        self._allocated: set[int] = set()
        self._lock = threading.Lock()

    def acquire(self) -> int:
        with self._lock:
            port = self._next
            while port in self._allocated or not self._is_free(port):
                port += 1
            self._allocated.add(port)
            self._next = port + 1
            return port

    def reserve(self, port: int) -> None:
        with self._lock:
            if port in self._allocated or not self._is_free(port):
                raise RuntimeError(f"Port {port} is unavailable")
            self._allocated.add(port)

    def release(self, port: int) -> None:
        with self._lock:
            self._allocated.discard(port)

    @staticmethod
    def _is_free(port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as candidate:
            try:
                candidate.bind(("127.0.0.1", port))
            except OSError:
                return False
        return True


@dataclass
class AppiumServer:
    port: int
    process: ManagedProcess
    generation: int = 1

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    @property
    def is_running(self) -> bool:
        return self.process.poll() is None


class AppiumServiceManager:
    def __init__(
        self,
        executable_path: Optional[Path] = None,
        process_factory: Optional[ProcessFactory] = None,
        status_probe: Optional[StatusProbe] = None,
        port_allocator: Optional[PortAllocator] = None,
        startup_timeout: float = 15.0,
    ) -> None:
        configured = str(executable_path) if executable_path else shutil.which("appium")
        self.executable_path = Path(configured) if configured else None
        self._process_factory = process_factory or _start_process
        self._status_probe = status_probe or _probe_status
        self._ports = port_allocator or PortAllocator()
        self._startup_timeout = startup_timeout
        self._servers: dict[int, AppiumServer] = {}
        self._lock = threading.RLock()
        self._watchdog_stop = threading.Event()
        self._watchdog_thread: Optional[threading.Thread] = None

    @property
    def is_available(self) -> bool:
        return self.executable_path is not None and self.executable_path.exists()

    def start(self, port: Optional[int] = None) -> AppiumServer:
        if not self.is_available or not self.executable_path:
            raise RuntimeError("Appium executable not found")
        selected_port = port or self._ports.acquire()
        if port:
            self._ports.reserve(port)
        process = self._process_factory(
            [
                str(self.executable_path),
                "--address",
                "127.0.0.1",
                "--port",
                str(selected_port),
            ]
        )
        server = AppiumServer(port=selected_port, process=process)
        with self._lock:
            prior = self._servers.get(selected_port)
            if prior:
                server.generation = prior.generation + 1
            self._servers[selected_port] = server
        if not self._wait_until_ready(server):
            self.stop(server)
            raise RuntimeError(f"Appium failed to start on port {selected_port}")
        return server

    def ensure_running(self, server: AppiumServer) -> AppiumServer:
        with self._lock:
            current = self._servers.get(server.port)
        if (
            current is not None
            and current is not server
            and current.is_running
            and self._status_probe(current.url, 1.0)
        ):
            return current
        if server.is_running and self._status_probe(server.url, 1.0):
            return server
        self._stop_process(server.process)
        with self._lock:
            if self._servers.get(server.port) is server:
                self._servers.pop(server.port, None)
        self._ports.release(server.port)
        replacement = self.start(server.port)
        replacement.generation = server.generation + 1
        return replacement

    def stop(self, server: AppiumServer) -> None:
        self._stop_process(server.process)
        with self._lock:
            if self._servers.get(server.port) is server:
                self._servers.pop(server.port, None)
                self._ports.release(server.port)

    def stop_all(self) -> None:
        with self._lock:
            servers = list(self._servers.values())
        for server in servers:
            self.stop(server)
        self.stop_watchdog()

    def start_watchdog(self, interval_seconds: float = 5.0) -> None:
        with self._lock:
            if self._watchdog_thread and self._watchdog_thread.is_alive():
                return
            self._watchdog_stop.clear()
            self._watchdog_thread = threading.Thread(
                target=self._watch,
                args=(interval_seconds,),
                name="appium-watchdog",
                daemon=True,
            )
            self._watchdog_thread.start()

    def stop_watchdog(self) -> None:
        self._watchdog_stop.set()
        thread = self._watchdog_thread
        if thread and thread is not threading.current_thread():
            thread.join(timeout=2.0)
        self._watchdog_thread = None

    def diagnostics(self) -> dict[str, object]:
        with self._lock:
            servers = list(self._servers.values())
        return {
            "available": self.is_available,
            "executable_path": str(self.executable_path or ""),
            "servers": [
                {
                    "port": server.port,
                    "running": server.is_running,
                    "generation": server.generation,
                }
                for server in servers
            ],
        }

    def _watch(self, interval_seconds: float) -> None:
        while not self._watchdog_stop.wait(interval_seconds):
            with self._lock:
                servers = list(self._servers.values())
            for server in servers:
                with contextlib.suppress(RuntimeError):
                    self.ensure_running(server)

    def _wait_until_ready(self, server: AppiumServer) -> bool:
        deadline = time.monotonic() + self._startup_timeout
        while server.is_running and time.monotonic() < deadline:
            if self._status_probe(server.url, 0.5):
                return True
            time.sleep(0.05)
        return False

    @staticmethod
    def _stop_process(process: ManagedProcess) -> None:
        if process.poll() is not None:
            return
        process.terminate()
        try:
            process.wait(timeout=5.0)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=2.0)
