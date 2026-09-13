"""CuteButton component supporting primary, cute pink, secondary, ghost, and danger roles."""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QPushButton, QWidget


class CuteButton(QPushButton):
    """Button adhering to Cute Light Design System tokens."""

    def __init__(
        self,
        text: str = "",
        role: str = "primary",  # primary, cute, secondary, ghost, danger
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setProperty("role", role)
        self.setMinimumHeight(34)
