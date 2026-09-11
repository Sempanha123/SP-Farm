# core/data_manager.py
import json
import os
import random
import shutil
import re
import sys
class DataManager:
    def __init__(self):
        
        # File paths
        accounts_file = 'accounts.json'
        categories_file = 'categories.json'
        pages_file = 'pages.json'
        ldplayer_file = 'ldplayer.json'
        reg_file = 'reg_settings.json'
        active_settings = 'active_settings.json'
        accounts_reg_file = 'account_reg.json'
        post_setting = 'post_setting.json'
        vpn = 'vpn.json'
        email_tracking = 'email_tracking.json'
        groups_file = 'groups.json'

        
        self.files = {
            "accounts": accounts_file,
            "categories": categories_file,
            "pages": pages_file,
            "ldplayer": ldplayer_file,
            "reg_setting": reg_file,
            "accounts_reg": accounts_reg_file,
            "active_settings": active_settings,
            "post_setting": post_setting,
            "vpn": vpn,
            "email_tracking": email_tracking,
            "groups": groups_file,
        }


        # RAM cache
        self._cache = {}
        # self._ensure_sequential_ids("accounts")
        # self._ensure_sequential_ids("pages")
        # self._ensure_sequential_ids("accounts_reg")


        self.post_setting_datas = self._load_json("post_setting", [])


    def _load_json(self, key, default_data, force_reload=False):
        if not force_reload and key in self._cache:
            return self._cache[key]
        filename = self.files[key]
        if not os.path.exists(filename):
            self._cache[key] = default_data
            return default_data
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(default_data, dict) and isinstance(data, dict):
                data = {**default_data, **data}

            self._cache[key] = data

            return data

        except (json.JSONDecodeError, IOError):

            self._cache[key] = default_data

            return default_data

    def _save_json_data(self, key, computational_data):
        self._cache[key] = computational_data
        filename = self.files[key]

        # 🟢 Double check: Ensure we aren't saving empty structures by mistake
        if not computational_data:
            print(f"⚠️ Warning: Attempted to save empty data for key: {key}")

        # Always force UTF-8 and disable ASCII escaping for Khmer script
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(computational_data, f, indent=4, ensure_ascii=False)

    def get_all_accounts(self, force_reload=False):
        return self._load_json(
            "accounts",
            [],
            force_reload
        )

    def get_all_categories(self, force_reload=False):
        return self._load_json(
            "categories",
            [],
            force_reload
        )

    def get_all_regs(self, force_reload=False):
        return self._load_json(
            "accounts_reg",
            [],
            force_reload
        )

    def _ensure_sequential_ids(self, key):
        items = self._load_json(key, [])
        if not isinstance(items, list):
            return
            
        needs_saving = False
        for index, item in enumerate(items):
            new_id = str(index + 1)
            if item.get("id") != new_id:
                item["id"] = new_id
                needs_saving = True
        if needs_saving:
            self._save_json_data(key, items)

    def save_all_accounts(self, accounts):
        self._save_json_data("accounts", accounts)

    def remap_post_settings(self, id_map, deleted_ids):
        post_settings = self._load_json("post_setting", [])
        deleted_ids = {str(i) for i in deleted_ids}
        new_data = []
        for item in post_settings:
            old = str(item["id"])
            if old in deleted_ids:
                continue
            if old in id_map:
                item["id"] = id_map[old]
            new_data.append(item)
        self._save_json_data(
            "post_setting",
            new_data
        )

    def delete_backup_folder(self, account):
        backup = account.get("backup_file_name")
        if not backup:
            return
        if not os.path.isdir(backup):
            return
        try:
            shutil.rmtree(backup)
            print(f"Deleted backup: {backup}")
        except Exception as e:
            print(e)

    def save_all_categories(self, categories):
        self._save_json_data("categories", categories)

    def add_category(self, category_name: str) -> bool:
        category_name = " ".join(category_name.split())
        if not category_name:
            return False
        categories = self._load_json("categories", [])
        lower_names = {
            c.casefold()
            for c in categories
        }
        if category_name.casefold() in lower_names:
            return False
        categories.append(category_name)
        categories.sort(key=str.casefold)
        self._save_json_data(
            "categories",
            categories
        )

        return True

    def delete_category(self, category_name):

        categories = self._load_json("categories", [])
        accounts = self._load_json("accounts", [])

        if category_name not in categories:
            return False

        categories.remove(category_name)

        for account in accounts:
            if account.get("category") == category_name:
                account["category"] = None

        self._save_json_data("categories", categories)
        self._save_json_data("accounts", accounts)

        return True

    def update_single_account(self, account_data: dict) -> bool:
        account_id = str(account_data.get("id"))
        if not account_id or account_id == "None":
            return False
            
        # 1. Load the current accounts from cache
        accounts = self.get_all_accounts()
        
        updated = False
        # 2. Find the specific account and replace it
        for i, acc in enumerate(accounts):
            if str(acc.get("id")) == account_id:
                # Replace the old dictionary with the newly updated one
                accounts[i] = account_data
                updated = True
                break
                
        # 3. Save the file if a change was actually made
        if updated:
            self.save_all_accounts(accounts)
            return True
            
        return False

    def update_multiple_accounts(self, updated_accounts_list: list) -> bool:
        if not updated_accounts_list:
            return False
            
        # Create a fast-lookup dictionary { "1": {account_data}, "2": {account_data} }
        updates_map = {str(acc.get("id")): acc for acc in updated_accounts_list if acc.get("id")}
        
        # 1. Load the current accounts from cache
        accounts = self.get_all_accounts()
        
        updated = False
        # 2. Find and replace all matching accounts in one loop
        for i, acc in enumerate(accounts):
            acc_id = str(acc.get("id"))
            if acc_id in updates_map:
                accounts[i] = updates_map[acc_id]
                updated = True
                
        # 3. Save the file exactly ONCE
        if updated:
            self.save_all_accounts(accounts)
            return True
            
        return False

    # --- LDPlayer ---
    def get_ldplayer_settings(self):
        return self._load_json("ldplayer", [])

    def update_ldplayer_settings(self, new_data: dict):
        settings = self._load_json("ldplayer", [])
        settings.update(new_data)
        self._save_json_data("ldplayer", settings)

    # --- Accounts Registration (account_reg.json) ---
    def get_reg_settings(self):
        reg_data = self._load_json("reg_setting", {})
        if not isinstance(reg_data, dict):
            reg_data = {}
        return reg_data

    def update_reg_settings(self, new_settings: dict):
        reg_data = self._load_json("reg_setting", {})
        reg_data.update(new_settings)
        self._save_json_data("reg_setting", reg_data)

    def get_all_regs(self):
        return self._load_json("accounts_reg", [])
    
    def add_reg_account(self, account_dict: dict):
        accounts_reg = self._load_json("accounts_reg", [])
        if not isinstance(accounts_reg, list):
            accounts_reg = []

        next_id = str(len(accounts_reg) + 1)
        account_dict["id"] = next_id

        accounts_reg.append(account_dict)
        self._save_json_data("accounts_reg", accounts_reg)
        # print(f"✅ Added registration account ID '{next_id}' safely.")
        return next_id

    def update_reg_account_by_id(self, account_id, updated_fields: dict):
        accounts_reg = self._load_json("accounts_reg", [])
        for account in accounts_reg:
            if str(account.get("id")) == str(account_id):
                account.update(updated_fields)
                self._save_json_data("accounts_reg", accounts_reg)
                print(f"✅ Registration Account ID '{account_id}' updated successfully.")
                return True
        print(f"⚠️ Error: Registration Account ID '{account_id}' not found.")
        return False

    def delete_multiple_reg_accounts(self, id_list):

        str_id_list = [str(x) for x in id_list]
        accounts_reg = self._load_json("accounts_reg", [])
        initial_length = len(accounts_reg)

        # =============================================================
        # 🟢 STEP 1: FIND EACH ID AND REMOVE ITS BACKUP FOLDER
        # =============================================================
        for target_id in str_id_list:
            # Locate the account dictionary within the freshly loaded registration pool
            data_acc = None
            for acc in accounts_reg:
                if str(acc.get("id")) == target_id:
                    data_acc = acc
                    break
            
            if data_acc and isinstance(data_acc, dict):
                backup_path = data_acc.get("backup_file_name")
                
                # Verify that the backup path string contains text data
                if backup_path and str(backup_path).strip():
                    target_folder = str(backup_path).strip()
                    
                    # If the folder physically exists on the drive, wipe it completely
                    if os.path.exists(target_folder):
                        try:
                            shutil.rmtree(target_folder)
                            print(f"🧹 Cleaned up registration backup directory: {target_folder}")
                        except Exception as e:
                            print(f"⚠️ Warning: Could not delete directory folder {target_folder}: {e}")
                    else:
                        # 🟢 Automatically skips without crashing if the folder isn't found
                        pass

        # =============================================================
        # 🟢 STEP 2: REMOVE POOL ENTRIES AND CONSOLIDATE IDS
        # =============================================================
        accounts_reg = [acc for acc in accounts_reg if str(acc.get("id")) not in str_id_list]

        if len(accounts_reg) < initial_length:
            # Write updated dataset straight back to account_reg.json
            self._save_json_data("accounts_reg", accounts_reg)
            
            # Re-index remaining accounts sequentially to guarantee uniform UI lists
            self._ensure_sequential_ids("accounts_reg")
            
            print(f"🗑️ Bulk deleted {initial_length - len(accounts_reg)} registration accounts successfully.")
            return True
            
        return False

    def move_multiple_reg_to_main_accounts(self, ids_to_move):
        ids = {str(i) for i in ids_to_move}

        accounts = self._load_json("accounts", [])
        accounts_reg = self._load_json("accounts_reg", [])

        moved = []
        remaining = []

        for reg in accounts_reg:

            reg_id = str(reg.get("id", ""))
            uid = str(reg.get("uid", ""))

            if reg_id not in ids and uid not in ids:
                remaining.append(reg)
                continue

            moved.append({
                "id": "",
                "name": reg.get("name", ""),
                "uid": reg.get("uid", ""),
                "phone_number": reg.get("phone_number", ""),
                "cookies": reg.get("cookies", ""),
                "email": reg.get("email", ""),
                "password": reg.get("password", ""),
                "category": reg.get("category", ""),
                "page": int(reg.get("page", 0)),
                "friends": int(reg.get("friends", 0)),
                "page_ids": reg.get("page_ids", []),
                "notes": reg.get("notes", ""),
                "status": reg.get("status", ""),
                "gps": dict(reg.get("gps", {})),
                "vpn": dict(reg.get("vpn", {})),
                "imei": reg.get("imei", ""),
                "manufacturer": reg.get("manufacturer", ""),
                "model": reg.get("model", ""),
                "market_name": reg.get("market_name", ""),
                "android_id": reg.get("android_id", ""),
                "mac": reg.get("mac", ""),
                "imsi": reg.get("imsi", ""),
                "simid": reg.get("simid", ""),
                "serial_number": reg.get("serial_number", ""),
                "hardware": reg.get("hardware", ""),
                "board": reg.get("board", ""),
                "bootloader": reg.get("bootloader", ""),
                "build_fingerprint": reg.get("build_fingerprint", ""),
                "meid": reg.get("meid", ""),
                "gsf_id": reg.get("gsf_id", ""),
                "advertising_id": reg.get("advertising_id", ""),
                "bluetooth_mac": reg.get("bluetooth_mac", ""),
                "wifi_ssid": reg.get("wifi_ssid", ""),
                "wifi_bssid": reg.get("wifi_bssid", ""),
                "network_generation": reg.get("network_generation", "13"),
                "esim_eid": reg.get("esim_eid", ""),
                "sim_operator": reg.get("sim_operator", ""),
                "sim_operator_name": reg.get("sim_operator_name", ""),
                "sim_country_iso": reg.get("sim_country_iso", ""),
                "time_zone": reg.get("time_zone", ""),
                "date_created": reg.get("date_created", ""),
                "last_date": reg.get("last_date", ""),    # 🟢 FIXED
                "backup_file_name": reg.get("backup_file_name", ""),
            })

        if not moved:
            return 0

        accounts.extend(moved)

        # Re-index accounts
        for i, account in enumerate(accounts, start=1):
            account["id"] = str(i)

        # Re-index registration accounts
        for i, account in enumerate(remaining, start=1):
            account["id"] = str(i)

        self._save_json_data("accounts", accounts)
        self._save_json_data("accounts_reg", remaining)


        return len(moved)


    # ======= Group ==========
    def save_groups(self, acc_id, groups_list):
        all_groups = self._load_json("groups", {})
        all_groups[str(acc_id)] = groups_list
        self._save_json_data("groups", all_groups)


    # ========== Active Accounts ===============
    def update_active_settings(self, new_settings: dict):
        active_settings_data = self._load_json("active_settings", {})
        active_settings_data.update(new_settings)
        self._save_json_data("active_settings", active_settings_data)

    def get_active_settings(self):
        return self._load_json("active_settings", [])
    


    # ============= Post Setting ====================
    def update_post_settings(self, ids, new_settings: dict):
        # self.post_setting_datas = self._load_json("post_setting", [])

        # if not isinstance(self.post_setting_datas, list):
        #     self.post_setting_datas = []

        # Convert to strings for safe comparison
        ids = [str(x) for x in ids]

        for target_id in ids:

            found = False

            # Update existing ID
            for item in self.post_setting_datas:

                if str(item.get("id")) == target_id:

                    item.update(new_settings)
                    found = True
                    break

            # Create new ID if not found
            if not found:

                new_item = {
                    "id": target_id,
                    **new_settings
                }

                self.post_setting_datas.append(new_item)

        # Save everything back
        self._save_json_data(
            "post_setting",
            self.post_setting_datas
        )

        # print(f"✅ Updated post settings for IDs: {ids}")

        return True

    def get_post_setting_by_id(self, account_id):
        for item in self.post_setting_datas:
            if str(item.get("id")) == str(account_id):
                return item
        return {}



    # ======== VPN ==================
    def get_vpn_data(self):
        vpn_path = self.files.get("vpn")
        if vpn_path and os.path.exists(vpn_path):
            with open(vpn_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}



    #========= Yandex ===============
    def get_next_tracking_email(self, base_email):
        """
        Reads the highest used tracking number, increments it by 1, 
        and safely handles malformed JSON files. 
        Supports jumping forward if a higher number is passed in the email string.
        """
        self.tracking_yandex = self._load_json("email_tracking", [])
        
        # 🟢 CRITICAL FIX 1: Ensure JSON is a list
        if isinstance(self.tracking_yandex, dict):
            self.tracking_yandex = [self.tracking_yandex]
        elif not isinstance(self.tracking_yandex, list):
            self.tracking_yandex = []
            
        if not base_email:
            return ""

        # Clean the email and extract the number (if any)
        match = re.match(r'^([^@+]+)(?:\+(\d+))?(@.+)$', base_email.strip())
        if not match:
            return base_email 
            
        prefix = match.group(1)  # 'sempanha02'
        passed_num_str = match.group(2)  # '10' (or None if no number was passed)
        domain = match.group(3)  # '@yandex.com'
        
        clean_base = f"{prefix}{domain}" # 'sempanha02@yandex.com'

        # 🟢 NEW: Convert the passed string number to an integer (default to 0 if none)
        passed_num = int(passed_num_str) if passed_num_str else 0

        found = False
        next_num = 1
        
        for entry in self.tracking_yandex:
            if isinstance(entry, dict):
                
                if entry.get("yandex_acc") == clean_base or entry.get("yandex_acc") == prefix:
                    # Get the number currently saved in the JSON
                    json_num = int(entry.get("yandex_unique", "0"))
                    
                    # 🟢 THE MAGIC UPGRADE: Take the highest of the two numbers!
                    highest_known_num = max(json_num, passed_num)
                    
                    # Increment by 1
                    next_num = highest_known_num + 1
                    
                    # Update the JSON memory
                    entry["yandex_unique"] = str(next_num)
                    entry["yandex_acc"] = clean_base 
                    
                    found = True
                    break
                
        # If this email has never been seen in the JSON before
        if not found:
            highest_known_num = passed_num
            next_num = highest_known_num + 1
            
            self.tracking_yandex.append({
                "yandex_acc": clean_base,
                "yandex_unique": str(next_num)
            })
            
        # Save the updated data back to your JSON file
        self._save_json_data("email_tracking", self.tracking_yandex)
        
        return f"{prefix}+{next_num}{domain}"