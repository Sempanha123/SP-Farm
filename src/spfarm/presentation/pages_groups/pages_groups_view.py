"""Cute Pages and Groups Workspace view with Table and Card grid modes."""

from __future__ import annotations

import logging
from typing import Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSplitter,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from spfarm.application.commands.page_group_commands import (
    AddGroupHandler,
    AddPageHandler,
    DeleteGroupCommand,
    DeleteGroupHandler,
    DeletePageCommand,
    DeletePageHandler,
    UpdateGroupCommand,
    UpdateGroupHandler,
    UpdatePageCommand,
    UpdatePageHandler,
)
from spfarm.application.events.base import Event, EventBus
from spfarm.application.events.page_group_events import (
    GroupAddedEvent,
    GroupDeletedEvent,
    GroupUpdatedEvent,
    PageAddedEvent,
    PageDeletedEvent,
    PageUpdatedEvent,
)
from spfarm.application.queries.accounts import AccountQueryService
from spfarm.application.queries.pages_groups import (
    GroupSummaryDTO,
    PagesAndGroupsQueryService,
    PageSummaryDTO,
)
from spfarm.presentation.components.buttons import CuteButton
from spfarm.presentation.components.inspector import CuteInspector
from spfarm.presentation.pages_groups.cards import CuteGroupCard, CutePageCard
from spfarm.presentation.pages_groups.group_dialog import GroupDialog
from spfarm.presentation.pages_groups.page_dialog import PageDialog
from spfarm.shared.theme import PALETTE

logger = logging.getLogger(__name__)


