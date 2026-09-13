"""Domain interfaces package."""

from spfarm.domain.interfaces.device_provider import IDeviceProvider
from spfarm.domain.interfaces.secret_store import ISecretStore
from spfarm.domain.interfaces.unit_of_work import IUnitOfWork

__all__ = ["IDeviceProvider", "ISecretStore", "IUnitOfWork"]
