"""Commands and handlers for managing Account aggregates and lifecycle."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Callable, Optional

from spfarm.application.commands.base import Command, CommandHandler
from spfarm.application.events.account_events import (
    AccountArchivedEvent,
    AccountCreatedEvent,
    AccountDeletedEvent,
    AccountRestoredEvent,
    AccountStatusChangedEvent,
    AccountUpdatedEvent,
)
from spfarm.application.events.base import EventBus
from spfarm.application.services.account_dedup import AccountDuplicateDetector
from spfarm.application.services.audit import AuditService
from spfarm.domain.accounts.models import (
    Account,
    AccountEmail,
    AccountPhone,
    AccountSecurity,
)
from spfarm.domain.enums import AccountHealthState, AccountStatus, TwoFactorMethod
from spfarm.domain.interfaces.secret_store import ISecretStore
from spfarm.domain.interfaces.unit_of_work import IUnitOfWork
from spfarm.shared.errors import AppError, ConflictError, NotFoundError, ValidationError
from spfarm.shared.ids import generate_id
from spfarm.shared.result import Failure, Result, Success

logger = logging.getLogger(__name__)


# =============================================================================
# Create Account Command
# =============================================================================

@dataclass(frozen=True, kw_only=True)
class CreateAccountCommand(Command):
    """Command to register a new account."""

    display_name: str
    profile_id: str
    primary_email: Optional[str] = None
    primary_phone: Optional[str] = None
    password_plain: Optional[str] = None
    totp_seed_plain: Optional[str] = None
    two_factor_method: TwoFactorMethod = TwoFactorMethod.NONE
    category_id: Optional[str] = None
    notes: Optional[str] = None
    locale: str = "en_US"
    timezone: str = "UTC"
    allow_duplicates: bool = False


class CreateAccountHandler(CommandHandler[CreateAccountCommand, str]):
    """Handles creating an Account, vaulting credentials, and emitting domain events."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        secret_store: ISecretStore,
        event_bus: EventBus,
        audit_service: AuditService,
        dedup_detector: AccountDuplicateDetector,
    ) -> None:
        self._uow_factory = uow_factory
        self._secret_store = secret_store
        self._event_bus = event_bus
        self._audit = audit_service
        self._dedup = dedup_detector

    def handle(self, cmd: CreateAccountCommand) -> Result[str, AppError]:
        if not cmd.display_name.strip():
            return Failure(ValidationError("Account display name cannot be empty."))
        if not cmd.profile_id.strip():
            return Failure(ValidationError("Platform profile ID cannot be empty."))

        account_id = generate_id()

        with self._uow_factory() as uow:
            # 1. Duplicate check
            if not cmd.allow_duplicates:
                emails = [cmd.primary_email] if cmd.primary_email else []
                phones = [cmd.primary_phone] if cmd.primary_phone else []
                matches = self._dedup.check_duplicates_in_collection(
                    target_profile_id=cmd.profile_id,
                    target_emails=emails,
                    target_phones=phones,
                    existing_accounts=uow.accounts.list_all(),
                )
                if matches:
                    m = matches[0]
                    return Failure(
                        ConflictError(
                            f"Duplicate detected with account '{m.display_name}': matching {m.match_field} '{m.match_value}'"
                        )
                    )

            # 2. Vault credentials if provided
            password_ref: Optional[str] = None
            if cmd.password_plain:
                password_ref = f"vault://accounts/{account_id}/password"
                self._secret_store.store_secret(password_ref, cmd.password_plain)

            totp_ref: Optional[str] = None
            if cmd.totp_seed_plain:
                totp_ref = f"vault://accounts/{account_id}/totp_seed"
                self._secret_store.store_secret(totp_ref, cmd.totp_seed_plain)

            # 3. Create aggregate
            account = Account(
                id=account_id,
                profile_id=cmd.profile_id.strip(),
                display_name=cmd.display_name.strip(),
                locale=cmd.locale,
                timezone=cmd.timezone,
                category_id=cmd.category_id,
                notes=cmd.notes,
                status=AccountStatus.ACTIVE,
                health_state=AccountHealthState.HEALTHY,
                security=AccountSecurity(
                    account_id=account_id,
                    two_factor_enabled=(cmd.two_factor_method != TwoFactorMethod.NONE),
                    two_factor_method=cmd.two_factor_method,
                    password_secret_ref=password_ref,
                    totp_secret_ref=totp_ref,
                ),
            )

            if cmd.primary_email:
                account.add_email(
                    AccountEmail(
                        account_id=account_id,
                        address=cmd.primary_email.strip(),
                        is_primary=True,
                    )
                )

            if cmd.primary_phone:
                account.add_phone(
                    AccountPhone(
                        account_id=account_id,
                        number=cmd.primary_phone.strip(),
                        is_primary=True,
                    )
                )

            uow.accounts.add(account)
            uow.commit()

        # Audit and Events
        self._audit.record(
            event_type="account.created",
            target_type="account",
            target_id=account_id,
            details={"display_name": cmd.display_name, "profile_id": cmd.profile_id},
        )
        self._event_bus.publish(
            AccountCreatedEvent(account_id=account_id, display_name=cmd.display_name)
        )

        return Success(account_id)


