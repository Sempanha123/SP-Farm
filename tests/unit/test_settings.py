"""Unit tests for typed AppSettings and SettingsManager."""

import threading
from pathlib import Path

from spfarm.shared.settings import AppSettings, SettingsManager


def test_app_settings_defaults() -> None:
    settings = AppSettings()
    assert settings.general.app_name == "SP-Farm V2"
    assert settings.general.environment == "production"
    assert settings.appearance.theme == "light_blue"
    assert settings.appearance.scale_factor == 1.0
    assert settings.storage.auto_backup_enabled is True
    assert settings.devices.poll_interval_seconds == 5.0
    assert settings.automation.default_timeout_seconds == 60
    assert settings.setup.is_first_run is True


def test_settings_manager_load_default_when_missing(tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.json"
    mgr = SettingsManager(settings_file=settings_file)
    s = mgr.get()
    assert s.general.app_name == "SP-Farm V2"
    assert not settings_file.exists()


def test_settings_manager_save_and_reload(tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.json"
    mgr = SettingsManager(settings_file=settings_file)

    def mutate(s: AppSettings) -> None:
        s.general.app_name = "Custom Farm Name"
        s.appearance.theme = "pink"
        s.setup.is_first_run = False

    mgr.update(mutate)

    assert settings_file.exists()

    # Create new manager instance to simulate application restart
    restart_mgr = SettingsManager(settings_file=settings_file)
    loaded = restart_mgr.get()

    assert loaded.general.app_name == "Custom Farm Name"
    assert loaded.appearance.theme == "pink"
    assert loaded.setup.is_first_run is False


def test_settings_manager_corrupt_file_recovery(tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.json"
    settings_file.write_text("{corrupt-json-string!", encoding="utf-8")

    mgr = SettingsManager(settings_file=settings_file)
    loaded = mgr.get()

    assert loaded.general.app_name == "SP-Farm V2"
    corrupt_backup = tmp_path / "settings.json.corrupt"
    assert corrupt_backup.exists()


def test_settings_manager_reset(tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.json"
    mgr = SettingsManager(settings_file=settings_file)
    mgr.update(lambda s: setattr(s.general, "app_name", "Changed"))

    assert mgr.get().general.app_name == "Changed"

    reset_settings = mgr.reset()
    assert reset_settings.general.app_name == "SP-Farm V2"

    # Reload from disk
    mgr2 = SettingsManager(settings_file=settings_file)
    assert mgr2.get().general.app_name == "SP-Farm V2"


def test_settings_manager_thread_safety(tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.json"
    mgr = SettingsManager(settings_file=settings_file)

    def worker(worker_id: int) -> None:
        for _ in range(10):
            mgr.update(lambda s: setattr(s.general, "app_name", f"Worker-{worker_id}"))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    final = mgr.get()
    assert final.general.app_name.startswith("Worker-")
