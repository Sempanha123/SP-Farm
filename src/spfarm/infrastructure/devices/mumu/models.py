"""Data models and output parsers for MuMu Player emulator instances."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

# Base ADB port for MuMu 12 instances (index 0 is 16384, each step adds 32)
MUMU_BASE_ADB_PORT = 16384
MUMU_PORT_STEP = 32


@dataclass(frozen=True)
class MuMuInstanceInfo:
    """Descriptor for a MuMu Player emulator instance."""

    index: int
    title: str
    is_running: bool
    adb_port: int
    pid: int = 0
    name: str = ""

    def __post_init__(self) -> None:
        if not self.name:
            object.__setattr__(self, "name", self.title)

    @property
    def adb_target(self) -> str:
        """ADB target connection address."""
        return f"127.0.0.1:{self.adb_port}"

    @classmethod
    def calculate_default_port(cls, index: int) -> int:
        """Default port allocation algorithm for MuMu 12."""
        return MUMU_BASE_ADB_PORT + (index * MUMU_PORT_STEP)

    @classmethod
    def from_dict(cls, data: dict) -> Optional[MuMuInstanceInfo]:
        """Parse dictionary item from MuMuManager JSON output."""
        try:
            idx = int(data.get("index", data.get("id", 0)))
            title = str(data.get("title", data.get("name", f"MuMuPlayer-{idx}")))
            name = str(data.get("name", title))
            if "is_running" in data:
                is_run = bool(data["is_running"])
            else:
                status = str(data.get("status", data.get("state", ""))).lower()
                is_run = status in {"running", "started", "ready", "1", "true"}
            port = int(data.get("adb_port", cls.calculate_default_port(idx)))
            pid = int(data.get("pid", 0))

            return cls(
                index=idx,
                title=title,
                name=name,
                is_running=is_run,
                adb_port=port,
                pid=pid,
            )
        except (ValueError, TypeError) as err:
            logger.debug("Failed parsing MuMu instance dict %s: %s", data, err)
            return None

    @classmethod
    def from_csv_line(cls, line: str) -> Optional[MuMuInstanceInfo]:
        """Parse CSV line in format: index,name,is_running,port."""
        parts = [p.strip() for p in line.strip().split(",")]
        if len(parts) < 2:
            return None
        try:
            idx = int(parts[0])
            name = parts[1]
            is_run = bool(int(parts[2])) if len(parts) > 2 else False
            port = int(parts[3]) if len(parts) > 3 else cls.calculate_default_port(idx)
            return cls(index=idx, title=name, is_running=is_run, adb_port=port)
        except (ValueError, IndexError):
            return None

    @classmethod
    def parse_output(cls, output: str) -> list[MuMuInstanceInfo]:
        """Parse raw stdout from MuMuManager which may be JSON or text."""
        cleaned = output.strip()
        if not cleaned:
            return []

        # Try JSON first
        if cleaned.startswith("[") or cleaned.startswith("{"):
            try:
                parsed = json.loads(cleaned)
                if isinstance(parsed, list):
                    return [inst for item in parsed if (inst := cls.from_dict(item)) is not None]
                if isinstance(parsed, dict):
                    inst = cls.from_dict(parsed)
                    return [inst] if inst else []
            except json.JSONDecodeError:
                pass

        # Fallback to CSV / line-based parsing
        instances: list[MuMuInstanceInfo] = []
        for line in cleaned.splitlines():
            line = line.strip()
            if not line:
                continue
            inst = cls.from_csv_line(line)
            if inst:
                instances.append(inst)
        return instances
