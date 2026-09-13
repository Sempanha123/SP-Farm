"""Tests for physical Android ADB discovery and operations."""

from __future__ import annotations

from pathlib import Path

from spfarm.domain.enums import DeviceHealth, DeviceProvider, DeviceState
from spfarm.infrastructure.devices.adb import AdbRunner
from spfarm.infrastructure.devices.android.provider import PhysicalAndroidProvider

PNG = b"\x89PNG\r\n\x1a\nmock"


class FakeAdb:
    def __init__(self, executable: Path) -> None:
        self.executable = executable
        self.devices = (
            "List of devices attached\n"
            "R58M1234\tdevice product:a model:Pixel_7 device:panther transport_id:1\n"
            "192.168.1.20:5555\tdevice product:b model:Galaxy_S23 device:dm1 transport_id:2\n"
            "R58LOCKED\tunauthorized transport_id:3\n"
            "R58OFFLINE\toffline transport_id:4\n"
        )
        self.calls: list[list[str]] = []

    def __call__(self, args: list[str], timeout: float) -> tuple[int, bytes, bytes]:
        self.calls.append(args)
        command = args[1:]
        if command == ["devices", "-l"]:
            return 0, self.devices.encode(), b""
        serial = command[1] if command and command[0] == "-s" else ""
        tail = command[2:]
        properties = {
            "ro.product.manufacturer": "Google",
            "ro.product.model": "Pixel 7",
            "ro.build.version.release": "14",
            "ro.build.version.sdk": "34",
            "ro.product.cpu.abi": "arm64-v8a",
        }
        if tail[:2] == ["shell", "getprop"]:
            return 0, properties.get(tail[2], "").encode(), b""
        if tail == ["shell", "wm", "size"]:
            return 0, b"Physical size: 1080x2400\n", b""
        if tail == ["shell", "wm", "density"]:
            return 0, b"Physical density: 420\n", b""
        if tail == ["shell", "dumpsys", "battery"]:
            return 0, b"level: 87\n status: 2\n temperature: 315\n", b""
        if tail == ["shell", "df", "/data"]:
            return 0, b"Filesystem 1K-blocks Used Available Use% Mounted on\n/data 100 25 75 25% /data\n", b""
        if tail == ["exec-out", "screencap", "-p"]:
            return 0, PNG, b""
        if command[:1] in (["connect"], ["disconnect"]):
            return 0, f"ok {serial}".encode(), b""
        return 0, b"Success\n", b""


def _provider(tmp_path: Path) -> tuple[PhysicalAndroidProvider, FakeAdb]:
    executable = tmp_path / "adb.exe"
    executable.write_bytes(b"fake")
    fake = FakeAdb(executable)
    return PhysicalAndroidProvider(AdbRunner(executable, fake)), fake


def test_discovery_distinguishes_usb_tcp_and_access_states(tmp_path: Path) -> None:
    provider, _ = _provider(tmp_path)
    devices = provider.discover()

    assert [device.provider for device in devices] == [DeviceProvider.PHYSICAL_ANDROID] * 4
    assert devices[0].friendly_name == "Pixel 7 (USB)"
    assert devices[0].state == DeviceState.READY
    assert devices[0].health == DeviceHealth.HEALTHY
    assert devices[1].friendly_name == "Galaxy S23 (TCP)"
    assert devices[2].state == DeviceState.UNAUTHORIZED
    assert devices[2].health == DeviceHealth.WARNING
    assert devices[3].state == DeviceState.OFFLINE
    assert devices[3].health == DeviceHealth.UNHEALTHY


def test_properties_health_capabilities_and_alias(tmp_path: Path) -> None:
    provider, _ = _provider(tmp_path)
    provider.discover()
    provider.set_alias("R58M1234", "QA Pixel")

    assert provider.discover()[0].friendly_name == "QA Pixel (USB)"
    properties = provider.read_safe_properties("R58M1234")
    assert properties["connection"] == "USB"
    assert properties["android_version"] == "14"
    assert properties["display_resolution"] == "1080x2400"
    health = provider.get_health("R58M1234")
    assert health["battery_percent"] == "87"
    assert health["storage_used_percent"] == "25%"
    caps = provider.get_capabilities("R58M1234")
    assert caps.abi == "arm64-v8a"
    assert caps.android_api_level == 34
    assert caps.screen_height == 2400


def test_package_lifecycle_screenshot_and_tcp_connection(tmp_path: Path) -> None:
    provider, fake = _provider(tmp_path)
    provider.discover()
    apk = tmp_path / "app.apk"
    apk.write_bytes(b"apk")
    screenshot = tmp_path / "screen.png"

    assert provider.install_package("R58M1234", apk).success
    assert provider.uninstall_package("R58M1234", "com.example.app").success
    assert provider.launch_package("R58M1234", "com.example.app").success
    assert provider.stop_package("R58M1234", "com.example.app").success
    assert provider.restart("R58M1234").success
    assert provider.take_screenshot("R58M1234", screenshot).success
    assert screenshot.read_bytes() == PNG
    assert provider.start("192.168.1.20:5555").success
    assert provider.stop("192.168.1.20:5555").success
    assert any("install" in call for call in fake.calls)


def test_unauthorized_operations_return_actionable_failure(tmp_path: Path) -> None:
    provider, _ = _provider(tmp_path)
    provider.discover()

    result = provider.restart("R58LOCKED")
    assert not result.success
    assert result.error_code == "DEVICE_UNAUTHORIZED"
    assert "Authorize this computer" in result.message
    start_result = provider.start("R58LOCKED")
    assert not start_result.success
    assert start_result.error_code == "DEVICE_UNAUTHORIZED"

    offline_result = provider.start("R58OFFLINE")
    assert not offline_result.success
    assert offline_result.error_code == "DEVICE_OFFLINE"


def test_uncached_state_uses_serial_before_get_state(tmp_path: Path) -> None:
    provider, fake = _provider(tmp_path)

    provider.get_state("R58M1234")

    assert fake.calls[-1][1:] == ["-s", "R58M1234", "get-state"]
