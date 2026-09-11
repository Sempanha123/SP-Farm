"""Generic functional Result monad for explicit error handling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, Union

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")
F = TypeVar("F")


@dataclass(frozen=True, slots=True)
class Success(Generic[T]):
    """Represents a successful computation outcome."""

    value: T

    @property
    def is_success(self) -> bool:
        return True

    @property
    def is_failure(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self.value

    def unwrap_or(self, _default: T) -> T:
        return self.value

    def map(self, fn: Callable[[T], U]) -> Result[U, E]:
        return Success(fn(self.value))

    def map_err(self, _fn: Callable[[E], F]) -> Result[T, F]:
        return Success(self.value)

    def and_then(self, fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return fn(self.value)


@dataclass(frozen=True, slots=True)
class Failure(Generic[E]):
    """Represents a failed computation outcome."""

    error: E

    @property
    def is_success(self) -> bool:
        return False

    @property
    def is_failure(self) -> bool:
        return True

    def unwrap(self) -> T:
        if isinstance(self.error, Exception):
            raise self.error
        raise ValueError(f"Called unwrap on a Failure: {self.error}")

    def unwrap_or(self, default: T) -> T:
        return default

    def map(self, _fn: Callable[[T], U]) -> Result[U, E]:
        return Failure(self.error)

    def map_err(self, fn: Callable[[E], F]) -> Result[T, F]:
        return Failure(fn(self.error))

    def and_then(self, _fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return Failure(self.error)


Result = Union[Success[T], Failure[E]]
