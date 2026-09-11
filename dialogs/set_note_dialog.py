from PySide6.QtWidgets import QDialog
from ui.ui_set_note_dialog import Ui_set_note_dialog # Assuming this is your UI class

class SetNoteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.ui = Ui_set_note_dialog()
        self.ui.setupUi(self)
        
        self.data = None

        self.ui.save.clicked.connect(self.on_save_clicked)
        self.ui.cancel.clicked.connect(self.reject)

    def on_save_clicked(self):
        self.data = self.get_data()
        self.accept() # This closes the dialog with an "OK" result

    def get_data(self):
        return {
            "notes": self.ui.notes_text_edit.toPlainText()
        }
    
    def set_data(self, **kwargs):
        if "notes" in kwargs:
            self.ui.notes_text_edit.setPlainText(kwargs["notes"])