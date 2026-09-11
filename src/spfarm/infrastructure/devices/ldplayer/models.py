"""Data models and output parsers for LDPlayer emulator instances."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LDInstanceInfo:
    """Descriptor for an LDPlayer emulator instance parsed from ldconsole list2."""

    index: int
    title: str
    top_hwnd: int
    bind_hwnd: int
    android_started: bool
    pid: int
    vbox_pid: int

    @property
    def adb_port(self) -> int:
        """Standard ADB local port for this LDPlayer instance index."""
        return 5555 + (self.index * 2)

    @property
    def adb_target(self) -> str:
        """ADB target connection address."""
        return f"127.0.0.1:{self.adb_port}"

    @classmethod
    def from_csv_line(cls, line: str) -> Optional[LDInstanceInfo]:
        """Parse a single line from 'ldconsole list2'.

        Format: index,title,top_hwnd,bind_hwnd,android_started,pid,vbox_pid
        Example: 0,LDPlayer,0,0,0,0,0
        Example: 1,LDPlayer-1,12345,12346,1,4567,4568
        """
        parts = [p.strip() for p in line.strip().split(",")]
        if len(parts) < 7:
            return None

        try:
            return cls(
                index=int(parts[0]),
                title=parts[1],
                top_hwnd=int(parts[2]),
                bind_hwnd=int(parts[3]),
                android_started=bool(int(parts[4])),
                pid=int(parts[5]),
                vbox_pid=int(parts[6]),
            )
        except (ValueError, IndexError) as err:
            logger.debug("Failed parsing ldconsole line '%s': %s", line, err)
            return None

    @classmethod
    def parse_list2_output(cls, output: str) -> list[LDInstanceInfo]:
        """Parse multi-line stdout from 'ldconsole list2'."""
        instances: list[LDInstanceInfo] = []
        for line in output.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            inst = cls.from_csv_line(line)
            if inst is not None:
                instances.append(inst)
        return instances
