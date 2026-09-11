"""Cute Light Design System tokens and stylesheet helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    """Cute Light Design System Palette."""

    # Backgrounds & Surfaces
    background: str = "#F7F9FE"
    surface: str = "#FFFFFF"
    surface_alt: str = "#F2F6FD"
    soft_blue: str = "#EDF5FF"
    soft_pink: str = "#FFF1F7"

    # Primary Accents (Blue)
    primary_blue: str = "#5B8DEF"
    blue_hover: str = "#79A5F5"
    blue_pressed: str = "#4676D7"

    # Cute Accents (Pink & Lavender)
    cute_pink: str = "#F38BB7"
    pink_hover: str = "#F6A4C6"
    lavender: str = "#A894F6"
    sky: str = "#78C7F7"

    # Semantic Status
    success: str = "#55BFA3"
    warning: str = "#F2B65E"
    danger: str = "#E96F7F"

    # Typography
    text: str = "#293247"
    text_secondary: str = "#657089"
    text_muted: str = "#98A2B8"

    # Borders & Selection
    border: str = "#E3E9F3"
    border_strong: str = "#D3DCEC"
    selection: str = "#EEF5FF"


PALETTE = Palette()


def build_app_stylesheet(p: Palette = PALETTE) -> str:
    """Build root QSS stylesheet adhering to the Cute Light Design System."""
    return f"""
    QWidget {{
        background-color: {p.background};
        color: {p.text};
        font-family: 'Segoe UI', 'SF Pro Text', system-ui, sans-serif;
        font-size: 13px;
    }}

    /* Buttons */
    QPushButton {{
        background-color: {p.primary_blue};
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
    }}
    QPushButton:hover {{
        background-color: {p.blue_hover};
    }}
    QPushButton:pressed {{
        background-color: {p.blue_pressed};
    }}
    QPushButton:disabled {{
        background-color: {p.border};
        color: {p.text_muted};
    }}

    /* Secondary Cute Button */
    QPushButton[role="cute"] {{
        background-color: {p.cute_pink};
        color: #FFFFFF;
    }}
    QPushButton[role="cute"]:hover {{
        background-color: {p.pink_hover};
    }}

    /* Cards & Panels */
    QFrame[role="surface"] {{
        background-color: {p.surface};
        border: 1px solid {p.border};
        border-radius: 12px;
    }}

    /* Progress Bar */
    QProgressBar {{
        background-color: {p.surface_alt};
        border: 1px solid {p.border};
        border-radius: 6px;
        text-align: center;
        height: 10px;
        color: {p.text_secondary};
    }}
    QProgressBar::chunk {{
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {p.sky}, stop:1 {p.cute_pink});
        border-radius: 5px;
    }}
    """