# =============================================================================
# Update Account Command
# =============================================================================

@dataclass(frozen=True, kw_only=True)
class UpdateAccountCommand(Command):
    """Command to update an existing account's metadata."""

    account_id: str
    display_name: Optional[str] = None
    category_id: Optional[str] = None
    notes: Optional[str] = None
    priority: Optional[int] = None
    health_state: Optional[AccountHealthState] = None
    two_factor_method: Optional[TwoFactorMethod] = None


class UpdateAccountHandler(CommandHandler[UpdateAccountCommand, None]):
    """Handles updating account attributes."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        event_bus: EventBus,
        audit_service: AuditService,
    ) -> None:
        self._uow_factory = uow_factory
        self._event_bus = event_bus
        self._audit = audit_service

    def handle(self, cmd: UpdateAccountCommand) -> Result[None, AppError]:
        with self._uow_factory() as uow:
            account = uow.accounts.get_by_id(cmd.account_id)
            if not account:
                return Failure(NotFoundError(f"Account '{cmd.account_id}' not found."))

            if cmd.display_name is not None:
                account.display_name = cmd.display_name.strip()
            if cmd.category_id is not None:
                account.category_id = cmd.category_id
            if cmd.notes is not None:
                account.notes = cmd.notes
            if cmd.priority is not None:
                account.priority = cmd.priority
            if cmd.health_state is not None:
                account.health_state = cmd.health_state
            if cmd.two_factor_method is not None and account.security:
                account.security.two_factor_method = cmd.two_factor_method
                account.security.two_factor_enabled = (cmd.two_factor_method != TwoFactorMethod.NONE)

            uow.accounts.add(account)
            uow.commit()

        self._audit.record(
            event_type="account.updated",
            target_type="account",
            target_id=cmd.account_id,
            details={"changes": "metadata_updated"},
        )
        self._event_bus.publish(AccountUpdatedEvent(account_id=cmd.account_id))
        return Success(None)


# =============================================================================
# Archive & Restore Commands
# =============================================================================

@dataclass(frozen=True, kw_only=True)
class ArchiveAccountCommand(Command):
    """Command to archive an account."""

    account_id: str


class ArchiveAccountHandler(CommandHandler[ArchiveAccountCommand, None]):
    """Handles archiving an account."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        event_bus: EventBus,
        audit_service: AuditService,
    ) -> None:
        self._uow_factory = uow_factory
        self._event_bus = event_bus
        self._audit = audit_service

    def handle(self, cmd: ArchiveAccountCommand) -> Result[None, AppError]:
        with self._uow_factory() as uow:
            account = uow.accounts.get_by_id(cmd.account_id)
            if not account:
                return Failure(NotFoundError(f"Account '{cmd.account_id}' not found."))

            account.set_status(AccountStatus.ARCHIVED)
            uow.accounts.add(account)
            uow.commit()

        self._audit.record(
            event_type="account.archived",
            target_type="account",
            target_id=cmd.account_id,
            details={"status": "ARCHIVED"},
        )
        self._event_bus.publish(AccountArchivedEvent(account_id=cmd.account_id))
        return Success(None)


