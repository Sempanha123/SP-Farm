"""Settings dialog with category navigation and masked secret management."""

from __future__ import annotations

import logging
from typing import Optional

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from spfarm.application.services.masked_secret import MaskedSecret
from spfarm.domain.interfaces.secret_store import ISecretStore
from spfarm.infrastructure.secrets.ref import make_secret_ref
from spfarm.shared.settings import AppSettings, SettingsManager
from spfarm.shared.theme import PALETTE

logger = logging.getLogger(__name__)


class SettingsDialog(QDialog):
    """Cute Light settings management dialog."""

    def __init__(
        self,
        settings_manager: SettingsManager,
        secret_store: ISecretStore,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.secret_store = secret_store
        self._current_settings = self.settings_manager.get()

        self.setWindowTitle("Settings & Security Vault — SP-Farm V2")
        self.setMinimumSize(820, 560)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {PALETTE.background};
                color: {PALETTE.text};
            }}
            QListWidget {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border};
                border-radius: 10px;
                padding: 6px;
                outline: none;
            }}
            QListWidget::item {{
                padding: 10px 14px;
                border-radius: 6px;
                margin-bottom: 4px;
                font-weight: 500;
            }}
            QListWidget::item:selected {{
                background-color: {PALETTE.soft_blue};
                color: {PALETTE.primary_blue};
                font-weight: bold;
            }}
            QGroupBox {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border};
                border-radius: 10px;
                margin-top: 14px;
                padding: 14px;
                font-weight: 600;
                color: {PALETTE.primary_blue};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
            }}
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border_strong};
                border-radius: 6px;
                padding: 6px 10px;
                color: {PALETTE.text};
            }}
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
                border: 1.5px solid {PALETTE.primary_blue};
            }}
        """)

        self._setup_ui()
        self._load_values()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Header banner
        header = QFrame()
        header.setStyleSheet(f"""
            background-color: {PALETTE.surface};
            border: 1px solid {PALETTE.border};
            border-radius: 10px;
            padding: 10px 16px;
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(8, 6, 8, 6)

        title_lbl = QLabel("⚙️ Application Settings & Vault")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title_lbl.setFont(font)
        title_lbl.setStyleSheet(f"color: {PALETTE.primary_blue};")
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()

        badge_lbl = QLabel("🛡️ Vault Active")
        badge_lbl.setStyleSheet(f"""
            background-color: {PALETTE.soft_pink};
            color: {PALETTE.cute_pink};
            font-weight: bold;
            border-radius: 12px;
            padding: 4px 10px;
        """)
        header_layout.addWidget(badge_lbl)
        main_layout.addWidget(header)

        # Body: Categories sidebar + Stacked views
        body_layout = QHBoxLayout()
        body_layout.setSpacing(16)

        self.category_list = QListWidget()
        self.category_list.setFixedWidth(190)
        self.category_list.addItem(QListWidgetItem("🌐 General"))
        self.category_list.addItem(QListWidgetItem("🎨 Appearance"))
        self.category_list.addItem(QListWidgetItem("📁 Storage"))
        self.category_list.addItem(QListWidgetItem("📱 Devices"))
        self.category_list.addItem(QListWidgetItem("⚡ Automation"))
        self.category_list.addItem(QListWidgetItem("🔒 Security Vault"))
        self.category_list.setCurrentRow(0)
        self.category_list.currentRowChanged.connect(self._on_category_changed)
        body_layout.addWidget(self.category_list)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self._create_general_page())
        self.stacked_widget.addWidget(self._create_appearance_page())
        self.stacked_widget.addWidget(self._create_storage_page())
        self.stacked_widget.addWidget(self._create_devices_page())
        self.stacked_widget.addWidget(self._create_automation_page())
        self.stacked_widget.addWidget(self._create_security_page())
        body_layout.addWidget(self.stacked_widget, 1)

        main_layout.addLayout(body_layout, 1)

        # Footer buttons
        footer_layout = QHBoxLayout()
        self.btn_reset = QPushButton("🔄 Reset Defaults")
        self.btn_reset.setStyleSheet(
            f"background-color: {PALETTE.surface_alt}; color: {PALETTE.text_secondary};"
        )
        self.btn_reset.clicked.connect(self._on_reset_defaults)
        footer_layout.addWidget(self.btn_reset)

        footer_layout.addStretch()

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet(
            f"background-color: {PALETTE.surface_alt}; color: {PALETTE.text};"
        )
        self.btn_cancel.clicked.connect(self.reject)
        footer_layout.addWidget(self.btn_cancel)

        self.btn_save = QPushButton("💾 Save Changes")
        self.btn_save.setStyleSheet(f"""
            background-color: {PALETTE.cute_pink};
            color: white;
            font-weight: bold;
            padding: 8px 20px;
            border-radius: 8px;
        """)
        self.btn_save.clicked.connect(self._on_save)
        footer_layout.addWidget(self.btn_save)

        main_layout.addLayout(footer_layout)

    def _on_category_changed(self, row: int) -> None:
        self.stacked_widget.setCurrentIndex(row)

    def _create_general_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        group = QGroupBox("General Configuration")
        form = QFormLayout(group)
        form.setVerticalSpacing(12)

        self.txt_app_name = QLineEdit()
        self.cmb_environment = QComboBox()
        self.cmb_environment.addItems(["production", "development", "test"])

        self.cmb_log_level = QComboBox()
        self.cmb_log_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])

        form.addRow("Application Name:", self.txt_app_name)
        form.addRow("Environment:", self.cmb_environment)
        form.addRow("Log Level:", self.cmb_log_level)

        layout.addWidget(group)
        layout.addStretch()
        return page

    def _create_appearance_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        group = QGroupBox("Cute Light Theme & Visuals")
        form = QFormLayout(group)
        form.setVerticalSpacing(12)

        self.cmb_theme = QComboBox()
        self.cmb_theme.addItems(["light_blue", "pink", "lavender", "dark_blue", "system"])

        self.spn_scale = QDoubleSpinBox()
        self.spn_scale.setRange(0.5, 3.0)
        self.spn_scale.setSingleStep(0.1)

        self.chk_animations = QCheckBox("Enable Smooth UI Animations")

        form.addRow("Theme Palette:", self.cmb_theme)
        form.addRow("Scale Factor:", self.spn_scale)
        form.addRow("", self.chk_animations)

        layout.addWidget(group)
        layout.addStretch()
        return page

    def _create_storage_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        group = QGroupBox("Storage Directories & Retention")
        form = QFormLayout(group)
        form.setVerticalSpacing(12)

        self.txt_data_dir = QLineEdit()
        self.txt_data_dir.setPlaceholderText("(Default: AppData/spfarm/data)")

        self.txt_logs_dir = QLineEdit()
        self.txt_logs_dir.setPlaceholderText("(Default: AppData/spfarm/logs)")

        self.txt_backups_dir = QLineEdit()
        self.txt_backups_dir.setPlaceholderText("(Default: AppData/spfarm/backups)")

        self.chk_auto_backup = QCheckBox("Enable Automatic Database Backups")
        self.spn_backup_interval = QSpinBox()
        self.spn_backup_interval.setRange(1, 168)
        self.spn_backup_interval.setSuffix(" hrs")

        self.spn_retained_backups = QSpinBox()
        self.spn_retained_backups.setRange(1, 100)

        form.addRow("Data Directory:", self.txt_data_dir)
        form.addRow("Logs Directory:", self.txt_logs_dir)
        form.addRow("Backups Directory:", self.txt_backups_dir)
        form.addRow("", self.chk_auto_backup)
        form.addRow("Backup Frequency:", self.spn_backup_interval)
        form.addRow("Retained Snapshots:", self.spn_retained_backups)

        layout.addWidget(group)
        layout.addStretch()
        return page

    def _create_devices_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        group = QGroupBox("Device Runtime Providers")
        form = QFormLayout(group)
        form.setVerticalSpacing(12)

        self.txt_adb_path = QLineEdit()
        self.txt_adb_path.setPlaceholderText("(Auto-detected from PATH or standard SDK)")

        self.txt_appium_path = QLineEdit()
        self.txt_appium_path.setPlaceholderText("(Auto-detected from PATH)")

        self.txt_ldplayer_path = QLineEdit()
        self.txt_ldplayer_path.setPlaceholderText("(e.g. C:\\LDPlayer\\LDPlayer9)")

        self.txt_mumu_path = QLineEdit()
        self.txt_mumu_path.setPlaceholderText("(e.g. C:\\Program Files\\Netease\\MuMuPlayerGlobal)")

        self.spn_poll_interval = QDoubleSpinBox()
        self.spn_poll_interval.setRange(1.0, 60.0)
        self.spn_poll_interval.setSuffix(" sec")

        self.chk_auto_discover = QCheckBox("Automatically Discover Connected Devices")

        form.addRow("ADB Executable:", self.txt_adb_path)
        form.addRow("Appium Executable:", self.txt_appium_path)
        form.addRow("LDPlayer Path:", self.txt_ldplayer_path)
        form.addRow("MuMu Player Path:", self.txt_mumu_path)
        form.addRow("Poll Interval:", self.spn_poll_interval)
        form.addRow("", self.chk_auto_discover)

        layout.addWidget(group)
        layout.addStretch()
        return page

    def _create_automation_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        group = QGroupBox("Automation Engine")
        form = QFormLayout(group)
        form.setVerticalSpacing(12)

        self.spn_timeout = QSpinBox()
        self.spn_timeout.setRange(10, 600)
        self.spn_timeout.setSuffix(" sec")

        self.spn_max_concurrent = QSpinBox()
        self.spn_max_concurrent.setRange(1, 20)

        self.cmb_emulation = QComboBox()
        self.cmb_emulation.addItems(["standard", "high", "low"])

        self.spn_jitter = QDoubleSpinBox()
        self.spn_jitter.setRange(0.0, 100.0)
        self.spn_jitter.setSuffix(" %")

        form.addRow("Operation Timeout:", self.spn_timeout)
        form.addRow("Max Concurrent Jobs:", self.spn_max_concurrent)
        form.addRow("Human Emulation Level:", self.cmb_emulation)
        form.addRow("Delay Jitter:", self.spn_jitter)

        layout.addWidget(group)
        layout.addStretch()
        return page

    def _create_security_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        # Overview group
        info_group = QGroupBox("Vault Status & Storage Backend")
        info_layout = QVBoxLayout(info_group)
        backend_desc = "🔒 Protected by OS Keyring (Windows Credential Manager / DPAPI) with AES-128-CBC local encrypted fallback."
        lbl_desc = QLabel(backend_desc)
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet(f"color: {PALETTE.text_secondary};")
        info_layout.addWidget(lbl_desc)
        layout.addWidget(info_group)

        # Test Credential Entry group
        secret_group = QGroupBox("Vault Secret Inspector & Entry")
        sform = QFormLayout(secret_group)
        sform.setVerticalSpacing(10)

        self.cmb_secret_category = QComboBox()
        self.cmb_secret_category.addItems(["accounts", "proxies", "mail", "tokens"])

        self.txt_secret_entity = QLineEdit("acc_demo")
        self.cmb_secret_key = QComboBox()
        self.cmb_secret_key.addItems(["password", "cookie", "totp_seed", "session", "api_token"])

        # Masked value row with Reveal and Copy buttons
        val_container = QWidget()
        val_layout = QHBoxLayout(val_container)
        val_layout.setContentsMargins(0, 0, 0, 0)
        val_layout.setSpacing(6)

        self.txt_secret_val = QLineEdit()
        self.txt_secret_val.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_secret_val.setPlaceholderText("Enter secret value to store...")
        val_layout.addWidget(self.txt_secret_val, 1)

        self.btn_reveal = QPushButton("👁️ Reveal")
        self.btn_reveal.setStyleSheet(
            f"background-color: {PALETTE.soft_blue}; color: {PALETTE.primary_blue};"
        )
        self.btn_reveal.clicked.connect(self._toggle_reveal_secret)
        val_layout.addWidget(self.btn_reveal)

        self.btn_copy = QPushButton("📋 Copy")
        self.btn_copy.setStyleSheet(
            f"background-color: {PALETTE.soft_pink}; color: {PALETTE.cute_pink};"
        )
        self.btn_copy.clicked.connect(self._copy_secret_to_clipboard)
        val_layout.addWidget(self.btn_copy)

        sform.addRow("Category:", self.cmb_secret_category)
        sform.addRow("Entity ID:", self.txt_secret_entity)
        sform.addRow("Secret Key:", self.cmb_secret_key)
        sform.addRow("Secret Value:", val_container)

        btn_store_layout = QHBoxLayout()
        self.btn_save_secret = QPushButton("Save Secret to Vault")
        self.btn_save_secret.setStyleSheet(
            f"background-color: {PALETTE.primary_blue}; color: white;"
        )
        self.btn_save_secret.clicked.connect(self._save_secret_action)
        btn_store_layout.addWidget(self.btn_save_secret)

        self.lbl_vault_feedback = QLabel("")
        self.lbl_vault_feedback.setStyleSheet(f"color: {PALETTE.success}; font-weight: 500;")
        btn_store_layout.addWidget(self.lbl_vault_feedback)
        btn_store_layout.addStretch()

        sform.addRow("", btn_store_layout)
        layout.addWidget(secret_group)

        layout.addStretch()
        return page

    def _toggle_reveal_secret(self) -> None:
        if self.txt_secret_val.echoMode() == QLineEdit.EchoMode.Password:
            self.txt_secret_val.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_reveal.setText("🙈 Hide")
        else:
            self.txt_secret_val.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_reveal.setText("👁️ Reveal")

    def _copy_secret_to_clipboard(self) -> None:
        ref = make_secret_ref(
            category=self.cmb_secret_category.currentText(),
            entity_id=self.txt_secret_entity.text().strip(),
            key_name=self.cmb_secret_key.currentText(),
        )
        masked = MaskedSecret.from_ref(ref, self.secret_store)
        if not masked.is_set and not self.txt_secret_val.text():
            QMessageBox.information(self, "Copy Secret", "No secret stored for this reference.")
            return

        def copy_cb(text: str) -> None:
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText(text)

        if masked.is_set:
            masked.copy(self.secret_store, copy_cb)
        else:
            copy_cb(self.txt_secret_val.text())

        self.lbl_vault_feedback.setText("✅ Copied to clipboard!")

    def _save_secret_action(self) -> None:
        val = self.txt_secret_val.text()
        if not val:
            QMessageBox.warning(self, "Save Secret", "Please enter a secret value to store.")
            return

        ref = make_secret_ref(
            category=self.cmb_secret_category.currentText(),
            entity_id=self.txt_secret_entity.text().strip(),
            key_name=self.cmb_secret_key.currentText(),
        )
        masked = MaskedSecret(secret_ref=ref)
        masked.update(val, self.secret_store)
        self.lbl_vault_feedback.setText(f"✅ Stored under {ref}")
        self.txt_secret_val.clear()
        self.txt_secret_val.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn_reveal.setText("👁️ Reveal")

    def _load_values(self) -> None:
        s = self._current_settings
        self.txt_app_name.setText(s.general.app_name)
        self.cmb_environment.setCurrentText(s.general.environment)
        self.cmb_log_level.setCurrentText(s.general.log_level)

        self.cmb_theme.setCurrentText(s.appearance.theme)
        self.spn_scale.setValue(s.appearance.scale_factor)
        self.chk_animations.setChecked(s.appearance.enable_animations)

        self.txt_data_dir.setText(s.storage.data_dir)
        self.txt_logs_dir.setText(s.storage.logs_dir)
        self.txt_backups_dir.setText(s.storage.backups_dir)
        self.chk_auto_backup.setChecked(s.storage.auto_backup_enabled)
        self.spn_backup_interval.setValue(s.storage.auto_backup_interval_hours)
        self.spn_retained_backups.setValue(s.storage.max_retained_backups)

        self.txt_adb_path.setText(s.devices.adb_path)
        self.txt_appium_path.setText(s.devices.appium_path)
        self.txt_ldplayer_path.setText(s.devices.ldplayer_path)
        self.txt_mumu_path.setText(s.devices.mumu_path)
        self.spn_poll_interval.setValue(s.devices.poll_interval_seconds)
        self.chk_auto_discover.setChecked(s.devices.auto_discover_devices)

        self.spn_timeout.setValue(s.automation.default_timeout_seconds)
        self.spn_max_concurrent.setValue(s.automation.max_concurrent_jobs)
        self.cmb_emulation.setCurrentText(s.automation.human_emulation_level)
        self.spn_jitter.setValue(s.automation.delay_jitter_percent)

    def _on_save(self) -> None:
        def update_fn(s: AppSettings) -> None:
            s.general.app_name = self.txt_app_name.text().strip()
            s.general.environment = self.cmb_environment.currentText()
            s.general.log_level = self.cmb_log_level.currentText()

            s.appearance.theme = self.cmb_theme.currentText()
            s.appearance.scale_factor = self.spn_scale.value()
            s.appearance.enable_animations = self.chk_animations.isChecked()

            s.storage.data_dir = self.txt_data_dir.text().strip()
            s.storage.logs_dir = self.txt_logs_dir.text().strip()
            s.storage.backups_dir = self.txt_backups_dir.text().strip()
            s.storage.auto_backup_enabled = self.chk_auto_backup.isChecked()
            s.storage.auto_backup_interval_hours = self.spn_backup_interval.value()
            s.storage.max_retained_backups = self.spn_retained_backups.value()

            s.devices.adb_path = self.txt_adb_path.text().strip()
            s.devices.appium_path = self.txt_appium_path.text().strip()
            s.devices.ldplayer_path = self.txt_ldplayer_path.text().strip()
            s.devices.mumu_path = self.txt_mumu_path.text().strip()
            s.devices.poll_interval_seconds = self.spn_poll_interval.value()
            s.devices.auto_discover_devices = self.chk_auto_discover.isChecked()

            s.automation.default_timeout_seconds = self.spn_timeout.value()
            s.automation.max_concurrent_jobs = self.spn_max_concurrent.value()
            s.automation.human_emulation_level = self.cmb_emulation.currentText()
            s.automation.delay_jitter_percent = self.spn_jitter.value()

        self.settings_manager.update(update_fn)
        self.accept()

    def _on_reset_defaults(self) -> None:
        ans = QMessageBox.question(
            self,
            "Reset Defaults",
            "Are you sure you want to reset all settings to default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if ans == QMessageBox.StandardButton.Yes:
            self._current_settings = self.settings_manager.reset()
            self._load_values()
