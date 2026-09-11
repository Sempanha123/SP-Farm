"""Encrypted file secret store using Fernet symmetric encryption."""

from __future__ import annotations

import json
import logging
import os
import threading
from pathlib import Path

from cryptography.fernet import Fernet

from spfarm.domain.interfaces.secret_store import ISecretStore
from spfarm.shared.paths import paths

logger = logging.getLogger(__name__)


class EncryptedFileSecretStore(ISecretStore):
    """File-backed secret store using Fernet (AES-128-CBC + HMAC-SHA256).

    Ensures zero plaintext credentials on disk, atomic file persistence,
    and restricted file permissions (0o600).
    """

    def __init__(
        self,
        vault_file: Path | None = None,
        key_file: Path | None = None,
        master_key: bytes | None = None,
    ) -> None:
        self._vault_file = vault_file or (paths.secrets_dir / "vault.enc")
        self._key_file = key_file or (paths.secrets_dir / ".vault_key")
        self._lock = threading.RLock()

        if master_key is not None:
            self._fernet = Fernet(master_key)
        else:
            key = self._load_or_create_key()
            self._fernet = Fernet(key)

        self._cache: dict[str, str] | None = None

    def _set_restricted_permissions(self, path: Path) -> None:
        """Apply strict 0o600 permissions where supported (POSIX)."""
        try:
            if hasattr(os, "chmod") and os.name != "nt":
                os.chmod(path, 0o600)
        except Exception:
            pass

    def _load_or_create_key(self) -> bytes:
        """Load existing master key or generate a new cryptographically strong 256-bit Fernet key."""
        self._key_file.parent.mkdir(parents=True, exist_ok=True)
        if self._key_file.exists():
            return self._key_file.read_bytes().strip()

        key = Fernet.generate_key()
        temp_key = self._key_file.with_suffix(".tmp")
        temp_key.write_bytes(key)
        self._set_restricted_permissions(temp_key)
        temp_key.replace(self._key_file)
        self._set_restricted_permissions(self._key_file)
        return key

    def _read_vault(self) -> dict[str, str]:
        """Read and decrypt the vault payload from disk."""
        if not self._vault_file.exists():
            return {}

        try:
            encrypted_data = self._vault_file.read_bytes()
            if not encrypted_data:
                return {}
            decrypted_json = self._fernet.decrypt(encrypted_data).decode("utf-8")
            return json.loads(decrypted_json)
        except Exception as exc:
            logger.error("Failed to decrypt secret vault at %s: %s", self._vault_file, exc)
            return {}

    def _write_vault(self, data: dict[str, str]) -> None:
        """Encrypt and atomically write the vault payload to disk."""
        self._vault_file.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(data).encode("utf-8")
        encrypted = self._fernet.encrypt(payload)

        temp_file = self._vault_file.with_suffix(".tmp")
        temp_file.write_bytes(encrypted)
        self._set_restricted_permissions(temp_file)
        temp_file.replace(self._vault_file)
        self._set_restricted_permissions(self._vault_file)

    def store_secret(self, ref: str, value: str) -> None:
        """Store a secret under the given reference."""
        with self._lock:
            data = self._read_vault()
            data[ref] = value
            self._write_vault(data)
            self._cache = data

    def retrieve_secret(self, ref: str) -> str | None:
        """Retrieve a secret under the given reference, or None if not found."""
        with self._lock:
            if self._cache is None:
                self._cache = self._read_vault()
            return self._cache.get(ref)

    def delete_secret(self, ref: str) -> bool:
        """Delete a secret under the given reference."""
        with self._lock:
            data = self._read_vault()
            if ref in data:
                del data[ref]
                self._write_vault(data)
                self._cache = data
                return True
            return False

    def has_secret(self, ref: str) -> bool:
        """Check if a secret exists under the given reference."""
        with self._lock:
            if self._cache is None:
                self._cache = self._read_vault()
            return ref in self._cache
