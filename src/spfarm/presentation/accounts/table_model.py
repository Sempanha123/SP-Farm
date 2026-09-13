"""High-performance QAbstractTableModel for the accounts workspace."""

from __future__ import annotations

from typing import Any, Optional

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor

from spfarm.application.queries.accounts import AccountSummaryDTO
from spfarm.shared.theme import PALETTE

COL_CHECK = 0
COL_NAME = 1
COL_CONTACT = 2
COL_STATUS = 3
COL_HEALTH = 4
COL_PAGES_GROUPS = 5
COL_DEVICE = 6
COL_LAST_ACTIVE = 7

HEADERS = [
    "☑",
    "Account / Name",
    "Primary Contact",
    "Status",
    "Health",
    "Pages / Groups",
    "Device / Env",
    "Last Active",
]


_ROOT_INDEX = QModelIndex()


class AccountsTableModel(QAbstractTableModel):
    """Virtual table model capable of smoothly rendering 10,000+ accounts."""

    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(parent)
        self._accounts: list[AccountSummaryDTO] = []
        self._selected_ids: set[str] = set()

    def rowCount(self, parent: QModelIndex = _ROOT_INDEX) -> int:
        if parent.isValid():
            return 0
        return len(self._accounts)

    def columnCount(self, parent: QModelIndex = _ROOT_INDEX) -> int:
        if parent.isValid():
            return 0
        return len(HEADERS)

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole
    ) -> Any:
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
            and 0 <= section < len(HEADERS)
        ):
            return HEADERS[section]
        return None

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or not (0 <= index.row() < len(self._accounts)):
            return None

        acc = self._accounts[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.CheckStateRole and col == COL_CHECK:
            return (
                Qt.CheckState.Checked if acc.id in self._selected_ids else Qt.CheckState.Unchecked
            )

        if role == Qt.ItemDataRole.DisplayRole:
            if col == COL_CHECK:
                return ""
            elif col == COL_NAME:
                return f"{acc.display_name} ({acc.profile_id})"
            elif col == COL_CONTACT:
                return acc.masked_contact
            elif col == COL_STATUS:
                return acc.status
            elif col == COL_HEALTH:
                return acc.health_state
            elif col == COL_PAGES_GROUPS:
                return f"{acc.pages_count}p / {acc.groups_count}g"
            elif col == COL_DEVICE:
                return acc.device_name
            elif col == COL_LAST_ACTIVE:
                if acc.last_activity_at:
                    return acc.last_activity_at.split("T")[0]
                return "Never"

        if role == Qt.ItemDataRole.ForegroundRole:
            if col == COL_STATUS:
                if acc.status == "ACTIVE":
                    return QColor(PALETTE.success)
                elif acc.status in ("RESTRICTED", "CHECKPOINT"):
                    return QColor(PALETTE.warning)
                elif acc.status in ("SUSPENDED", "ARCHIVED"):
                    return QColor(PALETTE.danger)
            elif col == COL_HEALTH:
                if acc.health_state == "HEALTHY":
                    return QColor(PALETTE.success)
                elif acc.health_state == "WARNING":
                    return QColor(PALETTE.warning)
                elif acc.health_state == "REQUIRES_ATTENTION":
                    return QColor(PALETTE.danger)

        if role == Qt.ItemDataRole.TextAlignmentRole and col in (
            COL_CHECK,
            COL_STATUS,
            COL_HEALTH,
            COL_PAGES_GROUPS,
        ):
            return Qt.AlignmentFlag.AlignCenter

        return None

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if (
            index.isValid()
            and index.column() == COL_CHECK
            and role == Qt.ItemDataRole.CheckStateRole
        ):
            acc = self._accounts[index.row()]
            if value == Qt.CheckState.Checked:
                self._selected_ids.add(acc.id)
            else:
                self._selected_ids.discard(acc.id)
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.CheckStateRole])
            return True
        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        base_flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if index.column() == COL_CHECK:
            base_flags |= Qt.ItemFlag.ItemIsUserCheckable
        return base_flags

    def set_accounts(self, accounts: list[AccountSummaryDTO]) -> None:
        """Update the underlying dataset with virtual reload."""
        self.beginResetModel()
        self._accounts = accounts
        # Prune selected IDs that no longer exist
        valid_ids = {a.id for a in accounts}
        self._selected_ids.intersection_update(valid_ids)
        self.endResetModel()

    def get_account_at(self, row: int) -> Optional[AccountSummaryDTO]:
        if 0 <= row < len(self._accounts):
            return self._accounts[row]
        return None

    def get_selected_ids(self) -> list[str]:
        return list(self._selected_ids)

    def select_all(self) -> None:
        self._selected_ids = {a.id for a in self._accounts}
        if self._accounts:
            top_left = self.index(0, COL_CHECK)
            bottom_right = self.index(len(self._accounts) - 1, COL_CHECK)
            self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.CheckStateRole])

    def clear_selection(self) -> None:
        self._selected_ids.clear()
        if self._accounts:
            top_left = self.index(0, COL_CHECK)
            bottom_right = self.index(len(self._accounts) - 1, COL_CHECK)
            self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.CheckStateRole])

    def toggle_selection(self, row: int) -> None:
        if 0 <= row < len(self._accounts):
            acc = self._accounts[row]
            if acc.id in self._selected_ids:
                self._selected_ids.remove(acc.id)
            else:
                self._selected_ids.add(acc.id)
            idx = self.index(row, COL_CHECK)
            self.dataChanged.emit(idx, idx, [Qt.ItemDataRole.CheckStateRole])
