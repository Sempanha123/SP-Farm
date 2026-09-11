"""Tests for SettingsDialog and SetupWizardDialog UI components."""

from pathlib import Path

from PySide6.QtWidgets import QApplication

from spfarm.infrastructure.secrets.encrypted_file import EncryptedFileSecretStore
from spfarm.presentation.settings.settings_view import SettingsDialog
from spfarm.presentation.shell.setup_wizard import SetupWizardDialog
from spfarm.shared.settings import SettingsManager


def test_settings_dialog_init_and_switch_pages(qapp: QApplication, tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.json"
    mgr = SettingsManager(settings_file=settings_file)
    secret_store = EncryptedFileSecretStore(
        vault_file=tmp_path / "vault.enc",
        key_file=tmp_path / "key",
    )

    dialog = SettingsDialog(settings_manager=mgr, secret_store=secret_store)
    assert dialog.windowTitle().startswith("Settings & Security Vault")
    assert dialog.category_list.count() == 6

    # Switch category pages
    dialog.category_list.setCurrentRow(1)
    assert dialog.stacked_widget.currentIndex() == 1

    dialog.category_list.setCurrentRow(5)
    assert dialog.stacked_widget.currentIndex() == 5

    dialog.close()


def test_setup_wizard_dialog_flow(qapp: QApplication, tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.json"
    mgr = SettingsManager(settings_file=settings_file)
    assert mgr.get().setup.is_first_run is True

    secret_store = EncryptedFileSecretStore(
        vault_file=tmp_path / "vault.enc",
        key_file=tmp_path / "key",
    )

    wizard = SetupWizardDialog(settings_manager=mgr, secret_store=secret_store)
    assert wizard.windowTitle().startswith("Welcome to SP-Farm V2")
    assert wizard.current_step == 0

    # Step through wizard
    wizard._next_step()
    assert wizard.current_step == 1
    wizard._next_step()
    assert wizard.current_step == 2
    wizard._next_step()
    assert wizard.current_step == 3

    # Final step completion
    wizard._next_step()
    assert mgr.get().setup.is_first_run is False
    assert mgr.get().setup.wizard_completed is True

    wizard.close()
