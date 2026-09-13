"""Dialog for adding or editing a Facebook Group."""

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
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from spfarm.application.commands.page_group_commands import AddGroupCommand, UpdateGroupCommand
from spfarm.application.queries.accounts import AccountSummaryDTO
from spfarm.application.queries.pages_groups import GroupSummaryDTO
from spfarm.presentation.components.buttons import CuteButton
from spfarm.shared.theme import PALETTE


class GroupDialog(QDialog):
    """Dialog for associating or updating Facebook Groups."""

    def __init__(
        self,
        accounts: list[AccountSummaryDTO],
        group: Optional[GroupSummaryDTO] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.accounts = accounts
        self.group = group
        self.is_edit = group is not None

        title = "Edit Facebook Group" if self.is_edit else "➕ Associate Facebook Group"
        self.setWindowTitle(title)
        self.setMinimumWidth(440)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {PALETTE.surface};
                color: {PALETTE.text};
            }}
            QLineEdit, QTextEdit, QComboBox, QSpinBox {{
                background-color: {PALETTE.background};
                border: 1px solid {PALETTE.border};
                border-radius: 6px;
                padding: 6px 10px;
                color: {PALETTE.text};
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {{
                border: 1.5px solid {PALETTE.primary};
            }}
        """)

        self._setup_ui()
        if self.group:
            self._populate_data(self.group)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        header_lbl = QLabel(
            "Configure Facebook Group" if self.is_edit else "Associate Facebook Group Record"
        )
        header_lbl.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {PALETTE.primary};")
        layout.addWidget(header_lbl)

        form = QFormLayout()
        form.setSpacing(10)

        # Managing account
        self.cmb_account = QComboBox()
        for a in self.accounts:
            self.cmb_account.addItem(f"{a.display_name} ({a.profile_id})", a.id)
        if self.is_edit:
            self.cmb_account.setEnabled(False)
        form.addRow("Managing Account*:", self.cmb_account)

        self.txt_group_id = QLineEdit()
        self.txt_group_id.setPlaceholderText("e.g. 555888999111")
        if self.is_edit:
            self.txt_group_id.setEnabled(False)
        form.addRow("Platform Group ID*:", self.txt_group_id)

        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("e.g. VIP Community Hub")
        form.addRow("Group Name*:", self.txt_name)

        self.cmb_role = QComboBox()
        self.cmb_role.addItems(["ADMIN", "MODERATOR", "MEMBER"])
        form.addRow("Account Role:", self.cmb_role)

        self.spin_members = QSpinBox()
        self.spin_members.setRange(0, 100_000_000)
        self.spin_members.setValue(0)
        form.addRow("Total Members:", self.spin_members)

        self.cmb_permission = QComboBox()
        self.cmb_permission.addItems(["ALLOWED", "PENDING_APPROVAL", "MUTED"])
        form.addRow("Posting Permission:", self.cmb_permission)

        self.txt_notes = QTextEdit()
        self.txt_notes.setFixedHeight(60)
        self.txt_notes.setPlaceholderText("Optional notes or moderation guidelines...")
        form.addRow("Notes:", self.txt_notes)

        layout.addLayout(form)

        # Buttons
        btn_box = QHBoxLayout()
        btn_box.addStretch()

        self.btn_cancel = CuteButton("Cancel", role="secondary")
        self.btn_cancel.clicked.connect(self.reject)
        btn_box.addWidget(self.btn_cancel)

        self.btn_save = CuteButton("Save Group", role="primary")
        self.btn_save.clicked.connect(self._on_save)
        btn_box.addWidget(self.btn_save)

        layout.addLayout(btn_box)

    def _populate_data(self, g: GroupSummaryDTO) -> None:
        self.txt_name.setText(g.name)
        self.txt_group_id.setText(g.platform_group_id)
        self.spin_members.setValue(g.members)
        self.txt_notes.setText(g.notes or "")

        idx_role = self.cmb_role.findText(g.role)
        if idx_role >= 0:
            self.cmb_role.setCurrentIndex(idx_role)

        idx_perm = self.cmb_permission.findText(g.posting_permission)
        if idx_perm >= 0:
            self.cmb_permission.setCurrentIndex(idx_perm)

        idx_acc = self.cmb_account.findData(g.account_id)
        if idx_acc >= 0:
            self.cmb_account.setCurrentIndex(idx_acc)

    def _on_save(self) -> None:
        if not self.is_edit and self.cmb_account.currentIndex() < 0:
            QMessageBox.warning(self, "Validation Error", "Please select a managing account.")
            return
        if not self.txt_group_id.text().strip():
            QMessageBox.warning(self, "Validation Error", "Platform Group ID is required.")
            return
        if not self.txt_name.text().strip():
            QMessageBox.warning(self, "Validation Error", "Group Name is required.")
            return
        self.accept()

    def get_add_command(self) -> AddGroupCommand:
        return AddGroupCommand(
            account_id=self.cmb_account.currentData(),
            platform_group_id=self.txt_group_id.text().strip(),
            name=self.txt_name.text().strip(),
            role=self.cmb_role.currentText(),
            members=self.spin_members.value(),
            posting_permission=self.cmb_permission.currentText(),
            notes=self.txt_notes.toPlainText().strip() or None,
        )

    def get_update_command(self) -> UpdateGroupCommand:
        if not self.group:
            raise ValueError("No group for update")
        return UpdateGroupCommand(
            group_id=self.group.id,
            name=self.txt_name.text().strip(),
            role=self.cmb_role.currentText(),
            members=self.spin_members.value(),
            posting_permission=self.cmb_permission.currentText(),
            notes=self.txt_notes.toPlainText().strip() or None,
        )
