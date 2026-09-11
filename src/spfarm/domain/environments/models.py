"""Account Environment Profile domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from spfarm.domain.enums import AppChannel, DeviceProvider
from spfarm.shared.ids import generate_id
from spfarm.shared.time import format_iso, utcnow

if TYPE_CHECKING:
    from spfarm.domain.devices.models import RuntimeDevice


@dataclass(kw_only=True)
class EnvironmentRevision:
    """Historical revision entry for an account environment configuration."""

    id: str = field(default_factory=generate_id)
    environment_id: str
    revision: int
    note: str = "Configuration update"
    created_at: str = field(default_factory=format_iso)
    snapshot: dict[str, str | int | None] = field(default_factory=dict)


@dataclass(kw_only=True)
class AccountEnvironmentProfile:
    """Persistent configuration profile bound to an account.

    Decoupled from runtime device hosts: may run on any compatible device.
    """

    id: str = field(default_factory=generate_id)
    account_id: str
    label: str = "Default Environment"
    status: str = "ACTIVE"
    revision: int = 1

    # Runtime host preferences
    preferred_device_provider: Optional[DeviceProvider] = None
    preferred_android_version: Optional[str] = None

    # Application package configuration
    app_channel: AppChannel = AppChannel.FACEBOOK_OFFICIAL
    app_package: str = "com.facebook.katana"
    app_version: Optional[str] = None

    # System parameters
    locale: str = "en_US"
    language: str = "en"
    timezone: str = "UTC"

    # Display configuration
    screen_width: int = 720
    screen_height: int = 1280
    density_dpi: int = 320
    orientation: str = "portrait"

    # Profile references
    network_profile_id: Optional[str] = None
    location_profile_id: Optional[str] = None
    permission_profile_id: Optional[str] = None
    notification_profile_id: Optional[str] = None
    storage_profile_id: Optional[str] = None

    # Secret and backup references (no raw tokens)
    session_vault_ref: Optional[str] = None
    app_state_backup_ref: Optional[str] = None

    # Transient runtime tracking
    last_runtime_device_id: Optional[str] = None
    last_restored_at: Optional[str] = None
    last_backup_at: Optional[str] = None

    created_at: str = field(default_factory=format_iso)
    updated_at: str = field(default_factory=format_iso)

    def is_compatible_with(self, device: RuntimeDevice) -> bool:
        """Evaluate whether a runtime device satisfies this environment's constraints."""
        # 1. Check provider preference if defined
        if self.preferred_device_provider and device.provider != self.preferred_device_provider:
            return False

        # 2. Check Android version requirement if defined
        if self.preferred_android_version and device.android_version:
            try:
                env_major = int(self.preferred_android_version.split(".")[0])
                dev_major = int(device.android_version.split(".")[0])
                if dev_major < env_major:
                    return False
            except (ValueError, IndexError):
                pass

        return True

    def bump_revision(self, note: str = "Configuration updated") -> EnvironmentRevision:
        """Increment revision and produce a revision snapshot."""
        self.revision += 1
        self.updated_at = format_iso(utcnow())

        snapshot = {
            "app_package": self.app_package,
            "app_version": self.app_version,
            "locale": self.locale,
            "language": self.language,
            "timezone": self.timezone,
            "screen_width": self.screen_width,
            "screen_height": self.screen_height,
            "density_dpi": self.density_dpi,
            "network_profile_id": self.network_profile_id,
            "location_profile_id": self.location_profile_id,
        }

        return EnvironmentRevision(
            environment_id=self.id,
            revision=self.revision,
            note=note,
            snapshot=snapshot,
        )
