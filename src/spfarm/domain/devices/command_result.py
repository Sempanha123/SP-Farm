"""Generic device command execution result."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(frozen=True)
class DeviceCommandResult:
    """Standard outcome model returned by device provider operations."""

    success: bool
    message: str
    data: dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0
    error_code: Optional[str] = None

    @classmethod
    def ok(
        cls,
        message: str = "Success",
        data: Optional[dict[str, Any]] = None,
        duration_ms: float = 0.0,
    ) -> DeviceCommandResult:
        """Helper to create a successful command result."""
        return cls(
            success=True,
            message=message,
            data=data or {},
            duration_ms=duration_ms,
        )

    @classmethod
    def fail(
        cls,
        message: str,
        error_code: Optional[str] = None,
        data: Optional[dict[str, Any]] = None,
        duration_ms: float = 0.0,
    ) -> DeviceCommandResult:
        """Helper to create a failed command result."""
        return cls(
            success=False,
            message=message,
            error_code=error_code,
            data=data or {},
            duration_ms=duration_ms,
        )
