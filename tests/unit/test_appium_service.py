"""Tests for Appium process lifecycle and restart recovery."""

from pathlib import Path
from typing import Optional

from spfarm.infrastructure.automation.appium.service import AppiumServiceManager


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
        assert self.returncode is not None
        return self.returncode


def test_appium_manager_restarts_failed_server(tmp_path: Path) -> None:
    executable = tmp_path / "appium"
    executable.touch()
    processes: list[FakeProcess] = []
    commands: list[list[str]] = []

    def start(args: list[str]) -> FakeProcess:
        commands.append(args)
        process = FakeProcess()
        processes.append(process)
        return process

    manager = AppiumServiceManager(
        executable_path=executable,
        process_factory=start,
        status_probe=lambda _url, _timeout: True,
        startup_timeout=0.1,
    )
    first = manager.start()
    processes[0].returncode = 1
    replacement = manager.ensure_running(first)

    assert replacement.port == first.port
    assert replacement.generation == 2
    assert replacement.process is processes[1]
    assert len(commands) == 2
    manager.stop_all()


def test_appium_manager_assigns_unique_ports(tmp_path: Path) -> None:
    executable = tmp_path / "appium"
    executable.touch()
    manager = AppiumServiceManager(
        executable_path=executable,
        process_factory=lambda _args: FakeProcess(),
        status_probe=lambda _url, _timeout: True,
    )

    first = manager.start()
    second = manager.start()

    assert first.port != second.port
    manager.stop_all()
