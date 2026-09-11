"""Query service and DTOs for runtime devices workspace."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable, Optional

from spfarm.application.queries.base import Query
from spfarm.application.services.device_registry import DeviceRegistry
from spfarm.domain.devices.capabilities import DeviceCapabilities
from spfarm.domain.interfaces.unit_of_work import IUnitOfWork

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeviceSummaryDTO:
    """Consolidated summary representation of a runtime device."""

    id: str
    friendly_name: str
    provider: str
    adb_target: str
    android_version: str
    state: str
    health: str
    manufacturer: str
    model: str
    capabilities: list[str] = field(default_factory=list)
    current_environment_id: Optional[str] = None
    current_job_id: Optional[str] = None
    last_seen_at: Optional[str] = None


@dataclass(frozen=True)
class DeviceDetailDTO(DeviceSummaryDTO):
    """Rich detail representation of a runtime device including hardware specs."""

    capabilities_detail: Optional[DeviceCapabilities] = None
    resolution_display: str = "1080x1920 (320 DPI)"
    lease_token: Optional[str] = None


@dataclass(frozen=True)
class ListDevicesQuery(Query):
    """Query criteria for filtering runtime devices."""

    provider: Optional[str] = None
    state: Optional[str] = None
    health: Optional[str] = None
    search: Optional[str] = None


class DeviceQueryService:
    """Query service retrieving cached and registered runtime device details."""

    def __init__(
        self,
        registry: DeviceRegistry,
        uow_factory: Optional[Callable[[], IUnitOfWork]] = None,
    ) -> None:
        self.registry = registry
        self.uow_factory = uow_factory

    def list_devices(self, query: Optional[ListDevicesQuery] = None) -> list[DeviceSummaryDTO]:
        """List and filter runtime devices across the registered fleet."""
        devices = self.registry.get_all_devices()
        summaries: list[DeviceSummaryDTO] = []

        q_prov = (
            query.provider.upper()
            if (query and query.provider and query.provider != "ALL")
            else None
        )
        q_state = query.state.upper() if (query and query.state and query.state != "ALL") else None
        q_health = (
            query.health.upper() if (query and query.health and query.health != "ALL") else None
        )
        q_text = query.search.lower().strip() if (query and query.search) else None

        for d in devices:
            if q_prov and d.provider.value != q_prov:
                continue
            if q_state and d.state.value != q_state:
                continue
            if q_health and d.health.value != q_health:
                continue
            if q_text:
                match = (
                    q_text in d.friendly_name.lower()
                    or q_text in d.adb_target.lower()
                    or q_text in d.id.lower()
                    or q_text in d.manufacturer_display.lower()
                    or q_text in d.model_display.lower()
                )
                if not match:
                    continue

            summaries.append(
                DeviceSummaryDTO(
                    id=d.id,
                    friendly_name=d.friendly_name,
                    provider=d.provider.value,
                    adb_target=d.adb_target,
                    android_version=d.android_version,
                    state=d.state.value,
                    health=d.health.value,
                    manufacturer=d.manufacturer_display,
                    model=d.model_display,
                    capabilities=list(d.capabilities),
                    current_environment_id=d.current_environment_id,
                    current_job_id=d.current_job_id,
                    last_seen_at=d.last_seen_at,
                )
            )

        return summaries

    def get_device_detail(self, device_id: str) -> Optional[DeviceDetailDTO]:
        """Obtain detailed device information including capabilities."""
        device = self.registry.get_device(device_id)
        if not device:
            return None

        caps = self.registry.get_capabilities(device_id)
        lease_tok = device.current_lease.lease_token if device.current_lease else None

        return DeviceDetailDTO(
            id=device.id,
            friendly_name=device.friendly_name,
            provider=device.provider.value,
            adb_target=device.adb_target,
            android_version=device.android_version,
            state=device.state.value,
            health=device.health.value,
            manufacturer=device.manufacturer_display,
            model=device.model_display,
            capabilities=list(device.capabilities),
            current_environment_id=device.current_environment_id,
            current_job_id=device.current_job_id,
            last_seen_at=device.last_seen_at,
            capabilities_detail=caps,
            resolution_display=caps.resolution_str,
            lease_token=lease_tok,
        )
