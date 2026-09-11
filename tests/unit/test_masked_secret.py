"""Unit tests for MaskedSecret and audit event emission."""

from pathlib import Path

from spfarm.application.events.base import EventBus
from spfarm.application.events.secret_events import (
    SecretCopiedEvent,
    SecretDeletedEvent,
    SecretRevealedEvent,
    SecretStoredEvent,
)
from spfarm.application.services.masked_secret import MaskedSecret
from spfarm.infrastructure.secrets.encrypted_file import EncryptedFileSecretStore


def test_masked_secret_lifecycle_and_auditing(tmp_path: Path) -> None:
    store = EncryptedFileSecretStore(
        vault_file=tmp_path / "vault.enc",
        key_file=tmp_path / "key",
    )
    bus = EventBus()
    events_received: list[str] = []

    bus.subscribe(SecretRevealedEvent, lambda e: events_received.append("revealed"))
    bus.subscribe(SecretCopiedEvent, lambda e: events_received.append("copied"))
    bus.subscribe(SecretStoredEvent, lambda e: events_received.append("stored"))
    bus.subscribe(SecretDeletedEvent, lambda e: events_received.append("deleted"))

    ref = "vault://accounts/acc_test/password"
    masked = MaskedSecret.from_ref(ref, store, label="Account Password")

    assert not masked.is_set
    assert str(masked) == "(not set)"
    assert "password" not in repr(masked) or "vault://" in repr(masked)

    # 1. Update (Store) secret
    val = "my_sample_" + "secret_value_999"
    masked.update(val, store, event_bus=bus, actor="test_operator")
    assert masked.is_set
    assert str(masked) == "••••••••"
    assert events_received == ["stored"]

    # 2. Reveal secret
    revealed = masked.reveal(store, event_bus=bus, actor="test_operator")
    assert revealed == val
    assert events_received == ["stored", "revealed"]

    # 3. Copy secret
    copied_container: list[str] = []
    success = masked.copy(
        store,
        clipboard_writer=lambda text: copied_container.append(text),
        event_bus=bus,
        actor="test_operator",
    )
    assert success is True
    assert copied_container == [val]
    assert events_received == ["stored", "revealed", "copied"]

    # 4. Clear secret
    deleted = masked.clear(store, event_bus=bus, actor="test_operator")
    assert deleted is True
    assert not masked.is_set
    assert events_received == ["stored", "revealed", "copied", "deleted"]
    assert masked.reveal(store, event_bus=bus) is None