@dataclass(frozen=True, kw_only=True)
class RestoreAccountCommand(Command):
    """Command to restore an archived account to active status."""

    account_id: str


class RestoreAccountHandler(CommandHandler[RestoreAccountCommand, None]):
    """Handles restoring an archived account."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        event_bus: EventBus,
        audit_service: AuditService,
    ) -> None:
        self._uow_factory = uow_factory
        self._event_bus = event_bus
        self._audit = audit_service

    def handle(self, cmd: RestoreAccountCommand) -> Result[None, AppError]:
        with self._uow_factory() as uow:
            account = uow.accounts.get_by_id(cmd.account_id)
            if not account:
                return Failure(NotFoundError(f"Account '{cmd.account_id}' not found."))

            account.set_status(AccountStatus.ACTIVE)
            account.archived_at = None
            uow.accounts.add(account)
            uow.commit()

        self._audit.record(
            event_type="account.restored",
            target_type="account",
            target_id=cmd.account_id,
            details={"status": "ACTIVE"},
        )
        self._event_bus.publish(AccountRestoredEvent(account_id=cmd.account_id))
        return Success(None)


# =============================================================================
# Delete Account Command
# =============================================================================

@dataclass(frozen=True, kw_only=True)
class DeleteAccountCommand(Command):
    """Command to permanently delete an account and its credentials."""

    account_id: str


class DeleteAccountHandler(CommandHandler[DeleteAccountCommand, None]):
    """Handles permanent account deletion."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        secret_store: ISecretStore,
        event_bus: EventBus,
        audit_service: AuditService,
    ) -> None:
        self._uow_factory = uow_factory
        self._secret_store = secret_store
        self._event_bus = event_bus
        self._audit = audit_service

    def handle(self, cmd: DeleteAccountCommand) -> Result[None, AppError]:
        with self._uow_factory() as uow:
            account = uow.accounts.get_by_id(cmd.account_id)
            if not account:
                return Failure(NotFoundError(f"Account '{cmd.account_id}' not found."))

            # Clean up secrets
            if account.security:
                if account.security.password_secret_ref:
                    self._secret_store.delete_secret(account.security.password_secret_ref)
                if account.security.totp_secret_ref:
                    self._secret_store.delete_secret(account.security.totp_secret_ref)

            uow.accounts.delete(cmd.account_id)
            uow.commit()

        self._audit.record(
            event_type="account.deleted",
            target_type="account",
            target_id=cmd.account_id,
            details={},
        )
        self._event_bus.publish(AccountDeletedEvent(account_id=cmd.account_id))
        return Success(None)


# =============================================================================
# Bulk Update Status Command
# =============================================================================

@dataclass(frozen=True, kw_only=True)
class BulkUpdateAccountStatusCommand(Command):
    """Command to update status across multiple accounts in one transaction."""

    account_ids: list[str]
    new_status: AccountStatus


class BulkUpdateAccountStatusHandler(CommandHandler[BulkUpdateAccountStatusCommand, int]):
    """Handles bulk status changes."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        event_bus: EventBus,
        audit_service: AuditService,
    ) -> None:
        self._uow_factory = uow_factory
        self._event_bus = event_bus
        self._audit = audit_service

    def handle(self, cmd: BulkUpdateAccountStatusCommand) -> Result[int, AppError]:
        updated_count = 0
        with self._uow_factory() as uow:
            for aid in cmd.account_ids:
                account = uow.accounts.get_by_id(aid)
                if account:
                    old_status = account.status.value
                    try:
                        account.set_status(cmd.new_status)
                        uow.accounts.add(account)
                        updated_count += 1
                        self._event_bus.publish(
                            AccountStatusChangedEvent(
                                account_id=aid,
                                old_status=old_status,
                                new_status=cmd.new_status.value,
                            )
                        )
                    except ValidationError as err:
                        logger.warning("Could not transition account %s: %s", aid, err)
            uow.commit()

        self._audit.record(
            event_type="account.bulk_status_changed",
            target_type="accounts",
            target_id="bulk",
            details={"count": updated_count, "new_status": cmd.new_status.value},
        )
        return Success(updated_count)
