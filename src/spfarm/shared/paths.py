"""Configurable application paths using pathlib."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppPaths:
    """Resolved and configurable paths for the application runtime."""

    base_dir: Path
    data_dir: Path
    logs_dir: Path
    backups_dir: Path
    cache_dir: Path
    secrets_dir: Path
    database_file: Path

    @classmethod
    def resolve(cls) -> AppPaths:
        """Resolve paths from environment variables or sensible OS defaults."""
        # 1. Base data directory
        env_data = os.getenv("SPFARM_DATA_DIR")
        if env_data:
            base = Path(env_data).resolve()
        else:
            local_app_data = os.getenv("LOCALAPPDATA")
            if local_app_data:
                base = (Path(local_app_data) / "spfarm").resolve()
            else:
                base = (Path.home() / ".spfarm").resolve()

        # 2. Subdirectories with optional specific environment overrides
        data = base / "data"
        logs = Path(os.getenv("SPFARM_LOG_DIR")).resolve() if os.getenv("SPFARM_LOG_DIR") else base / "logs"
        backups = Path(os.getenv("SPFARM_BACKUP_DIR")).resolve() if os.getenv("SPFARM_BACKUP_DIR") else base / "backups"
        cache = Path(os.getenv("SPFARM_CACHE_DIR")).resolve() if os.getenv("SPFARM_CACHE_DIR") else base / "cache"
        secrets = base / "secrets"

        # 3. Database path
        db_file = data / "spfarm.db"

        return cls(
            base_dir=base,
            data_dir=data,
            logs_dir=logs,
            backups_dir=backups,
            cache_dir=cache,
            secrets_dir=secrets,
            database_file=db_file,
        )

    def ensure_directories(self) -> None:
        """Create standard runtime directories if they do not already exist."""
        for path in (
            self.base_dir,
            self.data_dir,
            self.logs_dir,
            self.backups_dir,
            self.cache_dir,
            self.secrets_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)


# Global default instance
paths = AppPaths.resolve()
