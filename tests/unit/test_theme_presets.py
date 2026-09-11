"""Unit tests for theme tokens, presets, and dynamic stylesheet generation."""

import re
from pathlib import Path

from spfarm.shared.settings import SettingsManager
from spfarm.shared.theme import (
    THEME_DARK_BLUE,
    THEME_LIGHT_BLUE,
    THEME_LIGHT_LAVENDER,
    THEME_LIGHT_PINK,
    THEME_PRESETS,
    build_app_stylesheet,
    get_theme_palette,
)

HEX_COLOR_REGEX = re.compile(r"^#[0-9a-fA-F]{6}$")


def test_theme_presets_tokens_are_valid_hex() -> None:
    for theme_name, palette in THEME_PRESETS.items():
        assert palette.name != ""
        assert HEX_COLOR_REGEX.match(palette.background), f"{theme_name} background invalid"
        assert HEX_COLOR_REGEX.match(palette.surface), f"{theme_name} surface invalid"
        assert HEX_COLOR_REGEX.match(palette.primary), f"{theme_name} primary invalid"
        assert HEX_COLOR_REGEX.match(palette.cute_pink), f"{theme_name} cute_pink invalid"
        assert HEX_COLOR_REGEX.match(palette.text), f"{theme_name} text invalid"


def test_theme_presets_dark_mode_flag() -> None:
    assert THEME_LIGHT_BLUE.is_dark is False
    assert THEME_LIGHT_PINK.is_dark is False
    assert THEME_LIGHT_LAVENDER.is_dark is False
    assert THEME_DARK_BLUE.is_dark is True


def test_get_theme_palette_lookup_and_fallback() -> None:
    assert get_theme_palette("light_blue") == THEME_LIGHT_BLUE
    assert get_theme_palette("pink") == THEME_LIGHT_PINK
    assert get_theme_palette("lavender") == THEME_LIGHT_LAVENDER
    assert get_theme_palette("dark_blue") == THEME_DARK_BLUE
    # Fallback to default
    assert get_theme_palette("unknown_palette") == THEME_LIGHT_BLUE


def test_stylesheet_generation_contains_theme_colors() -> None:
    for _, palette in THEME_PRESETS.items():
        qss = build_app_stylesheet(palette)
        assert palette.primary in qss
        assert palette.background in qss
        assert palette.cute_pink in qss
        assert 'role="cute"' in qss
        assert 'role="surface"' in qss


def test_theme_persists_in_settings(tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.json"
    mgr = SettingsManager(settings_file=settings_file)
    assert mgr.get().appearance.theme == "light_blue"

    # Switch theme to pink
    mgr.update(lambda s: setattr(s.appearance, "theme", "pink"))

    # Reload from disk (simulating restart)
    restart_mgr = SettingsManager(settings_file=settings_file)
    assert restart_mgr.get().appearance.theme == "pink"
