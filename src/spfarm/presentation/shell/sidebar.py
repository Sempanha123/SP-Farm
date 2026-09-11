"""Cute left navigation sidebar for SP-Farm V2."""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from spfarm.shared.i18n import t
from spfarm.shared.theme import PALETTE


class SidebarItem(QListWidgetItem):
    def __init__(self, icon_text: str, label_key: str, route_id: str) -> None:
        label = t(label_key)
        super().__init__(f"{icon_text}  {label}")
        self.route_id = route_id
        self.setData(Qt.ItemDataRole.UserRole, route_id)


class AppSidebar(QFrame):
    """Left navigation sidebar adhering to 01_UX_UI_SOURCE_OF_TRUTH.txt."""

    route_changed = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(220)
        self.setStyleSheet(f"""
            AppSidebar {{
                background-color: {PALETTE.surface_alt};
                border-right: 1px solid {PALETTE.border};
            }}
            QListWidget {{
                background: transparent;
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                padding: 9px 14px;
                border-radius: 8px;
                color: {PALETTE.text};
                margin-bottom: 2px;
                font-weight: 500;
            }}
            QListWidget::item:hover {{
                background-color: {PALETTE.soft_primary};
                color: {PALETTE.primary};
            }}
            QListWidget::item:selected {{
                background-color: {PALETTE.soft_primary};
                color: {PALETTE.primary};
                font-weight: bold;
            }}
        """)

        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(12)

        # App Brand Header: ♡ SP FARM
        brand_layout = QHBoxLayout()
        heart_lbl = QLabel("♡")
        heart_lbl.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        heart_lbl.setStyleSheet(f"color: {PALETTE.cute_pink};")

        title_lbl = QLabel("SP-FARM")
        title_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_lbl.setStyleSheet(f"color: {PALETTE.primary}; letter-spacing: 1px;")

        brand_layout.addWidget(heart_lbl)
        brand_layout.addWidget(title_lbl)
        brand_layout.addStretch()
        layout.addLayout(brand_layout)

        v2_badge = QLabel("V2 OPERATIONS")
        v2_badge.setStyleSheet(f"color: {PALETTE.text_muted}; font-size: 10px; font-weight: 600; padding-left: 2px;")
        layout.addWidget(v2_badge)

        # Navigation List
        self.nav_list = QListWidget()
        self.nav_list.currentRowChanged.connect(self._on_row_changed)

        def add_header(label: str) -> None:
            item = QListWidgetItem(f"— {label.upper()} —")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            item.setForeground(Qt.GlobalColor.darkGray)
            font = QFont("Segoe UI", 8, QFont.Weight.Bold)
            item.setFont(font)
            self.nav_list.addItem(item)

        add_header("Overview")
        self.nav_list.addItem(SidebarItem("📊", "route.dashboard", "dashboard"))
        self.nav_list.addItem(SidebarItem("👤", "route.accounts", "accounts"))
        self.nav_list.addItem(SidebarItem("🌐", "route.environments", "environments"))

        add_header("Devices")
        self.nav_list.addItem(SidebarItem("📱", "route.devices", "devices"))
        self.nav_list.addItem(SidebarItem("🏊", "route.device_pool", "device_pool"))
        self.nav_list.addItem(SidebarItem("📦", "route.apps", "apps"))

        add_header("Operations")
        self.nav_list.addItem(SidebarItem("📢", "route.campaigns", "campaigns"))
        self.nav_list.addItem(SidebarItem("📅", "route.scheduler", "scheduler"))
        self.nav_list.addItem(SidebarItem("⚡", "route.jobs", "jobs"))
        self.nav_list.addItem(SidebarItem("🎯", "route.actions", "actions"))

        add_header("System")
        self.nav_list.addItem(SidebarItem("📜", "route.activity", "activity"))
        self.nav_list.addItem(SidebarItem("⚙️", "route.settings", "settings"))

        layout.addWidget(self.nav_list, 1)

        # Select initial item (Dashboard, index 1)
        self.nav_list.setCurrentRow(1)

    def _on_row_changed(self, row: int) -> None:
        item = self.nav_list.item(row)
        if item and item.flags() & Qt.ItemFlag.ItemIsEnabled:
            route_id = item.data(Qt.ItemDataRole.UserRole)
            if route_id:
                self.route_changed.emit(route_id)

    def select_route(self, route_id: str) -> None:
        """Select a route programmatically by its ID."""
        for i in range(self.nav_list.count()):
            item = self.nav_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == route_id:
                self.nav_list.setCurrentRow(i)
                break
