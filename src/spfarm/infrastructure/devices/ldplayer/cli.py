"""Subprocess runner for LDPlayer CLI (ldconsole.exe / dnconsole.exe)."""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path
from typing import Callable, Optional

from spfarm.infrastructure.devices.ldplayer.models import LDInstanceInfo

logger = logging.getLogger(__name__)

# Standard candidate directories where LDPlayer 9 / 4 is installed on Windows
CANDIDATE_PATHS = [
    Path(r"C:\LDPlayer\LDPlayer9"),
    Path(r"D:\LDPlayer\LDPlayer9"),
    Path(r"E:\LDPlayer\LDPlayer9"),
    Path(r"C:\leidian\LDPlayer9"),
    Path(r"D:\leidian\LDPlayer9"),
    Path(r"C:\LDPlayer\LDPlayer4"),
    Path(r"C:\Program Files\LDPlayer\LDPlayer9"),
]

# Type signature for low-level process executor: (args, cwd, timeout) -> (returncode, stdout, stderr)
ProcessExecutor = Callable[[list[str], Optional[Path], float], tuple[int, str, str]]


def default_process_executor(
    args: list[str],
    cwd: Optional[Path],
    timeout: float,
) -> tuple[int, str, str]:
    """Default Windows subprocess execution using subprocess.run."""
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
        logger.warning("LDPlayer command timed out after %.1fs: %s", timeout, args)
        return -1, "", f"Command timed out after {timeout} seconds"
    except Exception as err:
        logger.error("Failed running LDPlayer command %s: %s", args, err)
        return -1, "", str(err)


class LDConsoleRunner:
    """Discovers and executes commands against the LDPlayer command line utility."""

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
        """Check whether ldconsole.exe exists and is executable."""
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
                (candidate / "ldconsole.exe").exists() or (candidate / "dnconsole.exe").exists()
            ):
                return candidate

        return None

    def _resolve_executable(self) -> Optional[Path]:
        if not self._install_dir:
            return None

        ldconsole = self._install_dir / "ldconsole.exe"
        if ldconsole.exists():
            return ldconsole

        dnconsole = self._install_dir / "dnconsole.exe"
        if dnconsole.exists():
            return dnconsole

        return None

    def set_install_dir(self, directory: Path) -> bool:
        """Manually point to an installation directory."""
        self._install_dir = directory
        self._executable_path = self._resolve_executable()
        return self.is_available

    def run_raw(self, *args: str, timeout: float = 30.0) -> tuple[int, str, str]:
        """Execute ldconsole with the specified arguments."""
        if not self.is_available or not self._executable_path:
            return -1, "", "LDPlayer executable (ldconsole.exe) not found on system"

        cmd = [str(self._executable_path), *args]
        return self.process_executor(cmd, self._install_dir, timeout)

    # -------------------------------------------------------------------------
    # High-level LDConsole Commands
    # -------------------------------------------------------------------------
    def list2(self, timeout: float = 10.0) -> list[LDInstanceInfo]:
        """Query all instances via 'ldconsole list2'."""
        code, out, _ = self.run_raw("list2", timeout=timeout)
        if code != 0 or not out:
            return []
        return LDInstanceInfo.parse_list2_output(out)

    def is_running(self, index: int, timeout: float = 5.0) -> bool:
        """Check if an instance is running via 'ldconsole isrunning --index <index>'."""
        code, out, _ = self.run_raw("isrunning", "--index", str(index), timeout=timeout)
        if code == 0 and "running" in out.lower():
            return True
        # Fallback to list2 check
        instances = self.list2(timeout=timeout)
        for inst in instances:
            if inst.index == index:
                return inst.android_started
        return False

    def launch(self, index: int, timeout: float = 30.0) -> tuple[int, str, str]:
        """Start the emulator instance at index."""
        return self.run_raw("launch", "--index", str(index), timeout=timeout)

    def quit(self, index: int, timeout: float = 20.0) -> tuple[int, str, str]:
        """Gracefully stop the emulator instance at index."""
        return self.run_raw("quit", "--index", str(index), timeout=timeout)

    def quit_all(self, timeout: float = 30.0) -> tuple[int, str, str]:
        """Stop all running emulator instances."""
        return self.run_raw("quitall", timeout=timeout)

    def reboot(self, index: int, timeout: float = 30.0) -> tuple[int, str, str]:
        """Reboot the emulator instance at index."""
        return self.run_raw("reboot", "--index", str(index), timeout=timeout)

    def install_app(
        self, index: int, apk_path: Path, timeout: float = 60.0
    ) -> tuple[int, str, str]:
        """Install an APK file onto the emulator instance."""
        return self.run_raw(
            "installapp", "--index", str(index), "--filename", str(apk_path), timeout=timeout
        )

    def uninstall_app(
        self, index: int, package_name: str, timeout: float = 20.0
    ) -> tuple[int, str, str]:
        """Uninstall an app package from the emulator instance."""
        return self.run_raw(
            "uninstallapp", "--index", str(index), "--packagename", package_name, timeout=timeout
        )

    def run_app(self, index: int, package_name: str, timeout: float = 15.0) -> tuple[int, str, str]:
        """Launch an app package on the emulator instance."""
        return self.run_raw(
            "runapp", "--index", str(index), "--packagename", package_name, timeout=timeout
        )

    def kill_app(
        self, index: int, package_name: str, timeout: float = 15.0
    ) -> tuple[int, str, str]:
        """Kill a running app package on the emulator instance."""
        return self.run_raw(
            "killapp", "--index", str(index), "--packagename", package_name, timeout=timeout
        )

    def sort_windows(self, timeout: float = 10.0) -> tuple[int, str, str]:
        """Arrange all running LDPlayer windows in a grid across monitors."""
        return self.run_raw("sortWnd", timeout=timeout)
