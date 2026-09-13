"""Masked secret UI model with audited reveal and copy operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from spfarm.application.events.base import EventBus
from spfarm.application.events.secret_events import (
    SecretCopiedEvent,
    SecretDeletedEvent,
    SecretRevealedEvent,
    SecretStoredEvent,
)
from spfarm.domain.interfaces.secret_store import ISecretStore


@dataclass
class MaskedSecret:
    """Masked view of a vault credential for display in UI, tables, and dialogs.

    Ensures that secrets are never accidentally leaked in string representation,
    and requires explicit audited operations to reveal or copy.
    """

    secret_ref: str
    is_set: bool = False
    masked_display: str = "••••••••"
    label: str = ""

    def __repr__(self) -> str:
        return f"MaskedSecret(ref='{self.secret_ref}', is_set={self.is_set}, display='{self.masked_display}')"

    def __str__(self) -> str:
        return self.masked_display if self.is_set else "(not set)"

    @classmethod
    def from_ref(cls, secret_ref: str, secret_store: ISecretStore, label: str = "") -> MaskedSecret:
        """Create a MaskedSecret by checking existence in the given store."""
        is_set = secret_store.has_secret(secret_ref)
        return cls(secret_ref=secret_ref, is_set=is_set, label=label)

    def reveal(
        self,
        secret_store: ISecretStore,
        event_bus: Optional[EventBus] = None,
        actor: str = "operator",
    ) -> str | None:
        """Explicitly retrieve the plaintext secret and publish an audit event."""
        if not self.is_set:
            return None

        val = secret_store.retrieve_secret(self.secret_ref)
        if val is not None and event_bus is not None:
            event_bus.publish(SecretRevealedEvent(secret_ref=self.secret_ref, actor=actor))
        return val

    def copy(
        self,
        secret_store: ISecretStore,
        clipboard_writer: Callable[[str], None],
        event_bus: Optional[EventBus] = None,
        actor: str = "operator",
    ) -> bool:
        """Explicitly write the plaintext secret to the clipboard and publish an audit event."""
        if not self.is_set:
            return False

        val = secret_store.retrieve_secret(self.secret_ref)
        if val is None:
            return False

        clipboard_writer(val)
        if event_bus is not None:
            event_bus.publish(SecretCopiedEvent(secret_ref=self.secret_ref, actor=actor))
        return True

    def update(
        self,
        new_value: str,
        secret_store: ISecretStore,
        event_bus: Optional[EventBus] = None,
        actor: str = "operator",
    ) -> None:
        """Store a new secret value and publish an audit event."""
        secret_store.store_secret(self.secret_ref, new_value)
        self.is_set = True
        if event_bus is not None:
            event_bus.publish(SecretStoredEvent(secret_ref=self.secret_ref, actor=actor))

    def clear(
        self,
        secret_store: ISecretStore,
        event_bus: Optional[EventBus] = None,
        actor: str = "operator",
    ) -> bool:
        """Delete secret value and publish an audit event."""
        deleted = secret_store.delete_secret(self.secret_ref)
        if deleted:
            self.is_set = False
            if event_bus is not None:
                event_bus.publish(SecretDeletedEvent(secret_ref=self.secret_ref, actor=actor))
        return deleted
