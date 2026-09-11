
# app/core/context_menus.py
from PySide6.QtWidgets import QMenu, QMessageBox
from PySide6.QtGui import QAction  # QAction lives in QtGui in PySide6
from PySide6.QtGui import QIcon
from PySide6.QtCore import QPoint

from core.utils import get_selected_account_ids

def show_table_profile_context_menu(parent, table_widget, position: QPoint, all_categories: list):
    def selected_ids():
        return get_selected_account_ids(table_widget)
    index = table_widget.indexAt(position)

    if not index.isValid():
        return
    context_menu = QMenu(parent)

    # === Main Actions ===
    start_action = QAction(QIcon(":/icons/images/start.png"), "Start", parent)
    context_menu.addAction(start_action)

    stop_action = QAction(QIcon(":/icons/images/stop.png"), "Stop", parent)
    context_menu.addAction(stop_action)

    context_menu.addSeparator()

    delete_action = QAction(QIcon(":/icons/images/delete_red.png"), "Delete", parent)
    context_menu.addAction(delete_action)

    context_menu.addSeparator()

    set_location_action = QAction(QIcon(":/icons/images/location.png"), "Set Fake Location", parent)
    context_menu.addAction(set_location_action)

    set_vpn_action = QAction(QIcon(":/icons/images/vpn_loaction.png"), "Set VPN", parent)
    context_menu.addAction(set_vpn_action)


    context_menu.addSeparator()

    # --- 1. Create the top-level "Category" submenu ---
    category_submenu = context_menu.addMenu("Category")
    category_submenu.setIcon(QIcon(":/icons/images/folder.png")) # Optional icon for the main item

    # --- 2. Create the "Add To Category" submenu INSIDE the "Category" submenu ---
    add_to_submenu = category_submenu.addMenu("Add To Category")
    add_to_submenu.setIcon(QIcon(":/icons/images/add_folder.png")) # Specific icon for this action

    # --- 3. Loop through categories and add them to the INNER submenu ---
    if all_categories:
        for category_name in all_categories:
            category_action = QAction(category_name, parent)
            category_action.triggered.connect( lambda checked=False, cat=category_name: parent.update_accounts_category_by_id(selected_ids(), cat))
            add_to_submenu.addAction(category_action)
    else:
        no_categories_action = QAction("No categories available", parent)
        no_categories_action.setEnabled(False)
        add_to_submenu.addAction(no_categories_action)

        # --- FIX: "Remove Category" Action ---
    category_submenu.addSeparator()
    #Remove From Category
    remove_category_action = QAction(QIcon(":/icons/images/delete_red.png"), "Remove From Category", parent)
    category_submenu.addAction(remove_category_action)
    remove_category_action.triggered.connect( lambda: parent.update_accounts_category_by_id(selected_ids(), None))

    # === Connect Delete with Confirmation ===

    # ==== Start ==========
    start_action.triggered.connect(lambda: parent.start_accounts_manual(ids=selected_ids(), actions=None))
    stop_action.triggered.connect(lambda: parent.stop_accounts_manual(selected_ids()))


    delete_action.triggered.connect(lambda: parent.delete_multiple_accounts(selected_ids()))

    # === Connect open_set_location_dialog ===
    set_location_action.triggered.connect(lambda: parent.set_location(selected_ids()))

    set_vpn_action.triggered.connect(lambda: parent.set_VPN(selected_ids()))

    # set Note
    context_menu.addSeparator()
    set_note_action = QAction(QIcon(":/icons/images/notes.png"), "Set Notes", parent)
    context_menu.addAction(set_note_action)
    set_note_action.triggered.connect(lambda: parent.set_notes(selected_ids()))

    # set Up Post
    set_up_post = QAction(QIcon(":/icons/images/post_icon.png"), "Set Up Post", parent)
    context_menu.addAction(set_up_post)
    set_up_post.triggered.connect(lambda: parent.pop_up_set_up_post(selected_ids()))

    # Get User ID
    get_user_id = QAction(QIcon(":/icons/images/get_uid.png"), "Get User ID", parent)
    context_menu.addAction(get_user_id)
    get_user_id.triggered.connect(lambda: parent.start_accounts_manual(selected_ids(), actions="get_user_ids"))

    # Scrape Group
    scrape_group = QAction(QIcon(":/icons/images/get_uid.png"), "Scrap Groups", parent)
    context_menu.addAction(scrape_group)
    scrape_group.triggered.connect(lambda: parent.start_accounts_manual(selected_ids(), actions="scrape_group"))


    context_menu.addSeparator()
    delete_action = QAction(QIcon(":/icons/images/delete_red.png"), "Check Like", parent)
    context_menu.addAction(delete_action)
    context_menu.addSeparator()
    delete_action.triggered.connect(lambda: parent.check_live_by_uid(selected_ids()))




    # === Show Menu ===
    context_menu.exec(
        table_widget.viewport().mapToGlobal(position)
    )






















# Reg Table
def show_table_reg_accounts_context_menu(parent, table_widget, position: QPoint, all_categories: list):
    item = table_widget.itemAt(position)


    if item is None:
        return

    row = item.row()
    context_menu = QMenu(parent)


    delete_action = QAction(QIcon(":/icons/images/delete_red.png"), "Delete", parent)
    context_menu.addAction(delete_action)

    context_menu.addSeparator()

    move_to_dashboard = QAction(QIcon(":/icons/images/add_folder.png"), "Move to Dashboard", parent)
    context_menu.addAction(move_to_dashboard)

    

    # === Connect Delete with Confirmation ===
    delete_action.triggered.connect(lambda: parent.confirm_and_delete_selected_accounts_reg())
    move_to_dashboard.triggered.connect(lambda: parent.confirm_and_move_selected_accounts_reg())


    # === Show Menu ===
    clicked_x = position.x()
    row_y = table_widget.visualRect(table_widget.model().index(row, 0)).y()
    precise_point = QPoint(clicked_x, row_y)
    context_menu.setMinimumWidth(180)
    global_position = table_widget.viewport().mapToGlobal(precise_point)
    context_menu.exec(global_position)



