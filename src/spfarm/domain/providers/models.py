"""Provider, Network, Location, and Audit domain entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from spfarm.domain.enums import AppChannel, NetworkProfileType
from spfarm.shared.ids import generate_id
from spfarm.shared.time import format_iso


@dataclass(kw_only=True)
class NetworkProfile:
    """A configured network egress profile (direct, proxy, or VPN)."""

    id: str = field(default_factory=generate_id)
    name: str
    profile_type: NetworkProfileType = NetworkProfileType.DIRECT
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password_secret_ref: Optional[str] = None
    is_active: bool = True
    created_at: str = field(default_factory=format_iso)


@dataclass(kw_only=True)
class LocationProfile:
    """A QA or test mock geographic location profile."""

    id: str = field(default_factory=generate_id)
    name: str
    latitude: float
    longitude: float
    country_code: str = "US"
    city: str = "Default City"
    is_active: bool = True
    created_at: str = field(default_factory=format_iso)


@dataclass(kw_only=True)
class AppPackage:
    """An approved mobile application version catalog item."""

    id: str = field(default_factory=generate_id)
    channel: AppChannel
    package_name: str
    version_name: str
    version_code: int = 1
    min_android_version: str = "9.0"
    is_approved: bool = True
    sha256_hash: Optional[str] = None
    created_at: str = field(default_factory=format_iso)


@dataclass(kw_only=True)
class ProviderAccount:
    """External service integration account (e.g. Meta App, Mail service)."""

    id: str = field(default_factory=generate_id)
    provider_type: str  # META, GMAIL, OUTLOOK, etc.
    name: str
    credentials_secret_ref: Optional[str] = None
    is_active: bool = True
    created_at: str = field(default_factory=format_iso)


@dataclass(kw_only=True)
class AuditEvent:
    """Immutable audit record of a user or system action."""

    id: str = field(default_factory=generate_id)
    event_type: str
    actor: str = "SYSTEM"
    target_type: str
    target_id: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=format_iso)
