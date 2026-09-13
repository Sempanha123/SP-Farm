"""Cute Light Devices Workspace view for managing runtime devices fleet."""

from __future__ import annotations

import html
import logging
from typing import Any, Callable, Optional

from PySide6.QtCore import QObject, QRunnable, Qt, QThreadPool, QTimer, Signal, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from spfarm.application.commands.device_commands import (
    DiscoverDevicesCommand,
    DiscoverDevicesHandler,
    LaunchDevicePackageHandler,
    RestartDeviceCommand,
    RestartDeviceHandler,
    StartDeviceCommand,
    StartDeviceHandler,
    StopDeviceCommand,
    StopDeviceHandler,
    StopDevicePackageHandler,
    TakeDeviceScreenshotCommand,
    TakeDeviceScreenshotHandler,
)
from spfarm.application.events.base import Event, EventBus
from spfarm.application.events.device_events import (
    DeviceCommandExecutedEvent,
    DeviceDiscoveredEvent,
    DeviceHealthChangedEvent,
    DeviceStateChangedEvent,
)
from spfarm.application.queries.devices import (
    DeviceDetailDTO,
    DeviceQueryService,
    DeviceSummaryDTO,
    ListDevicesQuery,
)
from spfarm.presentation.components.buttons import CuteButton
from spfarm.presentation.components.inspector import CuteInspector
from spfarm.presentation.components.status_pill import CuteStatusPill
from spfarm.shared.paths import paths
from spfarm.shared.theme import PALETTE

logger = logging.getLogger(__name__)

PROVIDER_ICONS = {
    "PHYSICAL_ANDROID": "📱 Physical",
    "LDPLAYER": "🎮 LDPlayer",
    "MUMU": "🐱 MuMu",
    "CUSTOM": "💻 Custom",
    "FAKE": "🧪 Simulated",
}

class _OperationSignals(QObject):
    completed = Signal(object)


class _Operation(QRunnable):
    def __init__(self, function: Callable[[], Any]) -> None:
        super().__init__()
        self.function = function
        self.signals = _OperationSignals()

    @Slot()
    def run(self) -> None:
        self.signals.completed.emit(self.function())


STATE_PILL_TYPES = {
    "READY": "ready",
    "RUNNING": "running",
    "RESERVED": "running",
    "BOOTING": "warning",
    "STOPPING": "cooldown",
    "COOLDOWN": "cooldown",
    "OFFLINE": "offline",
    "UNAUTHORIZED": "warning",
    "ERROR": "error",
}


