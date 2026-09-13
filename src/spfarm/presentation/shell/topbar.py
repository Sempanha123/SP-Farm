"""Cute AppTopbar with title, global search trigger, system pills, theme and language switches."""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from spfarm.presentation.components.status_pill import CuteStatusPill
from spfarm.shared.theme import PALETTE


class AppTopbar(QFrame):
    """Top bar component adhering to 01_UX_UI_SOURCE_OF_TRUTH.txt."""

    theme_changed = Signal(str)
    language_changed = Signal(str)
    command_palette_requested = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(56)
        self.setStyleSheet(f"""
            AppTopbar {{
                background-color: {PALETTE.surface};
                border-bottom: 1px solid {PALETTE.border};
            }}
            QPushButton#cmd_btn {{
                background-color: {PALETTE.surface_alt};
                color: {PALETTE.text_secondary};
                border: 1px solid {PALETTE.border};
                border-radius: 8px;
                padding: 6px 14px;
                text-align: left;
            }}
            QPushButton#cmd_btn:hover {{
                border-color: {PALETTE.primary};
                color: {PALETTE.primary};
            }}
            QComboBox {{
                background-color: {PALETTE.surface_alt};
                border: 1px solid {PALETTE.border};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 12px;
            }}
        """)

        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(12)

        # Page Title
        self.lbl_title = QLabel("Dashboard")
        self.lbl_title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.lbl_title.setStyleSheet(f"color: {PALETTE.primary};")
        layout.addWidget(self.lbl_title)

        layout.addSpacing(16)

        # Global Search / Command Palette trigger button (Ctrl+K)
        self.btn_search = QPushButton("🔍 Search or press Ctrl+K...")
        self.btn_search.setObjectName("cmd_btn")
        self.btn_search.setFixedWidth(260)
        self.btn_search.clicked.connect(self.command_palette_requested.emit)
        layout.addWidget(self.btn_search)

        layout.addStretch()

        # Operational status pills
        self.pill_jobs = CuteStatusPill("0 Jobs Running", status_type="ready")
        self.pill_devices = CuteStatusPill("Devices Ready", status_type="ready")
        layout.addWidget(self.pill_jobs)
        layout.addWidget(self.pill_devices)

        layout.addSpacing(8)

        # Theme switcher
        self.cmb_theme = QComboBox()
        self.cmb_theme.addItem("🎨 Light Blue", "light_blue")
        self.cmb_theme.addItem("🌸 Cute Pink", "pink")
        self.cmb_theme.addItem("💜 Lavender", "lavender")
        self.cmb_theme.addItem("🌙 Dark Blue", "dark_blue")
        self.cmb_theme.currentIndexChanged.connect(self._on_theme_changed)
        layout.addWidget(self.cmb_theme)

        # Language switcher
        self.cmb_lang = QComboBox()
        self.cmb_lang.addItem("🇬🇧 EN", "en")
        self.cmb_lang.addItem("🇰🇭 KM", "km")
        self.cmb_lang.currentIndexChanged.connect(self._on_lang_changed)
        layout.addWidget(self.cmb_lang)

    def set_title(self, title: str) -> None:
        """Update topbar title."""
        self.lbl_title.setText(title)

    def set_job_count(self, count: int) -> None:
        """Update running jobs indicator."""
        if count > 0:
            self.pill_jobs.set_status(f"{count} Running", "running")
        else:
            self.pill_jobs.set_status("Idle", "ready")

    def _on_theme_changed(self, index: int) -> None:
        theme_id = self.cmb_theme.itemData(index)
        if theme_id:
            self.theme_changed.emit(theme_id)

    def _on_lang_changed(self, index: int) -> None:
        lang_code = self.cmb_lang.itemData(index)
        if lang_code:
            self.language_changed.emit(lang_code)
