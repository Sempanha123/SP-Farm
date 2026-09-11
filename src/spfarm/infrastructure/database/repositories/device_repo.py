"""Runtime Device and history repository implementation."""

from __future__ import annotations

import json
from typing import Optional

from sqlalchemy import select

from spfarm.domain.devices.models import RuntimeDevice, RuntimeHistoryRecord
from spfarm.domain.enums import DeviceHealth, DeviceProvider, DeviceState
from spfarm.infrastructure.database.models import RuntimeDeviceModel, RuntimeHistoryModel
from spfarm.infrastructure.database.repositories.base import BaseRepository


class DeviceRepository(BaseRepository[RuntimeDevice]):
    """Repository managing RuntimeDevice entities and execution history."""

    def add(self, device: RuntimeDevice) -> None:
        """Persist or update a RuntimeDevice."""
        model = self.session.get(RuntimeDeviceModel, device.id)
        if not model:
            model = RuntimeDeviceModel(
                id=device.id,
                provider=device.provider.value,
                provider_instance_id=device.provider_instance_id,
                friendly_name=device.friendly_name,
                adb_target=device.adb_target,
                last_seen_at=device.last_seen_at,
            )
            self.session.add(model)

        model.friendly_name = device.friendly_name
        model.adb_target = device.adb_target
        model.android_version = device.android_version
        model.manufacturer_display = device.manufacturer_display
        model.model_display = device.model_display
        model.state = device.state.value
        model.health = device.health.value
        model.capabilities_json = json.dumps(device.capabilities)
        model.current_job_id = device.current_job_id
        model.current_environment_id = device.current_environment_id
        model.last_seen_at = device.last_seen_at

    def get_by_id(self, device_id: str) -> Optional[RuntimeDevice]:
        """Retrieve a device by UUID."""
        model = self.session.get(RuntimeDeviceModel, device_id)
        if not model:
            return None
        return self._to_domain(model)

    def get_by_adb_target(self, adb_target: str) -> Optional[RuntimeDevice]:
        """Retrieve a device by ADB target string."""
        stmt = select(RuntimeDeviceModel).where(RuntimeDeviceModel.adb_target == adb_target)
        model = self.session.execute(stmt).scalar_one_or_none()
        if not model:
            return None
        return self._to_domain(model)

    def list_all(self) -> list[RuntimeDevice]:
        """List all known runtime devices."""
        stmt = select(RuntimeDeviceModel)
        models = self.session.execute(stmt).scalars().all()
        return [self._to_domain(m) for m in models]

    def add_history(self, record: RuntimeHistoryRecord) -> None:
        """Record an execution session history entry."""
        model = RuntimeHistoryModel(
            id=record.id,
            account_id=record.account_id,
            environment_id=record.environment_id,
            device_id=record.device_id,
            job_id=record.job_id,
            started_at=record.started_at,
            ended_at=record.ended_at,
            result_state=record.result_state,
            app_version=record.app_version,
            network_profile_id=record.network_profile_id,
            notes=record.notes,
        )
        self.session.add(model)

    def _to_domain(self, m: RuntimeDeviceModel) -> RuntimeDevice:
        caps = json.loads(m.capabilities_json) if m.capabilities_json else ["adb"]
        return RuntimeDevice(
            id=m.id,
            provider=DeviceProvider(m.provider),
            provider_instance_id=m.provider_instance_id,
            friendly_name=m.friendly_name,
            adb_target=m.adb_target,
            android_version=m.android_version,
            manufacturer_display=m.manufacturer_display,
            model_display=m.model_display,
            state=DeviceState(m.state),
            health=DeviceHealth(m.health),
            capabilities=caps,
            current_job_id=m.current_job_id,
            current_environment_id=m.current_environment_id,
            last_seen_at=m.last_seen_at,
        )
