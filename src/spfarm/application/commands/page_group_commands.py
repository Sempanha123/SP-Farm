"""Commands and handlers for managing Facebook Pages and Groups."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Callable, Optional

from spfarm.application.commands.base import Command, CommandHandler
from spfarm.application.events.base import EventBus
from spfarm.application.events.page_group_events import (
    GroupAddedEvent,
    GroupDeletedEvent,
    GroupUpdatedEvent,
    PageAddedEvent,
    PageDeletedEvent,
    PageUpdatedEvent,
)
from spfarm.application.services.audit import AuditService
from spfarm.domain.accounts.models import Group, Page
from spfarm.domain.interfaces.unit_of_work import IUnitOfWork
from spfarm.shared.errors import AppError, NotFoundError, ValidationError
from spfarm.shared.ids import generate_id
from spfarm.shared.result import Failure, Result, Success
from spfarm.shared.time import format_iso, utcnow

logger = logging.getLogger(__name__)


# =============================================================================
# Page Commands
# =============================================================================


@dataclass(frozen=True, kw_only=True)
class AddPageCommand(Command):
    """Command to attach a Facebook Page to an account."""

    account_id: str
    platform_page_id: str
    name: str
    category: str = "General"
    followers: int = 0
    profile_url: Optional[str] = None
    publishing_enabled: bool = True
    notes: Optional[str] = None


class AddPageHandler(CommandHandler[AddPageCommand, str]):
    """Handles attaching a Page to an account."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        event_bus: EventBus,
        audit_service: AuditService,
    ) -> None:
        self._uow_factory = uow_factory
        self._event_bus = event_bus
        self._audit = audit_service

    def handle(self, cmd: AddPageCommand) -> Result[str, AppError]:
        if not cmd.name.strip():
            return Failure(ValidationError("Page name cannot be empty."))
        if not cmd.platform_page_id.strip():
            return Failure(ValidationError("Platform Page ID cannot be empty."))

        page_id = generate_id()
        with self._uow_factory() as uow:
            account = uow.accounts.get_by_id(cmd.account_id)
            if not account:
                return Failure(NotFoundError(f"Account '{cmd.account_id}' not found."))

            # Ensure not duplicate within account
            for p in account.pages:
                if p.platform_page_id == cmd.platform_page_id.strip():
                    return Failure(
                        ValidationError(
                            f"Page '{cmd.platform_page_id}' is already managed by this account."
                        )
                    )

            page = Page(
                id=page_id,
                account_id=cmd.account_id,
                platform_page_id=cmd.platform_page_id.strip(),
                name=cmd.name.strip(),
                category=cmd.category.strip() or "General",
                followers=max(0, cmd.followers),
                profile_url=cmd.profile_url,
                publishing_enabled=cmd.publishing_enabled,
                notes=cmd.notes,
                last_synced_at=format_iso(utcnow()),
            )
            account.pages.append(page)
            uow.accounts.add(account)
            uow.commit()

        self._audit.record(
            event_type="page.added",
            target_type="page",
            target_id=page_id,
            details={
                "name": cmd.name,
                "platform_page_id": cmd.platform_page_id,
                "account_id": cmd.account_id,
            },
        )
        self._event_bus.publish(
            PageAddedEvent(account_id=cmd.account_id, page_id=page_id, page_name=cmd.name)
        )
        return Success(page_id)


@dataclass(frozen=True, kw_only=True)
class UpdatePageCommand(Command):
    """Command to update Page metadata, publishing switch, or notes."""

    page_id: str
    name: Optional[str] = None
    category: Optional[str] = None
    followers: Optional[int] = None
    publishing_enabled: Optional[bool] = None
    notes: Optional[str] = None


