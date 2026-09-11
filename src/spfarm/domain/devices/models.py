"""Runtime device and allocation domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from spfarm.domain.enums import DeviceHealth, DeviceProvider, DeviceState
from spfarm.shared.errors import ConflictError
from spfarm.shared.ids import generate_id
from spfarm.shared.time import format_iso, utcnow


@dataclass(kw_only=True)
class DeviceLease:
    """Ephemeral lease reserving a runtime device for an environment and job."""

    id: str = field(default_factory=generate_id)
    device_id: str
    environment_id: str
    job_id: Optional[str] = None
    lease_token: str = field(default_factory=generate_id)
    acquired_at: str = field(default_factory=format_iso)
    expires_at: Optional[str] = None
    released_at: Optional[str] = None
    is_active: bool = True

    def release(self) -> None:
        """Mark the lease as released."""
        self.is_active = False
        self.released_at = format_iso(utcnow())


@dataclass(kw_only=True)
class RuntimeDevice:
    """A physical Android device or emulator instance execution host."""

    id: str = field(default_factory=generate_id)
    provider: DeviceProvider
    provider_instance_id: str
    friendly_name: str
    adb_target: str
    android_version: str = "12"
    manufacturer_display: str = "Android"
    model_display: str = "Generic Device"
    state: DeviceState = DeviceState.READY
    health: DeviceHealth = DeviceHealth.HEALTHY
    capabilities: list[str] = field(default_factory=lambda: ["adb", "touch", "apk_install"])

    # Current execution assignment
    current_job_id: Optional[str] = None
    current_environment_id: Optional[str] = None
    current_lease: Optional[DeviceLease] = None
    last_seen_at: str = field(default_factory=format_iso)

    @property
    def is_available(self) -> bool:
        """Check if device is ready and unassigned."""
        return self.state == DeviceState.READY and self.current_environment_id is None

    def reserve(self, environment_id: str, job_id: Optional[str] = None) -> DeviceLease:
        """Reserve this device for an environment/job execution."""
        if not self.is_available:
            raise ConflictError(
                f"Device '{self.friendly_name}' is not available for reservation (state={self.state.value})"
            )

        lease = DeviceLease(
            device_id=self.id,
            environment_id=environment_id,
            job_id=job_id,
        )
        self.current_lease = lease
        self.current_environment_id = environment_id
        self.current_job_id = job_id
        self.state = DeviceState.RESERVED
        return lease

    def release(self) -> None:
        """Release current lease and return device to ready state."""
        if self.current_lease and self.current_lease.is_active:
            self.current_lease.release()

        self.current_lease = None
        self.current_environment_id = None
        self.current_job_id = None
        self.state = DeviceState.READY

    def set_state(self, new_state: DeviceState) -> None:
        """Update device operational state."""
        self.state = new_state
        self.last_seen_at = format_iso(utcnow())


@dataclass(kw_only=True)
class RuntimeHistoryRecord:
    """Historical record of an account environment run on a runtime device."""

    id: str = field(default_factory=generate_id)
    account_id: str
    environment_id: str
    device_id: str
    job_id: Optional[str] = None
    started_at: str = field(default_factory=format_iso)
    ended_at: Optional[str] = None
    result_state: str = "SUCCESS"  # SUCCESS, FAILED, TIMEOUT, CANCELLED
    app_version: Optional[str] = None
    network_profile_id: Optional[str] = None
    notes: Optional[str] = None