class PagesAndGroupsView(QWidget):
    """Workspace for Facebook Pages and Groups with dual table/card views."""

    navigate_requested = Signal(str)

    def __init__(
        self,
        query_service: PagesAndGroupsQueryService,
        account_queries: AccountQueryService,
        add_page_handler: AddPageHandler,
        update_page_handler: UpdatePageHandler,
        delete_page_handler: DeletePageHandler,
        add_group_handler: AddGroupHandler,
        update_group_handler: UpdateGroupHandler,
        delete_group_handler: DeleteGroupHandler,
        event_bus: Optional[EventBus] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.query_service = query_service
        self.account_queries = account_queries
        self.add_page_handler = add_page_handler
        self.update_page_handler = update_page_handler
        self.delete_page_handler = delete_page_handler
        self.add_group_handler = add_group_handler
        self.update_group_handler = update_group_handler
        self.delete_group_handler = delete_group_handler
        self.event_bus = event_bus

        self.current_section = "pages"  # "pages" or "groups"
        self.view_mode = "table"  # "table" or "cards"
        self._selected_item_id: Optional[str] = None

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {PALETTE.background};
                color: {PALETTE.text};
            }}
            QTableWidget {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border};
                border-radius: 10px;
                gridline-color: {PALETTE.border};
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

        if self.event_bus:
            self.event_bus.subscribe_all(self._on_event_received)

        self.refresh_data()

    def _setup_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 16, 20, 20)
        root_layout.setSpacing(12)

        # 1. Top Section Toolbar
        root_layout.addLayout(self._build_top_toolbar())

        # 2. Splitter: Center content + Right Inspector
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background-color: transparent; width: 8px; }")

        # Center stack (Table vs Cards)
        self.center_stack = QStackedWidget()
        self.table_view = self._build_table_widget()
        self.cards_scroll = self._build_cards_scroll()
        self.center_stack.addWidget(self.table_view)
        self.center_stack.addWidget(self.cards_scroll)
        splitter.addWidget(self.center_stack)

        # Inspector Panel
        self.inspector = self._build_inspector()
        splitter.addWidget(self.inspector)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        root_layout.addWidget(splitter, 1)

    def _build_top_toolbar(self) -> QHBoxLayout:
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        # Section Selector (Pages / Groups)
        self.btn_tab_pages = CuteButton("📄 Pages", role="primary")
        self.btn_tab_pages.clicked.connect(lambda: self._set_section("pages"))
        toolbar.addWidget(self.btn_tab_pages)

        self.btn_tab_groups = CuteButton("👥 Groups", role="secondary")
        self.btn_tab_groups.clicked.connect(lambda: self._set_section("groups"))
        toolbar.addWidget(self.btn_tab_groups)

        # View Mode Toggle (Table / Cards)
        self.btn_view_mode = CuteButton("🎴 Cards View", role="ghost")
        self.btn_view_mode.clicked.connect(self._toggle_view_mode)
        toolbar.addWidget(self.btn_view_mode)

        toolbar.addSpacing(16)

        # Search box
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Search by name, ID, category...")
        self.txt_search.setClearButtonEnabled(True)
        self.txt_search.setFixedWidth(240)
        self.txt_search.textChanged.connect(self.refresh_data)
        toolbar.addWidget(self.txt_search)

        # Account filter
        self.cmb_account = QComboBox()
        self.cmb_account.addItem("All Accounts", None)
        self.cmb_account.currentIndexChanged.connect(self.refresh_data)
        toolbar.addWidget(self.cmb_account)

        toolbar.addStretch()

        # Action Buttons
        self.btn_add = CuteButton("➕ Add Page", role="cute")
        self.btn_add.clicked.connect(self._on_add_item)
        toolbar.addWidget(self.btn_add)

        self.btn_refresh = QPushButton("🔄")
        self.btn_refresh.setFixedSize(34, 34)
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
        self.btn_refresh.clicked.connect(self.refresh_data)
        toolbar.addWidget(self.btn_refresh)

        return toolbar

    def _build_table_widget(self) -> QTableWidget:
        table = QTableWidget()
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setDefaultSectionSize(36)
        table.verticalHeader().hide()
        table.cellClicked.connect(self._on_table_cell_clicked)
        return table

    def _build_cards_scroll(self) -> QScrollArea:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")

        self.cards_container = QWidget()
        self.cards_grid = QGridLayout(self.cards_container)
        self.cards_grid.setContentsMargins(0, 0, 0, 0)
        self.cards_grid.setSpacing(12)
        scroll.setWidget(self.cards_container)
        return scroll

    def _build_inspector(self) -> CuteInspector:
        inspector = CuteInspector(parent=self)
        inspector.lbl_title.setText("Entity Details")
        inspector.setFixedWidth(340)

        body = QWidget()
        layout = QVBoxLayout(body)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Header card
        self.insp_title = QLabel("No Selection")
        self.insp_title.setStyleSheet(
            f"font-size: 13px; font-weight: bold; color: {PALETTE.primary};"
        )
        self.insp_subtitle = QLabel("Select an item to view records")
        self.insp_subtitle.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 11px;")
        layout.addWidget(self.insp_title)
        layout.addWidget(self.insp_subtitle)

        # Details list frame
        self.insp_details = QLabel("")
        self.insp_details.setStyleSheet("font-size: 11px; line-height: 1.5;")
        self.insp_details.setWordWrap(True)
        layout.addWidget(self.insp_details)

        # Notes editor
        layout.addWidget(QLabel("Notes & Remarks:"))
        self.insp_notes = QTextEdit()
        self.insp_notes.setFixedHeight(60)
        layout.addWidget(self.insp_notes)

        self.btn_save_notes = CuteButton("Save Notes", role="secondary")
        self.btn_save_notes.clicked.connect(self._on_save_notes)
        layout.addWidget(self.btn_save_notes)

        layout.addStretch()

        # Action bar
        btn_box = QHBoxLayout()
        self.btn_insp_edit = CuteButton("✏️ Edit", role="primary")
        self.btn_insp_edit.clicked.connect(self._on_edit_item)
        btn_box.addWidget(self.btn_insp_edit)

        self.btn_insp_del = CuteButton("🗑️ Delete", role="danger")
        self.btn_insp_del.clicked.connect(self._on_delete_item)
        btn_box.addWidget(self.btn_insp_del)
        layout.addLayout(btn_box)

        inspector.content_layout.addWidget(body)
        return inspector

    # -------------------------------------------------------------------------
    # Mode & Section Toggles
    # -------------------------------------------------------------------------

    def _set_section(self, section: str) -> None:
        self.current_section = section
        if section == "pages":
            self.btn_tab_pages.setProperty("role", "primary")
            self.btn_tab_groups.setProperty("role", "secondary")
            self.btn_add.setText("➕ Add Page")
        else:
            self.btn_tab_pages.setProperty("role", "secondary")
            self.btn_tab_groups.setProperty("role", "primary")
            self.btn_add.setText("➕ Add Group")

        # Force style re-polish
        self.btn_tab_pages.style().polish(self.btn_tab_pages)
        self.btn_tab_groups.style().polish(self.btn_tab_groups)

        self._selected_item_id = None
        self.refresh_data()

    def _toggle_view_mode(self) -> None:
        if self.view_mode == "table":
            self.view_mode = "cards"
            self.btn_view_mode.setText("📋 Table View")
            self.center_stack.setCurrentIndex(1)
        else:
            self.view_mode = "table"
            self.btn_view_mode.setText("🎴 Cards View")
            self.center_stack.setCurrentIndex(0)
        self.refresh_data()

    # -------------------------------------------------------------------------
    # Data Refresh
    # -------------------------------------------------------------------------

    def refresh_data(self) -> None:
        """Fetch fresh records and render according to active section and view mode."""
        # 1. Update Accounts filter dropdown if needed
        accounts = self.account_queries.list_accounts()
        cur_acc = self.cmb_account.currentData()
        self.cmb_account.blockSignals(True)
        self.cmb_account.clear()
        self.cmb_account.addItem("All Managing Accounts", None)
        for a in accounts:
            self.cmb_account.addItem(a.display_name, a.id)
        idx = self.cmb_account.findData(cur_acc)
        if idx >= 0:
            self.cmb_account.setCurrentIndex(idx)
        self.cmb_account.blockSignals(False)

        search_kw = self.txt_search.text().strip()
        selected_acc_id = self.cmb_account.currentData()

        if self.current_section == "pages":
            pages = self.query_service.list_pages(account_id=selected_acc_id, search=search_kw)
            if self.view_mode == "table":
                self._render_pages_table(pages)
            else:
                self._render_pages_cards(pages)
        else:
            groups = self.query_service.list_groups(account_id=selected_acc_id, search=search_kw)
            if self.view_mode == "table":
                self._render_groups_table(groups)
            else:
                self._render_groups_cards(groups)

    def _render_pages_table(self, pages: list[PageSummaryDTO]) -> None:
        self.table_view.clear()
        self.table_view.setColumnCount(6)
        self.table_view.setHorizontalHeaderLabels(
            [
                "Platform ID",
                "Page Name",
                "Managing Account",
                "Category",
                "Followers",
                "Publishing",
            ]
        )
        self.table_view.setRowCount(len(pages))
        for row, p in enumerate(pages):
            self.table_view.setItem(row, 0, QTableWidgetItem(p.platform_page_id))
            self.table_view.setItem(row, 1, QTableWidgetItem(p.name))
            self.table_view.setItem(row, 2, QTableWidgetItem(p.account_name))
            self.table_view.setItem(row, 3, QTableWidgetItem(p.category))
            self.table_view.setItem(row, 4, QTableWidgetItem(f"{p.followers:,}"))
            pub_item = QTableWidgetItem("✓ Enabled" if p.publishing_enabled else "— Disabled")
            pub_item.setForeground(
                Qt.GlobalColor.darkGreen if p.publishing_enabled else Qt.GlobalColor.gray
            )
            self.table_view.setItem(row, 5, pub_item)
            self.table_view.item(row, 0).setData(Qt.ItemDataRole.UserRole, p.id)

    def _render_pages_cards(self, pages: list[PageSummaryDTO]) -> None:
        # Clear grid
        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cols = 3
        for i, p in enumerate(pages):
            card = CutePageCard(p)
            card.clicked.connect(self._on_card_clicked)
            card.publishing_toggled.connect(self._on_page_publishing_toggled)
            self.cards_grid.addWidget(card, i // cols, i % cols)

    def _render_groups_table(self, groups: list[GroupSummaryDTO]) -> None:
        self.table_view.clear()
        self.table_view.setColumnCount(6)
        self.table_view.setHorizontalHeaderLabels(
            [
                "Platform ID",
                "Group Name",
                "Managing Account",
                "Role",
                "Members",
                "Posting Permission",
            ]
        )
        self.table_view.setRowCount(len(groups))
        for row, g in enumerate(groups):
            self.table_view.setItem(row, 0, QTableWidgetItem(g.platform_group_id))
            self.table_view.setItem(row, 1, QTableWidgetItem(g.name))
            self.table_view.setItem(row, 2, QTableWidgetItem(g.account_name))
            self.table_view.setItem(row, 3, QTableWidgetItem(g.role))
            self.table_view.setItem(row, 4, QTableWidgetItem(f"{g.members:,}"))
            self.table_view.setItem(row, 5, QTableWidgetItem(g.posting_permission))
            self.table_view.item(row, 0).setData(Qt.ItemDataRole.UserRole, g.id)

    def _render_groups_cards(self, groups: list[GroupSummaryDTO]) -> None:
        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cols = 3
        for i, g in enumerate(groups):
            card = CuteGroupCard(g)
            card.clicked.connect(self._on_card_clicked)
            self.cards_grid.addWidget(card, i // cols, i % cols)

    # -------------------------------------------------------------------------
    # Inspector Selection
    # -------------------------------------------------------------------------

    def _on_table_cell_clicked(self, row: int, _col: int) -> None:
        item = self.table_view.item(row, 0)
        if item:
            entity_id = item.data(Qt.ItemDataRole.UserRole)
            self._select_entity(entity_id)

    def _on_card_clicked(self, entity_id: str) -> None:
        self._select_entity(entity_id)

    def _select_entity(self, entity_id: str) -> None:
        self._selected_item_id = entity_id
        if self.current_section == "pages":
            pages = self.query_service.list_pages()
            matched = next((p for p in pages if p.id == entity_id), None)
            if matched:
                self.insp_title.setText(f"📄 {matched.name}")
                self.insp_subtitle.setText(f"Platform Page ID: {matched.platform_page_id}")
                details_text = (
                    f"<b>Managing Account:</b> {matched.account_name}<br>"
                    f"<b>Category:</b> {matched.category}<br>"
                    f"<b>Followers:</b> {matched.followers:,}<br>"
                    f"<b>Publishing:</b> {'Enabled' if matched.publishing_enabled else 'Disabled'}<br>"
                    f"<b>Last Synced:</b> {matched.last_synced_at or 'Never'}"
                )
                self.insp_details.setText(details_text)
                self.insp_notes.setText(matched.notes or "")
        else:
            groups = self.query_service.list_groups()
            matched_g = next((g for g in groups if g.id == entity_id), None)
            if matched_g:
                self.insp_title.setText(f"👥 {matched_g.name}")
                self.insp_subtitle.setText(f"Platform Group ID: {matched_g.platform_group_id}")
                details_text = (
                    f"<b>Managing Account:</b> {matched_g.account_name}<br>"
                    f"<b>Role:</b> {matched_g.role}<br>"
                    f"<b>Members:</b> {matched_g.members:,}<br>"
                    f"<b>Posting Permission:</b> {matched_g.posting_permission}<br>"
                    f"<b>Last Synced:</b> {matched_g.last_synced_at or 'Never'}"
                )
                self.insp_details.setText(details_text)
                self.insp_notes.setText(matched_g.notes or "")

    # -------------------------------------------------------------------------
    # Dialog Handlers
    # -------------------------------------------------------------------------

    def _on_add_item(self) -> None:
        accounts = self.account_queries.list_accounts()
        if not accounts:
            QMessageBox.warning(
                self,
                "No Accounts",
                "Please onboard an account first before adding Pages or Groups.",
            )
            return

        if self.current_section == "pages":
            dlg = PageDialog(accounts=accounts, parent=self)
            if dlg.exec():
                cmd = dlg.get_add_command()
                res = self.add_page_handler.handle(cmd)
                if res.is_success:
                    self.refresh_data()
                else:
                    QMessageBox.critical(self, "Failed to Add Page", res.error.message)
        else:
            dlg_g = GroupDialog(accounts=accounts, parent=self)
            if dlg_g.exec():
                cmd_g = dlg_g.get_add_command()
                res_g = self.add_group_handler.handle(cmd_g)
                if res_g.is_success:
                    self.refresh_data()
                else:
                    QMessageBox.critical(self, "Failed to Add Group", res_g.error.message)

    def _on_edit_item(self) -> None:
        if not self._selected_item_id:
            return
        accounts = self.account_queries.list_accounts()

        if self.current_section == "pages":
            pages = self.query_service.list_pages()
            page = next((p for p in pages if p.id == self._selected_item_id), None)
            if not page:
                return
            dlg = PageDialog(accounts=accounts, page=page, parent=self)
            if dlg.exec():
                cmd = dlg.get_update_command()
                res = self.update_page_handler.handle(cmd)
                if res.is_success:
                    self.refresh_data()
                    self._select_entity(self._selected_item_id)
                else:
                    QMessageBox.critical(self, "Failed to Update Page", res.error.message)
        else:
            groups = self.query_service.list_groups()
            group = next((g for g in groups if g.id == self._selected_item_id), None)
            if not group:
                return
            dlg_g = GroupDialog(accounts=accounts, group=group, parent=self)
            if dlg_g.exec():
                cmd_g = dlg_g.get_update_command()
                res_g = self.update_group_handler.handle(cmd_g)
                if res_g.is_success:
                    self.refresh_data()
                    self._select_entity(self._selected_item_id)
                else:
                    QMessageBox.critical(self, "Failed to Update Group", res_g.error.message)

    def _on_delete_item(self) -> None:
        if not self._selected_item_id:
            return
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to detach this record?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        if self.current_section == "pages":
            res = self.delete_page_handler.handle(DeletePageCommand(page_id=self._selected_item_id))
        else:
            res = self.delete_group_handler.handle(
                DeleteGroupCommand(group_id=self._selected_item_id)
            )

        if res.is_success:
            self._selected_item_id = None
            self.insp_title.setText("No Selection")
            self.insp_subtitle.setText("Select an item to view records")
            self.insp_details.setText("")
            self.insp_notes.setText("")
            self.refresh_data()
        else:
            QMessageBox.critical(self, "Delete Failed", res.error.message)

    def _on_save_notes(self) -> None:
        if not self._selected_item_id:
            return
        notes_text = self.insp_notes.toPlainText().strip()
        if self.current_section == "pages":
            self.update_page_handler.handle(
                UpdatePageCommand(page_id=self._selected_item_id, notes=notes_text)
            )
        else:
            self.update_group_handler.handle(
                UpdateGroupCommand(group_id=self._selected_item_id, notes=notes_text)
            )
        self.refresh_data()

    def _on_page_publishing_toggled(self, page_id: str, enabled: bool) -> None:
        self.update_page_handler.handle(
            UpdatePageCommand(page_id=page_id, publishing_enabled=enabled)
        )

    def _on_event_received(self, event: Event) -> None:
        if isinstance(
            event,
            (
                PageAddedEvent,
                PageUpdatedEvent,
                PageDeletedEvent,
                GroupAddedEvent,
                GroupUpdatedEvent,
                GroupDeletedEvent,
            ),
        ):
            QTimer.singleShot(50, self.refresh_data)
