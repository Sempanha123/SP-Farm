"""CuteCard container component adhering to Cute Light surface tokens."""

from __future__ import annotations

from typing import Optional

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from spfarm.shared.theme import PALETTE


class CuteCard(QFrame):
    """Rounded container card with header, badge slot, and content area."""

    def __init__(
        self,
        title: str = "",
        badge: Optional[QWidget] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setProperty("role", "surface")
        self.setStyleSheet(f"""
            CuteCard {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border};
                border-radius: 12px;
            }}
        """)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(14, 14, 14, 14)
        self.main_layout.setSpacing(10)

        # Header bar (optional)
        if title or badge:
            header_layout = QHBoxLayout()
            header_layout.setContentsMargins(0, 0, 0, 4)

            if title:
                self.title_label = QLabel(title)
                self.title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
                self.title_label.setStyleSheet(f"color: {PALETTE.primary};")
                header_layout.addWidget(self.title_label)

            header_layout.addStretch()

            if badge:
                header_layout.addWidget(badge)

            self.main_layout.addLayout(header_layout)

        # Body container
        self.body_widget = QWidget()
        self.body_layout = QVBoxLayout(self.body_widget)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.body_widget)

    def add_widget(self, widget: QWidget) -> None:
        """Add a child widget to the card body."""
        self.body_layout.addWidget(widget)