class UpdatePageHandler(CommandHandler[UpdatePageCommand, None]):
    """Handles updating a Page."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        event_bus: EventBus,
        audit_service: AuditService,
    ) -> None:
        self._uow_factory = uow_factory
        self._event_bus = event_bus
        self._audit = audit_service

    def handle(self, cmd: UpdatePageCommand) -> Result[None, AppError]:
        target_account_id: Optional[str] = None
        with self._uow_factory() as uow:
            accounts = uow.accounts.list_all()
            page_found = False
            for acc in accounts:
                for p in acc.pages:
                    if p.id == cmd.page_id:
                        page_found = True
                        target_account_id = acc.id
                        if cmd.name is not None:
                            p.name = cmd.name.strip()
                        if cmd.category is not None:
                            p.category = cmd.category.strip()
                        if cmd.followers is not None:
                            p.followers = max(0, cmd.followers)
                        if cmd.publishing_enabled is not None:
                            p.publishing_enabled = cmd.publishing_enabled
                        if cmd.notes is not None:
                            p.notes = cmd.notes
                        p.last_synced_at = format_iso(utcnow())
                        uow.accounts.add(acc)
                        break
                if page_found:
                    break

            if not page_found or not target_account_id:
                return Failure(NotFoundError(f"Page '{cmd.page_id}' not found."))

            uow.commit()

        self._audit.record(
            event_type="page.updated",
            target_type="page",
            target_id=cmd.page_id,
            details={"account_id": target_account_id},
        )
        self._event_bus.publish(PageUpdatedEvent(account_id=target_account_id, page_id=cmd.page_id))
        return Success(None)


@dataclass(frozen=True, kw_only=True)
class DeletePageCommand(Command):
    """Command to detach a Page from an account."""

    page_id: str


class DeletePageHandler(CommandHandler[DeletePageCommand, None]):
    """Handles removing a Page."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        event_bus: EventBus,
        audit_service: AuditService,
    ) -> None:
        self._uow_factory = uow_factory
        self._event_bus = event_bus
        self._audit = audit_service

    def handle(self, cmd: DeletePageCommand) -> Result[None, AppError]:
        target_account_id: Optional[str] = None
        with self._uow_factory() as uow:
            accounts = uow.accounts.list_all()
            removed = False
            for acc in accounts:
                for i, p in enumerate(acc.pages):
                    if p.id == cmd.page_id:
                        target_account_id = acc.id
                        acc.pages.pop(i)
                        uow.accounts.add(acc)
                        removed = True
                        break
                if removed:
                    break

            if not removed or not target_account_id:
                return Failure(NotFoundError(f"Page '{cmd.page_id}' not found."))

            uow.commit()

        self._audit.record(
            event_type="page.deleted",
            target_type="page",
            target_id=cmd.page_id,
            details={"account_id": target_account_id},
        )
        self._event_bus.publish(PageDeletedEvent(account_id=target_account_id, page_id=cmd.page_id))
        return Success(None)


# =============================================================================
# Group Commands
# =============================================================================


@dataclass(frozen=True, kw_only=True)
class AddGroupCommand(Command):
    """Command to associate a Facebook Group with an account."""

    account_id: str
    platform_group_id: str
    name: str
    role: str = "MEMBER"  # ADMIN, MODERATOR, MEMBER
    members: int = 0
    posting_permission: str = "ALLOWED"  # ALLOWED, PENDING_APPROVAL, MUTED
    notes: Optional[str] = None


