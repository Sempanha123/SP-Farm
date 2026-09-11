"""Unit tests for secret store implementations and ref utilities."""

from pathlib import Path

import pytest

from spfarm.infrastructure.secrets.encrypted_file import EncryptedFileSecretStore
from spfarm.infrastructure.secrets.keyring_store import KeyringSecretStore
from spfarm.infrastructure.secrets.ref import is_secret_ref, make_secret_ref, parse_secret_ref


def test_secret_ref_utilities() -> None:
    ref = make_secret_ref("accounts", "acc_100", "password")
    assert ref == "vault://accounts/acc_100/password"
    assert is_secret_ref(ref) is True

    cat, eid, key = parse_secret_ref(ref)
    assert cat == "accounts"
    assert eid == "acc_100"
    assert key == "password"

    assert is_secret_ref("invalid://ref") is False
    assert is_secret_ref("vault://accounts/acc_100") is False

    with pytest.raises(ValueError):
        parse_secret_ref("invalid://ref")


def test_encrypted_file_secret_store(tmp_path: Path) -> None:
    vault_file = tmp_path / "vault.enc"
    key_file = tmp_path / ".key"

    store = EncryptedFileSecretStore(vault_file=vault_file, key_file=key_file)
    ref = "vault://accounts/acc_01/token"
    val = "sample_val_" + "secret_token_123"

    assert store.has_secret(ref) is False
    assert store.retrieve_secret(ref) is None

    # Store secret
    store.store_secret(ref, val)
    assert store.has_secret(ref) is True
    assert store.retrieve_secret(ref) == val

    # Verify on-disk file is encrypted and does NOT contain plaintext value
    raw_disk_bytes = vault_file.read_bytes()
    assert val.encode("utf-8") not in raw_disk_bytes

    # Simulate new store instance with existing key/vault file
    store2 = EncryptedFileSecretStore(vault_file=vault_file, key_file=key_file)
    assert store2.has_secret(ref) is True
    assert store2.retrieve_secret(ref) == val

    # Delete secret
    assert store.delete_secret(ref) is True
    assert store.has_secret(ref) is False
    assert store.retrieve_secret(ref) is None
    assert store.delete_secret(ref) is False


def test_keyring_secret_store_fallback(tmp_path: Path) -> None:
    # Use explicit fallback store in temp path
    fallback = EncryptedFileSecretStore(
        vault_file=tmp_path / "fb_vault.enc",
        key_file=tmp_path / "fb_key",
    )

    store = KeyringSecretStore(
        service_name="spfarm_test_vault",
        fallback_store=fallback,
    )

    ref = "vault://accounts/acc_02/cookie"
    val = "sample_val_" + "cookie_payload_abc"

    store.store_secret(ref, val)
    assert store.has_secret(ref) is True
    assert store.retrieve_secret(ref) == val

    assert store.delete_secret(ref) is True
    assert store.has_secret(ref) is False
