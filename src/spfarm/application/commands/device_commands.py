"""CQRS commands and handlers for runtime device control."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from spfarm.application.commands.base import Command, CommandHandler
from spfarm.application.services.device_registry import DeviceRegistry
from spfarm.domain.devices.command_result import DeviceCommandResult
from spfarm.domain.devices.models import RuntimeDevice
from spfarm.shared.errors import AppError, InfrastructureError
from spfarm.shared.result import Failure, Result, Success


# -----------------------------------------------------------------------------
# Commands
# -----------------------------------------------------------------------------
@dataclass(frozen=True)
class DiscoverDevicesCommand(Command):
    """Scan and discover all available runtime devices."""

    pass


@dataclass(frozen=True)
class StartDeviceCommand(Command):
    """Power on / boot a runtime device."""

    device_id: str


@dataclass(frozen=True)
class StopDeviceCommand(Command):
    """Gracefully stop / power down a runtime device."""

    device_id: str


@dataclass(frozen=True)
class RestartDeviceCommand(Command):
    """Reboot a runtime device."""

    device_id: str


@dataclass(frozen=True)
class TakeDeviceScreenshotCommand(Command):
    """Capture a screen image from the runtime device."""

    device_id: str
    output_path: Path


@dataclass(frozen=True)
class InstallDevicePackageCommand(Command):
    """Install an APK package onto the device."""

    device_id: str
    apk_path: Path


@dataclass(frozen=True)
class LaunchDevicePackageCommand(Command):
    """Launch an application package on the device."""

    device_id: str
    package_name: str
    activity_name: Optional[str] = None


@dataclass(frozen=True)
class StopDevicePackageCommand(Command):
    """Force-stop an application package on the device."""

    device_id: str
    package_name: str


# -----------------------------------------------------------------------------
# Handlers
# -----------------------------------------------------------------------------
class DiscoverDevicesHandler(CommandHandler[DiscoverDevicesCommand, list[RuntimeDevice]]):
    def __init__(self, registry: DeviceRegistry) -> None:
        self.registry = registry

    def handle(self, command: DiscoverDevicesCommand) -> Result[list[RuntimeDevice], AppError]:
        devices = self.registry.discover_all()
        return Success(devices)


class StartDeviceHandler(CommandHandler[StartDeviceCommand, DeviceCommandResult]):
    def __init__(self, registry: DeviceRegistry) -> None:
        self.registry = registry

    def handle(self, command: StartDeviceCommand) -> Result[DeviceCommandResult, AppError]:
        res = self.registry.start_device(command.device_id)
        if res.success:
            return Success(res)
        return Failure(InfrastructureError(res.message))


class StopDeviceHandler(CommandHandler[StopDeviceCommand, DeviceCommandResult]):
    def __init__(self, registry: DeviceRegistry) -> None:
        self.registry = registry

    def handle(self, command: StopDeviceCommand) -> Result[DeviceCommandResult, AppError]:
        res = self.registry.stop_device(command.device_id)
        if res.success:
            return Success(res)
        return Failure(InfrastructureError(res.message))


class RestartDeviceHandler(CommandHandler[RestartDeviceCommand, DeviceCommandResult]):
    def __init__(self, registry: DeviceRegistry) -> None:
        self.registry = registry

    def handle(self, command: RestartDeviceCommand) -> Result[DeviceCommandResult, AppError]:
        res = self.registry.restart_device(command.device_id)
        if res.success:
            return Success(res)
        return Failure(InfrastructureError(res.message))


class TakeDeviceScreenshotHandler(CommandHandler[TakeDeviceScreenshotCommand, DeviceCommandResult]):
    def __init__(self, registry: DeviceRegistry) -> None:
        self.registry = registry

    def handle(self, command: TakeDeviceScreenshotCommand) -> Result[DeviceCommandResult, AppError]:
        res = self.registry.take_screenshot(command.device_id, command.output_path)
        if res.success:
            return Success(res)
        return Failure(InfrastructureError(res.message))


class InstallDevicePackageHandler(CommandHandler[InstallDevicePackageCommand, DeviceCommandResult]):
    def __init__(self, registry: DeviceRegistry) -> None:
        self.registry = registry

    def handle(self, command: InstallDevicePackageCommand) -> Result[DeviceCommandResult, AppError]:
        res = self.registry.install_package(command.device_id, command.apk_path)
        if res.success:
            return Success(res)
        return Failure(InfrastructureError(res.message))


class LaunchDevicePackageHandler(CommandHandler[LaunchDevicePackageCommand, DeviceCommandResult]):
    def __init__(self, registry: DeviceRegistry) -> None:
        self.registry = registry

    def handle(self, command: LaunchDevicePackageCommand) -> Result[DeviceCommandResult, AppError]:
        res = self.registry.launch_package(
            command.device_id,
            command.package_name,
            command.activity_name,
        )
        if res.success:
            return Success(res)
        return Failure(InfrastructureError(res.message))


class StopDevicePackageHandler(CommandHandler[StopDevicePackageCommand, DeviceCommandResult]):
    def __init__(self, registry: DeviceRegistry) -> None:
        self.registry = registry

    def handle(self, command: StopDevicePackageCommand) -> Result[DeviceCommandResult, AppError]:
        res = self.registry.stop_package(command.device_id, command.package_name)
        if res.success:
            return Success(res)
        return Failure(InfrastructureError(res.message))
