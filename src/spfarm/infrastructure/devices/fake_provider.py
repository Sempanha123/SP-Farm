"""In-memory FakeDeviceProvider implementing IDeviceProvider for contracts and testing."""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Optional

from spfarm.domain.devices.capabilities import DeviceCapabilities
from spfarm.domain.devices.command_result import DeviceCommandResult
from spfarm.domain.devices.models import RuntimeDevice
from spfarm.domain.enums import DeviceHealth, DeviceProvider, DeviceState
from spfarm.domain.interfaces.device_provider import IDeviceProvider

logger = logging.getLogger(__name__)

# Minimal valid 1x1 transparent PNG bytes for testing screenshots
_TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06"
    b"\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
    b"\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


class FakeDeviceProvider(IDeviceProvider):
    """In-memory simulated runtime device provider for contract testing and offline use."""

    def __init__(
        self,
        provider_type: DeviceProvider = DeviceProvider.FAKE,
        provider_name: str = "Fake Android Emulator",
    ) -> None:
        self._type = provider_type
        self._name = provider_name
        self._devices: dict[str, RuntimeDevice] = {}
        self._installed_packages: dict[str, set[str]] = {}
        self._running_packages: dict[str, set[str]] = {}
        self.should_fail_start: bool = False
        self.should_fail_install: bool = False

        # Pre-seed 2 fake devices
        self.create_synthetic_device("fake_dev_01", "Pixel 6 - Simulated (Fake)", "emulator-5554")
        self.create_synthetic_device(
            "fake_dev_02", "Galaxy S22 - Simulated (Fake)", "emulator-5556"
        )

    def create_synthetic_device(
        self,
        instance_id: str,
        friendly_name: str,
        adb_target: str,
        state: DeviceState = DeviceState.READY,
    ) -> RuntimeDevice:
        """Create and register a synthetic mock device."""
        dev = RuntimeDevice(
            id=instance_id,
            provider=self._type,
            provider_instance_id=instance_id,
            friendly_name=friendly_name,
            adb_target=adb_target,
            android_version="12",
            manufacturer_display="Google",
            model_display="Pixel Simulated",
            state=state,
            health=DeviceHealth.HEALTHY,
            capabilities=["adb", "touch", "snapshots", "proxy", "bridge", "apk_install"],
        )
        self._devices[instance_id] = dev
        self._installed_packages[instance_id] = {"com.android.settings", "com.google.android.gms"}
        self._running_packages[instance_id] = set()
        return dev

    @property
    def provider_type(self) -> DeviceProvider:
        return self._type

    @property
    def provider_name(self) -> str:
        return self._name

    def discover(self) -> list[RuntimeDevice]:
        return list(self._devices.values())

    def start(self, device_id: str) -> DeviceCommandResult:
        t0 = time.perf_counter()
        dev = self._devices.get(device_id)
        if not dev:
            return DeviceCommandResult.fail(f"Device '{device_id}' not found", "NOT_FOUND")

        if self.should_fail_start:
            return DeviceCommandResult.fail("Simulated boot failure", "BOOT_FAILED")

        dev.set_state(DeviceState.READY)
        duration = (time.perf_counter() - t0) * 1000
        return DeviceCommandResult.ok(
            f"Device {device_id} started successfully", duration_ms=duration
        )

    def stop(self, device_id: str) -> DeviceCommandResult:
        t0 = time.perf_counter()
        dev = self._devices.get(device_id)
        if not dev:
            return DeviceCommandResult.fail(f"Device '{device_id}' not found", "NOT_FOUND")

        dev.set_state(DeviceState.OFFLINE)
        self._running_packages[device_id].clear()
        duration = (time.perf_counter() - t0) * 1000
        return DeviceCommandResult.ok(f"Device {device_id} stopped", duration_ms=duration)

    def restart(self, device_id: str) -> DeviceCommandResult:
        stop_res = self.stop(device_id)
        if not stop_res.success:
            return stop_res
        return self.start(device_id)

    def get_state(self, device_id: str) -> DeviceState:
        dev = self._devices.get(device_id)
        return dev.state if dev else DeviceState.OFFLINE

    def get_adb_target(self, device_id: str) -> Optional[str]:
        dev = self._devices.get(device_id)
        return dev.adb_target if dev else None

    def get_capabilities(self, device_id: str) -> DeviceCapabilities:
        return DeviceCapabilities(
            supports_snapshots=True,
            supports_proxy=True,
            supports_headless=True,
            supports_companion_bridge=True,
            supports_touch_recording=True,
            abi="x86_64",
            android_api_level=31,
            screen_width=1080,
            screen_height=1920,
            screen_density=320,
        )

    def take_screenshot(self, device_id: str, output_path: Path) -> DeviceCommandResult:
        t0 = time.perf_counter()
        dev = self._devices.get(device_id)
        if not dev:
            return DeviceCommandResult.fail(f"Device '{device_id}' not found", "NOT_FOUND")

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(_TINY_PNG)
            duration = (time.perf_counter() - t0) * 1000
            return DeviceCommandResult.ok(
                "Screenshot captured",
                data={"path": str(output_path), "bytes": len(_TINY_PNG)},
                duration_ms=duration,
            )
        except Exception as e:
            return DeviceCommandResult.fail(f"Failed to write screenshot: {e}", "IO_ERROR")

    def install_package(self, device_id: str, apk_path: Path) -> DeviceCommandResult:
        t0 = time.perf_counter()
        dev = self._devices.get(device_id)
        if not dev:
            return DeviceCommandResult.fail(f"Device '{device_id}' not found", "NOT_FOUND")

        if self.should_fail_install:
            return DeviceCommandResult.fail("Simulated APK installation failure", "INSTALL_FAILED")

        pkg_name = apk_path.stem
        self._installed_packages[device_id].add(pkg_name)
        duration = (time.perf_counter() - t0) * 1000
        return DeviceCommandResult.ok(
            f"Package '{pkg_name}' installed",
            data={"package": pkg_name},
            duration_ms=duration,
        )

    def uninstall_package(self, device_id: str, package_name: str) -> DeviceCommandResult:
        t0 = time.perf_counter()
        dev = self._devices.get(device_id)
        if not dev:
            return DeviceCommandResult.fail(f"Device '{device_id}' not found", "NOT_FOUND")

        self._installed_packages[device_id].discard(package_name)
        self._running_packages[device_id].discard(package_name)
        duration = (time.perf_counter() - t0) * 1000
        return DeviceCommandResult.ok(f"Package '{package_name}' uninstalled", duration_ms=duration)

    def launch_package(
        self,
        device_id: str,
        package_name: str,
        activity_name: Optional[str] = None,
    ) -> DeviceCommandResult:
        t0 = time.perf_counter()
        dev = self._devices.get(device_id)
        if not dev:
            return DeviceCommandResult.fail(f"Device '{device_id}' not found", "NOT_FOUND")

        if package_name not in self._installed_packages[device_id]:
            return DeviceCommandResult.fail(
                f"Package '{package_name}' is not installed", "NOT_INSTALLED"
            )

        self._running_packages[device_id].add(package_name)
        duration = (time.perf_counter() - t0) * 1000
        return DeviceCommandResult.ok(
            f"Launched '{package_name}'",
            data={"package": package_name, "activity": activity_name},
            duration_ms=duration,
        )

    def stop_package(self, device_id: str, package_name: str) -> DeviceCommandResult:
        t0 = time.perf_counter()
        dev = self._devices.get(device_id)
        if not dev:
            return DeviceCommandResult.fail(f"Device '{device_id}' not found", "NOT_FOUND")

        self._running_packages[device_id].discard(package_name)
        duration = (time.perf_counter() - t0) * 1000
        return DeviceCommandResult.ok(f"Stopped '{package_name}'", duration_ms=duration)
