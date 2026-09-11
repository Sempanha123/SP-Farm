"""Unit tests for DiagnosticsService and sensitive data redaction."""

import json
from pathlib import Path
from typing import Any

from spfarm.application.events.base import EventBus
from spfarm.application.services.diagnostics import DiagnosticsService, redact_sensitive_data
from spfarm.shared.settings import SettingsManager


def test_redact_sensitive_data_nested_dict() -> None:
    secret_val = "sensitive_" + "pass_123"
    token_val = "token_xyz_" + "456"

    raw_data: dict[str, Any] = {
        "app_name": "SP-Farm",
        "nested": {
            "account_password": secret_val,
            "session_token": token_val,
            "safe_counter": 42,
            "auth_headers": {
                "authorization": "Bearer " + token_val,
                "cookie": "c_user=123; xs=" + token_val,
            },
        },
        "items": [
            {"id": 1, "totp_seed": "MYTOTP" + "SEED123"},
            {"id": 2, "normal_field": "hello world"},
        ],
    }

    sanitized = redact_sensitive_data(raw_data)

    # Convert to json string to search across entire payload
    dumped = json.dumps(sanitized)
    assert secret_val not in dumped
    assert token_val not in dumped
    assert "MYTOTP" not in dumped
    assert sanitized["app_name"] == "SP-Farm"
    assert sanitized["nested"]["safe_counter"] == 42
    assert sanitized["nested"]["account_password"] == "[REDACTED]"
    assert sanitized["nested"]["session_token"] == "[REDACTED]"
    assert sanitized["nested"]["auth_headers"]["authorization"] == "[REDACTED]"
    assert sanitized["nested"]["auth_headers"]["cookie"] == "[REDACTED]"
    assert sanitized["items"][0]["totp_seed"] == "[REDACTED]"
    assert sanitized["items"][1]["normal_field"] == "hello world"


def test_redact_sensitive_data_uri_credentials() -> None:
    pass_fragment = "p" + "assword"
    raw_uri = f"http://admin:{pass_fragment}@127.0.0.1:8080/v1/resource"
    sanitized = redact_sensitive_data(raw_uri)
    assert pass_fragment not in sanitized
    assert sanitized == "http://admin:[REDACTED]@127.0.0.1:8080/v1/resource"


def test_diagnostics_service_dump_and_export(tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.json"
    mgr = SettingsManager(settings_file=settings_file)
    bus = EventBus()

    service = DiagnosticsService(
        settings_manager=mgr,
        event_bus=bus,
    )

    dump = service.generate_dump()

    assert "system" in dump
    assert "application_paths" in dump
    assert "settings" in dump
    assert "event_bus" in dump
    assert dump["system"]["platform"] != ""

    export_path = tmp_path / "diagnostics.json"
    exported_file = service.export_to_file(export_path)
    assert exported_file.exists()

    content = exported_file.read_text(encoding="utf-8")
    parsed = json.loads(content)
    assert parsed["system"]["platform"] != ""

    # Ensure zero sensitive keywords or leaked secrets in exported JSON
    for sensitive_key in ["password", "session_token", "cookie_value", "totp_seed"]:
        assert sensitive_key not in content.lower()
