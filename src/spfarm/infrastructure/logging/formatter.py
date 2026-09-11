"""Structured JSON and human-readable logging formatters with secret redaction."""

from __future__ import annotations

import json
import logging
import traceback
from typing import Any

from spfarm.application.services.diagnostics import redact_sensitive_data
from spfarm.infrastructure.logging.context import get_log_context
from spfarm.shared.time import format_iso


class StructuredJsonFormatter(logging.Formatter):
    """Formats log records as JSON lines enriched with correlation context and redacted secrets."""

    def format(self, record: logging.LogRecord) -> str:
        # Extract base message
        msg = record.getMessage()

        # Build structured payload
        payload: dict[str, Any] = {
            "timestamp": format_iso(),
            "level": record.levelname,
            "logger": record.name,
            "message": msg,
            "source": f"{record.filename}:{record.lineno}",
        }

        # Merge active correlation context
        ctx = get_log_context()
        if ctx:
            payload["correlation"] = ctx

        # Merge custom extras if provided
        for k, v in record.__dict__.items():
            if k not in (
                "args",
                "asctime",
                "created",
                "exc_info",
                "exc_text",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "msg",
                "name",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "stack_info",
                "thread",
                "threadName",
            ):
                payload.setdefault("extra", {})[k] = v

        # Format exception if present
        if record.exc_info:
            payload["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info),
            }

        # Strict redaction pass: credentials, tokens, session cookies are scrubbed
        sanitized = redact_sensitive_data(payload)
        return json.dumps(sanitized, default=str)


class CuteConsoleFormatter(logging.Formatter):
    """Clean, readable development console formatter with correlation tags and secret redaction."""

    LEVEL_COLORS = {
        "DEBUG": "\033[90m",  # Gray
        "INFO": "\033[94m",  # Light Blue
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[95m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        msg = record.getMessage()

        # Sanitize message
        sanitized_msg = redact_sensitive_data(msg)

        ctx = get_log_context()
        corr_parts: list[str] = []
        if "job_id" in ctx:
            corr_parts.append(f"job={ctx['job_id']}")
        if "device_id" in ctx:
            corr_parts.append(f"dev={ctx['device_id']}")
        if "account_id" in ctx:
            corr_parts.append(f"acc={ctx['account_id']}")

        corr_str = f"[{' '.join(corr_parts)}] " if corr_parts else ""
        color = self.LEVEL_COLORS.get(record.levelname, "")

        time_str = format_iso().split("T")[1][:8]
        formatted = f"{color}[{time_str}] [{record.levelname:<7}]{self.RESET} {record.name}: {corr_str}{sanitized_msg}"

        if record.exc_info:
            formatted += "\n" + "".join(traceback.format_exception(*record.exc_info))

        return formatted
