"""CuteMetricCard component with soft pastel icon badge and clean white surface."""

from __future__ import annotations

from typing import Any, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from spfarm.shared.theme import PALETTE


class CuteMetricCard(QFrame):
    """Metric KPI card adhering to 01_UX_UI_SOURCE_OF_TRUTH.txt.

    Features a pure white surface, soft subtle border, and a gentle pastel icon badge.
    """

    def __init__(
        self,
        title: str,
        value: str = "0",
        icon: str = "📊",
        pastel_bg: str = "#EDF5FF",
        icon_fg: str = "#5B8DEF",
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(f"""
            CuteMetricCard {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border};
                border-radius: 12px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(12)

        # Pastel Icon Badge
        self.badge_frame = QFrame()
        self.badge_frame.setFixedSize(44, 44)
        self.badge_frame.setStyleSheet(f"""
            background-color: {pastel_bg};
            border-radius: 10px;
        """)
        badge_layout = QVBoxLayout(self.badge_frame)
        badge_layout.setContentsMargins(0, 0, 0, 0)
        badge_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.icon_lbl = QLabel(icon)
        self.icon_lbl.setFont(QFont("Segoe UI Emoji", 18))
        self.icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_lbl.setStyleSheet(f"color: {icon_fg};")
        badge_layout.addWidget(self.icon_lbl)
        layout.addWidget(self.badge_frame)

        # Content: Title + Big Value
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(2)

        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 11px; font-weight: 600;")
        content_layout.addWidget(self.lbl_title)

        self.lbl_value = QLabel(str(value))
        val_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        self.lbl_value.setFont(val_font)
        self.lbl_value.setStyleSheet(f"color: {PALETTE.text};")
        content_layout.addWidget(self.lbl_value)

        self.lbl_extra = QLabel("")
        self.lbl_extra.setStyleSheet(f"color: {PALETTE.text_muted}; font-size: 10px;")
        self.lbl_extra.hide()
        content_layout.addWidget(self.lbl_extra)

        layout.addLayout(content_layout)
        layout.addStretch()

    def set_value(self, value: Any, extra_text: str = "") -> None:
        """Update counter and optional extra text."""
        self.lbl_value.setText(str(value))
        if extra_text:
            self.lbl_extra.setText(extra_text)
            self.lbl_extra.show()
        else:
            self.lbl_extra.hide()
