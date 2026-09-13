"""OS Keyring and Windows Credential Manager integration with encrypted fallback."""

from __future__ import annotations

import contextlib
import logging
from typing import Optional

import keyring
import keyring.errors

from spfarm.domain.interfaces.secret_store import ISecretStore
from spfarm.infrastructure.secrets.encrypted_file import EncryptedFileSecretStore

logger = logging.getLogger(__name__)

DEFAULT_SERVICE_NAME = "spfarm_vault"


class KeyringSecretStore(ISecretStore):
    """Secure secret store backed by the OS Keyring (Windows Credential Manager / DPAPI)

    with seamless automatic fallback to local Fernet encryption when running headless or in CI.
    """

    def __init__(
        self,
        service_name: str = DEFAULT_SERVICE_NAME,
        fallback_store: Optional[EncryptedFileSecretStore] = None,
    ) -> None:
        self._service_name = service_name
        self._fallback_store = fallback_store or EncryptedFileSecretStore()
        self._keyring_available: bool | None = None

    def _check_keyring_usable(self) -> bool:
        """Check if keyring backend is operational and not a dummy/fail backend."""
        if self._keyring_available is not None:
            return self._keyring_available

        try:
            backend = keyring.get_keyring()
            backend_name = backend.__class__.__name__.lower()
            # If keyring backend is explicitly a dummy/fail backend (like in headless linux without gnome-keyring)
            if "fail" in backend_name or "null" in backend_name:
                logger.info(
                    "Keyring backend is %s; using EncryptedFileSecretStore fallback.", backend_name
                )
                self._keyring_available = False
                return False

            # Test a temporary probe
            test_key = "__spfarm_probe__"
            keyring.set_password(self._service_name, test_key, "probe_val")
            val = keyring.get_password(self._service_name, test_key)
            with contextlib.suppress(Exception):
                keyring.delete_password(self._service_name, test_key)

            if val == "probe_val":
                self._keyring_available = True
                return True
            else:
                self._keyring_available = False
                return False
        except Exception as exc:
            logger.warning(
                "OS Keyring check failed (%s). Defaulting to encrypted fallback vault.", exc
            )
            self._keyring_available = False
            return False

    @property
    def is_keyring_active(self) -> bool:
        """True if the OS Keyring / Windows Credential Manager is operational."""
        return self._check_keyring_usable()

    def store_secret(self, ref: str, value: str) -> None:
        """Store secret into OS Keyring or fallback store."""
        if self._check_keyring_usable():
            try:
                keyring.set_password(self._service_name, ref, value)
                return
            except Exception as exc:
                logger.warning(
                    "Failed storing secret in keyring (%s); storing in fallback vault.", exc
                )

        # Use encrypted fallback
        self._fallback_store.store_secret(ref, value)

    def retrieve_secret(self, ref: str) -> str | None:
        """Retrieve secret from OS Keyring, falling back to encrypted file if needed."""
        if self._check_keyring_usable():
            try:
                val = keyring.get_password(self._service_name, ref)
                if val is not None:
                    return val
            except Exception as exc:
                logger.warning(
                    "Failed retrieving secret from keyring (%s); checking fallback vault.", exc
                )

        return self._fallback_store.retrieve_secret(ref)

    def delete_secret(self, ref: str) -> bool:
        """Delete secret from both OS Keyring and fallback store."""
        deleted_from_keyring = False
        if self._check_keyring_usable():
            try:
                keyring.delete_password(self._service_name, ref)
                deleted_from_keyring = True
            except keyring.errors.PasswordDeleteError:
                pass
            except Exception as exc:
                logger.warning("Error deleting secret from keyring: %s", exc)

        deleted_from_fallback = self._fallback_store.delete_secret(ref)
        return deleted_from_keyring or deleted_from_fallback

    def has_secret(self, ref: str) -> bool:
        """Check whether secret exists in either OS Keyring or fallback store."""
        return self.retrieve_secret(ref) is not None
