"""Safe online SQLite point-in-time database backup helper."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from spfarm.shared.paths import paths
from spfarm.shared.time import format_iso, utcnow


def backup_database(
    source_db_path: Path | None = None,
    dest_dir: Path | None = None,
    backup_filename: str | None = None,
) -> Path:
    """Perform a live point-in-time backup using SQLite's online backup API.

    Safely snapshots the database without locking readers or requiring a reboot.
    """
    src = source_db_path or paths.database_file
    if not src.exists():
        raise FileNotFoundError(f"Source database does not exist: {src}")

    target_dir = dest_dir or paths.backups_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    if not backup_filename:
        timestamp_str = format_iso(utcnow()).replace(":", "-").replace(".", "-")
        backup_filename = f"spfarm_backup_{timestamp_str}.db"

    dest_path = target_dir / backup_filename

    # Perform online backup using sqlite3.Connection.backup
    src_conn = sqlite3.connect(str(src))
    dest_conn = sqlite3.connect(str(dest_path))

    try:
        with dest_conn:
            src_conn.backup(dest_conn, pages=100, sleep=0.01)
    finally:
        dest_conn.close()
        src_conn.close()

    return dest_path
