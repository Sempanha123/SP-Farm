# core\utils.py
import cv2
from PySide6.QtCore import Qt, QTimer, QTime, QCoreApplication, QSize
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QComboBox, QLabel,QTableView
from typing import List
import os
from PySide6.QtCore import QSortFilterProxyModel
from datetime import datetime

def is_widget_checked(widget: QWidget) -> bool:
    if hasattr(widget, 'isCheckable') and widget.isCheckable():
        return widget.isChecked()
    return False

def get_time_ago(date_string):
    if not date_string:
        return "Never"
    try:
        past_date = datetime.strptime(date_string, "%d/%m/%Y %I:%M:%S %p")
        diff = datetime.now() - past_date
        seconds = int(diff.total_seconds())
        
        if seconds < 60: return "Just now"
        if seconds < 3600: return f"{seconds // 60}mn ago"
        if seconds < 86400: return f"{seconds // 3600}h ago"
        if seconds < 2592000: return f"{seconds // 86400} days ago"
        return f"{seconds // 2592000} month ago"
    except:
        return date_string


def _get_nested_value(data_dict, key_string, joiner: str = ","):
    keys = key_string.split('.')

    # If it's a composite key with more than 2 segments:
    # Example: "gps.lat.long" or "vpn.name.city"
    if len(keys) > 2:
        root = keys[0]                      # gps / vpn
        subkeys = keys[1:]                  # ["lat","long"] / ["name","city"]
        container = data_dict.get(root, {})

        if isinstance(container, dict):
            values = [str(container.get(k, "")) for k in subkeys if container.get(k) is not None]
            return joiner.join(values) if values else ""
        return ""

    # --- Standard case (simple nesting) ---
    value = data_dict
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return ""
    return "" if value is None else str(value)


def populate_table_by_header(
    table_widget: QTableWidget,
    header_map: dict,
    all_accounts_data: list
):
    """
    Populate a table using the real ID from data instead of generating a new sequential one.
    """

    if table_widget is None:
        return

    table_widget.setUpdatesEnabled(False)

    table_widget.clearContents()
    table_widget.setRowCount(len(all_accounts_data))

    headers = [
        table_widget.horizontalHeaderItem(c).text()
        for c in range(table_widget.columnCount())
    ]

    for row_index, account in enumerate(all_accounts_data):
        
        # 1. Look up how 'ID' is mapped to your JSON/dict key (e.g., 'id', 'account_id', 'uid')
        # We find the exact header name that matches "ID" case-insensitively
        id_json_key = None
        for h_name, j_key in header_map.items():
            if h_name.strip().upper() == "ID":
                id_json_key = j_key
                break

        # 2. Get the real data ID, fallback to sequential string if not found or empty
        real_id = ""
        if id_json_key:
            real_id = str(_get_nested_value(account, id_json_key) or "")
            
        if not real_id:
            real_id = str(row_index + 1) # Fallback safety line

        for col_index, header_name in enumerate(headers):

            if header_name.strip().upper() == "ID":
                value = real_id
            else:
                json_key = header_map.get(header_name)
                value = (
                    _get_nested_value(account, json_key)
                    if json_key
                    else ""
                )

            item = QTableWidgetItem(str(value))

            # Keep the real ID stored safely in the item's custom data role
            item.setData(
                Qt.ItemDataRole.UserRole,
                real_id
            )

            table_widget.setItem(
                row_index,
                col_index,
                item
            )

    table_widget.setSortingEnabled(True)
    table_widget.setUpdatesEnabled(True)

    # Force refresh even if hidden inside QStackedWidget
    table_widget.viewport().repaint()
    QCoreApplication.processEvents()


def get_selected_rows_data(table_widget: QTableWidget, column_name: str) -> List[str]:
    selected_data = []
    column_index = -1
    
    # 🟢 FIX: Lowercase normalization guarantees columns are found regardless of casing
    target_col = str(column_name).strip().lower()
    
    for i in range(table_widget.columnCount()):
        header_item = table_widget.horizontalHeaderItem(i)
        if header_item and header_item.text().strip().lower() == target_col:
            column_index = i
            break
            
    if column_index == -1:
        print(f"Warning: Column '{column_name}' not found in table.")
        return []

    # Get a list of all selected rows
    selected_rows = table_widget.selectionModel().selectedRows()
    for index in selected_rows:
        item = table_widget.item(index.row(), column_index)
        if item:
            selected_data.append(item.text())
            
    return selected_data


