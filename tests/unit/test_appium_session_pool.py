"""Tests for concurrent per-device Appium sessions and disposable leases."""

import threading
from pathlib import Path
from typing import Any, Optional

from spfarm.infrastructure.automation.appium.service import AppiumServiceManager
from spfarm.infrastructure.automation.sessions.pool import AppiumSessionPool


class FakeProcess:
    def __init__(self) -> None:
        self.returncode: Optional[int] = None

    def poll(self) -> Optional[int]:
        return self.returncode

    def terminate(self) -> None:
        self.returncode = 0

    def kill(self) -> None:
        self.returncode = -9

    def wait(self, timeout: Optional[float] = None) -> int:
        del timeout
        return self.returncode or 0


class FakeTransport:
    def __init__(self) -> None:
        self.requests: list[tuple[str, str, Optional[dict[str, Any]]]] = []
        self._lock = threading.Lock()
        self._created = 0
        self.barrier = threading.Barrier(2)

    def request(
        self,
        method: str,
        url: str,
        payload: Optional[dict[str, Any]] = None,
        timeout: float = 30.0,
    ) -> tuple[int, dict[str, Any]]:
        del timeout
        with self._lock:
            self.requests.append((method, url, payload))
        if method == "POST" and url.endswith("/session"):
            self.barrier.wait(timeout=2.0)
            with self._lock:
                self._created += 1
                session_id = f"session-{self._created}"
            return 200, {"value": {"sessionId": session_id}}
        return 200, {"value": None}


def test_concurrent_devices_get_isolated_sessions_and_ports(tmp_path: Path) -> None:
    executable = tmp_path / "appium"
    executable.touch()
    manager = AppiumServiceManager(
        executable_path=executable,
        process_factory=lambda _args: FakeProcess(),
        status_probe=lambda _url, _timeout: True,
    )
    transport = FakeTransport()
    pool = AppiumSessionPool(manager, transport=transport)
    leases: list[object] = []

    def acquire(device_id: str, target: str) -> None:
        leases.append(pool.acquire(device_id, target))

    threads = [
        threading.Thread(target=acquire, args=("device-1", "emulator-5554")),
        threading.Thread(target=acquire, args=("device-2", "emulator-5556")),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    first = pool.get_session("device-1")
    second = pool.get_session("device-2")
    assert first.session_id != second.session_id
    assert first.server.port != second.server.port
    assert first.system_port != second.system_port
    assert first.capabilities["appium:options"]["udid"] == "emulator-5554"
    assert second.capabilities["appium:options"]["udid"] == "emulator-5556"

    for lease in leases:
        lease.release()  # type: ignore[attr-defined]
    assert pool.diagnostics()["active_sessions"] == 0


def test_session_is_recreated_after_appium_restart(tmp_path: Path) -> None:
    executable = tmp_path / "appium"
    executable.touch()
    processes: list[FakeProcess] = []

    def start(_args: list[str]) -> FakeProcess:
        process = FakeProcess()
        processes.append(process)
        return process

    manager = AppiumServiceManager(
        executable_path=executable,
        process_factory=start,
        status_probe=lambda _url, _timeout: True,
    )
    transport = FakeTransport()
    transport.barrier = threading.Barrier(1)
    pool = AppiumSessionPool(manager, transport=transport)
    lease = pool.acquire("device-1", "emulator-5554")
    original = lease.session

    processes[0].returncode = 1
    recovered = lease.session
    pool.execute(lease, "GET", "/source")
    recovered = lease.session

    assert recovered.session_id != original.session_id
    assert recovered.server.port == original.server.port
    assert recovered.system_port == original.system_port
    assert recovered.server.generation == 2
    lease.release()
