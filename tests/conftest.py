"""Pytest configuration and shared fixtures for SP-Farm V2."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Generator

import pytest
from PySide6.QtWidgets import QApplication

from spfarm.shared.paths import AppPaths


@pytest.fixture(scope="session")
def qapp() -> Generator[QApplication, None, None]:
    """Ensure a headless QApplication instance is active for tests."""
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    app = QApplication.instance()
    if app is None:
        app = QApplication(["pytest", "-platform", "offscreen"])
    yield app


@pytest.fixture
def tmp_app_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> AppPaths:
    """Fixture providing isolated temporary application paths."""
    data_dir = tmp_path / "spfarm_data"
    monkeypatch.setenv("SPFARM_DATA_DIR", str(data_dir))
    monkeypatch.delenv("SPFARM_LOG_DIR", raising=False)
    monkeypatch.delenv("SPFARM_BACKUP_DIR", raising=False)
    monkeypatch.delenv("SPFARM_CACHE_DIR", raising=False)

    app_paths = AppPaths.resolve()
    app_paths.ensure_directories()
    return app_paths
