"""Tests for CommandBus, QueryBus, EventBus, and Container."""

from dataclasses import dataclass

from spfarm.application.commands.base import Command, CommandBus, CommandHandler
from spfarm.application.events.base import Event, EventBus
from spfarm.application.queries.base import Query, QueryBus, QueryHandler
from spfarm.infrastructure.container import Container
from spfarm.shared.errors import AppError
from spfarm.shared.result import Result, Success


# Example Domain Event
@dataclass(frozen=True, kw_only=True)
class AccountCreatedEvent(Event):
    account_id: str = ""
    account_name: str = ""


# Example Command & Handler
@dataclass(frozen=True, kw_only=True)
class CreateAccountCommand(Command):
    account_id: str
    account_name: str


class CreateAccountHandler(CommandHandler[CreateAccountCommand, str]):
    def __init__(self, event_bus: EventBus) -> None:
        self.event_bus = event_bus

    def handle(self, command: CreateAccountCommand) -> Result[str, AppError]:
        # Publish domain event upon handling
        self.event_bus.publish(
            AccountCreatedEvent(
                account_id=command.account_id,
                account_name=command.account_name,
                correlation_id=command.correlation_id,
            )
        )
        return Success(command.account_id)


# Example Query & Handler
@dataclass(frozen=True)
class GetAccountCountQuery(Query):
    pass


class GetAccountCountHandler(QueryHandler[GetAccountCountQuery, int]):
    def handle(self, _query: GetAccountCountQuery) -> Result[int, AppError]:
        return Success(42)


def test_command_bus_dispatches_and_emits_event() -> None:
    event_bus = EventBus()
    command_bus = CommandBus()

    received_events: list[AccountCreatedEvent] = []

    def on_account_created(event: AccountCreatedEvent) -> None:
        received_events.append(event)

    event_bus.subscribe(AccountCreatedEvent, on_account_created)

    handler = CreateAccountHandler(event_bus)
    command_bus.register(CreateAccountCommand, handler)

    cmd = CreateAccountCommand(account_id="acc-001", account_name="Test Account", correlation_id="cid-999")
    result = command_bus.dispatch(cmd)

    assert result.is_success is True
    assert result.unwrap() == "acc-001"
    assert len(received_events) == 1
    assert received_events[0].account_id == "acc-001"
    assert received_events[0].account_name == "Test Account"
    assert received_events[0].correlation_id == "cid-999"


def test_query_bus_dispatches() -> None:
    query_bus = QueryBus()
    query_bus.register(GetAccountCountQuery, GetAccountCountHandler())

    res = query_bus.dispatch(GetAccountCountQuery())
    assert res.is_success is True
    assert res.unwrap() == 42


def test_unregistered_command_returns_failure() -> None:
    @dataclass(frozen=True)
    class UnknownCommand(Command):
        pass

    bus = CommandBus()
    res = bus.dispatch(UnknownCommand())
    assert res.is_failure is True
    assert "No command handler registered" in res.error.message


def test_container_resolves_singletons() -> None:
    cnt = Container()
    assert isinstance(cnt.command_bus, CommandBus)
    assert isinstance(cnt.query_bus, QueryBus)
    assert isinstance(cnt.event_bus, EventBus)
    assert cnt.command_bus is cnt.resolve(CommandBus)
