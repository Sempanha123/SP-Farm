"""Unit tests for account commands and handlers."""

from __future__ import annotations

from unittest.mock import MagicMock

from spfarm.application.commands.account_commands import (
    ArchiveAccountCommand,
    ArchiveAccountHandler,
    BulkUpdateAccountStatusCommand,
    BulkUpdateAccountStatusHandler,
    CreateAccountCommand,
    CreateAccountHandler,
    DeleteAccountCommand,
    DeleteAccountHandler,
    RestoreAccountCommand,
    RestoreAccountHandler,
    UpdateAccountCommand,
    UpdateAccountHandler,
)
from spfarm.application.events.base import EventBus
from spfarm.application.services.account_dedup import AccountDuplicateDetector
from spfarm.application.services.audit import AuditService
from spfarm.domain.accounts.models import Account, AccountEmail, AccountSecurity
from spfarm.domain.enums import AccountHealthState, AccountStatus, TwoFactorMethod
from spfarm.domain.interfaces.secret_store import ISecretStore


def test_create_account_command_success():
    mock_uow = MagicMock()
    mock_uow.accounts.list_all.return_value = []

    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow
    mock_uow_ctx.__exit__.return_value = None

    mock_secrets = MagicMock(spec=ISecretStore)
    bus = EventBus()
    audit = MagicMock(spec=AuditService)
    dedup = AccountDuplicateDetector()

    handler = CreateAccountHandler(
        uow_factory=lambda: mock_uow_ctx,
        secret_store=mock_secrets,
        event_bus=bus,
        audit_service=audit,
        dedup_detector=dedup,
    )

    cmd = CreateAccountCommand(
        display_name="Marketing Account 1",
        profile_id="1000123456",
        primary_email="marketing@test.com",
        primary_phone="+15551234567",
        password_plain="super_secure_pass_123",
        totp_seed_plain="JBSWY3DPEHPK3PXP",
        two_factor_method=TwoFactorMethod.TOTP,
    )

    res = handler.handle(cmd)
    assert res.is_success
    account_id = res.value
    assert isinstance(account_id, str)

    # Verify secrets were vaulted
    assert mock_secrets.store_secret.call_count == 2
    mock_secrets.store_secret.assert_any_call(
        f"vault://accounts/{account_id}/password", "super_secure_pass_123"
    )
    mock_secrets.store_secret.assert_any_call(
        f"vault://accounts/{account_id}/totp_seed", "JBSWY3DPEHPK3PXP"
    )

    # Verify UoW persistence
    assert mock_uow.accounts.add.call_count == 1
    saved_acc = mock_uow.accounts.add.call_args[0][0]
    assert saved_acc.display_name == "Marketing Account 1"
    assert saved_acc.profile_id == "1000123456"
    assert saved_acc.primary_email.address == "marketing@test.com"
    assert saved_acc.primary_phone.number == "+15551234567"
    assert saved_acc.security.two_factor_method == TwoFactorMethod.TOTP
    assert saved_acc.security.password_secret_ref == f"vault://accounts/{account_id}/password"
    assert mock_uow.commit.called


def test_create_account_duplicate_rejection():
    existing_acc = Account(
        id="acc_existing",
        profile_id="1000123456",
        display_name="Existing Account",
    )
    existing_acc.add_email(AccountEmail(account_id="acc_existing", address="shared@test.com"))

    mock_uow = MagicMock()
    mock_uow.accounts.list_all.return_value = [existing_acc]
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow
    mock_uow_ctx.__exit__.return_value = None

    handler = CreateAccountHandler(
        uow_factory=lambda: mock_uow_ctx,
        secret_store=MagicMock(spec=ISecretStore),
        event_bus=EventBus(),
        audit_service=MagicMock(spec=AuditService),
        dedup_detector=AccountDuplicateDetector(),
    )

    # Same profile ID
    res = handler.handle(
        CreateAccountCommand(
            display_name="Duplicate Profile",
            profile_id="1000123456",
        )
    )
    assert res.is_failure
    assert "Duplicate detected" in res.error.message

    # Same email
    res2 = handler.handle(
        CreateAccountCommand(
            display_name="Duplicate Email",
            profile_id="9999999999",
            primary_email="shared@test.com",
        )
    )
    assert res2.is_failure
    assert "Duplicate detected" in res2.error.message


