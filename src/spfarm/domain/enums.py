"""Domain enums and state constants for SP-Farm V2."""

from enum import Enum


class AccountStatus(str, Enum):
    """Lifecycle and operational status of a managed account."""

    ACTIVE = "ACTIVE"
    RESTRICTED = "RESTRICTED"
    CHECKPOINT = "CHECKPOINT"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"


class AccountHealthState(str, Enum):
    """Informational security and health assessment of an account."""

    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    REQUIRES_ATTENTION = "REQUIRES_ATTENTION"
    UNKNOWN = "UNKNOWN"


class DeviceProvider(str, Enum):
    """Supported runtime device host providers."""

    LDPLAYER = "LDPLAYER"
    MUMU = "MUMU"
    PHYSICAL_ANDROID = "PHYSICAL_ANDROID"


class DeviceState(str, Enum):
    """Runtime allocation state of a physical device or emulator instance."""

    OFFLINE = "OFFLINE"
    READY = "READY"
    RESERVED = "RESERVED"
    RUNNING = "RUNNING"
    COOLDOWN = "COOLDOWN"
    ERROR = "ERROR"


class DeviceHealth(str, Enum):
    """Operational health score of a runtime device."""

    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


class JobStatus(str, Enum):
    """Lifecycle status of a persistent background job."""

    PENDING = "PENDING"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    RETRYING = "RETRYING"


class JobPriority(str, Enum):
    """Scheduling priority for the persistent job queue."""

    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"


class PublishingStatus(str, Enum):
    """Publishing state for posts and media."""

    DRAFT = "DRAFT"
    SCHEDULED = "SCHEDULED"
    PUBLISHING = "PUBLISHING"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"


class TwoFactorMethod(str, Enum):
    """Configured two-factor authentication method."""

    NONE = "NONE"
    TOTP = "TOTP"
    SMS = "SMS"
    SECURITY_KEY = "SECURITY_KEY"


class NetworkProfileType(str, Enum):
    """Network connection routing type."""

    DIRECT = "DIRECT"
    PROXY = "PROXY"
    VPN = "VPN"


class AppChannel(str, Enum):
    """Approved mobile application package channel."""

    FACEBOOK_OFFICIAL = "com.facebook.katana"
    FACEBOOK_LITE = "com.facebook.lite"
