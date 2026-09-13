"""Unit tests for CQRS Device Commands and Queries."""

from __future__ import annotations

from pathlib import Path

from spfarm.application.commands.device_commands import (
    DiscoverDevicesCommand,
    DiscoverDevicesHandler,
    InstallDevicePackageCommand,
    InstallDevicePackageHandler,
    LaunchDevicePackageCommand,
    LaunchDevicePackageHandler,
    RestartDeviceCommand,
    RestartDeviceHandler,
    StartDeviceCommand,
    StartDeviceHandler,
    StopDeviceCommand,
    StopDeviceHandler,
    StopDevicePackageCommand,
    StopDevicePackageHandler,
    TakeDeviceScreenshotCommand,
    TakeDeviceScreenshotHandler,
)
from spfarm.application.queries.devices import (
    DeviceQueryService,
    ListDevicesQuery,
)
from spfarm.application.services.device_registry import DeviceRegistry
from spfarm.infrastructure.devices.fake_provider import FakeDeviceProvider


def test_device_commands_full_workflow(tmp_path: Path) -> None:
    """Validate all CQRS device command handlers against a registered provider."""
    registry = DeviceRegistry()
    fake_prov = FakeDeviceProvider()
    registry.register_provider(fake_prov)

    # 1. DiscoverDevicesHandler
    discover_h = DiscoverDevicesHandler(registry)
    res_disc = discover_h.handle(DiscoverDevicesCommand())
    assert res_disc.is_success
    assert len(res_disc.value) >= 2

    dev_id = "fake_dev_01"

    # 2. StopDeviceHandler
    stop_h = StopDeviceHandler(registry)
    res_stop = stop_h.handle(StopDeviceCommand(device_id=dev_id))
    assert res_stop.is_success

    # 3. StartDeviceHandler
    start_h = StartDeviceHandler(registry)
    res_start = start_h.handle(StartDeviceCommand(device_id=dev_id))
    assert res_start.is_success

    # 4. RestartDeviceHandler
    restart_h = RestartDeviceHandler(registry)
    res_re = restart_h.handle(RestartDeviceCommand(device_id=dev_id))
    assert res_re.is_success

    # 5. TakeDeviceScreenshotHandler
    shot_path = tmp_path / "shot.png"
    shot_h = TakeDeviceScreenshotHandler(registry)
    res_shot = shot_h.handle(TakeDeviceScreenshotCommand(device_id=dev_id, output_path=shot_path))
    assert res_shot.is_success
    assert shot_path.exists()

    # 6. Install & Launch & Stop Package Handlers
    apk_file = tmp_path / "test_app.apk"
    apk_file.write_text("payload")

    inst_h = InstallDevicePackageHandler(registry)
    assert inst_h.handle(
        InstallDevicePackageCommand(device_id=dev_id, apk_path=apk_file)
    ).is_success

    launch_h = LaunchDevicePackageHandler(registry)
    assert launch_h.handle(
        LaunchDevicePackageCommand(device_id=dev_id, package_name="test_app")
    ).is_success

    stop_pkg_h = StopDevicePackageHandler(registry)
    assert stop_pkg_h.handle(
        StopDevicePackageCommand(device_id=dev_id, package_name="test_app")
    ).is_success


def test_device_query_service_filtering() -> None:
    """DeviceQueryService correctly filters devices by provider, state, and search."""
    registry = DeviceRegistry()
    fake_prov = FakeDeviceProvider()
    registry.register_provider(fake_prov)
    registry.discover_all()

    query_svc = DeviceQueryService(registry)

    # 1. List all
    all_devs = query_svc.list_devices()
    assert len(all_devs) >= 2

    # 2. Filter by provider
    fake_devs = query_svc.list_devices(ListDevicesQuery(provider="FAKE"))
    assert len(fake_devs) == len(all_devs)

    other_devs = query_svc.list_devices(ListDevicesQuery(provider="MUMU"))
    assert len(other_devs) == 0

    # 3. Filter by search keyword
    search_devs = query_svc.list_devices(ListDevicesQuery(search="Pixel"))
    assert len(search_devs) >= 1
    assert "Pixel" in search_devs[0].friendly_name

    # 4. Detail DTO lookup
    detail = query_svc.get_device_detail("fake_dev_01")
    assert detail is not None
    assert detail.id == "fake_dev_01"
    assert detail.capabilities_detail is not None
    assert detail.capabilities_detail.supports_snapshots is True
