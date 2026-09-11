# app/tabs/reg_tab.py
# from ui.ui_main import Ui_MainWindow
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QInputDialog, QMessageBox
import time
import random
from datetime import datetime
from PySide6.QtCore import QMetaObject, Qt, Q_ARG
from core.utils import populate_table_by_header, get_selected_rows_data
from core.context_menus import show_table_reg_accounts_context_menu
from core.app_signals import signals
from core.five_sim_api import FiveSimAPI
import traceback
class RegTab(QWidget):
    def __init__(self, ui=None, parent=None, data_manager=None, ld_manager=None, general_function=None):
        super().__init__(parent)
        
        self._is_loading = True
        self.ui = ui
        self.data_manager = data_manager
        self.ld_manager = ld_manager          
        self.general_function = general_function


        self.settings = self.data_manager.get_reg_settings()

        api_token = self.settings.get("5sim_api", "")
        self.sim_api = FiveSimAPI(api_token)


        self.vpn_json_data = self.data_manager.get_vpn_data()


        # 🟢 CRITICAL ORDER FIX:
        self.setup_vpn_comboboxes()  # 1. Populate the VPN dropdown FIRST
        self._connect_signals()      # 2. Connect signals SECOND
        self.load_reg_settings()
        self.refresh_five_sim()

        
        self.refresh_reg_accounts()
        

        self._is_loading = False


    def refresh_five_sim(self):
        self.populate_5sim_countries()
        # Call the method
        self.ui.five_sim_username.setText("Loading...")
        result = self.sim_api.get_profile()
        
        if "error" in result:
            self.ui.five_sim_username.setText("Error")
            self.ui.five_sim_balance.setText("N/A")
            print(f"⚠️ {result['error']}")
        else:
            email = result.get("email", "Unknown")
            balance = result.get("balance", 0)
            self.ui.five_sim_username.setText(str(email))
            self.ui.five_sim_balance.setText(f"{balance} ₽")

    def populate_5sim_countries(self):
        
        self.ui.five_sim_country.clear() # Clear default UI items
        self.ui.five_sim_country.addItem("Loading countries...")

        result = self.sim_api.get_countries()
        
        self.ui.five_sim_country.clear() # Clear "Loading..." text
        
        if "error" in result:
            print(f"⚠️ Failed to load countries: {result['error']}")
            self.ui.five_sim_country.addItem("Error loading API")
            return

        # 1. Extract and format the data
        country_list = []
        for country_key, data in result.items():
            display_name = data.get("text_en", country_key.capitalize())
            country_list.append((display_name, country_key))

        country_list.sort(key=lambda x: x[0])

        for display_name, country_key in country_list:
            self.ui.five_sim_country.addItem(display_name, country_key)

        # 2. Restore the saved selection
        saved_country = self.settings.get("five_sim_country")
        
        if saved_country:
            # Attempt A: Search the hidden data (The new, correct way)
            index = self.ui.five_sim_country.findData(saved_country)
            
            # Attempt B: If it wasn't found (-1), search the visible text (Fallback for old saves)
            if index == -1:
                index = self.ui.five_sim_country.findText(saved_country)
            
            # 3. Apply the selection
            if index != -1:
                self.ui.five_sim_country.setCurrentIndex(index)



    def get_widget_text(self, widget):
        """Return text from either QLineEdit or QPlainTextEdit safely."""
        if hasattr(widget, "text"):
            return widget.text()
        elif hasattr(widget, "toPlainText"):
            return widget.toPlainText()
        return ""

    def set_widget_text(self, widget, value: str):
        """Set text for either QLineEdit or QPlainTextEdit safely."""
        if hasattr(widget, "setText"):
            widget.setText(value)
        elif hasattr(widget, "setPlainText"):
            widget.setPlainText(value)

    def _connect_signals(self):
        
        self.ui.name_path_btn.clicked.connect(lambda: self.browse_name_path())
        self.ui.profile_img_btn.clicked.connect(lambda: self.browse_profile_image())

        # Radio buttons
        self.ui.no_verify_radio.toggled.connect(lambda: self.save_reg_settings())
        self.ui.full_verify_radio.toggled.connect(lambda: self.save_reg_settings())
        self.ui.gender_male.toggled.connect(lambda: self.save_reg_settings())
        self.ui.gender_female.toggled.connect(lambda: self.save_reg_settings())
        self.ui.gender_random.toggled.connect(lambda: self.save_reg_settings())
        self.ui.five_sim.toggled.connect(lambda: self.save_reg_settings())
        self.ui.yandex.toggled.connect(lambda: self.save_reg_settings())
        self.ui.fixed_password.toggled.connect(lambda: self.save_reg_settings())
        self.ui.random_password.toggled.connect(lambda: self.save_reg_settings())

        # CheckBoxes
        self.ui.enable_vpn_checkbox.toggled.connect(lambda: self.save_reg_settings())
        self.ui.enable_fake_location_checkbox.toggled.connect(lambda: self.save_reg_settings())
        self.ui.upload_profile_checkbox.toggled.connect(lambda: self.save_reg_settings())

        # 🟢 NEW: Connect VPN comboboxes
        self.ui.vpn_combobox.currentTextChanged.connect(self.on_vpn_changed)
        self.ui.vpn_city.currentTextChanged.connect(lambda: self.save_reg_settings())
        self.ui.five_sim_country.currentTextChanged.connect(lambda: self.save_reg_settings())
        self.ui.time_zone.currentTextChanged.connect(lambda: self.save_reg_settings())

        # Inputs (Removed vpn_combobox and vpn_city from this list)
        inputs = [
            self.ui.fake_location_input,
            self.ui.five_sim_api,
            self.ui.phone_input1,
            self.ui.phone_input2,
            self.ui.phone_input3,
            self.ui.fake_phone_input1,
            self.ui.fake_phone_input2,
            self.ui.fake_phone_input3,
            self.ui.name_path_input,
            self.ui.profile_img_input,
            self.ui.fake_email,
            self.ui.yandex_mail_reg,
            self.ui.app_password_yandex_reg,
            self.ui.yandex_start_reg,
            self.ui.password_input1_reg,
            self.ui.password_input2_reg,
        ]
        
        for widget in inputs:
            if hasattr(widget, "textChanged"):
                widget.textChanged.connect(lambda: self.save_reg_settings())
            elif hasattr(widget, "currentIndexChanged"):
                widget.currentIndexChanged.connect(lambda: self.save_reg_settings())

        self.ui.accounts_reg_table.customContextMenuRequested.connect(
            lambda pos: show_table_reg_accounts_context_menu(self, self.ui.accounts_reg_table, pos, self.data_manager.get_all_categories())
        )
        self.ui.reload_reg_accounts.clicked.connect(lambda: self.refresh_reg_accounts())
        self.ui.refresh_five_sim_btn.clicked.connect(lambda: self.refresh_five_sim())
        self.ui.category_reg_accounts.currentTextChanged.connect(lambda: self.refresh_reg_accounts())

    def setup_vpn_comboboxes(self):
        self.ui.vpn_combobox.blockSignals(True)
        self.ui.vpn_combobox.clear()
        
        if isinstance(self.vpn_json_data, dict):
            self.ui.vpn_combobox.addItems(list(self.vpn_json_data.keys()))
            
        self.ui.vpn_combobox.setCurrentIndex(-1)
        self.ui.vpn_combobox.blockSignals(False)

    def on_vpn_changed(self, vpn_name):
        self.ui.vpn_city.blockSignals(True)
        self.ui.vpn_city.clear()
        
        if isinstance(self.vpn_json_data, dict):
            cities = self.vpn_json_data.get(vpn_name, [])
            if cities:
                self.ui.vpn_city.addItems(cities)
                
        self.ui.vpn_city.blockSignals(False)
        
        self.save_reg_settings()

    def load_reg_settings(self):
        

        # Radio buttons
        verify = self.settings.get("verify_type", "no_verify")
        self.ui.full_verify_radio.setChecked(verify == "full")
        self.ui.no_verify_radio.setChecked(verify != "full")
        self.ui.five_sim.setChecked(self.settings.get("five_sim", False))
        self.ui.yandex.setChecked(self.settings.get("yandex", False))
        self.ui.fixed_password.setChecked(self.settings.get("fixed_password", False))
        self.ui.random_password.setChecked(self.settings.get("random_password", False))


        gender = self.settings.get("gender", "random")
        self.ui.gender_male.setChecked(gender == "male")
        self.ui.gender_female.setChecked(gender == "female")
        self.ui.gender_random.setChecked(gender == "random")

        # Checkboxes
        self.ui.enable_vpn_checkbox.setChecked(self.settings.get("enable_vpn", False))
        self.ui.enable_fake_location_checkbox.setChecked(self.settings.get("enable_fake_location", False))
        self.ui.upload_profile_checkbox.setChecked(self.settings.get("upload_profile", False))

        # 🟢 FIX: Restore VPN and City Comboboxes safely using Index
        saved_vpn = self.settings.get("vpn", "")
        saved_city = self.settings.get("vpn_city", "")
        time_zone = self.settings.get("time_zone", "")

        if saved_vpn:
            index = self.ui.vpn_combobox.findText(saved_vpn)
            if index >= 0:
                self.ui.vpn_combobox.setCurrentIndex(index)
            
        if saved_city:
            index = self.ui.vpn_city.findText(saved_city)
            if index >= 0:
                self.ui.vpn_city.setCurrentIndex(index)

        if time_zone:
            index = self.ui.time_zone.findText(time_zone)
            if index >= 0:
                self.ui.time_zone.setCurrentIndex(index)

        # Inputs
        self.set_widget_text(self.ui.password_input1_reg, self.settings.get("password_input1_reg", ""))
        self.set_widget_text(self.ui.password_input2_reg, self.settings.get("password_input2_reg", ""))
        self.set_widget_text(self.ui.fake_location_input, self.settings.get("fake_location", ""))
        self.set_widget_text(self.ui.profile_img_input, self.settings.get("profile_image", ""))
        self.set_widget_text(self.ui.name_path_input, self.settings.get("name_path", ""))

        self.set_widget_text(self.ui.yandex_mail_reg, self.settings.get("yandex_mail_reg", ""))
        self.set_widget_text(self.ui.app_password_yandex_reg, self.settings.get("app_password_yandex_reg", ""))
        self.set_widget_text(self.ui.yandex_start_reg, self.settings.get("yandex_start_reg", ""))
        
        self.set_widget_text(self.ui.five_sim_api, self.settings.get("5sim_api", ""))
        self.set_widget_text(self.ui.phone_input1, self.settings.get("phone_input1", ""))
        self.set_widget_text(self.ui.phone_input2, self.settings.get("phone_input2", ""))
        self.set_widget_text(self.ui.phone_input3, self.settings.get("phone_input3", ""))
        self.set_widget_text(self.ui.fake_phone_input1, self.settings.get("fake_phone_input1", ""))
        self.set_widget_text(self.ui.fake_phone_input2, self.settings.get("fake_phone_input2", ""))
        self.set_widget_text(self.ui.fake_phone_input3, self.settings.get("fake_phone_input3", ""))
        self.set_widget_text(self.ui.fake_email, self.settings.get("fake_email", ""))

    def save_reg_settings(self):
        if getattr(self, "_is_loading", False):
            return

        self.settings = {
            "verify_type": "full" if self.ui.full_verify_radio.isChecked() else "no_verify",
            "gender": (
                "male" if self.ui.gender_male.isChecked()
                else "female" if self.ui.gender_female.isChecked()
                else "random"
            ),
            "enable_vpn": self.ui.enable_vpn_checkbox.isChecked(),
            "fixed_password": self.ui.fixed_password.isChecked(),
            "random_password": self.ui.random_password.isChecked(),
            "vpn": self.ui.vpn_combobox.currentText(),
            "vpn_city": self.ui.vpn_city.currentText(),
            "time_zone": self.ui.time_zone.currentText(),
            "enable_fake_location": self.ui.enable_fake_location_checkbox.isChecked(),
            "fake_location": self.get_widget_text(self.ui.fake_location_input),
            "upload_profile": self.ui.upload_profile_checkbox.isChecked(),
            "profile_image": self.get_widget_text(self.ui.profile_img_input),
            "name_path": self.get_widget_text(self.ui.name_path_input),
            "yandex": self.ui.yandex.isChecked(),
            "yandex_mail_reg": self.get_widget_text(self.ui.yandex_mail_reg),
            "app_password_yandex_reg": self.get_widget_text(self.ui.app_password_yandex_reg),
            "yandex_start_reg": self.get_widget_text(self.ui.yandex_start_reg),
            "five_sim": self.ui.five_sim.isChecked(),
            "5sim_api": self.get_widget_text(self.ui.five_sim_api),
            "five_sim_country": self.ui.five_sim_country.currentData(),
            "phone_input1": self.get_widget_text(self.ui.phone_input1),
            "phone_input2": self.get_widget_text(self.ui.phone_input2),
            "phone_input3": self.get_widget_text(self.ui.phone_input3),
            "fake_phone_input1": self.get_widget_text(self.ui.fake_phone_input1),
            "fake_phone_input2": self.get_widget_text(self.ui.fake_phone_input2),
            "fake_phone_input3": self.get_widget_text(self.ui.fake_phone_input3),
            "fake_email": self.get_widget_text(self.ui.fake_email),
            "password_input1_reg": self.get_widget_text(self.ui.password_input1_reg),
            "password_input2_reg": self.get_widget_text(self.ui.password_input2_reg)
        }

        self.data_manager.update_reg_settings(self.settings)

    def browse_name_path(self):
        # 🟢 CHANGED: Open a file dialog that specifically filters for .txt files
        file_path, _ = QFileDialog.getOpenFileName(
            None, 
            "Select Name TXT File", 
            "", 
            "Text Files (*.txt);;All Files (*)"
        )
        
        # If the user selected a file, update the UI input and save settings
        if file_path:
            self.ui.name_path_input.setText(file_path)
            self.save_reg_settings()

    def browse_profile_image(self):
        # Passing None removes the type error and lets PySide handle it cleanly
        folder = QFileDialog.getExistingDirectory(None, "Select Profile Image Folder")
        if folder:
            self.ui.profile_img_input.setText(folder)
            self.save_reg_settings()

    def get_gender(self):
        if self.ui.gender_male.isChecked():
            return "male"
        elif self.ui.gender_female.isChecked():
            return "female"
        else:
            return random.choice(["male", "female"])
    
    def generate_name(self):
        path = self.get_widget_text(self.ui.name_path_input)

        first_names = []
        last_names = []

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "|" not in line:
                    continue

                first, last = line.split("|", 1)
                first_names.append(first.strip())
                last_names.append(last.strip())

        firstname = random.choice(first_names)
        lastname = random.choice(last_names)

        return firstname, lastname

    def refresh_reg_accounts(self):

        # 2. Get and filter data
        selected_category = self.ui.category_reg_accounts.currentText()
        all_accounts = self.data_manager.get_all_regs()

        
        if selected_category == "All":
            filtered_accounts = all_accounts
        else:
            filtered_accounts = [acc for acc in all_accounts if acc.get("status") == selected_category]


        # 3️⃣ Define column header mapping (like your profile view)
        reg_header_map = {
            "ID": "id",
            "Name": "name",
            "UID": "uid",
            "Email": "email",
            "Phone Number": "phone_number",
            "Password": "password",
            "Fake GPS": "gps.enable",
            "Set Fake GPS": "gps.lat.long",
            "VPN": "vpn.enable",
            "Set VPN": "vpn.name",
            "Status": "status",
            "Model Name": "model",
            "Cookies": "cookies",
            "Date": "date_created",
        }

        # 4️⃣ Populate your Reg tab table
        populate_table_by_header(self.ui.accounts_reg_table, reg_header_map, filtered_accounts)




    def confirm_and_move_selected_accounts_reg(self):
        
        ids = get_selected_rows_data(self.ui.accounts_reg_table, "ID") 


        if not ids:
            QMessageBox.warning(self, "No Selection", "Please select one or more rows to move.")
            return


        message = f"Are you sure you want to move {len(ids)} selected account(s)?"

        reply = QMessageBox.question(
            self, "Confirm Deletion", message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:

            moved = self.data_manager.move_multiple_reg_to_main_accounts(ids)

            if moved:
                signals.accounts_changed.emit()

                self.refresh_reg_accounts()

    def confirm_and_delete_selected_accounts_reg(self):
        ids = get_selected_rows_data(self.ui.accounts_reg_table, "ID") # Assuming your header is named "UID"


        if not ids:
            QMessageBox.warning(self, "No Selection", "Please select one or more rows to delete.")
            return

        # Create a message based on how many items are selected
        message = f"Are you sure you want to delete {len(ids)} selected account(s)?"

        reply = QMessageBox.question(
            self, "Confirm Deletion", message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.data_manager.delete_multiple_reg_accounts(ids)
            self.refresh_reg_accounts()
    
    # Add data_device=None to the end
    def handle_save_new_registered_account(self, ld_name, backup_file_name, uid, data_device):
        current_date_str = self.general_function.current_date_time()
        sort_lat, sort_long = self.general_function.get_coordinates_from_ui(self.settings.get("fake_location", ""))
        
        # Fallback to empty dict if nothing is passed
        if data_device is None:
            data_device = {}

        new_account_data = {
            "name": "Mie Ky", # You can update this later when your bot scrapes the actual name
            "uid": uid,
            "phone_number": data_device.get("mobile_no", ""), 
            "cookies": "",
            "email": "sempanha@fastmail.com",
            "password": "SP-Farm123$",
            "verify_type": "full" if self.ui.full_verify_radio.isChecked() else "no_verify",
            "gps": {
                "enable": self.settings.get("enable_fake_location", ""),
                "lat": sort_lat,
                "long": sort_long,
            },
            "vpn": {
                "enable": self.settings.get("enable_vpn", ""),
                "name": self.settings.get("vpn", ""),
                "city": self.settings.get("vpn_city", "") # 🟢 Fixed hardcoded 'Paraguay'
            },
            "ld_name": ld_name,
            "status": "Live",
            "date_created": current_date_str,
            "last_date": current_date_str,
            "backup_file_name": backup_file_name,
            "time_zone": data_device.get("timezone", "")
        }

        # 🟢 Combine Data Automatically: Loop through all identity keys and add them!
        hardware_keys = [
            "imei", "manufacturer", "model", "market_name", "android_id", "mac", "imsi", "simid",
            "serial_number", "hardware", "board", "bootloader", "build_fingerprint", "meid",
            "gsf_id", "advertising_id", "bluetooth_mac", "wifi_ssid", "wifi_bssid",
            "network_generation", "esim_eid", "sim_operator", "sim_operator_name", "sim_country_iso"
        ]
        
        for key in hardware_keys:
            new_account_data[key] = data_device.get(key, "")

        self.data_manager.add_reg_account(new_account_data)
        self.refresh_reg_accounts()



    # =========================================================================
    # 🛠️ HELPER FUNCTIONS (Keeps the main loop clean!)
    # =========================================================================
    def _handle_fake_phone_input(self, bot, ld_name, acc_id, update_ld_signal, stop_event, initial_phone):
        """Loops phone input until Facebook accepts a number that isn't 'recently used'."""
        mobile_input_xpath = '//android.widget.EditText[@content-desc="Mobile Number"]'
        next_btn = '//*[@text="Next" or @content-desc="Next"]'
        error_xpath = '//android.view.View[@content-desc="The phone number you\'re trying to verify was recently used to verify a different account.  Please try a different number."]'
        password_screen_xpath = '//android.widget.EditText[contains(@content-desc, "Password")]'

        current_phone = initial_phone

        for attempt in range(10):
            if stop_event.is_set(): return False
            
            update_ld_signal.emit(ld_name, f"[{acc_id}] 📱 Entering Phone: {current_phone}")
            if bot.exists_xpath(mobile_input_xpath, timeout=5):
                bot.clear_xpath(mobile_input_xpath)
                bot.type_xpath(mobile_input_xpath, current_phone)
                bot.click_xpath(next_btn)
                
                # Check outcome: Did we get an error, or did we reach the Password screen?
                result = bot.wait_any([error_xpath, password_screen_xpath], timeout=8)
                
                if result == error_xpath:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Phone recently used. Generating new...")
                    p1 = self.settings.get("phone_input1", "")
                    p2 = self.settings.get("phone_input2", "")
                    p3 = self.settings.get("phone_input3", "")
                    current_phone = self.general_function.generate_random_phone(p1, p2, p3)
                    bot.wait(1)
                    continue
                elif result == password_screen_xpath:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Phone accepted!")
                    return current_phone # Return the successful phone number
                else:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Unknown state after entering phone.")
                    
        update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed to find a valid phone after 10 tries.")
        return False

    def _handle_password_creation(self, bot, ld_name, acc_id, update_ld_signal):
        """Generates and inputs a fixed or random password based on settings."""
        pwd_input_xpath = '//android.widget.EditText[@content-desc="Password,"] | //android.widget.EditText[contains(@content-desc, "Password")]'
        next_btn = '//*[@text="Next" or @content-desc="Next"]'

        # Generate Password
        p1 = self.settings.get("password_input1_reg", "")
        p2 = self.settings.get("password_input2_reg", "")
        
        if self.settings.get("random_password"):
            char_list = list(p2)
            random.shuffle(char_list)
            final_password = p1 + "".join(char_list)
        else:
            final_password = p1 + p2

        # Input Password
        if bot.exists_xpath(pwd_input_xpath, timeout=5):
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🔑 Entering Password...")
            bot.type_xpath(pwd_input_xpath, final_password)
            bot.click_xpath(next_btn)
            return final_password
            
        update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Password screen not found.")
        return False

    def _handle_save_and_agree(self, bot, ld_name, acc_id, update_ld_signal):
        """Clicks Save, clicks I Agree, and checks if Facebook blocked the account creation."""
        save_btn = '//android.view.View[@content-desc="Save"] | //android.widget.Button[@content-desc="Save"]'
        agree_btn = '//android.widget.Button[@content-desc="I agree"]'
        
        # 1. Click Save
        if bot.exists_xpath(save_btn, timeout=8):
            update_ld_signal.emit(ld_name, f"[{acc_id}] 💾 Clicking Save...")
            bot.click_xpath(save_btn)
            
        # 2. Click I Agree
        if bot.exists_xpath(agree_btn, timeout=8):
            update_ld_signal.emit(ld_name, f"[{acc_id}] 📜 Clicking I agree...")
            bot.click_xpath(agree_btn)
            
            # 3. Wait and check the account creation outcome
            update_ld_signal.emit(ld_name, f"[{acc_id}] ⏳ Waiting for account creation response...")
            bot.wait(6) 
            
            # 🟢 CHECK FOR THE BLOCK SCREEN: "We couldn’t create an account for you"
            block_error_xpath = '//*[contains(@text, "We couldn’t create an account") or contains(@content-desc, "We couldn’t create an account")]'
            ok_btn_xpath = '//android.widget.Button[@text="OK" or @content-desc="OK"]'
            
            if bot.exists_xpath(block_error_xpath, timeout=3):
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Facebook Blocked: 'We couldn’t create an account for you'.")
                
                # Click the "OK" button to clear the popup
                if bot.exists_xpath(ok_btn_xpath, timeout=2):
                    bot.click_xpath(ok_btn_xpath)
                    bot.wait(1)
                    
                return False # Returns False so the worker skips this account cleanly!
            
            # Check if still stuck on 'I agree'
            if bot.exists_xpath(agree_btn, timeout=2):
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Stuck on 'I agree'. Account creation blocked.")
                return False
                
            update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Passed 'I agree' screen!")
            return True
            
        update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ 'I agree' button not found.")
        return False

    # =========================================================================
    # 🚀 MAIN REGISTRATION FUNCTION
    # =========================================================================
    def Start_Reg(self, driver, bot, acc_id, ld_name, appium_name, update_ld_signal, stop_event, data_device, phone_number):
        try:



            uid = self.general_function.get_uid_in_background(appium_name)

            backup_folder_path = self.ld_manager.backup_full_device_with_identity(
                acc_id=acc_id,
                update_ld_signal=update_ld_signal, # Note: Made sure this uses the right argument name based on your earlier backup class
                ld_name=ld_name, 
                appium_name=appium_name,
                backup_name=None,
                output_dir="backups"
            )
            
            if backup_folder_path is None:
                return False
            
            # Save using the combined data_device dictionary
            self.handle_save_new_registered_account(ld_name, backup_folder_path, uid, data_device)

            return True






            self.ld_manager.factory_reset_user_apps(appium_name)
            
            if self.settings.get("enable_vpn"):
                vpn_success, msg = self.general_function.set_ravo_vpn(acc_id, ld_name, self.settings.get("vpn_city", ""), bot, update_ld_signal, stop_event)
                if not vpn_success:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed {msg}")
                    return False
                
            if stop_event.is_set(): return False
            
            # Master dictionary of ALL possible popups and onboarding buttons
            onboarding_elements = {
                'Get Started': '//android.widget.Button[@content-desc="Get started"]',
                'Create Account': '//android.widget.Button[@content-desc="Create new account"] | //android.view.view[@content-desc="Create new account"]',
                'Allow': (
                    '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"] | '
                    '//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_allow_button"] | '
                    '//android.widget.Button[contains(@text, "ALLOW") or contains(@text, "Allow")]'
                ),
                'Deny': (
                    '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_deny_button"] | '
                    '//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_deny_button"] | '
                    '//android.widget.Button[contains(@text, "DENY") or contains(@text, "Deny")]'
                ),
                'System Deny': '//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_deny_button"]',
                'Not Now / Skip': '//android.widget.TextView[@resource-id="android:id/button2"]'
            }
            next_btn = '//*[@text="Next" or @content-desc="Next"]'

            # ==========================================
            # 🚀 1. LAUNCH & REACH "NAME" SCREEN
            # ==========================================
            success, msg = bot.open_app("com.facebook.katana")
            success, msg = bot.open_app("com.facebook.lite")
            if not success:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed {msg}")
                return False
            
            first_name_xpath = '//android.widget.EditText[contains(@content-desc, "First name")]'
            last_name_xpath = '//android.widget.EditText[contains(@content-desc, "Last name")]'
            
            # 🟢 FIXED: Target ONLY the EditText for typing
            full_name_input_xpath = (
                '//android.widget.EditText[contains(@content-desc, "Full name")] | '
                "//android.widget.EditText[contains(@content-desc, \"What's your name\")]"
            )
            
            # This is just for checking if the screen exists (Views are okay here)
            full_name_screen_check = full_name_input_xpath + ' | //android.view.View[contains(@content-desc, "Full name")]'
            
            name_screen_reached = False
            is_full_name_mode = False
            
            for _ in range(10): 
                if stop_event.is_set(): return False
                
                # Check which version of the Name screen appeared
                if bot.exists_xpath(full_name_screen_check, timeout=1.5):
                    name_screen_reached = True
                    is_full_name_mode = True
                    break 
                elif bot.exists_xpath(first_name_xpath, timeout=1.5):
                    name_screen_reached = True
                    is_full_name_mode = False
                    break 
                
                # Check for random popups
                found_xpath = bot.wait_any(list(onboarding_elements.values()), timeout=1.5)
                if found_xpath:
                    element_name = next((name for name, xpath in onboarding_elements.items() if xpath == found_xpath), "Popup")
                    update_ld_signal.emit(ld_name, f"[{acc_id}] 🖱️ Found & Clicking: {element_name}")
                    bot.click_xpath(found_xpath)
                    bot.wait(1)

            if not name_screen_reached:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed to reach Name screen.")
                return False

            # ==========================================
            # 📝 2. SMART LOOP: INPUT NAME 
            # ==========================================
            mode_text = "Full Name" if is_full_name_mode else "First/Last Name"
            update_ld_signal.emit(ld_name, f"[{acc_id}] 📝 Entering Name ({mode_text} Mode)...")
            
            # 🟢 FIXED: Added the specific error Facebook throws when the box is left blank
            name_error_xpath = '//*[contains(@content-desc, "title or symbol") or contains(@text, "title or symbol") or contains(@text, "first and last name") or contains(@content-desc, "first and last name")]'
            
            pickers = [
                '//android.widget.LinearLayout[@resource-id="android:id/pickers"]/android.widget.NumberPicker[1]', 
                '//android.widget.LinearLayout[@resource-id="android:id/pickers"]/android.widget.NumberPicker[2]', 
                '//android.widget.LinearLayout[@resource-id="android:id/pickers"]/android.widget.NumberPicker[3]'  
            ]
            
            screen_reached = False
            
            for name_attempt in range(5):
                if stop_event.is_set(): return False
                    
                firstname, lastname = self.generate_name() 
                update_ld_signal.emit(ld_name, f"[{acc_id}] 📝 Typing Name: {firstname} {lastname} (Attempt {name_attempt + 1}/5)")
                
                typing_success = False
                for type_retry in range(4): 
                    try:
                        found_popup = bot.wait_any(list(onboarding_elements.values()), timeout=1)
                        if found_popup:
                            bot.click_xpath(found_popup)
                            bot.wait(1)

                        if is_full_name_mode:
                            if bot.exists_xpath(full_name_input_xpath, timeout=2):
                                # 🟢 FIXED: Click, Clear, and wait longer so React Native processes it
                                bot.click_xpath(full_name_input_xpath) 
                                bot.wait(1) 
                                bot.clear_xpath(full_name_input_xpath) 
                                bot.wait(0.5)
                                bot.type_xpath(full_name_input_xpath, f"{firstname} {lastname}")
                                bot.wait(1.5) # Give FB a second to register the typed text
                                
                                if bot.exists_xpath(next_btn, timeout=2):
                                    bot.click_xpath(next_btn)
                                typing_success = True
                                break
                        else:
                            if bot.exists_xpath(first_name_xpath, timeout=2):
                                bot.click_xpath(first_name_xpath)
                                bot.wait(0.5)
                                bot.clear_xpath(first_name_xpath)
                                bot.wait(0.5)
                                bot.type_xpath(first_name_xpath, firstname)
                                bot.wait(1)
                                
                                bot.click_xpath(last_name_xpath)
                                bot.wait(0.5)
                                bot.clear_xpath(last_name_xpath)
                                bot.wait(0.5)
                                bot.type_xpath(last_name_xpath, lastname)
                                bot.wait(1)
                                
                                if bot.exists_xpath(next_btn, timeout=2):
                                    bot.click_xpath(next_btn)
                                typing_success = True
                                break 
                            
                    except Exception as e:
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Popup interrupted typing! Retrying...")
                        bot.wait(0.6) 
                
                if not typing_success: continue 
                
                for wait_loop in range(4): 
                    if bot.exists_xpath(pickers[0], timeout=2):
                        screen_reached = True
                        break 
                    
                    if bot.exists_xpath(name_error_xpath, timeout=1):
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Name rejected or blank! Retrying...")
                        bot.wait(1)
                        break 
                        
                    found_popup = bot.wait_any(list(onboarding_elements.values()), timeout=1)
                    if found_popup:
                        bot.click_xpath(found_popup)
                        bot.wait(1)
                        continue
                        
                    is_stuck = bot.exists_xpath(full_name_screen_check, timeout=1) if is_full_name_mode else bot.exists_xpath(first_name_xpath, timeout=1)
                    if is_stuck:
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Stuck on Name screen. Clicking Next again...")
                        if bot.exists_xpath(next_btn, timeout=1):
                            bot.click_xpath(next_btn)
                            bot.wait(1)
                            
                if screen_reached: break 
                    
            if not screen_reached:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed to pass Name screen after 5 attempts.")
                return False
            # ==========================================
            # 🔄 3. SMART LOOP: REACH "BIRTHDAY" SCREEN & SET
            # ==========================================
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🔄 Navigating to Birthday Screen...")
            screen_reached = False
     
            for _ in range(4): 
                if bot.exists_xpath(pickers[0], timeout=10):
                    screen_reached = True
                    break 
                
                if _ > 0:
                    if bot.exists_xpath(first_name_xpath, timeout=1) or bot.exists_xpath(full_name_input_xpath, timeout=1):
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Stuck on Name screen. Clicking Next again...")
                        if bot.exists_xpath(next_btn, timeout=1):
                            bot.click_xpath(next_btn)
                            bot.wait(1)

                found_xpath = bot.wait_any(list(onboarding_elements.values()), timeout=2)
                if found_xpath:
                    bot.click_xpath(found_xpath)
                    bot.wait(1)
                    
            if not screen_reached:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed to reach Birthday screen.")
                return False

            update_ld_signal.emit(ld_name, f"[{acc_id}] 🎂 Setting Birthday...")
            bot.wait(1.5)
            
            try:
                bot.swipe_element(bot.find_xpath(pickers[0]), direction="up", times=random.randint(1, 4))
                bot.swipe_element(bot.find_xpath(pickers[1]), direction="down", times=random.randint(1, 4))
                bot.swipe_element(bot.find_xpath(pickers[2]), direction="down", times=random.randint(9, 11))
            except Exception as e:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Warning: Could not swipe all Birthday pickers. Skipping swipe...")
            
            if bot.exists_xpath('//android.widget.Button[@resource-id="android:id/button1"]', timeout=1):
                bot.click_xpath('//android.widget.Button[@resource-id="android:id/button1"]') 
            
            bot.click_xpath(next_btn)

            # ==========================================
            # 🚻 4. SMART LOOP: REACH & SELECT GENDER
            # ==========================================
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🔄 Waiting for Gender Screen...")
            
            gender = self.get_gender() # Assuming valid method in class
            target_gender = 'Male' if gender.lower() == 'male' else 'Female'
            gender_xpath = f'//android.widget.RadioButton[@content-desc="{target_gender}" or @text="{target_gender}"]'
            
            screen_reached = False
            
            for _ in range(4): 
                if bot.exists_xpath(gender_xpath, timeout=8):
                    screen_reached = True
                    break 
                
                if _ > 0:
                    if bot.exists_xpath(pickers[0], timeout=1): 
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Stuck on Birthday screen. Clicking Next...")
                        bot.click_xpath(next_btn)
                        bot.wait(1)

                found_xpath = bot.wait_any(list(onboarding_elements.values()), timeout=2)
                if found_xpath:
                    bot.click_xpath(found_xpath)
                    bot.wait(1)
                    
            if not screen_reached:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed to reach Gender screen.")
                return False

            update_ld_signal.emit(ld_name, f"[{acc_id}] 🚻 Selecting Gender...")
            bot.click_xpath(gender_xpath)
            
            if bot.exists_xpath(next_btn, timeout=3):
                bot.click_xpath(next_btn)
            else:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ 'Next' button missing on Gender screen.")
                return False

            # ==========================================
            # ⚙️ 5. BRANCHING WORKFLOWS (5sim vs Yandex)
            # ==========================================
            if self.settings.get("five_sim"):
                # ==========================================
                # 📱 5SIM INTEGRATION
                # ==========================================
                max_retries = 4
                order_id = None
                number_accepted = False

                for attempt in range(max_retries):
                    if stop_event.is_set(): return False
                    
                    update_ld_signal.emit(ld_name, f"[{acc_id}] 🛒 Buying number (Attempt {attempt + 1}/{max_retries})...")
                    
                    target_country = self.settings.get("five_sim_country", "any")
                    order_data = self.sim_api.buy_number(country=target_country, operator="any", product="facebook")
                    
                    if "error" in order_data:
                        error_msg = order_data["error"] 
                        if "not enough user balance" in str(error_msg).lower():
                            update_ld_signal.emit(ld_name, f"[{acc_id}] 🛑 Not enough user balance on 5sim")
                            return False 
                        
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ 5sim Error: {error_msg}")
                        bot.wait(5)
                        continue 

                    order_id = order_data.get("id")
                    phone_number = order_data.get("phone")
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Got Number: {phone_number}")

                    update_ld_signal.emit(ld_name, f"[{acc_id}] 📱 Entering Phone Number...")
                    if bot.exists_xpath('//android.widget.EditText[@content-desc="Mobile Number"]', timeout=5):
                        bot.type_xpath('//android.widget.EditText[@content-desc="Mobile Number"]', phone_number)
                        bot.click_xpath('//android.widget.Button[@content-desc="Next"]')
                        bot.wait(3)
                    else:
                        self.sim_api.cancel_order(order_id)
                        continue

                    update_ld_signal.emit(ld_name, f"[{acc_id}] 🔎 Checking if Facebook accepts the number...")
                    error_msg = bot.wait_any([
                        "//*[contains(@content-desc, 'recently used')]",
                        "//*[contains(@content-desc, 'invalid')]",
                        "//*[@text='Enter the mobile number where you can be contacted. No one will see this on your profile.']"
                    ], timeout=10)

                    if error_msg:
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Number blocked. Refunding and retrying...")
                        self.sim_api.cancel_order(order_id)
                        order_id = None 
                        bot.wait(2)
                        continue 
                    else:
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Number accepted!")
                        number_accepted = True
                        break 

                if not number_accepted:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed to get a valid number after 4 attempts.")
                    return False

                # WAIT FOR SMS & ENTER CODE
                update_ld_signal.emit(ld_name, f"[{acc_id}] ⏳ Waiting for SMS code from 5sim...")
                
                sms_code = None
                max_wait_time = 180 
                start_time = time.time()
                
                while time.time() - start_time < max_wait_time:
                    if stop_event.is_set():
                        update_ld_signal.emit(ld_name, f"[{acc_id}] 🛑 Cancelled. Refunding number...")
                        self.sim_api.cancel_order(order_id)
                        return False
                        
                    check_result = self.sim_api.check_sms(order_id)
                    
                    if "sms" in check_result and len(check_result["sms"]) > 0:
                        sms_code = check_result["sms"][0]["code"]
                        break 
                        
                    bot.wait(5)
                    
                if not sms_code:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ SMS Timeout. Refunding number...")
                    self.sim_api.cancel_order(order_id) 
                    return False
                    
                update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Got SMS Code: {sms_code}")

                if bot.exists_xpath('//android.widget.EditText[contains(@content-desc, "Code")]', timeout=5):
                    bot.type_xpath('//android.widget.EditText[contains(@content-desc, "Code")]', sms_code)
                    bot.click_xpath('//android.widget.Button[@content-desc="Next"]')
                    self.sim_api.finish_order(order_id)
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ SMS accepted, 5sim order finished!")
                else:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Could not find SMS input field.")
                    return False

            elif self.settings.get("yandex"):
                # ==========================================
                # 📱 YANDEX MODE (Fake Phone Loop -> Pwd -> Save)
                # ==========================================
                
                # 1. LOOP FAKE PHONE INPUT
                accepted_phone = self._handle_fake_phone_input(bot, ld_name, acc_id, update_ld_signal, stop_event, phone_number)
                if not accepted_phone:
                    return False
                data_device["phone_number"] = accepted_phone

                # 2. CREATE AND INPUT PASSWORD
                created_password = self._handle_password_creation(bot, ld_name, acc_id, update_ld_signal)
                if not created_password:
                    return False
                data_device["password"] = created_password

                # 3. SAVE AND AGREE TO TERMS
                agree_success = self._handle_save_and_agree(bot, ld_name, acc_id, update_ld_signal)
                if not agree_success:
                    return False

                # 4. FETCH YANDEX VERIFICATION CODE
                update_ld_signal.emit(ld_name, f"[{acc_id}] 📧 Fetching Yandex Code...")
                email_address = self.settings.get("yandex_mail_reg")
                app_password = self.settings.get("app_password_yandex_reg")
                new_email = self.data_manager.get_next_tracking_email(self.settings.get("yandex_start_reg"))
                
                yandex_code = self.general_function.get_yandex_code(email_address, app_password)
                
                if yandex_code:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Got Yandex Code: {yandex_code}")
                    # ========================================
                    # TODO: ADD BOT LOGIC HERE to input the Yandex Code on the verification screen!
                    # Example: bot.type_xpath('//android.widget.EditText...', yandex_code)
                    # ========================================
                else:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed to get Yandex code.")
                    return False

            # ==========================================
            # 💾 9. FINAL BACKUP & SAVE DATA
            # ==========================================
            uid = self.general_function.get_uid_in_background(appium_name)

            backup_folder_path = self.ld_manager.backup_full_device_with_identity(
                acc_id=acc_id,
                update_ld_signal=update_ld_signal, # Note: Made sure this uses the right argument name based on your earlier backup class
                ld_name=ld_name, 
                appium_name=appium_name,
                backup_name=None,
                output_dir="backups"
            )
            
            if backup_folder_path is None:
                return False
            
            # Save using the combined data_device dictionary
            self.handle_save_new_registered_account(ld_name, backup_folder_path, uid, data_device)
                
            return True
            
        except Exception as e:
            full_error = traceback.format_exc()
            print("\n==================================================")
            print(f"🔥 CRITICAL AUTOMATION CRASH ON ACCOUNT {acc_id}")
            print("==================================================")
            print(full_error)
            print("==================================================\n")
            print(f"❌ Registration Automation Error: {e}")
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Critical Registration Crash: {str(e)[:30]}")
            return False