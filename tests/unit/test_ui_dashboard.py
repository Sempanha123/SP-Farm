"""UI tests for CuteMetricCard and DashboardView."""

from __future__ import annotations

from unittest.mock import MagicMock

from PySide6.QtWidgets import QApplication

from spfarm.application.events.base import EventBus
from spfarm.application.queries.dashboard import (
    DashboardDataDTO,
    DashboardMetricsDTO,
    DashboardQueryService,
)
from spfarm.domain.providers.models import AuditEvent
from spfarm.presentation.dashboard.dashboard_view import DashboardView
from spfarm.presentation.dashboard.metric_card import CuteMetricCard


def test_cute_metric_card(qapp: QApplication) -> None:
    card = CuteMetricCard(
        title="Active Accounts",
        value="12",
        icon="👤",
        pastel_bg="#EDF5FF",
    )
    assert card.lbl_title.text() == "Active Accounts"
    assert card.lbl_value.text() == "12"

    card.set_value(25, "20 online")
    assert card.lbl_value.text() == "25"
    assert card.lbl_extra.text() == "20 online"


def test_dashboard_view_empty_state(qapp: QApplication) -> None:
    mock_service = MagicMock(spec=DashboardQueryService)
    mock_service.get_dashboard_data.return_value = DashboardDataDTO(
        metrics=DashboardMetricsDTO(),
        is_empty_state=True,
    )

    view = DashboardView(query_service=mock_service)
    assert not view.empty_banner.isHidden()
    assert view.metric_accounts.lbl_value.text() == "0"
    assert view.metric_devices.lbl_value.text() == "0"
    assert view.metric_running.lbl_value.text() == "0"


def test_dashboard_view_populated_state(qapp: QApplication) -> None:
    mock_service = MagicMock(spec=DashboardQueryService)
    mock_service.get_dashboard_data.return_value = DashboardDataDTO(
        metrics=DashboardMetricsDTO(
            total_accounts=5,
            active_accounts=4,
            total_pages=10,
            total_devices=3,
            ready_devices=2,
            running_jobs=1,
            failed_jobs=0,
            scheduled_today=2,
            active_workers=3,
            cpu_percent=12.5,
            ram_percent=42.0,
            disk_free_gb=128.4,
            recent_errors_count=0,
        ),
        running_jobs=[{"id": "job_1", "job_type": "post", "progress": 50}],
        device_pool_summary=[{"id": "dev_1", "name": "LD-1", "provider": "LDPLAYER", "state": "READY"}],
        upcoming_schedules=[{"id": "job_2", "job_type": "Campaign Run", "scheduled_time": "15:30"}],
        recent_activity=[{
            "id": "act_1",
            "event_type": "account.added",
            "actor": "admin",
            "target": "account:acc_1",
            "timestamp": "2026-09-12T10:00:00Z",
        }],
        is_empty_state=False,
    )

    view = DashboardView(query_service=mock_service)
    assert view.empty_banner.isVisible() is False
    assert view.metric_accounts.lbl_value.text() == "5"
    assert view.metric_pages.lbl_value.text() == "10"
    assert view.metric_devices.lbl_value.text() == "3"
    assert view.metric_running.lbl_value.text() == "1"
    assert view.upcoming_list.count() == 1
    assert view.activity_list.count() == 1
    assert "128.4 GB" in view.lbl_disk_free.text()
    assert "Active Workers: 3" in view.lbl_workers.text()


def test_dashboard_view_quick_action_navigation(qapp: QApplication) -> None:
    mock_service = MagicMock(spec=DashboardQueryService)
    mock_service.get_dashboard_data.return_value = DashboardDataDTO(
        metrics=DashboardMetricsDTO(),
        is_empty_state=False,
    )

    view = DashboardView(query_service=mock_service)

    emitted_routes: list[str] = []
    view.navigate_requested.connect(lambda route: emitted_routes.append(route))

    view.btn_action_account.click()
    assert emitted_routes[-1] == "accounts"

    view.btn_action_devices.click()
    assert emitted_routes[-1] == "devices"

    view.btn_action_campaign.click()
    assert emitted_routes[-1] == "campaigns"


def test_dashboard_view_event_bus_reaction(qapp: QApplication) -> None:
    mock_service = MagicMock(spec=DashboardQueryService)
    mock_service.get_dashboard_data.return_value = DashboardDataDTO(
        metrics=DashboardMetricsDTO(),
        is_empty_state=False,
    )

    bus = EventBus()
    view = DashboardView(query_service=mock_service, event_bus=bus)
    assert view is not None

    # Initial call was made
    initial_call_count = mock_service.get_dashboard_data.call_count
    assert initial_call_count >= 1

    # Publish an event on bus
    evt = AuditEvent(
        event_type="test.event",
        actor="system",
        target_type="test",
        target_id="1",
        details={},
    )
    bus.publish(evt)

    # Allow Qt events to process singleShot timer
    qapp.processEvents()
    assert mock_service.get_dashboard_data.call_count >= initial_call_count
