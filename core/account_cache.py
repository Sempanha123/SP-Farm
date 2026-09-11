from core.utils import get_time_ago

class AccountCache:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.accounts = []
        self.account_index = {} # id -> account dict
        self.row_index = {}     # id -> row
        self.dirty = False

    # -------------------------------------------------------
    # Load / Save
    # -------------------------------------------------------

    def load(self, force_reload=False):
        self.accounts = self.data_manager.get_all_accounts(force_reload=force_reload)
        self._refresh_time_ago_batch()
        self._build_index()
        self.dirty = False

    def reload(self):
        self.accounts = self.data_manager.get_all_accounts(force_reload=True)
        self._refresh_time_ago_batch()
        self._build_index()

    def save(self):
        if not self.dirty:
            return
        
        self.data_manager.save_all_accounts(self.accounts)
        self.dirty = False

    def save_single_account(self, account_id):
        account_data = self.get_by_id(account_id)
        if not account_data:
            return

        if hasattr(self.data_manager, 'update_single_account'):
            self.data_manager.update_single_account(account_data)
        else:
            # ⚠️ Failsafe Fallback: If the method doesn't exist, it safely saves everything.
            self.data_manager.save_all_accounts(self.accounts)
            self.dirty = False

    def save_multiple_accounts(self, account_ids: list):
        accounts_to_save = []
        for aid in account_ids:
            acc = self.get_by_id(aid)
            if acc:
                accounts_to_save.append(acc)

        if not accounts_to_save:
            return


        if hasattr(self.data_manager, 'update_multiple_accounts'):
            self.data_manager.update_multiple_accounts(accounts_to_save)
        else:
            self.data_manager.save_all_accounts(self.accounts)
            self.dirty = False


    def replace(self, accounts):
        self.accounts = list(accounts)
        self._build_index()
        self.dirty = False

    def clear(self):
        self.accounts.clear()
        self.account_index.clear()
        self.row_index.clear()
        self.dirty = False
    
    def insert(self, account):
        self.accounts.append(account)
        aid = str(account.get("id"))
        self.account_index[aid] = account
        self.row_index[aid] = len(self.accounts) - 1
        self.dirty = True

    # -------------------------------------------------------
    # Basic
    # -------------------------------------------------------

    def all(self):
        return self.accounts

    def count(self):
        return len(self.accounts)

    def get(self, row):
        if 0 <= row < len(self.accounts):
            return self.accounts[row]
        return None

    def row(self, account_id):
        return self.row_index.get(str(account_id), -1)

    def contains(self, account_id):
        return str(account_id) in self.account_index

    def get_by_id(self, account_id):
        return self.account_index.get(str(account_id))

    # -------------------------------------------------------
    # Add
    # -------------------------------------------------------

    def append(self, account):
        self.accounts.append(account)
        # 🟢 FIX: Changed get["id"] to get("id") to prevent a TypeError crash!
        aid = str(account.get("id"))
        self.account_index[aid] = account
        self.row_index[aid] = len(self.accounts) - 1
        self.dirty = True

    def add_many(self, accounts):
        for account in accounts:
            self.append(account)

    # -------------------------------------------------------
    # Remove
    # -------------------------------------------------------

    def remove_one(self, account_id):
        self.remove([account_id])

    def remove(self, ids):
        ids = {str(i) for i in ids}
        deleted_accounts = []
        remaining = []
        
        for account in self.accounts:
            if str(account["id"]) in ids:
                deleted_accounts.append(account)
            else:
                remaining.append(account)
                
        if not deleted_accounts:
            return []
            
        self.accounts = remaining
        
        # Reassign IDs sequentially
        id_map = {}
        for index, account in enumerate(self.accounts, start=1):
            old_id = str(account["id"])
            new_id = str(index)
            id_map[old_id] = new_id
            account["id"] = new_id
            
        self._build_index()
        self.dirty = True
        return deleted_accounts, id_map

    def remove_accounts(self, ids):
        ids = set(map(str, ids))
        self.accounts = [
            account for account in self.accounts
            if str(account.get("id")) not in ids
        ]
        self._build_index()
        self.dirty = True

    # -------------------------------------------------------
    # Update
    # -------------------------------------------------------

    def update_account(self, account_id, **fields):
        account = self.get_by_id(account_id)
        if account is None:
            return -1

        for key, value in fields.items():
            self._set_nested(account, key, value)

        self.dirty = True
        return self.row(account_id)

    def update_accounts(self, ids, **fields):
        rows = []
        for account_id in ids:
            account = self.get_by_id(account_id)
            if account is None:
                continue
            for key, value in fields.items():
                self._set_nested(account, key, value)
            rows.append(self.row(account_id))

        self.dirty = True
        return rows

    # -------------------------------------------------------
    # Values
    # -------------------------------------------------------

    def value(self, row, path):
        account = self.get(row)
        if account is None:
            return ""
        return self.get_value(account, path)

    def get_value(self, account, path):
        obj = account
        for part in path.split("."):
            if not isinstance(obj, dict):
                return ""
            obj = obj.get(part)
            if obj is None:
                return ""
        return obj

    # -------------------------------------------------------
    # Internal
    # -------------------------------------------------------
    
    def _refresh_time_ago_batch(self):
        for account in self.accounts:
            last_date = account.get("last_date", "")
            account["time_ago"] = get_time_ago(last_date)

    def _build_index(self):
        self.account_index.clear()
        self.row_index.clear()

        for row, account in enumerate(self.accounts):
            aid = str(account["id"])
            self.account_index[aid] = account
            self.row_index[aid] = row

    def _set_nested(self, obj, path, value):
        parts = path.split(".")
        for part in parts[:-1]:
            obj = obj.setdefault(part, {})
        obj[parts[-1]] = value