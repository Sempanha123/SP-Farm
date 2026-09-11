"""CSV and JSON account import preview and execution dialog."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from spfarm.application.services.account_import import (
    AccountImportService,
    ImportPreviewDTO,
    ImportResultDTO,
)
from spfarm.presentation.components.buttons import CuteButton
from spfarm.shared.theme import PALETTE


class AccountImportDialog(QDialog):
    """Dialog providing preview, validation, and duplicate handling before batch import."""

    def __init__(
        self,
        import_service: AccountImportService,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.import_service = import_service
        self._current_preview: Optional[ImportPreviewDTO] = None
        self.import_result: Optional[ImportResultDTO] = None

        self.setWindowTitle("📥 Batch Import Accounts (CSV / JSON)")
        self.resize(780, 520)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {PALETTE.surface};
                color: {PALETTE.text};
            }}
            QTableWidget {{
                background-color: {PALETTE.background};
                border: 1px solid {PALETTE.border};
                border-radius: 8px;
            }}
        """)

        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        # 1. Top File Selection Row
        file_box = QHBoxLayout()
        self.btn_select_file = CuteButton("📂 Select CSV or JSON File...", role="primary")
        self.btn_select_file.clicked.connect(self._on_select_file)
        file_box.addWidget(self.btn_select_file)

        self.lbl_file_path = QLabel("No file selected")
        self.lbl_file_path.setStyleSheet(f"color: {PALETTE.text_secondary}; font-style: italic;")
        file_box.addWidget(self.lbl_file_path, 1)

        layout.addLayout(file_box)

        # 2. Stats summary bar
        self.summary_bar = QFrame()
        self.summary_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {PALETTE.background};
                border: 1px solid {PALETTE.border};
                border-radius: 8px;
                padding: 6px 12px;
            }}
        """)
        sb_layout = QHBoxLayout(self.summary_bar)
        self.lbl_stat_total = QLabel("Total: 0")
        self.lbl_stat_valid = QLabel("Valid: 0")
        self.lbl_stat_valid.setStyleSheet(f"color: {PALETTE.success}; font-weight: bold;")
        self.lbl_stat_dup = QLabel("Duplicates: 0")
        self.lbl_stat_dup.setStyleSheet(f"color: {PALETTE.warning}; font-weight: bold;")
        self.lbl_stat_err = QLabel("Errors: 0")
        self.lbl_stat_err.setStyleSheet(f"color: {PALETTE.danger}; font-weight: bold;")

        sb_layout.addWidget(self.lbl_stat_total)
        sb_layout.addWidget(self.lbl_stat_valid)
        sb_layout.addWidget(self.lbl_stat_dup)
        sb_layout.addWidget(self.lbl_stat_err)
        sb_layout.addStretch()
        layout.addWidget(self.summary_bar)

        # 3. Preview Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["#", "Name", "Profile ID", "Contact", "Status", "Notes / Deduplication"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table, 1)

        # 4. Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # 5. Bottom control bar
        bottom_box = QHBoxLayout()
        self.chk_skip_dups = QCheckBox("Skip duplicate accounts (Recommended)")
        self.chk_skip_dups.setChecked(True)
        bottom_box.addWidget(self.chk_skip_dups)

        bottom_box.addStretch()

        self.btn_cancel = CuteButton("Close", role="secondary")
        self.btn_cancel.clicked.connect(self.reject)
        bottom_box.addWidget(self.btn_cancel)

        self.btn_import = CuteButton("Import Accounts", role="cute")
        self.btn_import.setEnabled(False)
        self.btn_import.clicked.connect(self._on_execute_import)
        bottom_box.addWidget(self.btn_import)

        layout.addLayout(bottom_box)

    def _on_select_file(self) -> None:
        path_str, _ = QFileDialog.getOpenFileName(
            self,
            "Select Account Metadata File",
            "",
            "Supported Files (*.csv *.json);;CSV Files (*.csv);;JSON Files (*.json)",
        )
        if not path_str:
            return

        path = Path(path_str)
        self.lbl_file_path.setText(str(path))

        if path.suffix.lower() == ".csv":
            self._current_preview = self.import_service.preview_csv_file(path)
        else:
            self._current_preview = self.import_service.preview_json_file(path)

        self._render_preview(self._current_preview)

    def _render_preview(self, preview: ImportPreviewDTO) -> None:
        self.lbl_stat_total.setText(f"Total: {preview.total_rows}")
        self.lbl_stat_valid.setText(f"Valid: {preview.valid_count}")
        self.lbl_stat_dup.setText(f"Duplicates: {preview.duplicate_count}")
        self.lbl_stat_err.setText(f"Errors: {preview.error_count}")

        self.table.setRowCount(len(preview.rows))
        for row_idx, r in enumerate(preview.rows):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(r.row_index)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(r.display_name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(r.profile_id))
            self.table.setItem(row_idx, 3, QTableWidgetItem(r.email or r.phone or "—"))

            # Status column
            if not r.is_valid:
                status_item = QTableWidgetItem("❌ Error")
                status_item.setForeground(Qt.GlobalColor.red)
                detail_item = QTableWidgetItem(r.validation_error or "Invalid format")
            elif r.is_duplicate:
                status_item = QTableWidgetItem("⚠️ Duplicate")
                status_item.setForeground(Qt.GlobalColor.darkYellow)
                detail_item = QTableWidgetItem(r.duplicate_reason or "Duplicate record")
            else:
                status_item = QTableWidgetItem("✓ Valid")
                status_item.setForeground(Qt.GlobalColor.darkGreen)
                detail_item = QTableWidgetItem("Ready to import")

            self.table.setItem(row_idx, 4, status_item)
            self.table.setItem(row_idx, 5, detail_item)

        # Enable import if we have valid rows or duplicates that can be imported
        can_import = preview.valid_count > 0 or (not self.chk_skip_dups.isChecked() and preview.duplicate_count > 0)
        self.btn_import.setEnabled(can_import)

    def _on_execute_import(self) -> None:
        if not self._current_preview:
            return

        self.btn_import.setEnabled(False)
        self.progress_bar.show()
        self.progress_bar.setRange(0, 0)  # indeterminate pulse

        skip_dups = self.chk_skip_dups.isChecked()
        self.import_result = self.import_service.execute_import(
            self._current_preview.rows,
            skip_duplicates=skip_dups,
        )

        self.progress_bar.hide()
        QMessageBox.information(
            self,
            "Import Complete",
            f"Successfully imported {self.import_result.imported_count} accounts.\n"
            f"Skipped {self.import_result.skipped_count} accounts.",
        )
        self.accept()
