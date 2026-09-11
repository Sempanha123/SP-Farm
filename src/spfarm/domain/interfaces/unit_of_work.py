"""Unit of Work interface definition for domain transactional boundaries."""

from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Type


class IUnitOfWork(ABC):
    """Abstract interface for managing database transaction boundaries without leaking ORM details."""

    @abstractmethod
    def __enter__(self) -> IUnitOfWork:
        """Begin transaction / unit of work context."""
        raise NotImplementedError

    @abstractmethod
    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit unit of work, automatically rolling back if an exception occurred."""
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        """Persist changes committed within this unit of work."""
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        """Rollback changes made within this unit of work."""
        raise NotImplementedError
