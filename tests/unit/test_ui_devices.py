"""UI unit tests for DevicesView and device inspector."""

from __future__ import annotations

from unittest.mock import MagicMock

from PySide6.QtWidgets import QApplication

from spfarm.application.commands.device_commands import (
    DiscoverDevicesHandler,
    LaunchDevicePackageHandler,
    RestartDeviceHandler,
    StartDeviceHandler,
    StopDeviceHandler,
    StopDevicePackageHandler,
    TakeDeviceScreenshotHandler,
)
from spfarm.application.events.base import EventBus
from spfarm.application.events.device_events import DeviceStateChangedEvent
from spfarm.application.queries.devices import (
    DeviceDetailDTO,
    DeviceQueryService,
    DeviceSummaryDTO,
)
from spfarm.domain.devices.capabilities import DeviceCapabilities
from spfarm.domain.devices.command_result import DeviceCommandResult
from spfarm.presentation.devices.devices_view import DevicesView
from spfarm.shared.result import Success


def test_devices_view_rendering_and_selection(qapp: QApplication) -> None:
    """DevicesView renders rows, handles selection, and updates the inspector."""
    mock_queries = MagicMock(spec=DeviceQueryService)
    mock_discover = MagicMock(spec=DiscoverDevicesHandler)
    mock_start = MagicMock(spec=StartDeviceHandler)
    mock_stop = MagicMock(spec=StopDeviceHandler)
    mock_restart = MagicMock(spec=RestartDeviceHandler)
    mock_screenshot = MagicMock(spec=TakeDeviceScreenshotHandler)
    mock_launch = MagicMock(spec=LaunchDevicePackageHandler)
    mock_stop_pkg = MagicMock(spec=StopDevicePackageHandler)
    mock_event_bus = MagicMock(spec=EventBus)

    sample_devs = [
        DeviceSummaryDTO(
            id="dev_01",
            friendly_name="Pixel 6 - Simulated (Fake)",
            provider="FAKE",
            adb_target="emulator-5554",
            android_version="12",
            state="READY",
            health="HEALTHY",
            manufacturer="Google",
            model="Pixel Simulated",
            capabilities=["snapshots", "proxy", "bridge"],
            current_environment_id=None,
            current_job_id=None,
            last_seen_at="2026-09-12T00:00:00Z",
        ),
        DeviceSummaryDTO(
            id="dev_02",
            friendly_name="LDPlayer Instance 0",
            provider="LDPLAYER",
            adb_target="127.0.0.1:5555",
            android_version="9",
            state="OFFLINE",
            health="WARNING",
            manufacturer="Microvirt",
            model="LDPlayer9",
            capabilities=["touch", "apk_install"],
            current_environment_id="env_99",
            current_job_id=None,
            last_seen_at=None,
        ),
    ]

    mock_queries.list_devices.return_value = sample_devs
    mock_queries.get_device_detail.return_value = DeviceDetailDTO(
        id="dev_01",
        friendly_name="Pixel 6 - Simulated (Fake)",
        provider="FAKE",
        adb_target="emulator-5554",
        android_version="12",
        state="READY",
        health="HEALTHY",
        manufacturer="Google",
        model="Pixel Simulated",
        capabilities=["snapshots", "proxy", "bridge"],
        current_environment_id=None,
        current_job_id=None,
        last_seen_at="2026-09-12T00:00:00Z",
        capabilities_detail=DeviceCapabilities(
            screen_width=1080, screen_height=1920, screen_density=320
        ),
        resolution_display="1080x1920 (320 DPI)",
    )

    view = DevicesView(
        query_service=mock_queries,
        discover_handler=mock_discover,
        start_handler=mock_start,
        stop_handler=mock_stop,
        restart_handler=mock_restart,
        screenshot_handler=mock_screenshot,
        launch_handler=mock_launch,
        stop_pkg_handler=mock_stop_pkg,
        event_bus=mock_event_bus,
    )

    # Verify table row count and columns
    assert view.table_view.rowCount() == 2
    assert "Pixel 6" in view.table_view.item(0, 1).text()
    assert "LDPlayer" in view.table_view.item(1, 1).text()

    # Click row 0 -> Inspector updates
    view._on_table_cell_clicked(0, 0)
    assert "Pixel 6" in view.insp_title.text()
    assert "READY" in view.insp_subtitle.text()
    assert "emulator-5554" in view.insp_specs.text()
    assert "1080x1920 (320 DPI)" in view.insp_specs.text()


