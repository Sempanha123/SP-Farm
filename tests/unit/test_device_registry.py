"""Unit tests for DeviceRegistry provider coordination and action routing."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from spfarm.application.events.base import EventBus
from spfarm.application.events.device_events import (
    DeviceDiscoveredEvent,
    DeviceHealthChangedEvent,
    DeviceStateChangedEvent,
)
from spfarm.application.services.audit import AuditService
from spfarm.application.services.device_registry import DeviceRegistry
from spfarm.domain.enums import DeviceHealth, DeviceProvider, DeviceState
from spfarm.infrastructure.devices.fake_provider import FakeDeviceProvider


def test_device_registry_provider_lifecycle() -> None:
    """Registering and unregistering providers operates as expected."""
    registry = DeviceRegistry()
    assert len(registry.list_providers()) == 0

    fake_prov = FakeDeviceProvider()
    registry.register_provider(fake_prov)

    assert registry.get_provider(DeviceProvider.FAKE) is fake_prov
    assert len(registry.list_providers()) == 1

    registry.unregister_provider(DeviceProvider.FAKE)
    assert registry.get_provider(DeviceProvider.FAKE) is None
    assert len(registry.list_providers()) == 0


def test_device_registry_composite_discovery_and_events() -> None:
    """Composite discovery updates registry and emits DeviceDiscoveredEvent."""
    mock_events = MagicMock(spec=EventBus)
    mock_audit = MagicMock(spec=AuditService)

    registry = DeviceRegistry(event_bus=mock_events, audit_service=mock_audit)
    fake_prov = FakeDeviceProvider()
    registry.register_provider(fake_prov)

    devices = registry.discover_all()
    assert len(devices) >= 2
    assert len(registry.get_all_devices()) == len(devices)

    # Discovered events published
    assert mock_events.publish.call_count >= 2
    event_args = [call[0][0] for call in mock_events.publish.call_args_list]
    assert any(isinstance(ev, DeviceDiscoveredEvent) for ev in event_args)


def test_device_registry_start_stop_routing_and_state_events() -> None:
    """Registry routes start/stop to provider and emits state transition events."""
    mock_events = MagicMock(spec=EventBus)
    mock_audit = MagicMock(spec=AuditService)

    registry = DeviceRegistry(event_bus=mock_events, audit_service=mock_audit)
    fake_prov = FakeDeviceProvider()
    registry.register_provider(fake_prov)
    registry.discover_all()

    dev_id = "fake_dev_01"
    dev = registry.get_device(dev_id)
    assert dev is not None
    dev.set_state(DeviceState.OFFLINE)

    # Start device
    res_start = registry.start_device(dev_id)
    assert res_start.success is True
    assert dev.state == DeviceState.READY

    # Stop device
    res_stop = registry.stop_device(dev_id)
    assert res_stop.success is True
    assert dev.state == DeviceState.OFFLINE

    # Verify audit recorded
    assert mock_audit.record.call_count >= 2


def test_device_registry_action_routing(tmp_path: Path) -> None:
    """Registry routes screenshots, restarts, and app lifecycle."""
    registry = DeviceRegistry()
    fake_prov = FakeDeviceProvider()
    registry.register_provider(fake_prov)
    registry.discover_all()

    dev_id = "fake_dev_01"

    # Screenshot
    shot_path = tmp_path / "screenshot.png"
    res_shot = registry.take_screenshot(dev_id, shot_path)
    assert res_shot.success is True
    assert shot_path.exists()

    # Restart
    res_restart = registry.restart_device(dev_id)
    assert res_restart.success is True

    # Package lifecycle
    apk_file = tmp_path / "mock.apk"
    apk_file.write_text("payload")
    res_inst = registry.install_package(dev_id, apk_file)
    assert res_inst.success is True

    res_launch = registry.launch_package(dev_id, "mock")
    assert res_launch.success is True

    res_stop_pkg = registry.stop_package(dev_id, "mock")
    assert res_stop_pkg.success is True

    res_uninst = registry.uninstall_package(dev_id, "mock")
    assert res_uninst.success is True


def test_discovery_marks_disconnected_devices_offline_and_emits_live_updates() -> None:
    mock_events = MagicMock(spec=EventBus)
    registry = DeviceRegistry(event_bus=mock_events)
    provider = FakeDeviceProvider()
    registry.register_provider(provider)
    registry.discover_all()
    removed_id = provider.discover()[0].id
    provider._devices.pop(removed_id)
    mock_events.reset_mock()

    registry.discover_all()

    disconnected = registry.get_device(removed_id)
    assert disconnected is not None
    assert disconnected.state == DeviceState.OFFLINE
    assert disconnected.health == DeviceHealth.UNHEALTHY
    events = [call.args[0] for call in mock_events.publish.call_args_list]
    assert any(isinstance(event, DeviceStateChangedEvent) for event in events)
    assert any(isinstance(event, DeviceHealthChangedEvent) for event in events)


def test_device_registry_unregistered_device_or_provider() -> None:
    """Operations against missing devices return clean failure results."""
    registry = DeviceRegistry()
    res = registry.start_device("unknown_id")
    assert res.success is False
    assert res.error_code == "NOT_FOUND"
