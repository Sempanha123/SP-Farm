"""Cute Light Activity Center view with live log tailing, batched rendering, Error Center, and Audit Trail."""

from __future__ import annotations

import json
import logging
from collections import deque
from typing import Any, Optional

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont, QTextCharFormat
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from spfarm.application.services.audit import AuditService
from spfarm.application.services.error_center import ErrorCenterService
from spfarm.infrastructure.logging.buffer import LogRingBuffer
from spfarm.shared.theme import PALETTE

logger = logging.getLogger(__name__)


class ActivityCenterView(QWidget):
    """Activity, Logs, Error Center, and Audit Trail monitoring interface."""

    def __init__(
        self,
        log_buffer: LogRingBuffer,
        error_center: ErrorCenterService,
        audit_service: AuditService,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.log_buffer = log_buffer
        self.error_center = error_center
        self.audit_service = audit_service

        self._pending_log_entries: deque[dict[str, Any]] = deque(maxlen=10000)
        self._is_paused = False
        self._auto_scroll = True

        self.setWindowTitle("Activity & Observability Center — SP-Farm V2")
        self.setMinimumSize(950, 600)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {PALETTE.background};
                color: {PALETTE.text};
                font-family: 'Segoe UI', system-ui, sans-serif;
            }}
            QTabWidget::pane {{
                border: 1px solid {PALETTE.border};
                background: {PALETTE.surface};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background: {PALETTE.surface_alt};
                color: {PALETTE.text_secondary};
                padding: 8px 18px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 4px;
                font-weight: 600;
            }}
            QTabBar::tab:selected {{
                background: {PALETTE.surface};
                color: {PALETTE.primary_blue};
                border: 1px solid {PALETTE.border};
                border-bottom: 2px solid {PALETTE.primary_blue};
            }}
            QLineEdit, QComboBox {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border_strong};
                border-radius: 6px;
                padding: 6px 10px;
            }}
            QTableWidget, QListWidget, QPlainTextEdit {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border};
                border-radius: 8px;
            }}
            QHeaderView::section {{
                background-color: {PALETTE.surface_alt};
                color: {PALETTE.text_secondary};
                font-weight: 600;
                padding: 6px;
                border: none;
                border-bottom: 1px solid {PALETTE.border};
            }}
        """)

        self._setup_ui()

        # Batch log UI rendering timer (100ms tick prevents UI freezing on flood)
        self._batch_timer = QTimer(self)
        self._batch_timer.setInterval(100)
        self._batch_timer.timeout.connect(self._flush_pending_logs)
        self._batch_timer.start()

        # Load initial backlog from buffer
        for entry in self.log_buffer.get_entries(limit=300):
            self._pending_log_entries.append(entry)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_logs_tab(), "📜 Live Logs")
        self.tabs.addTab(self._create_error_center_tab(), "⚠️ Error Center")
        self.tabs.addTab(self._create_audit_tab(), "🛡️ Audit Trail")
        layout.addWidget(self.tabs)

    # -------------------------------------------------------------------------
    # TAB 1: Live Logs
    # -------------------------------------------------------------------------
    def _create_logs_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Filters toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        lbl_level = QLabel("Level:")
        self.cmb_level = QComboBox()
        self.cmb_level.addItems(["ALL", "INFO", "WARNING", "ERROR", "DEBUG"])
        self.cmb_level.currentIndexChanged.connect(self._on_filter_changed)

        lbl_search = QLabel("Search:")
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Filter messages or loggers...")
        self.txt_search.textChanged.connect(self._on_filter_changed)

        self.btn_pause = QPushButton("⏸️ Pause")
        self.btn_pause.setCheckable(True)
        self.btn_pause.clicked.connect(self._toggle_pause)

        self.btn_clear = QPushButton("🧹 Clear")
        self.btn_clear.clicked.connect(self._clear_logs_view)

        toolbar.addWidget(lbl_level)
        toolbar.addWidget(self.cmb_level)
        toolbar.addWidget(lbl_search)
        toolbar.addWidget(self.txt_search, 1)
        toolbar.addWidget(self.btn_pause)
        toolbar.addWidget(self.btn_clear)
        layout.addLayout(toolbar)

        # Log Display
        self.log_text_edit = QPlainTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setMaximumBlockCount(4000)
        font = QFont("Consolas", 10)
        self.log_text_edit.setFont(font)
        layout.addWidget(self.log_text_edit, 1)

        return tab

    def enqueue_log_entry(self, entry: dict[str, Any]) -> None:
        """Enqueue an incoming log entry for batched rendering."""
        if not self._is_paused:
            self._pending_log_entries.append(entry)

    def _flush_pending_logs(self) -> None:
        """Batch process queued logs on a timer to ensure 60fps responsiveness."""
        if not self._pending_log_entries:
            return

        active_level = self.cmb_level.currentText()
        active_search = self.txt_search.text().strip().lower()

        # Batch up to 150 items per tick to prevent any UI stutter
        batch_size = min(len(self._pending_log_entries), 150)
        items_to_render: list[dict[str, Any]] = []

        for _ in range(batch_size):
            item = self._pending_log_entries.popleft()
            if active_level != "ALL" and item.get("level") != active_level:
                continue
            if active_search:
                msg = item.get("message", "").lower()
                logger_name = item.get("logger", "").lower()
                if active_search not in msg and active_search not in logger_name:
                    continue
            items_to_render.append(item)

        if not items_to_render:
            return

        cursor = self.log_text_edit.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)

        for entry in items_to_render:
            time_part = entry.get("timestamp", "").split("T")[-1][:8]
            level = entry.get("level", "INFO")
            logger_name = entry.get("logger", "root")
            message = entry.get("message", "")

            corr = entry.get("correlation", {})
            corr_str = ""
            if corr:
                pairs = [f"{k}={v}" for k, v in corr.items() if v]
                corr_str = f"[{' '.join(pairs)}] "

            fmt = QTextCharFormat()
            if level == "ERROR":
                fmt.setForeground(QColor(PALETTE.danger))
            elif level == "WARNING":
                fmt.setForeground(QColor(PALETTE.warning))
            else:
                fmt.setForeground(QColor(PALETTE.text))

            line = f"[{time_part}] [{level:<7}] {logger_name}: {corr_str}{message}"
            cursor.insertText(line + "\n", fmt)

        if self._auto_scroll:
            self.log_text_edit.verticalScrollBar().setValue(
                self.log_text_edit.verticalScrollBar().maximum()
            )

    def _toggle_pause(self) -> None:
        self._is_paused = self.btn_pause.isChecked()
        self.btn_pause.setText("▶️ Resume" if self._is_paused else "⏸️ Pause")

    def _clear_logs_view(self) -> None:
        self.log_text_edit.clear()
        self._pending_log_entries.clear()

    def _on_filter_changed(self) -> None:
        self.log_text_edit.clear()
        level = None if self.cmb_level.currentText() == "ALL" else self.cmb_level.currentText()
        search = self.txt_search.text().strip() or None
        backlog = self.log_buffer.get_entries(limit=300, level=level, search=search)
        for entry in backlog:
            self._pending_log_entries.append(entry)

    # -------------------------------------------------------------------------
    # TAB 2: Error Center
    # -------------------------------------------------------------------------
    def _create_error_center_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(12, 12, 12, 12)

        # Header with refresh
        header = QHBoxLayout()
        header_title = QLabel("⚠️ Grouped Application Errors")
        header_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        header.addWidget(header_title)
        header.addStretch()

        btn_refresh = QPushButton("🔄 Refresh Errors")
        btn_refresh.clicked.connect(self.refresh_error_center)
        header.addWidget(btn_refresh)
        layout.addLayout(header)

        # Splitter: List on Left, Trace & Details on Right
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.error_list = QListWidget()
        self.error_list.currentItemChanged.connect(self._on_error_selected)
        splitter.addWidget(self.error_list)

        # Right pane: Detail card
        self.error_detail_frame = QFrame()
        detail_layout = QVBoxLayout(self.error_detail_frame)
        detail_layout.setSpacing(10)

        self.lbl_error_title = QLabel("Select an error to inspect details and correlation trace.")
        self.lbl_error_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.lbl_error_title.setWordWrap(True)
        detail_layout.addWidget(self.lbl_error_title)

        # Trace chain card
        self.trace_card = QFrame()
        self.trace_card.setStyleSheet(f"""
            background-color: {PALETTE.surface_alt};
            border: 1px solid {PALETTE.border};
            border-radius: 8px;
            padding: 10px;
        """)
        self.trace_layout = QVBoxLayout(self.trace_card)
        self.lbl_trace_chain = QLabel("<b>Correlation Trace Chain:</b> None")
        self.lbl_trace_chain.setWordWrap(True)
        self.trace_layout.addWidget(self.lbl_trace_chain)
        detail_layout.addWidget(self.trace_card)

        # Stack trace box
        lbl_st = QLabel("Stack Trace:")
        lbl_st.setStyleSheet(f"color: {PALETTE.text_secondary}; font-weight: 600;")
        detail_layout.addWidget(lbl_st)

        self.txt_stack_trace = QPlainTextEdit()
        self.txt_stack_trace.setReadOnly(True)
        self.txt_stack_trace.setFont(QFont("Consolas", 9))
        detail_layout.addWidget(self.txt_stack_trace, 1)

        # Action buttons
        btn_layout = QHBoxLayout()
        self.btn_ack_error = QPushButton("Acknowledge")
        self.btn_ack_error.clicked.connect(self._ack_selected_error)
        self.btn_resolve_error = QPushButton("Resolve")
        self.btn_resolve_error.setStyleSheet(f"background-color: {PALETTE.success}; color: white;")
        self.btn_resolve_error.clicked.connect(self._resolve_selected_error)

        btn_layout.addWidget(self.btn_ack_error)
        btn_layout.addWidget(self.btn_resolve_error)
        btn_layout.addStretch()
        detail_layout.addLayout(btn_layout)

        splitter.addWidget(self.error_detail_frame)
        splitter.setSizes([350, 600])
        layout.addWidget(splitter, 1)

        self.refresh_error_center()
        return tab

    def refresh_error_center(self) -> None:
        """Reload grouped errors from ErrorCenterService."""
        self.error_list.clear()
        errors = self.error_center.list_errors()

        for err in errors:
            status_emoji = (
                "🔴" if err.status == "active" else ("🟡" if err.status == "acknowledged" else "🟢")
            )
            item_text = (
                f"{status_emoji} [{err.count}x] {err.error_type}: {err.message_template[:45]}"
            )
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, err.fingerprint)
            self.error_list.addItem(item)

    def _on_error_selected(
        self, current: Optional[QListWidgetItem], previous: Optional[QListWidgetItem]
    ) -> None:
        if not current:
            return

        fp = current.data(Qt.ItemDataRole.UserRole)
        err = self.error_center.get_error(fp)
        if not err:
            return

        self.lbl_error_title.setText(f"[{err.status.upper()}] {err.error_type}: {err.last_message}")
        self.txt_stack_trace.setPlainText(err.stack_trace or "(No stack trace recorded)")

        # Format multi-entity trace chain: Job -> Environment -> Device -> Account
        trace = self.error_center.trace_error(fp)
        if trace:
            tc = trace.get("trace_chain", {})
            jobs = ", ".join(tc.get("jobs", [])) or "none"
            envs = ", ".join(tc.get("environments", [])) or "none"
            devs = ", ".join(tc.get("devices", [])) or "none"
            accs = ", ".join(tc.get("accounts", [])) or "none"

            chain_text = (
                f"<b>Trace Path:</b><br>"
                f"• <b>Job:</b> {jobs}<br>"
                f"• <b>Environment:</b> {envs}<br>"
                f"• <b>Device:</b> {devs}<br>"
                f"• <b>Account:</b> {accs}<br>"
                f"• <i>First seen:</i> {err.first_seen_at} | <i>Last seen:</i> {err.last_seen_at}"
            )
            self.lbl_trace_chain.setText(chain_text)

    def _ack_selected_error(self) -> None:
        item = self.error_list.currentItem()
        if item:
            fp = item.data(Qt.ItemDataRole.UserRole)
            self.error_center.acknowledge_error(fp)
            self.refresh_error_center()

    def _resolve_selected_error(self) -> None:
        item = self.error_list.currentItem()
        if item:
            fp = item.data(Qt.ItemDataRole.UserRole)
            self.error_center.resolve_error(fp)
            self.refresh_error_center()

    # -------------------------------------------------------------------------
    # TAB 3: Audit Trail
    # -------------------------------------------------------------------------
    def _create_audit_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(12, 12, 12, 12)

        # Header
        header = QHBoxLayout()
        header_title = QLabel("🛡️ Immutable Security & Operator Audit Trail")
        header_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        header.addWidget(header_title)
        header.addStretch()

        btn_refresh = QPushButton("🔄 Refresh Audit")
        btn_refresh.clicked.connect(self.refresh_audit_trail)
        header.addWidget(btn_refresh)
        layout.addLayout(header)

        # Table
        self.audit_table = QTableWidget()
        self.audit_table.setColumnCount(6)
        self.audit_table.setHorizontalHeaderLabels(
            ["Timestamp", "Event Type", "Actor", "Target Type", "Target ID", "Details"]
        )
        self.audit_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.audit_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        self.audit_table.verticalHeader().setVisible(False)
        self.audit_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.audit_table, 1)

        self.refresh_audit_trail()
        return tab

    def refresh_audit_trail(self) -> None:
        """Reload audit entries from AuditService."""
        events = self.audit_service.query(limit=200)
        self.audit_table.setRowCount(len(events))

        for row, evt in enumerate(events):
            time_str = evt.timestamp.split("T")[-1][:8]
            self.audit_table.setItem(row, 0, QTableWidgetItem(f"{evt.timestamp[:10]} {time_str}"))
            self.audit_table.setItem(row, 1, QTableWidgetItem(evt.event_type))
            self.audit_table.setItem(row, 2, QTableWidgetItem(evt.actor))
            self.audit_table.setItem(row, 3, QTableWidgetItem(evt.target_type))
            self.audit_table.setItem(row, 4, QTableWidgetItem(evt.target_id))
            self.audit_table.setItem(row, 5, QTableWidgetItem(json.dumps(evt.details)))
