"""UI tests for AccountsTableModel, AccountInspectorPanel, Dialogs, and AccountsView."""

from __future__ import annotations

from unittest.mock import MagicMock

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from spfarm.application.commands.account_commands import (
    ArchiveAccountHandler,
    BulkUpdateAccountStatusHandler,
    CreateAccountHandler,
    DeleteAccountHandler,
    RestoreAccountHandler,
    UpdateAccountHandler,
)
from spfarm.application.queries.accounts import (
    AccountDetailDTO,
    AccountQueryService,
    AccountSummaryDTO,
)
from spfarm.application.services.account_import import (
    AccountImportService,
    ImportPreviewDTO,
    ImportResultDTO,
    ImportRowDTO,
)
from spfarm.application.services.audit import AuditService
from spfarm.domain.interfaces.secret_store import ISecretStore
from spfarm.presentation.accounts.account_dialog import AccountDialog
from spfarm.presentation.accounts.accounts_view import AccountsView
from spfarm.presentation.accounts.import_dialog import AccountImportDialog
from spfarm.presentation.accounts.inspector import AccountInspectorPanel
from spfarm.presentation.accounts.table_model import (
    COL_CHECK,
    COL_CONTACT,
    COL_NAME,
    AccountsTableModel,
)
from spfarm.shared.result import Success


