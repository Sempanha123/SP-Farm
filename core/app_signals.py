# core/app_signals.py
from PySide6.QtCore import QObject, Signal

class AppSignals(QObject):
    accounts_changed = Signal()
    update_account_status = Signal(int, bool, dict)

signals = AppSignals()