"""Contract tests verifying IDeviceProvider implementations against the provider contract."""

from __future__ import annotations

from pathlib import Path

from spfarm.domain.devices.capabilities import DeviceCapabilities
from spfarm.domain.enums import DeviceProvider, DeviceState
from spfarm.domain.interfaces.device_provider import IDeviceProvider
from spfarm.infrastructure.devices.fake_provider import FakeDeviceProvider


def test_fake_provider_satisfies_contract_interface() -> None:
    """Verify FakeDeviceProvider inherits and implements all IDeviceProvider methods."""
    provider: IDeviceProvider = FakeDeviceProvider()
    assert isinstance(provider, IDeviceProvider)
    assert provider.provider_type == DeviceProvider.FAKE
    assert "Simulated" in provider.provider_name or "Fake" in provider.provider_name


def test_fake_provider_discovery() -> None:
    """Discovery returns a non-empty list of RuntimeDevice instances."""
    provider = FakeDeviceProvider()
    devices = provider.discover()
    assert len(devices) >= 2

    dev1 = devices[0]
    assert dev1.provider == DeviceProvider.FAKE
    assert dev1.id.startswith("fake_dev_")
    assert dev1.adb_target.startswith("emulator-")
    assert dev1.state == DeviceState.READY


def test_fake_provider_lifecycle_power_states() -> None:
    """Test start, stop, and restart operations on a device."""
    provider = FakeDeviceProvider()
    dev_id = "fake_dev_01"

    # Stop device
    res_stop = provider.stop(dev_id)
    assert res_stop.success is True
    assert provider.get_state(dev_id) == DeviceState.OFFLINE

    # Start device
    res_start = provider.start(dev_id)
    assert res_start.success is True
    assert provider.get_state(dev_id) == DeviceState.READY

    # Restart device
    res_restart = provider.restart(dev_id)
    assert res_restart.success is True
    assert provider.get_state(dev_id) == DeviceState.READY


def test_fake_provider_capabilities_and_adb_target() -> None:
    """Capabilities and ADB target queries return expected values."""
    provider = FakeDeviceProvider()
    dev_id = "fake_dev_01"

    target = provider.get_adb_target(dev_id)
    assert target == "emulator-5554"

    caps = provider.get_capabilities(dev_id)
    assert isinstance(caps, DeviceCapabilities)
    assert caps.supports_snapshots is True
    assert caps.supports_proxy is True
    assert caps.supports_companion_bridge is True
    assert caps.screen_width == 1080
    assert caps.screen_height == 1920
    assert "1080x1920" in caps.resolution_str


def test_fake_provider_take_screenshot(tmp_path: Path) -> None:
    """Screenshot capture writes a valid PNG file to the given path."""
    provider = FakeDeviceProvider()
    dev_id = "fake_dev_01"
    output_png = tmp_path / "test_screen.png"

    res = provider.take_screenshot(dev_id, output_png)
    assert res.success is True
    assert output_png.exists()
    assert output_png.stat().st_size > 0
    # Check PNG magic bytes
    bytes_data = output_png.read_bytes()
    assert bytes_data[:4] == b"\x89PNG"


def test_fake_provider_package_lifecycle(tmp_path: Path) -> None:
    """Test APK install, launch, stop, and uninstall workflows."""
    provider = FakeDeviceProvider()
    dev_id = "fake_dev_01"

    # Mock APK file
    mock_apk = tmp_path / "com.facebook.katana.apk"
    mock_apk.write_text("dummy apk binary payload")

    # Install
    res_install = provider.install_package(dev_id, mock_apk)
    assert res_install.success is True

    # Launch
    res_launch = provider.launch_package(dev_id, "com.facebook.katana", "LoginActivity")
    assert res_launch.success is True

    # Stop package
    res_stop_pkg = provider.stop_package(dev_id, "com.facebook.katana")
    assert res_stop_pkg.success is True

    # Uninstall package
    res_uninstall = provider.uninstall_package(dev_id, "com.facebook.katana")
    assert res_uninstall.success is True


def test_fake_provider_simulated_failures(tmp_path: Path) -> None:
    """Provider properly reports structured errors when simulated failures are active."""
    provider = FakeDeviceProvider()
    dev_id = "fake_dev_01"

    provider.should_fail_start = True
    res_start = provider.start(dev_id)
    assert res_start.success is False
    assert res_start.error_code == "BOOT_FAILED"

    provider.should_fail_install = True
    apk = tmp_path / "app.apk"
    apk.write_text("mock")
    res_inst = provider.install_package(dev_id, apk)
    assert res_inst.success is False
    assert res_inst.error_code == "INSTALL_FAILED"


def test_unknown_device_operations_return_failure() -> None:
    """Operations against non-existent devices return failure result."""
    provider = FakeDeviceProvider()
    res = provider.start("non_existent_device_id")
    assert res.success is False
    assert res.error_code == "NOT_FOUND"
