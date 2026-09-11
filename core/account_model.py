from PySide6.QtCore import (
    Qt,
    QModelIndex,
    QAbstractTableModel,
)


class AccountModel(QAbstractTableModel):

    def __init__(self, cache, columns):
        super().__init__()

        self.cache = cache
        self.columns = columns

    # ==========================================================
    # Basic
    # ==========================================================

    def rowCount(self, parent=QModelIndex()):
        return self.cache.count()

    def columnCount(self, parent=QModelIndex()):
        return len(self.columns)

    # ==========================================================
    # Header
    # ==========================================================

    def headerData(self, section, orientation, role):

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.columns[section]["header"]

        return section + 1

    # ==========================================================
    # Cell Data
    # ==========================================================

    def data(self, index, role):

        if not index.isValid():
            return None

        if role == Qt.UserRole:
            return self.cache.value(index.row(), "id")

        if role != Qt.DisplayRole:
            return None

        col = self.columns[index.column()]
        key = col["key"]

        value = self.cache.value(index.row(), key)

        formatter = col.get("formatter")

        if formatter:
            try:
                return formatter(value)
            except Exception:
                return ""

        return "" if value is None else str(value)

    # ==========================================================
    # Refresh
    # ==========================================================

    def refresh(self, force_reload=False):
        """
        Reload cache from disk.
        """
        self.beginResetModel()

        self.cache.load(force_reload)

        self.endResetModel()

    def reset(self):
        """
        Cache already changed.
        Only refresh the view.
        """
        self.beginResetModel()
        self.endResetModel()

    # ==========================================================
    # Update One Account
    # ==========================================================

    def update_account(self, account_id, **fields):

        row = self.cache.update_many(
            account_id,
            **fields
        )

        if row == -1:
            return False

        self.notify_row_changed(row)

        return True

    # ==========================================================
    # Update Multiple Accounts
    # ==========================================================

    def update_accounts(self, ids, **fields):

        rows = self.cache.update_many_accounts(
            ids,
            **fields
        )

        self.notify_rows_changed(rows)

        return rows

    # ==========================================================
    # Notify
    # ==========================================================

    def notify_row_changed(self, row):

        if row < 0:
            return

        left = self.index(row, 0)
        right = self.index(
            row,
            self.columnCount() - 1
        )

        self.dataChanged.emit(
            left,
            right,
            [Qt.DisplayRole]
        )

    def notify_rows_changed(self, rows):

        for row in rows:
            self.notify_row_changed(row)

    # ==========================================================
    # Insert
    # ==========================================================

    def insert_accounts(self, accounts):

        if not accounts:
            return

        first = self.cache.count()
        last = first + len(accounts) - 1

        self.beginInsertRows(
            QModelIndex(),
            first,
            last
        )

        self.cache.add_many(accounts)

        self.endInsertRows()

    # ==========================================================
    # Remove
    # ==========================================================

    def remove_accounts(self, ids):

        if not ids:
            return

        self.beginResetModel()

        self.cache.remove(ids)

        self.endResetModel()