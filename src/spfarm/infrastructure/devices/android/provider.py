"""Physical Android device provider backed by standard ADB commands."""

from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Optional

from spfarm.domain.devices.capabilities import DeviceCapabilities
from spfarm.domain.devices.command_result import DeviceCommandResult
from spfarm.domain.devices.models import RuntimeDevice
from spfarm.domain.enums import DeviceHealth, DeviceProvider, DeviceState
from spfarm.domain.interfaces.device_provider import IDeviceProvider
from spfarm.infrastructure.devices.adb import AdbRunner


class PhysicalAndroidProvider(IDeviceProvider):
    def __init__(
        self,
        adb_runner: Optional[AdbRunner] = None,
        aliases: Optional[dict[str, str]] = None,
    ) -> None:
        self.adb_runner = adb_runner or AdbRunner()
        self._aliases = aliases or {}
        self._cached_devices: dict[str, RuntimeDevice] = {}

    @property
    def provider_type(self) -> DeviceProvider:
        return DeviceProvider.PHYSICAL_ANDROID

    @property
    def provider_name(self) -> str:
        return "Physical Android Device"

    @property
    def is_available(self) -> bool:
        return self.adb_runner.is_available

    def _run(self, serial: str, *args: str, timeout: float = 30.0) -> tuple[int, str, str]:
        return self.adb_runner.run_text(["-s", serial, *args], timeout)

    def _shell(self, serial: str, *args: str, timeout: float = 30.0) -> tuple[int, str, str]:
        return self._run(serial, "shell", *args, timeout=timeout)

    @staticmethod
    def _connection_type(serial: str) -> str:
        return "TCP" if ":" in serial else "USB"

    def _property(self, serial: str, name: str, default: str = "") -> str:
        code, output, _ = self._shell(serial, "getprop", name)
        return output.strip() if code == 0 and output.strip() else default

    def set_alias(self, serial: str, alias: str) -> None:
        clean_alias = alias.strip()
        if clean_alias:
            self._aliases[serial] = clean_alias
        else:
            self._aliases.pop(serial, None)
        if serial in self._cached_devices:
            self._cached_devices[serial].friendly_name = self._friendly_name(serial)

    def _friendly_name(self, serial: str, model: str = "Android") -> str:
        alias = self._aliases.get(serial)
        connection = self._connection_type(serial)
        return f"{alias or model} ({connection})"

    def discover(self) -> list[RuntimeDevice]:
        code, output, _ = self.adb_runner.run_text(["devices", "-l"])
        if code != 0:
            return []

        discovered: list[RuntimeDevice] = []
        for raw_line in output.splitlines()[1:]:
            line = raw_line.strip()
            if not line or "\t" not in line:
                continue
            serial, details = line.split("\t", 1)
            status, _, metadata = details.partition(" ")
            fields = dict(re.findall(r"(\w+):([^\s]+)", metadata))
            if status == "device":
                state = DeviceState.READY
                health = DeviceHealth.HEALTHY
                model = fields.get("model", "").replace("_", " ") or self._property(
                    serial, "ro.product.model", "Android"
                )
                manufacturer = self._property(serial, "ro.product.manufacturer", "Android")
                android_version = self._property(serial, "ro.build.version.release", "Unknown")
            elif status == "unauthorized":
                state = DeviceState.UNAUTHORIZED
                health = DeviceHealth.WARNING
                model = fields.get("model", "Android").replace("_", " ")
                manufacturer = "Android"
                android_version = "Unknown"
            else:
                state = DeviceState.OFFLINE
                health = DeviceHealth.UNHEALTHY
                model = fields.get("model", "Android").replace("_", " ")
                manufacturer = "Android"
                android_version = "Unknown"

            device = RuntimeDevice(
                id=f"android_{serial}",
                provider=DeviceProvider.PHYSICAL_ANDROID,
                provider_instance_id=serial,
                friendly_name=self._friendly_name(serial, model),
                adb_target=serial,
                android_version=android_version,
                manufacturer_display=manufacturer,
                model_display=model,
                state=state,
                health=health,
                capabilities=["adb", "touch", "apk_install", "screenshot"],
            )
            self._cached_devices[serial] = device
            discovered.append(device)
        return discovered

    def _require_authorized(self, serial: str) -> Optional[DeviceCommandResult]:
        state = self.get_state(serial)
        if state == DeviceState.UNAUTHORIZED:
            return DeviceCommandResult.fail(
                "Authorize this computer on the Android device, then scan again",
                "DEVICE_UNAUTHORIZED",
            )
        if state == DeviceState.OFFLINE:
            return DeviceCommandResult.fail("Device is offline", "DEVICE_OFFLINE")
        return None

    def start(self, device_id: str) -> DeviceCommandResult:
        if self._connection_type(device_id) == "USB":
            if failure := self._require_authorized(device_id):
                return failure
            return DeviceCommandResult.ok("USB device is connected")
        started = time.perf_counter()
        code, output, error = self.adb_runner.run_text(["connect", device_id])
        duration = (time.perf_counter() - started) * 1000
        if code == 0 and "failed" not in output.lower():
            return DeviceCommandResult.ok(output.strip() or "Device connected", duration_ms=duration)
        return DeviceCommandResult.fail(
            error.strip() or output.strip() or "ADB connect failed",
            "CONNECT_FAILED",
            duration_ms=duration,
        )

    def stop(self, device_id: str) -> DeviceCommandResult:
        if self._connection_type(device_id) == "USB":
            return DeviceCommandResult.fail(
                "Disconnect the USB cable to remove this device", "USB_DISCONNECT_REQUIRED"
            )
        started = time.perf_counter()
        code, output, error = self.adb_runner.run_text(["disconnect", device_id])
        duration = (time.perf_counter() - started) * 1000
        if code == 0:
            return DeviceCommandResult.ok(output.strip() or "Device disconnected", duration_ms=duration)
        return DeviceCommandResult.fail(
            error.strip() or output.strip(), "DISCONNECT_FAILED", duration_ms=duration
        )

    def restart(self, device_id: str) -> DeviceCommandResult:
        if failure := self._require_authorized(device_id):
            return failure
        started = time.perf_counter()
        code, output, error = self._run(device_id, "reboot")
        duration = (time.perf_counter() - started) * 1000
        if code == 0:
            return DeviceCommandResult.ok("Device reboot requested", duration_ms=duration)
        return DeviceCommandResult.fail(
            error.strip() or output.strip(), "REBOOT_FAILED", duration_ms=duration
        )

    def get_state(self, device_id: str) -> DeviceState:
        cached = self._cached_devices.get(device_id)
        if cached:
            return cached.state
        code, output, _ = self.adb_runner.run_text(["-s", device_id, "get-state"])
        if code == 0 and output.strip() == "device":
            return DeviceState.READY
        if "unauthorized" in output.lower():
            return DeviceState.UNAUTHORIZED
        return DeviceState.OFFLINE

    def get_adb_target(self, device_id: str) -> Optional[str]:
        return device_id

    def get_capabilities(self, device_id: str) -> DeviceCapabilities:
        if self.get_state(device_id) != DeviceState.READY:
            return DeviceCapabilities(abi="unknown", android_api_level=0)
        properties = self.read_safe_properties(device_id)
        width, height = 1080, 1920
        match = re.search(r"(\d+)x(\d+)", properties["display_resolution"])
        if match:
            width, height = int(match.group(1)), int(match.group(2))
        return DeviceCapabilities(
            supports_companion_bridge=True,
            abi=properties["abi"],
            android_api_level=int(properties["api_level"] or 0),
            screen_width=width,
            screen_height=height,
            screen_density=int(properties["dpi"] or 0),
        )

    def read_safe_properties(self, device_id: str) -> dict[str, str]:
        if self.get_state(device_id) != DeviceState.READY:
            return {
                "serial": device_id,
                "connection": self._connection_type(device_id),
                "authorization": self.get_state(device_id).value,
            }
        _, size, _ = self._shell(device_id, "wm", "size")
        _, density, _ = self._shell(device_id, "wm", "density")
        return {
            "serial": device_id,
            "connection": self._connection_type(device_id),
            "authorization": "AUTHORIZED",
            "manufacturer": self._property(device_id, "ro.product.manufacturer", "Android"),
            "model": self._property(device_id, "ro.product.model", "Android"),
            "android_version": self._property(device_id, "ro.build.version.release", "Unknown"),
            "api_level": self._property(device_id, "ro.build.version.sdk", "0"),
            "abi": self._property(device_id, "ro.product.cpu.abi", "unknown"),
            "display_resolution": size.rsplit(":", 1)[-1].strip(),
            "dpi": density.rsplit(":", 1)[-1].strip(),
        }

    def get_health(self, device_id: str) -> dict[str, str]:
        if self.get_state(device_id) != DeviceState.READY:
            return {"connection": self.get_state(device_id).value}
        _, battery, _ = self._shell(device_id, "dumpsys", "battery")
        _, storage, _ = self._shell(device_id, "df", "/data")
        battery_fields = dict(re.findall(r"^\s*(level|status|temperature):\s*(\d+)", battery, re.M))
        storage_line = next((line for line in storage.splitlines() if line.rstrip().endswith("/data")), "")
        columns = storage_line.split()
        return {
            "connection": "ONLINE",
            "transport": self._connection_type(device_id),
            "battery_percent": battery_fields.get("level", "Unknown"),
            "battery_status": battery_fields.get("status", "Unknown"),
            "battery_temperature_tenths_c": battery_fields.get("temperature", "Unknown"),
            "storage_available": columns[3] if len(columns) >= 4 else "Unknown",
            "storage_used_percent": columns[4] if len(columns) >= 5 else "Unknown",
        }

    def take_screenshot(self, device_id: str, output_path: Path) -> DeviceCommandResult:
        if failure := self._require_authorized(device_id):
            return failure
        started = time.perf_counter()
        code, error = self.adb_runner.screenshot(device_id, output_path)
        duration = (time.perf_counter() - started) * 1000
        if code == 0:
            return DeviceCommandResult.ok(
                f"Screenshot saved to {output_path.name}",
                {"path": str(output_path), "bytes": output_path.stat().st_size},
                duration,
            )
        return DeviceCommandResult.fail(error, "SCREENSHOT_FAILED", duration_ms=duration)

    def install_package(self, device_id: str, apk_path: Path) -> DeviceCommandResult:
        if failure := self._require_authorized(device_id):
            return failure
        if not apk_path.is_file():
            return DeviceCommandResult.fail(f"APK file not found: {apk_path}", "APK_NOT_FOUND")
        return self._command(device_id, ["install", "-r", str(apk_path)], "Package installed", "INSTALL_FAILED", 180)

    def uninstall_package(self, device_id: str, package_name: str) -> DeviceCommandResult:
        if failure := self._require_authorized(device_id):
            return failure
        return self._command(device_id, ["uninstall", package_name], "Package uninstalled", "UNINSTALL_FAILED")

    def launch_package(
        self, device_id: str, package_name: str, activity_name: Optional[str] = None
    ) -> DeviceCommandResult:
        if failure := self._require_authorized(device_id):
            return failure
        args = (
            ["shell", "am", "start", "-n", f"{package_name}/{activity_name}"]
            if activity_name
            else ["shell", "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"]
        )
        return self._command(device_id, args, "Package launched", "LAUNCH_FAILED")

    def stop_package(self, device_id: str, package_name: str) -> DeviceCommandResult:
        if failure := self._require_authorized(device_id):
            return failure
        return self._command(
            device_id,
            ["shell", "am", "force-stop", package_name],
            "Package stopped",
            "STOP_PACKAGE_FAILED",
        )

    def _command(
        self,
        serial: str,
        args: list[str],
        success_message: str,
        error_code: str,
        timeout: float = 30.0,
    ) -> DeviceCommandResult:
        started = time.perf_counter()
        code, output, error = self._run(serial, *args, timeout=timeout)
        duration = (time.perf_counter() - started) * 1000
        if code == 0 and "failure" not in output.lower():
            return DeviceCommandResult.ok(success_message, duration_ms=duration)
        return DeviceCommandResult.fail(
            error.strip() or output.strip() or success_message,
            error_code,
            duration_ms=duration,
        )