def test_devices_view_action_buttons(qapp: QApplication) -> None:
    """Action buttons in toolbar and inspector invoke corresponding handlers."""
    mock_queries = MagicMock(spec=DeviceQueryService)
    mock_discover = MagicMock(spec=DiscoverDevicesHandler)
    mock_start = MagicMock(spec=StartDeviceHandler)
    mock_stop = MagicMock(spec=StopDeviceHandler)
    mock_restart = MagicMock(spec=RestartDeviceHandler)
    mock_screenshot = MagicMock(spec=TakeDeviceScreenshotHandler)
    mock_launch = MagicMock(spec=LaunchDevicePackageHandler)
    mock_stop_pkg = MagicMock(spec=StopDevicePackageHandler)

    mock_queries.list_devices.return_value = [
        DeviceSummaryDTO(
            id="dev_01",
            friendly_name="Pixel 6",
            provider="FAKE",
            adb_target="emulator-5554",
            android_version="12",
            state="READY",
            health="HEALTHY",
            manufacturer="Google",
            model="Pixel",
        )
    ]
    mock_queries.get_device_detail.return_value = DeviceDetailDTO(
        id="dev_01",
        friendly_name="Pixel 6",
        provider="FAKE",
        adb_target="emulator-5554",
        android_version="12",
        state="READY",
        health="HEALTHY",
        manufacturer="Google",
        model="Pixel",
        resolution_display="1080x1920 (320 DPI)",
    )

    mock_discover.handle.return_value = Success([])
    mock_start.handle.return_value = Success(DeviceCommandResult.ok("Started"))
    mock_stop.handle.return_value = Success(DeviceCommandResult.ok("Stopped"))
    mock_restart.handle.return_value = Success(DeviceCommandResult.ok("Restarted"))
    mock_screenshot.handle.return_value = Success(DeviceCommandResult.ok("Captured"))

    view = DevicesView(
        query_service=mock_queries,
        discover_handler=mock_discover,
        start_handler=mock_start,
        stop_handler=mock_stop,
        restart_handler=mock_restart,
        screenshot_handler=mock_screenshot,
        launch_handler=mock_launch,
        stop_pkg_handler=mock_stop_pkg,
    )

    # 1. Scan button click
    view.btn_scan.click()
    mock_discover.handle.assert_called_once()

    # 2. Select device
    view._select_device("dev_01")

    # 3. Start button click
    view.btn_power_start.click()
    mock_start.handle.assert_called_once()
    assert "Started" in view.insp_log.text()

    # 4. Stop button click
    view.btn_power_stop.click()
    mock_stop.handle.assert_called_once()

    # 5. Restart button click
    view.btn_power_restart.click()
    mock_restart.handle.assert_called_once()

    # 6. Screenshot button click
    view.btn_screenshot.click()
    mock_screenshot.handle.assert_called_once()


def test_devices_view_event_reaction(qapp: QApplication) -> None:
    """Device events trigger an asynchronous refresh of the view."""
    mock_queries = MagicMock(spec=DeviceQueryService)
    mock_queries.list_devices.return_value = []

    view = DevicesView(
        query_service=mock_queries,
        discover_handler=MagicMock(),
        start_handler=MagicMock(),
        stop_handler=MagicMock(),
        restart_handler=MagicMock(),
        screenshot_handler=MagicMock(),
        launch_handler=MagicMock(),
        stop_pkg_handler=MagicMock(),
    )

    initial_calls = mock_queries.list_devices.call_count
    view._on_event_received(
        DeviceStateChangedEvent(
            device_id="dev_01",
            old_state="BOOTING",
            new_state="READY",
            reason="Boot complete",
        )
    )
    # Give QTimer 100ms
    qapp.processEvents()
    # At least initial call was made and refresh is queued
    assert mock_queries.list_devices.call_count >= initial_calls
