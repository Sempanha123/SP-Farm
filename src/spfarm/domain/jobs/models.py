"""Persistent Job and execution tracking domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from spfarm.domain.enums import JobPriority, JobStatus
from spfarm.shared.errors import ValidationError
from spfarm.shared.ids import generate_id
from spfarm.shared.time import format_iso, utcnow


@dataclass(kw_only=True)
class JobAttempt:
    """Record of an individual execution attempt for a persistent job."""

    id: str = field(default_factory=generate_id)
    job_id: str
    attempt_number: int
    started_at: str = field(default_factory=format_iso)
    ended_at: Optional[str] = None
    status: JobStatus = JobStatus.RUNNING
    error_message: Optional[str] = None


@dataclass(kw_only=True)
class Job:
    """A persistent background work unit managed by the job engine."""

    id: str = field(default_factory=generate_id)
    job_type: str
    target_account_id: Optional[str] = None
    target_device_id: Optional[str] = None
    target_environment_id: Optional[str] = None
    status: JobStatus = JobStatus.PENDING
    priority: JobPriority = JobPriority.NORMAL
    attempts: int = 0
    max_attempts: int = 3
    progress_pct: int = 0
    payload: dict[str, Any] = field(default_factory=dict)
    result_data: Optional[dict[str, Any]] = None
    error_message: Optional[str] = None

    created_at: str = field(default_factory=format_iso)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    def start(self, device_id: Optional[str] = None) -> JobAttempt:
        """Mark job as running and record attempt."""
        if self.status not in (JobStatus.PENDING, JobStatus.QUEUED, JobStatus.RETRYING):
            raise ValidationError(f"Cannot start job in status {self.status.value}")

        self.status = JobStatus.RUNNING
        self.started_at = format_iso(utcnow())
        if device_id:
            self.target_device_id = device_id
        self.attempts += 1

        return JobAttempt(
            job_id=self.id,
            attempt_number=self.attempts,
            status=JobStatus.RUNNING,
        )

    def complete(self, result_data: Optional[dict[str, Any]] = None) -> None:
        """Mark job as successfully finished."""
        self.status = JobStatus.COMPLETED
        self.progress_pct = 100
        self.completed_at = format_iso(utcnow())
        self.result_data = result_data or {}

    def fail(self, error_message: str) -> None:
        """Record a failure, transitioning to RETRYING or FAILED."""
        self.error_message = error_message
        if self.attempts < self.max_attempts:
            self.status = JobStatus.RETRYING
        else:
            self.status = JobStatus.FAILED
            self.completed_at = format_iso(utcnow())

    def cancel(self) -> None:
        """Cancel the job."""
        if self.status in (JobStatus.COMPLETED, JobStatus.FAILED):
            raise ValidationError(f"Cannot cancel a {self.status.value} job")
        self.status = JobStatus.CANCELLED
        self.completed_at = format_iso(utcnow())

    @property
    def can_retry(self) -> bool:
        return self.status == JobStatus.RETRYING and self.attempts < self.max_attempts
