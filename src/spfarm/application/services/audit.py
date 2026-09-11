"""Audit logging service for tracking security operations and operator actions."""

from __future__ import annotations

import json
import logging
import threading
from pathlib import Path
from typing import Any, Optional

from spfarm.application.events.base import EventBus
from spfarm.application.events.secret_events import (
    SecretCopiedEvent,
    SecretDeletedEvent,
    SecretRevealedEvent,
    SecretStoredEvent,
)
from spfarm.application.services.diagnostics import redact_sensitive_data
from spfarm.domain.providers.models import AuditEvent
from spfarm.shared.paths import paths

logger = logging.getLogger(__name__)


class AuditService:
    """Service for capturing, persisting, and querying immutable audit trails."""

    def __init__(
        self,
        audit_file: Optional[Path] = None,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self._audit_file = audit_file or (paths.logs_dir / "audit.jsonl")
        self._lock = threading.RLock()
        self._in_memory_events: list[AuditEvent] = []
        self._max_in_memory = 2000

        # Load existing entries from disk if file exists
        self._load_from_disk()

        # Connect to EventBus for automatic capture of secret access events
        if event_bus is not None:
            self._subscribe_events(event_bus)

    def _subscribe_events(self, bus: EventBus) -> None:
        bus.subscribe(
            SecretRevealedEvent,
            lambda e: self.record(
                event_type="SECRET_REVEALED",
                actor=e.actor,
                target_type="secret",
                target_id=e.secret_ref,
            ),
        )
        bus.subscribe(
            SecretCopiedEvent,
            lambda e: self.record(
                event_type="SECRET_COPIED",
                actor=e.actor,
                target_type="secret",
                target_id=e.secret_ref,
            ),
        )
        bus.subscribe(
            SecretStoredEvent,
            lambda e: self.record(
                event_type="SECRET_STORED",
                actor=e.actor,
                target_type="secret",
                target_id=e.secret_ref,
            ),
        )
        bus.subscribe(
            SecretDeletedEvent,
            lambda e: self.record(
                event_type="SECRET_DELETED",
                actor=e.actor,
                target_type="secret",
                target_id=e.secret_ref,
            ),
        )

    def _load_from_disk(self) -> None:
        if not self._audit_file.exists():
            return
        try:
            with open(self._audit_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        event = AuditEvent(
                            id=data["id"],
                            event_type=data["event_type"],
                            actor=data.get("actor", "SYSTEM"),
                            target_type=data.get("target_type", ""),
                            target_id=data.get("target_id", ""),
                            details=data.get("details", {}),
                            timestamp=data.get("timestamp", ""),
                        )
                        self._in_memory_events.append(event)
                    except Exception:
                        pass
        except Exception as exc:
            logger.warning("Could not read audit log file: %s", exc)

    def record(
        self,
        event_type: str,
        actor: str = "operator",
        target_type: str = "",
        target_id: str = "",
        details: Optional[dict[str, Any]] = None,
    ) -> AuditEvent:
        """Record an audited action with automatic secret scrubbing and persistent disk append."""
        with self._lock:
            clean_details = redact_sensitive_data(details or {})
            event = AuditEvent(
                event_type=event_type,
                actor=actor,
                target_type=target_type,
                target_id=target_id,
                details=clean_details,
            )

            self._in_memory_events.append(event)
            if len(self._in_memory_events) > self._max_in_memory:
                self._in_memory_events = self._in_memory_events[-self._max_in_memory :]

            # Persist to disk
            try:
                self._audit_file.parent.mkdir(parents=True, exist_ok=True)
                payload = {
                    "id": event.id,
                    "event_type": event.event_type,
                    "actor": event.actor,
                    "target_type": event.target_type,
                    "target_id": event.target_id,
                    "details": event.details,
                    "timestamp": event.timestamp,
                }
                with open(self._audit_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(payload) + "\n")
            except Exception as exc:
                logger.error("Failed to append to audit log file: %s", exc)

            return event

    def query(
        self,
        event_type: Optional[str] = None,
        actor: Optional[str] = None,
        target_type: Optional[str] = None,
        target_id: Optional[str] = None,
        limit: int = 100,
    ) -> list[AuditEvent]:
        """Query audit log entries with flexible filtering, ordered newest first."""
        with self._lock:
            results: list[AuditEvent] = []
            for item in reversed(self._in_memory_events):
                if event_type and item.event_type != event_type:
                    continue
                if actor and item.actor != actor:
                    continue
                if target_type and item.target_type != target_type:
                    continue
                if target_id and item.target_id != target_id:
                    continue

                results.append(item)
                if len(results) >= limit:
                    break

            return results
