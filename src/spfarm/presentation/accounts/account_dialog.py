"""Account creation and editing dialog."""

from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from spfarm.application.commands.account_commands import CreateAccountCommand, UpdateAccountCommand
from spfarm.application.queries.accounts import AccountDetailDTO
from spfarm.domain.enums import TwoFactorMethod
from spfarm.presentation.components.buttons import CuteButton
from spfarm.shared.theme import PALETTE


class AccountDialog(QDialog):
    """Cute dialog for onboarding or editing an account."""

    def __init__(
        self,
        account: Optional[AccountDetailDTO] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.account = account
        self.is_edit = account is not None

        title = "Edit Account" if self.is_edit else "➕ Onboard New Account"
        self.setWindowTitle(title)
        self.setMinimumWidth(480)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {PALETTE.surface};
                color: {PALETTE.text};
            }}
            QLineEdit, QTextEdit, QComboBox {{
                background-color: {PALETTE.background};
                border: 1px solid {PALETTE.border};
                border-radius: 6px;
                padding: 6px 10px;
                color: {PALETTE.text};
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border: 1.5px solid {PALETTE.primary};
            }}
        """)

        self._setup_ui()
        if self.account:
            self._populate_data(self.account)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Header title
        header_lbl = QLabel("Account Configuration" if self.is_edit else "Create Authorized Account Record")
        header_lbl.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {PALETTE.primary};")
        layout.addWidget(header_lbl)

        form = QFormLayout()
        form.setSpacing(10)

        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("e.g. Marketing Lead Alpha")
        form.addRow("Display Name*:", self.txt_name)

        self.txt_profile_id = QLineEdit()
        self.txt_profile_id.setPlaceholderText("e.g. 100087654321098")
        if self.is_edit:
            self.txt_profile_id.setEnabled(False)
        form.addRow("Facebook Profile ID*:", self.txt_profile_id)

        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("e.g. operator@example.com")
        form.addRow("Primary Email:", self.txt_email)

        self.txt_phone = QLineEdit()
        self.txt_phone.setPlaceholderText("e.g. +1 555-123-4567")
        form.addRow("Primary Phone:", self.txt_phone)

        self.cmb_2fa = QComboBox()
        for method in TwoFactorMethod:
            self.cmb_2fa.addItem(method.value, method)
        form.addRow("2FA Method:", self.cmb_2fa)

        if not self.is_edit:
            self.txt_password = QLineEdit()
            self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.txt_password.setPlaceholderText("Stored directly in encrypted vault")
            form.addRow("Password (Vaulted):", self.txt_password)

            self.txt_totp = QLineEdit()
            self.txt_totp.setPlaceholderText("e.g. JBSWY3DPEHPK3PXP")
            form.addRow("TOTP Secret Seed:", self.txt_totp)

        self.txt_category = QLineEdit()
        self.txt_category.setPlaceholderText("e.g. Marketing, Support, Personal")
        form.addRow("Category / Tag:", self.txt_category)

        self.txt_notes = QTextEdit()
        self.txt_notes.setFixedHeight(60)
        self.txt_notes.setPlaceholderText("Optional notes or instructions...")
        form.addRow("Notes:", self.txt_notes)

        layout.addLayout(form)

        # Buttons
        btn_box = QHBoxLayout()
        btn_box.addStretch()

        self.btn_cancel = CuteButton("Cancel", role="secondary")
        self.btn_cancel.clicked.connect(self.reject)
        btn_box.addWidget(self.btn_cancel)

        self.btn_save = CuteButton("Save Account", role="primary")
        self.btn_save.clicked.connect(self._on_save)
        btn_box.addWidget(self.btn_save)

        layout.addLayout(btn_box)

    def _populate_data(self, acc: AccountDetailDTO) -> None:
        self.txt_name.setText(acc.display_name)
        self.txt_profile_id.setText(acc.profile_id)
        if acc.emails:
            self.txt_email.setText(acc.emails[0].get("address", ""))
        if acc.phones:
            self.txt_phone.setText(acc.phones[0].get("number", ""))
        self.txt_category.setText(acc.category_id or "")
        self.txt_notes.setText(acc.notes or "")

        sec_2fa = (acc.security or {}).get("two_factor_method", "NONE")
        idx = self.cmb_2fa.findText(sec_2fa)
        if idx >= 0:
            self.cmb_2fa.setCurrentIndex(idx)

    def _on_save(self) -> None:
        name = self.txt_name.text().strip()
        pid = self.txt_profile_id.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Display Name is required.")
            return
        if not pid:
            QMessageBox.warning(self, "Validation Error", "Platform Profile ID is required.")
            return

        self.accept()

    def get_create_command(self) -> CreateAccountCommand:
        return CreateAccountCommand(
            display_name=self.txt_name.text().strip(),
            profile_id=self.txt_profile_id.text().strip(),
            primary_email=self.txt_email.text().strip() or None,
            primary_phone=self.txt_phone.text().strip() or None,
            password_plain=self.txt_password.text().strip() or None,
            totp_seed_plain=self.txt_totp.text().strip() or None,
            two_factor_method=self.cmb_2fa.currentData(),
            category_id=self.txt_category.text().strip() or None,
            notes=self.txt_notes.toPlainText().strip() or None,
        )

    def get_update_command(self) -> UpdateAccountCommand:
        if not self.account:
            raise ValueError("Cannot get update command on new account")
        return UpdateAccountCommand(
            account_id=self.account.id,
            display_name=self.txt_name.text().strip(),
            category_id=self.txt_category.text().strip() or None,
            notes=self.txt_notes.toPlainText().strip() or None,
            two_factor_method=self.cmb_2fa.currentData(),
        )
