"""Command palette (Ctrl+K) quick launcher dialog."""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from spfarm.shared.theme import PALETTE


class CommandPaletteDialog(QDialog):
    """Ctrl+K command palette popup for fast route jumping and action dispatch."""

    action_triggered = Signal(str)

    DEFAULT_COMMANDS = [
        ("📊 Jump to Dashboard", "dashboard", "Route"),
        ("👤 Jump to Accounts", "accounts", "Route"),
        ("🌐 Jump to Environments", "environments", "Route"),
        ("📱 Jump to Devices", "devices", "Route"),
        ("🏊 Jump to Device Pool", "device_pool", "Route"),
        ("📢 Jump to Campaigns", "campaigns", "Route"),
        ("📅 Jump to Scheduler", "scheduler", "Route"),
        ("⚡ Jump to Jobs", "jobs", "Route"),
        ("📜 Jump to Activity & Logs", "activity", "Route"),
        ("⚙️ Open Settings", "settings", "System"),
        ("🎨 Switch Theme: Light Blue", "theme:light_blue", "Theme"),
        ("🎨 Switch Theme: Pink", "theme:pink", "Theme"),
        ("🎨 Switch Theme: Lavender", "theme:lavender", "Theme"),
        ("🎨 Switch Theme: Dark Blue", "theme:dark_blue", "Theme"),
    ]

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Command Palette")
        self.setFixedSize(540, 360)
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border_strong};
                border-radius: 12px;
            }}
            QLineEdit {{
                background-color: {PALETTE.surface_alt};
                border: 1px solid {PALETTE.border};
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
                color: {PALETTE.text};
            }}
            QLineEdit:focus {{
                border: 1.5px solid {PALETTE.primary};
            }}
            QListWidget {{
                background: transparent;
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                padding: 8px 12px;
                border-radius: 6px;
                color: {PALETTE.text};
                margin-bottom: 2px;
            }}
            QListWidget::item:selected {{
                background-color: {PALETTE.soft_primary};
                color: {PALETTE.primary};
                font-weight: 600;
            }}
        """)

        self._setup_ui()
        self._populate_list()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        # Search field
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Type a command or jump to screen... (Esc to close)")
        self.txt_search.textChanged.connect(self._filter_items)
        layout.addWidget(self.txt_search)

        # Results list
        self.list_widget = QListWidget()
        self.list_widget.itemActivated.connect(self._on_item_selected)
        layout.addWidget(self.list_widget, 1)

        # Footer hint
        footer = QLabel("Use ↑↓ to navigate, Enter to select, Esc to close")
        footer.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 11px;")
        layout.addWidget(footer)

    def _populate_list(self) -> None:
        self.list_widget.clear()
        search = self.txt_search.text().strip().lower()

        for label, action_id, category in self.DEFAULT_COMMANDS:
            if search and search not in label.lower() and search not in category.lower():
                continue

            item = QListWidgetItem(f"{label}  [{category}]")
            item.setData(Qt.ItemDataRole.UserRole, action_id)
            self.list_widget.addItem(item)

        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _filter_items(self) -> None:
        self._populate_list()

    def _on_item_selected(self, item: QListWidgetItem) -> None:
        action_id = item.data(Qt.ItemDataRole.UserRole)
        self.action_triggered.emit(action_id)
        self.accept()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
        elif event.key() in (Qt.Key.Key_Down, Qt.Key.Key_Up):
            self.list_widget.keyPressEvent(event)
        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            current = self.list_widget.currentItem()
            if current:
                self._on_item_selected(current)
        else:
            super().keyPressEvent(event)
