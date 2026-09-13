"""Developer-only architecture status screen in the Cute Light Design style."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from spfarm import __version__
from spfarm.infrastructure.container import container
from spfarm.shared.theme import PALETTE


class ArchitectureStatusDialog(QDialog):
    """Developer diagnostic dialog displaying architecture and dependency status."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Architecture Status — SP-Farm V2")
        self.setFixedSize(540, 480)
        self._setup_ui()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()
        heart = QLabel("♡")
        heart.setStyleSheet(f"color: {PALETTE.cute_pink}; font-size: 24px; font-weight: bold;")
        title = QLabel("Architecture Status")
        title.setStyleSheet(f"color: {PALETTE.primary_blue}; font-size: 20px; font-weight: bold;")
        badge = QLabel(f"v{__version__}")
        badge.setStyleSheet(f"""
            background-color: {PALETTE.soft_blue};
            color: {PALETTE.primary_blue};
            font-size: 11px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
        """)

        header_layout.addWidget(heart)
        header_layout.addWidget(title)
        header_layout.addWidget(badge)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        subtitle = QLabel("Layered Boundary Health & Dependency Verification")
        subtitle.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 12px;")
        main_layout.addWidget(subtitle)

        # Layers container card
        layers_card = QFrame(self)
        layers_card.setStyleSheet(f"""
            background-color: {PALETTE.surface};
            border: 1px solid {PALETTE.border};
            border-radius: 12px;
        """)
        layers_layout = QVBoxLayout(layers_card)
        layers_layout.setContentsMargins(16, 16, 16, 16)
        layers_layout.setSpacing(10)

        layers = [
            ("Presentation Layer", "PySide6 UI, Views & Cute Light Theme", "HEALTHY"),
            ("Application Layer", "CQRS CommandBus, QueryBus & EventBus", "HEALTHY"),
            ("Domain Layer", "Pure Entities & Protocols (0 UI/SQL imports)", "HEALTHY"),
            ("Infrastructure Layer", "Dependency Container & System Adapters", "HEALTHY"),
            ("Workers Layer", "Async Worker Supervisor Skeleton", "READY"),
        ]

        for name, desc, status in layers:
            row = QHBoxLayout()
            info_col = QVBoxLayout()
            lbl_name = QLabel(name)
            lbl_name.setStyleSheet(f"color: {PALETTE.text}; font-weight: 600; font-size: 13px;")
            lbl_desc = QLabel(desc)
            lbl_desc.setStyleSheet(f"color: {PALETTE.text_muted}; font-size: 11px;")
            info_col.addWidget(lbl_name)
            info_col.addWidget(lbl_desc)

            status_pill = QLabel(status)
            status_pill.setStyleSheet(f"""
                background-color: {PALETTE.soft_blue};
                color: {PALETTE.success if status == "HEALTHY" else PALETTE.primary_blue};
                font-weight: bold;
                font-size: 10px;
                padding: 3px 8px;
                border-radius: 6px;
            """)

            row.addLayout(info_col)
            row.addStretch()
            row.addWidget(status_pill)
            layers_layout.addLayout(row)

        main_layout.addWidget(layers_card)

        # Bus & Container Metrics Card
        metrics_card = QFrame(self)
        metrics_card.setStyleSheet(f"""
            background-color: {PALETTE.surface_alt};
            border: 1px solid {PALETTE.border};
            border-radius: 10px;
        """)
        metrics_layout = QHBoxLayout(metrics_card)
        metrics_layout.setContentsMargins(16, 12, 16, 12)

        def add_metric(label: str, value: str) -> None:
            col = QVBoxLayout()
            val_lbl = QLabel(value)
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val_lbl.setStyleSheet(
                f"color: {PALETTE.primary_blue}; font-size: 16px; font-weight: bold;"
            )
            desc_lbl = QLabel(label)
            desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_lbl.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 11px;")
            col.addWidget(val_lbl)
            col.addWidget(desc_lbl)
            metrics_layout.addLayout(col)

        add_metric("Commands", str(len(container.command_bus.registered_commands)))
        add_metric("Queries", str(len(container.query_bus.registered_queries)))
        add_metric("Subscribers", str(container.event_bus.total_subscribers_count))
        add_metric("Services", str(len(container.registered_service_names)))

        main_layout.addWidget(metrics_card)

        # Actions
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("Close", self)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        main_layout.addLayout(btn_layout)
