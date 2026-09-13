"""Infrastructure device adapters package."""

from spfarm.infrastructure.devices.android.provider import PhysicalAndroidProvider
from spfarm.infrastructure.devices.fake_provider import FakeDeviceProvider
from spfarm.infrastructure.devices.ldplayer.provider import LDPlayerProvider
from spfarm.infrastructure.devices.mumu.provider import MuMuProvider

__all__ = ["FakeDeviceProvider", "LDPlayerProvider", "MuMuProvider", "PhysicalAndroidProvider"]
