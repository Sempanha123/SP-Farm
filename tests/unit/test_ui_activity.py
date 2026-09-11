"""Tests for ActivityCenterView live tail, batching under load, and Error Center tabs."""

from pathlib import Path

from PySide6.QtWidgets import QApplication

from spfarm.application.services.audit import AuditService
from spfarm.application.services.error_center import ErrorCenterService
from spfarm.infrastructure.logging.buffer import LogRingBuffer
from spfarm.presentation.activity.activity_view import ActivityCenterView


def test_activity_center_view_flood_batching(qapp: QApplication, tmp_path: Path) -> None:
    """Acceptance criteria: Large logs do not freeze UI."""
    buffer = LogRingBuffer(capacity=5000)
    error_center = ErrorCenterService()
    audit_service = AuditService(audit_file=tmp_path / "audit.jsonl")

    view = ActivityCenterView(
        log_buffer=buffer,
        error_center=error_center,
        audit_service=audit_service,
    )

    # 1. Simulate flood of 1,000 log records in rapid succession
    for i in range(1000):
        view.enqueue_log_entry(
            {
                "timestamp": "2026-09-12T04:00:00Z",
                "level": "INFO",
                "logger": "flood.test",
                "message": f"High throughput log event {i}",
                "correlation": {"job_id": f"job_{i % 5}"},
            }
        )

    # Assert queue buffered them without crashing or freezing
    assert len(view._pending_log_entries) == 1000

    # 2. Trigger batch flushing
    # The batch processor consumes items smoothly in chunks
    view._flush_pending_logs()
    # After first batch tick of 150 items:
    assert len(view._pending_log_entries) == 850
    assert "High throughput log event 0" in view.log_text_edit.toPlainText()

    # Flush remaining batches
    while view._pending_log_entries:
        view._flush_pending_logs()

    assert len(view._pending_log_entries) == 0
    assert view.log_text_edit.blockCount() > 50

    view.close()


def test_activity_center_error_and_audit_tabs(qapp: QApplication, tmp_path: Path) -> None:
    buffer = LogRingBuffer(capacity=100)
    error_center = ErrorCenterService()
    audit_service = AuditService(audit_file=tmp_path / "audit.jsonl")

    # Seed an error and an audit record
    error_center.record_error(
        "Connection refused to ADB",
        correlation_context={
            "job_id": "job_1",
            "environment_id": "env_1",
            "device_id": "dev_1",
            "account_id": "acc_1",
        },
    )
    audit_service.record("SETTINGS_UPDATED", actor="admin", target_type="settings", target_id="app")

    view = ActivityCenterView(
        log_buffer=buffer,
        error_center=error_center,
        audit_service=audit_service,
    )

    # Verify Error Center tab
    view.tabs.setCurrentIndex(1)
    assert view.error_list.count() == 1
    view.error_list.setCurrentRow(0)
    assert "ADB" in view.lbl_error_title.text()
    assert "job_1" in view.lbl_trace_chain.text()
    assert "dev_1" in view.lbl_trace_chain.text()

    # Verify Audit Trail tab
    view.tabs.setCurrentIndex(2)
    view.refresh_audit_trail()
    assert view.audit_table.rowCount() == 1
    assert view.audit_table.item(0, 1).text() == "SETTINGS_UPDATED"

    view.close()
