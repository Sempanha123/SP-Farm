"""Job repository implementation."""

from __future__ import annotations

import json
from typing import Optional

from sqlalchemy import select

from spfarm.domain.enums import JobPriority, JobStatus
from spfarm.domain.jobs.models import Job
from spfarm.infrastructure.database.models import JobModel
from spfarm.infrastructure.database.repositories.base import BaseRepository


class JobRepository(BaseRepository[Job]):
    """Repository managing persistent Job entities."""

    def add(self, job: Job) -> None:
        """Persist or update a Job entity."""
        model = self.session.get(JobModel, job.id)
        if not model:
            model = JobModel(
                id=job.id,
                job_type=job.job_type,
                created_at=job.created_at,
            )
            self.session.add(model)

        model.job_type = job.job_type
        model.target_account_id = job.target_account_id
        model.target_device_id = job.target_device_id
        model.target_environment_id = job.target_environment_id
        model.status = job.status.value
        model.priority = job.priority.value
        model.attempts = job.attempts
        model.max_attempts = job.max_attempts
        model.progress_pct = job.progress_pct
        model.payload_json = json.dumps(job.payload) if job.payload else None
        model.result_data_json = json.dumps(job.result_data) if job.result_data else None
        model.error_message = job.error_message
        model.started_at = job.started_at
        model.completed_at = job.completed_at

    def get_by_id(self, job_id: str) -> Optional[Job]:
        """Retrieve a job by UUID."""
        model = self.session.get(JobModel, job_id)
        if not model:
            return None
        return self._to_domain(model)

    def list_by_status(self, status: JobStatus) -> list[Job]:
        """List jobs matching a status."""
        stmt = select(JobModel).where(JobModel.status == status.value)
        models = self.session.execute(stmt).scalars().all()
        return [self._to_domain(m) for m in models]

    def _to_domain(self, m: JobModel) -> Job:
        payload = json.loads(m.payload_json) if m.payload_json else {}
        result_data = json.loads(m.result_data_json) if m.result_data_json else None

        return Job(
            id=m.id,
            job_type=m.job_type,
            target_account_id=m.target_account_id,
            target_device_id=m.target_device_id,
            target_environment_id=m.target_environment_id,
            status=JobStatus(m.status),
            priority=JobPriority(m.priority),
            attempts=m.attempts,
            max_attempts=m.max_attempts,
            progress_pct=m.progress_pct,
            payload=payload,
            result_data=result_data,
            error_message=m.error_message,
            created_at=m.created_at,
            started_at=m.started_at,
            completed_at=m.completed_at,
        )