def test_update_account_command():
    acc = Account(id="acc_1", profile_id="1001", display_name="Old Name")
    mock_uow = MagicMock()
    mock_uow.accounts.get_by_id.return_value = acc
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow

    handler = UpdateAccountHandler(
        uow_factory=lambda: mock_uow_ctx,
        event_bus=EventBus(),
        audit_service=MagicMock(spec=AuditService),
    )

    res = handler.handle(
        UpdateAccountCommand(
            account_id="acc_1",
            display_name="New Brand Name",
            health_state=AccountHealthState.WARNING,
            notes="Requires attention",
        )
    )
    assert res.is_success
    assert acc.display_name == "New Brand Name"
    assert acc.health_state == AccountHealthState.WARNING
    assert acc.notes == "Requires attention"
    assert mock_uow.commit.called


def test_archive_and_restore_account():
    acc = Account(id="acc_1", profile_id="1001", display_name="Test Acc")
    mock_uow = MagicMock()
    mock_uow.accounts.get_by_id.return_value = acc
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow

    archive_handler = ArchiveAccountHandler(
        uow_factory=lambda: mock_uow_ctx,
        event_bus=EventBus(),
        audit_service=MagicMock(spec=AuditService),
    )
    restore_handler = RestoreAccountHandler(
        uow_factory=lambda: mock_uow_ctx,
        event_bus=EventBus(),
        audit_service=MagicMock(spec=AuditService),
    )

    # Archive
    res_arch = archive_handler.handle(ArchiveAccountCommand(account_id="acc_1"))
    assert res_arch.is_success
    assert acc.status == AccountStatus.ARCHIVED
    assert acc.archived_at is not None

    # Restore
    res_rest = restore_handler.handle(RestoreAccountCommand(account_id="acc_1"))
    assert res_rest.is_success
    assert acc.status == AccountStatus.ACTIVE
    assert acc.archived_at is None


def test_delete_account_cleans_secrets():
    acc = Account(
        id="acc_del",
        profile_id="1001",
        display_name="To Delete",
        security=AccountSecurity(
            account_id="acc_del",
            password_secret_ref="vault://accounts/acc_del/password",
            totp_secret_ref="vault://accounts/acc_del/totp",
        ),
    )
    mock_uow = MagicMock()
    mock_uow.accounts.get_by_id.return_value = acc
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow

    mock_secrets = MagicMock(spec=ISecretStore)

    handler = DeleteAccountHandler(
        uow_factory=lambda: mock_uow_ctx,
        secret_store=mock_secrets,
        event_bus=EventBus(),
        audit_service=MagicMock(spec=AuditService),
    )

    res = handler.handle(DeleteAccountCommand(account_id="acc_del"))
    assert res.is_success
    mock_secrets.delete_secret.assert_any_call("vault://accounts/acc_del/password")
    mock_secrets.delete_secret.assert_any_call("vault://accounts/acc_del/totp")
    mock_uow.accounts.delete.assert_called_with("acc_del")


def test_bulk_update_status():
    acc1 = Account(id="acc_1", profile_id="1001", display_name="Acc 1")
    acc2 = Account(id="acc_2", profile_id="1002", display_name="Acc 2")

    mock_uow = MagicMock()
    mock_uow.accounts.get_by_id.side_effect = lambda aid: (
        acc1 if aid == "acc_1" else (acc2 if aid == "acc_2" else None)
    )
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow

    handler = BulkUpdateAccountStatusHandler(
        uow_factory=lambda: mock_uow_ctx,
        event_bus=EventBus(),
        audit_service=MagicMock(spec=AuditService),
    )

    res = handler.handle(
        BulkUpdateAccountStatusCommand(
            account_ids=["acc_1", "acc_2"],
            new_status=AccountStatus.RESTRICTED,
        )
    )
    assert res.is_success
    assert res.value == 2
    assert acc1.status == AccountStatus.RESTRICTED
    assert acc2.status == AccountStatus.RESTRICTED
