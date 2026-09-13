"""Unit tests for DeviceStateMachine verifying valid and invalid state transitions."""

from __future__ import annotations

from spfarm.domain.devices.models import RuntimeDevice
from spfarm.domain.devices.state_machine import DeviceStateMachine
from spfarm.domain.enums import DeviceProvider, DeviceState


def _make_test_device(initial_state: DeviceState) -> RuntimeDevice:
    return RuntimeDevice(
        id="dev_test_sm",
        provider=DeviceProvider.FAKE,
        provider_instance_id="sm_inst",
        friendly_name="State Machine Test Device",
        adb_target="127.0.0.1:5555",
        state=initial_state,
    )


def test_valid_forward_state_flow() -> None:
    """Validate typical lifecycle: OFFLINE -> BOOTING -> READY -> RUNNING -> COOLDOWN -> OFFLINE."""
    dev = _make_test_device(DeviceState.OFFLINE)

    # 1. OFFLINE -> BOOTING
    assert DeviceStateMachine.can_transition(dev.state, DeviceState.BOOTING)
    res = DeviceStateMachine.transition(dev, DeviceState.BOOTING, reason="Power on")
    assert res.is_success
    assert dev.state == DeviceState.BOOTING

    # 2. BOOTING -> READY
    assert DeviceStateMachine.can_transition(dev.state, DeviceState.READY)
    res = DeviceStateMachine.transition(dev, DeviceState.READY, reason="Boot finished")
    assert res.is_success
    assert dev.state == DeviceState.READY

    # 3. READY -> RUNNING
    assert DeviceStateMachine.can_transition(dev.state, DeviceState.RUNNING)
    res = DeviceStateMachine.transition(dev, DeviceState.RUNNING, reason="Job execution started")
    assert res.is_success
    assert dev.state == DeviceState.RUNNING

    # 4. RUNNING -> COOLDOWN
    assert DeviceStateMachine.can_transition(dev.state, DeviceState.COOLDOWN)
    res = DeviceStateMachine.transition(dev, DeviceState.COOLDOWN, reason="Job completed")
    assert res.is_success
    assert dev.state == DeviceState.COOLDOWN

    # 5. COOLDOWN -> READY
    assert DeviceStateMachine.can_transition(dev.state, DeviceState.READY)
    res = DeviceStateMachine.transition(dev, DeviceState.READY, reason="Cooldown expired")
    assert res.is_success
    assert dev.state == DeviceState.READY

    # 6. READY -> STOPPING
    assert DeviceStateMachine.can_transition(dev.state, DeviceState.STOPPING)
    res = DeviceStateMachine.transition(dev, DeviceState.STOPPING, reason="Shutdown requested")
    assert res.is_success
    assert dev.state == DeviceState.STOPPING

    # 7. STOPPING -> OFFLINE
    assert DeviceStateMachine.can_transition(dev.state, DeviceState.OFFLINE)
    res = DeviceStateMachine.transition(dev, DeviceState.OFFLINE, reason="Shutdown finished")
    assert res.is_success
    assert dev.state == DeviceState.OFFLINE


def test_error_state_transitions_and_recovery() -> None:
    """Devices can transition into ERROR from operational states and recover."""
    dev = _make_test_device(DeviceState.RUNNING)

    # RUNNING -> ERROR
    res = DeviceStateMachine.transition(dev, DeviceState.ERROR, reason="ADB connection lost")
    assert res.is_success
    assert dev.state == DeviceState.ERROR

    # ERROR -> READY (Recovered)
    res = DeviceStateMachine.transition(dev, DeviceState.READY, reason="ADB reconnected")
    assert res.is_success
    assert dev.state == DeviceState.READY


def test_illegal_state_transitions_rejected() -> None:
    """Illegal state jumps must fail without altering device state."""
    dev = _make_test_device(DeviceState.OFFLINE)

    # OFFLINE cannot jump directly to RUNNING without booting/ready
    assert not DeviceStateMachine.can_transition(dev.state, DeviceState.RUNNING)
    res = DeviceStateMachine.transition(dev, DeviceState.RUNNING)
    assert res.is_failure
    assert dev.state == DeviceState.OFFLINE

    # OFFLINE cannot jump directly to COOLDOWN
    assert not DeviceStateMachine.can_transition(dev.state, DeviceState.COOLDOWN)
    res = DeviceStateMachine.transition(dev, DeviceState.COOLDOWN)
    assert res.is_failure
    assert dev.state == DeviceState.OFFLINE


def test_same_state_transition_is_noop() -> None:
    """Transitioning to the current state succeeds trivially without error."""
    dev = _make_test_device(DeviceState.READY)
    res = DeviceStateMachine.transition(dev, DeviceState.READY)
    assert res.is_success
    assert dev.state == DeviceState.READY
