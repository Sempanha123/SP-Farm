"""Tests for cancellation-aware ADB execution."""

import threading
from pathlib import Path

from spfarm.infrastructure.automation.adb.service import AdbCommandOutput, AdbService
from spfarm.infrastructure.devices.adb import AdbRunner


def test_adb_service_passes_target_timeout_and_cancellation(tmp_path: Path) -> None:
    adb = tmp_path / "adb"
    adb.touch()
    seen: dict[str, object] = {}

    def execute(
        args: list[str], timeout: float, cancel_event: threading.Event
    ) -> AdbCommandOutput:
        seen.update(args=args, timeout=timeout, cancel_event=cancel_event)
        return AdbCommandOutput(returncode=0, stdout=b"ok")

    service = AdbService(AdbRunner(executable_path=adb), executor=execute)
    cancellation = threading.Event()
    output = service.run_for_device(
        "emulator-5554",
        ["shell", "getprop", "ro.build.version.release"],
        timeout=4.0,
        cancel_event=cancellation,
    )

    assert output.succeeded
    assert output.stdout_text == "ok"
    assert seen["args"] == [
        str(adb),
        "-s",
        "emulator-5554",
        "shell",
        "getprop",
        "ro.build.version.release",
    ]
    assert seen["timeout"] == 4.0
    assert seen["cancel_event"] is cancellation


def test_adb_service_returns_cancelled_without_starting_executor(tmp_path: Path) -> None:
    adb = tmp_path / "adb"
    adb.touch()
    started = False

    def execute(
        _args: list[str], _timeout: float, _cancel_event: threading.Event
    ) -> AdbCommandOutput:
        nonlocal started
        started = True
        return AdbCommandOutput(returncode=0)

    cancellation = threading.Event()
    cancellation.set()
    output = AdbService(
        AdbRunner(executable_path=adb), executor=execute
    ).run(["devices"], cancel_event=cancellation)

    assert output.cancelled
    assert not started
