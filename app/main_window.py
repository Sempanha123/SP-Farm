# app/main_window.py
from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtGui import QMovie

from ui.ui_main import Ui_MainWindow
from core.ui_functions import change_stacked_widget_page
from app.tabs.dashboard_tab import DashboardTab
from app.tabs.active_tab import ActiveTab
from app.tabs.reg_tab import RegTab
from core.utils import get_selected_account_mode
from core.general_function import GeneralFunction
from core.ld_manager import LDManager
from core.data_manager import DataManager
from dialogs.post_account_dialog import PostAccountDialog
from dialogs.set_vpn_dialog import SetVPNDialog
from PySide6.QtWidgets import QHeaderView
from core.account_cache import AccountCache
import sys
class MainWindow(QMainWindow):
    """Manages the main window, navigation, and page controllers."""
    def __init__(self):
        super().__init__()

        sys.stdout.reconfigure(encoding='utf-8')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.data_manager = DataManager()
        self.general_function = GeneralFunction()
        self.ld_manager = LDManager(self.ui, self.general_function, self.data_manager)
        self.post_dialog = PostAccountDialog(self, self.data_manager, self.general_function)
        self.set_vpn_dialog = SetVPNDialog(self, self.data_manager, self.general_function)

        self.account_cache = AccountCache(self.data_manager)
        self.account_cache.load()

        # Create controllers for each page
        self.active_tab_controller = ActiveTab(
            ui=self.ui, 
            parent=self, 
            data_manager=self.data_manager, 
            ld_manager=self.ld_manager,
            general_function=self.general_function,
            account_cache=self.account_cache
        )

        self.reg_tab_controller = RegTab(
            ui=self.ui, 
            parent=self, 
            data_manager=self.data_manager, 
            ld_manager=self.ld_manager,
            general_function=self.general_function
        )
        self.dashboard_controller = DashboardTab(
            main_window=self,
            ui=self.ui,
            data_manager=self.data_manager,
            ld_manager=self.ld_manager,
            general_function=self.general_function,
            reg_tab_controller=self.reg_tab_controller,
            active_tab_controller=self.active_tab_controller,
            account_cache=self.account_cache,
        )


        self.ui.ldplayer_list.setColumnWidth(0, 0) # Status


        table = self.ui.profile_table_accounts
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )


        table.setColumnWidth(0, 0) # ID
        table.setColumnWidth(1, 160) # ID
        table.setColumnWidth(2, 140) # ID
        table.setColumnWidth(3, 200) # ID
        table.setColumnWidth(4, 280) # ID
        table.setColumnWidth(5, 110) 
        table.setColumnWidth(6, 50) # ID
        table.setColumnWidth(7, 70) # ID
        table.setColumnWidth(8, 170) # ID
        table.setColumnWidth(9, 70) # ID
        table.setColumnWidth(10, 170) # ID
        table.setColumnWidth(11, 170) # ID
        table.setColumnWidth(12, 140) # ID
        table.setColumnWidth(13, 170) # ID
        table.setColumnWidth(14, 170) # ID

        table = self.ui.profile_table_details_accounts

        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )
        table.setColumnWidth(0, 0)
        table.setColumnWidth(1, 160)
        table.setColumnWidth(2, 140)
        table.setColumnWidth(3, 200)
        table.setColumnWidth(4, 280)
        table.setColumnWidth(5, 110)
        table.setColumnWidth(6, 50)
        table.setColumnWidth(7, 70)
        table.setColumnWidth(8, 170)
        table.setColumnWidth(9, 70)
        table.setColumnWidth(10, 170)
        table.setColumnWidth(11, 200)
        table.setColumnWidth(12, 140)
        table.setColumnWidth(13, 150)
        table.setColumnWidth(14, 150)
        table.setColumnWidth(15, 150)
        table.setColumnWidth(16, 150)
        table.setColumnWidth(17, 150)
        table.setColumnWidth(18, 150)
        table.setColumnWidth(19, 150)
        table.setColumnWidth(20, 150)
        table.setColumnWidth(21, 170)
        table.setColumnWidth(22, 140)
        table.setColumnWidth(23, 170)
        table.setColumnWidth(24, 140)
        table.setColumnWidth(25, 170)
        table.setColumnWidth(26, 170)

        
        
        # Global setup
        self.load_gif()
        self._connect_signals()
        
        self.show()


 


    def _connect_signals(self):
        self.ui.icon_only_widget.setHidden(True)

        # Navigation buttons
        self.ui.dashboard_1.clicked.connect(lambda: change_stacked_widget_page(self.ui.stacked_main, 0))
        self.ui.active_menu_1.clicked.connect(lambda: change_stacked_widget_page(self.ui.stacked_main, 1))
        self.ui.reg_1.clicked.connect(lambda: change_stacked_widget_page(self.ui.stacked_main, 2))
        self.ui.page4_1.clicked.connect(lambda: change_stacked_widget_page(self.ui.stacked_main, 3))
        self.ui.page5_1.clicked.connect(lambda: change_stacked_widget_page(self.ui.stacked_main, 4))

        self.ui.dashboard_2.clicked.connect(lambda: change_stacked_widget_page(self.ui.stacked_main, 0))
        self.ui.active_menu_2.clicked.connect(lambda: change_stacked_widget_page(self.ui.stacked_main, 1))
        self.ui.reg_2.clicked.connect(lambda: change_stacked_widget_page(self.ui.stacked_main, 2))
        self.ui.page4_2.clicked.connect(lambda: change_stacked_widget_page(self.ui.stacked_main, 3))
        self.ui.page5_2.clicked.connect(lambda: change_stacked_widget_page(self.ui.stacked_main, 4))


        
    def load_gif(self):
        try:
            self.gif_label = self.findChild(QLabel, "gif_label")
            if self.gif_label:
                self.movie = QMovie("images/peach-goma.gif")
                self.gif_label.setMovie(self.movie)
                self.movie.start()
        except Exception as e:
            print(f"Could not load GIF: {e}")

