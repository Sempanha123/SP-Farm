"""CuteStatusPill component for table rows, cards, and header summaries."""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from spfarm.shared.theme import PALETTE


class CuteStatusPill(QFrame):
    """Rounded status pill badge with semantic color coding."""

    STATUS_STYLES = {
        "ready": {"bg": "#E8F8F2", "fg": "#27AE60", "dot": "●"},
        "running": {"bg": "#EDF5FF", "fg": "#2F80ED", "dot": "●"},
        "error": {"bg": "#FEECEE", "fg": "#EB5757", "dot": "●"},
        "warning": {"bg": "#FEF7E6", "fg": "#F2994A", "dot": "●"},
        "offline": {"bg": "#F2F4F7", "fg": "#828282", "dot": "○"},
        "cooldown": {"bg": "#F4EFFE", "fg": "#9B51E0", "dot": "◌"},
        "active": {"bg": "#E8F8F2", "fg": "#27AE60", "dot": "●"},
    }

    def __init__(
        self,
        text: str = "Ready",
        status_type: str = "ready",
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.status_type = status_type.lower()
        self.text_label = QLabel(text)

        self._setup_ui(text)

    def _setup_ui(self, text: str) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 2, 8, 2)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        style = self.STATUS_STYLES.get(self.status_type, self.STATUS_STYLES["ready"])

        self.dot_label = QLabel(style["dot"])
        self.dot_label.setStyleSheet(f"color: {style['fg']}; font-size: 9px;")
        layout.addWidget(self.dot_label)

        self.text_label.setText(text)
        self.text_label.setStyleSheet(f"color: {style['fg']}; font-weight: 600; font-size: 11px;")
        layout.addWidget(self.text_label)

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {style["bg"]};
                border-radius: 10px;
                border: 1px solid {PALETTE.border};
            }}
        """)

    def set_status(self, text: str, status_type: str) -> None:
        """Update the status label and color styling."""
        self.status_type = status_type.lower()
        style = self.STATUS_STYLES.get(self.status_type, self.STATUS_STYLES["ready"])
        self.dot_label.setText(style["dot"])
        self.dot_label.setStyleSheet(f"color: {style['fg']}; font-size: 9px;")
        self.text_label.setText(text)
        self.text_label.setStyleSheet(f"color: {style['fg']}; font-weight: 600; font-size: 11px;")
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {style["bg"]};
                border-radius: 10px;
                border: 1px solid {PALETTE.border};
            }}
        """)