class AddGroupHandler(CommandHandler[AddGroupCommand, str]):
    """Handles attaching a Group to an account."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        event_bus: EventBus,
        audit_service: AuditService,
    ) -> None:
        self._uow_factory = uow_factory
        self._event_bus = event_bus
        self._audit = audit_service

    def handle(self, cmd: AddGroupCommand) -> Result[str, AppError]:
        if not cmd.name.strip():
            return Failure(ValidationError("Group name cannot be empty."))
        if not cmd.platform_group_id.strip():
            return Failure(ValidationError("Platform Group ID cannot be empty."))

        group_id = generate_id()
        with self._uow_factory() as uow:
            account = uow.accounts.get_by_id(cmd.account_id)
            if not account:
                return Failure(NotFoundError(f"Account '{cmd.account_id}' not found."))

            for g in account.groups:
                if g.platform_group_id == cmd.platform_group_id.strip():
                    return Failure(
                        ValidationError(
                            f"Group '{cmd.platform_group_id}' is already managed by this account."
                        )
                    )

            group = Group(
                id=group_id,
                account_id=cmd.account_id,
                platform_group_id=cmd.platform_group_id.strip(),
                name=cmd.name.strip(),
                role=cmd.role.upper(),
                members=max(0, cmd.members),
                posting_permission=cmd.posting_permission.upper(),
                notes=cmd.notes,
                last_synced_at=format_iso(utcnow()),
            )
            account.groups.append(group)
            uow.accounts.add(account)
            uow.commit()

        self._audit.record(
            event_type="group.added",
            target_type="group",
            target_id=group_id,
            details={
                "name": cmd.name,
                "platform_group_id": cmd.platform_group_id,
                "account_id": cmd.account_id,
            },
        )
        self._event_bus.publish(
            GroupAddedEvent(account_id=cmd.account_id, group_id=group_id, group_name=cmd.name)
        )
        return Success(group_id)


@dataclass(frozen=True, kw_only=True)
class UpdateGroupCommand(Command):
    """Command to update Group role, permissions, or metadata."""

    group_id: str
    name: Optional[str] = None
    role: Optional[str] = None
    members: Optional[int] = None
    posting_permission: Optional[str] = None
    notes: Optional[str] = None


class UpdateGroupHandler(CommandHandler[UpdateGroupCommand, None]):
    """Handles updating a Group."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        event_bus: EventBus,
        audit_service: AuditService,
    ) -> None:
        self._uow_factory = uow_factory
        self._event_bus = event_bus
        self._audit = audit_service

    def handle(self, cmd: UpdateGroupCommand) -> Result[None, AppError]:
        target_account_id: Optional[str] = None
        with self._uow_factory() as uow:
            accounts = uow.accounts.list_all()
            group_found = False
            for acc in accounts:
                for g in acc.groups:
                    if g.id == cmd.group_id:
                        group_found = True
                        target_account_id = acc.id
                        if cmd.name is not None:
                            g.name = cmd.name.strip()
                        if cmd.role is not None:
                            g.role = cmd.role.upper()
                        if cmd.members is not None:
                            g.members = max(0, cmd.members)
                        if cmd.posting_permission is not None:
                            g.posting_permission = cmd.posting_permission.upper()
                        if cmd.notes is not None:
                            g.notes = cmd.notes
                        g.last_synced_at = format_iso(utcnow())
                        uow.accounts.add(acc)
                        break
                if group_found:
                    break

            if not group_found or not target_account_id:
                return Failure(NotFoundError(f"Group '{cmd.group_id}' not found."))

            uow.commit()

        self._audit.record(
            event_type="group.updated",
            target_type="group",
            target_id=cmd.group_id,
            details={"account_id": target_account_id},
        )
        self._event_bus.publish(
            GroupUpdatedEvent(account_id=target_account_id, group_id=cmd.group_id)
        )
        return Success(None)


@dataclass(frozen=True, kw_only=True)
class DeleteGroupCommand(Command):
    """Command to detach a Group from an account."""

    group_id: str


class DeleteGroupHandler(CommandHandler[DeleteGroupCommand, None]):
    """Handles removing a Group."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        event_bus: EventBus,
        audit_service: AuditService,
    ) -> None:
        self._uow_factory = uow_factory
        self._event_bus = event_bus
        self._audit = audit_service

    def handle(self, cmd: DeleteGroupCommand) -> Result[None, AppError]:
        target_account_id: Optional[str] = None
        with self._uow_factory() as uow:
            accounts = uow.accounts.list_all()
            removed = False
            for acc in accounts:
                for i, g in enumerate(acc.groups):
                    if g.id == cmd.group_id:
                        target_account_id = acc.id
                        acc.groups.pop(i)
                        uow.accounts.add(acc)
                        removed = True
                        break
                if removed:
                    break

            if not removed or not target_account_id:
                return Failure(NotFoundError(f"Group '{cmd.group_id}' not found."))

            uow.commit()

        self._audit.record(
            event_type="group.deleted",
            target_type="group",
            target_id=cmd.group_id,
            details={"account_id": target_account_id},
        )
        self._event_bus.publish(
            GroupDeletedEvent(account_id=target_account_id, group_id=cmd.group_id)
        )
        return Success(None)
