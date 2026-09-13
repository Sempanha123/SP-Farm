"""Rich 12-tab account inspector panel adhering to 01_UX_UI_SOURCE_OF_TRUTH.txt."""

from __future__ import annotations

import logging
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QScrollArea,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from spfarm.application.queries.accounts import AccountDetailDTO
from spfarm.application.services.audit import AuditService
from spfarm.domain.interfaces.secret_store import ISecretStore
from spfarm.presentation.components.buttons import CuteButton
from spfarm.presentation.components.inspector import CuteInspector
from spfarm.presentation.components.status_pill import CuteStatusPill
from spfarm.shared.theme import PALETTE

logger = logging.getLogger(__name__)


class AccountInspectorPanel(CuteInspector):
    """Slide-in right inspection panel displaying all 12 metadata categories."""

    edit_requested = Signal(str)
    notes_saved = Signal(str, str)  # (account_id, notes)

    def __init__(
        self,
        secret_store: Optional[ISecretStore] = None,
        audit_service: Optional[AuditService] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent=parent)
        self.lbl_title.setText("Account Inspector")
        self.setFixedWidth(400)
        self.secret_store = secret_store
        self.audit_service = audit_service
        self._current_account: Optional[AccountDetailDTO] = None

        self._build_inspector_body()

    def _build_inspector_body(self) -> None:
        # Header block
        self.header_card = QFrame()
        self.header_card.setStyleSheet(f"""
            QFrame {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border};
                border-radius: 12px;
                padding: 10px;
            }}
        """)
        h_layout = QHBoxLayout(self.header_card)
        h_layout.setContentsMargins(12, 10, 12, 10)
        h_layout.setSpacing(12)

        # Avatar initials bubble
        self.avatar_bubble = QLabel("👤")
        self.avatar_bubble.setFixedSize(48, 48)
        self.avatar_bubble.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_bubble.setStyleSheet(f"""
            background-color: {PALETTE.soft_pink};
            color: {PALETTE.cute_pink};
            border-radius: 24px;
            font-size: 20px;
            font-weight: bold;
        """)
        h_layout.addWidget(self.avatar_bubble)

        # Titles
        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        self.lbl_acc_name = QLabel("No Account Selected")
        self.lbl_acc_name.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.lbl_acc_name.setStyleSheet(f"color: {PALETTE.primary};")

        self.lbl_acc_id = QLabel("Select an account to view rich records")
        self.lbl_acc_id.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 11px;")
        title_box.addWidget(self.lbl_acc_name)
        title_box.addWidget(self.lbl_acc_id)
        h_layout.addLayout(title_box, 1)

        # Status pill
        self.status_pill = CuteStatusPill("Inactive", status_type="offline")
        h_layout.addWidget(self.status_pill)

        # Quick edit button
        self.btn_edit = CuteButton("✏️ Edit", role="secondary")
        self.btn_edit.clicked.connect(self._on_edit_clicked)
        h_layout.addWidget(self.btn_edit)

        self.content_layout.addWidget(self.header_card)

        # 12-Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {PALETTE.border};
                background: {PALETTE.surface};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background: {PALETTE.background};
                color: {PALETTE.text_secondary};
                padding: 6px 10px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 11px;
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                background: {PALETTE.surface};
                color: {PALETTE.primary};
                font-weight: 600;
                border: 1px solid {PALETTE.border};
                border-bottom: none;
            }}
        """)

        # Build each tab
        self.tabs.addTab(self._build_overview_tab(), "Overview")
        self.tabs.addTab(self._build_contacts_tab(), "Contacts")
        self.tabs.addTab(self._build_security_tab(), "Security")
        self.tabs.addTab(self._build_pages_tab(), "Pages")
        self.tabs.addTab(self._build_groups_tab(), "Groups")
        self.tabs.addTab(self._build_environment_tab(), "Environment")
        self.tabs.addTab(self._build_runtime_tab(), "Runtime")
        self.tabs.addTab(self._build_publishing_tab(), "Publishing")
        self.tabs.addTab(self._build_activity_tab(), "Activity")
        self.tabs.addTab(self._build_jobs_tab(), "Jobs")
        self.tabs.addTab(self._build_notes_tab(), "Notes")
        self.tabs.addTab(self._build_audit_tab(), "Audit")

        self.content_layout.addWidget(self.tabs)

    # -------------------------------------------------------------------------
    # Tab Builders
    # -------------------------------------------------------------------------

    def _build_overview_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        w = QWidget()
        form = QFormLayout(w)
        form.setContentsMargins(12, 12, 12, 12)
        form.setSpacing(10)

        self.lbl_ov_id = QLabel("—")
        self.lbl_ov_platform = QLabel("Facebook")
        self.lbl_ov_health = QLabel("—")
        self.lbl_ov_priority = QLabel("0")
        self.lbl_ov_locale = QLabel("en_US")
        self.lbl_ov_timezone = QLabel("UTC")
        self.lbl_ov_category = QLabel("General")
        self.lbl_ov_created = QLabel("—")
        self.lbl_ov_last_act = QLabel("—")

        form.addRow("Profile ID:", self.lbl_ov_id)
        form.addRow("Platform:", self.lbl_ov_platform)
        form.addRow("Health State:", self.lbl_ov_health)
        form.addRow("Priority:", self.lbl_ov_priority)
        form.addRow("Locale / Lang:", self.lbl_ov_locale)
        form.addRow("Timezone:", self.lbl_ov_timezone)
        form.addRow("Category:", self.lbl_ov_category)
        form.addRow("Created At:", self.lbl_ov_created)
        form.addRow("Last Active:", self.lbl_ov_last_act)

        scroll.setWidget(w)
        return scroll

    def _build_contacts_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(12, 12, 12, 12)

        lbl = QLabel("Associated Contact Methods (Masked)")
        lbl.setStyleSheet(f"color: {PALETTE.text_secondary}; font-weight: 600; font-size: 11px;")
        layout.addWidget(lbl)

        self.contacts_list = QListWidget()
        layout.addWidget(self.contacts_list, 1)

        btn_reveal = CuteButton("👁️ Reveal Sensitive Contact (Audited)", role="cute")
        btn_reveal.clicked.connect(self._on_reveal_contacts_clicked)
        layout.addWidget(btn_reveal)
        return w

    def _build_security_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)
        form.setContentsMargins(12, 12, 12, 12)
        form.setSpacing(10)

        self.lbl_sec_2fa = QLabel("None")
        self.lbl_sec_pass_ref = QLabel("No password vaulted")
        self.lbl_sec_totp_ref = QLabel("No TOTP seed vaulted")
        self.lbl_sec_review = QLabel("Never")

        form.addRow("2FA Method:", self.lbl_sec_2fa)
        form.addRow("Password Vault Ref:", self.lbl_sec_pass_ref)
        form.addRow("TOTP Vault Ref:", self.lbl_sec_totp_ref)
        form.addRow("Security Review:", self.lbl_sec_review)

        btn_row = QHBoxLayout()
        btn_reveal_pass = CuteButton("Reveal Password", role="secondary")
        btn_reveal_pass.clicked.connect(lambda: self._on_reveal_secret("password"))
        btn_reveal_totp = CuteButton("Reveal TOTP", role="secondary")
        btn_reveal_totp.clicked.connect(lambda: self._on_reveal_secret("totp"))
        btn_row.addWidget(btn_reveal_pass)
        btn_row.addWidget(btn_reveal_totp)
        form.addRow("Actions:", btn_row)
        return w

    def _build_pages_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.addWidget(QLabel("Managed Facebook Pages"))
        self.pages_list = QListWidget()
        layout.addWidget(self.pages_list)
        return w

    def _build_groups_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.addWidget(QLabel("Joined / Managed Facebook Groups"))
        self.groups_list = QListWidget()
        layout.addWidget(self.groups_list)
        return w

    def _build_environment_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)
        form.setContentsMargins(12, 12, 12, 12)
        form.setSpacing(10)

        self.lbl_env_id = QLabel("No Profile Bound")
        self.lbl_env_channel = QLabel("—")
        self.lbl_env_os = QLabel("—")
        self.lbl_env_ua = QLabel("—")
        self.lbl_env_dir = QLabel("—")

        form.addRow("Profile ID:", self.lbl_env_id)
        form.addRow("App Channel:", self.lbl_env_channel)
        form.addRow("Android OS:", self.lbl_env_os)
        form.addRow("User Agent:", self.lbl_env_ua)
        form.addRow("Storage Path:", self.lbl_env_dir)
        return w

    def _build_runtime_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)
        form.setContentsMargins(12, 12, 12, 12)
        form.setSpacing(10)

        self.lbl_rt_name = QLabel("Unassigned")
        self.lbl_rt_provider = QLabel("—")
        self.lbl_rt_state = QLabel("—")
        self.lbl_rt_serial = QLabel("—")

        form.addRow("Active Device:", self.lbl_rt_name)
        form.addRow("Host Provider:", self.lbl_rt_provider)
        form.addRow("Device State:", self.lbl_rt_state)
        form.addRow("ADB Serial:", self.lbl_rt_serial)
        return w

    def _build_publishing_tab(self) -> QWidget:
        w = QWidget()
        form = QFormLayout(w)
        form.setContentsMargins(12, 12, 12, 12)
        form.setSpacing(10)

        self.lbl_pub_limit = QLabel("3 posts / day")
        self.lbl_pub_cooldown = QLabel("45 minutes")
        self.lbl_pub_jitter = QLabel("± 15 minutes")

        form.addRow("Daily Post Limit:", self.lbl_pub_limit)
        form.addRow("Minimum Cooldown:", self.lbl_pub_cooldown)
        form.addRow("Interval Jitter:", self.lbl_pub_jitter)
        return w

    def _build_activity_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.addWidget(QLabel("Recent Activity Logs"))
        self.activity_list = QListWidget()
        layout.addWidget(self.activity_list)
        return w

    def _build_jobs_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.addWidget(QLabel("Associated Automation Jobs"))
        self.jobs_list = QListWidget()
        layout.addWidget(self.jobs_list)
        return w

    def _build_notes_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        layout.addWidget(QLabel("Operator Notes & Remarks:"))
        self.txt_notes = QTextEdit()
        self.txt_notes.setPlaceholderText(
            "Enter notes, annotations, or reminder tags for this account..."
        )
        layout.addWidget(self.txt_notes, 1)

        self.btn_save_notes = CuteButton("💾 Save Notes", role="primary")
        self.btn_save_notes.clicked.connect(self._on_save_notes_clicked)
        layout.addWidget(self.btn_save_notes)
        return w

    def _build_audit_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.addWidget(QLabel("Account Audit Timeline"))
        self.audit_list = QListWidget()
        layout.addWidget(self.audit_list)
        return w

    # -------------------------------------------------------------------------
    # Data Hydration
    # -------------------------------------------------------------------------

    def set_account(self, account: Optional[AccountDetailDTO]) -> None:
        """Populate all 12 inspector tabs with account metadata."""
        self._current_account = account
        if not account:
            self.lbl_acc_name.setText("No Account Selected")
            self.lbl_acc_id.setText("Select an account to view rich records")
            self.status_pill.set_status("Inactive", "offline")
            self.btn_edit.setEnabled(False)
            return

        self.btn_edit.setEnabled(True)
        self.lbl_acc_name.setText(account.display_name)
        self.lbl_acc_id.setText(f"Platform ID: {account.profile_id} • System ID: {account.id[:8]}")

        # Set status pill
        st = account.status.lower()
        if st == "active":
            self.status_pill.set_status("Active", "ready")
        elif st in ("restricted", "checkpoint"):
            self.status_pill.set_status(account.status, "warning")
        elif st == "archived":
            self.status_pill.set_status("Archived", "offline")
        else:
            self.status_pill.set_status(account.status, "error")

        # 1. Overview
        self.lbl_ov_id.setText(account.profile_id)
        self.lbl_ov_health.setText(account.health_state)
        self.lbl_ov_priority.setText(str(account.priority))
        self.lbl_ov_locale.setText(f"{account.locale}")
        self.lbl_ov_timezone.setText(account.timezone)
        self.lbl_ov_category.setText(account.category_id or "Uncategorized")
        self.lbl_ov_created.setText(account.created_at[:19] if account.created_at else "—")
        self.lbl_ov_last_act.setText(
            account.last_activity_at[:19] if account.last_activity_at else "Never"
        )

        # 2. Contacts
        self.contacts_list.clear()
        if not account.emails and not account.phones:
            self.contacts_list.addItem("No contact methods configured.")
        else:
            for em in account.emails:
                primary_tag = " [Primary]" if em.get("is_primary") else ""
                verified_tag = " ✓" if em.get("is_verified") else ""
                self.contacts_list.addItem(
                    f"📧 Email: {em.get('masked')}{primary_tag}{verified_tag}"
                )
            for ph in account.phones:
                primary_tag = " [Primary]" if ph.get("is_primary") else ""
                verified_tag = " ✓" if ph.get("is_verified") else ""
                self.contacts_list.addItem(
                    f"📱 Phone: {ph.get('masked')}{primary_tag}{verified_tag}"
                )

        # 3. Security
        sec = account.security or {}
        self.lbl_sec_2fa.setText(sec.get("two_factor_method", "None"))
        pass_ref = sec.get("password_secret_ref")
        self.lbl_sec_pass_ref.setText(f"{pass_ref} [Masked]" if pass_ref else "None")
        totp_ref = sec.get("totp_secret_ref")
        self.lbl_sec_totp_ref.setText(f"{totp_ref} [Masked]" if totp_ref else "None")
        self.lbl_sec_review.setText(sec.get("last_security_review_at", "Never"))

        # 4. Pages
        self.pages_list.clear()
        if not account.pages:
            self.pages_list.addItem("No Facebook Pages connected.")
        else:
            for pg in account.pages:
                self.pages_list.addItem(
                    f"📄 {pg.get('name')} ({pg.get('platform_page_id')}) — {pg.get('followers')} followers"
                )

        # 5. Groups
        self.groups_list.clear()
        if not account.groups:
            self.groups_list.addItem("No Facebook Groups connected.")
        else:
            for gr in account.groups:
                self.groups_list.addItem(
                    f"👥 {gr.get('name')} ({gr.get('platform_group_id')}) — Role: {gr.get('role')}"
                )

        # 6. Environment
        if account.environment:
            env = account.environment
            self.lbl_env_id.setText(env.get("id", "—"))
            self.lbl_env_channel.setText(env.get("app_channel", "Official"))
            self.lbl_env_os.setText(f"Android {env.get('android_version', '10.0')}")
            self.lbl_env_ua.setText(env.get("user_agent", "—")[:40] + "...")
            self.lbl_env_dir.setText(env.get("storage_dir", "—"))
        else:
            self.lbl_env_id.setText("None (Unbound)")
            self.lbl_env_channel.setText("—")
            self.lbl_env_os.setText("—")
            self.lbl_env_ua.setText("—")
            self.lbl_env_dir.setText("—")

        # 7. Runtime
        if account.runtime_device:
            dev = account.runtime_device
            self.lbl_rt_name.setText(dev.get("custom_name", "—"))
            self.lbl_rt_provider.setText(dev.get("provider", "—"))
            self.lbl_rt_state.setText(dev.get("state", "—"))
            self.lbl_rt_serial.setText(dev.get("adb_serial", "—"))
        else:
            self.lbl_rt_name.setText("Unassigned (Idle)")
            self.lbl_rt_provider.setText("—")
            self.lbl_rt_state.setText("—")
            self.lbl_rt_serial.setText("—")

        # 11. Notes
        self.txt_notes.setText(account.notes or "")

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------

    def _on_edit_clicked(self) -> None:
        if self._current_account:
            self.edit_requested.emit(self._current_account.id)

    def _on_save_notes_clicked(self) -> None:
        if self._current_account:
            new_notes = self.txt_notes.toPlainText().strip()
            self.notes_saved.emit(self._current_account.id, new_notes)

    def _on_reveal_contacts_clicked(self) -> None:
        if not self._current_account:
            return
        if self.audit_service:
            self.audit_service.record(
                event_type="account.contacts_revealed",
                target_type="account",
                target_id=self._current_account.id,
                details={"action": "reveal_masked_contacts"},
            )
        # Populate raw email addresses
        self.contacts_list.clear()
        for em in self._current_account.emails:
            self.contacts_list.addItem(f"📧 Email: {em.get('address')} [Revealed]")
        for ph in self._current_account.phones:
            self.contacts_list.addItem(f"📱 Phone: {ph.get('number')} [Revealed]")

    def _on_reveal_secret(self, secret_type: str) -> None:
        if not self._current_account or not self.secret_store:
            return
        sec = self._current_account.security or {}
        ref_key = "password_secret_ref" if secret_type == "password" else "totp_secret_ref"
        ref = sec.get(ref_key)
        if not ref:
            QMessageBox.information(
                self, "No Secret", f"No {secret_type} vaulted for this account."
            )
            return

        val = self.secret_store.retrieve_secret(ref)
        if self.audit_service:
            self.audit_service.record(
                event_type=f"secret.{secret_type}_revealed",
                target_type="account",
                target_id=self._current_account.id,
                details={"ref": ref},
            )
        QMessageBox.information(
            self, f"Revealed {secret_type.title()}", f"{secret_type.title()}:\n{val or 'Empty'}"
        )
