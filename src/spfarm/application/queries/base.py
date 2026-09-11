"""Query abstractions and QueryBus for CQRS pattern."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Generic, Type, TypeVar

from spfarm.shared.errors import AppError, NotFoundError
from spfarm.shared.result import Failure, Result

Q = TypeVar("Q", bound="Query")
R = TypeVar("R")


@dataclass(frozen=True)
class Query:
    """Base class for all read-only queries."""

    pass


class QueryHandler(ABC, Generic[Q, R]):
    """Abstract interface for handling a specific query type."""

    @abstractmethod
    def handle(self, query: Q) -> Result[R, AppError]:
        """Execute the query and return a typed Result."""
        raise NotImplementedError


class QueryBus:
    """In-process bus that routes queries to registered query handlers."""

    def __init__(self) -> None:
        self._handlers: dict[
            Type[Query], QueryHandler[Any, Any] | Callable[[Any], Result[Any, AppError]]
        ] = {}

    def register(
        self,
        query_type: Type[Q],
        handler: QueryHandler[Q, R] | Callable[[Q], Result[R, AppError]],
    ) -> None:
        """Register a handler for a specific query class."""
        self._handlers[query_type] = handler

    def dispatch(self, query: Query) -> Result[Any, AppError]:
        """Dispatch query to its registered handler."""
        q_type = type(query)
        handler = self._handlers.get(q_type)
        if not handler:
            return Failure(NotFoundError(f"No query handler registered for {q_type.__name__}"))

        if isinstance(handler, QueryHandler):
            return handler.handle(query)
        return handler(query)

    @property
    def registered_queries(self) -> list[str]:
        """Return names of all registered queries."""
        return [q.__name__ for q in self._handlers]
