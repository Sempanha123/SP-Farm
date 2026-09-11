"""Interface definition for secure secret storage."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ISecretStore(ABC):
    """Abstract interface for storing and retrieving sensitive secrets by URI reference."""

    @abstractmethod
    def store_secret(self, ref: str, value: str) -> None:
        """Store a sensitive secret value associated with the given secret reference."""
        raise NotImplementedError

    @abstractmethod
    def retrieve_secret(self, ref: str) -> str | None:
        """Retrieve the sensitive secret value associated with the given reference, or None."""
        raise NotImplementedError

    @abstractmethod
    def delete_secret(self, ref: str) -> bool:
        """Delete a sensitive secret by its reference. Returns True if deleted, False otherwise."""
        raise NotImplementedError

    @abstractmethod
    def has_secret(self, ref: str) -> bool:
        """Check whether a secret exists for the given reference."""
        raise NotImplementedError
