"""Tests for Cute Light theme palette and stylesheet."""

import re

from spfarm.shared.theme import PALETTE, build_app_stylesheet

HEX_COLOR_REGEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def test_palette_hex_values() -> None:
    """Verify all palette colors are valid 6-character hex codes."""
    colors = [
        PALETTE.background,
        PALETTE.surface,
        PALETTE.surface_alt,
        PALETTE.soft_blue,
        PALETTE.soft_pink,
        PALETTE.primary_blue,
        PALETTE.blue_hover,
        PALETTE.blue_pressed,
        PALETTE.cute_pink,
        PALETTE.pink_hover,
        PALETTE.lavender,
        PALETTE.sky,
        PALETTE.success,
        PALETTE.warning,
        PALETTE.danger,
        PALETTE.text,
        PALETTE.text_secondary,
        PALETTE.text_muted,
        PALETTE.border,
        PALETTE.border_strong,
        PALETTE.selection,
    ]
    for color in colors:
        assert HEX_COLOR_REGEX.match(color) is not None, f"Invalid hex color: {color}"


def test_theme_constants() -> None:
    """Verify cute theme signature colors."""
    assert PALETTE.background.upper() == "#F7F9FE"
    assert PALETTE.primary_blue.upper() == "#5B8DEF"
    assert PALETTE.cute_pink.upper() == "#F38BB7"
    assert PALETTE.lavender.upper() == "#A894F6"


def test_app_stylesheet_generation() -> None:
    """Verify that generated QSS contains palette styling."""
    qss = build_app_stylesheet(PALETTE)
    assert PALETTE.background in qss
    assert PALETTE.primary_blue in qss
    assert PALETTE.cute_pink in qss
