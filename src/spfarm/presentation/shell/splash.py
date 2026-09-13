"""Cute light boot/splash screen for SP-Farm V2."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from spfarm import __version__
from spfarm.shared.theme import PALETTE


class SplashWindow(QWidget):
    """Minimal cute light boot screen displayed during startup initialization."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("SP-Farm V2")
        self.setFixedSize(480, 280)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self._setup_ui()

    def _setup_ui(self) -> None:
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(12, 12, 12, 12)

        # Card container with soft shadow styling & border
        self.card = QFrame(self)
        self.card.setObjectName("splashCard")
        self.card.setStyleSheet(f"""
            QFrame#splashCard {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border};
                border-radius: 20px;
            }}
        """)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(32, 28, 32, 24)
        card_layout.setSpacing(12)

        # Header with cute heart logo
        header_layout = QHBoxLayout()
        heart_label = QLabel("♡")
        heart_label.setStyleSheet(
            f"color: {PALETTE.cute_pink}; font-size: 28px; font-weight: bold;"
        )
        title_label = QLabel("SP FARM")
        title_label.setStyleSheet(
            f"color: {PALETTE.primary_blue}; font-size: 24px; font-weight: 800; letter-spacing: 1px;"
        )

        version_badge = QLabel(f"v{__version__}")
        version_badge.setStyleSheet(f"""
            background-color: {PALETTE.soft_blue};
            color: {PALETTE.primary_blue};
            font-size: 11px;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 6px;
        """)

        header_layout.addWidget(heart_label)
        header_layout.addWidget(title_label)
        header_layout.addWidget(version_badge)
        header_layout.addStretch()

        card_layout.addLayout(header_layout)

        # Subtitle
        subtitle_label = QLabel("Modern Desktop Operations Platform")
        subtitle_label.setStyleSheet(
            f"color: {PALETTE.text_secondary}; font-size: 13px; font-weight: 500;"
        )
        card_layout.addWidget(subtitle_label)

        card_layout.addSpacing(16)

        # Progress bar
        self.progress_bar = QProgressBar(self.card)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(15)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {PALETTE.surface_alt};
                border: none;
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {PALETTE.sky}, stop:1 {PALETTE.cute_pink});
                border-radius: 4px;
            }}
        """)
        card_layout.addWidget(self.progress_bar)

        # Status text
        self.status_label = QLabel("Ready", self.card)
        self.status_label.setStyleSheet(f"color: {PALETTE.text_muted}; font-size: 12px;")
        card_layout.addWidget(self.status_label)

        card_layout.addStretch()

        outer_layout.addWidget(self.card)

    def set_status(self, text: str, progress: int | None = None) -> None:
        """Update the displayed loading status and progress value."""
        self.status_label.setText(text)
        if progress is not None:
            self.progress_bar.setValue(progress)

    def center_on_screen(self) -> None:
        """Center splash screen on active monitor."""
        screen = self.screen()
        if screen:
            geo = screen.geometry()
            x = (geo.width() - self.width()) // 2
            y = (geo.height() - self.height()) // 2
            self.move(geo.x() + x, geo.y() + y)
