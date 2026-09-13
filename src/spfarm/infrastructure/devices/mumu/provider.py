"""Production MuMu Player device provider implementing IDeviceProvider."""

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
from spfarm.infrastructure.devices.adb import AdbRunner
from spfarm.infrastructure.devices.mumu.cli import MuMuManagerRunner

logger = logging.getLogger(__name__)


class MuMuProvider(IDeviceProvider):
    """Adapter managing MuMu Player 12 / X emulator instances via MuMuManager."""

    def __init__(
        self,
        runner: Optional[MuMuManagerRunner] = None,
        custom_install_dir: Optional[Path] = None,
        adb_runner: Optional[AdbRunner] = None,
    ) -> None:
        self.runner = runner or MuMuManagerRunner(custom_install_dir=custom_install_dir)
        self.adb_runner = adb_runner or AdbRunner()
        self._cached_devices: dict[str, RuntimeDevice] = {}

    @property
    def provider_type(self) -> DeviceProvider:
        return DeviceProvider.MUMU

    @property
    def provider_name(self) -> str:
        return "MuMu Player Android Emulator"

    @property
    def is_available(self) -> bool:
        """Indicates whether MuMu Player is detected on the operating system."""
        return self.runner.is_available

    def _resolve_index(self, device_id: str) -> int:
        """Extract index from device ID (e.g. 'mumu_0' -> 0)."""
        if device_id in self._cached_devices:
            dev = self._cached_devices[device_id]
            try:
                return int(dev.provider_instance_id)
            except ValueError:
                pass

        clean = device_id.lower().replace("mumu-", "").replace("mumu_", "")
        try:
            return int(clean)
        except ValueError:
            return 0

    # -------------------------------------------------------------------------
    # IDeviceProvider Implementation
    # -------------------------------------------------------------------------
    def discover(self) -> list[RuntimeDevice]:
        """Discover all created MuMu Player emulator instances."""
        if not self.runner.is_available:
            logger.debug("MuMu Player not found on system; discovery returning empty list")
            return []

        instances = self.runner.list_instances()
        discovered: list[RuntimeDevice] = []

        for inst in instances:
            dev_id = f"mumu_{inst.index}"
            state = DeviceState.READY if inst.is_running else DeviceState.OFFLINE
            title_display = inst.title if inst.title else f"Instance-{inst.index}"

            dev = RuntimeDevice(
                id=dev_id,
                provider=self.provider_type,
                provider_instance_id=str(inst.index),
                friendly_name=f"MuMu-{inst.index} ({title_display})",
                adb_target=inst.adb_target,
                android_version="12.0",
                manufacturer_display="Netease",
                model_display="MuMu 12",
                state=state,
                health=DeviceHealth.HEALTHY,
                capabilities=[
                    "adb",
                    "touch",
                    "snapshots",
                    "proxy",
                    "bridge",
                    "apk_install",
                ],
            )
            self._cached_devices[dev_id] = dev
            discovered.append(dev)

        return discovered

    def start(self, device_id: str) -> DeviceCommandResult:
        t0 = time.perf_counter()
        idx = self._resolve_index(device_id)

        code, out, err = self.runner.launch(idx)
        duration = (time.perf_counter() - t0) * 1000

        if code == 0:
            if device_id in self._cached_devices:
                self._cached_devices[device_id].set_state(DeviceState.READY)
            return DeviceCommandResult.ok(
                f"MuMu instance {idx} launched",
                data={"index": idx, "output": out},
                duration_ms=duration,
            )
        return DeviceCommandResult.fail(
            f"Failed to launch MuMu instance {idx}: {err or out}",
            error_code="LAUNCH_FAILED",
            duration_ms=duration,
        )

    def stop(self, device_id: str) -> DeviceCommandResult:
        t0 = time.perf_counter()
        idx = self._resolve_index(device_id)

        code, out, err = self.runner.close(idx)
        duration = (time.perf_counter() - t0) * 1000

        if code == 0:
            if device_id in self._cached_devices:
                self._cached_devices[device_id].set_state(DeviceState.OFFLINE)
            return DeviceCommandResult.ok(
                f"MuMu instance {idx} closed",
                data={"index": idx, "output": out},
                duration_ms=duration,
            )
        return DeviceCommandResult.fail(
            f"Failed to close MuMu instance {idx}: {err or out}",
            error_code="CLOSE_FAILED",
            duration_ms=duration,
        )

    def restart(self, device_id: str) -> DeviceCommandResult:
        t0 = time.perf_counter()
        idx = self._resolve_index(device_id)

        code, out, err = self.runner.restart(idx)
        duration = (time.perf_counter() - t0) * 1000

        if code == 0:
            return DeviceCommandResult.ok(
                f"MuMu instance {idx} restarted",
                data={"index": idx, "output": out},
                duration_ms=duration,
            )
        return DeviceCommandResult.fail(
            f"Failed to restart MuMu instance {idx}: {err or out}",
            error_code="RESTART_FAILED",
            duration_ms=duration,
        )

    def get_state(self, device_id: str) -> DeviceState:
        idx = self._resolve_index(device_id)
        if self.runner.is_running(idx):
            return DeviceState.READY
        return DeviceState.OFFLINE

    def get_adb_target(self, device_id: str) -> Optional[str]:
        idx = self._resolve_index(device_id)
        return f"127.0.0.1:{16384 + (idx * 32)}"

    def get_capabilities(self, device_id: str) -> DeviceCapabilities:
        return DeviceCapabilities(
            supports_snapshots=True,
            supports_proxy=True,
            supports_headless=False,
            supports_companion_bridge=True,
            supports_touch_recording=True,
            abi="x86_64",
            android_api_level=31,
            screen_width=1080,
            screen_height=1920,
            screen_density=320,
        )

    def wait_boot_completed(
        self,
        device_id: str,
        timeout_sec: float = 60.0,
        poll_interval_sec: float = 1.0,
    ) -> bool:
        """Poll non-blockingly until MuMu instance is running."""
        idx = self._resolve_index(device_id)
        t_deadline = time.time() + timeout_sec

        while time.time() < t_deadline:
            if self.runner.is_running(idx):
                return True
            time.sleep(poll_interval_sec)

        return False

    def read_safe_properties(self, device_id: str) -> dict[str, str]:
        """Read standard MuMu emulator metadata without anti-detection evasion."""
        idx = self._resolve_index(device_id)
        return {
            "provider": "MuMu",
            "instance_index": str(idx),
            "adb_target": self.get_adb_target(device_id) or "",
            "manufacturer": "Netease",
            "model": "MuMu 12",
            "android_version": "12.0",
            "display_resolution": "1080x1920",
            "dpi": "320",
        }

    def take_screenshot(self, device_id: str, output_path: Path) -> DeviceCommandResult:
        t0 = time.perf_counter()
        target = self.get_adb_target(device_id)
        if not target:
            return DeviceCommandResult.fail("Device has no ADB target", "ADB_TARGET_MISSING")

        code, error = self.adb_runner.screenshot(target, output_path)
        duration = (time.perf_counter() - t0) * 1000
        if code != 0:
            return DeviceCommandResult.fail(
                f"Failed to capture screenshot: {error}",
                "SCREENSHOT_FAILED",
                duration_ms=duration,
            )
        return DeviceCommandResult.ok(
            f"Screenshot saved to {output_path.name}",
            data={"path": str(output_path), "bytes": output_path.stat().st_size},
            duration_ms=duration,
        )

    def install_package(self, device_id: str, apk_path: Path) -> DeviceCommandResult:
        t0 = time.perf_counter()
        idx = self._resolve_index(device_id)

        code, out, err = self.runner.install_app(idx, apk_path)
        duration = (time.perf_counter() - t0) * 1000

        if code == 0:
            return DeviceCommandResult.ok(
                f"Installed '{apk_path.name}' on MuMu-{idx}",
                data={"package": apk_path.stem},
                duration_ms=duration,
            )
        return DeviceCommandResult.fail(
            f"Failed to install package: {err or out}",
            error_code="INSTALL_FAILED",
            duration_ms=duration,
        )

    def uninstall_package(self, device_id: str, package_name: str) -> DeviceCommandResult:
        t0 = time.perf_counter()
        idx = self._resolve_index(device_id)

        code, out, err = self.runner.uninstall_app(idx, package_name)
        duration = (time.perf_counter() - t0) * 1000

        if code == 0:
            return DeviceCommandResult.ok(
                f"Uninstalled '{package_name}' from MuMu-{idx}",
                duration_ms=duration,
            )
        return DeviceCommandResult.fail(
            f"Failed to uninstall package: {err or out}",
            error_code="UNINSTALL_FAILED",
            duration_ms=duration,
        )

    def launch_package(
        self,
        device_id: str,
        package_name: str,
        activity_name: Optional[str] = None,
    ) -> DeviceCommandResult:
        t0 = time.perf_counter()
        idx = self._resolve_index(device_id)

        code, out, err = self.runner.run_app(idx, package_name)
        duration = (time.perf_counter() - t0) * 1000

        if code == 0:
            return DeviceCommandResult.ok(
                f"Launched '{package_name}' on MuMu-{idx}",
                data={"package": package_name, "activity": activity_name},
                duration_ms=duration,
            )
        return DeviceCommandResult.fail(
            f"Failed to launch package: {err or out}",
            error_code="LAUNCH_APP_FAILED",
            duration_ms=duration,
        )

    def stop_package(self, device_id: str, package_name: str) -> DeviceCommandResult:
        t0 = time.perf_counter()
        idx = self._resolve_index(device_id)

        code, out, err = self.runner.stop_app(idx, package_name)
        duration = (time.perf_counter() - t0) * 1000

        if code == 0:
            return DeviceCommandResult.ok(
                f"Stopped '{package_name}' on MuMu-{idx}",
                duration_ms=duration,
            )
        return DeviceCommandResult.fail(
            f"Failed to stop package: {err or out}",
            error_code="STOP_APP_FAILED",
            duration_ms=duration,
        )
