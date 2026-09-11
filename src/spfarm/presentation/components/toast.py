"""CuteToast floating feedback notification component."""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from spfarm.shared.theme import PALETTE


class CuteToast(QFrame):
    """Floating non-blocking toast notification with auto-dismiss."""

    TOAST_THEMES = {
        "success": {"bg": "#E8F8F2", "fg": "#27AE60", "icon": "✅"},
        "info": {"bg": "#EDF5FF", "fg": "#2F80ED", "icon": "ℹ️"},
        "warning": {"bg": "#FEF7E6", "fg": "#F2994A", "icon": "⚠️"},
        "danger": {"bg": "#FEECEE", "fg": "#EB5757", "icon": "❌"},
    }

    def __init__(
        self,
        message: str,
        toast_type: str = "success",
        duration_ms: int = 3000,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.duration_ms = duration_ms
        self.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint)

        theme = self.TOAST_THEMES.get(toast_type, self.TOAST_THEMES["info"])

        self.setStyleSheet(f"""
            CuteToast {{
                background-color: {theme["bg"]};
                border: 1px solid {PALETTE.border};
                border-radius: 10px;
                padding: 10px 16px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        icon_lbl = QLabel(theme["icon"])
        layout.addWidget(icon_lbl)

        msg_lbl = QLabel(message)
        msg_lbl.setStyleSheet(f"color: {theme['fg']}; font-weight: 600; font-size: 12px;")
        layout.addWidget(msg_lbl)

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._dismiss)

    def show_toast(self) -> None:
        """Display the toast and start auto-dismiss timer."""
        self.show()
        self._timer.start(self.duration_ms)

    def _dismiss(self) -> None:
        self.hide()
        self.deleteLater()
