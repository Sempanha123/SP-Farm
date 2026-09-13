"""Cute Accounts Workspace main view adhering to 01_UX_UI_SOURCE_OF_TRUTH.txt."""

from __future__ import annotations

import logging
from typing import Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from spfarm.application.commands.account_commands import (
    ArchiveAccountHandler,
    BulkUpdateAccountStatusCommand,
    BulkUpdateAccountStatusHandler,
    CreateAccountHandler,
    DeleteAccountHandler,
    RestoreAccountHandler,
    UpdateAccountCommand,
    UpdateAccountHandler,
)
from spfarm.application.events.account_events import (
    AccountArchivedEvent,
    AccountCreatedEvent,
    AccountDeletedEvent,
    AccountRestoredEvent,
    AccountStatusChangedEvent,
    AccountUpdatedEvent,
)
from spfarm.application.events.base import Event, EventBus
from spfarm.application.queries.accounts import (
    AccountFilterCriteria,
    AccountQueryService,
)
from spfarm.application.services.account_import import AccountImportService
from spfarm.application.services.audit import AuditService
from spfarm.domain.enums import AccountStatus
from spfarm.domain.interfaces.secret_store import ISecretStore
from spfarm.presentation.accounts.account_dialog import AccountDialog
from spfarm.presentation.accounts.import_dialog import AccountImportDialog
from spfarm.presentation.accounts.inspector import AccountInspectorPanel
from spfarm.presentation.accounts.table_model import AccountsTableModel
from spfarm.presentation.components.buttons import CuteButton
from spfarm.shared.theme import PALETTE

logger = logging.getLogger(__name__)


