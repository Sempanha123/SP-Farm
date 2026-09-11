"""Application CQRS queries package."""

from spfarm.application.queries.base import Query, QueryBus, QueryHandler
from spfarm.application.queries.dashboard import (
    DashboardDataDTO,
    DashboardMetricsDTO,
    DashboardQueryService,
    GetDashboardDataQuery,
)

__all__ = [
    "DashboardDataDTO",
    "DashboardMetricsDTO",
    "DashboardQueryService",
    "GetDashboardDataQuery",
    "Query",
    "QueryBus",
    "QueryHandler",
]
