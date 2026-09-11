"""SqlAlchemy implementation of the domain UnitOfWork interface."""

from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

from sqlalchemy.orm import Session, sessionmaker

from spfarm.domain.interfaces.unit_of_work import IUnitOfWork
from spfarm.infrastructure.database.repositories.account_repo import AccountRepository
from spfarm.infrastructure.database.repositories.device_repo import DeviceRepository
from spfarm.infrastructure.database.repositories.environment_repo import EnvironmentRepository
from spfarm.infrastructure.database.repositories.job_repo import JobRepository
from spfarm.infrastructure.database.session import create_session_factory


class SqlAlchemyUnitOfWork(IUnitOfWork):
    """Transactional Unit of Work using SQLAlchemy sessions."""

    def __init__(self, session_factory: Optional[sessionmaker[Session]] = None) -> None:
        self._session_factory = session_factory or create_session_factory()
        self._session: Optional[Session] = None

    @property
    def session(self) -> Session:
        if self._session is None:
            raise RuntimeError("UnitOfWork has not been entered. Use 'with uow:' context.")
        return self._session

    def __enter__(self) -> SqlAlchemyUnitOfWork:
        self._session = self._session_factory()
        self.accounts = AccountRepository(self._session)
        self.environments = EnvironmentRepository(self._session)
        self.devices = DeviceRepository(self._session)
        self.jobs = JobRepository(self._session)
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._session is not None:
            if exc_type is not None:
                self.rollback()
            self._session.close()
            self._session = None

    def commit(self) -> None:
        """Commit current transaction."""
        self.session.commit()

    def rollback(self) -> None:
        """Rollback current transaction."""
        if self._session is not None:
            self.session.rollback()
