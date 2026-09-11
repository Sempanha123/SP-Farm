"""Account Environment Profile repository implementation."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import select

from spfarm.domain.enums import AppChannel, DeviceProvider
from spfarm.domain.environments.models import AccountEnvironmentProfile
from spfarm.infrastructure.database.models import AccountEnvironmentProfileModel
from spfarm.infrastructure.database.repositories.base import BaseRepository


class EnvironmentRepository(BaseRepository[AccountEnvironmentProfile]):
    """Repository managing AccountEnvironmentProfile entities."""

    def add(self, env: AccountEnvironmentProfile) -> None:
        """Persist or update an AccountEnvironmentProfile."""
        model = self.session.get(AccountEnvironmentProfileModel, env.id)
        if not model:
            model = AccountEnvironmentProfileModel(
                id=env.id,
                account_id=env.account_id,
                label=env.label,
                created_at=env.created_at,
                updated_at=env.updated_at,
            )
            self.session.add(model)

        model.label = env.label
        model.status = env.status
        model.revision = env.revision
        model.preferred_device_provider = env.preferred_device_provider.value if env.preferred_device_provider else None
        model.preferred_android_version = env.preferred_android_version
        model.app_channel = env.app_channel.value
        model.app_package = env.app_package
        model.app_version = env.app_version
        model.locale = env.locale
        model.language = env.language
        model.timezone = env.timezone
        model.screen_width = env.screen_width
        model.screen_height = env.screen_height
        model.density_dpi = env.density_dpi
        model.orientation = env.orientation
        model.network_profile_id = env.network_profile_id
        model.location_profile_id = env.location_profile_id
        model.permission_profile_id = env.permission_profile_id
        model.notification_profile_id = env.notification_profile_id
        model.storage_profile_id = env.storage_profile_id
        model.session_vault_ref = env.session_vault_ref
        model.app_state_backup_ref = env.app_state_backup_ref
        model.last_runtime_device_id = env.last_runtime_device_id
        model.last_restored_at = env.last_restored_at
        model.last_backup_at = env.last_backup_at
        model.updated_at = env.updated_at

    def get_by_id(self, env_id: str) -> Optional[AccountEnvironmentProfile]:
        """Retrieve an environment profile by UUID."""
        model = self.session.get(AccountEnvironmentProfileModel, env_id)
        if not model:
            return None
        return self._to_domain(model)

    def get_by_account_id(self, account_id: str) -> list[AccountEnvironmentProfile]:
        """Retrieve all environment profiles for an account."""
        stmt = select(AccountEnvironmentProfileModel).where(AccountEnvironmentProfileModel.account_id == account_id)
        models = self.session.execute(stmt).scalars().all()
        return [self._to_domain(m) for m in models]

    def _to_domain(self, m: AccountEnvironmentProfileModel) -> AccountEnvironmentProfile:
        return AccountEnvironmentProfile(
            id=m.id,
            account_id=m.account_id,
            label=m.label,
            status=m.status,
            revision=m.revision,
            preferred_device_provider=DeviceProvider(m.preferred_device_provider) if m.preferred_device_provider else None,
            preferred_android_version=m.preferred_android_version,
            app_channel=AppChannel(m.app_channel),
            app_package=m.app_package,
            app_version=m.app_version,
            locale=m.locale,
            language=m.language,
            timezone=m.timezone,
            screen_width=m.screen_width,
            screen_height=m.screen_height,
            density_dpi=m.density_dpi,
            orientation=m.orientation,
            network_profile_id=m.network_profile_id,
            location_profile_id=m.location_profile_id,
            permission_profile_id=m.permission_profile_id,
            notification_profile_id=m.notification_profile_id,
            storage_profile_id=m.storage_profile_id,
            session_vault_ref=m.session_vault_ref,
            app_state_backup_ref=m.app_state_backup_ref,
            last_runtime_device_id=m.last_runtime_device_id,
            last_restored_at=m.last_restored_at,
            last_backup_at=m.last_backup_at,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )
