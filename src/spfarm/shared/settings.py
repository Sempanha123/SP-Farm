"""Typed application settings and thread-safe atomic configuration management."""

from __future__ import annotations

import contextlib
import json
import logging
import os
import shutil
import threading
from pathlib import Path
from typing import Callable

from pydantic import BaseModel, Field

from spfarm.shared.paths import paths

logger = logging.getLogger(__name__)


class GeneralSettings(BaseModel):
    """General application settings."""

    app_name: str = "SP-Farm V2"
    environment: str = "production"  # production, development, test
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR


class AppearanceSettings(BaseModel):
    """Visual theme and display settings adhering to the Cute Light Design System."""

    theme: str = "light_blue"  # light_blue, pink, lavender, dark_blue, system
    scale_factor: float = Field(default=1.0, ge=0.5, le=3.0)
    window_width: int = Field(default=1280, ge=800)
    window_height: int = Field(default=800, ge=600)
    enable_animations: bool = True


class StorageSettings(BaseModel):
    """Application directories and retention configuration."""

    data_dir: str = ""
    logs_dir: str = ""
    backups_dir: str = ""
    cache_dir: str = ""
    auto_backup_enabled: bool = True
    auto_backup_interval_hours: int = Field(default=24, ge=1, le=168)
    max_retained_backups: int = Field(default=7, ge=1, le=100)


class DevicesSettings(BaseModel):
    """Device pool and emulator execution configuration."""

    adb_path: str = ""
    ldplayer_path: str = ""
    mumu_path: str = ""
    poll_interval_seconds: float = Field(default=5.0, ge=1.0, le=60.0)
    auto_discover_devices: bool = True
    default_device_pool: str = "default"


class AutomationSettings(BaseModel):
    """Safe automation engine parameters."""

    default_timeout_seconds: int = Field(default=60, ge=10, le=600)
    max_concurrent_jobs: int = Field(default=3, ge=1, le=20)
    human_emulation_level: str = "standard"  # low, standard, high
    delay_jitter_percent: float = Field(default=20.0, ge=0.0, le=100.0)


class SetupSettings(BaseModel):
    """First-run onboarding state."""

    is_first_run: bool = True
    wizard_completed: bool = False


class AppSettings(BaseModel):
    """Root typed configuration model for SP-Farm V2.

    CRITICAL SECURITY NOTICE:
    This model and its serialized representation must NEVER contain plaintext
    credentials, tokens, session keys, or passwords. All secrets are stored
    in the secure vault and referenced via secret refs.
    """

    general: GeneralSettings = Field(default_factory=GeneralSettings)
    appearance: AppearanceSettings = Field(default_factory=AppearanceSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    devices: DevicesSettings = Field(default_factory=DevicesSettings)
    automation: AutomationSettings = Field(default_factory=AutomationSettings)
    setup: SetupSettings = Field(default_factory=SetupSettings)


class SettingsManager:
    """Thread-safe manager for loading, updating, and atomically saving AppSettings."""

    def __init__(self, settings_file: Path | None = None) -> None:
        self._settings_file = settings_file or paths.settings_file
        self._lock = threading.RLock()
        self._settings: AppSettings | None = None

    @property
    def settings_file(self) -> Path:
        return self._settings_file

    def get(self) -> AppSettings:
        """Get current settings, loading from disk if not yet cached."""
        with self._lock:
            if self._settings is None:
                self._settings = self.load()
            return self._settings

    def load(self) -> AppSettings:
        """Load settings from JSON file with error recovery for corrupt data."""
        with self._lock:
            if not self._settings_file.exists():
                logger.info(
                    "Settings file not found at %s. Using default settings.", self._settings_file
                )
                self._settings = AppSettings()
                return self._settings

            try:
                content = self._settings_file.read_text(encoding="utf-8")
                data = json.loads(content)
                self._settings = AppSettings.model_validate(data)
                return self._settings
            except Exception as exc:
                logger.warning(
                    "Failed to read or parse settings file at %s: %s. Preserving backup and resetting defaults.",
                    self._settings_file,
                    exc,
                )
                # Create a backup of the corrupted file for safety
                backup_corrupt = self._settings_file.with_suffix(".json.corrupt")
                with contextlib.suppress(Exception):
                    shutil.copyfile(self._settings_file, backup_corrupt)
                self._settings = AppSettings()
                return self._settings

    def save(self, settings: AppSettings | None = None) -> AppSettings:
        """Atomically persist settings to disk using a temporary file and atomic rename."""
        with self._lock:
            if settings is not None:
                self._settings = settings
            elif self._settings is None:
                self._settings = AppSettings()

            # Ensure parent directory exists
            self._settings_file.parent.mkdir(parents=True, exist_ok=True)

            temp_file = self._settings_file.with_suffix(".tmp")
            json_data = self._settings.model_dump_json(indent=2)

            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(json_data)
                f.flush()
                os.fsync(f.fileno())

            # Atomic replace
            temp_file.replace(self._settings_file)
            return self._settings

    def update(self, mutator: Callable[[AppSettings], None]) -> AppSettings:
        """Apply a mutation function to the current settings and atomically persist."""
        with self._lock:
            current = self.get()
            mutator(current)
            return self.save(current)

    def reset(self) -> AppSettings:
        """Reset settings to default values and persist."""
        with self._lock:
            self._settings = AppSettings()
            return self.save(self._settings)
