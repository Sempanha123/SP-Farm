from PySide6.QtWidgets import QStackedWidget, QTableWidgetItem
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt, QTimer

def change_stacked_widget_page(stacked_widget: QStackedWidget, page_index: int):
    if stacked_widget:
        stacked_widget.setCurrentIndex(page_index)
        QCoreApplication.processEvents()







def Update_Table_By_ID_RowName(
    table_widget,
    row_id,
    *args
):
    """
    Update table values by ID column.

    Example:
        Update_Table_By_ID_RowName(
            table,
            2,
            "Noted", "tested",
            "Sex", "M"
        )
    """

    if len(args) % 2 != 0:
        raise ValueError(
            "Arguments must be column_name, value pairs"
        )

    # -----------------------------
    # Build header map once
    # -----------------------------
    headers = {}

    for col in range(table_widget.columnCount()):

        item = table_widget.horizontalHeaderItem(col)

        if item:
            headers[item.text().strip().lower()] = col

    id_col = headers.get("id")

    if id_col is None:
        print("❌ ID column not found")
        return False

    # -----------------------------
    # Find row
    # -----------------------------
    target_row = None

    for row in range(table_widget.rowCount()):

        item = table_widget.item(row, id_col)

        if item and str(item.text()) == str(row_id):
            target_row = row
            break

    if target_row is None:
        print(f"❌ ID {row_id} not found")
        return False

    # -----------------------------
    # Update cells
    # -----------------------------
    table_widget.setUpdatesEnabled(False)

    for i in range(0, len(args), 2):

        column_name = str(args[i]).strip().lower()
        value = str(args[i + 1])

        col = headers.get(column_name)

        if col is None:
            print(f"⚠️ Column '{column_name}' not found")
            continue

        existing_item = table_widget.item(target_row, col)

        if existing_item:
            existing_item.setText(value)
        else:
            table_widget.setItem(
                target_row,
                col,
                QTableWidgetItem(value)
            )

    table_widget.setUpdatesEnabled(True)

    # Works even if hidden in QStackedWidget
    table_widget.viewport().repaint()
    QCoreApplication.processEvents()

    return True



def Show_Message(
    parent,
    title="Message",
    text="",
    icon="info",
    buttons=QMessageBox.StandardButton.Ok,
    auto_close_ms=None
):
    """
    General alert dialog.

    icon:
        "info"
        "warning"
        "error"
        "question"

    auto_close_ms:
        None = wait for user
        3000 = close after 3 seconds
    """

    msg = QMessageBox(parent)

    msg.setWindowTitle(title)
    msg.setText(str(text))
    msg.setStandardButtons(buttons)

    # Prevent clicking behind the dialog
    msg.setWindowModality(Qt.WindowModality.ApplicationModal)

    # Always stay on top
    msg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    # Select icon
    icon_map = {
        "info": QMessageBox.Icon.Information,
        "warning": QMessageBox.Icon.Warning,
        "error": QMessageBox.Icon.Critical,
        "question": QMessageBox.Icon.Question,
    }

    msg.setIcon(
        icon_map.get(icon.lower(), QMessageBox.Icon.Information)
    )

    # Auto close
    if auto_close_ms:
        QTimer.singleShot(auto_close_ms, msg.accept)

    return msg.exec()

