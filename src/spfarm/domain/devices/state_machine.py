"""Runtime device state machine validating operational lifecycle transitions."""

from __future__ import annotations

import logging

from spfarm.domain.devices.models import RuntimeDevice
from spfarm.domain.enums import DeviceState
from spfarm.shared.errors import AppError, ConflictError
from spfarm.shared.result import Failure, Result, Success

logger = logging.getLogger(__name__)

VALID_TRANSITIONS: dict[DeviceState, set[DeviceState]] = {
    DeviceState.OFFLINE: {
        DeviceState.BOOTING,
        DeviceState.READY,
        DeviceState.UNAUTHORIZED,
        DeviceState.ERROR,
    },
    DeviceState.UNAUTHORIZED: {DeviceState.OFFLINE, DeviceState.READY, DeviceState.ERROR},
    DeviceState.BOOTING: {DeviceState.READY, DeviceState.ERROR, DeviceState.OFFLINE},
    DeviceState.READY: {
        DeviceState.RESERVED,
        DeviceState.RUNNING,
        DeviceState.STOPPING,
        DeviceState.OFFLINE,
        DeviceState.UNAUTHORIZED,
        DeviceState.ERROR,
    },
    DeviceState.RESERVED: {
        DeviceState.RUNNING,
        DeviceState.READY,
        DeviceState.STOPPING,
        DeviceState.ERROR,
    },
    DeviceState.RUNNING: {
        DeviceState.READY,
        DeviceState.COOLDOWN,
        DeviceState.STOPPING,
        DeviceState.ERROR,
    },
    DeviceState.COOLDOWN: {
        DeviceState.READY,
        DeviceState.STOPPING,
        DeviceState.OFFLINE,
        DeviceState.ERROR,
    },
    DeviceState.STOPPING: {DeviceState.OFFLINE, DeviceState.ERROR},
    DeviceState.ERROR: {DeviceState.OFFLINE, DeviceState.READY},
}


class DeviceStateMachine:
    """Validates and performs lifecycle state transitions on runtime devices."""

    @staticmethod
    def can_transition(current_state: DeviceState, target_state: DeviceState) -> bool:
        """Check if transition between current and target state is permitted."""
        if current_state == target_state:
            return True
        allowed = VALID_TRANSITIONS.get(current_state, set())
        return target_state in allowed

    @classmethod
    def transition(
        cls,
        device: RuntimeDevice,
        target_state: DeviceState,
        reason: str = "",
    ) -> Result[DeviceState, AppError]:
        """Attempt to transition a device to a new state."""
        current_state = device.state
        if current_state == target_state:
            return Success(target_state)

        if not cls.can_transition(current_state, target_state):
            msg = (
                f"Illegal device state transition from {current_state.value} to {target_state.value} "
                f"for device '{device.friendly_name}' ({device.id})"
            )
            if reason:
                msg += f" (reason: {reason})"
            logger.warning(msg)
            return Failure(ConflictError(msg))

        device.set_state(target_state)
        logger.info(
            "Device '%s' transitioned: %s -> %s%s",
            device.friendly_name,
            current_state.value,
            target_state.value,
            f" ({reason})" if reason else "",
        )
        return Success(target_state)
