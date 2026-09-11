"""CuteInspector right-side slide-in panel for routine edits without modal dialogs."""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from spfarm.shared.theme import PALETTE


class CuteInspector(QFrame):
    """Right-side collapsible detail inspector panel."""

    closed = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(360)
        self.setStyleSheet(f"""
            CuteInspector {{
                background-color: {PALETTE.surface};
                border-left: 1px solid {PALETTE.border};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        # Header with title and close button
        header = QHBoxLayout()
        self.lbl_title = QLabel("Inspector")
        self.lbl_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.lbl_title.setStyleSheet(f"color: {PALETTE.primary};")
        header.addWidget(self.lbl_title)
        header.addStretch()

        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(26, 26)
        self.btn_close.setStyleSheet(f"""
            QPushButton {{
                background-color: {PALETTE.surface_alt};
                color: {PALETTE.text_secondary};
                border-radius: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {PALETTE.soft_pink};
                color: {PALETTE.danger};
            }}
        """)
        self.btn_close.clicked.connect(self._on_close)
        header.addWidget(self.btn_close)
        layout.addLayout(header)

        # Subtitle or status badge row
        self.lbl_subtitle = QLabel("")
        self.lbl_subtitle.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 11px;")
        layout.addWidget(self.lbl_subtitle)

        # Scrollable content area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)
        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area, 1)

        # Footer actions area
        self.footer_widget = QWidget()
        self.footer_layout = QHBoxLayout(self.footer_widget)
        self.footer_layout.setContentsMargins(0, 4, 0, 0)
        layout.addWidget(self.footer_widget)

    def set_header(self, title: str, subtitle: str = "") -> None:
        """Set the inspector title and optional subtitle."""
        self.lbl_title.setText(title)
        self.lbl_subtitle.setText(subtitle)
        self.lbl_subtitle.setVisible(bool(subtitle))

    def set_content(self, widget: QWidget) -> None:
        """Replace the inspector content with the given widget."""
        # Clear existing
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.content_layout.addWidget(widget)

    def _on_close(self) -> None:
        self.hide()
        self.closed.emit()
