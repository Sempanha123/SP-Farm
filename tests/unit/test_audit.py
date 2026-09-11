"""Unit tests for AuditService, persistence, and EventBus tracking."""

import json
from pathlib import Path

from spfarm.application.events.base import EventBus
from spfarm.application.events.secret_events import SecretCopiedEvent, SecretRevealedEvent
from spfarm.application.services.audit import AuditService


def test_audit_record_and_file_persistence(tmp_path: Path) -> None:
    audit_file = tmp_path / "audit.jsonl"
    service = AuditService(audit_file=audit_file)

    secret_key = "user_" + "pass_xyz"
    service.record(
        event_type="ACCOUNT_LOGIN",
        actor="admin_user",
        target_type="account",
        target_id="acc_001",
        details={"ip": "127.0.0.1", "account_password": secret_key},
    )

    # In-memory query
    events = service.query()
    assert len(events) == 1
    evt = events[0]
    assert evt.event_type == "ACCOUNT_LOGIN"
    assert evt.actor == "admin_user"
    assert evt.target_id == "acc_001"
    # Secret must be redacted
    assert evt.details["account_password"] == "[REDACTED]"
    assert secret_key not in json.dumps(evt.details)

    # Disk file check
    assert audit_file.exists()
    disk_content = audit_file.read_text(encoding="utf-8")
    assert "ACCOUNT_LOGIN" in disk_content
    assert secret_key not in disk_content


def test_audit_event_bus_automatic_capture(tmp_path: Path) -> None:
    audit_file = tmp_path / "audit.jsonl"
    bus = EventBus()
    service = AuditService(audit_file=audit_file, event_bus=bus)

    # Publish secret revealed event on bus
    bus.publish(
        SecretRevealedEvent(secret_ref="vault://accounts/acc_1/password", actor="operator_alice")
    )
    bus.publish(
        SecretCopiedEvent(secret_ref="vault://accounts/acc_1/totp_seed", actor="operator_bob")
    )

    events = service.query()
    assert len(events) == 2

    # Newest first
    assert events[0].event_type == "SECRET_COPIED"
    assert events[0].actor == "operator_bob"
    assert events[0].target_id == "vault://accounts/acc_1/totp_seed"

    assert events[1].event_type == "SECRET_REVEALED"
    assert events[1].actor == "operator_alice"
    assert events[1].target_id == "vault://accounts/acc_1/password"
