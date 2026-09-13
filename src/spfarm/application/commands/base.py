"""Command abstractions and CommandBus for CQRS pattern."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Generic, Type, TypeVar

from spfarm.shared.errors import AppError, NotFoundError
from spfarm.shared.result import Failure, Result

C = TypeVar("C", bound="Command")
R = TypeVar("R")


@dataclass(frozen=True, kw_only=True)
class Command:
    """Base class for all state-mutating commands."""

    correlation_id: str | None = None


class CommandHandler(ABC, Generic[C, R]):
    """Abstract interface for handling a specific command type."""

    @abstractmethod
    def handle(self, command: C) -> Result[R, AppError]:
        """Process the command and return a typed Result."""
        raise NotImplementedError


class CommandBus:
    """In-process bus that routes commands to registered handlers."""

    def __init__(self) -> None:
        self._handlers: dict[
            Type[Command], CommandHandler[Any, Any] | Callable[[Any], Result[Any, AppError]]
        ] = {}

    def register(
        self,
        command_type: Type[C],
        handler: CommandHandler[C, R] | Callable[[C], Result[R, AppError]],
    ) -> None:
        """Register a handler for a specific command class."""
        self._handlers[command_type] = handler

    def dispatch(self, command: Command) -> Result[Any, AppError]:
        """Dispatch command to its registered handler."""
        cmd_type = type(command)
        handler = self._handlers.get(cmd_type)
        if not handler:
            return Failure(NotFoundError(f"No command handler registered for {cmd_type.__name__}"))

        if isinstance(handler, CommandHandler):
            return handler.handle(command)
        return handler(command)

    @property
    def registered_commands(self) -> list[str]:
        """Return names of all registered commands."""
        return [cmd.__name__ for cmd in self._handlers]
