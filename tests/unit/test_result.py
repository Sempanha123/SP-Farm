"""Tests for functional Result monad and AppError taxonomy."""

import pytest

from spfarm.shared.errors import AppError, NotFoundError, ValidationError
from spfarm.shared.result import Failure, Result, Success


def test_success_properties() -> None:
    res: Result[int, AppError] = Success(42)
    assert res.is_success is True
    assert res.is_failure is False
    assert res.unwrap() == 42
    assert res.unwrap_or(0) == 42


def test_failure_properties() -> None:
    err = NotFoundError("Item not found")
    res: Result[int, AppError] = Failure(err)
    assert res.is_success is False
    assert res.is_failure is True
    assert res.unwrap_or(100) == 100

    with pytest.raises(NotFoundError):
        res.unwrap()


def test_result_map() -> None:
    res_success: Result[int, str] = Success(10)
    mapped_success = res_success.map(lambda x: x * 2)
    assert mapped_success.unwrap() == 20

    res_fail: Result[int, str] = Failure("error")
    mapped_fail = res_fail.map(lambda x: x * 2)
    assert mapped_fail.is_failure is True
    assert mapped_fail.unwrap_or(0) == 0


def test_result_and_then() -> None:
    def parse_even(val: int) -> Result[int, str]:
        if val % 2 == 0:
            return Success(val)
        return Failure("Not even")

    res1: Result[int, str] = Success(4)
    assert res1.and_then(parse_even).unwrap() == 4

    res2: Result[int, str] = Success(5)
    assert res2.and_then(parse_even).is_failure is True


def test_app_error_attributes() -> None:
    err = ValidationError("Bad input", details={"field": "email"}, correlation_id="cid-123")
    assert err.code == "VALIDATION_ERROR"
    assert err.message == "Bad input"
    assert err.details["field"] == "email"
    assert err.correlation_id == "cid-123"
