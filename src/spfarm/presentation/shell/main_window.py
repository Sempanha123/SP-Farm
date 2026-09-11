"""Cute Light MainWindow root desktop application shell."""

from __future__ import annotations

import logging
from typing import Optional

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from spfarm.domain.interfaces.secret_store import ISecretStore
from spfarm.infrastructure.container import Container
from spfarm.infrastructure.container import container as default_container
from spfarm.presentation.activity.activity_view import ActivityCenterView
from spfarm.presentation.components.cards import CuteCard
from spfarm.presentation.components.command_palette import CommandPaletteDialog
from spfarm.presentation.components.inspector import CuteInspector
from spfarm.presentation.components.status_pill import CuteStatusPill
from spfarm.presentation.settings.settings_view import SettingsDialog
from spfarm.presentation.shell.sidebar import AppSidebar
from spfarm.presentation.shell.topbar import AppTopbar
from spfarm.shared.i18n import i18n, t
from spfarm.shared.settings import AppSettings, SettingsManager
from spfarm.shared.theme import build_app_stylesheet, get_theme_palette

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application shell coordinating sidebar, topbar, route views, and inspector."""

    def __init__(
        self,
        app_container: Optional[Container] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.container = app_container or default_container
        self.settings_manager: SettingsManager = self.container.settings_manager
        self.secret_store: ISecretStore = self.container.secret_store

        # Window geometry per UX specs: 1366x768 default support
        self.setWindowTitle("SP-Farm V2 — Social Operations Platform")
        self.setMinimumSize(1024, 640)
        self.resize(1366, 768)

        self._current_theme = self.settings_manager.get().appearance.theme
        self._apply_theme(self._current_theme)

        self._setup_ui()
        self._setup_shortcuts()

    def _setup_ui(self) -> None:
        root_widget = QWidget()
        root_layout = QHBoxLayout(root_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 1. Left Sidebar
        self.sidebar = AppSidebar()
        self.sidebar.route_changed.connect(self.navigate_to_route)
        root_layout.addWidget(self.sidebar)

        # 2. Main Center Workspace (Topbar + Stacked Views)
        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        # Topbar
        self.topbar = AppTopbar()
        self.topbar.theme_changed.connect(self._on_theme_changed)
        self.topbar.language_changed.connect(self._on_language_changed)
        self.topbar.command_palette_requested.connect(self.open_command_palette)
        center_layout.addWidget(self.topbar)

        # Stacked Views
        self.stack = QStackedWidget()
        self._route_indices: dict[str, int] = {}

        self._register_route("dashboard", self._create_dashboard_view())
        self._register_route("accounts", self._create_placeholder_view("👤 Accounts Management", "Profiles, Pages, Groups"))
        self._register_route("environments", self._create_placeholder_view("🌐 Account Environment Profiles", "Decoupled device profiles"))
        self._register_route("devices", self._create_placeholder_view("📱 Runtime Devices", "Physical Android, LDPlayer, MuMu"))
        self._register_route("device_pool", self._create_placeholder_view("🏊 Device Pool Orchestrator", "Multi-device allocation"))
        self._register_route("apps", self._create_placeholder_view("📦 Mobile Applications", "Facebook Official & Lite catalogs"))
        self._register_route("campaigns", self._create_placeholder_view("📢 Publishing Campaigns", "Content scheduling"))
        self._register_route("scheduler", self._create_placeholder_view("📅 Operations Calendar", "Scheduled workflows"))
        self._register_route("jobs", self._create_placeholder_view("⚡ Automation Jobs", "Job execution and queue"))
        self._register_route("actions", self._create_placeholder_view("🎯 Action Drawer", "Routine batch operations"))
        self._register_route("activity", self._create_activity_view())
        self._register_route("settings", self._create_settings_embed())

        center_layout.addWidget(self.stack, 1)
        root_layout.addWidget(center_container, 1)

        # 3. Right-side Inspector Panel (Collapsible)
        self.inspector = CuteInspector()
        self.inspector.hide()
        root_layout.addWidget(self.inspector)

        self.setCentralWidget(root_widget)

    def _setup_shortcuts(self) -> None:
        # Ctrl+K: Command Palette
        cmd_action = QAction(self)
        cmd_action.setShortcut(QKeySequence("Ctrl+K"))
        cmd_action.triggered.connect(self.open_command_palette)
        self.addAction(cmd_action)

        # Ctrl+,: Settings
        settings_action = QAction(self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(lambda: self.navigate_to_route("settings"))
        self.addAction(settings_action)

    def _register_route(self, route_id: str, widget: QWidget) -> None:
        idx = self.stack.addWidget(widget)
        self._route_indices[route_id] = idx

    def navigate_to_route(self, route_id: str) -> None:
        """Switch central workspace to the specified route."""
        if route_id in self._route_indices:
            self.stack.setCurrentIndex(self._route_indices[route_id])
            self.topbar.set_title(t(f"route.{route_id}", default=route_id.capitalize()))
            self.sidebar.select_route(route_id)

    def open_command_palette(self) -> None:
        """Open the Ctrl+K command palette modal dialog."""
        palette_dlg = CommandPaletteDialog(self)
        palette_dlg.action_triggered.connect(self._handle_command_palette_action)
        palette_dlg.exec()

    def _handle_command_palette_action(self, action_id: str) -> None:
        if action_id.startswith("theme:"):
            theme_name = action_id.split(":", 1)[1]
            self._on_theme_changed(theme_name)
        elif action_id in self._route_indices:
            self.navigate_to_route(action_id)

    def _on_theme_changed(self, theme_id: str) -> None:
        self._current_theme = theme_id
        self._apply_theme(theme_id)

        # Persist theme in settings
        def update_theme(s: AppSettings) -> None:
            s.appearance.theme = theme_id

        self.settings_manager.update(update_theme)

    def _apply_theme(self, theme_id: str) -> None:
        pal = get_theme_palette(theme_id)
        stylesheet = build_app_stylesheet(pal)
        qapp = QApplication.instance()
        if qapp:
            qapp.setStyleSheet(stylesheet)

    def _on_language_changed(self, lang_code: str) -> None:
        i18n.set_language(lang_code)
        # Refresh current topbar title
        current_route = list(self._route_indices.keys())[self.stack.currentIndex()]
        self.topbar.set_title(t(f"route.{current_route}", default=current_route.capitalize()))

    # -------------------------------------------------------------------------
    # Route Views
    # -------------------------------------------------------------------------
    def _create_dashboard_view(self) -> QWidget:
        view = QWidget()
        layout = QVBoxLayout(view)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Welcome Card
        welcome_card = CuteCard(title="🌱 Welcome to SP-Farm V2")
        w_lbl = QLabel(
            "Clean, modern operations dashboard adhering to the Cute Light Design System. "
            "Navigate using the left sidebar or press <b>Ctrl+K</b> to quickly jump between screens."
        )
        w_lbl.setWordWrap(True)
        welcome_card.add_widget(w_lbl)
        layout.addWidget(welcome_card)

        # Metrics summary row
        metrics_row = QHBoxLayout()
        metrics_row.setSpacing(12)

        card1 = CuteCard(title="👥 Accounts", badge=CuteStatusPill("Healthy", "ready"))
        card1.add_widget(QLabel("<b>Total Managed:</b> 0 accounts<br><b>Active Sessions:</b> 0"))
        metrics_row.addWidget(card1)

        card2 = CuteCard(title="📱 Device Pool", badge=CuteStatusPill("Ready", "ready"))
        card2.add_widget(QLabel("<b>Ready Devices:</b> 0<br><b>Running Jobs:</b> 0"))
        metrics_row.addWidget(card2)

        card3 = CuteCard(title="📢 Campaigns", badge=CuteStatusPill("Idle", "cooldown"))
        card3.add_widget(QLabel("<b>Scheduled Posts:</b> 0<br><b>Pending Reviews:</b> 0"))
        metrics_row.addWidget(card3)

        layout.addLayout(metrics_row)
        layout.addStretch()
        return view

    def _create_activity_view(self) -> QWidget:
        return ActivityCenterView(
            log_buffer=self.container.resolve("LogRingBuffer") if "LogRingBuffer" in self.container.registered_service_names else self.container.resolve("spfarm.infrastructure.logging.buffer.LogRingBuffer") if False else None or __import__("spfarm.infrastructure.logging.setup", fromlist=["get_log_buffer"]).get_log_buffer(),
            error_center=self.container.error_center,
            audit_service=self.container.audit_service,
        )

    def _create_settings_embed(self) -> QWidget:
        view = QWidget()
        layout = QVBoxLayout(view)
        layout.setContentsMargins(20, 20, 20, 20)

        card = CuteCard(title="⚙️ Application Settings")
        desc = QLabel("Configure visual theme, local storage paths, device emulators, and secure secret vault.")
        btn_launch = QPushButton("Launch Full Settings Dialog")
        btn_launch.clicked.connect(self._launch_settings_dialog)

        card.add_widget(desc)
        card.add_widget(btn_launch)
        layout.addWidget(card)
        layout.addStretch()
        return view

    def _launch_settings_dialog(self) -> None:
        dlg = SettingsDialog(self.settings_manager, self.secret_store, self)
        dlg.exec()

    def _create_placeholder_view(self, title: str, subtitle: str) -> QWidget:
        view = QWidget()
        layout = QVBoxLayout(view)
        layout.setContentsMargins(20, 20, 20, 20)

        card = CuteCard(title=title)
        sub_lbl = QLabel(f"<i>{subtitle}</i><br><br>Ready for full module orchestration in subsequent phases.")
        card.add_widget(sub_lbl)
        layout.addWidget(card)
        layout.addStretch()
        return view
