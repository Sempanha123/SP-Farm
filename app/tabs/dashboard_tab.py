# app/tabs/dashboard_tab.py
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog, QDialog
import time
from PySide6.QtCore import Slot , QTimer
from core.utils import UITimer
import os
from core.context_menus import show_table_profile_context_menu
from core.ui_functions import change_stacked_widget_page, Show_Message
from core.utils import populate_table_by_header, update_table_cell_by_name, get_selected_rows_data, get_selected_account_mode
import threading
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dialogs.set_note_dialog import SetNoteDialog
from dialogs.set_location_dialog import SetLocationDialog
from dialogs.set_vpn_dialog import SetVPNDialog
from threading import Event
import concurrent.futures
from dialogs.post_account_dialog import SelectAccountDialog

import queue
from core.emulator_worker import EmulatorWorker, EmulatorManualWorker

# ==== Accounts =============
from core.account_columns import SIMPLE_COLUMNS, DETAIL_COLUMNS
from core.account_model import AccountModel
from core.account_proxy import AccountProxy

# ======== Signal =========
from core.app_signals import signals


class DashboardTab(QWidget):
    update_finished_check_acc = Signal(list)
    
    
    def __init__(self, main_window=None, ui=None, data_manager=None, ld_manager=None, general_function=None, reg_tab_controller=None, active_tab_controller=None, account_cache=None):
        super().__init__(main_window)

        self.main_window = main_window
        self.ui = ui
        self.data_manager = data_manager
        self.ld_manager = ld_manager
        self.general_function = general_function
        self.reg_tab_controller = reg_tab_controller
        self.active_tab_controller = active_tab_controller
        self.account_cache = account_cache


        self.mode = ""
        self._details_view_enabled = False 
        self._page_index = 0 

        #========= Signal ============
        signals.accounts_changed.connect(self._on_accounts_changed) # Free update from another
        signals.update_account_status.connect(self._on_update_account) #From Signal
        self.update_finished_check_acc.connect(self._update_check_acc_finished) # From Thread check UID Save Data all in once


        # ---------- Simple ----------
        self.account_model = AccountModel(
            self.account_cache,
            SIMPLE_COLUMNS
        )

        self.account_proxy = AccountProxy()
        self.account_proxy.setSourceModel(self.account_model)

        self.ui.profile_table_accounts.setModel(
            self.account_proxy
        )

        # ---------- Detail ----------
        self.detail_model = AccountModel(
            self.account_cache,
            DETAIL_COLUMNS
        )

        self.detail_proxy = AccountProxy()
        self.detail_proxy.setSourceModel(self.detail_model)

        self.ui.profile_table_details_accounts.setModel(
            self.detail_proxy
        )

        self.active_workers = []
        self.ld_executor = ThreadPoolExecutor(max_workers=20)
        self.stop_events = {}
        self.stop_events_manual = {}

        self.ld_workers = {} 
        self.task_queue = queue.Queue()


        
        
   
        self.load_ldplayer_settings()
        self.populate_category_combobox()
        self._connect_signals()
        self.refresh_tables()
        self.refresh_ld_list()


        

       
    

    def _connect_signals(self):

        self.tool_timer = UITimer(self.ui.time)

        # Connect start/stop buttons here
        self.ui.start.clicked.connect(self.on_start_clicked)
        self.ui.stop.clicked.connect(self.on_stop_all_clicked)


        # Connect the context menu for both tables to your reusable function
        self.ui.profile_table_accounts.customContextMenuRequested.connect(
            lambda pos: show_table_profile_context_menu(self, self.ui.profile_table_accounts, pos, self.data_manager.get_all_categories())
        )
        self.ui.profile_table_details_accounts.customContextMenuRequested.connect(
            lambda pos: show_table_profile_context_menu(self, self.ui.profile_table_details_accounts, pos, self.data_manager.get_all_categories())
        )

        self.ui.profile_table_accounts.selectionModel().selectionChanged.connect(
            lambda *_: self.general_function.update_selection_label(self.ui.profile_table_accounts, self.ui.seleted_accounts)
        )
        self.ui.profile_table_details_accounts.selectionModel().selectionChanged.connect(
            lambda *_: self.general_function.update_selection_label(self.ui.profile_table_details_accounts, self.ui.seleted_accounts)
        )
        self.ui.search_accs.textChanged.connect(
            self.on_search_accounts
        )

        self.account_proxy.rowsInserted.connect(
            lambda *_: self.general_function.update_selection_label(
                self.ui.profile_table_accounts,
                self.ui.seleted_accounts
            )
        )

        self.account_proxy.rowsRemoved.connect(
            lambda *_: self.general_function.update_selection_label(
                self.ui.profile_table_accounts,
                self.ui.seleted_accounts
            )
        )

        self.account_proxy.modelReset.connect(
            lambda *_: self.general_function.update_selection_label(
                self.ui.profile_table_accounts,
                self.ui.seleted_accounts
            )
        )
        self.detail_proxy.rowsInserted.connect(
            lambda *_: self.general_function.update_selection_label(
                self.ui.profile_table_details_accounts,
                self.ui.seleted_accounts
            )
        )
        self.detail_proxy.rowsRemoved.connect(
            lambda *_: self.general_function.update_selection_label(
                self.ui.profile_table_details_accounts,
                self.ui.seleted_accounts
            )
        )
        self.detail_proxy.modelReset.connect(
            lambda *_: self.general_function.update_selection_label(
                self.ui.profile_table_details_accounts,
                self.ui.seleted_accounts
            )
        )


        
        
        # Connect the toggle button and category filter
        self.ui.show_details.toggled.connect(self.on_show_details_toggled)

        self.ui.category_filter_combobox.currentTextChanged.connect(self.on_category_changed)
        self.ui.refresh_table_accounts_dashboard.clicked.connect(self.refresh_tables)


        self.ui.refresh_ld.clicked.connect(self.refresh_ld_list)
        self.ui.add_new_category_btn.clicked.connect(self.on_add_category) # Connect your "add" button
        self.ui.delete_category_btn.clicked.connect(self.on_delete_category)
        # Connect save button
        
        # Auto-save for SpinBoxes
        self.ui.delay_per_ld.valueChanged.connect(self.save_ldplayer_settings)
        self.ui.ld_per_column.valueChanged.connect(self.save_ldplayer_settings)
        self.ui.ld_sleep.valueChanged.connect(self.save_ldplayer_settings)
        self.ui.loop.valueChanged.connect(self.save_ldplayer_settings)
        self.ui.ld_per_row.valueChanged.connect(self.save_ldplayer_settings)

        # Auto-save for CheckBoxes
        self.ui.active_accounts.toggled.connect(self.save_ldplayer_settings)
        self.ui.reg_accounts.toggled.connect(self.save_ldplayer_settings)
        self.ui.auto_expand_fit_active.toggled.connect(self.save_ldplayer_settings)
        self.ui.auto_arrange_ldplayer.toggled.connect(self.save_ldplayer_settings)
        self.ui.run_schedule_checkbox.toggled.connect(self.save_ldplayer_settings)
        self.ui.shop_tool_if_no_internet.toggled.connect(self.save_ldplayer_settings)
        #browse_ld_path
        self.ui.browse_ld_path_btn.clicked.connect(self.browse_ldplayer_path)



    # ====== Helper update to Accounts ===========
    def update_account_ui(self, account_id, save=False, **fields):
        row = self.account_cache.update_account(account_id, **fields)
        
        if row == -1 or row is None:
            return
            
        # 2. Update the UI tables
        self.account_model.notify_row_changed(row)
        self.detail_model.notify_row_changed(row)
        
        # 3. 🟢 THE FIX: Trigger the targeted save if requested!
        if save:
            self.account_cache.save_single_account(account_id)
    def update_multiple_accounts_ui(self, account_ids: list, save=False, **fields):
        # 1. Update the data in memory RAM (returns a list of affected row numbers)
        rows = self.account_cache.update_accounts(account_ids, **fields)
        
        if not rows:
            return
            
        for row in rows:
            self.account_model.notify_row_changed(row)
            self.detail_model.notify_row_changed(row)
            
        if save:
            self.account_cache.save_multiple_accounts(account_ids)


    # ======= Connect Signal Message ============
    def _on_accounts_changed(self):
        self.account_cache.reload()
        self.account_model.refresh()
        self.detail_model.refresh()
    def _on_update_account(self, account_id, save: bool, fields):
        self.update_account_ui(account_id, save=save, **fields)
    def _update_ld_status(self, ld_name, status):
        update_table_cell_by_name(
            table_widget=self.ui.ldplayer_list,
            name_column_name="LDPlayer Name",
            target_name=ld_name,
            update_column_name="Status",
            new_text=status
        )


    # ========= General Function on Dashboard ===========
    def on_search_accounts(self, text):
        self.account_proxy.set_search(text)
        self.detail_proxy.set_search(text)

    def on_add_category(self):
        category_name = self.ui.enter_category_line_edit.text().strip()
        if not category_name:
            Show_Message(
                self,
                "Warning",
                "Please enter a category name."
            )
            return
        if not self.data_manager.add_category(category_name):
            Show_Message(
                self,
                "Warning",
                f"Category '{category_name}' already exists."
            )
            return
        self.populate_category_combobox()
        self.ui.enter_category_line_edit.clear()
        Show_Message(
            self,
            "Success",
            "Category added successfully."
        )

    def on_delete_category(self):
        current_category = self.ui.category_filter_combobox.currentText()
        if current_category == "All":
            QMessageBox.warning(
                self,
                "Cannot Delete",
                "You cannot delete 'All'."
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{current_category}'?\n\n"
            "All accounts and pages will become Empty.",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        if not self.data_manager.delete_category(current_category):
            Show_Message(self, "Error", "Delete category failed.")
            return

        # Reload data first
        self.account_cache.reload()

        # Refresh models
        self.account_model.refresh()
        self.detail_model.refresh()

        # Rebuild category list
        self.populate_category_combobox()

        # Reset to All
        self.ui.category_filter_combobox.setCurrentText("All")

        # Reset every proxy that filters by category
        self.account_proxy.set_category("All")
        self.detail_proxy.set_category("All")

        Show_Message(
            self,
            "Success",
            "Category deleted successfully."
        )

    def refresh_tables(self):
        current_view = self.ui.switch_profile_page_combobox.currentText()
        if current_view == "Profile":
            QTimer.singleShot(
                0,
                self._refresh_profile_view
            )
        print("Print from refresh")

    def on_category_changed(self, category):
        self.account_proxy.set_category(category)
        self.detail_proxy.set_category(category)

        # Update label counts
        self.general_function.update_selection_label(
            self.ui.profile_table_accounts,
            self.ui.seleted_accounts
        )

    def on_search_accounts(self, text):
        self.account_proxy.set_search(text)
        self.detail_proxy.set_search(text)

    def _refresh_profile_view(self):

        self.ui.show_details.setCheckable(True)
        self.ui.stacked_accounts.setCurrentIndex(self._page_index)
        self.ui.show_details.setChecked(self._details_view_enabled)

        category = self.ui.category_filter_combobox.currentText()

        if getattr(self, "_last_category", None) != category:
            self._last_category = category
            self.account_proxy.set_category(category)
            self.detail_proxy.set_category(category)

        if self.account_cache.dirty:
            self.account_model.refresh()
            self.detail_model.refresh()
            self.account_cache.dirty = False

    def populate_category_combobox(self):
        all_categories = self.data_manager.get_all_categories()
        self.general_function.populate_combobox(
            combobox=self.ui.category_filter_combobox,
            data=all_categories,
            default_item="All"
        )

    def on_show_details_toggled(self, is_checked):
        self._details_view_enabled = is_checked
        page_index = 1 if is_checked else 0
        self._page_index = page_index

        
        change_stacked_widget_page(self.ui.stacked_accounts, page_index)

    def update_accounts_category_by_id(self, ids, category_name):

        self.update_multiple_accounts_ui(ids, save=True, category=category_name)

        Show_Message(
            self,
            "Success",
            "Assign Category Successfully"
        )

    def set_notes(self, ids: list):
        first_account_id = ids[0]
        account_data = self.account_cache.get_by_id(first_account_id)
        existing_note = account_data.get("notes", "")
        result, dialog = self.general_function.show_custom_dialog(
            SetNoteDialog,
            self,
            notes=existing_note
        )

        if not result:
            print("Dialog was cancelled.")
            return
        new_note = dialog.data["notes"]

        self.update_multiple_accounts_ui(ids, save=True, notes=new_note)

        Show_Message(
            self,
            "Success",
            "Note Updated Successfully"
        )

    def set_location(self, ids: list):
        first_account_id = ids[0]
        account_data = self.account_cache.get_by_id(first_account_id)

        existing_gps = account_data.get(
            "gps",
            {
                "enable": False,
                "lat": "",
                "long": ""
            }
        )

        result, dialog = self.general_function.show_custom_dialog(
            SetLocationDialog,
            self,
            gps_data=existing_gps
        )

        if not result:
            return

        saved_gps = dialog.data["gps"]



        self.update_multiple_accounts_ui(ids, save=True, 
            **{
                "gps.enable": saved_gps["enable"],
                "gps.lat": saved_gps["lat"],
                "gps.long": saved_gps["long"],
            })

        Show_Message(
            self,
            "Success",
            "GPS Updated Successfully"
        )

    def set_VPN(self, ids: list):
        if not ids:
            return

        first_account_id = ids[0]
        account_data = self.account_cache.get_by_id(first_account_id)

        existing_vpn = account_data.get(
            "vpn",
            {
                "enable": False,
                "name": None,
                "city": None
            }
        )

        # 🟢 Create the dialog (Assuming you pass the necessary managers)
        # dialog = SetVPNDialog(self, self.data_manager, self.general_function)
        dialog = self.main_window.set_vpn_dialog
        
        # 🟢 Pass the data into the dialog
        dialog.set_vpn_data_acc(existing_vpn)
        
        # 🟢 Use .exec() to wait for the user. QDialog.Accepted means they clicked Save.
        if dialog.exec() == QDialog.Accepted:
            saved_vpn = dialog.get_data()

            self.update_multiple_accounts_ui(ids, save=True, 
            **{
                "vpn.enable": saved_vpn["enable"],
                "vpn.name": saved_vpn["name"],
                "vpn.city": saved_vpn["city"],
            })


            Show_Message(self, "Success", "VPN Updated Successfully") 
        else:
            print("Set VPN dialog was cancelled.")

    def delete_multiple_accounts(self, ids):
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {len(ids)} selected account(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.Yes:
            return
        result = self.account_cache.remove(ids)
        if not result:
            Show_Message(
                self,
                "Error",
                "Nothing deleted."
            )

            return
        deleted_accounts, id_map = result
        for account in deleted_accounts:
            self.data_manager.delete_backup_folder(account)
        self.data_manager.remap_post_settings(
            id_map,
            ids
        )

        self.account_cache.save()

        self.account_model.refresh()
        self.detail_model.refresh()

        Show_Message(
            self,
            "Success",
            "Deleted successfully."
        )

    def current_selected_ids(self):
        current_page = self.general_function.get_current_page_name(self.ui.stacked_accounts)
        if current_page == "profile_table_widget":
            ids = self.general_function.get_selected_account_ids(self.ui.profile_table_accounts)
        else:
            ids = self.general_function.get_selected_account_ids(self.ui.profile_table_details_accounts)
        return ids

    def pop_up_set_up_post(self, acc_ids):
        if not acc_ids:
            return

        final_acc_ids = acc_ids.copy()

        # 1. If multiple accounts, force user to pick a reference account
        if len(acc_ids) > 1:
            result, dialog = self.general_function.show_custom_dialog(
                SelectAccountDialog, 
                parent=self, 
                acc_ids=acc_ids
            )
            
            if result == QDialog.Accepted and dialog.selected_id:
                selected_id = dialog.selected_id
                
                # Move selected ID to front so PostAccountDialog loads this one
                final_acc_ids.remove(selected_id)
                final_acc_ids.insert(0, selected_id)
            else:
                return # User cancelled

        # 2. Open the Post Dialog with the chosen list
        dialog = self.main_window.post_dialog
        dialog.selected_ids(final_acc_ids)
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()




    def validate_registration_setup(self):
        # 1. Validate LDPlayer Selection
        ld_selected = get_selected_rows_data(self.ui.ldplayer_list, "LDPlayer Name")
        if not ld_selected:
            Show_Message(self, "Error", "No LD Players selected.")
            return False, None, None

        # 2. Validate Loop Settings
        try:
            loops_per_ld = int(self.ld_manager.settings.get("loop", 1))
            if loops_per_ld < 1: raise ValueError
        except:
            Show_Message(self, "Error", "Invalid Loop count. Please set it to at least 1.")
            return False, None, None

        # 3. Validate 5SIM / Phone API Settings
        api_key = self.reg_tab_controller.settings.get("5sim_api", "")
        if not api_key:
            Show_Message(self, "Error", "5SIM API Key is missing in Settings!")
            return False, None, None

        # 4. Validate Phone Input Placeholders
        # Ensure at least one input is configured
        if not any([self.reg_tab_controller.settings.get("phone_input1"), 
                    self.reg_tab_controller.settings.get("phone_input2"), 
                    self.reg_tab_controller.settings.get("phone_input3")]):
            Show_Message(self, "Warning", "No Phone Input fields are configured. Registration might fail.")
            # Note: return False here if you want to force them to configure it
            
        return True, ld_selected, loops_per_ld

    # ======== Start ===========
    def on_start_clicked(self):
        # if not AppiumServerManager.is_running():
        #     AppiumServerManager.start_server()
    
        if not self.ld_manager.check_ld_path():
            Show_Message(self, "Error", "LD Player path not found.")
            return
        
        lds_names = get_selected_rows_data(self.ui.ldplayer_list, "LDPlayer Name")
        if not lds_names:
            Show_Message(self, "Error", "No LD Player selected.")
            return
        
        self.mode = get_selected_account_mode(self.ui)
        
        if self.mode == "active":
            ids = self.current_selected_ids()
            if not ids:
                Show_Message(self, "Error", "No Accounts Selected.")
                return
                
            # 🟢 NEW LOGIC: Match Emulators to Accounts
            if len(lds_names) > len(ids):
                print(f"⚠️ Selected {len(lds_names)} LDPlayers but only {len(ids)} Accounts. Reducing LDs to match.")
                lds_names = lds_names[:len(ids)] # Slices the list to only keep the exact amount needed
                
        else:
            is_valid, ld_selected, loops_per_ld = self.validate_registration_setup()
            if not is_valid:
                return
            
            total_targets = len(ld_selected) * loops_per_ld
            ids = [f"REG_{i+1}" for i in range(total_targets)]
            
            if total_targets <= 0:
                Show_Message(self, "Error", "No LDPlayers selected or loop count is 0.")
                return
            
        self.account_queue = queue.Queue()
        for acc_id in ids:
            self.account_queue.put(acc_id)
            self.stop_events[acc_id] = Event() 
            self._on_update_account(acc_id, False, {"status": "⏳ Waiting in Rank"})

        self.total_accounts = len(ids)
        self.completed_accounts = 0
        self.started_accounts = 0
        self._update_auto_ui_counter()

        self.tool_timer.start()

        # 2. Spawn a separate worker thread for EACH selected emulator
        self.active_workers = []
        for ld_name in lds_names:
            worker = EmulatorWorker(
                ld_name=ld_name,
                account_queue=self.account_queue,
                stop_events=self.stop_events,
                ld_manager=self.ld_manager,
                account_cache=self.account_cache,
                general_function=self.general_function,
                mode=self.mode,
                active_tab=self.active_tab_controller,
                reg_tab=self.reg_tab_controller
            )
            
            # Connect your UI signals
            worker.update_acc_signal.connect(self._on_update_account)
            worker.update_ld_signal.connect(self._update_ld_status)
            worker.account_finished_signal.connect(self._on_account_finished)
            worker.account_started_signal.connect(self._on_account_started)
            
            # Start the thread in your pool
            self.ld_executor.submit(worker.run)
            self.active_workers.append(worker)

    def _on_account_started(self, acc_id):
        """Fires when a worker officially pulls an account from the queue."""
        self.started_accounts += 1
        self._update_auto_ui_counter()

    def _on_account_finished(self, acc_id):
        """Fires when a worker finishes (success, fail, or skip)."""
        self.completed_accounts += 1
        self._update_auto_ui_counter()

    def _update_auto_ui_counter(self):
        """Calculates running vs finished and updates the UI text."""
        running = max(0, self.started_accounts - self.completed_accounts)
        
        if self.completed_accounts >= self.total_accounts:
            self.ui.runing_ld_counter.setText(f"All Finished: {self.completed_accounts}/{self.total_accounts}")
            self.tool_timer.stop() # Safely stop the timer when everything is 100% done
        else:
            self.ui.runing_ld_counter.setText(f"Running: {running} | Finished: {self.completed_accounts}/{self.total_accounts}")
    
    def on_stop_all_clicked(self):
        print("🛑 Initiating emergency stop for all workers...")
        self.tool_timer.stop()
        
        # 1. Tell all active workers to abort (stops them if they are still booting)
        for worker in self.active_workers:
            if hasattr(worker, 'stop'):
                worker.stop()

        # 2. Trigger the stop events for every account currently processing
        for acc_id, event in self.stop_events.items():
            event.set()
            
        # 3. Safely clear the queue and update math for skipped accounts
        if hasattr(self, 'account_queue'):
            with self.account_queue.mutex:
                current_queue_items = list(self.account_queue.queue)
                self.account_queue.queue.clear()
                
                for queued_id in current_queue_items:
                    self.account_queue.task_done()
                    self._on_account_finished(queued_id) 
        
        # 🟢 FIX: Do NOT call self.stop_events.clear() here! 
        # Active threads checking `stop_events[acc_id]` will crash with KeyError.
        # Just leave them set to True. They will naturally die.
        
        completed = getattr(self, 'completed_accounts', 0)
        total = getattr(self, 'total_accounts', 0)
        self.ui.runing_ld_counter.setText(f"Stopped : {completed}/{total}")
        
        Show_Message(self, "Success", "All emulator threads have been ordered to stop.")






    def start_accounts_manual(self, ids, actions=None):
        # 1. Get available LDPlayers
        ld_list = self.general_function.get_ldplayer_list(self.ui.ldplayer_path.text())
        available_lds = []
        for ld in ld_list[1:]:
            ld_name = ld["name"]
            if ld_name in self.ld_workers:
                continue 
                
            if self.ld_manager.is_ld_running(ld_name):
                print(f"⚠️ Skipping {ld_name}: It is already running outside the bot's control.")
                continue
            available_lds.append(ld_name)
            
        if not available_lds:
            Show_Message(self, "Warning", "No available/closed LD Players to start tasks!")
            return

        if actions is None:
            # If we have 10 accounts but only 3 LDs available, skip accounts from index 3 onwards
            if len(ids) > len(available_lds):
                skipped_accounts = ids[len(available_lds):]
                print(f"⚠️ skipped {len(skipped_accounts)} accounts due to insufficient available LDs for manual mode.")
                for skipped_id in skipped_accounts:
                    self.update_account_ui(int(skipped_id), status="❌ Skipped (No available LD)")
                
                # Keep only the accounts that fit into the available emulators
                ids = ids[:len(available_lds)]

        # 🟢 SETUP UI COUNTERS
        self.total_manual_accounts = len(ids)
        self.started_manual_accounts = 0
        self.completed_manual_accounts = 0 # 🟢 Ensure this resets to 0 when starting a new batch!
        self.ui.runing_ld_counter.setText(f"Progressing : 0/{self.total_manual_accounts}")

        # 2. Add the optimized/filtered IDs to the Queue
        for acc_id in ids:
            self.task_queue.put(acc_id)
            self.stop_events_manual[acc_id] = Event()
            self.update_account_ui(acc_id, status="⏳ Waiting")

        # 3. Start Workers
        threads_to_start = min(len(available_lds), self.task_queue.qsize())
        for i in range(threads_to_start):
            ld_name = available_lds[i]
            worker = EmulatorManualWorker(
                self.stop_events_manual, ld_name, self.task_queue, actions,
                self.ld_manager, self.account_cache, self.general_function, self.active_tab_controller
            )
            
            worker.update_acc_signal.connect(self._on_update_account)
            worker.update_ld_signal.connect(self._update_ld_status)
            worker.finished.connect(lambda name=ld_name: self.ld_workers.pop(name, None))
            
            worker.account_started_signal.connect(self._on_manual_account_started)
            worker.account_finished_signal.connect(self._on_manual_account_finished)
            
            self.ld_workers[ld_name] = worker
            worker.start()
            print(f"🚀 Started Worker on {ld_name}")

    def stop_accounts_manual(self, ids=None):
        if not ids:
            return
            
        target_ids = [int(x) for x in ids]
        
        # 1. REMOVE FROM QUEUE
        with self.task_queue.mutex:
            current_queue_items = list(self.task_queue.queue)
            self.task_queue.queue.clear()
            
            for queued_id in current_queue_items:
                if int(queued_id) in target_ids:
                    self.update_account_ui(queued_id, status="🛑 Stopped (Removed from Queue)")
                    
                    # 🟢 FIX: Simulate a 'start' so the running/finished math stays perfectly balanced!
                    self.started_manual_accounts += 1
                    
                    self._on_manual_account_finished(queued_id)
                else:
                    self.task_queue.queue.append(queued_id) 
                    
        # 2. STOP ACTIVE WORKERS SAFELY
        for ld_name, worker in list(self.ld_workers.items()):
            if worker.current_acc_id is not None and int(worker.current_acc_id) in target_ids:
                worker.stop() 
                self.update_account_ui(worker.current_acc_id, status="🛑 Stopping...")

    def _on_manual_account_started(self, acc_id):
        self.started_manual_accounts += 1
        self._update_ui_counter()

    def _on_manual_account_finished(self, acc_id):
        self.completed_manual_accounts += 1
        self._update_ui_counter()

    def _update_ui_counter(self):
        running = max(0, self.started_manual_accounts - self.completed_manual_accounts)
        
        if self.completed_manual_accounts >= self.total_manual_accounts:
            self.ui.runing_ld_counter.setText(f"All Finished: {self.completed_manual_accounts}/{self.total_manual_accounts}")
        else:
            self.ui.runing_ld_counter.setText(f"Running: {running} | Finished: {self.completed_manual_accounts}/{self.total_manual_accounts}")


    # ==== Check UID =========
    def check_live_by_uid(self, ids):
        bg_thread = threading.Thread(target=self._run_checker_in_background, args=(ids,), daemon=True)
        bg_thread.start()

    def _run_checker_in_background(self, ids):
        current_time = self.general_function.current_date_time()
        def check_single_account(acc_id):
            try:
                time.sleep(1)
                data_acc = self.account_cache.get_by_id(acc_id)
                if not data_acc:
                    self.update_account_ui(acc_id, False, status= "❌ Not Found")
                    return None

                uid = data_acc.get("uid")
                
                self.update_account_ui(acc_id, False, 
                    status= "🔍 Checking UID..."
                )
                status_detail = self.general_function.check_uid_live_status(uid, proxy=None)
                self.update_account_ui(acc_id, False, **{
                    "account_status": status_detail, 
                    "status": f"✅ Account Checked", 
                    "last_date": current_time
                })

                return acc_id
                
            except Exception as e:
                self.update_account_ui(acc_id, False, status= "❌ Thread Error")
                return None

        # Run Multithreading
        completed_ids = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(check_single_account, acc_id): acc_id for acc_id in ids}
            
            for future in concurrent.futures.as_completed(futures):
                result_id = future.result()
                if result_id is not None:
                    completed_ids.append(result_id)
                    
        self.update_finished_check_acc.emit(completed_ids)

    def _update_check_acc_finished(self, completed_ids: list):
        # This safely runs on the Main Thread and hits your hard drive ONCE.
        if completed_ids:
            self.account_cache.save_multiple_accounts(completed_ids)
            print(f"🎉 {len(completed_ids)} accounts physically saved to DB!")


    # ========= LDPlayer ============
    def load_ldplayer_settings(self):
        self.ui.ldplayer_path.setText(self.ld_manager.settings.get("ldplayer_path", ""))
        self.ui.delay_per_ld.setValue(int(self.ld_manager.settings.get("delay_per_ld", 0)))
        self.ui.ld_per_column.setValue(int(self.ld_manager.settings.get("ld_per_column", 0)))
        self.ui.ld_sleep.setValue(int(self.ld_manager.settings.get("ld_sleep", 0)))
        self.ui.loop.setValue(int(self.ld_manager.settings.get("loop", 0)))
        self.ui.ld_per_row.setValue(int(self.ld_manager.settings.get("ld_per_row", 0)))

        self.ui.active_accounts.setChecked(self.ld_manager.settings.get("active_accounts", False))
        self.ui.reg_accounts.setChecked(self.ld_manager.settings.get("reg_accounts", False))
        self.ui.auto_expand_fit_active.setChecked(self.ld_manager.settings.get("auto_expand_fit_active", False))
        self.ui.auto_arrange_ldplayer.setChecked(self.ld_manager.settings.get("auto_arrange_ldplayer", False))
        self.ui.run_schedule_checkbox.setChecked(self.ld_manager.settings.get("run_schedule_checkbox", False))
        self.ui.shop_tool_if_no_internet.setChecked(self.ld_manager.settings.get("shop_tool_if_no_internet", False))

    def save_ldplayer_settings(self):
        new_settings = {
            "ldplayer_path": self.ui.ldplayer_path.text(),
            "delay_per_ld": self.ui.delay_per_ld.value(),
            "ld_per_column": self.ui.ld_per_column.value(),
            "ld_sleep": self.ui.ld_sleep.value(),
            "loop": self.ui.loop.value(),
            "ld_per_row": self.ui.ld_per_row.value(),
            "active_accounts": self.ui.active_accounts.isChecked(),
            "reg_accounts": self.ui.reg_accounts.isChecked(),
            "auto_expand_fit_active": self.ui.auto_expand_fit_active.isChecked(),
            "auto_arrange_ldplayer": self.ui.auto_arrange_ldplayer.isChecked(),
            "run_schedule_checkbox": self.ui.run_schedule_checkbox.isChecked(),
            "shop_tool_if_no_internet": self.ui.shop_tool_if_no_internet.isChecked(),
        }

        self.data_manager.update_ldplayer_settings(new_settings)

    def browse_ldplayer_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select LDPlayer Folder")

        if folder:
            self.ui.ldplayer_path.setText(folder)
            self.data_manager.update_ldplayer_settings({"ldplayer_path": folder})
            print(f"LDPlayer path updated: {folder}")

    def refresh_ld_list(self):
        ld_list = self.general_function.get_ldplayer_list(self.ui.ldplayer_path.text())

        ld_header_map = {"LDPlayer Name": "name"}
        populate_table_by_header(self.ui.ldplayer_list, ld_header_map, ld_list)










