"""Domain events for runtime device lifecycle and operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from spfarm.application.events.base import Event


@dataclass(frozen=True)
class DeviceDiscoveredEvent(Event):
    """Emitted when a runtime device is discovered on the host system."""

    device_id: str
    provider: str
    friendly_name: str
    adb_target: str
    android_version: str


@dataclass(frozen=True)
class DeviceStateChangedEvent(Event):
    """Emitted when a device lifecycle state changes."""

    device_id: str
    old_state: str
    new_state: str
    reason: Optional[str] = None


@dataclass(frozen=True)
class DeviceHealthChangedEvent(Event):
    """Emitted when device health rating updates."""

    device_id: str
    old_health: str
    new_health: str


@dataclass(frozen=True)
class DeviceCommandExecutedEvent(Event):
    """Emitted when a provider command completes execution."""

    device_id: str
    action: str
    success: bool
    message: str
    duration_ms: float
