"""Infrastructure device adapters package."""

from spfarm.infrastructure.devices.fake_provider import FakeDeviceProvider
from spfarm.infrastructure.devices.ldplayer.provider import LDPlayerProvider

__all__ = ["FakeDeviceProvider", "LDPlayerProvider"]