class DevicesView(QWidget):
    """Modern Cute Light workspace for managing runtime devices and emulators."""

    navigate_requested = Signal(str)

    def __init__(
        self,
        query_service: DeviceQueryService,
        discover_handler: DiscoverDevicesHandler,
        start_handler: StartDeviceHandler,
        stop_handler: StopDeviceHandler,
        restart_handler: RestartDeviceHandler,
        screenshot_handler: TakeDeviceScreenshotHandler,
        launch_handler: LaunchDevicePackageHandler,
        stop_pkg_handler: StopDevicePackageHandler,
        event_bus: Optional[EventBus] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.query_service = query_service
        self.discover_handler = discover_handler
        self.start_handler = start_handler
        self.stop_handler = stop_handler
        self.restart_handler = restart_handler
        self.screenshot_handler = screenshot_handler
        self.launch_handler = launch_handler
        self.stop_pkg_handler = stop_pkg_handler
        self.event_bus = event_bus

        self._selected_device_id: Optional[str] = None
        self._devices_cache: list[DeviceSummaryDTO] = []
        self._thread_pool = QThreadPool.globalInstance()
        self._operations: set[_Operation] = set()

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

        # 1. Top Toolbar
        root_layout.addLayout(self._build_top_toolbar())

        # 2. Main Content Splitter (Table + Inspector)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background-color: transparent; width: 8px; }")

        # Table Widget
        self.table_view = self._build_table_widget()
        splitter.addWidget(self.table_view)

        # Inspector Panel
        self.inspector = self._build_inspector()
        splitter.addWidget(self.inspector)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        root_layout.addWidget(splitter, 1)

    def _build_top_toolbar(self) -> QHBoxLayout:
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        # Scan / Discover Button
        self.btn_scan = CuteButton("🔍 Scan Fleet", role="primary")
        self.btn_scan.clicked.connect(self._on_scan_devices)
        toolbar.addWidget(self.btn_scan)

        toolbar.addSpacing(10)

        # Provider Filter
        self.cmb_provider = QComboBox()
        self.cmb_provider.addItem("All Providers", "ALL")
        self.cmb_provider.addItem("📱 Physical Android", "PHYSICAL_ANDROID")
        self.cmb_provider.addItem("🎮 LDPlayer", "LDPLAYER")
        self.cmb_provider.addItem("🐱 MuMu", "MUMU")
        self.cmb_provider.addItem("🧪 Simulated (Fake)", "FAKE")
        self.cmb_provider.currentIndexChanged.connect(self.refresh_data)
        toolbar.addWidget(self.cmb_provider)

        # State Filter
        self.cmb_state = QComboBox()
        self.cmb_state.addItem("All States", "ALL")
        self.cmb_state.addItem("Ready", "READY")
        self.cmb_state.addItem("Running / Busy", "RUNNING")
        self.cmb_state.addItem("Booting", "BOOTING")
        self.cmb_state.addItem("Offline", "OFFLINE")
        self.cmb_state.addItem("Unauthorized — approve USB debugging", "UNAUTHORIZED")
        self.cmb_state.addItem("Error", "ERROR")
        self.cmb_state.currentIndexChanged.connect(self.refresh_data)
        toolbar.addWidget(self.cmb_state)

        # Search box
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Search by name, ADB target, ID...")
        self.txt_search.setClearButtonEnabled(True)
        self.txt_search.setFixedWidth(240)
        self.txt_search.textChanged.connect(self.refresh_data)
        toolbar.addWidget(self.txt_search)

        toolbar.addStretch()

        # Refresh button
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
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(
            [
                "Provider",
                "Device Name",
                "ADB Target",
                "Android OS",
                "State",
                "Health",
                "Lease / Env",
            ]
        )
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setDefaultSectionSize(38)
        table.verticalHeader().hide()
        table.cellClicked.connect(self._on_table_cell_clicked)
        return table

    def _build_inspector(self) -> CuteInspector:
        inspector = CuteInspector(parent=self)
        inspector.lbl_title.setText("Device Inspector")
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
        self.insp_subtitle = QLabel("Select a device to view hardware & controls")
        self.insp_subtitle.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 11px;")
        layout.addWidget(self.insp_title)
        layout.addWidget(self.insp_subtitle)

        # Specifications block
        self.insp_specs = QLabel("")
        self.insp_specs.setStyleSheet("font-size: 11px; line-height: 1.5;")
        self.insp_specs.setWordWrap(True)
        layout.addWidget(self.insp_specs)

        # Action Buttons Layout
        layout.addWidget(QLabel("Device Controls:"))

        btn_row_power = QHBoxLayout()
        self.btn_power_start = CuteButton("▶ Start", role="cute")
        self.btn_power_start.clicked.connect(self._on_start_selected)
        btn_row_power.addWidget(self.btn_power_start)

        self.btn_power_stop = CuteButton("⏹ Stop", role="secondary")
        self.btn_power_stop.clicked.connect(self._on_stop_selected)
        btn_row_power.addWidget(self.btn_power_stop)

        self.btn_power_restart = CuteButton("🔄 Restart", role="ghost")
        self.btn_power_restart.clicked.connect(self._on_restart_selected)
        btn_row_power.addWidget(self.btn_power_restart)
        layout.addLayout(btn_row_power)

        btn_row_tools = QHBoxLayout()
        self.btn_screenshot = CuteButton("📸 Screenshot", role="ghost")
        self.btn_screenshot.clicked.connect(self._on_screenshot_selected)
        btn_row_tools.addWidget(self.btn_screenshot)

        layout.addLayout(btn_row_tools)

        # Command outcome feedback
        self.insp_log = QLabel("")
        self.insp_log.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 10px;")
        self.insp_log.setWordWrap(True)
        layout.addWidget(self.insp_log)

        layout.addStretch()
        inspector.content_layout.addWidget(body)
        return inspector

    # -------------------------------------------------------------------------
    # Data Refresh & Rendering
    # -------------------------------------------------------------------------
    def refresh_data(self) -> None:
        """Fetch and render devices according to current filters."""
        provider_val = self.cmb_provider.currentData()
        state_val = self.cmb_state.currentData()
        search_val = self.txt_search.text().strip() or None

        query = ListDevicesQuery(
            provider=provider_val,
            state=state_val,
            search=search_val,
        )

        self._devices_cache = self.query_service.list_devices(query)
        self._render_table(self._devices_cache)

        # Reselect item if still exists
        if self._selected_device_id:
            exists = any(d.id == self._selected_device_id for d in self._devices_cache)
            if exists:
                self._select_device(self._selected_device_id)
            else:
                self._clear_inspector()

    def _render_table(self, devices: list[DeviceSummaryDTO]) -> None:
        self.table_view.setRowCount(len(devices))
        for row, d in enumerate(devices):
            prov_text = PROVIDER_ICONS.get(d.provider, d.provider)
            item_prov = QTableWidgetItem(prov_text)
            item_prov.setData(Qt.ItemDataRole.UserRole, d.id)

            item_name = QTableWidgetItem(d.friendly_name)
            item_name.setToolTip(f"ID: {d.id}\nModel: {d.model}")

            connection = "TCP" if d.provider == "PHYSICAL_ANDROID" and ":" in d.adb_target else "USB"
            adb_text = (
                f"{d.adb_target} · {connection}"
                if d.provider == "PHYSICAL_ANDROID"
                else d.adb_target
            )
            item_adb = QTableWidgetItem(adb_text)
            item_os = QTableWidgetItem(f"Android {d.android_version}")

            self.table_view.setItem(row, 0, item_prov)
            self.table_view.setItem(row, 1, item_name)
            self.table_view.setItem(row, 2, item_adb)
            self.table_view.setItem(row, 3, item_os)

            # State status pill
            pill_type = STATE_PILL_TYPES.get(d.state, "offline")
            pill_state = CuteStatusPill(d.state, pill_type)
            self.table_view.setCellWidget(row, 4, pill_state)

            # Health status pill
            h_type = (
                "ready"
                if d.health == "HEALTHY"
                else ("warning" if d.health == "WARNING" else "error")
            )
            pill_health = CuteStatusPill(d.health, h_type)
            self.table_view.setCellWidget(row, 5, pill_health)

            # Lease / Env
            env_txt = (
                f"Env: {d.current_environment_id}" if d.current_environment_id else "— Available —"
            )
            item_env = QTableWidgetItem(env_txt)
            self.table_view.setItem(row, 6, item_env)

    def _on_table_cell_clicked(self, row: int, _col: int) -> None:
        item = self.table_view.item(row, 0)
        if item:
            dev_id = item.data(Qt.ItemDataRole.UserRole)
            if dev_id:
                self._select_device(dev_id)

    def _select_device(self, device_id: str, clear_log: bool = False) -> None:
        self._selected_device_id = device_id
        detail: Optional[DeviceDetailDTO] = self.query_service.get_device_detail(device_id)
        if not detail:
            return

        prov_icon = PROVIDER_ICONS.get(detail.provider, detail.provider)
        self.insp_title.setText(f"{detail.friendly_name}")
        self.insp_subtitle.setText(f"{prov_icon} • State: <b>{detail.state}</b>")

        caps_list = ", ".join(detail.capabilities) if detail.capabilities else "None"
        adb_status = "Available" if detail.adb_diagnostics.get("available") else "Unavailable"
        appium_status = (
            "Available" if detail.appium_diagnostics.get("available") else "Unavailable"
        )
        active_sessions = detail.session_diagnostics.get("active_sessions", 0)
        connection = (
            "TCP" if detail.provider == "PHYSICAL_ANDROID" and ":" in detail.adb_target else "USB"
        )
        connection_html = (
            f"<b>Connection:</b> {connection}<br>"
            if detail.provider == "PHYSICAL_ANDROID"
            else ""
        )
        specs_html = f"""
        <b>ADB Target:</b> {html.escape(detail.adb_target)}<br>
        {connection_html}
        <b>ADB Service:</b> {adb_status}<br>
        <b>Appium:</b> {appium_status}<br>
        <b>Appium Sessions:</b> {active_sessions}<br>
        <b>Android:</b> Version {html.escape(detail.android_version)}<br>
        <b>Display:</b> {html.escape(detail.resolution_display)}<br>
        <b>Manufacturer:</b> {html.escape(detail.manufacturer)}<br>
        <b>Model:</b> {html.escape(detail.model)}<br>
        <b>Capabilities:</b> {html.escape(caps_list)}<br>
        <b>Assigned Env:</b> {html.escape(detail.current_environment_id or "None")}<br>
        <b>Active Lease:</b> {html.escape(detail.lease_token or "None")}<br>
        <b>Last Seen:</b> {html.escape(detail.last_seen_at or "Never")}
        """
        self.insp_specs.setText(specs_html)
        if clear_log:
            self.insp_log.setText("")

    def _clear_inspector(self) -> None:
        self._selected_device_id = None
        self.insp_title.setText("No Selection")
        self.insp_subtitle.setText("Select a device to view hardware & controls")
        self.insp_specs.setText("")
        self.insp_log.setText("")

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------
    def _run_operation(
        self, function: Callable[[], Any], completed: Callable[[Any], None]
    ) -> None:
        operation = _Operation(function)
        self._operations.add(operation)

        def finish(result: object) -> None:
            self._operations.discard(operation)
            completed(result)

        operation.signals.completed.connect(finish)
        self._thread_pool.start(operation)

    def _on_scan_devices(self) -> None:
        self.btn_scan.setEnabled(False)
        self._run_operation(
            lambda: self.discover_handler.handle(DiscoverDevicesCommand()),
            self._on_scan_completed,
        )

    def _on_scan_completed(self, result: Any) -> None:
        self.btn_scan.setEnabled(True)
        res = result
        if res.is_success:
            count = len(res.value)
            self.refresh_data()
            self.insp_log.setText(f"Fleet scan completed: {count} device(s) found.")
        else:
            QMessageBox.critical(self, "Scan Error", res.error.message)

    def _on_start_selected(self) -> None:
        if not self._selected_device_id:
            return
        device_id = self._selected_device_id
        self._run_operation(
            lambda: self.start_handler.handle(StartDeviceCommand(device_id=device_id)),
            lambda result: self._on_device_operation_completed(result, "Start Device Failed"),
        )

    def _on_stop_selected(self) -> None:
        if not self._selected_device_id:
            return
        device_id = self._selected_device_id
        self._run_operation(
            lambda: self.stop_handler.handle(StopDeviceCommand(device_id=device_id)),
            lambda result: self._on_device_operation_completed(result, "Stop Device Failed"),
        )

    def _on_restart_selected(self) -> None:
        if not self._selected_device_id:
            return
        device_id = self._selected_device_id
        self._run_operation(
            lambda: self.restart_handler.handle(RestartDeviceCommand(device_id=device_id)),
            lambda result: self._on_device_operation_completed(result, "Restart Device Failed"),
        )

    def _on_device_operation_completed(self, result: Any, error_title: str) -> None:
        if result.is_success:
            self.refresh_data()
            self.insp_log.setText(f"✓ {result.value.message}")
        else:
            QMessageBox.warning(self, error_title, result.error.message)

    def _on_screenshot_selected(self) -> None:
        if not self._selected_device_id:
            return
        device_id = self._selected_device_id
        out_path = paths.logs_dir / "screenshots" / f"screenshot_{device_id}.png"
        self._run_operation(
            lambda: self.screenshot_handler.handle(
                TakeDeviceScreenshotCommand(device_id=device_id, output_path=out_path)
            ),
            lambda result: self._on_screenshot_completed(result, out_path.name),
        )

    def _on_screenshot_completed(self, result: Any, filename: str) -> None:
        if result.is_success:
            self.refresh_data()
            self.insp_log.setText(f"✓ Screenshot saved to {filename}")
        else:
            QMessageBox.warning(self, "Screenshot Failed", result.error.message)

    def _on_event_received(self, event: Event) -> None:
        if isinstance(
            event,
            (
                DeviceDiscoveredEvent,
                DeviceStateChangedEvent,
                DeviceHealthChangedEvent,
                DeviceCommandExecutedEvent,
            ),
        ):
            QTimer.singleShot(50, self.refresh_data)
