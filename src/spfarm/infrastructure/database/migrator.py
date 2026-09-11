"""Automated database schema initialization and migration runner."""

from __future__ import annotations

from sqlalchemy import Engine

from spfarm.infrastructure.database.models import Base
from spfarm.infrastructure.database.session import create_db_engine


def apply_migrations(engine: Engine | None = None) -> None:
    """Ensure database schema and tables exist on application startup."""
    eng = engine or create_db_engine()
    # Create all declarative tables if not already present
    Base.metadata.create_all(bind=eng)
