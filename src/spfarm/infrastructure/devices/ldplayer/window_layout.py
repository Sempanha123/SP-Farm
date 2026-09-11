"""Window layout and display management for LDPlayer emulator instances."""

from __future__ import annotations

import logging

from spfarm.domain.devices.command_result import DeviceCommandResult
from spfarm.infrastructure.devices.ldplayer.provider import LDPlayerProvider

logger = logging.getLogger(__name__)


class LDPlayerWindowLayoutService:
    """Arranges, sorts, and aligns emulator windows across operators' monitors."""

    def __init__(self, provider: LDPlayerProvider) -> None:
        self.provider = provider

    def align_grid(self) -> DeviceCommandResult:
        """Trigger native LDPlayer window grid sorting."""
        if not self.provider.is_available:
            return DeviceCommandResult.fail(
                "LDPlayer is not installed or available", "NOT_AVAILABLE"
            )

        return self.provider.sort_windows()
