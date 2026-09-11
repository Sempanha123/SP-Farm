from PySide6.QtWidgets import QDialog
from ui.ui_set_vpn_dialog import Ui_SetVPN  # QtDesigner-generated UI

class SetVPNDialog(QDialog):
    def __init__(self, parent=None, data_manager=None, general_function=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.general_function = general_function
        
        self.ui = Ui_SetVPN()
        self.ui.setupUi(self)
        
        self.data = None
        self.data_acc = None
        self.vpn_json_data = {} # Will hold the dict from vpn.json

        # 🟢 CONNECT COMBOBOX CHANGED SIGNAL
        self.ui.vpn_comboBox.currentTextChanged.connect(self.on_vpn_changed)

        # Button connections
        self.ui.save.clicked.connect(self.on_save_clicked)
        self.ui.cancel.clicked.connect(self.reject)

    # 🟢 CHANGED TO A STANDARD SETTER METHOD
    def set_vpn_data_acc(self, vpn_data_acc):
        self.data_acc = vpn_data_acc
        self.setup_ui()
        self.load_data_to_ui(self.data_acc)

    def setup_ui(self):
        # 1. Load data from JSON via DataManager
        if self.data_manager:
            self.vpn_json_data = self.data_manager.get_vpn_data()
        
        # 2. Populate VPN Combo Box with the keys (VPN Names)
        self.ui.vpn_comboBox.blockSignals(True) 
        self.ui.vpn_comboBox.clear()
        
        # This grabs "Ravo VPN" (and any future VPNs you add) as the keys
        if isinstance(self.vpn_json_data, dict):
            self.ui.vpn_comboBox.addItems(list(self.vpn_json_data.keys()))
            
        self.ui.vpn_comboBox.setCurrentIndex(-1)
        self.ui.vpn_comboBox.blockSignals(False)

    def on_vpn_changed(self, vpn_name):
        # 3. Update City Combo Box when VPN changes
        self.ui.city_comboBox.clear()
        
        # This grabs the array of cities attached to that specific VPN key
        if isinstance(self.vpn_json_data, dict):
            cities = self.vpn_json_data.get(vpn_name, [])
            if cities:
                self.ui.city_comboBox.addItems(cities)

    def load_data_to_ui(self, vpn_data=None):
        if not vpn_data:
            self.ui.enable.setChecked(False)
            self.ui.vpn_comboBox.setCurrentIndex(-1)
            self.ui.city_comboBox.setCurrentIndex(-1)
            return

        enabled = vpn_data.get("enable", False)
        name = vpn_data.get("name")
        city = vpn_data.get("city")

        self.ui.enable.setChecked(enabled)

        # 4. Set VPN text first (this will trigger on_vpn_changed and load the cities)
        if name:
            self.ui.vpn_comboBox.setCurrentText(name)
        else:
            self.ui.vpn_comboBox.setCurrentIndex(-1)

        # 5. Set City text AFTER VPN has populated the city list
        if city:
            self.ui.city_comboBox.setCurrentText(city)
        else:
            self.ui.city_comboBox.setCurrentIndex(-1)

    def on_save_clicked(self):
        self.data = self.get_data()
        self.accept()  # Close with QDialog.Accepted result

    def get_data(self):
        return {
            "enable": self.ui.enable.isChecked(),
            "name": self.ui.vpn_comboBox.currentText() or None,
            "city": self.ui.city_comboBox.currentText() or None
        }