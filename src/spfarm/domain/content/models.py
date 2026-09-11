"""Content, Campaign, and Schedule domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from spfarm.domain.enums import PublishingStatus
from spfarm.shared.ids import generate_id
from spfarm.shared.time import format_iso


@dataclass(kw_only=True)
class ContentAsset:
    """A media asset (image, video, or creative) stored in the content library."""

    id: str = field(default_factory=generate_id)
    name: str
    file_path: str
    file_size_bytes: int = 0
    mime_type: str = "image/jpeg"
    sha256_hash: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    usage_count: int = 0
    created_at: str = field(default_factory=format_iso)


@dataclass(kw_only=True)
class Schedule:
    """Execution timing and cadence configuration."""

    id: str = field(default_factory=generate_id)
    name: str
    cron_expression: Optional[str] = None
    scheduled_at: Optional[str] = None
    timezone: str = "UTC"
    is_active: bool = True
    created_at: str = field(default_factory=format_iso)


@dataclass(kw_only=True)
class Campaign:
    """A multi-target posting or distribution campaign."""

    id: str = field(default_factory=generate_id)
    name: str
    status: PublishingStatus = PublishingStatus.DRAFT
    target_page_ids: list[str] = field(default_factory=list)
    content_asset_ids: list[str] = field(default_factory=list)
    schedule_id: Optional[str] = None
    post_caption: str = ""
    created_at: str = field(default_factory=format_iso)
