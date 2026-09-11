class AccountController:

    def __init__(self, cache):

        self.cache = cache
        self.models = []

    # -------------------------------------------------------
    # Models
    # -------------------------------------------------------

    def register_model(self, model):

        if model not in self.models:
            self.models.append(model)

    # -------------------------------------------------------
    # Reload
    # -------------------------------------------------------

    def reload(self, force_reload=True):

        self.cache.load(force_reload)

        for model in self.models:
            model.refresh()

    # -------------------------------------------------------
    # Save
    # -------------------------------------------------------

    def save(self):

        self.cache.save()

    # -------------------------------------------------------
    # Update
    # -------------------------------------------------------

    def update(self, account_id, **fields):

        row = self.cache.update_many(
            account_id,
            **fields
        )

        if row == -1:
            return False

        for model in self.models:
            model.notify_row_changed(row)

        return True

    # -------------------------------------------------------
    # Update Multiple
    # -------------------------------------------------------

    def update_many_accounts(self, ids, **fields):

        rows = self.cache.update_many_accounts(
            ids,
            **fields
        )

        if not rows:
            return False

        for row in rows:

            for model in self.models:
                model.notify_row_changed(row)

        return True

    # -------------------------------------------------------
    # Remove
    # -------------------------------------------------------

    def remove(self, ids):

        self.cache.remove(ids)

        for model in self.models:
            model.refresh()

    # -------------------------------------------------------
    # Add
    # -------------------------------------------------------

    def append(self, account):

        self.cache.append(account)

        for model in self.models:
            model.refresh()