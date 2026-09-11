"""CuteStepper horizontal multi-step progress indicator."""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from spfarm.shared.theme import PALETTE


class CuteStepper(QWidget):
    """Horizontal stepper for multi-step wizards adhering to Cute Light styling."""

    step_changed = Signal(int)

    def __init__(
        self,
        steps: list[str],
        current_step: int = 0,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.steps = steps
        self.current_step = current_step
        self._step_widgets: list[tuple[QLabel, QLabel]] = []

        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for i, label_text in enumerate(self.steps):
            step_container = QWidget()
            s_layout = QHBoxLayout(step_container)
            s_layout.setContentsMargins(0, 0, 0, 0)
            s_layout.setSpacing(6)

            # Circle badge
            circle = QLabel(str(i + 1))
            circle.setFixedSize(24, 24)
            circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            circle.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))

            # Step title
            title = QLabel(label_text)
            title.setFont(QFont("Segoe UI", 11, QFont.Weight.Normal))

            s_layout.addWidget(circle)
            s_layout.addWidget(title)
            layout.addWidget(step_container)

            self._step_widgets.append((circle, title))

            # Connecting divider line except after last step
            if i < len(self.steps) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFixedWidth(28)
                line.setStyleSheet(f"background-color: {PALETTE.border_strong}; max-height: 2px;")
                layout.addWidget(line)

        self._update_styles()

    def set_step(self, step_idx: int) -> None:
        """Set current active step index (0-indexed)."""
        if 0 <= step_idx < len(self.steps):
            self.current_step = step_idx
            self._update_styles()
            self.step_changed.emit(self.current_step)

    def _update_styles(self) -> None:
        for i, (circle, title) in enumerate(self._step_widgets):
            if i < self.current_step:
                # Completed step
                circle.setText("✓")
                circle.setStyleSheet(f"""
                    background-color: {PALETTE.success};
                    color: white;
                    border-radius: 12px;
                """)
                title.setStyleSheet(f"color: {PALETTE.text}; font-weight: 500;")
            elif i == self.current_step:
                # Current active step
                circle.setText(str(i + 1))
                circle.setStyleSheet(f"""
                    background-color: {PALETTE.primary};
                    color: white;
                    border-radius: 12px;
                """)
                title.setStyleSheet(f"color: {PALETTE.primary}; font-weight: bold;")
            else:
                # Upcoming step
                circle.setText(str(i + 1))
                circle.setStyleSheet(f"""
                    background-color: {PALETTE.surface_alt};
                    color: {PALETTE.text_secondary};
                    border-radius: 12px;
                    border: 1px solid {PALETTE.border};
                """)
                title.setStyleSheet(f"color: {PALETTE.text_muted}; font-weight: normal;")
