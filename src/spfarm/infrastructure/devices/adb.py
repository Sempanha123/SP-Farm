"""Minimal ADB command runner shared by runtime device providers."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Callable, Optional

AdbExecutor = Callable[[list[str], float], tuple[int, bytes, bytes]]


def default_adb_executor(args: list[str], timeout: float) -> tuple[int, bytes, bytes]:
    try:
        process = subprocess.run(
            args,
            capture_output=True,
            timeout=timeout,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        return process.returncode, process.stdout, process.stderr
    except subprocess.TimeoutExpired:
        return -1, b"", f"ADB command timed out after {timeout} seconds".encode()
    except Exception as error:
        return -1, b"", str(error).encode()


class AdbRunner:
    def __init__(
        self,
        executable_path: Optional[Path] = None,
        executor: Optional[AdbExecutor] = None,
    ) -> None:
        configured = str(executable_path) if executable_path else shutil.which("adb")
        self.executable_path = Path(configured) if configured else None
        self.executor = executor or default_adb_executor

    @property
    def is_available(self) -> bool:
        return self.executable_path is not None and self.executable_path.exists()

    def run(self, args: list[str], timeout: float = 30.0) -> tuple[int, bytes, bytes]:
        if not self.is_available or not self.executable_path:
            return -1, b"", b"ADB executable not found"
        return self.executor([str(self.executable_path), *args], timeout)

    def run_text(self, args: list[str], timeout: float = 30.0) -> tuple[int, str, str]:
        code, stdout, stderr = self.run(args, timeout)
        return code, stdout.decode(errors="replace"), stderr.decode(errors="replace")

    def screenshot(
        self, target: str, output_path: Path, timeout: float = 30.0
    ) -> tuple[int, str]:
        code, stdout, stderr = self.run(
            ["-s", target, "exec-out", "screencap", "-p"], timeout
        )
        if code != 0:
            return code, stderr.decode(errors="replace") or stdout.decode(errors="replace")
        if not stdout.startswith(b"\x89PNG\r\n\x1a\n"):
            return -1, "ADB screenshot returned invalid PNG data"

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(stdout)
        except OSError as error:
            return -1, str(error)
        return 0, ""
