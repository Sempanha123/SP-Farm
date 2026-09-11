"""Unit tests for structured logging, correlation context, and retention cleanup."""

import json
import logging
import time
from pathlib import Path

from spfarm.infrastructure.logging.buffer import LogRingBuffer
from spfarm.infrastructure.logging.context import (
    clear_log_context,
    get_log_context,
    log_context,
)
from spfarm.infrastructure.logging.formatter import StructuredJsonFormatter
from spfarm.infrastructure.logging.setup import cleanup_old_logs, configure_logging


def test_log_context_propagation_and_nesting() -> None:
    clear_log_context()
    assert get_log_context() == {}

    with log_context(job_id="job-101", account_id="acc-202"):
        ctx1 = get_log_context()
        assert ctx1["job_id"] == "job-101"
        assert ctx1["account_id"] == "acc-202"
        assert "correlation_id" in ctx1

        # Nested context override
        with log_context(device_id="dev-303", account_id="acc-overridden"):
            ctx2 = get_log_context()
            assert ctx2["job_id"] == "job-101"
            assert ctx2["device_id"] == "dev-303"
            assert ctx2["account_id"] == "acc-overridden"

        # Restores previous values
        ctx3 = get_log_context()
        assert ctx3["account_id"] == "acc-202"
        assert "device_id" not in ctx3

    # Cleared on block exit
    assert get_log_context() == {}


def test_structured_json_formatter_redacts_secrets() -> None:
    formatter = StructuredJsonFormatter()
    logger = logging.getLogger("test_redact")
    secret_pass = "my_" + "password_xyz"

    record = logger.makeRecord(
        name="test_redact",
        level=logging.INFO,
        fn="test.py",
        lno=10,
        msg=f"Operator accessed http://admin:{secret_pass}@127.0.0.1:8080/api",
        args=(),
        exc_info=None,
        extra={"account_password": secret_pass, "token_payload": "token123"},
    )

    with log_context(job_id="job-99"):
        formatted = formatter.format(record)

    parsed = json.loads(formatted)
    assert parsed["level"] == "INFO"
    assert parsed["correlation"]["job_id"] == "job-99"

    # Secret redaction assertions
    assert secret_pass not in formatted
    assert parsed["extra"]["account_password"] == "[REDACTED]"
    assert parsed["extra"]["token_payload"] == "[REDACTED]"
    assert "[REDACTED]" in parsed["message"]


def test_log_ring_buffer_capacity_and_filtering() -> None:
    buf = LogRingBuffer(capacity=5)

    for i in range(10):
        level = "ERROR" if i % 2 == 0 else "INFO"
        buf.append({
            "level": level,
            "message": f"Message {i}",
            "correlation": {"job_id": f"job-{i}"},
        })

    # Buffer length is bounded to capacity
    assert len(buf) == 5

    # Retrieves newest entries
    all_entries = buf.get_entries(limit=10)
    assert len(all_entries) == 5
    assert all_entries[-1]["message"] == "Message 9"

    # Filtering by level
    errors = buf.get_entries(level="ERROR")
    assert all(e["level"] == "ERROR" for e in errors)

    # Filtering by correlation
    filtered_job = buf.get_entries(correlation_id="job-8")
    assert len(filtered_job) == 1
    assert filtered_job[0]["message"] == "Message 8"


def test_configure_logging_and_cleanup(tmp_path: Path) -> None:
    logs_dir = tmp_path / "logs"
    buffer = configure_logging(logs_dir=logs_dir, enable_console=False)

    test_logger = logging.getLogger("spfarm.test_setup")
    test_logger.info("Application starting up with correlation tracing")

    log_file = logs_dir / "spfarm.log"
    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")
    assert "Application starting up with correlation tracing" in content

    # Test in-memory buffer captured the message
    entries = buffer.get_entries(limit=10)
    assert any("Application starting up" in e.get("message", "") for e in entries)

    # Test retention cleanup
    old_log = logs_dir / "spfarm.log.2025-01-01"
    old_log.write_text("old logs", encoding="utf-8")
    # Simulate old mtime (30 days ago)
    old_time = time.time() - (30 * 86400)
    import os
    os.utime(old_log, (old_time, old_time))

    deleted = cleanup_old_logs(logs_dir=logs_dir, max_age_days=14)
    assert deleted >= 1
    assert not old_log.exists()
