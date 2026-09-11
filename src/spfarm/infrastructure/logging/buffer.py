"""Thread-safe circular ring buffer and in-memory logging handler."""

from __future__ import annotations

import contextlib
import logging
import threading
from collections import deque
from typing import Any, Callable

from spfarm.application.services.diagnostics import redact_sensitive_data
from spfarm.infrastructure.logging.context import get_log_context
from spfarm.shared.time import format_iso


class LogRingBuffer:
    """Thread-safe bounded in-memory circular buffer for real-time log tailing."""

    def __init__(self, capacity: int = 5000) -> None:
        self.capacity = capacity
        self._buffer: deque[dict[str, Any]] = deque(maxlen=capacity)
        self._lock = threading.Lock()

    def append(self, entry: dict[str, Any]) -> None:
        """Add a log entry to the buffer, dropping the oldest if capacity exceeded."""
        with self._lock:
            self._buffer.append(entry)

    def get_entries(
        self,
        limit: int = 200,
        level: str | None = None,
        search: str | None = None,
        correlation_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieve filtered entries from the buffer."""
        with self._lock:
            results: list[dict[str, Any]] = []
            for entry in reversed(self._buffer):
                if level and entry.get("level") != level.upper():
                    continue

                if correlation_id:
                    corr = entry.get("correlation", {})
                    if correlation_id not in (
                        corr.get("correlation_id"),
                        corr.get("job_id"),
                        corr.get("device_id"),
                        corr.get("account_id"),
                    ):
                        continue

                if search:
                    s_lower = search.lower()
                    msg = entry.get("message", "").lower()
                    logger_name = entry.get("logger", "").lower()
                    if s_lower not in msg and s_lower not in logger_name:
                        continue

                results.append(entry)
                if len(results) >= limit:
                    break

            return list(reversed(results))

    def clear(self) -> None:
        """Clear all entries in the buffer."""
        with self._lock:
            self._buffer.clear()

    def __len__(self) -> int:
        with self._lock:
            return len(self._buffer)


class LogBufferHandler(logging.Handler):
    """Logging handler that pushes sanitized structured records into a LogRingBuffer."""

    def __init__(self, buffer: LogRingBuffer) -> None:
        super().__init__()
        self.buffer = buffer
        self._listeners: list[Callable[[dict[str, Any]], None]] = []
        self._listener_lock = threading.Lock()

    def add_listener(self, listener: Callable[[dict[str, Any]], None]) -> None:
        """Register a callback for real-time log event streaming."""
        with self._listener_lock:
            if listener not in self._listeners:
                self._listeners.append(listener)

    def remove_listener(self, listener: Callable[[dict[str, Any]], None]) -> None:
        """Unregister a real-time log event callback."""
        with self._listener_lock:
            if listener in self._listeners:
                self._listeners.remove(listener)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            entry: dict[str, Any] = {
                "timestamp": format_iso(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "source": f"{record.filename}:{record.lineno}",
            }

            ctx = get_log_context()
            if ctx:
                entry["correlation"] = ctx

            if record.exc_info:
                entry["exception_type"] = (
                    record.exc_info[0].__name__ if record.exc_info[0] else "Error"
                )
                entry["exception_message"] = str(record.exc_info[1])

            sanitized_entry = redact_sensitive_data(entry)
            self.buffer.append(sanitized_entry)

            with self._listener_lock:
                listeners = list(self._listeners)

            for cb in listeners:
                with contextlib.suppress(Exception):
                    cb(sanitized_entry)
        except Exception:
            self.handleError(record)
