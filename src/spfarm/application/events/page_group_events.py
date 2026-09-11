"""Domain and application events for Page and Group management."""

from __future__ import annotations

from dataclasses import dataclass

from spfarm.application.events.base import Event


@dataclass(frozen=True, kw_only=True)
class PageAddedEvent(Event):
    """Emitted when a Facebook Page is attached to an account."""

    account_id: str
    page_id: str
    page_name: str


@dataclass(frozen=True, kw_only=True)
class PageUpdatedEvent(Event):
    """Emitted when Page settings or metadata update."""

    account_id: str
    page_id: str


@dataclass(frozen=True, kw_only=True)
class PageDeletedEvent(Event):
    """Emitted when a Page is detached from an account."""

    account_id: str
    page_id: str


@dataclass(frozen=True, kw_only=True)
class GroupAddedEvent(Event):
    """Emitted when a Facebook Group is attached to an account."""

    account_id: str
    group_id: str
    group_name: str


@dataclass(frozen=True, kw_only=True)
class GroupUpdatedEvent(Event):
    """Emitted when Group settings or metadata update."""

    account_id: str
    group_id: str


@dataclass(frozen=True, kw_only=True)
class GroupDeletedEvent(Event):
    """Emitted when a Group is detached from an account."""

    account_id: str
    group_id: str
