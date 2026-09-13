"""Domain devices package."""

from spfarm.domain.devices.capabilities import DeviceCapabilities
from spfarm.domain.devices.command_result import DeviceCommandResult
from spfarm.domain.devices.models import (
    DeviceLease,
    RuntimeDevice,
    RuntimeHistoryRecord,
)
from spfarm.domain.devices.state_machine import VALID_TRANSITIONS, DeviceStateMachine

__all__ = [
    "DeviceCapabilities",
    "DeviceCommandResult",
    "DeviceLease",
    "DeviceStateMachine",
    "RuntimeDevice",
    "RuntimeHistoryRecord",
    "VALID_TRANSITIONS",
]
