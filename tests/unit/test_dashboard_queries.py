"""Unit tests for DashboardQueryService and system telemetry."""

from __future__ import annotations

from unittest.mock import MagicMock

from spfarm.application.queries.dashboard import (
    DashboardDataDTO,
    DashboardQueryService,
    get_system_telemetry,
)
from spfarm.domain.accounts.models import Account
from spfarm.domain.devices.models import RuntimeDevice
from spfarm.domain.enums import AccountStatus, DeviceProvider, DeviceState, JobStatus
from spfarm.domain.jobs.models import Job


def test_get_system_telemetry():
    cpu, ram, disk = get_system_telemetry()
    assert isinstance(cpu, (int, float))
    assert isinstance(ram, (int, float))
    assert isinstance(disk, (int, float))
    assert 0.0 <= ram <= 100.0
    assert disk >= 0.0


def test_dashboard_query_service_empty_uow():
    mock_uow = MagicMock()
    mock_uow.accounts.list_all.return_value = []
    mock_uow.devices.list_all.return_value = []
    mock_uow.jobs.list_all.return_value = []

    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow
    mock_uow_ctx.__exit__.return_value = None

    mock_error_center = MagicMock()
    mock_error_center.list_errors.return_value = []

    mock_audit = MagicMock()
    mock_audit.query.return_value = []

    service = DashboardQueryService(
        uow_factory=lambda: mock_uow_ctx,
        error_center=mock_error_center,
        audit_service=mock_audit,
    )

    data: DashboardDataDTO = service.get_dashboard_data()
    assert data.is_empty_state is True
    assert data.metrics.total_accounts == 0
    assert data.metrics.total_devices == 0
    assert data.metrics.running_jobs == 0
    assert data.metrics.recent_errors_count == 0
    assert len(data.running_jobs) == 0
    assert len(data.device_pool_summary) == 0


def test_dashboard_query_service_populated():
    # Account with active status
    acc1 = MagicMock(spec=Account)
    acc1.id = "acc_01"
    acc1.status = AccountStatus.ACTIVE
    acc1.pages = ["page_1", "page_2"]

    acc2 = MagicMock(spec=Account)
    acc2.id = "acc_02"
    acc2.status = AccountStatus.SUSPENDED
    acc2.pages = []

    # Devices
    dev1 = MagicMock(spec=RuntimeDevice)
    dev1.id = "dev_01"
    dev1.custom_name = "LDPlayer-1"
    dev1.provider = DeviceProvider.LDPLAYER
    dev1.state = DeviceState.READY

    dev2 = MagicMock(spec=RuntimeDevice)
    dev2.id = "dev_02"
    dev2.custom_name = "Physical-1"
    dev2.provider = DeviceProvider.PHYSICAL_ANDROID
    dev2.state = DeviceState.OFFLINE

    # Jobs
    job1 = MagicMock(spec=Job)
    job1.id = "job_01"
    job1.status = JobStatus.RUNNING
    job1.job_type = "warmup"
    job1.progress_percent = 45
    job1.account_id = "acc_01"
    job1.runtime_device_id = "dev_01"

    job2 = MagicMock(spec=Job)
    job2.id = "job_02"
    job2.status = JobStatus.FAILED
    job2.job_type = "post"

    job3 = MagicMock(spec=Job)
    job3.id = "job_03"
    job3.status = JobStatus.PENDING
    job3.job_type = "scheduled_post"
    job3.scheduled_at = "14:00"

    mock_uow = MagicMock()
    mock_uow.accounts.list_all.return_value = [acc1, acc2]
    mock_uow.devices.list_all.return_value = [dev1, dev2]
    mock_uow.jobs.list_all.return_value = [job1, job2, job3]

    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow
    mock_uow_ctx.__exit__.return_value = None

    mock_error_entry = MagicMock()
    mock_error_entry.to_dict.return_value = {"id": "err_1", "message": "Failed step"}
    mock_error_center = MagicMock()
    mock_error_center.list_errors.return_value = [mock_error_entry]

    mock_audit_event = MagicMock()
    mock_audit_event.id = "evt_1"
    mock_audit_event.event_type = "account.created"
    mock_audit_event.actor = "system"
    mock_audit_event.target_type = "account"
    mock_audit_event.target_id = "acc_01"
    mock_audit_event.timestamp = "2026-09-12T05:00:00Z"
    mock_audit = MagicMock()
    mock_audit.query.return_value = [mock_audit_event]

    service = DashboardQueryService(
        uow_factory=lambda: mock_uow_ctx,
        error_center=mock_error_center,
        audit_service=mock_audit,
    )

    data = service.get_dashboard_data()
    assert data.is_empty_state is False
    assert data.metrics.total_accounts == 2
    assert data.metrics.active_accounts == 1
    assert data.metrics.total_pages == 2
    assert data.metrics.total_devices == 2
    assert data.metrics.ready_devices == 1
    assert data.metrics.running_jobs == 1
    assert data.metrics.failed_jobs == 1
    assert data.metrics.scheduled_today == 1
    assert data.metrics.recent_errors_count == 1
    assert len(data.running_jobs) == 1
    assert len(data.device_pool_summary) == 2
    assert len(data.upcoming_schedules) == 1
    assert len(data.recent_activity) == 1
