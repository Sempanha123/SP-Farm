"""Subprocess runner for MuMu Player CLI (MuMuManager.exe / mumu.exe)."""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path
from typing import Callable, Optional

from spfarm.infrastructure.devices.mumu.models import MuMuInstanceInfo

logger = logging.getLogger(__name__)

CANDIDATE_PATHS = [
    Path(r"C:\Program Files\Netease\MuMuPlayer-12.0\shell"),
    Path(r"D:\Program Files\Netease\MuMuPlayer-12.0\shell"),
    Path(r"E:\Program Files\Netease\MuMuPlayer-12.0\shell"),
    Path(r"C:\MuMuPlayer-12.0\shell"),
    Path(r"D:\MuMuPlayer-12.0\shell"),
    Path(r"C:\Program Files (x86)\Netease\MuMuPlayer-12.0\shell"),
    Path(r"C:\Program Files\Netease\MuMuPlayer-12.0\nx_device\12.0\shell"),
]

ProcessExecutor = Callable[[list[str], Optional[Path], float], tuple[int, str, str]]


def default_process_executor(
    args: list[str],
    cwd: Optional[Path],
    timeout: float,
) -> tuple[int, str, str]:
    """Execute MuMu CLI commands via subprocess.run."""
    try:
        proc = subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        logger.warning("MuMu command timed out after %.1fs: %s", timeout, args)
        return -1, "", f"Command timed out after {timeout} seconds"
    except Exception as err:
        logger.error("Failed running MuMu command %s: %s", args, err)
        return -1, "", str(err)


class MuMuManagerRunner:
    """Discovers and executes commands against MuMuManager.exe."""

    def __init__(
        self,
        custom_install_dir: Optional[Path] = None,
        process_executor: Optional[ProcessExecutor] = None,
    ) -> None:
        self.process_executor = process_executor or default_process_executor
        self._install_dir: Optional[Path] = self._resolve_install_dir(custom_install_dir)
        self._executable_path: Optional[Path] = self._resolve_executable()

    @property
    def is_available(self) -> bool:
        """Check whether MuMuManager.exe exists and is executable."""
        return self._executable_path is not None and self._executable_path.exists()

    @property
    def install_dir(self) -> Optional[Path]:
        return self._install_dir

    @property
    def executable_path(self) -> Optional[Path]:
        return self._executable_path

    def _resolve_install_dir(self, custom_dir: Optional[Path]) -> Optional[Path]:
        if custom_dir is not None:
            return custom_dir if custom_dir.exists() else None

        for candidate in CANDIDATE_PATHS:
            if candidate.exists() and (
                (candidate / "MuMuManager.exe").exists()
                or (candidate / "mumu.exe").exists()
                or (candidate / "nemuconsole.exe").exists()
            ):
                return candidate

        return None

    def _resolve_executable(self) -> Optional[Path]:
        if not self._install_dir:
            return None

        for exe_name in ("MuMuManager.exe", "mumu.exe", "nemuconsole.exe"):
            candidate = self._install_dir / exe_name
            if candidate.exists():
                return candidate

        return None

    def set_install_dir(self, directory: Path) -> bool:
        """Manually configure MuMu installation directory."""
        self._install_dir = directory
        self._executable_path = self._resolve_executable()
        return self.is_available

    def run_raw(self, *args: str, timeout: float = 30.0) -> tuple[int, str, str]:
        """Execute MuMuManager with raw CLI arguments."""
        if not self.is_available or not self._executable_path:
            return -1, "", "MuMu executable (MuMuManager.exe) not found on system"

        cmd = [str(self._executable_path), *args]
        return self.process_executor(cmd, self._install_dir, timeout)

    # -------------------------------------------------------------------------
    # High-level MuMu Commands
    # -------------------------------------------------------------------------
    def list_instances(self, timeout: float = 10.0) -> list[MuMuInstanceInfo]:
        """Enumerate emulator instances via 'MuMuManager.exe api -v all player_state'."""
        code, out, _ = self.run_raw("api", "-v", "all", "player_state", timeout=timeout)
        if code != 0 or not out:
            # Fallback format: api -v all info
            code, out, _ = self.run_raw("api", "-v", "all", "info", timeout=timeout)
            if code != 0 or not out:
                return []
        return MuMuInstanceInfo.parse_output(out)

    def is_running(self, index: int, timeout: float = 5.0) -> bool:
        """Check if an instance is running via player_state."""
        code, out, _ = self.run_raw("api", "-v", str(index), "player_state", timeout=timeout)
        if code == 0 and ("running" in out.lower() or "started" in out.lower() or "1" in out.strip()):
            return True
        # Check instance list
        instances = self.list_instances(timeout=timeout)
        for inst in instances:
            if inst.index == index:
                return inst.is_running
        return False

    def launch(self, index: int, timeout: float = 30.0) -> tuple[int, str, str]:
        """Launch the emulator instance at index."""
        return self.run_raw("api", "-v", str(index), "launch_player", timeout=timeout)

    def close(self, index: int, timeout: float = 20.0) -> tuple[int, str, str]:
        """Close / power off the emulator instance at index."""
        return self.run_raw("api", "-v", str(index), "close_player", timeout=timeout)

    def restart(self, index: int, timeout: float = 30.0) -> tuple[int, str, str]:
        """Restart the emulator instance at index."""
        return self.run_raw("api", "-v", str(index), "restart_player", timeout=timeout)

    def install_app(self, index: int, apk_path: Path, timeout: float = 60.0) -> tuple[int, str, str]:
        """Install an APK onto the emulator instance."""
        return self.run_raw("api", "-v", str(index), "app", "-i", str(apk_path), timeout=timeout)

    def uninstall_app(self, index: int, package_name: str, timeout: float = 20.0) -> tuple[int, str, str]:
        """Uninstall an app package from the emulator instance."""
        return self.run_raw("api", "-v", str(index), "app", "-u", package_name, timeout=timeout)

    def run_app(self, index: int, package_name: str, timeout: float = 15.0) -> tuple[int, str, str]:
        """Launch an app package on the emulator instance."""
        return self.run_raw("api", "-v", str(index), "app", "-l", package_name, timeout=timeout)

    def stop_app(self, index: int, package_name: str, timeout: float = 15.0) -> tuple[int, str, str]:
        """Stop a running app package on the emulator instance."""
        return self.run_raw("api", "-v", str(index), "app", "-k", package_name, timeout=timeout)
