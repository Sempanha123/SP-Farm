
pyside6-uic designs/main.ui -o ui/ui_main.py   
from . import resources_rc
pyside6-rcc ui/resources.qrc -o ui/resources_rc.py
pyside6-uic designs/set_location_dialog.ui -o ui/ui_set_location_dialog.py
pyside6-uic designs/set_vpn_dialog.ui -o ui/ui_set_vpn_dialog.py
pyside6-uic designs/set_note_dialog.ui -o ui/ui_set_note_dialog.py
pyside6-uic designs/set_post_account_dialog.ui -o ui/set_post_account_dialog.py

appium --allow-cors