class AccountsView(QWidget):
    """Main Accounts Workspace managing scalable account fleets and rich inspector records."""

    navigate_requested = Signal(str)

    def __init__(
        self,
        query_service: AccountQueryService,
        create_handler: CreateAccountHandler,
        update_handler: UpdateAccountHandler,
        archive_handler: ArchiveAccountHandler,
        restore_handler: RestoreAccountHandler,
        delete_handler: DeleteAccountHandler,
        bulk_handler: BulkUpdateAccountStatusHandler,
        import_service: AccountImportService,
        event_bus: Optional[EventBus] = None,
        secret_store: Optional[ISecretStore] = None,
        audit_service: Optional[AuditService] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.query_service = query_service
        self.create_handler = create_handler
        self.update_handler = update_handler
        self.archive_handler = archive_handler
        self.restore_handler = restore_handler
        self.delete_handler = delete_handler
        self.bulk_handler = bulk_handler
        self.import_service = import_service
        self.event_bus = event_bus
        self.secret_store = secret_store
        self.audit_service = audit_service

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {PALETTE.background};
                color: {PALETTE.text};
            }}
            QTableView {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border};
                border-radius: 10px;
                gridline-color: {PALETTE.border};
                selection-background-color: {PALETTE.soft_primary};
                selection-color: {PALETTE.primary};
            }}
            QHeaderView::section {{
                background-color: {PALETTE.background};
                color: {PALETTE.text_secondary};
                font-size: 11px;
                font-weight: 600;
                border: none;
                border-bottom: 1px solid {PALETTE.border};
                padding: 6px 8px;
            }}
        """)

        self._setup_ui()

        # Connect EventBus
        if self.event_bus:
            self.event_bus.subscribe_all(self._on_event_received)

        # Initial load
        self.refresh_accounts()

    def _setup_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 16, 20, 20)
        root_layout.setSpacing(12)

        # Table model must exist before toolbar / bulk bar
        self.table_model = AccountsTableModel(self)
        self.table_model.dataChanged.connect(self._on_model_data_changed)
        self.table_model.modelReset.connect(self._on_model_data_changed)

        # 1. Top Filter & Action Bar
        root_layout.addLayout(self._build_toolbar())

        # 2. Bulk Action Bar (Hidden when 0 checked)
        self.bulk_bar = self._build_bulk_action_bar()
        root_layout.addWidget(self.bulk_bar)

        # 3. Main Splitter: Table View (Left) + Rich Inspector (Right)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background-color: transparent; width: 8px; }")

        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table_view.verticalHeader().setDefaultSectionSize(36)
        self.table_view.verticalHeader().hide()
        self.table_view.clicked.connect(self._on_row_clicked)
        splitter.addWidget(self.table_view)

        # Inspector Panel
        self.inspector = AccountInspectorPanel(
            secret_store=self.secret_store,
            audit_service=self.audit_service,
            parent=self,
        )
        self.inspector.edit_requested.connect(self._on_edit_account_requested)
        self.inspector.notes_saved.connect(self._on_save_notes)
        splitter.addWidget(self.inspector)

        # 60% table, 40% inspector default split
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        root_layout.addWidget(splitter, 1)

    def _build_toolbar(self) -> QHBoxLayout:
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        # Search box
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Search accounts by name, ID, email, tag...")
        self.txt_search.setClearButtonEnabled(True)
        self.txt_search.setFixedWidth(260)
        self.txt_search.textChanged.connect(self._on_filter_changed)
        toolbar.addWidget(self.txt_search)

        # Status filter
        self.cmb_status = QComboBox()
        self.cmb_status.addItem("All Statuses", None)
        for s in AccountStatus:
            self.cmb_status.addItem(s.value.title(), s.value)
        self.cmb_status.currentIndexChanged.connect(self._on_filter_changed)
        toolbar.addWidget(self.cmb_status)

        # Show archived checkbox
        self.chk_archived = QCheckBox("Show Archived")
        self.chk_archived.stateChanged.connect(self._on_filter_changed)
        toolbar.addWidget(self.chk_archived)

        toolbar.addStretch()

        # Action buttons
        self.btn_add = CuteButton("➕ Add Account", role="primary")
        self.btn_add.clicked.connect(self._on_add_account)
        toolbar.addWidget(self.btn_add)

        self.btn_import = CuteButton("📥 Import", role="secondary")
        self.btn_import.clicked.connect(self._on_import_accounts)
        toolbar.addWidget(self.btn_import)

        self.btn_refresh = QPushButton("🔄")
        self.btn_refresh.setFixedSize(34, 34)
        self.btn_refresh.setToolTip("Refresh Accounts")
        self.btn_refresh.setStyleSheet(f"""
            QPushButton {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border};
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {PALETTE.soft_primary};
            }}
        """)
        self.btn_refresh.clicked.connect(self.refresh_accounts)
        toolbar.addWidget(self.btn_refresh)

        return toolbar

    def _build_bulk_action_bar(self) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {PALETTE.soft_primary};
                border: 1px solid {PALETTE.primary};
                border-radius: 8px;
                padding: 4px 10px;
            }}
        """)
        b_layout = QHBoxLayout(frame)
        b_layout.setContentsMargins(10, 4, 10, 4)
        b_layout.setSpacing(10)

        self.lbl_selected_count = QLabel("0 accounts selected")
        self.lbl_selected_count.setStyleSheet(f"color: {PALETTE.primary}; font-weight: bold;")
        b_layout.addWidget(self.lbl_selected_count)

        b_layout.addStretch()

        self.btn_bulk_archive = CuteButton("Archive Selected", role="secondary")
        self.btn_bulk_archive.clicked.connect(self._on_bulk_archive)
        b_layout.addWidget(self.btn_bulk_archive)

        self.btn_bulk_active = CuteButton("Set Active", role="secondary")
        self.btn_bulk_active.clicked.connect(lambda: self._on_bulk_status(AccountStatus.ACTIVE))
        b_layout.addWidget(self.btn_bulk_active)

        self.btn_deselect = CuteButton("Deselect All", role="ghost")
        self.btn_deselect.clicked.connect(self.table_model.clear_selection)
        b_layout.addWidget(self.btn_deselect)

        frame.hide()
        return frame

    # -------------------------------------------------------------------------
    # Filtering & Data Loading
    # -------------------------------------------------------------------------

    def _on_filter_changed(self) -> None:
        self.refresh_accounts()

    def refresh_accounts(self) -> None:
        """Fetch and populate accounts matching active filters."""
        status_val = self.cmb_status.currentData()
        search_val = self.txt_search.text().strip()
        include_archived = self.chk_archived.isChecked()

        criteria = AccountFilterCriteria(
            search=search_val,
            status=status_val,
            include_archived=include_archived,
        )

        accounts = self.query_service.list_accounts(criteria)
        self.table_model.set_accounts(accounts)

        # Clear inspector if no accounts
        if not accounts:
            self.inspector.set_account(None)
        elif not self.inspector.isVisible():
            # Automatically inspect first row
            detail = self.query_service.get_account_detail(accounts[0].id)
            self.inspector.set_account(detail)

    def _on_row_clicked(self, index) -> None:
        acc = self.table_model.get_account_at(index.row())
        if acc:
            detail = self.query_service.get_account_detail(acc.id)
            self.inspector.set_account(detail)

    def _on_model_data_changed(self) -> None:
        selected = self.table_model.get_selected_ids()
        count = len(selected)
        if count > 0:
            self.lbl_selected_count.setText(f"{count} account{'s' if count > 1 else ''} selected")
            self.bulk_bar.show()
        else:
            self.bulk_bar.hide()

    def _on_event_received(self, event: Event) -> None:
        if isinstance(
            event,
            (
                AccountCreatedEvent,
                AccountUpdatedEvent,
                AccountArchivedEvent,
                AccountRestoredEvent,
                AccountDeletedEvent,
                AccountStatusChangedEvent,
            ),
        ):
            QTimer.singleShot(50, self.refresh_accounts)

    # -------------------------------------------------------------------------
    # CRUD Dialog Handlers
    # -------------------------------------------------------------------------

    def _on_add_account(self) -> None:
        dlg = AccountDialog(parent=self)
        if dlg.exec():
            cmd = dlg.get_create_command()
            res = self.create_handler.handle(cmd)
            if res.is_success:
                self.refresh_accounts()
                # Select new account in inspector
                detail = self.query_service.get_account_detail(res.value)
                self.inspector.set_account(detail)
            else:
                QMessageBox.critical(self, "Failed to Create Account", res.error.message)

    def _on_edit_account_requested(self, account_id: str) -> None:
        detail = self.query_service.get_account_detail(account_id)
        if not detail:
            return
        dlg = AccountDialog(account=detail, parent=self)
        if dlg.exec():
            cmd = dlg.get_update_command()
            res = self.update_handler.handle(cmd)
            if res.is_success:
                self.refresh_accounts()
                updated_detail = self.query_service.get_account_detail(account_id)
                self.inspector.set_account(updated_detail)
            else:
                QMessageBox.critical(self, "Failed to Update Account", res.error.message)

    def _on_save_notes(self, account_id: str, notes: str) -> None:
        res = self.update_handler.handle(UpdateAccountCommand(account_id=account_id, notes=notes))
        if res.is_success:
            self.refresh_accounts()
        else:
            QMessageBox.warning(self, "Notes Save Error", res.error.message)

    def _on_import_accounts(self) -> None:
        dlg = AccountImportDialog(import_service=self.import_service, parent=self)
        if dlg.exec():
            self.refresh_accounts()

    def _on_bulk_archive(self) -> None:
        selected = self.table_model.get_selected_ids()
        if not selected:
            return
        res = self.bulk_handler.handle(
            BulkUpdateAccountStatusCommand(
                account_ids=selected,
                new_status=AccountStatus.ARCHIVED,
            )
        )
        if res.is_success:
            self.table_model.clear_selection()
            self.refresh_accounts()

    def _on_bulk_status(self, new_status: AccountStatus) -> None:
        selected = self.table_model.get_selected_ids()
        if not selected:
            return
        res = self.bulk_handler.handle(
            BulkUpdateAccountStatusCommand(
                account_ids=selected,
                new_status=new_status,
            )
        )
        if res.is_success:
            self.table_model.clear_selection()
            self.refresh_accounts()
