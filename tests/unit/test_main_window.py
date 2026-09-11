"""Tests for MainWindow shell, route navigation, theme persistence, and 1366x768 responsiveness."""

from pathlib import Path

from PySide6.QtWidgets import QApplication

from spfarm.infrastructure.container import Container
from spfarm.infrastructure.secrets.encrypted_file import EncryptedFileSecretStore
from spfarm.presentation.shell.main_window import MainWindow
from spfarm.shared.settings import SettingsManager


def test_main_window_resolution_and_all_routes(qapp: QApplication, tmp_path: Path) -> None:
    """Acceptance criteria: All routes render in one shell, 1366x768 works."""
    settings_file = tmp_path / "settings.json"
    mgr = SettingsManager(settings_file=settings_file)
    secret_store = EncryptedFileSecretStore(
        vault_file=tmp_path / "vault.enc",
        key_file=tmp_path / "key",
    )

    test_container = Container()
    test_container.register_singleton(SettingsManager, mgr)
    test_container.register_singleton("ISecretStore", secret_store)

    window = MainWindow(app_container=test_container)

    # 1. 1366x768 resolution check
    assert window.width() == 1366
    assert window.height() == 768
    assert window.minimumWidth() <= 1024
    assert window.minimumHeight() <= 640

    # 2. Verify all routes render in one shell
    routes = [
        "dashboard",
        "accounts",
        "environments",
        "devices",
        "device_pool",
        "apps",
        "campaigns",
        "scheduler",
        "jobs",
        "actions",
        "activity",
        "settings",
    ]

    for route_id in routes:
        window.navigate_to_route(route_id)
        current_idx = window.stack.currentIndex()
        assert current_idx == window._route_indices[route_id]
        assert window.stack.currentWidget() is not None

    window.close()


def test_main_window_theme_persists(qapp: QApplication, tmp_path: Path) -> None:
    """Acceptance criteria: Theme persists."""
    settings_file = tmp_path / "settings.json"
    mgr = SettingsManager(settings_file=settings_file)

    test_container = Container()
    test_container.register_singleton(SettingsManager, mgr)

    window = MainWindow(app_container=test_container)

    # Switch theme to pink
    window._on_theme_changed("pink")
    assert window._current_theme == "pink"

    # Verify persisted in SettingsManager
    assert mgr.get().appearance.theme == "pink"

    # Reload simulated restart
    restart_mgr = SettingsManager(settings_file=settings_file)
    assert restart_mgr.get().appearance.theme == "pink"

    # Switch theme to lavender
    window._on_theme_changed("lavender")
    assert restart_mgr.load().appearance.theme == "lavender"

    window.close()


def test_main_window_language_switching(qapp: QApplication, tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.json"
    mgr = SettingsManager(settings_file=settings_file)

    test_container = Container()
    test_container.register_singleton(SettingsManager, mgr)

    window = MainWindow(app_container=test_container)
    window.navigate_to_route("dashboard")
    assert window.topbar.lbl_title.text() == "Dashboard"

    # Switch to Khmer
    window._on_language_changed("km")
    assert window.topbar.lbl_title.text() == "ផ្ទាំងគ្រប់គ្រង"

    # Switch back to English
    window._on_language_changed("en")
    assert window.topbar.lbl_title.text() == "Dashboard"

    window.close()
