"""Application error taxonomy for SP-Farm V2."""

from __future__ import annotations

from typing import Any


class AppError(Exception):
    """Base error class for all application and domain errors."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        details: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}
        self.correlation_id = correlation_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code!r}, message={self.message!r})"


class ValidationError(AppError):
    """Raised or returned when input or domain entity validation fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> None:
        super().__init__(
            message, code="VALIDATION_ERROR", details=details, correlation_id=correlation_id
        )


class NotFoundError(AppError):
    """Raised or returned when an entity or resource does not exist."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> None:
        super().__init__(message, code="NOT_FOUND", details=details, correlation_id=correlation_id)


class ConflictError(AppError):
    """Raised or returned when an operation conflicts with existing state."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> None:
        super().__init__(message, code="CONFLICT", details=details, correlation_id=correlation_id)


class UnauthorizedError(AppError):
    """Raised or returned when an action violates authorization or ownership rules."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> None:
        super().__init__(
            message, code="UNAUTHORIZED", details=details, correlation_id=correlation_id
        )


class InfrastructureError(AppError):
    """Raised or returned when low-level storage, database, or network fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> None:
        super().__init__(
            message, code="INFRASTRUCTURE_ERROR", details=details, correlation_id=correlation_id
        )


class DeviceError(AppError):
    """Raised or returned when device driver, ADB, or emulator operation fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> None:
        super().__init__(
            message, code="DEVICE_ERROR", details=details, correlation_id=correlation_id
        )


class ArchitectureViolationError(AppError):
    """Raised when an architectural boundary or import rule is violated."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> None:
        super().__init__(
            message, code="ARCHITECTURE_VIOLATION", details=details, correlation_id=correlation_id
        )
