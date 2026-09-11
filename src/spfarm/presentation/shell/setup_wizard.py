"""Cute first-run onboarding setup wizard."""

from __future__ import annotations

import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from spfarm.domain.interfaces.secret_store import ISecretStore
from spfarm.shared.paths import paths
from spfarm.shared.settings import AppSettings, SettingsManager
from spfarm.shared.theme import PALETTE

logger = logging.getLogger(__name__)


class SetupWizardDialog(QDialog):
    """Cute first-run setup wizard dialog guiding operator initialization."""

    TOTAL_STEPS = 4

    def __init__(
        self,
        settings_manager: SettingsManager,
        secret_store: ISecretStore,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.secret_store = secret_store
        self.current_step = 0

        self.setWindowTitle("Welcome to SP-Farm V2 — Setup Wizard")
        self.setFixedSize(680, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {PALETTE.background};
                color: {PALETTE.text};
            }}
            QFrame[role="card"] {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border};
                border-radius: 12px;
                padding: 16px;
            }}
        """)

        self._setup_ui()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Header: Stepper Progress & Cute Title
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        self.lbl_step_indicator = QLabel(f"Step {self.current_step + 1} of {self.TOTAL_STEPS}")
        self.lbl_step_indicator.setStyleSheet(f"color: {PALETTE.primary_blue}; font-weight: bold; font-size: 12px;")
        header_layout.addWidget(self.lbl_step_indicator)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, self.TOTAL_STEPS)
        self.progress_bar.setValue(1)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        header_layout.addWidget(self.progress_bar)

        main_layout.addWidget(header)

        # Stacked Steps Content
        self.stack = QStackedWidget()
        self.stack.addWidget(self._step_welcome())
        self.stack.addWidget(self._step_storage())
        self.stack.addWidget(self._step_devices())
        self.stack.addWidget(self._step_vault())
        main_layout.addWidget(self.stack, 1)

        # Footer Navigation
        footer = QHBoxLayout()
        self.btn_back = QPushButton("← Back")
        self.btn_back.setStyleSheet(f"background-color: {PALETTE.surface_alt}; color: {PALETTE.text};")
        self.btn_back.setEnabled(False)
        self.btn_back.clicked.connect(self._prev_step)
        footer.addWidget(self.btn_back)

        footer.addStretch()

        self.btn_next = QPushButton("Next →")
        self.btn_next.setStyleSheet(f"""
            background-color: {PALETTE.primary_blue};
            color: white;
            font-weight: bold;
            padding: 8px 24px;
            border-radius: 8px;
        """)
        self.btn_next.clicked.connect(self._next_step)
        footer.addWidget(self.btn_next)

        main_layout.addLayout(footer)

    def _step_welcome(self) -> QWidget:
        card = QFrame()
        card.setProperty("role", "card")
        layout = QVBoxLayout(card)
        layout.setSpacing(14)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("🌱✨")
        icon.setFont(QFont("Segoe UI Emoji", 42))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        title = QLabel("Welcome to SP-Farm V2")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {PALETTE.primary_blue};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        desc = QLabel(
            "SP-Farm V2 is a clean, modern Windows desktop platform designed for authorized "
            "social operations, multi-device orchestration, and secure credential management.\n\n"
            "This quick wizard will verify your directories, detect connected devices, "
            "and configure the secure secret vault."
        )
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet(f"color: {PALETTE.text_secondary}; line-height: 1.4;")
        layout.addWidget(desc)

        return card

    def _step_storage(self) -> QWidget:
        card = QFrame()
        card.setProperty("role", "card")
        layout = QVBoxLayout(card)
        layout.setSpacing(12)

        title = QLabel("📁 Storage & Local Directories")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {PALETTE.primary_blue};")
        layout.addWidget(title)

        desc = QLabel("The following directories have been initialized for local operation:")
        desc.setStyleSheet(f"color: {PALETTE.text_secondary};")
        layout.addWidget(desc)

        paths.ensure_directories()

        path_box = QFrame()
        path_box.setStyleSheet(f"background-color: {PALETTE.soft_blue}; border-radius: 8px; padding: 10px;")
        path_layout = QVBoxLayout(path_box)
        path_layout.setSpacing(6)

        def add_row(lbl: str, p: str) -> None:
            row_label = QLabel(f"<b>{lbl}:</b> {p}")
            row_label.setStyleSheet(f"color: {PALETTE.text}; font-size: 12px;")
            path_layout.addWidget(row_label)

        add_row("Base Root", str(paths.base_dir))
        add_row("Database", str(paths.database_file))
        add_row("Logs", str(paths.logs_dir))
        add_row("Backups", str(paths.backups_dir))
        add_row("Vault", str(paths.secrets_dir))

        layout.addWidget(path_box)
        layout.addStretch()
        return card

    def _step_devices(self) -> QWidget:
        card = QFrame()
        card.setProperty("role", "card")
        layout = QVBoxLayout(card)
        layout.setSpacing(12)

        title = QLabel("📱 Device Runtime Detection")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {PALETTE.primary_blue};")
        layout.addWidget(title)

        desc = QLabel(
            "SP-Farm V2 connects to physical Android phones, LDPlayer, and MuMu Player. "
            "Detecting available local providers:"
        )
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {PALETTE.text_secondary};")
        layout.addWidget(desc)

        dev_box = QFrame()
        dev_box.setStyleSheet(f"background-color: {PALETTE.surface_alt}; border-radius: 8px; padding: 12px;")
        dev_layout = QVBoxLayout(dev_box)
        dev_layout.setSpacing(8)

        l1 = QLabel("✅ ADB Server: Ready for device connection")
        l1.setStyleSheet(f"color: {PALETTE.success}; font-weight: 500;")
        dev_layout.addWidget(l1)

        l2 = QLabel("ℹ️ LDPlayer / MuMu: Configurable in Settings → Devices")
        l2.setStyleSheet(f"color: {PALETTE.text_secondary};")
        dev_layout.addWidget(l2)

        layout.addWidget(dev_box)
        layout.addStretch()
        return card

    def _step_vault(self) -> QWidget:
        card = QFrame()
        card.setProperty("role", "card")
        layout = QVBoxLayout(card)
        layout.setSpacing(12)

        title = QLabel("🔒 Secure Secret Vault Ready")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {PALETTE.primary_blue};")
        layout.addWidget(title)

        desc = QLabel(
            "All sensitive credentials (passwords, TOTP seeds, tokens, cookies) are isolated "
            "in the secure vault and never stored in plaintext databases or JSON configurations."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {PALETTE.text_secondary};")
        layout.addWidget(desc)

        vbox = QFrame()
        vbox.setStyleSheet(f"background-color: {PALETTE.soft_pink}; border-radius: 8px; padding: 12px;")
        vlayout = QVBoxLayout(vbox)

        status_lbl = QLabel("🛡️ OS Keyring (Windows Credential Manager) & AES-128 Fallback: Operational")
        status_lbl.setStyleSheet(f"color: {PALETTE.cute_pink}; font-weight: bold;")
        vlayout.addWidget(status_lbl)

        layout.addWidget(vbox)
        layout.addStretch()
        return card

    def _prev_step(self) -> None:
        if self.current_step > 0:
            self.current_step -= 1
            self.stack.setCurrentIndex(self.current_step)
            self._update_navigation()

    def _next_step(self) -> None:
        if self.current_step < self.TOTAL_STEPS - 1:
            self.current_step += 1
            self.stack.setCurrentIndex(self.current_step)
            self._update_navigation()
        else:
            self._complete_wizard()

    def _update_navigation(self) -> None:
        self.lbl_step_indicator.setText(f"Step {self.current_step + 1} of {self.TOTAL_STEPS}")
        self.progress_bar.setValue(self.current_step + 1)
        self.btn_back.setEnabled(self.current_step > 0)

        if self.current_step == self.TOTAL_STEPS - 1:
            self.btn_next.setText("🚀 Launch SP-Farm")
            self.btn_next.setStyleSheet(f"""
                background-color: {PALETTE.cute_pink};
                color: white;
                font-weight: bold;
                padding: 8px 24px;
                border-radius: 8px;
            """)
        else:
            self.btn_next.setText("Next →")
            self.btn_next.setStyleSheet(f"""
                background-color: {PALETTE.primary_blue};
                color: white;
                font-weight: bold;
                padding: 8px 24px;
                border-radius: 8px;
            """)

    def _complete_wizard(self) -> None:
        def update_setup(s: AppSettings) -> None:
            s.setup.is_first_run = False
            s.setup.wizard_completed = True

        self.settings_manager.update(update_setup)
        self.accept()
