"""Tests for application path resolution."""

from pathlib import Path

import pytest

from spfarm.shared.paths import AppPaths


def test_paths_default_are_pathlib() -> None:
    paths = AppPaths.resolve()
    assert isinstance(paths.base_dir, Path)
    assert isinstance(paths.data_dir, Path)
    assert isinstance(paths.logs_dir, Path)
    assert isinstance(paths.backups_dir, Path)
    assert isinstance(paths.cache_dir, Path)
    assert isinstance(paths.secrets_dir, Path)
    assert isinstance(paths.database_file, Path)
    assert isinstance(paths.settings_file, Path)


def test_paths_custom_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    custom_root = tmp_path / "custom_spfarm"
    monkeypatch.setenv("SPFARM_DATA_DIR", str(custom_root))
    monkeypatch.delenv("SPFARM_LOG_DIR", raising=False)

    paths = AppPaths.resolve()
    assert paths.base_dir == custom_root.resolve()
    assert paths.data_dir == (custom_root / "data").resolve()
    assert paths.logs_dir == (custom_root / "logs").resolve()

    paths.ensure_directories()
    assert paths.base_dir.is_dir()
    assert paths.data_dir.is_dir()
    assert paths.logs_dir.is_dir()
    assert paths.backups_dir.is_dir()
    assert paths.cache_dir.is_dir()
    assert paths.secrets_dir.is_dir()
