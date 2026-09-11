"""Thread-safe and async-safe correlation context for structured tracing."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Generator

from spfarm.shared.ids import generate_id

_correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")
_job_id_var: ContextVar[str] = ContextVar("job_id", default="")
_device_id_var: ContextVar[str] = ContextVar("device_id", default="")
_account_id_var: ContextVar[str] = ContextVar("account_id", default="")
_environment_id_var: ContextVar[str] = ContextVar("environment_id", default="")
_page_id_var: ContextVar[str] = ContextVar("page_id", default="")


def get_log_context() -> dict[str, str]:
    """Retrieve the current active correlation context metadata."""
    ctx: dict[str, str] = {}
    cid = _correlation_id_var.get()
    if cid:
        ctx["correlation_id"] = cid

    jid = _job_id_var.get()
    if jid:
        ctx["job_id"] = jid

    did = _device_id_var.get()
    if did:
        ctx["device_id"] = did

    aid = _account_id_var.get()
    if aid:
        ctx["account_id"] = aid

    eid = _environment_id_var.get()
    if eid:
        ctx["environment_id"] = eid

    pid = _page_id_var.get()
    if pid:
        ctx["page_id"] = pid

    return ctx


@contextmanager
def log_context(
    correlation_id: str | None = None,
    job_id: str | None = None,
    device_id: str | None = None,
    account_id: str | None = None,
    environment_id: str | None = None,
    page_id: str | None = None,
) -> Generator[dict[str, str], None, None]:
    """Context manager setting scoped correlation attributes for the current thread/task.

    Automatically restores previous context values when exiting the block.
    """
    tokens: list[tuple[ContextVar[Any], Any]] = []

    # If no correlation_id is provided and none active, generate one
    cid = correlation_id or _correlation_id_var.get() or generate_id()
    tokens.append((_correlation_id_var, _correlation_id_var.set(cid)))

    if job_id is not None:
        tokens.append((_job_id_var, _job_id_var.set(job_id)))

    if device_id is not None:
        tokens.append((_device_id_var, _device_id_var.set(device_id)))

    if account_id is not None:
        tokens.append((_account_id_var, _account_id_var.set(account_id)))

    if environment_id is not None:
        tokens.append((_environment_id_var, _environment_id_var.set(environment_id)))

    if page_id is not None:
        tokens.append((_page_id_var, _page_id_var.set(page_id)))

    try:
        yield get_log_context()
    finally:
        for var, token in reversed(tokens):
            var.reset(token)


def clear_log_context() -> None:
    """Clear all active correlation context variables."""
    _correlation_id_var.set("")
    _job_id_var.set("")
    _device_id_var.set("")
    _account_id_var.set("")
    _environment_id_var.set("")
    _page_id_var.set("")
