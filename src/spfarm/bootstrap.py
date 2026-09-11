"""Application bootstrap and initialization entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from spfarm import __version__
from spfarm.presentation.shell.splash import SplashWindow
from spfarm.shared.paths import paths
from spfarm.shared.theme import build_app_stylesheet


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="spfarm",
        description="SP-Farm V2 — Modern Desktop Operations Platform",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"SP-Farm V2 {__version__}",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run startup initialization without displaying GUI window",
    )
    parser.add_argument(
        "--arch-status",
        action="store_true",
        help="Display developer architecture status screen",
    )
    return parser.parse_args(argv)


def bootstrap_environment() -> None:
    """Prepare filesystem paths and environment variables."""
    # Load .env file if it exists
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

    # Ensure required runtime directories exist
    paths.ensure_directories()


def main(argv: list[str] | None = None) -> int:
    """Main application entry point."""
    args = parse_args(argv)

    # 1. Initialize environment & paths
    bootstrap_environment()

    # 2. If headless, initialize and exit cleanly
    if args.headless:
        print(f"SP-Farm V2 (v{__version__}) initialized in headless mode.")
        return 0

    # 3. Create Qt Application
    app = QApplication.instance()
    if app is None:
        app = QApplication(argv or sys.argv)

    app.setApplicationName("SP-Farm")
    app.setApplicationVersion(__version__)
    app.setStyleSheet(build_app_stylesheet())

    # 4. If developer architecture status requested, open architecture dialog
    if args.arch_status:
        from spfarm.presentation.shell.architecture_view import ArchitectureStatusDialog

        dlg = ArchitectureStatusDialog()
        dlg.show()
        return app.exec()

    # 5. Display Splash / Boot Window
    splash = SplashWindow()
    splash.center_on_screen()
    splash.show()

    # 5. Boot sequence steps
    steps = [
        (25, "Ensuring runtime directories..."),
        (50, "Checking secure storage..."),
        (75, "Loading configuration..."),
        (100, "Ready! Starting SP-Farm V2..."),
    ]

    current_step = 0

    def step_forward() -> None:
        nonlocal current_step
        if current_step < len(steps):
            pct, msg = steps[current_step]
            splash.set_status(msg, pct)
            current_step += 1
        else:
            timer.stop()

    timer = QTimer()
    timer.timeout.connect(step_forward)
    timer.start(400)

    # For Phase 01 (splash boot screen verification):
    # Window stays open for user to view or until closed.
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
