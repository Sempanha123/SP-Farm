"""Database engine and session management with SQLite WAL & busy timeout."""

from __future__ import annotations

import sqlite3
from typing import Any

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from spfarm.shared.paths import paths


def _set_sqlite_pragmas(dbapi_connection: Any, _connection_record: Any) -> None:
    """Apply performance and concurrency pragmas to each SQLite connection."""
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA busy_timeout=5000")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()


def create_db_engine(db_url: str | None = None) -> Engine:
    """Create and configure a SQLAlchemy engine."""
    if not db_url:
        paths.ensure_directories()
        db_path = paths.database_file.as_posix()
        db_url = f"sqlite:///{db_path}"

    engine = create_engine(
        db_url,
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
    )

    event.listen(engine, "connect", _set_sqlite_pragmas)
    return engine


def create_session_factory(engine: Engine | None = None) -> sessionmaker[Session]:
    """Create a thread-safe sessionmaker factory."""
    eng = engine or create_db_engine()
    return sessionmaker(
        bind=eng,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
