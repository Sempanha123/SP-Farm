"""Error Center service for fingerprinting, deduplicating, and correlating application errors."""

from __future__ import annotations

import hashlib
import re
import threading
import traceback
from dataclasses import dataclass, field
from typing import Any, Optional

from spfarm.shared.time import format_iso

# Pattern for normalizing variable tokens in error messages (IDs, hex, numbers)
UUID_PATTERN = re.compile(
    r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}"
)
ID_PATTERN = re.compile(r"\b[a-zA-Z0-9_\-]+_\d+\b")
NUMBER_PATTERN = re.compile(r"\b\d+\b")


def compute_error_fingerprint(
    error_type: str,
    message: str,
    location: str = "",
) -> str:
    """Generate a stable deterministic SHA-256 fingerprint for grouping repeated errors.

    Normalizes UUIDs, entity IDs, and numbers so parameterized messages aggregate cleanly.
    """
    normalized_msg = UUID_PATTERN.sub("<UUID>", message)
    normalized_msg = ID_PATTERN.sub("<ID>", normalized_msg)
    normalized_msg = NUMBER_PATTERN.sub("<NUM>", normalized_msg)
    normalized_msg = normalized_msg.strip().lower()

    raw_signature = f"{error_type.strip()}:{normalized_msg}:{location.strip()}"
    return hashlib.sha256(raw_signature.encode("utf-8")).hexdigest()[:16]


@dataclass
class GroupedError:
    """Aggregated group of repeated errors sharing the same root-cause fingerprint."""

    fingerprint: str
    error_type: str
    message_template: str
    last_message: str
    count: int = 1
    first_seen_at: str = field(default_factory=format_iso)
    last_seen_at: str = field(default_factory=format_iso)
    stack_trace: str = ""
    status: str = "active"  # active, acknowledged, resolved

    # Multi-entity correlation trace: Job -> Environment -> Device -> Account
    correlated_job_ids: set[str] = field(default_factory=set)
    correlated_environment_ids: set[str] = field(default_factory=set)
    correlated_device_ids: set[str] = field(default_factory=set)
    correlated_account_ids: set[str] = field(default_factory=set)
    correlated_page_ids: set[str] = field(default_factory=set)

    def to_dict(self) -> dict[str, Any]:
        """Convert grouped error to a serializable dictionary."""
        return {
            "fingerprint": self.fingerprint,
            "error_type": self.error_type,
            "message_template": self.message_template,
            "last_message": self.last_message,
            "count": self.count,
            "first_seen_at": self.first_seen_at,
            "last_seen_at": self.last_seen_at,
            "status": self.status,
            "stack_trace": self.stack_trace,
            "correlations": {
                "jobs": sorted(list(self.correlated_job_ids)),
                "environments": sorted(list(self.correlated_environment_ids)),
                "devices": sorted(list(self.correlated_device_ids)),
                "accounts": sorted(list(self.correlated_account_ids)),
                "pages": sorted(list(self.correlated_page_ids)),
            },
        }


class ErrorCenterService:
    """Thread-safe service for aggregating, querying, and managing grouped application errors."""

    def __init__(self) -> None:
        self._errors: dict[str, GroupedError] = {}
        self._lock = threading.RLock()

    def record_error(
        self,
        exc: Exception | str,
        correlation_context: Optional[dict[str, str]] = None,
        location: str = "",
        stack_trace: Optional[str] = None,
    ) -> GroupedError:
        """Record an error instance, either updating an existing group or creating a new one."""
        with self._lock:
            if isinstance(exc, Exception):
                error_type = exc.__class__.__name__
                raw_msg = str(exc)
                if not stack_trace:
                    stack_trace = "".join(
                        traceback.format_exception(type(exc), exc, exc.__traceback__)
                    )
            else:
                error_type = "ApplicationError"
                raw_msg = str(exc)
                stack_trace = stack_trace or ""

            fingerprint = compute_error_fingerprint(error_type, raw_msg, location=location)
            now = format_iso()

            ctx = correlation_context or {}
            job_id = ctx.get("job_id")
            env_id = ctx.get("environment_id")
            dev_id = ctx.get("device_id")
            acc_id = ctx.get("account_id")
            page_id = ctx.get("page_id")

            if fingerprint in self._errors:
                existing = self._errors[fingerprint]
                existing.count += 1
                existing.last_seen_at = now
                existing.last_message = raw_msg
                if stack_trace:
                    existing.stack_trace = stack_trace

                # Re-activate if error was previously resolved
                if existing.status == "resolved":
                    existing.status = "active"

                if job_id:
                    existing.correlated_job_ids.add(job_id)
                if env_id:
                    existing.correlated_environment_ids.add(env_id)
                if dev_id:
                    existing.correlated_device_ids.add(dev_id)
                if acc_id:
                    existing.correlated_account_ids.add(acc_id)
                if page_id:
                    existing.correlated_page_ids.add(page_id)

                return existing

            new_group = GroupedError(
                fingerprint=fingerprint,
                error_type=error_type,
                message_template=raw_msg,
                last_message=raw_msg,
                first_seen_at=now,
                last_seen_at=now,
                stack_trace=stack_trace,
                status="active",
                correlated_job_ids={job_id} if job_id else set(),
                correlated_environment_ids={env_id} if env_id else set(),
                correlated_device_ids={dev_id} if dev_id else set(),
                correlated_account_ids={acc_id} if acc_id else set(),
                correlated_page_ids={page_id} if page_id else set(),
            )
            self._errors[fingerprint] = new_group
            return new_group

    def list_errors(self, status: Optional[str] = None) -> list[GroupedError]:
        """List all grouped errors, optionally filtered by status (active/acknowledged/resolved)."""
        with self._lock:
            errors = list(self._errors.values())
            if status:
                errors = [e for e in errors if e.status == status]
            # Sort by last_seen_at descending
            return sorted(errors, key=lambda e: e.last_seen_at, reverse=True)

    def get_error(self, fingerprint: str) -> GroupedError | None:
        """Retrieve a specific grouped error by fingerprint."""
        with self._lock:
            return self._errors.get(fingerprint)

    def acknowledge_error(self, fingerprint: str) -> bool:
        """Mark an error as acknowledged by the operator."""
        with self._lock:
            if fingerprint in self._errors:
                self._errors[fingerprint].status = "acknowledged"
                return True
            return False

    def resolve_error(self, fingerprint: str) -> bool:
        """Mark an error as resolved."""
        with self._lock:
            if fingerprint in self._errors:
                self._errors[fingerprint].status = "resolved"
                return True
            return False

    def trace_error(self, fingerprint: str) -> dict[str, Any] | None:
        """Trace a grouped error across Job -> Environment -> Device -> Account relationships."""
        with self._lock:
            err = self.get_error(fingerprint)
            if not err:
                return None
            return {
                "fingerprint": err.fingerprint,
                "error_type": err.error_type,
                "last_message": err.last_message,
                "count": err.count,
                "status": err.status,
                "trace_chain": {
                    "jobs": sorted(list(err.correlated_job_ids)),
                    "environments": sorted(list(err.correlated_environment_ids)),
                    "devices": sorted(list(err.correlated_device_ids)),
                    "accounts": sorted(list(err.correlated_account_ids)),
                    "pages": sorted(list(err.correlated_page_ids)),
                },
            }

    def clear(self) -> None:
        """Clear all stored errors."""
        with self._lock:
            self._errors.clear()
