"""Cancellation-aware ADB command execution."""

from __future__ import annotations

import os
import subprocess
import threading
import time
from dataclasses import dataclass
from typing import Callable, Optional

from spfarm.infrastructure.devices.adb import AdbRunner


@dataclass(frozen=True)
class AdbCommandOutput:
    returncode: int
    stdout: bytes = b""
    stderr: bytes = b""
    timed_out: bool = False
    cancelled: bool = False
    duration_ms: float = 0.0

    @property
    def succeeded(self) -> bool:
        return self.returncode == 0 and not self.timed_out and not self.cancelled

    @property
    def stdout_text(self) -> str:
        return self.stdout.decode(errors="replace")

    @property
    def stderr_text(self) -> str:
        return self.stderr.decode(errors="replace")


AdbServiceExecutor = Callable[
    [list[str], float, threading.Event],
    AdbCommandOutput,
]


def _execute_cancellable(
    args: list[str], timeout: float, cancel_event: threading.Event
) -> AdbCommandOutput:
    started = time.perf_counter()
    try:
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
    except OSError as error:
        return AdbCommandOutput(
            returncode=-1,
            stderr=str(error).encode(),
            duration_ms=(time.perf_counter() - started) * 1000,
        )

    deadline = time.monotonic() + timeout
    while process.poll() is None:
        cancelled = cancel_event.wait(0.05)
        timed_out = time.monotonic() >= deadline
        if cancelled or timed_out:
            process.kill()
            stdout, stderr = process.communicate()
            message = b"ADB command cancelled" if cancelled else b"ADB command timed out"
            return AdbCommandOutput(
                returncode=-1,
                stdout=stdout,
                stderr=stderr or message,
                timed_out=timed_out,
                cancelled=cancelled,
                duration_ms=(time.perf_counter() - started) * 1000,
            )

    stdout, stderr = process.communicate()
    return AdbCommandOutput(
        returncode=process.returncode,
        stdout=stdout,
        stderr=stderr,
        duration_ms=(time.perf_counter() - started) * 1000,
    )


class AdbService:
    def __init__(
        self,
        runner: Optional[AdbRunner] = None,
        executor: Optional[AdbServiceExecutor] = None,
    ) -> None:
        self.runner = runner or AdbRunner()
        self._executor = executor or _execute_cancellable

    @property
    def is_available(self) -> bool:
        return self.runner.is_available

    @property
    def executable_path(self) -> str:
        return str(self.runner.executable_path or "")

    def run(
        self,
        args: list[str],
        timeout: float = 30.0,
        cancel_event: Optional[threading.Event] = None,
    ) -> AdbCommandOutput:
        cancellation = cancel_event or threading.Event()
        if cancellation.is_set():
            return AdbCommandOutput(
                returncode=-1,
                stderr=b"ADB command cancelled",
                cancelled=True,
            )
        if not self.runner.is_available or not self.runner.executable_path:
            return AdbCommandOutput(returncode=-1, stderr=b"ADB executable not found")
        return self._executor(
            [str(self.runner.executable_path), *args],
            timeout,
            cancellation,
        )

    def run_for_device(
        self,
        target: str,
        args: list[str],
        timeout: float = 30.0,
        cancel_event: Optional[threading.Event] = None,
    ) -> AdbCommandOutput:
        return self.run(["-s", target, *args], timeout, cancel_event)

    def diagnostics(self) -> dict[str, object]:
        return {
            "available": self.is_available,
            "executable_path": self.executable_path,
        }
