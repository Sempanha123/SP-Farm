"""Lightweight dependency container for managing application services and buses."""

from __future__ import annotations

from typing import Any, Callable, Type, TypeVar

from spfarm.application.commands.base import CommandBus
from spfarm.application.events.base import EventBus
from spfarm.application.queries.base import QueryBus
from spfarm.shared.paths import AppPaths, paths

T = TypeVar("T")


class Container:
    """Dependency container providing service registration and resolution."""

    def __init__(self) -> None:
        self._singletons: dict[Type[Any] | str, Any] = {}
        self._factories: dict[Type[Any] | str, Callable[[], Any]] = {}

        # Register foundational buses and utilities
        self.register_singleton(AppPaths, paths)
        self.register_singleton(CommandBus, CommandBus())
        self.register_singleton(QueryBus, QueryBus())
        self.register_singleton(EventBus, EventBus())

        # Register Unit of Work factory
        from spfarm.domain.interfaces.unit_of_work import IUnitOfWork
        from spfarm.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork

        self.register_factory(IUnitOfWork, lambda: SqlAlchemyUnitOfWork())

    def register_singleton(self, service_type: Type[T] | str, instance: T) -> None:
        """Register an existing object as a singleton service."""
        self._singletons[service_type] = instance

    def register_factory(self, service_type: Type[T] | str, factory: Callable[[], T]) -> None:
        """Register a factory callable that creates a new instance on each resolve."""
        self._factories[service_type] = factory

    def resolve(self, service_type: Type[T] | str) -> T:
        """Resolve an instance for the requested service type or key."""
        if service_type in self._singletons:
            return self._singletons[service_type]

        if service_type in self._factories:
            return self._factories[service_type]()

        raise KeyError(f"Service {service_type} has not been registered in the Container.")

    @property
    def command_bus(self) -> CommandBus:
        return self.resolve(CommandBus)

    @property
    def query_bus(self) -> QueryBus:
        return self.resolve(QueryBus)

    @property
    def event_bus(self) -> EventBus:
        return self.resolve(EventBus)

    @property
    def app_paths(self) -> AppPaths:
        return self.resolve(AppPaths)

    @property
    def registered_service_names(self) -> list[str]:
        keys: list[str] = []
        for k in self._singletons:
            keys.append(k.__name__ if hasattr(k, "__name__") else str(k))
        for k in self._factories:
            keys.append(k.__name__ if hasattr(k, "__name__") else str(k))
        return keys


# Global default container instance
container = Container()
