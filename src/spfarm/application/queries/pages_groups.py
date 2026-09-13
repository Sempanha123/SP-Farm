"""Query service and DTOs for Facebook Pages and Groups workspace."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Callable, Optional

from spfarm.application.queries.base import Query
from spfarm.domain.interfaces.unit_of_work import IUnitOfWork

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PageSummaryDTO:
    """Consolidated representation of a Facebook Page."""

    id: str
    account_id: str
    account_name: str
    platform_page_id: str
    name: str
    category: str
    followers: int
    status: str
    publishing_enabled: bool
    last_synced_at: Optional[str] = None
    last_published_at: Optional[str] = None
    notes: Optional[str] = None


@dataclass(frozen=True)
class GroupSummaryDTO:
    """Consolidated representation of a Facebook Group."""

    id: str
    account_id: str
    account_name: str
    platform_group_id: str
    name: str
    role: str
    members: int
    posting_permission: str
    last_synced_at: Optional[str] = None
    notes: Optional[str] = None


@dataclass(frozen=True)
class ListPagesQuery(Query):
    """Query to list managed Facebook Pages."""

    account_id: Optional[str] = None
    search: str = ""
    category: Optional[str] = None


@dataclass(frozen=True)
class ListGroupsQuery(Query):
    """Query to list joined and managed Facebook Groups."""

    account_id: Optional[str] = None
    search: str = ""
    role: Optional[str] = None


class PagesAndGroupsQueryService:
    """Service providing fast projections for Pages and Groups."""

    def __init__(self, uow_factory: Callable[[], IUnitOfWork]) -> None:
        self._uow_factory = uow_factory

    def list_pages(
        self,
        account_id: Optional[str] = None,
        search: str = "",
        category: Optional[str] = None,
    ) -> list[PageSummaryDTO]:
        """Query all pages with optional account and keyword filters."""
        results: list[PageSummaryDTO] = []
        search_lower = search.strip().lower()

        try:
            with self._uow_factory() as uow:
                accounts = uow.accounts.list_all()
                for acc in accounts:
                    if account_id and acc.id != account_id:
                        continue

                    for p in acc.pages:
                        if category and p.category.lower() != category.lower():
                            continue

                        if search_lower:
                            matches_name = search_lower in p.name.lower()
                            matches_id = search_lower in p.platform_page_id.lower()
                            matches_notes = search_lower in (p.notes or "").lower()
                            if not (matches_name or matches_id or matches_notes):
                                continue

                        results.append(
                            PageSummaryDTO(
                                id=p.id,
                                account_id=acc.id,
                                account_name=acc.display_name,
                                platform_page_id=p.platform_page_id,
                                name=p.name,
                                category=p.category,
                                followers=p.followers,
                                status=p.status,
                                publishing_enabled=p.publishing_enabled,
                                last_synced_at=p.last_synced_at,
                                last_published_at=p.last_published_at,
                                notes=p.notes,
                            )
                        )
        except Exception as exc:
            logger.warning("Could not list pages from UnitOfWork: %s", exc)
            return []

        return results

    def list_groups(
        self,
        account_id: Optional[str] = None,
        search: str = "",
        role: Optional[str] = None,
    ) -> list[GroupSummaryDTO]:
        """Query all groups with optional account and keyword filters."""
        results: list[GroupSummaryDTO] = []
        search_lower = search.strip().lower()

        try:
            with self._uow_factory() as uow:
                accounts = uow.accounts.list_all()
                for acc in accounts:
                    if account_id and acc.id != account_id:
                        continue

                    for g in acc.groups:
                        if role and g.role.upper() != role.upper():
                            continue

                        if search_lower:
                            matches_name = search_lower in g.name.lower()
                            matches_id = search_lower in g.platform_group_id.lower()
                            matches_notes = search_lower in (g.notes or "").lower()
                            if not (matches_name or matches_id or matches_notes):
                                continue

                        results.append(
                            GroupSummaryDTO(
                                id=g.id,
                                account_id=acc.id,
                                account_name=acc.display_name,
                                platform_group_id=g.platform_group_id,
                                name=g.name,
                                role=g.role,
                                members=g.members,
                                posting_permission=g.posting_permission,
                                last_synced_at=g.last_synced_at,
                                notes=g.notes,
                            )
                        )
        except Exception as exc:
            logger.warning("Could not list groups from UnitOfWork: %s", exc)
            return []

        return results
