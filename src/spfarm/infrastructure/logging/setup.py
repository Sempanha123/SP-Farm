"""Logging system configuration, rotating file handlers, and retention cleanup."""

from __future__ import annotations

import logging
import os
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

from spfarm.infrastructure.logging.buffer import LogBufferHandler, LogRingBuffer
from spfarm.infrastructure.logging.formatter import CuteConsoleFormatter, StructuredJsonFormatter
from spfarm.shared.paths import paths

_global_buffer: LogRingBuffer | None = None


def get_log_buffer() -> LogRingBuffer:
    """Get the singleton in-memory ring buffer."""
    global _global_buffer
    if _global_buffer is None:
        _global_buffer = LogRingBuffer(capacity=5000)
    return _global_buffer


def configure_logging(
    logs_dir: Path | None = None,
    log_level: str = "INFO",
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
    enable_console: bool = True,
) -> LogRingBuffer:
    """Initialize application logging with rotating files, console output, and in-memory buffer."""
    target_dir = logs_dir or paths.logs_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    log_file = target_dir / "spfarm.log"

    root_logger = logging.getLogger()
    level_num = getattr(logging, log_level.upper(), logging.INFO)
    root_logger.setLevel(level_num)

    # Remove existing handlers to avoid duplicate logging upon reconfiguration
    root_logger.handlers.clear()

    # 1. Rotating File Handler (Structured JSON)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(StructuredJsonFormatter())
    file_handler.setLevel(level_num)
    root_logger.addHandler(file_handler)

    # 2. Console Handler (Human-readable Cute Console)
    if enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(CuteConsoleFormatter())
        console_handler.setLevel(level_num)
        root_logger.addHandler(console_handler)

    # 3. In-Memory Ring Buffer Handler
    buffer = get_log_buffer()
    buf_handler = LogBufferHandler(buffer)
    buf_handler.setLevel(level_num)
    root_logger.addHandler(buf_handler)

    return buffer


def cleanup_old_logs(logs_dir: Path | None = None, max_age_days: int = 14) -> int:
    """Purge rotated log files older than max_age_days. Returns count of deleted files."""
    target_dir = logs_dir or paths.logs_dir
    if not target_dir.exists():
        return 0

    now = time.time()
    cutoff_seconds = now - (max_age_days * 86400)
    deleted_count = 0

    for file_path in target_dir.glob("spfarm.log.*"):
        try:
            mtime = os.path.getmtime(file_path)
            if mtime < cutoff_seconds:
                file_path.unlink()
                deleted_count += 1
        except Exception:
            pass

    return deleted_count
