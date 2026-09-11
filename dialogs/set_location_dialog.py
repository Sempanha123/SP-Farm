from PySide6.QtWidgets import QDialog
from ui.ui_set_location_dialog import Ui_set_location_dialog

class SetLocationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_set_location_dialog()
        self.ui.setupUi(self)

        self.data = None


        # Connect buttons
        self.ui.save.clicked.connect(self.on_save_clicked)
        self.ui.cancel.clicked.connect(self.reject)

    def on_save_clicked(self):
        self.data = self.get_data()
        print("Data saved:", self.data)  # Debug
        self.accept()  # Closes dialog with OK

    def get_data(self):
        """Return user input from dialog widgets safely matching accounts format."""
        is_enabled = self.ui.enable.isChecked()
        coords = self.ui.coordinate_line_edit.text().strip()
        
        # Default empty values if parsing fails or text is empty
        lat_val = ""
        long_val = ""

        # Always try to parse the string if it contains a comma
        if "," in coords:
            try:
                lat, long = coords.split(",", 1)
                lat_val = lat.strip()
                long_val = long.strip()
            except ValueError:
                pass  # Fallback safe catch if splitting fails

        return {
            "gps": {
                "enable": is_enabled,
                "lat": lat_val,
                "long": long_val
            }
        }
    def set_data(self, gps_data=None):
        if gps_data:
            lat = gps_data.get("lat")
            long = gps_data.get("long")
            enable = gps_data.get("enable")
            self.ui.enable.setChecked(enable)
            self.ui.coordinate_line_edit.setText(f"{lat},{long}")