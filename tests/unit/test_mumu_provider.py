"""Contract and integration unit tests for MuMuProvider."""

from __future__ import annotations

import json
from pathlib import Path

from spfarm.domain.devices.capabilities import DeviceCapabilities
from spfarm.domain.enums import DeviceProvider, DeviceState
from spfarm.domain.interfaces.device_provider import IDeviceProvider
from spfarm.infrastructure.devices.adb import AdbRunner
from spfarm.infrastructure.devices.mumu.cli import MuMuManagerRunner
from spfarm.infrastructure.devices.mumu.provider import MuMuProvider

_PNG = b"\x89PNG\r\n\x1a\nmock-screen"


def _create_mocked_provider(tmp_path: Path) -> MuMuProvider:
    mock_exe = tmp_path / "MuMuManager.exe"
    mock_exe.write_text("fake binary")

    instances_payload = [
        {"index": 0, "name": "MuMuPlayer-0", "title": "MainInstance", "is_running": False, "adb_port": 16384},
        {"index": 1, "name": "MuMuPlayer-1", "title": "WorkerInstance", "is_running": True, "adb_port": 16416},
    ]

    def mock_executor(args: list[str], cwd: Path | None, timeout: float) -> tuple[int, str, str]:
        # Handle list queries
        if "api" in args and "player_state" in args and "all" in args:
            return 0, json.dumps(instances_payload), ""
        if "api" in args and "player_state" in args:
            # Check individual state
            idx = args[args.index("-v") + 1]
            return 0, "running" if idx == "1" else "stopped", ""
        return 0, "SUCCESS", ""

    runner = MuMuManagerRunner(custom_install_dir=tmp_path, process_executor=mock_executor)
    adb_exe = tmp_path / "adb.exe"
    adb_exe.write_text("fake binary")

    def mock_adb_executor(args: list[str], timeout: float) -> tuple[int, bytes, bytes]:
        return 0, _PNG, b""

    adb_runner = AdbRunner(executable_path=adb_exe, executor=mock_adb_executor)
    return MuMuProvider(runner=runner, adb_runner=adb_runner)


def test_mumu_provider_contract_compliance(tmp_path: Path) -> None:
    """MuMuProvider adheres strictly to the IDeviceProvider abstract contract."""
    provider: IDeviceProvider = _create_mocked_provider(tmp_path)
    assert isinstance(provider, IDeviceProvider)
    assert provider.provider_type == DeviceProvider.MUMU
    assert "MuMu" in provider.provider_name


def test_mumu_provider_discovery(tmp_path: Path) -> None:
    """Discovery enumerates MuMu instances with calculated adb targets."""
    provider = _create_mocked_provider(tmp_path)
    devices = provider.discover()

    assert len(devices) == 2

    # Instance 0 (Offline)
    dev0 = devices[0]
    assert dev0.provider == DeviceProvider.MUMU
    assert dev0.provider_instance_id == "0"
    assert dev0.adb_target == "127.0.0.1:16384"
    assert dev0.state == DeviceState.OFFLINE
    assert "MuMu-0" in dev0.friendly_name

    # Instance 1 (Running)
    dev1 = devices[1]
    assert dev1.provider_instance_id == "1"
    assert dev1.adb_target == "127.0.0.1:16416"
    assert dev1.state == DeviceState.READY
    assert "MuMu-1" in dev1.friendly_name

    # Capabilities
    assert "snapshots" in dev1.capabilities
    assert "proxy" in dev1.capabilities


def test_mumu_provider_lifecycle_operations(tmp_path: Path) -> None:
    """Start, stop, and restart invoke underlying runner cleanly."""
    provider = _create_mocked_provider(tmp_path)
    provider.discover()

    # Start
    res_start = provider.start("mumu_0")
    assert res_start.success is True
    assert "launched" in res_start.message

    # Stop
    res_stop = provider.stop("mumu_1")
    assert res_stop.success is True
    assert "closed" in res_stop.message

    # Restart
    res_restart = provider.restart("mumu_1")
    assert res_restart.success is True
    assert "restarted" in res_restart.message


def test_mumu_capabilities_and_safe_properties(tmp_path: Path) -> None:
    """Capabilities query and safe property inspection comply with safety rules."""
    provider = _create_mocked_provider(tmp_path)

    caps = provider.get_capabilities("mumu_1")
    assert isinstance(caps, DeviceCapabilities)
    assert caps.supports_snapshots is True
    assert caps.supports_proxy is True
    assert caps.supports_companion_bridge is True
    assert caps.screen_width == 1080
    assert caps.screen_height == 1920

    # Safe properties
    props = provider.read_safe_properties("mumu_1")
    assert props["provider"] == "MuMu"
    assert props["adb_target"] == "127.0.0.1:16416"
    assert props["manufacturer"] == "Netease"

    # STRICT SAFETY CHECK: Zero anti-detection evasion or fake IMEI rotation
    assert "fake_imei" not in props
    assert "fake_meid" not in props
    assert "fingerprint_rotation" not in props


def test_mumu_wait_boot_completed(tmp_path: Path) -> None:
    """Non-blocking boot readiness wait succeeds when emulator is running."""
    provider = _create_mocked_provider(tmp_path)
    ready = provider.wait_boot_completed("mumu_1", timeout_sec=2.0, poll_interval_sec=0.1)
    assert ready is True


def test_mumu_package_operations_and_screenshot(tmp_path: Path) -> None:
    """Package management and screenshot capture work properly."""
    provider = _create_mocked_provider(tmp_path)

    # Screenshot
    shot = tmp_path / "mumu_shot.png"
    res_shot = provider.take_screenshot("mumu_1", shot)
    assert res_shot.success is True
    assert shot.read_bytes() == _PNG

    # Package lifecycle
    apk = tmp_path / "test.apk"
    apk.write_text("payload")

    assert provider.install_package("mumu_1", apk).success is True
    assert provider.launch_package("mumu_1", "com.facebook.katana").success is True
    assert provider.stop_package("mumu_1", "com.facebook.katana").success is True
    assert provider.uninstall_package("mumu_1", "com.facebook.katana").success is True
