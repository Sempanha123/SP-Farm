"""Event abstractions and in-process EventBus for decoupled messaging."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Generic, Type, TypeVar

from spfarm.shared.ids import generate_id
from spfarm.shared.time import format_iso

E = TypeVar("E", bound="Event")


@dataclass(frozen=True, kw_only=True)
class Event:
    """Base class for all domain and application events."""

    id: str = field(default_factory=generate_id)
    occurred_at: str = field(default_factory=format_iso)
    correlation_id: str | None = None


class EventHandler(Generic[E]):
    """Interface for processing published events."""

    def handle(self, event: E) -> None:
        """Handle the published event."""
        raise NotImplementedError


class EventBus:
    """In-process publisher/subscriber event bus."""

    def __init__(self) -> None:
        self._subscribers: dict[Type[Event], list[Callable[[Any], None]]] = {}
        self._all_events_subscribers: list[Callable[[Event], None]] = []

    def subscribe(
        self,
        event_type: Type[E],
        handler: Callable[[E], None],
    ) -> None:
        """Subscribe a handler callback to a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def subscribe_all(self, handler: Callable[[Event], None]) -> None:
        """Subscribe a handler to observe every published event."""
        self._all_events_subscribers.append(handler)

    def unsubscribe(
        self,
        event_type: Type[E],
        handler: Callable[[E], None],
    ) -> None:
        """Unsubscribe a handler from a specific event type."""
        if event_type in self._subscribers and handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)

    def publish(self, event: Event) -> None:
        """Publish an event to all subscribed handlers."""
        event_type = type(event)

        # 1. Notify specific subscribers
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                try:
                    handler(event)
                except Exception as exc:
                    # Log or handle subscriber exceptions without failing publisher
                    print(f"[EventBus] Error in subscriber for {event_type.__name__}: {exc}")

        # 2. Notify catch-all subscribers
        for global_handler in self._all_events_subscribers:
            try:
                global_handler(event)
            except Exception as exc:
                print(f"[EventBus] Error in global subscriber for {event_type.__name__}: {exc}")

    @property
    def total_subscribers_count(self) -> int:
        """Return total count of registered event subscriptions."""
        return sum(len(subs) for subs in self._subscribers.values()) + len(self._all_events_subscribers)

    @property
    def subscribed_event_types(self) -> list[str]:
        """Return names of all event types with active subscribers."""
        return [evt.__name__ for evt in self._subscribers]