def test_accounts_table_model_10000_rows(qapp: QApplication) -> None:
    """Acceptance criterion: 10,000 rows must be usable and fast without UI freezing."""
    model = AccountsTableModel()
    synthetic_accounts = [
        AccountSummaryDTO(
            id=f"acc_{i:05d}",
            profile_id=f"10000{i:05d}",
            display_name=f"Account {i}",
            masked_contact=f"user_{i}@example.com",
            status="ACTIVE" if i % 10 != 0 else "RESTRICTED",
            health_state="HEALTHY",
            pages_count=2,
            groups_count=3,
            device_name=f"LDPlayer-{i % 4}",
            last_activity_at="2026-09-12T00:00:00Z",
        )
        for i in range(10000)
    ]

    model.set_accounts(synthetic_accounts)
    assert model.rowCount() == 10000
    assert model.columnCount() == 8

    # Fast indexed data lookups
    idx_first = model.index(0, COL_NAME)
    assert "Account 0" in model.data(idx_first, Qt.ItemDataRole.DisplayRole)

    idx_last = model.index(9999, COL_CONTACT)
    assert "user_9999" in model.data(idx_last, Qt.ItemDataRole.DisplayRole)

    # Selection performance
    model.toggle_selection(5)
    assert model.get_selected_ids() == ["acc_00005"]
    assert model.data(model.index(5, COL_CHECK), Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked

    model.clear_selection()
    assert len(model.get_selected_ids()) == 0


def test_account_inspector_all_12_tabs(qapp: QApplication) -> None:
    """Acceptance criterion: Inspector supports full rich metadata across all tabs."""
    mock_secrets = MagicMock(spec=ISecretStore)
    mock_secrets.retrieve_secret.return_value = "secret_decrypted_password"
    mock_audit = MagicMock(spec=AuditService)

    inspector = AccountInspectorPanel(secret_store=mock_secrets, audit_service=mock_audit)
    assert inspector.tabs.count() == 12

    # Hydrate with rich detail record
    detail = AccountDetailDTO(
        id="acc_test_123",
        profile_id="1000998877",
        display_name="Enterprise Page Lead",
        status="ACTIVE",
        health_state="HEALTHY",
        priority=5,
        locale="en_US",
        timezone="America/New_York",
        category_id="Enterprise",
        notes="Important business account",
        created_at="2026-09-12T10:00:00Z",
        last_activity_at="2026-09-12T12:00:00Z",
        emails=[{"id": "em_1", "address": "ceo@firm.com", "masked": "c***o@firm.com", "is_primary": True, "is_verified": True}],
        phones=[{"id": "ph_1", "number": "+15551234567", "masked": "***-***-4567", "is_primary": True, "is_verified": False}],
        security={
            "two_factor_enabled": True,
            "two_factor_method": "TOTP",
            "password_secret_ref": "vault://accounts/acc_test_123/password",
            "totp_secret_ref": "vault://accounts/acc_test_123/totp",
            "last_security_review_at": "2026-09-10T00:00:00Z",
        },
        pages=[{"id": "pg_1", "name": "Firm Official", "platform_page_id": "999888", "followers": 15000}],
        groups=[{"id": "grp_1", "name": "Firm VIPs", "platform_group_id": "777666", "role": "ADMIN"}],
        environment={
            "id": "env_1",
            "app_channel": "Official",
            "android_version": "11.0",
            "user_agent": "Mozilla/5.0 Android 11 Facebook Katana",
            "storage_dir": "C:/envs/env_1",
        },
        runtime_device={
            "id": "dev_1",
            "custom_name": "Physical Pixel 6",
            "provider": "PHYSICAL_ANDROID",
            "state": "READY",
            "adb_serial": "99AABBC001",
        },
    )

    inspector.set_account(detail)

    assert inspector.lbl_acc_name.text() == "Enterprise Page Lead"
    assert "1000998877" in inspector.lbl_acc_id.text()
    assert inspector.status_pill.status_type == "ready"

    # Verify Overview Tab
    assert inspector.lbl_ov_id.text() == "1000998877"
    assert inspector.lbl_ov_health.text() == "HEALTHY"
    assert inspector.lbl_ov_category.text() == "Enterprise"

    # Verify Contacts Tab & Masked display
    assert inspector.contacts_list.count() == 2
    assert "c***o@firm.com" in inspector.contacts_list.item(0).text()

    # Trigger audited reveal
    inspector._on_reveal_contacts_clicked()
    assert "ceo@firm.com [Revealed]" in inspector.contacts_list.item(0).text()
    mock_audit.record.assert_called_with(
        event_type="account.contacts_revealed",
        target_type="account",
        target_id="acc_test_123",
        details={"action": "reveal_masked_contacts"},
    )

    # Verify Security Tab
    assert inspector.lbl_sec_2fa.text() == "TOTP"
    assert "[Masked]" in inspector.lbl_sec_pass_ref.text()

    # Verify Pages & Groups
    assert inspector.pages_list.count() == 1
    assert "Firm Official" in inspector.pages_list.item(0).text()
    assert inspector.groups_list.count() == 1
    assert "Firm VIPs" in inspector.groups_list.item(0).text()

    # Verify Environment & Runtime
    assert "Official" in inspector.lbl_env_channel.text()
    assert "Physical Pixel 6" in inspector.lbl_rt_name.text()

    # Verify Notes
    assert inspector.txt_notes.toPlainText() == "Important business account"


def test_account_dialog_create_and_edit_modes(qapp: QApplication) -> None:
    # 1. Create Mode
    dlg_create = AccountDialog()
    assert dlg_create.is_edit is False
    assert dlg_create.txt_profile_id.isEnabled() is True

    dlg_create.txt_name.setText("Support Agent 1")
    dlg_create.txt_profile_id.setText("1000223344")
    dlg_create.txt_email.setText("agent1@company.com")
    dlg_create.txt_phone.setText("+15553334444")
    dlg_create.txt_password.setText("SecretPass!")
    dlg_create.txt_totp.setText("JBSWY3DPEHPK3PXP")
    dlg_create.txt_category.setText("Support")

    cmd = dlg_create.get_create_command()
    assert cmd.display_name == "Support Agent 1"
    assert cmd.profile_id == "1000223344"
    assert cmd.primary_email == "agent1@company.com"
    assert cmd.primary_phone == "+15553334444"
    assert cmd.password_plain == "SecretPass!"
    assert cmd.totp_seed_plain == "JBSWY3DPEHPK3PXP"
    assert cmd.category_id == "Support"

    # 2. Edit Mode
    existing_detail = AccountDetailDTO(
        id="acc_edit_1",
        profile_id="1000555",
        display_name="Original Name",
        status="ACTIVE",
        health_state="HEALTHY",
        priority=0,
        locale="en_US",
        timezone="UTC",
        category_id="General",
        notes="Some notes",
        created_at="",
        last_activity_at=None,
    )
    dlg_edit = AccountDialog(account=existing_detail)
    assert dlg_edit.is_edit is True
    assert dlg_edit.txt_profile_id.isEnabled() is False
    assert dlg_edit.txt_name.text() == "Original Name"


def test_account_import_dialog_preview(qapp: QApplication) -> None:
    mock_import_service = MagicMock(spec=AccountImportService)
    mock_import_service.preview_csv_file.return_value = ImportPreviewDTO(
        total_rows=2,
        valid_count=1,
        duplicate_count=1,
        error_count=0,
        rows=[
            ImportRowDTO(row_index=1, display_name="Account Alpha", profile_id="1001", email="a@test.com", is_valid=True),
            ImportRowDTO(row_index=2, display_name="Account Beta", profile_id="1002", is_valid=True, is_duplicate=True, duplicate_reason="Matched existing profile"),
        ],
    )
    mock_import_service.execute_import.return_value = ImportResultDTO(imported_count=1, skipped_count=1)

    dlg = AccountImportDialog(import_service=mock_import_service)
    dlg._current_preview = mock_import_service.preview_csv_file("dummy.csv")
    dlg._render_preview(dlg._current_preview)

    assert dlg.table.rowCount() == 2
    assert dlg.lbl_stat_total.text() == "Total: 2"
    assert dlg.lbl_stat_valid.text() == "Valid: 1"
    assert dlg.lbl_stat_dup.text() == "Duplicates: 1"
    assert dlg.btn_import.isEnabled() is True


def test_accounts_view_filtering_and_bulk_actions(qapp: QApplication) -> None:
    mock_query = MagicMock(spec=AccountQueryService)
    mock_query.list_accounts.return_value = [
        AccountSummaryDTO(
            id="acc_1",
            profile_id="1001",
            display_name="Marketing Lead",
            masked_contact="m***g@test.com",
            status="ACTIVE",
            health_state="HEALTHY",
            pages_count=2,
            groups_count=1,
            device_name="LD-1",
        ),
        AccountSummaryDTO(
            id="acc_2",
            profile_id="1002",
            display_name="Support Desk",
            masked_contact="s***t@test.com",
            status="RESTRICTED",
            health_state="WARNING",
            pages_count=0,
            groups_count=0,
            device_name="Unassigned",
        ),
    ]
    mock_query.get_account_detail.return_value = AccountDetailDTO(
        id="acc_1",
        profile_id="1001",
        display_name="Marketing Lead",
        status="ACTIVE",
        health_state="HEALTHY",
        priority=0,
        locale="en_US",
        timezone="UTC",
        category_id=None,
        notes="Test note",
        created_at="",
        last_activity_at=None,
    )

    mock_create = MagicMock(spec=CreateAccountHandler)
    mock_update = MagicMock(spec=UpdateAccountHandler)
    mock_archive = MagicMock(spec=ArchiveAccountHandler)
    mock_restore = MagicMock(spec=RestoreAccountHandler)
    mock_delete = MagicMock(spec=DeleteAccountHandler)
    mock_bulk = MagicMock(spec=BulkUpdateAccountStatusHandler)
    mock_bulk.handle.return_value = Success(1)
    mock_import = MagicMock(spec=AccountImportService)

    view = AccountsView(
        query_service=mock_query,
        create_handler=mock_create,
        update_handler=mock_update,
        archive_handler=mock_archive,
        restore_handler=mock_restore,
        delete_handler=mock_delete,
        bulk_handler=mock_bulk,
        import_service=mock_import,
    )

    assert view.table_model.rowCount() == 2
    assert view.bulk_bar.isHidden() is True

    # Select an account
    view.table_model.toggle_selection(0)
    assert not view.bulk_bar.isHidden()
    assert "1 account selected" in view.lbl_selected_count.text()

    # Bulk action trigger
    view.btn_bulk_archive.click()
    mock_bulk.handle.assert_called_once()
    assert view.table_model.get_selected_ids() == []
