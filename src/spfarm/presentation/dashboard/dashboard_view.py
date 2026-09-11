"""Cute Operations Dashboard view adhering to 01_UX_UI_SOURCE_OF_TRUTH.txt."""

from __future__ import annotations

import logging
from typing import Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from spfarm.application.events.base import Event, EventBus
from spfarm.application.queries.dashboard import DashboardDataDTO, DashboardQueryService
from spfarm.presentation.components.buttons import CuteButton
from spfarm.presentation.components.cards import CuteCard
from spfarm.presentation.components.status_pill import CuteStatusPill
from spfarm.presentation.dashboard.metric_card import CuteMetricCard
from spfarm.shared.theme import PALETTE

logger = logging.getLogger(__name__)


class DashboardView(QWidget):
    """Main operations dashboard with live metric counters, fleet telemetry, and activity."""

    navigate_requested = Signal(str)

    def __init__(
        self,
        query_service: DashboardQueryService,
        event_bus: Optional[EventBus] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.query_service = query_service
        self.event_bus = event_bus

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {PALETTE.background};
                color: {PALETTE.text};
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QListWidget {{
                background: transparent;
                border: none;
            }}
            QListWidget::item {{
                padding: 6px 8px;
                border-radius: 6px;
                border-bottom: 1px solid {PALETTE.border};
            }}
        """)

        self._setup_ui()

        # Connect EventBus for immediate reactive updates
        if self.event_bus:
            self.event_bus.subscribe_all(self._on_event_received)

        # Low-frequency poll timer (every 5 seconds) for system telemetry
        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(5000)
        self._refresh_timer.timeout.connect(self.refresh_data)
        self._refresh_timer.start()

        # Initial data load
        self.refresh_data()

    def _setup_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area to comfortably handle 1366x768 without clipping
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        root_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(20, 16, 20, 20)
        self.layout.setSpacing(14)

        # 1. Quick Action & Header Toolbar
        self._build_header_toolbar()

        # 2. Empty State Banner (Shown conditionally)
        self._build_empty_state_banner()

        # 3. KPI Metrics Row (6 Pastel Cards)
        self._build_metrics_grid()

        # 4. Middle Section: Running Workflows & Upcoming Schedules
        middle_row = QHBoxLayout()
        middle_row.setSpacing(14)

        self.card_running_jobs = self._build_running_jobs_card()
        middle_row.addWidget(self.card_running_jobs, 1)

        self.card_upcoming = self._build_upcoming_schedules_card()
        middle_row.addWidget(self.card_upcoming, 1)
        self.layout.addLayout(middle_row)

        # 5. Bottom Section: Recent Activity & System Telemetry
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(14)

        self.card_activity = self._build_recent_activity_card()
        bottom_row.addWidget(self.card_activity, 1)

        self.card_telemetry = self._build_telemetry_card()
        bottom_row.addWidget(self.card_telemetry, 1)
        self.layout.addLayout(bottom_row)

    def _build_header_toolbar(self) -> None:
        header = QHBoxLayout()
        header.setSpacing(10)

        title_box = QVBoxLayout()
        lbl_title = QLabel("Operations Dashboard")
        lbl_title.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        lbl_title.setStyleSheet(f"color: {PALETTE.primary};")

        lbl_sub = QLabel("Real-time fleet status, workflow executions, and system health")
        lbl_sub.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 11px;")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_sub)
        header.addLayout(title_box)

        header.addStretch()

        # Quick action buttons
        self.btn_action_account = CuteButton("➕ New Account", role="primary")
        self.btn_action_account.clicked.connect(lambda: self.navigate_requested.emit("accounts"))
        header.addWidget(self.btn_action_account)

        self.btn_action_devices = CuteButton("📱 Scan Devices", role="secondary")
        self.btn_action_devices.clicked.connect(lambda: self.navigate_requested.emit("devices"))
        header.addWidget(self.btn_action_devices)

        self.btn_action_campaign = CuteButton("📢 New Campaign", role="cute")
        self.btn_action_campaign.clicked.connect(lambda: self.navigate_requested.emit("campaigns"))
        header.addWidget(self.btn_action_campaign)

        self.btn_refresh = QPushButton("🔄")
        self.btn_refresh.setToolTip("Refresh Dashboard Data")
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
        header.addWidget(self.btn_refresh)

        self.layout.addLayout(header)

    def _build_empty_state_banner(self) -> None:
        self.empty_banner = QFrame()
        self.empty_banner.setStyleSheet(f"""
            QFrame {{
                background-color: {PALETTE.soft_primary};
                border: 1px dashed {PALETTE.primary};
                border-radius: 12px;
                padding: 12px;
            }}
        """)
        eb_layout = QHBoxLayout(self.empty_banner)
        eb_layout.setContentsMargins(16, 12, 16, 12)
        eb_layout.setSpacing(12)

        icon_lbl = QLabel("🌱✨")
        icon_lbl.setFont(QFont("Segoe UI Emoji", 24))
        eb_layout.addWidget(icon_lbl)

        msg_layout = QVBoxLayout()
        msg_title = QLabel("Welcome to SP-Farm V2! Your workspace is ready.")
        msg_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        msg_title.setStyleSheet(f"color: {PALETTE.primary};")

        msg_desc = QLabel("Get started by onboarding your first Facebook account or connecting an Android emulator or device.")
        msg_desc.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 11px;")
        msg_layout.addWidget(msg_title)
        msg_layout.addWidget(msg_desc)
        eb_layout.addLayout(msg_layout, 1)

        btn_onboard = CuteButton("Add First Account", role="cute")
        btn_onboard.clicked.connect(lambda: self.navigate_requested.emit("accounts"))
        eb_layout.addWidget(btn_onboard)

        self.empty_banner.hide()
        self.layout.addWidget(self.empty_banner)

    def _build_metrics_grid(self) -> None:
        grid_layout = QGridLayout()
        grid_layout.setSpacing(12)

        self.metric_accounts = CuteMetricCard("Accounts", value="0", icon="👤", pastel_bg="#EDF5FF", icon_fg=PALETTE.primary)
        self.metric_pages = CuteMetricCard("Pages", value="0", icon="📄", pastel_bg="#FFF1F7", icon_fg=PALETTE.cute_pink)
        self.metric_devices = CuteMetricCard("Devices", value="0", icon="📱", pastel_bg="#F3F0FF", icon_fg=PALETTE.lavender)
        self.metric_running = CuteMetricCard("Running Jobs", value="0", icon="⚡", pastel_bg="#E8F8F2", icon_fg=PALETTE.success)
        self.metric_errors = CuteMetricCard("Active Errors", value="0", icon="⚠️", pastel_bg="#FEECEE", icon_fg=PALETTE.danger)
        self.metric_scheduled = CuteMetricCard("Scheduled Today", value="0", icon="📅", pastel_bg="#FEF7E6", icon_fg=PALETTE.warning)

        grid_layout.addWidget(self.metric_accounts, 0, 0)
        grid_layout.addWidget(self.metric_pages, 0, 1)
        grid_layout.addWidget(self.metric_devices, 0, 2)
        grid_layout.addWidget(self.metric_running, 0, 3)
        grid_layout.addWidget(self.metric_errors, 0, 4)
        grid_layout.addWidget(self.metric_scheduled, 0, 5)

        self.layout.addLayout(grid_layout)

    def _build_running_jobs_card(self) -> CuteCard:
        card = CuteCard(title="⚡ Active Workflows & Device Pool", badge=CuteStatusPill("0 Running", "ready"))
        self.running_jobs_layout = QVBoxLayout()
        self.running_jobs_layout.setSpacing(8)

        self.lbl_no_jobs = QLabel("No active automation jobs running. System is idle.")
        self.lbl_no_jobs.setStyleSheet(f"color: {PALETTE.text_secondary}; font-style: italic; padding: 12px 0;")
        self.running_jobs_layout.addWidget(self.lbl_no_jobs)

        card.add_widget(QWidget())
        # Replace default layout with custom
        card.body_layout.addLayout(self.running_jobs_layout)
        return card

    def _build_upcoming_schedules_card(self) -> CuteCard:
        card = CuteCard(title="📅 Scheduled Operations Peek", badge=CuteStatusPill("Upcoming", "cooldown"))
        self.upcoming_list = QListWidget()
        self.upcoming_list.setFixedHeight(140)

        card.add_widget(self.upcoming_list)
        return card

    def _build_recent_activity_card(self) -> CuteCard:
        card = CuteCard(title="🛡️ Recent Operator & System Activity")
        self.activity_list = QListWidget()
        self.activity_list.setFixedHeight(140)

        card.add_widget(self.activity_list)
        return card

    def _build_telemetry_card(self) -> CuteCard:
        card = CuteCard(title="🖥️ Host Telemetry & System Health")
        t_layout = QVBoxLayout()
        t_layout.setSpacing(8)

        # CPU row
        cpu_box = QHBoxLayout()
        cpu_box.addWidget(QLabel("CPU Load:"))
        self.bar_cpu = QProgressBar()
        self.bar_cpu.setRange(0, 100)
        self.bar_cpu.setValue(10)
        self.bar_cpu.setFixedHeight(8)
        self.bar_cpu.setTextVisible(False)
        cpu_box.addWidget(self.bar_cpu, 1)
        self.lbl_cpu_val = QLabel("10%")
        self.lbl_cpu_val.setFixedWidth(40)
        cpu_box.addWidget(self.lbl_cpu_val)
        t_layout.addLayout(cpu_box)

        # RAM row
        ram_box = QHBoxLayout()
        ram_box.addWidget(QLabel("RAM Load:"))
        self.bar_ram = QProgressBar()
        self.bar_ram.setRange(0, 100)
        self.bar_ram.setValue(35)
        self.bar_ram.setFixedHeight(8)
        self.bar_ram.setTextVisible(False)
        ram_box.addWidget(self.bar_ram, 1)
        self.lbl_ram_val = QLabel("35%")
        self.lbl_ram_val.setFixedWidth(40)
        ram_box.addWidget(self.lbl_ram_val)
        t_layout.addLayout(ram_box)

        # Storage & Worker labels
        hw_box = QHBoxLayout()
        self.lbl_disk_free = QLabel("Free Disk: Calculating...")
        self.lbl_disk_free.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 11px;")
        self.lbl_workers = QLabel("Active Workers: 0")
        self.lbl_workers.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 11px;")

        hw_box.addWidget(self.lbl_disk_free)
        hw_box.addStretch()
        hw_box.addWidget(self.lbl_workers)
        t_layout.addLayout(hw_box)

        card.add_widget(QWidget())
        card.body_layout.addLayout(t_layout)
        return card

    def _on_event_received(self, event: Event) -> None:
        # Debounce or refresh on next tick
        QTimer.singleShot(50, self.refresh_data)

    def refresh_data(self) -> None:
        """Fetch fresh data via DashboardQueryService and update UI widgets."""
        try:
            data: DashboardDataDTO = self.query_service.get_dashboard_data()
        except Exception as exc:
            logger.warning("Failed refreshing dashboard data: %s", exc)
            return

        m = data.metrics

        # Update KPI Cards
        self.metric_accounts.set_value(m.total_accounts, f"{m.active_accounts} active")
        self.metric_pages.set_value(m.total_pages)
        self.metric_devices.set_value(m.total_devices, f"{m.ready_devices} ready")
        self.metric_running.set_value(m.running_jobs)
        self.metric_errors.set_value(m.recent_errors_count)
        self.metric_scheduled.set_value(m.scheduled_today)

        # Empty state banner toggle
        self.empty_banner.setVisible(data.is_empty_state)

        # Update Telemetry
        self.bar_cpu.setValue(int(m.cpu_percent))
        self.lbl_cpu_val.setText(f"{int(m.cpu_percent)}%")
        self.bar_ram.setValue(int(m.ram_percent))
        self.lbl_ram_val.setText(f"{int(m.ram_percent)}%")
        self.lbl_disk_free.setText(f"Free Disk: {m.disk_free_gb:.1f} GB")
        self.lbl_workers.setText(f"Active Workers: {m.active_workers}")

        # Update Upcoming schedules list
        self.upcoming_list.clear()
        if not data.upcoming_schedules:
            item = QListWidgetItem("No upcoming scheduled campaigns today.")
            item.setForeground(Qt.GlobalColor.gray)
            self.upcoming_list.addItem(item)
        else:
            for s in data.upcoming_schedules[:5]:
                self.upcoming_list.addItem(QListWidgetItem(f"⏰ {s['scheduled_time']} — {s['job_type']}"))

        # Update Recent Activity list
        self.activity_list.clear()
        if not data.recent_activity:
            item = QListWidgetItem("No recent operator activity recorded.")
            item.setForeground(Qt.GlobalColor.gray)
            self.activity_list.addItem(item)
        else:
            for act in data.recent_activity:
                time_part = act.get("timestamp", "").split("T")[-1][:8]
                self.activity_list.addItem(
                    QListWidgetItem(f"[{time_part}] {act['actor']}: {act['event_type']} ({act['target']})")
                )