def get_id_of_selected_row(table_widget: QTableWidget):
    """
    🟢 FIX: Removed the incorrect standalone 'self' parameter.
    Now accepts any active table widget directly from your UI controllers.
    """
    selected_rows = table_widget.selectionModel().selectedRows()
    if not selected_rows:
        return None

    selected_row_index = selected_rows[0].row()
    id_column_index = -1
    
    # Find the 'ID' column index with case safety
    for i in range(table_widget.columnCount()):
        header_item = table_widget.horizontalHeaderItem(i)
        if header_item and header_item.text().strip().upper() == "ID":
            id_column_index = i
            break
            
    if id_column_index != -1:
        id_item = table_widget.item(selected_row_index, id_column_index)
        if id_item:
            return id_item.text()
            
    return None






def get_selected_account_mode(ui: QWidget) -> str:
    if hasattr(ui, "active_accounts") and ui.active_accounts.isChecked():
        return "active"
    elif hasattr(ui, "reg_accounts") and ui.reg_accounts.isChecked():
        return "reg"
    else:
        return "none"


def update_table_cell_by_name(table_widget: QTableWidget, name_column_name: str, target_name: str, update_column_name: str, new_text: str):
    """
    📝 Updates a specific cell text based on a matching row identifier name and column header.
    🛡️ Optimized with try-finally to guarantee UI signals are NEVER locked up.
    """
    table_widget.blockSignals(True)
    
    try:
        name_col_idx = -1
        update_col_idx = -1
        
        # Case-insensitive lookups for cell configuration definitions
        target_name_header = str(name_column_name).strip().lower()
        target_update_header = str(update_column_name).strip().lower()
        
        for i in range(table_widget.columnCount()):
            header_item = table_widget.horizontalHeaderItem(i)
            if header_item:
                header_text = header_item.text().strip().lower()
                if header_text == target_name_header:
                    name_col_idx = i
                if header_text == target_update_header:
                    update_col_idx = i

        if name_col_idx == -1 or update_col_idx == -1:
            print(f"⚠️ Error: Column tracking failed. Name col: {name_col_idx}, Update col: {update_col_idx}")
            return False

        for row in range(table_widget.rowCount()):
            item = table_widget.item(row, name_col_idx)
            if item and item.text().strip() == str(target_name).strip():
                cell_item = table_widget.item(row, update_col_idx)
                if not cell_item:
                    cell_item = QTableWidgetItem()
                    table_widget.setItem(row, update_col_idx, cell_item)
                
                cell_item.setText(str(new_text))
                return True
                
        print(f"⚠️ Warning: Row named '{target_name}' not found in table.")
        return False

    finally:
        # 🟢 ALWAYS RUNS: This guarantees the main thread recovers its signals 
        # even if an error occurs or an early return is triggered!
        table_widget.blockSignals(False)



#========== New QTableView==============
def get_selected_account_ids(table_view):
    ids = []

    selection = table_view.selectionModel()

    if not selection:
        return ids

    model = table_view.model()

    for index in selection.selectedRows():

        # Handle proxy models safely
        if isinstance(model, QSortFilterProxyModel):
            source_index = model.mapToSource(index)
            source_model = model.sourceModel()
        else:
            source_index = index
            source_model = model

        # Your AccountModel stores ID in UserRole
        account_id = source_model.data(
            source_index,
            Qt.UserRole
        )

        if account_id is not None:
            ids.append(str(account_id))

    return ids





class UITimer:
    """Reusable timer that updates QLabel or QLineEdit."""
    def __init__(self, widget):
        """
        widget: QLineEdit or QLabel that displays time.
        """
        self.widget = widget
        self.timer = QTimer()
        self.timer.timeout.connect(self._update)
        self.elapsed = QTime(0, 0, 0)
        self.running = False

        # If widget is QLineEdit, make it read-only
        if hasattr(self.widget, "setReadOnly"):
            self.widget.setReadOnly(True)

        # Initialize with 00:00:00
        self.widget.setText("00:00:00")

    def start(self):
        """Start timer from 00:00:00."""
        if self.running:
            return
        self.elapsed = QTime(0, 0, 0)
        self.widget.setText("00:00:00")
        self.timer.start(1000)
        self.running = True

    def stop(self):
        """Stop timer but keep current display."""
        if not self.running:
            return
        self.timer.stop()
        self.running = False

    def reset(self):
        """Reset timer to 00:00:00 without starting."""
        self.elapsed = QTime(0, 0, 0)
        self.widget.setText("00:00:00")

    def _update(self):
        """Update time every second."""
        self.elapsed = self.elapsed.addSecs(1)
        self.widget.setText(self.elapsed.toString("hh:mm:ss"))
    def check_clock_running(self):
        return self.running

