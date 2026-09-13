"""Dialog for adding or editing a Facebook Page."""

from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import (
    QCheckBox,
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

from spfarm.application.commands.page_group_commands import AddPageCommand, UpdatePageCommand
from spfarm.application.queries.accounts import AccountSummaryDTO
from spfarm.application.queries.pages_groups import PageSummaryDTO
from spfarm.presentation.components.buttons import CuteButton
from spfarm.shared.theme import PALETTE


class PageDialog(QDialog):
    """Dialog for attaching or updating Facebook Pages."""

    def __init__(
        self,
        accounts: list[AccountSummaryDTO],
        page: Optional[PageSummaryDTO] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.accounts = accounts
        self.page = page
        self.is_edit = page is not None

        title = "Edit Facebook Page" if self.is_edit else "➕ Attach Facebook Page"
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
        if self.page:
            self._populate_data(self.page)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        header_lbl = QLabel(
            "Configure Facebook Page" if self.is_edit else "Attach Managed Facebook Page"
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

        self.txt_page_id = QLineEdit()
        self.txt_page_id.setPlaceholderText("e.g. 10987654321")
        if self.is_edit:
            self.txt_page_id.setEnabled(False)
        form.addRow("Platform Page ID*:", self.txt_page_id)

        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("e.g. Official Brand Page")
        form.addRow("Page Name*:", self.txt_name)

        self.txt_category = QLineEdit()
        self.txt_category.setText("General")
        form.addRow("Category:", self.txt_category)

        self.spin_followers = QSpinBox()
        self.spin_followers.setRange(0, 100_000_000)
        self.spin_followers.setValue(0)
        form.addRow("Followers:", self.spin_followers)

        self.txt_profile_url = QLineEdit()
        self.txt_profile_url.setPlaceholderText("https://facebook.com/yourpage")
        form.addRow("Profile URL:", self.txt_profile_url)

        self.chk_publishing = QCheckBox("Enable Automated Publishing")
        self.chk_publishing.setChecked(True)
        form.addRow("", self.chk_publishing)

        self.txt_notes = QTextEdit()
        self.txt_notes.setFixedHeight(60)
        self.txt_notes.setPlaceholderText("Optional notes or content guidelines...")
        form.addRow("Notes:", self.txt_notes)

        layout.addLayout(form)

        # Buttons
        btn_box = QHBoxLayout()
        btn_box.addStretch()

        self.btn_cancel = CuteButton("Cancel", role="secondary")
        self.btn_cancel.clicked.connect(self.reject)
        btn_box.addWidget(self.btn_cancel)

        self.btn_save = CuteButton("Save Page", role="primary")
        self.btn_save.clicked.connect(self._on_save)
        btn_box.addWidget(self.btn_save)

        layout.addLayout(btn_box)

    def _populate_data(self, p: PageSummaryDTO) -> None:
        self.txt_name.setText(p.name)
        self.txt_page_id.setText(p.platform_page_id)
        self.txt_category.setText(p.category)
        self.spin_followers.setValue(p.followers)
        self.chk_publishing.setChecked(p.publishing_enabled)
        self.txt_notes.setText(p.notes or "")

        idx = self.cmb_account.findData(p.account_id)
        if idx >= 0:
            self.cmb_account.setCurrentIndex(idx)

    def _on_save(self) -> None:
        if not self.is_edit and self.cmb_account.currentIndex() < 0:
            QMessageBox.warning(self, "Validation Error", "Please select a managing account.")
            return
        if not self.txt_page_id.text().strip():
            QMessageBox.warning(self, "Validation Error", "Platform Page ID is required.")
            return
        if not self.txt_name.text().strip():
            QMessageBox.warning(self, "Validation Error", "Page Name is required.")
            return
        self.accept()

    def get_add_command(self) -> AddPageCommand:
        return AddPageCommand(
            account_id=self.cmb_account.currentData(),
            platform_page_id=self.txt_page_id.text().strip(),
            name=self.txt_name.text().strip(),
            category=self.txt_category.text().strip() or "General",
            followers=self.spin_followers.value(),
            profile_url=self.txt_profile_url.text().strip() or None,
            publishing_enabled=self.chk_publishing.isChecked(),
            notes=self.txt_notes.toPlainText().strip() or None,
        )

    def get_update_command(self) -> UpdatePageCommand:
        if not self.page:
            raise ValueError("No page for update")
        return UpdatePageCommand(
            page_id=self.page.id,
            name=self.txt_name.text().strip(),
            category=self.txt_category.text().strip() or "General",
            followers=self.spin_followers.value(),
            publishing_enabled=self.chk_publishing.isChecked(),
            notes=self.txt_notes.toPlainText().strip() or None,
        )
