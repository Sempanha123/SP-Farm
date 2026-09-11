"""Hardware and operational capabilities descriptor for runtime devices."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceCapabilities:
    """Hardware and operational capabilities descriptor for a runtime device."""

    supports_snapshots: bool = False
    supports_proxy: bool = False
    supports_headless: bool = False
    supports_companion_bridge: bool = False
    supports_touch_recording: bool = True
    abi: str = "x86_64"
    android_api_level: int = 31
    screen_width: int = 1080
    screen_height: int = 1920
    screen_density: int = 320

    @property
    def resolution_str(self) -> str:
        """Formatted display string for resolution and DPI."""
        return f"{self.screen_width}x{self.screen_height} ({self.screen_density} DPI)"
