"""Sanitized diagnostics dump service with recursive secret redaction."""

from __future__ import annotations

import json
import logging
import platform
import re
import sys
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional

from spfarm.application.events.base import EventBus
from spfarm.domain.interfaces.unit_of_work import IUnitOfWork
from spfarm.shared.paths import paths
from spfarm.shared.settings import SettingsManager
from spfarm.shared.time import format_iso

if TYPE_CHECKING:
    from spfarm.application.services.device_registry import DeviceRegistry
    from spfarm.infrastructure.automation.adb.service import AdbService
    from spfarm.infrastructure.automation.appium.service import AppiumServiceManager
    from spfarm.infrastructure.automation.sessions.pool import AppiumSessionPool

logger = logging.getLogger(__name__)

# Patterns matching sensitive key names
SENSITIVE_KEYS_PATTERN = re.compile(
    r"(password|secret|token|cookie|session|seed|totp|credential|auth|authorization|private_key|apikey|api_key|passphrase)",
    re.IGNORECASE,
)

# Pattern matching embedded credentials in URIs: scheme://user:password@host
URI_CREDENTIAL_PATTERN = re.compile(r"([a-zA-Z][a-zA-Z0-9+.-]*://)([^:]+):([^@]+)@")


def redact_sensitive_data(data: Any, mask: str = "[REDACTED]") -> Any:
    """Recursively sanitize any data structure by redacting sensitive keys and values.

    Guarantees that credentials, tokens, session cookies, and passwords are never
    leaked into exported diagnostics or crash logs.
    """
    if isinstance(data, dict):
        cleaned: dict[str, Any] = {}
        for k, v in data.items():
            key_str = str(k)
            if isinstance(v, dict):
                cleaned[key_str] = redact_sensitive_data(v, mask=mask)
            elif isinstance(v, (list, tuple, set)):
                if SENSITIVE_KEYS_PATTERN.search(key_str):
                    # Sensitive collection (e.g. recovery_codes: [...])
                    cleaned[key_str] = [mask for _ in v] if isinstance(v, list) else mask
                else:
                    cleaned[key_str] = redact_sensitive_data(v, mask=mask)
            elif SENSITIVE_KEYS_PATTERN.search(key_str):
                cleaned[key_str] = mask
            else:
                cleaned[key_str] = redact_sensitive_data(v, mask=mask)
        return cleaned

    if isinstance(data, list):
        return [redact_sensitive_data(item, mask=mask) for item in data]

    if isinstance(data, tuple):
        return tuple(redact_sensitive_data(item, mask=mask) for item in data)

    if isinstance(data, set):
        return {redact_sensitive_data(item, mask=mask) for item in data}

    if isinstance(data, str):
        # Redact URI embedded credentials
        if "://" in data and "@" in data:
            data = URI_CREDENTIAL_PATTERN.sub(r"\1\2:" + mask + "@", data)
        return data

    if hasattr(data, "model_dump") and callable(data.model_dump):
        return redact_sensitive_data(data.model_dump(), mask=mask)

    if hasattr(data, "__dict__"):
        return redact_sensitive_data(vars(data), mask=mask)

    return data


class DiagnosticsService:
    """Collects runtime state, system information, and sanitized configuration for support reports."""

    def __init__(
        self,
        settings_manager: Optional[SettingsManager] = None,
        event_bus: Optional[EventBus] = None,
        uow_factory: Optional[Callable[[], IUnitOfWork]] = None,
        device_registry: Optional["DeviceRegistry"] = None,
        adb_service: Optional["AdbService"] = None,
        appium_manager: Optional["AppiumServiceManager"] = None,
        session_pool: Optional["AppiumSessionPool"] = None,
    ) -> None:
        self._settings_manager = settings_manager
        self._event_bus = event_bus
        self._uow_factory = uow_factory
        self._device_registry = device_registry
        self._adb_service = adb_service
        self._appium_manager = appium_manager
        self._session_pool = session_pool

    def generate_dump(self) -> dict[str, Any]:
        """Compile a fully redacted diagnostics dump."""
        dump: dict[str, Any] = {
            "timestamp": format_iso(),
            "system": {
                "platform": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "python_version": sys.version,
                "python_executable": sys.executable,
            },
            "application_paths": {
                "base_dir": str(paths.base_dir),
                "data_dir": str(paths.data_dir),
                "logs_dir": str(paths.logs_dir),
                "backups_dir": str(paths.backups_dir),
                "cache_dir": str(paths.cache_dir),
                "secrets_dir": str(paths.secrets_dir),
                "database_file": str(paths.database_file),
                "database_file_exists": paths.database_file.exists(),
            },
        }

        # 1. Settings
        if self._settings_manager is not None:
            settings_data = self._settings_manager.get().model_dump()
            dump["settings"] = redact_sensitive_data(settings_data)
        else:
            dump["settings"] = None

        # 2. EventBus metrics
        if self._event_bus is not None:
            dump["event_bus"] = {
                "total_subscribers": self._event_bus.total_subscribers_count,
                "subscribed_event_types": self._event_bus.subscribed_event_types,
            }

        # 3. Database table counts (if UoW available)
        if self._uow_factory is not None:
            table_counts: dict[str, int | str] = {}
            try:
                with self._uow_factory() as uow:
                    try:
                        table_counts["accounts"] = len(uow.accounts.list_all())
                    except Exception as e:
                        table_counts["accounts"] = f"error: {e}"

                    try:
                        table_counts["environments"] = len(uow.environments.list_all())
                    except Exception as e:
                        table_counts["environments"] = f"error: {e}"

                    try:
                        table_counts["devices"] = len(uow.devices.list_all())
                    except Exception as e:
                        table_counts["devices"] = f"error: {e}"

                    try:
                        table_counts["jobs"] = len(uow.jobs.list_all())
                    except Exception as e:
                        table_counts["jobs"] = f"error: {e}"
            except Exception as exc:
                table_counts["status"] = f"unreachable: {exc}"

            dump["database_metrics"] = table_counts

        if self._adb_service is not None:
            dump["adb"] = self._adb_service.diagnostics()
        if self._appium_manager is not None:
            dump["appium"] = self._appium_manager.diagnostics()
        if self._session_pool is not None:
            dump["appium_sessions"] = self._session_pool.diagnostics()

        if self._device_registry is not None:
            devices = self._device_registry.get_all_devices()
            dump["device_providers"] = [
                {
                    "type": provider.provider_type.value,
                    "name": provider.provider_name,
                    "available": getattr(provider, "is_available", True),
                    "install_dir": str(getattr(getattr(provider, "runner", None), "install_dir", "") or ""),
                    "device_count": sum(
                        device.provider == provider.provider_type for device in devices
                    ),
                }
                for provider in self._device_registry.list_providers()
            ]
            dump["runtime_devices"] = [
                {
                    "id": device.id,
                    "provider": device.provider.value,
                    "friendly_name": device.friendly_name,
                    "adb_target": device.adb_target,
                    "state": device.state.value,
                    "health": device.health.value,
                    "capabilities": asdict(self._device_registry.get_capabilities(device.id)),
                }
                for device in devices
            ]

        return redact_sensitive_data(dump)

    def export_to_file(self, destination: Path) -> Path:
        """Write sanitized diagnostics dump to a JSON file."""
        dump = self.generate_dump()
        destination.parent.mkdir(parents=True, exist_ok=True)
        content = json.dumps(dump, indent=2)
        destination.write_text(content, encoding="utf-8")
        return destination
