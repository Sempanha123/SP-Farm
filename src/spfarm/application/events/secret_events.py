"""Audit events emitted when secrets are stored, retrieved, revealed, copied, or deleted."""

from __future__ import annotations

from dataclasses import dataclass

from spfarm.application.events.base import Event


@dataclass(frozen=True, kw_only=True)
class SecretRevealedEvent(Event):
    """Emitted when an operator explicitly reveals a secret value in the UI or CLI."""

    secret_ref: str
    actor: str = "operator"


@dataclass(frozen=True, kw_only=True)
class SecretCopiedEvent(Event):
    """Emitted when an operator explicitly copies a secret value to the system clipboard."""

    secret_ref: str
    actor: str = "operator"


@dataclass(frozen=True, kw_only=True)
class SecretStoredEvent(Event):
    """Emitted when a new secret is persisted into the vault."""

    secret_ref: str
    actor: str = "operator"


@dataclass(frozen=True, kw_only=True)
class SecretDeletedEvent(Event):
    """Emitted when a secret is permanently removed from the vault."""

    secret_ref: str
    actor: str = "operator"
