"""Central DeviceRegistry managing discovery, providers, and device execution routing."""

from __future__ import annotations

import logging
import threading
from pathlib import Path
from typing import Optional

from spfarm.application.events.base import EventBus
from spfarm.application.events.device_events import (
    DeviceCommandExecutedEvent,
    DeviceDiscoveredEvent,
    DeviceStateChangedEvent,
)
from spfarm.application.services.audit import AuditService
from spfarm.domain.devices.capabilities import DeviceCapabilities
from spfarm.domain.devices.command_result import DeviceCommandResult
from spfarm.domain.devices.models import RuntimeDevice
from spfarm.domain.devices.state_machine import DeviceStateMachine
from spfarm.domain.enums import DeviceProvider, DeviceState
from spfarm.domain.interfaces.device_provider import IDeviceProvider

logger = logging.getLogger(__name__)


class DeviceRegistry:
    """Central registry and execution router across all runtime device providers."""

    def __init__(
        self,
        event_bus: Optional[EventBus] = None,
        audit_service: Optional[AuditService] = None,
    ) -> None:
        self.event_bus = event_bus
        self.audit_service = audit_service
        self._providers: dict[DeviceProvider, IDeviceProvider] = {}
        self._devices: dict[str, RuntimeDevice] = {}
        self._lock = threading.RLock()

    # -------------------------------------------------------------------------
    # Provider Registration
    # -------------------------------------------------------------------------
    def register_provider(self, provider: IDeviceProvider) -> None:
        """Register a runtime device provider."""
        with self._lock:
            self._providers[provider.provider_type] = provider
            logger.info(
                "Registered device provider: %s (%s)",
                provider.provider_name,
                provider.provider_type.value,
            )

    def unregister_provider(self, provider_type: DeviceProvider) -> None:
        """Unregister a runtime device provider."""
        with self._lock:
            if provider_type in self._providers:
                del self._providers[provider_type]
                logger.info("Unregistered device provider: %s", provider_type.value)

    def get_provider(self, provider_type: DeviceProvider) -> Optional[IDeviceProvider]:
        """Obtain provider adapter by type."""
        with self._lock:
            return self._providers.get(provider_type)

    def list_providers(self) -> list[IDeviceProvider]:
        """List all registered provider adapters."""
        with self._lock:
            return list(self._providers.values())

    # -------------------------------------------------------------------------
    # Discovery & State
    # -------------------------------------------------------------------------
    def discover_all(self) -> list[RuntimeDevice]:
        """Perform composite discovery across all registered providers."""
        all_discovered: list[RuntimeDevice] = []

        for provider in self.list_providers():
            try:
                devs = provider.discover()
                for device in devs:
                    with self._lock:
                        is_new = device.id not in self._devices
                        self._devices[device.id] = device
                    all_discovered.append(device)

                    if is_new and self.event_bus:
                        self.event_bus.publish(
                            DeviceDiscoveredEvent(
                                device_id=device.id,
                                provider=device.provider.value,
                                friendly_name=device.friendly_name,
                                adb_target=device.adb_target,
                                android_version=device.android_version,
                            )
                        )
            except Exception as e:
                logger.error(
                    "Error discovering devices for provider %s: %s",
                    provider.provider_type.value,
                    e,
                )

        return all_discovered

    def register_device(self, device: RuntimeDevice) -> None:
        """Directly register or update a runtime device in the registry."""
        with self._lock:
            self._devices[device.id] = device

    def get_device(self, device_id: str) -> Optional[RuntimeDevice]:
        """Retrieve a device by its ID."""
        with self._lock:
            return self._devices.get(device_id)

    def get_all_devices(self) -> list[RuntimeDevice]:
        """Retrieve all currently known devices."""
        with self._lock:
            return list(self._devices.values())

    def get_device_provider(self, device: RuntimeDevice) -> Optional[IDeviceProvider]:
        """Get the provider instance responsible for the specified device."""
        with self._lock:
            return self._providers.get(device.provider)

    # -------------------------------------------------------------------------
    # Command Dispatch & Lifecycle Routing
    # -------------------------------------------------------------------------
    def start_device(self, device_id: str) -> DeviceCommandResult:
        """Transition device to BOOTING and start the physical/virtual device."""
        with self._lock:
            device = self._devices.get(device_id)
            if not device:
                return DeviceCommandResult.fail(
                    f"Device '{device_id}' not found in registry", "NOT_FOUND"
                )

            provider = self._providers.get(device.provider)
            if not provider:
                return DeviceCommandResult.fail(
                    f"No provider registered for {device.provider.value}", "NO_PROVIDER"
                )

            old_state = device.state
            transition = DeviceStateMachine.transition(
                device, DeviceState.BOOTING, reason="Start requested"
            )
            if not transition.is_success:
                return DeviceCommandResult.fail(
                    f"Cannot start device from state {old_state.value}", "INVALID_STATE"
                )

        self._emit_state_change(
            device.id, old_state.value, DeviceState.BOOTING.value, "Start requested"
        )
        result = provider.start(device.provider_instance_id or device.id)

        with self._lock:
            if result.success:
                DeviceStateMachine.transition(device, DeviceState.READY, reason="Boot successful")
                final_state = DeviceState.READY
                reason = "Boot successful"
            else:
                DeviceStateMachine.transition(device, DeviceState.ERROR, reason=result.message)
                final_state = DeviceState.ERROR
                reason = result.message

        self._emit_state_change(
            device.id, DeviceState.BOOTING.value, final_state.value, reason
        )
        self._emit_command_executed(device.id, "start", result)
        return result

    def stop_device(self, device_id: str) -> DeviceCommandResult:
        """Gracefully stop device and transition to OFFLINE."""
        with self._lock:
            device = self._devices.get(device_id)
            if not device:
                return DeviceCommandResult.fail(
                    f"Device '{device_id}' not found in registry", "NOT_FOUND"
                )

            provider = self._providers.get(device.provider)
            if not provider:
                return DeviceCommandResult.fail(
                    f"No provider registered for {device.provider.value}", "NO_PROVIDER"
                )

            old_state = device.state
            transition = DeviceStateMachine.transition(
                device, DeviceState.STOPPING, reason="Stop requested"
            )
            if not transition.is_success:
                return DeviceCommandResult.fail(
                    f"Cannot stop device from state {old_state.value}", "INVALID_STATE"
                )

        self._emit_state_change(
            device.id, old_state.value, DeviceState.STOPPING.value, "Stop requested"
        )
        result = provider.stop(device.provider_instance_id or device.id)

        with self._lock:
            if result.success:
                DeviceStateMachine.transition(device, DeviceState.OFFLINE, reason="Stopped")
                final_state = DeviceState.OFFLINE
                reason = "Stopped"
            else:
                DeviceStateMachine.transition(device, DeviceState.ERROR, reason=result.message)
                final_state = DeviceState.ERROR
                reason = result.message

        self._emit_state_change(
            device.id, DeviceState.STOPPING.value, final_state.value, reason
        )
        self._emit_command_executed(device.id, "stop", result)
        return result

    def _resolve_device_provider(
        self, device_id: str
    ) -> tuple[Optional[RuntimeDevice], Optional[IDeviceProvider]]:
        with self._lock:
            device = self._devices.get(device_id)
            return device, self._providers.get(device.provider) if device else None

    @staticmethod
    def _routing_failure(
        device_id: str, device: Optional[RuntimeDevice], provider: Optional[IDeviceProvider]
    ) -> Optional[DeviceCommandResult]:
        if not device:
            return DeviceCommandResult.fail(
                f"Device '{device_id}' not found in registry", "NOT_FOUND"
            )
        if not provider:
            return DeviceCommandResult.fail(
                f"No provider registered for {device.provider.value}", "NO_PROVIDER"
            )
        return None

    def restart_device(self, device_id: str) -> DeviceCommandResult:
        """Reboot or restart the specified device."""
        device, provider = self._resolve_device_provider(device_id)
        failure = self._routing_failure(device_id, device, provider)
        if failure:
            return failure
        assert device is not None and provider is not None
        result = provider.restart(device.provider_instance_id or device.id)
        self._emit_command_executed(device.id, "restart", result)
        return result

    def take_screenshot(self, device_id: str, output_path: Path) -> DeviceCommandResult:
        """Capture screenshot on the device."""
        device, provider = self._resolve_device_provider(device_id)
        failure = self._routing_failure(device_id, device, provider)
        if failure:
            return failure
        assert device is not None and provider is not None
        result = provider.take_screenshot(device.provider_instance_id or device.id, output_path)
        self._emit_command_executed(device.id, "screenshot", result)
        return result

    def install_package(self, device_id: str, apk_path: Path) -> DeviceCommandResult:
        """Install APK package onto the device."""
        device, provider = self._resolve_device_provider(device_id)
        failure = self._routing_failure(device_id, device, provider)
        if failure:
            return failure
        assert device is not None and provider is not None
        result = provider.install_package(device.provider_instance_id or device.id, apk_path)
        self._emit_command_executed(device.id, "install_package", result)
        return result

    def uninstall_package(self, device_id: str, package_name: str) -> DeviceCommandResult:
        """Uninstall package from the device."""
        device, provider = self._resolve_device_provider(device_id)
        failure = self._routing_failure(device_id, device, provider)
        if failure:
            return failure
        assert device is not None and provider is not None
        result = provider.uninstall_package(device.provider_instance_id or device.id, package_name)
        self._emit_command_executed(device.id, "uninstall_package", result)
        return result

    def launch_package(
        self,
        device_id: str,
        package_name: str,
        activity_name: Optional[str] = None,
    ) -> DeviceCommandResult:
        """Launch package on the device."""
        device, provider = self._resolve_device_provider(device_id)
        failure = self._routing_failure(device_id, device, provider)
        if failure:
            return failure
        assert device is not None and provider is not None
        result = provider.launch_package(
            device.provider_instance_id or device.id,
            package_name,
            activity_name,
        )
        self._emit_command_executed(device.id, "launch_package", result)
        return result

    def stop_package(self, device_id: str, package_name: str) -> DeviceCommandResult:
        """Force-stop package on the device."""
        device, provider = self._resolve_device_provider(device_id)
        failure = self._routing_failure(device_id, device, provider)
        if failure:
            return failure
        assert device is not None and provider is not None
        result = provider.stop_package(device.provider_instance_id or device.id, package_name)
        self._emit_command_executed(device.id, "stop_package", result)
        return result

    def get_capabilities(self, device_id: str) -> DeviceCapabilities:
        """Retrieve hardware/software capabilities for the device."""
        device, provider = self._resolve_device_provider(device_id)
        if not device or not provider:
            return DeviceCapabilities()
        return provider.get_capabilities(device.provider_instance_id or device.id)

    # -------------------------------------------------------------------------
    # Internal Event Emitters
    # -------------------------------------------------------------------------
    def _emit_state_change(
        self, device_id: str, old_state: str, new_state: str, reason: str
    ) -> None:
        if self.event_bus:
            self.event_bus.publish(
                DeviceStateChangedEvent(
                    device_id=device_id,
                    old_state=old_state,
                    new_state=new_state,
                    reason=reason,
                )
            )
        if self.audit_service:
            self.audit_service.record(
                event_type="device.state_changed",
                target_type="device",
                target_id=device_id,
                details={"old_state": old_state, "new_state": new_state, "reason": reason},
            )

    def _emit_command_executed(
        self, device_id: str, action: str, result: DeviceCommandResult
    ) -> None:
        if self.event_bus:
            self.event_bus.publish(
                DeviceCommandExecutedEvent(
                    device_id=device_id,
                    action=action,
                    success=result.success,
                    message=result.message,
                    duration_ms=result.duration_ms,
                )
            )
        if self.audit_service:
            self.audit_service.record(
                event_type=f"device.{action}",
                target_type="device",
                target_id=device_id,
                details={"success": result.success, "message": result.message},
            )
