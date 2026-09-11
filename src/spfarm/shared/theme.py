"""Cute Light Design System tokens, presets, and dynamic stylesheet generator."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    """Cute Light Design System Palette tokens."""

    name: str = "light_blue"
    is_dark: bool = False

    # Backgrounds & Surfaces
    background: str = "#F7F9FE"
    surface: str = "#FFFFFF"
    surface_alt: str = "#F2F6FD"
    soft_primary: str = "#EDF5FF"
    soft_pink: str = "#FFF1F7"
    soft_blue: str = "#EDF5FF"

    # Primary Accents
    primary: str = "#5B8DEF"
    primary_hover: str = "#79A5F5"
    primary_pressed: str = "#4676D7"

    # Secondary Cute Accents
    cute_pink: str = "#F38BB7"
    pink_hover: str = "#F6A4C6"
    pink_pressed: str = "#E0699A"
    lavender: str = "#A894F6"
    sky: str = "#78C7F7"

    # Semantic Status
    success: str = "#55BFA3"
    warning: str = "#F2B65E"
    danger: str = "#E96F7F"
    info: str = "#5B8DEF"

    # Typography
    text: str = "#293247"
    text_secondary: str = "#657089"
    text_muted: str = "#98A2B8"

    # Borders, Focus & Selection
    border: str = "#E3E9F3"
    border_strong: str = "#D3DCEC"
    selection: str = "#EEF5FF"
    focus_ring: str = "#5B8DEF"

    # Backward compatibility aliases
    @property
    def primary_blue(self) -> str:
        return self.primary

    @property
    def blue_hover(self) -> str:
        return self.primary_hover

    @property
    def blue_pressed(self) -> str:
        return self.primary_pressed


# 1. Light + Sky Blue (Default)
THEME_LIGHT_BLUE = Palette(
    name="light_blue",
    is_dark=False,
    primary="#5B8DEF",
    primary_hover="#79A5F5",
    primary_pressed="#4676D7",
    soft_primary="#EDF5FF",
    focus_ring="#5B8DEF",
)

# 2. Light + Pink
THEME_LIGHT_PINK = Palette(
    name="pink",
    is_dark=False,
    primary="#F38BB7",
    primary_hover="#F6A4C6",
    primary_pressed="#E0699A",
    soft_primary="#FFF1F7",
    focus_ring="#F38BB7",
)

# 3. Light + Lavender
THEME_LIGHT_LAVENDER = Palette(
    name="lavender",
    is_dark=False,
    primary="#A894F6",
    primary_hover="#BEAFF8",
    primary_pressed="#8E75F4",
    soft_primary="#F3F0FF",
    focus_ring="#A894F6",
)

# 4. Dark + Blue
THEME_DARK_BLUE = Palette(
    name="dark_blue",
    is_dark=True,
    background="#0B1120",
    surface="#1E293B",
    surface_alt="#161F30",
    soft_primary="#1E3A8A",
    soft_pink="#3B1D2D",
    soft_blue="#1E293B",
    primary="#38BDF8",
    primary_hover="#60A5FA",
    primary_pressed="#2563EB",
    cute_pink="#F472B6",
    pink_hover="#FB7185",
    pink_pressed="#E11D48",
    lavender="#C084FC",
    sky="#38BDF8",
    success="#34D399",
    warning="#FBBF24",
    danger="#F87171",
    info="#38BDF8",
    text="#F8FAFC",
    text_secondary="#94A3B8",
    text_muted="#64748B",
    border="#334155",
    border_strong="#475569",
    selection="#1E293B",
    focus_ring="#38BDF8",
)

THEME_PRESETS: dict[str, Palette] = {
    "light_blue": THEME_LIGHT_BLUE,
    "pink": THEME_LIGHT_PINK,
    "lavender": THEME_LIGHT_LAVENDER,
    "dark_blue": THEME_DARK_BLUE,
    "system": THEME_LIGHT_BLUE,
}

PALETTE = THEME_LIGHT_BLUE


def get_theme_palette(theme_name: str) -> Palette:
    """Retrieve the palette tokens for a given theme name."""
    return THEME_PRESETS.get(theme_name.lower(), THEME_LIGHT_BLUE)


def build_app_stylesheet(p: Palette = PALETTE) -> str:
    """Build root QSS stylesheet adhering to the Cute Light Design System."""
    return f"""
    QWidget {{
        background-color: {p.background};
        color: {p.text};
        font-family: 'Segoe UI', 'SF Pro Text', system-ui, sans-serif;
        font-size: 13px;
    }}

    /* Global Focus Outline */
    QWidget:focus {{
        outline: none;
    }}

    /* Standard Primary Button */
    QPushButton {{
        background-color: {p.primary};
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 7px 16px;
        font-weight: 600;
    }}
    QPushButton:hover {{
        background-color: {p.primary_hover};
    }}
    QPushButton:pressed {{
        background-color: {p.primary_pressed};
    }}
    QPushButton:focus {{
        border: 2px solid {p.focus_ring};
    }}
    QPushButton:disabled {{
        background-color: {p.border};
        color: {p.text_muted};
    }}

    /* Cute Accent Button */
    QPushButton[role="cute"] {{
        background-color: {p.cute_pink};
        color: #FFFFFF;
    }}
    QPushButton[role="cute"]:hover {{
        background-color: {p.pink_hover};
    }}
    QPushButton[role="cute"]:pressed {{
        background-color: {p.pink_pressed};
    }}

    /* Secondary / Outline Button */
    QPushButton[role="secondary"] {{
        background-color: {p.surface};
        color: {p.text};
        border: 1px solid {p.border};
    }}
    QPushButton[role="secondary"]:hover {{
        background-color: {p.surface_alt};
        border-color: {p.border_strong};
    }}

    /* Ghost Button */
    QPushButton[role="ghost"] {{
        background-color: transparent;
        color: {p.text_secondary};
    }}
    QPushButton[role="ghost"]:hover {{
        background-color: {p.soft_primary};
        color: {p.primary};
    }}

    /* Danger Button */
    QPushButton[role="danger"] {{
        background-color: {p.danger};
        color: #FFFFFF;
    }}
    QPushButton[role="danger"]:hover {{
        background-color: #D9534F;
    }}

    /* Cards & Panels */
    QFrame[role="surface"] {{
        background-color: {p.surface};
        border: 1px solid {p.border};
        border-radius: 12px;
    }}

    /* Inputs */
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
        background-color: {p.surface};
        border: 1px solid {p.border};
        border-radius: 8px;
        padding: 6px 12px;
        color: {p.text};
    }}
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
        border: 1.5px solid {p.focus_ring};
    }}

    /* Tables */
    QTableWidget {{
        background-color: {p.surface};
        border: 1px solid {p.border};
        border-radius: 8px;
        gridline-color: {p.border};
        selection-background-color: {p.soft_primary};
        selection-color: {p.primary};
    }}
    QHeaderView::section {{
        background-color: {p.surface_alt};
        color: {p.text_secondary};
        font-weight: 600;
        padding: 8px;
        border: none;
        border-bottom: 1px solid {p.border};
    }}

    /* Scrollbars */
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0px;
    }}
    QScrollBar::handle:vertical {{
        background: {p.border_strong};
        min-height: 24px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {p.primary};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
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
