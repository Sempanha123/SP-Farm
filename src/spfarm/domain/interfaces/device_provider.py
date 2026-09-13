"""Generic DeviceProvider interface defining runtime device adapter contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from spfarm.domain.devices.capabilities import DeviceCapabilities
from spfarm.domain.devices.command_result import DeviceCommandResult
from spfarm.domain.devices.models import RuntimeDevice
from spfarm.domain.enums import DeviceProvider, DeviceState


class IDeviceProvider(ABC):
    """Abstract interface for all hardware and emulator runtime device providers."""

    @property
    @abstractmethod
    def provider_type(self) -> DeviceProvider:
        """The enumerated provider type (e.g. LDPLAYER, MUMU, PHYSICAL_ANDROID, FAKE)."""
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable provider display title."""
        ...

    @abstractmethod
    def discover(self) -> list[RuntimeDevice]:
        """Discover all locally accessible or configured devices under this provider."""
        ...

    @abstractmethod
    def start(self, device_id: str) -> DeviceCommandResult:
        """Boot or power on the specified device."""
        ...

    @abstractmethod
    def stop(self, device_id: str) -> DeviceCommandResult:
        """Gracefully power off or terminate the specified device."""
        ...

    @abstractmethod
    def restart(self, device_id: str) -> DeviceCommandResult:
        """Reboot or restart the specified device."""
        ...

    @abstractmethod
    def get_state(self, device_id: str) -> DeviceState:
        """Query the current live state of the specified device."""
        ...

    @abstractmethod
    def get_adb_target(self, device_id: str) -> Optional[str]:
        """Obtain the ADB connection target (e.g. '127.0.0.1:5555' or USB serial)."""
        ...

    @abstractmethod
    def get_capabilities(self, device_id: str) -> DeviceCapabilities:
        """Retrieve hardware and operational capabilities for the device."""
        ...

    @abstractmethod
    def take_screenshot(self, device_id: str, output_path: Path) -> DeviceCommandResult:
        """Capture screen image and save to the specified file path."""
        ...

    @abstractmethod
    def install_package(self, device_id: str, apk_path: Path) -> DeviceCommandResult:
        """Install an Android APK file onto the device."""
        ...

    @abstractmethod
    def uninstall_package(self, device_id: str, package_name: str) -> DeviceCommandResult:
        """Uninstall an Android package from the device."""
        ...

    @abstractmethod
    def launch_package(
        self,
        device_id: str,
        package_name: str,
        activity_name: Optional[str] = None,
    ) -> DeviceCommandResult:
        """Launch an Android application package on the device."""
        ...

    @abstractmethod
    def stop_package(self, device_id: str, package_name: str) -> DeviceCommandResult:
        """Force-stop a running application package on the device."""
        ...
