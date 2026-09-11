"""Domain and application events for account lifecycle changes."""

from __future__ import annotations

from dataclasses import dataclass

from spfarm.application.events.base import Event


@dataclass(frozen=True, kw_only=True)
class AccountCreatedEvent(Event):
    """Emitted when a new account is registered."""

    account_id: str
    display_name: str


@dataclass(frozen=True, kw_only=True)
class AccountUpdatedEvent(Event):
    """Emitted when account profile metadata or fields change."""

    account_id: str


@dataclass(frozen=True, kw_only=True)
class AccountArchivedEvent(Event):
    """Emitted when an account is moved to the archive."""

    account_id: str


@dataclass(frozen=True, kw_only=True)
class AccountRestoredEvent(Event):
    """Emitted when an archived account is restored to active status."""

    account_id: str


@dataclass(frozen=True, kw_only=True)
class AccountDeletedEvent(Event):
    """Emitted when an account is permanently removed."""

    account_id: str


@dataclass(frozen=True, kw_only=True)
class AccountStatusChangedEvent(Event):
    """Emitted when an account operational status transitions."""

    account_id: str
    old_status: str
    new_status: str
