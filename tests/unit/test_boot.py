"""Tests for application boot, versioning, and splash window."""

from PySide6.QtWidgets import QApplication

from spfarm import __version__
from spfarm.bootstrap import parse_args
from spfarm.presentation.shell.splash import SplashWindow


def test_version_format() -> None:
    assert __version__.startswith("2.")


def test_parse_args_headless() -> None:
    args = parse_args(["--headless"])
    assert args.headless is True


def test_parse_args_default() -> None:
    args = parse_args([])
    assert args.headless is False


def test_splash_window_init(qapp: QApplication) -> None:
    splash = SplashWindow()
    assert splash.windowTitle() == "SP-Farm V2"
    assert splash.width() == 480
    assert splash.height() == 280

    # Test status updating
    splash.set_status("Loading modules...", 45)
    assert splash.status_label.text() == "Loading modules..."
    assert splash.progress_bar.value() == 45
    splash.close()
