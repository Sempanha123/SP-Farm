from PySide6.QtCore import Qt, QSortFilterProxyModel


class AccountProxy(QSortFilterProxyModel):

    def __init__(self):
        super().__init__()

        self._category = "All"
        self._search = ""

        # Case-insensitive sorting/filtering
        self.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)

    # ---------------------------------------------------
    # Category
    # ---------------------------------------------------

    def set_category(self, category):

        self._category = category

        self.invalidateFilter()

    # ---------------------------------------------------
    # Search
    # ---------------------------------------------------

    def set_search(self, text):

        self._search = text.strip().lower()

        self.invalidateFilter()

    # ---------------------------------------------------
    # Filter
    # ---------------------------------------------------

    def filterAcceptsRow(self, source_row, parent):

        model = self.sourceModel()

        account = model.cache.get(source_row)

        if account is None:
            return False

        # ---------- Category ----------

        if self._category != "All":

            if account.get("category", "") != self._category:
                return False

        # ---------- Search ----------

        if self._search:

            keyword = self._search

            searchable = " ".join([
                str(account.get("id", "")),
                str(account.get("name", "")),
                str(account.get("uid", "")),
                str(account.get("email", "")),
                str(account.get("phone_number", "")),
                str(account.get("category", "")),
                str(account.get("notes", "")),
            ]).lower()

            if keyword not in searchable:
                return False

        return True