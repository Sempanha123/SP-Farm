# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QButtonGroup, QCheckBox,
    QComboBox, QFormLayout, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPlainTextEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QTabWidget, QTableView, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
from . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1268, 870)
        MainWindow.setStyleSheet(u"QWidget, #post_group {\n"
"	background-color: rgb(226, 241, 255);\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"/* GroupBox panels */\n"
"QGroupBox {\n"
"	\n"
"	background-color: rgb(255, 188, 218);\n"
"    border: 2px solid rgb(157, 178, 255); /* very subtle border */\n"
"    border-radius: 8px;\n"
"    margin-top: 10px;\n"
"    padding:4px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"/* Optional: GroupBox title */\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    padding: 0px 4px;\n"
"	color: rgb(16, 16, 16);\n"
"font-size: 18px;\n"
"}\n"
"QPushButton {\n"
"	background-color: rgb(74, 81, 127);\n"
"    color: white;     /* dark gray text */\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 3px 13px;\n"
"    font-weight: bold;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #F48EB9;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #E96DA4;  /* deeper pink when pressed */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
""
                        "    background-color: #FBD8E4;  /* faded pink for disabled state */\n"
"    color: #999999;\n"
"}\n"
"/* ComboBox Main Style */\n"
"QComboBox {\n"
"    background-color: #FFFFFF; /* white so it stands out on aqua panel */\n"
"    color: rgb(50, 50, 50);    /* dark gray text */\n"
"    border: 1px solid #A3C9D4; /* subtle aqua border */\n"
"    border-radius: 6px;\n"
"    padding: 4px 8px;\n"
"}\n"
"\n"
"/* ComboBox Main Style */\n"
"QComboBox {\n"
"	background-color: rgb(85, 170, 255);\n"
"	color: rgb(255, 255, 255);\n"
"    border: 1px solid #A3C9D4; /* subtle aqua border */\n"
"    border-radius: 6px;\n"
"    padding: 4px 8px;\n"
"}\n"
"\n"
"/* Drop-down Button */\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 20px;\n"
"	background-color: rgb(77, 155, 232);\n"
"    border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"}\n"
"\n"
"/* Arrow Icon */\n"
"QComboBox::down-arrow {\n"
"	image: url(:/icons/images/down-arrow.png"
                        ");\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"/* Popup List */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #A3C9D4;\n"
"    selection-background-color: #F6AAC9; /* pastel pink highlight */\n"
"    selection-color: rgb(50, 50, 50);\n"
"}\n"
"/* LineEdit Style */\n"
"QLineEdit {\n"
"    background-color: #FFFFFF; /* clean white for good contrast */\n"
"    color: rgb(50, 50, 50);    /* dark gray text */\n"
"    border: 1px solid #A3C9D4; /* same subtle aqua border as ComboBox */\n"
"    border-radius: 6px;\n"
"    padding: 4px 8px;\n"
"    selection-background-color: #F6AAC9; /* pastel pink text highlight */\n"
"    selection-color: rgb(50, 50, 50);\n"
"}\n"
"\n"
"/* Focused (active) state */\n"
"QLineEdit:focus {\n"
"    border: 2px solid #F6AAC9; /* pink border when focused */\n"
"    outline: none;\n"
"}\n"
"\n"
"/* ---------------------------------------------------------------------------\n"
" * QTableWidget -- A detailed, professional style\n"
""
                        " * --------------------------------------------------------------------------- */\n"
"\n"
"/* Main Table Widget Area */\n"
"QTableWidget {\n"
"    background-color: white; /* Base color for rows */\n"
"    alternate-background-color: rgb(246, 248, 255); /* Lighter blue for alternate rows */\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"/* Individual cells (items) in the table */\n"
"QTableWidget::item {\n"
"    padding: 10px; /* Ample spacing for readability */\n"
"	border: none;\n"
"}\n"
"\n"
"/* Style for selected cells or rows */\n"
"QTableWidget::item:selected {\n"
"	background-color: rgb(74, 81, 127);\n"
"    color: white;\n"
"}\n"
"\n"
"/* ---------------------------------------------------------------------------\n"
" * QHeaderView -- Styling for the top header\n"
" * --------------------------------------------------------------------------- */\n"
"\n"
"/* The entire header bar */\n"
"QHeaderView {\n"
"	background-color: rgb(248, 251, 255);\n"
"}\n"
"\n"
"/* Each individual section/column in the header */"
                        "\n"
"QHeaderView::section {\n"
"	background-color: rgb(213, 242, 250);\n"
"    border: none;\n"
"    text-align: center; /* Ensure text is aligned left */\n"
"padding: 3px;\n"
"}\n"
"\n"
"/* Style for when a header section is clicked/pressed */\n"
"QHeaderView::section:pressed {\n"
"	border: none;\n"
"}\n"
"\n"
"/* The small sort indicator arrow that appears when you click a header */\n"
"QHeaderView::down-arrow {\n"
"    \n"
"	image: url(:/icons/images/down-arrow.png);\n"
"}\n"
"\n"
"QHeaderView::up-arrow {\n"
"    image: url(:/icons/images/down-arrow.png);\n"
"}\n"
"\n"
"/* ---------------------------------------------------------------------------\n"
" * QScrollBar -- Styling for the vertical and horizontal scrollbars\n"
" * --------------------------------------------------------------------------- */\n"
"\n"
"/* Vertical Scrollbar */\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: #2E3440; /* Match the darkest background */\n"
"    width: 14px;\n"
"    margin: 0px;\n"
"}\n"
"QScrollBar"
                        "::handle:vertical {\n"
"    background: #4C566A; /* Handle color */\n"
"    min-height: 10px;\n"
"    border-radius: 7px;\n"
"}\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #5E81AC; /* Highlight on hover */\n"
"}\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    height: 0px; /* Hide the top and bottom arrow buttons */\n"
"    background: none;\n"
"}\n"
"\n"
"/* Horizontal Scrollbar */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: #2E3440;\n"
"    height: 10px;\n"
"    margin: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: #4C566A;\n"
"    min-width: 25px;\n"
"    border-radius: 7px;\n"
"}\n"
"QScrollBar::handle:horizontal:hover {\n"
"    background: #5E81AC;\n"
"}\n"
"QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {\n"
"    width: 0px; /* Hide the left and right arrow buttons */\n"
"    background: none;\n"
"}\n"
"\n"
"/* ---------------------------------------------------------------------------\n"
" * QSpinB"
                        "ox -- Professional Dark Theme Style\n"
" * --------------------------------------------------------------------------- */\n"
"\n"
"QSpinBox {\n"
"	background-color: rgb(136, 199, 247);\n"
"    color: white; /* Light grey text */\n"
"    /*border: 1px solid #2E3440;  Darker border for depth */\n"
"    border-radius: 5px;\n"
"    padding: 4px; /* Give text some space */\n"
"    /*font-size: 14px;*/\n"
"}\n"
"\n"
"QSpinBox:focus {\n"
"    /*border: 1px solid #88C0D0;  Cyan focus border, same as QLineEdit */\n"
"}\n"
"\n"
"\n"
"/* --- Styling the Up and Down Buttons --- */\n"
"\n"
"QSpinBox::up-button {\n"
"background-color:  rgb(125, 151, 216);\n"
"    subcontrol-position: top right; /* Position at the top right */\n"
"    width: 20px;\n"
"    border-top-right-radius: 5px;\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"background-color:  rgb(125, 151, 216);\n"
"    subcontrol-position: bottom right; /* Position at the bottom right */\n"
"    width: 20px;\n"
"    border-bottom-right-radius: 5px;\n"
"}\n"
"\n"
"/* Styl"
                        "e for when hovering over the buttons */\n"
"QSpinBox::up-button:hover, QSpinBox::down-button:hover {\n"
"    background-color: #5E81AC; /* Main blue accent color */\n"
"}\n"
"\n"
"/* --- Styling the Up and Down Arrows --- */\n"
"\n"
"QSpinBox::up-arrow {\n"
"    image: url(:/icons/images/up-arrow.png); /* You need a white up-arrow icon */\n"
"    width: 17px;\n"
"    height: 17px;\n"
"}\n"
"\n"
"QSpinBox::down-arrow {\n"
"    image: url(:/icons/images/down-arrow.png); /* You need a white down-arrow icon */\n"
"    width: 17px;\n"
"    height: 17px;\n"
"}\n"
"\n"
"\n"
"/* ---------------------------------------------------------------------------\n"
" * QCheckBox -- Professional Dark Theme Style\n"
" * --------------------------------------------------------------------------- */\n"
"\n"
"/* Style for the entire checkbox widget (box + text) */\n"
"QCheckBox {\n"
"    color: black; /* Light grey text */\n"
"    spacing: 10px; /* Space between the box and the text */\n"
"}\n"
"\n"
"/* Style for the checkable box "
                        "itself */\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    background-color: white; /* Dark input field background */\n"
"    border: 2px solid rgb(136, 199, 247);  /* Darker border */\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"/* Style for when the mouse is hovering over the checkbox */\n"
"QCheckBox::indicator:hover {\n"
"    border: 2px solid rgb(42, 126, 0); /* Lighter blue border on hover */\n"
"}\n"
"\n"
"/* Style for when the checkbox is checked */\n"
"QCheckBox::indicator:checked {\n"
"    /* This displays a checkmark icon from your resources */\n"
"    image: url(:/icons/images/checkmark.png);\n"
"}\n"
"\n"
"/* Style for when a checked checkbox is hovered */\n"
"\n"
"\n"
"/* Style for when the checkbox is disabled */\n"
"QCheckBox:disabled {\n"
"    color: #4C566A; /* Greyed-out text */\n"
"}\n"
"\n"
"QCheckBox::indicator:disabled {\n"
"    background-color: #3B4252; /* Darker, disabled background */\n"
"    border: 1px solid #434C5E;\n"
"}\n"
"\n"
"/* --------------------"
                        "-------------------------------------------------------\n"
" * QRadioButton \u2014 Pastel Aqua & Pink Modern Style\n"
" * --------------------------------------------------------------------------- */\n"
"\n"
"QRadioButton {\n"
"    color: black;                /* Text color */\n"
"    spacing: 10px;               /* Space between circle and text */\n"
"    font-weight: medium;\n"
"}\n"
"\n"
"/* Radio circle (indicator) */\n"
"QRadioButton::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border-radius: 10px;          /* Make it round */\n"
"    border: 2px solid rgb(136, 199, 247);   /* Same blue tone as QCheckBox */\n"
"    background-color: white;     /* Base background */\n"
"}\n"
"\n"
"/* Hover effect */\n"
"QRadioButton::indicator:hover {\n"
"    border: 2px solid rgb(42, 126, 0);      /* Light green-blue hover border */\n"
"}\n"
"\n"
"/* Checked (active) state */\n"
"QRadioButton::indicator:checked {\n"
"    border: 2px solid rgb(129, 199, 132); /* Pastel green border */\n"
"    background"
                        "-color: qradialgradient(\n"
"        cx: 0.5, cy: 0.5, radius: 0.6,\n"
"        fx: 0.5, fy: 0.5,\n"
"        stop: 0 rgb(102, 187, 106),\n"
"        stop: 1 white\n"
"    );\n"
"}\n"
"\n"
"\n"
"/* Disabled state */\n"
"QRadioButton:disabled {\n"
"    color: #4C566A;\n"
"}\n"
"\n"
"QRadioButton::indicator:disabled {\n"
"    background-color: #E0E0E0;\n"
"    border: 1px solid #B0B0B0;\n"
"}\n"
"\n"
"/* Focus state (optional glowing border) */\n"
"QRadioButton:focus {\n"
"    outline: none;\n"
"}\n"
"\n"
"QRadioButton::indicator:focus {\n"
"    border: 2px solid rgb(157, 178, 255);\n"
"}\n"
"QPlainTextEdit{\n"
"	\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* ---------------------------------------------------------------------------\n"
" * QMenu -- Style for multi-level context menus\n"
" * --------------------------------------------------------------------------- */\n"
"\n"
"QMenu {\n"
"    background-color: #3B4252; /* Dark grey background */\n"
"    color: #ECEFF4; /* Light text */\n"
"    bo"
                        "rder: 1px solid #4C566A;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}\n"
"QMenu::icon {\n"
"  width: 24px;\n"
"    height: 24px;\n"
"    padding-left: 10px; /* \ud83d\udc48 Pushes icons to the right */\n"
"}\n"
"\n"
"/* Style for each item in the menu */\n"
"QMenu::item {\n"
"    padding: 4px 6px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"/* This is the hover effect for any menu item */\n"
"QMenu::item:selected {\n"
"    background-color: #5E81AC; /* Main blue accent color */\n"
"}\n"
"/* Style for the separator line */\n"
"QMenu::separator {\n"
"    height: 1px;\n"
"    background-color: #4C566A;\n"
"    margin: 5px 0px;\n"
"}\n"
"\n"
"/* The arrow for submenus */\n"
"QMenu::right-arrow {\n"
"    image: url(:/icons/images/right-arrow-48.png); /* You need a right-arrow icon */\n"
"    width: 16px;\n"
"    height: 16px;\n"
"padding-right: 10px;\n"
"}\n"
"\n"
"/* ------------------------------\n"
"   QTabWidget Base Pane\n"
"--------------------------------*/\n"
"QTabWidget::pane {\n"
"    border: 2p"
                        "x solid  rgb(157, 178, 255);        /* Light mint border */\n"
"    border-radius: 7px;\n"
"    background-color: #f1f8f6;        /* Very light green background */\n"
"    padding: 1px;\n"
"}\n"
"\n"
"/* ------------------------------\n"
"   QTabBar (Tabs Container)\n"
"--------------------------------*/\n"
"QTabBar {\n"
"    qproperty-drawBase: 0; /* Prevents double border */\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"/* ------------------------------\n"
"   Tabs - General Style\n"
"--------------------------------*/\n"
"QTabBar::tab {\n"
"    background-color: qlineargradient(\n"
"        x1: 0, y1: 0, x2: 0, y2: 1,\n"
"        stop: 0 #e8f5e9,\n"
"        stop: 1 #c8e6c9\n"
"    );\n"
"    border: 1px solid  rgb(157, 178, 255);\n"
"    border-bottom: none;               /* So selected tab merges with pane */\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 100px;\n"
"    padding: 4px 7px;\n"
"    color: #2e7d32;                    /* Dark green text */"
                        "\n"
"    margin-right: 3px;\n"
"}\n"
"\n"
"/* ------------------------------\n"
"   Hovered Tab\n"
"--------------------------------*/\n"
"QTabBar::tab:hover {\n"
"    background-color: qlineargradient(\n"
"        x1: 0, y1: 0, x2: 0, y2: 1,\n"
"        stop: 0 #dcedc8,\n"
"        stop: 1 #aed581\n"
"    );\n"
"    border-color: #81c784;\n"
"}\n"
"\n"
"/* ------------------------------\n"
"   Selected (Active) Tab\n"
"--------------------------------*/\n"
"QTabBar::tab:selected {\n"
"    background-color: qlineargradient(\n"
"        x1: 0, y1: 0, x2: 0, y2: 1,\n"
"        stop: 0 #a5d6a7,\n"
"        stop: 1 #81c784\n"
"    );\n"
"    border-color: #66bb6a;\n"
"    color: white;\n"
"    font-weight: 600;\n"
"}\n"
"\n"
"/* ------------------------------\n"
"   Disabled Tab\n"
"--------------------------------*/\n"
"QTabBar::tab:disabled {\n"
"    color: #bdbdbd;\n"
"    background-color: #f5f5f5;\n"
"    border-color: #dcdcdc;\n"
"}\n"
"\n"
"/* ------------------------------\n"
"   Tab Positions (Optional)\n"
""
                        "--------------------------------*/\n"
"QTabBar::tab:top:selected {\n"
"    margin-bottom: -1px;\n"
"}\n"
"\n"
"QTabBar::tab:bottom:selected {\n"
"    margin-top: -1px;\n"
"}\n"
"\n"
"QTabBar::tab:left:selected {\n"
"    margin-right: -1px;\n"
"}\n"
"\n"
"QTabBar::tab:right:selected {\n"
"    margin-left: -1px;\n"
"}\n"
"\n"
"\n"
"\n"
"#bg_options,#bg_options_2, #show_details{\n"
"	background-color: rgb(255, 188, 218);\n"
"}\n"
"#ldplayer_controller_widget, #react_group, #first_group_active, #reels_group, #general_option_group, #vidos_group, #reel_group, #share_reel_groups, #long_videos_group, #share_reel_groups_2, #option_reg{\n"
"	background-color: rgb(204, 211, 250);\n"
"}\n"
"#shares_groups, #schedulce_group, #shares_groups_2, #schedulce_group_2, #full_verify_upload, #full_verify_yandex, #no_veriry_group, #create_type_verify_or_no_verify, #frame_2, #frame_4, #option1, #horizontalLayout_43, #frame_3, #frame_9{\n"
"	background-color: rgb(194, 202, 250);\n"
"}\n"
"#thread_option, #ld_sleep_frame, #option_check"
                        "box, #option_checkbox_2, #run_schedule_checkbox, #shop_tool_if_no_internet, #auto_shutdown_pc, #auto_arrange_ldplayer, #backup_data_fb_ld, #label_9{\n"
"	background-color: rgb(204, 211, 250);\n"
"}\n"
"\n"
"/* ---------------------------------------------------------------------------\n"
" * QTableView\n"
" * --------------------------------------------------------------------------- */\n"
"QTableView {\n"
"    alternate-background-color: rgb(246, 248, 255);\n"
"    border-radius: 8px;\n"
"    selection-background-color: rgb(74, 81, 127);\n"
"    selection-color: white;\n"
"}\n"
"\n"
"QTableView::item {\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"    background-color: rgb(74, 81, 127);\n"
"    color: white;\n"
"}\n"
"")
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.actionjlj = QAction(MainWindow)
        self.actionjlj.setObjectName(u"actionjlj")
        self.actionsfdsf = QAction(MainWindow)
        self.actionsfdsf.setObjectName(u"actionsfdsf")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_32 = QGridLayout(self.centralwidget)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.icon_only_widget = QWidget(self.centralwidget)
        self.icon_only_widget.setObjectName(u"icon_only_widget")
        self.icon_only_widget.setStyleSheet(u"QWidget{\n"
"	background-color: #7291BE;\n"
"	background-color: rgb(143, 171, 247);\n"
"}\n"
"QPushButton{\n"
"	color: white;\n"
"	text-align: center;\n"
"	height: 30px;\n"
"	border: none;\n"
"}\n"
"QPushButton::checked{\n"
"	\n"
"	background-color: rgb(245, 250, 254);\n"
"	color: rgb(31, 149, 239);\n"
"	font-weight: bold;\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.icon_only_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.icon_only_widget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(40, 40))
        self.label.setMaximumSize(QSize(40, 40))
        self.label.setPixmap(QPixmap(u":/icons/images/logo.png"))
        self.label.setScaledContents(False)

        self.horizontalLayout_2.addWidget(self.label)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 15, -1, -1)
        self.dashboard_1 = QPushButton(self.icon_only_widget)
        self.dashboard_1.setObjectName(u"dashboard_1")
        self.dashboard_1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/dashboard-white.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon.addFile(u":/icons/images/dashboard-dark.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.dashboard_1.setIcon(icon)
        self.dashboard_1.setIconSize(QSize(24, 24))
        self.dashboard_1.setCheckable(True)
        self.dashboard_1.setChecked(True)
        self.dashboard_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.dashboard_1)

        self.active_menu_1 = QPushButton(self.icon_only_widget)
        self.active_menu_1.setObjectName(u"active_menu_1")
        self.active_menu_1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.active_menu_1.setIcon(icon)
        self.active_menu_1.setIconSize(QSize(24, 24))
        self.active_menu_1.setCheckable(True)
        self.active_menu_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.active_menu_1)

        self.reg_1 = QPushButton(self.icon_only_widget)
        self.reg_1.setObjectName(u"reg_1")
        self.reg_1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.reg_1.setIcon(icon)
        self.reg_1.setIconSize(QSize(24, 24))
        self.reg_1.setCheckable(True)
        self.reg_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.reg_1)

        self.page4_1 = QPushButton(self.icon_only_widget)
        self.page4_1.setObjectName(u"page4_1")
        self.page4_1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.page4_1.setIcon(icon)
        self.page4_1.setIconSize(QSize(24, 24))
        self.page4_1.setCheckable(True)
        self.page4_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.page4_1)

        self.page5_1 = QPushButton(self.icon_only_widget)
        self.page5_1.setObjectName(u"page5_1")
        self.page5_1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.page5_1.setIcon(icon)
        self.page5_1.setIconSize(QSize(24, 24))
        self.page5_1.setCheckable(True)
        self.page5_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.page5_1)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(20, 310, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.pushButton_6 = QPushButton(self.icon_only_widget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/dashboard-white.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_6.setIcon(icon1)
        self.pushButton_6.setIconSize(QSize(24, 24))
        self.pushButton_6.setCheckable(True)

        self.verticalLayout_2.addWidget(self.pushButton_6)


        self.gridLayout_32.addWidget(self.icon_only_widget, 0, 0, 1, 1)

        self.icon_name_widget = QWidget(self.centralwidget)
        self.icon_name_widget.setObjectName(u"icon_name_widget")
        self.icon_name_widget.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(143, 171, 247);\n"
"	color: white;\n"
"}\n"
"QPushButton{\n"
"	color: white;\n"
"	text-align: left;\n"
"	height: 30px;\n"
"	border: none;\n"
"	padding-left: 10px;\n"
"	border-top-left-radius: 10px;\n"
"	border-bottom-left-radius: 10px;\n"
"}\n"
"QPushButton::checked{\n"
"	\n"
"	background-color: rgb(245, 250, 254);\n"
"	color: rgb(31, 149, 239);\n"
"	font-weight: bold;\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.icon_name_widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, 9, -1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, 20, -1)
        self.label_4 = QLabel(self.icon_name_widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(40, 40))
        self.label_4.setMaximumSize(QSize(40, 40))
        self.label_4.setPixmap(QPixmap(u":/icons/images/logo.png"))

        self.horizontalLayout_3.addWidget(self.label_4)

        self.label_2 = QLabel(self.icon_name_widget)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_2.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 15, -1, -1)
        self.dashboard_2 = QPushButton(self.icon_name_widget)
        self.dashboard_2.setObjectName(u"dashboard_2")
        self.dashboard_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.dashboard_2.setIcon(icon)
        self.dashboard_2.setIconSize(QSize(24, 24))
        self.dashboard_2.setCheckable(True)
        self.dashboard_2.setChecked(True)
        self.dashboard_2.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.dashboard_2)

        self.active_menu_2 = QPushButton(self.icon_name_widget)
        self.active_menu_2.setObjectName(u"active_menu_2")
        self.active_menu_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.active_menu_2.setIcon(icon)
        self.active_menu_2.setIconSize(QSize(24, 24))
        self.active_menu_2.setCheckable(True)
        self.active_menu_2.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.active_menu_2)

        self.reg_2 = QPushButton(self.icon_name_widget)
        self.reg_2.setObjectName(u"reg_2")
        self.reg_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.reg_2.setIcon(icon)
        self.reg_2.setIconSize(QSize(24, 24))
        self.reg_2.setCheckable(True)
        self.reg_2.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.reg_2)

        self.page4_2 = QPushButton(self.icon_name_widget)
        self.page4_2.setObjectName(u"page4_2")
        self.page4_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.page4_2.setIcon(icon)
        self.page4_2.setIconSize(QSize(24, 24))
        self.page4_2.setCheckable(True)
        self.page4_2.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.page4_2)

        self.page5_2 = QPushButton(self.icon_name_widget)
        self.page5_2.setObjectName(u"page5_2")
        self.page5_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.page5_2.setIcon(icon)
        self.page5_2.setIconSize(QSize(24, 24))
        self.page5_2.setCheckable(True)
        self.page5_2.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.page5_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 310, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.pushButton_16 = QPushButton(self.icon_name_widget)
        self.pushButton_16.setObjectName(u"pushButton_16")
        self.pushButton_16.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_16.setIcon(icon1)
        self.pushButton_16.setIconSize(QSize(24, 24))
        self.pushButton_16.setCheckable(True)

        self.verticalLayout_4.addWidget(self.pushButton_16)


        self.gridLayout_32.addWidget(self.icon_name_widget, 0, 1, 1, 1)

        self.name_menu = QWidget(self.centralwidget)
        self.name_menu.setObjectName(u"name_menu")
        self.verticalLayout_5 = QVBoxLayout(self.name_menu)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.name_menu)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_4 = QHBoxLayout(self.widget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.menu = QPushButton(self.widget)
        self.menu.setObjectName(u"menu")
        self.menu.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.menu.setStyleSheet(u"border: none;\n"
"background-color: none;")
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/menu.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu.setIcon(icon2)
        self.menu.setIconSize(QSize(20, 20))
        self.menu.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.menu)

        self.horizontalSpacer = QSpacerItem(229, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.start = QPushButton(self.widget)
        self.start.setObjectName(u"start")
        self.start.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.start.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/start.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.start.setIcon(icon3)
        self.start.setIconSize(QSize(20, 20))

        self.horizontalLayout_4.addWidget(self.start)

        self.time = QLabel(self.widget)
        self.time.setObjectName(u"time")
        font1 = QFont()
        font1.setPointSize(21)
        font1.setBold(True)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        self.time.setFont(font1)
        self.time.setStyleSheet(u"color: rgb(0, 0, 127);")

        self.horizontalLayout_4.addWidget(self.time)

        self.stop = QPushButton(self.widget)
        self.stop.setObjectName(u"stop")
        self.stop.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/stop.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.stop.setIcon(icon4)
        self.stop.setIconSize(QSize(20, 20))

        self.horizontalLayout_4.addWidget(self.stop)

        self.horizontalSpacer_2 = QSpacerItem(229, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.gif_label = QLabel(self.widget)
        self.gif_label.setObjectName(u"gif_label")
        self.gif_label.setMaximumSize(QSize(35, 35))
        self.gif_label.setPixmap(QPixmap(u":/icons/images/peach-goma.gif"))
        self.gif_label.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.gif_label)


        self.verticalLayout_5.addWidget(self.widget)

        self.stacked_main = QStackedWidget(self.name_menu)
        self.stacked_main.setObjectName(u"stacked_main")
        self.stacked_main.setStyleSheet(u"")
        self.dashboard_page = QWidget()
        self.dashboard_page.setObjectName(u"dashboard_page")
        self.gridLayout_2 = QGridLayout(self.dashboard_page)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(9)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.ldplayer_list_widget = QGroupBox(self.dashboard_page)
        self.ldplayer_list_widget.setObjectName(u"ldplayer_list_widget")
        self.gridLayout_4 = QGridLayout(self.ldplayer_list_widget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.ldplayer_list = QTableWidget(self.ldplayer_list_widget)
        if (self.ldplayer_list.columnCount() < 3):
            self.ldplayer_list.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.ldplayer_list.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.ldplayer_list.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.ldplayer_list.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.ldplayer_list.rowCount() < 1):
            self.ldplayer_list.setRowCount(1)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.ldplayer_list.setVerticalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.ldplayer_list.setItem(0, 1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.ldplayer_list.setItem(0, 2, __qtablewidgetitem5)
        self.ldplayer_list.setObjectName(u"ldplayer_list")
        font2 = QFont()
        font2.setFamilies([u"Noto Sans Khmer"])
        self.ldplayer_list.setFont(font2)
        self.ldplayer_list.setFocusPolicy(Qt.NoFocus)
        self.ldplayer_list.setEditTriggers(QAbstractItemView.EditKeyPressed)
        self.ldplayer_list.setDragDropOverwriteMode(False)
        self.ldplayer_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ldplayer_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.ldplayer_list.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.ldplayer_list.setShowGrid(True)
        self.ldplayer_list.setCornerButtonEnabled(True)
        self.ldplayer_list.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_4.addWidget(self.ldplayer_list, 0, 0, 1, 1)


        self.horizontalLayout_7.addWidget(self.ldplayer_list_widget)

        self.ldplayer_controller_widget = QGroupBox(self.dashboard_page)
        self.ldplayer_controller_widget.setObjectName(u"ldplayer_controller_widget")
        self.ldplayer_controller_widget.setStyleSheet(u"")
        self.gridLayout_3 = QGridLayout(self.ldplayer_controller_widget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_9 = QFrame(self.ldplayer_controller_widget)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_59 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_59.setSpacing(0)
        self.horizontalLayout_59.setObjectName(u"horizontalLayout_59")
        self.horizontalLayout_59.setContentsMargins(0, 0, 0, 0)
        self.ldplayer_path_line_edit_3 = QHBoxLayout()
        self.ldplayer_path_line_edit_3.setSpacing(0)
        self.ldplayer_path_line_edit_3.setObjectName(u"ldplayer_path_line_edit_3")
        self.ldplayer_path_line_edit_7 = QHBoxLayout()
        self.ldplayer_path_line_edit_7.setSpacing(9)
        self.ldplayer_path_line_edit_7.setObjectName(u"ldplayer_path_line_edit_7")
        self.label_26 = QLabel(self.frame_9)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.ldplayer_path_line_edit_7.addWidget(self.label_26)

        self.ld_per_row_2 = QSpinBox(self.frame_9)
        self.ld_per_row_2.setObjectName(u"ld_per_row_2")
        self.ld_per_row_2.setMinimumSize(QSize(100, 0))
        self.ld_per_row_2.setMinimum(4)

        self.ldplayer_path_line_edit_7.addWidget(self.ld_per_row_2)


        self.ldplayer_path_line_edit_3.addLayout(self.ldplayer_path_line_edit_7)

        self.frame_12 = QFrame(self.frame_9)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_60 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_60.setSpacing(0)
        self.horizontalLayout_60.setObjectName(u"horizontalLayout_60")
        self.horizontalLayout_60.setContentsMargins(0, 0, 0, 0)
        self.label_25 = QLabel(self.frame_12)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_60.addWidget(self.label_25)

        self.ld_per_row = QSpinBox(self.frame_12)
        self.ld_per_row.setObjectName(u"ld_per_row")
        self.ld_per_row.setMinimumSize(QSize(100, 0))
        self.ld_per_row.setMinimum(4)

        self.horizontalLayout_60.addWidget(self.ld_per_row)


        self.ldplayer_path_line_edit_3.addWidget(self.frame_12)


        self.horizontalLayout_59.addLayout(self.ldplayer_path_line_edit_3)


        self.gridLayout_3.addWidget(self.frame_9, 2, 0, 1, 1)

        self.option_checkbox_3 = QFrame(self.ldplayer_controller_widget)
        self.option_checkbox_3.setObjectName(u"option_checkbox_3")
        self.option_checkbox_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.option_checkbox_3.setFrameShape(QFrame.StyledPanel)
        self.option_checkbox_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.option_checkbox_3)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.active_accounts = QRadioButton(self.option_checkbox_3)
        self.active_accounts.setObjectName(u"active_accounts")
        self.active_accounts.setChecked(True)

        self.horizontalLayout_29.addWidget(self.active_accounts)

        self.reg_accounts = QRadioButton(self.option_checkbox_3)
        self.reg_accounts.setObjectName(u"reg_accounts")

        self.horizontalLayout_29.addWidget(self.reg_accounts)


        self.gridLayout_3.addWidget(self.option_checkbox_3, 4, 0, 1, 1)

        self.thread_option = QFrame(self.ldplayer_controller_widget)
        self.thread_option.setObjectName(u"thread_option")
        self.thread_option.setStyleSheet(u"")
        self.thread_option.setFrameShape(QFrame.StyledPanel)
        self.thread_option.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.thread_option)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.ldplayer_path_line_edit_2 = QHBoxLayout()
        self.ldplayer_path_line_edit_2.setSpacing(9)
        self.ldplayer_path_line_edit_2.setObjectName(u"ldplayer_path_line_edit_2")
        self.label_14 = QLabel(self.thread_option)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.ldplayer_path_line_edit_2.addWidget(self.label_14)

        self.delay_per_ld = QSpinBox(self.thread_option)
        self.delay_per_ld.setObjectName(u"delay_per_ld")
        self.delay_per_ld.setMinimumSize(QSize(100, 0))
        self.delay_per_ld.setMinimum(3)

        self.ldplayer_path_line_edit_2.addWidget(self.delay_per_ld)


        self.horizontalLayout_8.addLayout(self.ldplayer_path_line_edit_2)

        self.ldplayer_path_line_edit_4 = QHBoxLayout()
        self.ldplayer_path_line_edit_4.setObjectName(u"ldplayer_path_line_edit_4")
        self.label_16 = QLabel(self.thread_option)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.ldplayer_path_line_edit_4.addWidget(self.label_16)

        self.ld_per_column = QSpinBox(self.thread_option)
        self.ld_per_column.setObjectName(u"ld_per_column")
        self.ld_per_column.setMinimumSize(QSize(100, 0))
        self.ld_per_column.setFrame(True)
        self.ld_per_column.setMinimum(2)

        self.ldplayer_path_line_edit_4.addWidget(self.ld_per_column)


        self.horizontalLayout_8.addLayout(self.ldplayer_path_line_edit_4)


        self.gridLayout_3.addWidget(self.thread_option, 1, 0, 1, 1)

        self.ld_sleep_frame = QFrame(self.ldplayer_controller_widget)
        self.ld_sleep_frame.setObjectName(u"ld_sleep_frame")
        self.ld_sleep_frame.setStyleSheet(u"")
        self.ld_sleep_frame.setFrameShape(QFrame.StyledPanel)
        self.ld_sleep_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.ld_sleep_frame)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.ldplayer_path_line_edit_5 = QHBoxLayout()
        self.ldplayer_path_line_edit_5.setSpacing(9)
        self.ldplayer_path_line_edit_5.setObjectName(u"ldplayer_path_line_edit_5")
        self.label_17 = QLabel(self.ld_sleep_frame)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.ldplayer_path_line_edit_5.addWidget(self.label_17)

        self.ld_sleep = QSpinBox(self.ld_sleep_frame)
        self.ld_sleep.setObjectName(u"ld_sleep")
        self.ld_sleep.setMinimumSize(QSize(100, 0))

        self.ldplayer_path_line_edit_5.addWidget(self.ld_sleep)


        self.horizontalLayout_9.addLayout(self.ldplayer_path_line_edit_5)

        self.ldplayer_path_line_edit_6 = QHBoxLayout()
        self.ldplayer_path_line_edit_6.setObjectName(u"ldplayer_path_line_edit_6")
        self.label_18 = QLabel(self.ld_sleep_frame)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.ldplayer_path_line_edit_6.addWidget(self.label_18)

        self.loop = QSpinBox(self.ld_sleep_frame)
        self.loop.setObjectName(u"loop")
        self.loop.setMinimumSize(QSize(100, 0))
        self.loop.setFrame(True)

        self.ldplayer_path_line_edit_6.addWidget(self.loop)


        self.horizontalLayout_9.addLayout(self.ldplayer_path_line_edit_6)


        self.gridLayout_3.addWidget(self.ld_sleep_frame, 3, 0, 1, 1)

        self.option_checkbox = QFrame(self.ldplayer_controller_widget)
        self.option_checkbox.setObjectName(u"option_checkbox")
        self.option_checkbox.setFrameShape(QFrame.StyledPanel)
        self.option_checkbox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.option_checkbox)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.auto_expand_fit_active = QCheckBox(self.option_checkbox)
        self.auto_expand_fit_active.setObjectName(u"auto_expand_fit_active")
        self.auto_expand_fit_active.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.auto_expand_fit_active.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.auto_expand_fit_active.setChecked(False)

        self.horizontalLayout_10.addWidget(self.auto_expand_fit_active)

        self.backup_data_fb_ld = QCheckBox(self.option_checkbox)
        self.backup_data_fb_ld.setObjectName(u"backup_data_fb_ld")
        self.backup_data_fb_ld.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.backup_data_fb_ld.setChecked(False)

        self.horizontalLayout_10.addWidget(self.backup_data_fb_ld)

        self.auto_arrange_ldplayer = QCheckBox(self.option_checkbox)
        self.auto_arrange_ldplayer.setObjectName(u"auto_arrange_ldplayer")
        self.auto_arrange_ldplayer.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.auto_arrange_ldplayer.setChecked(False)

        self.horizontalLayout_10.addWidget(self.auto_arrange_ldplayer)


        self.gridLayout_3.addWidget(self.option_checkbox, 5, 0, 1, 1)

        self.option_checkbox_2 = QFrame(self.ldplayer_controller_widget)
        self.option_checkbox_2.setObjectName(u"option_checkbox_2")
        self.option_checkbox_2.setFrameShape(QFrame.StyledPanel)
        self.option_checkbox_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.option_checkbox_2)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.run_schedule_checkbox = QCheckBox(self.option_checkbox_2)
        self.run_schedule_checkbox.setObjectName(u"run_schedule_checkbox")
        self.run_schedule_checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.run_schedule_checkbox.setChecked(False)

        self.horizontalLayout_12.addWidget(self.run_schedule_checkbox)

        self.shop_tool_if_no_internet = QCheckBox(self.option_checkbox_2)
        self.shop_tool_if_no_internet.setObjectName(u"shop_tool_if_no_internet")
        self.shop_tool_if_no_internet.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.shop_tool_if_no_internet.setChecked(False)

        self.horizontalLayout_12.addWidget(self.shop_tool_if_no_internet)

        self.runing_ld_counter = QLabel(self.option_checkbox_2)
        self.runing_ld_counter.setObjectName(u"runing_ld_counter")
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(True)
        self.runing_ld_counter.setFont(font3)
        self.runing_ld_counter.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_12.addWidget(self.runing_ld_counter)


        self.gridLayout_3.addWidget(self.option_checkbox_2, 6, 0, 1, 1)

        self.ldplayer_path_line_edit = QHBoxLayout()
        self.ldplayer_path_line_edit.setObjectName(u"ldplayer_path_line_edit")
        self.label_13 = QLabel(self.ldplayer_controller_widget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.ldplayer_path_line_edit.addWidget(self.label_13)

        self.ldplayer_path = QLineEdit(self.ldplayer_controller_widget)
        self.ldplayer_path.setObjectName(u"ldplayer_path")

        self.ldplayer_path_line_edit.addWidget(self.ldplayer_path)

        self.browse_ld_path_btn = QPushButton(self.ldplayer_controller_widget)
        self.browse_ld_path_btn.setObjectName(u"browse_ld_path_btn")
        self.browse_ld_path_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.browse_ld_path_btn.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        icon5 = QIcon()
        icon5.addFile(u":/icons/images/folder.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.browse_ld_path_btn.setIcon(icon5)
        self.browse_ld_path_btn.setIconSize(QSize(20, 24))

        self.ldplayer_path_line_edit.addWidget(self.browse_ld_path_btn)

        self.refresh_ld = QPushButton(self.ldplayer_controller_widget)
        self.refresh_ld.setObjectName(u"refresh_ld")
        self.refresh_ld.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.refresh_ld.setStyleSheet(u"background-color: rgb(255, 85, 127);\n"
"background-color: rgb(255, 193, 7);\n"
"background-color: rgb(175, 128, 255);")
        icon6 = QIcon()
        icon6.addFile(u":/icons/images/refresh.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.refresh_ld.setIcon(icon6)
        self.refresh_ld.setIconSize(QSize(20, 24))

        self.ldplayer_path_line_edit.addWidget(self.refresh_ld)


        self.gridLayout_3.addLayout(self.ldplayer_path_line_edit, 0, 0, 1, 1)


        self.horizontalLayout_7.addWidget(self.ldplayer_controller_widget)


        self.gridLayout_2.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)

        self.Accounts_widget = QGroupBox(self.dashboard_page)
        self.Accounts_widget.setObjectName(u"Accounts_widget")
        font4 = QFont()
        font4.setPointSize(9)
        font4.setBold(True)
        self.Accounts_widget.setFont(font4)
        self.verticalLayout_6 = QVBoxLayout(self.Accounts_widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.bg_options = QWidget(self.Accounts_widget)
        self.bg_options.setObjectName(u"bg_options")
        self.bg_options.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.bg_options)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(12)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.switch_profile_page_combobox = QComboBox(self.bg_options)
        self.switch_profile_page_combobox.addItem("")
        self.switch_profile_page_combobox.addItem("")
        self.switch_profile_page_combobox.setObjectName(u"switch_profile_page_combobox")
        self.switch_profile_page_combobox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.switch_profile_page_combobox.setStyleSheet(u"background-color: rgb(125, 115, 127);")

        self.horizontalLayout_6.addWidget(self.switch_profile_page_combobox)

        self.refresh_table_accounts_dashboard = QPushButton(self.bg_options)
        self.refresh_table_accounts_dashboard.setObjectName(u"refresh_table_accounts_dashboard")
        self.refresh_table_accounts_dashboard.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.refresh_table_accounts_dashboard.setStyleSheet(u"background-color: rgb(85, 170, 0);")
        icon7 = QIcon()
        icon7.addFile(u":/icons/images/icons8-reload-64.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.refresh_table_accounts_dashboard.setIcon(icon7)
        self.refresh_table_accounts_dashboard.setIconSize(QSize(20, 20))

        self.horizontalLayout_6.addWidget(self.refresh_table_accounts_dashboard)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

        self.seleted_accounts_2 = QLabel(self.bg_options)
        self.seleted_accounts_2.setObjectName(u"seleted_accounts_2")
        font5 = QFont()
        font5.setBold(True)
        self.seleted_accounts_2.setFont(font5)
        self.seleted_accounts_2.setStyleSheet(u"background-color: rgb(255, 188, 218);")

        self.horizontalLayout_6.addWidget(self.seleted_accounts_2)

        self.seleted_accounts = QLabel(self.bg_options)
        self.seleted_accounts.setObjectName(u"seleted_accounts")
        self.seleted_accounts.setFont(font5)
        self.seleted_accounts.setStyleSheet(u"background-color: rgb(255, 188, 218);")

        self.horizontalLayout_6.addWidget(self.seleted_accounts)

        self.show_details = QCheckBox(self.bg_options)
        self.show_details.setObjectName(u"show_details")
        self.show_details.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_6.addWidget(self.show_details)


        self.gridLayout.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.category_filter_combobox = QComboBox(self.bg_options)
        self.category_filter_combobox.addItem("")
        self.category_filter_combobox.addItem("")
        self.category_filter_combobox.setObjectName(u"category_filter_combobox")
        self.category_filter_combobox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.category_filter_combobox.setStyleSheet(u"")
        self.category_filter_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_5.addWidget(self.category_filter_combobox)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.label_6 = QLabel(self.bg_options)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"background-color: rgb(255, 188, 218);")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.search_accs = QLineEdit(self.bg_options)
        self.search_accs.setObjectName(u"search_accs")

        self.horizontalLayout_5.addWidget(self.search_accs)

        self.enter_category_line_edit = QLineEdit(self.bg_options)
        self.enter_category_line_edit.setObjectName(u"enter_category_line_edit")

        self.horizontalLayout_5.addWidget(self.enter_category_line_edit)

        self.add_new_category_btn = QPushButton(self.bg_options)
        self.add_new_category_btn.setObjectName(u"add_new_category_btn")
        self.add_new_category_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.add_new_category_btn.setStyleSheet(u"")
        icon8 = QIcon()
        icon8.addFile(u":/icons/images/icons8-add-64.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.add_new_category_btn.setIcon(icon8)
        self.add_new_category_btn.setIconSize(QSize(20, 20))

        self.horizontalLayout_5.addWidget(self.add_new_category_btn)

        self.delete_category_btn = QPushButton(self.bg_options)
        self.delete_category_btn.setObjectName(u"delete_category_btn")
        self.delete_category_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.delete_category_btn.setStyleSheet(u"background-color: rgb(255, 0, 123);")
        icon9 = QIcon()
        icon9.addFile(u":/icons/images/icons8-delete-64.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.delete_category_btn.setIcon(icon9)
        self.delete_category_btn.setIconSize(QSize(20, 20))

        self.horizontalLayout_5.addWidget(self.delete_category_btn)


        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.bg_options)

        self.stacked_accounts = QStackedWidget(self.Accounts_widget)
        self.stacked_accounts.setObjectName(u"stacked_accounts")
        self.profile_table_widget = QWidget()
        self.profile_table_widget.setObjectName(u"profile_table_widget")
        self.formLayout = QFormLayout(self.profile_table_widget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(0)
        self.formLayout.setVerticalSpacing(0)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.profile_table_accounts = QTableView(self.profile_table_widget)
        self.profile_table_accounts.setObjectName(u"profile_table_accounts")
        font6 = QFont()
        font6.setFamilies([u"Noto Sans Khmer"])
        font6.setPointSize(9)
        font6.setBold(False)
        self.profile_table_accounts.setFont(font6)
        self.profile_table_accounts.setFocusPolicy(Qt.NoFocus)
        self.profile_table_accounts.setContextMenuPolicy(Qt.CustomContextMenu)
        self.profile_table_accounts.setLayoutDirection(Qt.LeftToRight)
        self.profile_table_accounts.setAutoFillBackground(False)
        self.profile_table_accounts.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.profile_table_accounts.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.profile_table_accounts.setDragDropOverwriteMode(False)
        self.profile_table_accounts.setAlternatingRowColors(True)
        self.profile_table_accounts.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.profile_table_accounts.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.profile_table_accounts.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.profile_table_accounts.setShowGrid(True)
        self.profile_table_accounts.setSortingEnabled(True)
        self.profile_table_accounts.horizontalHeader().setDefaultSectionSize(39)
        self.profile_table_accounts.horizontalHeader().setHighlightSections(True)
        self.profile_table_accounts.verticalHeader().setCascadingSectionResizes(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.profile_table_accounts)

        self.stacked_accounts.addWidget(self.profile_table_widget)
        self.profile_details_table_widget = QWidget()
        self.profile_details_table_widget.setObjectName(u"profile_details_table_widget")
        self.formLayout_2 = QFormLayout(self.profile_details_table_widget)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(0)
        self.formLayout_2.setVerticalSpacing(0)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.profile_table_details_accounts = QTableView(self.profile_details_table_widget)
        self.profile_table_details_accounts.setObjectName(u"profile_table_details_accounts")
        font7 = QFont()
        font7.setFamilies([u"Noto Sans Khmer"])
        font7.setBold(False)
        self.profile_table_details_accounts.setFont(font7)
        self.profile_table_details_accounts.setFocusPolicy(Qt.NoFocus)
        self.profile_table_details_accounts.setContextMenuPolicy(Qt.CustomContextMenu)
        self.profile_table_details_accounts.setLayoutDirection(Qt.LeftToRight)
        self.profile_table_details_accounts.setAutoFillBackground(False)
        self.profile_table_details_accounts.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.profile_table_details_accounts.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.profile_table_details_accounts.setDragDropOverwriteMode(False)
        self.profile_table_details_accounts.setAlternatingRowColors(True)
        self.profile_table_details_accounts.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.profile_table_details_accounts.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.profile_table_details_accounts.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.profile_table_details_accounts.setShowGrid(True)
        self.profile_table_details_accounts.setSortingEnabled(True)
        self.profile_table_details_accounts.setWordWrap(True)
        self.profile_table_details_accounts.horizontalHeader().setDefaultSectionSize(39)
        self.profile_table_details_accounts.horizontalHeader().setHighlightSections(True)
        self.profile_table_details_accounts.verticalHeader().setCascadingSectionResizes(True)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.profile_table_details_accounts)

        self.stacked_accounts.addWidget(self.profile_details_table_widget)
        self.page_table_widget = QWidget()
        self.page_table_widget.setObjectName(u"page_table_widget")
        self.formLayout_3 = QFormLayout(self.page_table_widget)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setHorizontalSpacing(0)
        self.formLayout_3.setVerticalSpacing(0)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pages_table_accounts = QTableView(self.page_table_widget)
        self.pages_table_accounts.setObjectName(u"pages_table_accounts")
        font8 = QFont()
        font8.setFamilies([u"Noto Sans Khmer"])
        font8.setBold(True)
        self.pages_table_accounts.setFont(font8)
        self.pages_table_accounts.setFocusPolicy(Qt.NoFocus)
        self.pages_table_accounts.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pages_table_accounts.setLayoutDirection(Qt.LeftToRight)
        self.pages_table_accounts.setAutoFillBackground(False)
        self.pages_table_accounts.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.pages_table_accounts.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.pages_table_accounts.setDragDropOverwriteMode(False)
        self.pages_table_accounts.setAlternatingRowColors(True)
        self.pages_table_accounts.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.pages_table_accounts.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.pages_table_accounts.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.pages_table_accounts.setShowGrid(True)
        self.pages_table_accounts.setSortingEnabled(True)
        self.pages_table_accounts.horizontalHeader().setDefaultSectionSize(46)
        self.pages_table_accounts.horizontalHeader().setHighlightSections(True)
        self.pages_table_accounts.verticalHeader().setCascadingSectionResizes(True)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.pages_table_accounts)

        self.stacked_accounts.addWidget(self.page_table_widget)

        self.verticalLayout_6.addWidget(self.stacked_accounts)


        self.gridLayout_2.addWidget(self.Accounts_widget, 0, 0, 1, 1)

        self.gridLayout_2.setRowStretch(0, 500)
        self.stacked_main.addWidget(self.dashboard_page)
        self.active_page = QWidget()
        self.active_page.setObjectName(u"active_page")
        self.gridLayout_6 = QGridLayout(self.active_page)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.active_page)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_25 = QGridLayout(self.groupBox)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.Watch_GroupBox = QFrame(self.groupBox)
        self.Watch_GroupBox.setObjectName(u"Watch_GroupBox")
        self.Watch_GroupBox.setFrameShape(QFrame.StyledPanel)
        self.Watch_GroupBox.setFrameShadow(QFrame.Raised)
        self.gridLayout_23 = QGridLayout(self.Watch_GroupBox)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.tabWidget_3 = QTabWidget(self.Watch_GroupBox)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_57 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_57.setObjectName(u"horizontalLayout_57")
        self.reels_group = QGroupBox(self.tab_2)
        self.reels_group.setObjectName(u"reels_group")
        self.reels_group.setEnabled(True)
        self.reels_group.setStyleSheet(u"")
        self.verticalLayout_14 = QVBoxLayout(self.reels_group)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.watch_feeds = QCheckBox(self.reels_group)
        self.watch_feeds.setObjectName(u"watch_feeds")
        self.watch_feeds.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_22.addWidget(self.watch_feeds)

        self.from_12 = QLabel(self.reels_group)
        self.from_12.setObjectName(u"from_12")
        self.from_12.setLayoutDirection(Qt.LeftToRight)
        self.from_12.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_22.addWidget(self.from_12)

        self.watch_feeds_from = QSpinBox(self.reels_group)
        self.watch_feeds_from.setObjectName(u"watch_feeds_from")
        self.watch_feeds_from.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_22.addWidget(self.watch_feeds_from)

        self.to_12 = QLabel(self.reels_group)
        self.to_12.setObjectName(u"to_12")
        self.to_12.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_12.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_22.addWidget(self.to_12)

        self.watch_feeds_to = QSpinBox(self.reels_group)
        self.watch_feeds_to.setObjectName(u"watch_feeds_to")
        self.watch_feeds_to.setMinimumSize(QSize(100, 0))
        self.watch_feeds_to.setMinimum(1)

        self.horizontalLayout_22.addWidget(self.watch_feeds_to)

        self.horizontalLayout_22.setStretch(0, 11)
        self.horizontalLayout_22.setStretch(1, 1)

        self.horizontalLayout_23.addLayout(self.horizontalLayout_22)


        self.verticalLayout_14.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_3 = QLabel(self.reels_group)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_24.addWidget(self.label_3)

        self.from_14 = QLabel(self.reels_group)
        self.from_14.setObjectName(u"from_14")
        self.from_14.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_24.addWidget(self.from_14)

        self.delay_watch_feeds_from = QSpinBox(self.reels_group)
        self.delay_watch_feeds_from.setObjectName(u"delay_watch_feeds_from")
        self.delay_watch_feeds_from.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_24.addWidget(self.delay_watch_feeds_from)

        self.to_14 = QLabel(self.reels_group)
        self.to_14.setObjectName(u"to_14")
        self.to_14.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_14.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_24.addWidget(self.to_14)

        self.delay_watch_feeds_to = QSpinBox(self.reels_group)
        self.delay_watch_feeds_to.setObjectName(u"delay_watch_feeds_to")
        self.delay_watch_feeds_to.setMinimumSize(QSize(100, 0))
        self.delay_watch_feeds_to.setMinimum(1)

        self.horizontalLayout_24.addWidget(self.delay_watch_feeds_to)

        self.horizontalLayout_24.setStretch(0, 1)

        self.verticalLayout_14.addLayout(self.horizontalLayout_24)

        self.verticalLayout_23 = QVBoxLayout()
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.feeds_no_emoji = QRadioButton(self.reels_group)
        self.feeds_no_emoji.setObjectName(u"feeds_no_emoji")
        self.feeds_no_emoji.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.feeds_no_emoji.setChecked(True)

        self.verticalLayout_23.addWidget(self.feeds_no_emoji)

        self.feeds_alway_emoji = QRadioButton(self.reels_group)
        self.feeds_alway_emoji.setObjectName(u"feeds_alway_emoji")
        self.feeds_alway_emoji.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.verticalLayout_23.addWidget(self.feeds_alway_emoji)

        self.feeds_random_emoji = QRadioButton(self.reels_group)
        self.feeds_random_emoji.setObjectName(u"feeds_random_emoji")
        self.feeds_random_emoji.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.verticalLayout_23.addWidget(self.feeds_random_emoji)


        self.verticalLayout_14.addLayout(self.verticalLayout_23)


        self.horizontalLayout_57.addWidget(self.reels_group)

        self.react_group_2 = QGroupBox(self.tab_2)
        self.react_group_2.setObjectName(u"react_group_2")
        self.react_group_2.setStyleSheet(u"background-color: rgb(213, 242, 250);")
        self.verticalLayout_13 = QVBoxLayout(self.react_group_2)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.feeds_like = QCheckBox(self.react_group_2)
        self.feeds_like.setObjectName(u"feeds_like")
        self.feeds_like.setStyleSheet(u"")
        icon10 = QIcon()
        icon10.addFile(u":/icons/images/like_emoji.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.feeds_like.setIcon(icon10)
        self.feeds_like.setIconSize(QSize(30, 30))
        self.feeds_like.setChecked(False)

        self.horizontalLayout_30.addWidget(self.feeds_like)

        self.from_label_2 = QLabel(self.react_group_2)
        self.from_label_2.setObjectName(u"from_label_2")
        self.from_label_2.setStyleSheet(u"")

        self.horizontalLayout_30.addWidget(self.from_label_2)

        self.feeds_like_from = QSpinBox(self.react_group_2)
        self.feeds_like_from.setObjectName(u"feeds_like_from")
        self.feeds_like_from.setMinimumSize(QSize(100, 0))
        self.feeds_like_from.setStyleSheet(u"\n"
"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_30.addWidget(self.feeds_like_from)

        self.to_label_2 = QLabel(self.react_group_2)
        self.to_label_2.setObjectName(u"to_label_2")
        self.to_label_2.setStyleSheet(u"")
        self.to_label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_30.addWidget(self.to_label_2)

        self.feeds_like_to = QSpinBox(self.react_group_2)
        self.feeds_like_to.setObjectName(u"feeds_like_to")
        self.feeds_like_to.setMinimumSize(QSize(100, 0))
        self.feeds_like_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.feeds_like_to.setMinimum(1)

        self.horizontalLayout_30.addWidget(self.feeds_like_to)


        self.verticalLayout_13.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.feeds_love = QCheckBox(self.react_group_2)
        self.feeds_love.setObjectName(u"feeds_love")
        self.feeds_love.setStyleSheet(u"")
        icon11 = QIcon()
        icon11.addFile(u":/icons/images/love_emoji.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.feeds_love.setIcon(icon11)
        self.feeds_love.setIconSize(QSize(30, 30))
        self.feeds_love.setChecked(False)

        self.horizontalLayout_34.addWidget(self.feeds_love)

        self.from_4 = QLabel(self.react_group_2)
        self.from_4.setObjectName(u"from_4")
        self.from_4.setStyleSheet(u"")

        self.horizontalLayout_34.addWidget(self.from_4)

        self.feeds_love_from = QSpinBox(self.react_group_2)
        self.feeds_love_from.setObjectName(u"feeds_love_from")
        self.feeds_love_from.setMinimumSize(QSize(100, 0))
        self.feeds_love_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_34.addWidget(self.feeds_love_from)

        self.to_4 = QLabel(self.react_group_2)
        self.to_4.setObjectName(u"to_4")
        self.to_4.setStyleSheet(u"")
        self.to_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_34.addWidget(self.to_4)

        self.feeds_love_to = QSpinBox(self.react_group_2)
        self.feeds_love_to.setObjectName(u"feeds_love_to")
        self.feeds_love_to.setMinimumSize(QSize(100, 0))
        self.feeds_love_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.feeds_love_to.setMinimum(1)

        self.horizontalLayout_34.addWidget(self.feeds_love_to)


        self.verticalLayout_13.addLayout(self.horizontalLayout_34)

        self.horizontalLayout_46 = QHBoxLayout()
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.feeds_haha = QCheckBox(self.react_group_2)
        self.feeds_haha.setObjectName(u"feeds_haha")
        self.feeds_haha.setStyleSheet(u"")
        icon12 = QIcon()
        icon12.addFile(u":/icons/images/haha_emoji.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.feeds_haha.setIcon(icon12)
        self.feeds_haha.setIconSize(QSize(30, 30))
        self.feeds_haha.setChecked(False)

        self.horizontalLayout_46.addWidget(self.feeds_haha)

        self.from_5 = QLabel(self.react_group_2)
        self.from_5.setObjectName(u"from_5")
        self.from_5.setStyleSheet(u"")

        self.horizontalLayout_46.addWidget(self.from_5)

        self.feeds_haha_from = QSpinBox(self.react_group_2)
        self.feeds_haha_from.setObjectName(u"feeds_haha_from")
        self.feeds_haha_from.setMinimumSize(QSize(100, 0))
        self.feeds_haha_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_46.addWidget(self.feeds_haha_from)

        self.to_5 = QLabel(self.react_group_2)
        self.to_5.setObjectName(u"to_5")
        self.to_5.setStyleSheet(u"")
        self.to_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_46.addWidget(self.to_5)

        self.feeds_haha_to = QSpinBox(self.react_group_2)
        self.feeds_haha_to.setObjectName(u"feeds_haha_to")
        self.feeds_haha_to.setMinimumSize(QSize(100, 0))
        self.feeds_haha_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.feeds_haha_to.setMinimum(1)

        self.horizontalLayout_46.addWidget(self.feeds_haha_to)


        self.verticalLayout_13.addLayout(self.horizontalLayout_46)

        self.horizontalLayout_47 = QHBoxLayout()
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.feeds_cry = QCheckBox(self.react_group_2)
        self.feeds_cry.setObjectName(u"feeds_cry")
        self.feeds_cry.setStyleSheet(u"")
        icon13 = QIcon()
        icon13.addFile(u":/icons/images/cry_emoji.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.feeds_cry.setIcon(icon13)
        self.feeds_cry.setIconSize(QSize(30, 30))
        self.feeds_cry.setChecked(False)

        self.horizontalLayout_47.addWidget(self.feeds_cry)

        self.from_8 = QLabel(self.react_group_2)
        self.from_8.setObjectName(u"from_8")
        self.from_8.setStyleSheet(u"")

        self.horizontalLayout_47.addWidget(self.from_8)

        self.feeds_cry_from = QSpinBox(self.react_group_2)
        self.feeds_cry_from.setObjectName(u"feeds_cry_from")
        self.feeds_cry_from.setMinimumSize(QSize(100, 0))
        self.feeds_cry_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_47.addWidget(self.feeds_cry_from)

        self.to_8 = QLabel(self.react_group_2)
        self.to_8.setObjectName(u"to_8")
        self.to_8.setStyleSheet(u"")
        self.to_8.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_47.addWidget(self.to_8)

        self.feeds_cry_to = QSpinBox(self.react_group_2)
        self.feeds_cry_to.setObjectName(u"feeds_cry_to")
        self.feeds_cry_to.setMinimumSize(QSize(100, 0))
        self.feeds_cry_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.feeds_cry_to.setMinimum(1)

        self.horizontalLayout_47.addWidget(self.feeds_cry_to)


        self.verticalLayout_13.addLayout(self.horizontalLayout_47)

        self.horizontalLayout_48 = QHBoxLayout()
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.feeds_angry = QCheckBox(self.react_group_2)
        self.feeds_angry.setObjectName(u"feeds_angry")
        self.feeds_angry.setStyleSheet(u"")
        icon14 = QIcon()
        icon14.addFile(u":/icons/images/angry_emoji.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.feeds_angry.setIcon(icon14)
        self.feeds_angry.setIconSize(QSize(30, 30))
        self.feeds_angry.setChecked(False)

        self.horizontalLayout_48.addWidget(self.feeds_angry)

        self.from_9 = QLabel(self.react_group_2)
        self.from_9.setObjectName(u"from_9")
        self.from_9.setStyleSheet(u"")

        self.horizontalLayout_48.addWidget(self.from_9)

        self.feeds_angry_from = QSpinBox(self.react_group_2)
        self.feeds_angry_from.setObjectName(u"feeds_angry_from")
        self.feeds_angry_from.setMinimumSize(QSize(100, 0))
        self.feeds_angry_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_48.addWidget(self.feeds_angry_from)

        self.to_9 = QLabel(self.react_group_2)
        self.to_9.setObjectName(u"to_9")
        self.to_9.setStyleSheet(u"")
        self.to_9.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_48.addWidget(self.to_9)

        self.feeds_angry_to = QSpinBox(self.react_group_2)
        self.feeds_angry_to.setObjectName(u"feeds_angry_to")
        self.feeds_angry_to.setMinimumSize(QSize(100, 0))
        self.feeds_angry_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.feeds_angry_to.setMinimum(1)

        self.horizontalLayout_48.addWidget(self.feeds_angry_to)


        self.verticalLayout_13.addLayout(self.horizontalLayout_48)


        self.horizontalLayout_57.addWidget(self.react_group_2)

        self.tabWidget_3.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.horizontalLayout_38 = QHBoxLayout(self.tab_3)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.vidos_group = QGroupBox(self.tab_3)
        self.vidos_group.setObjectName(u"vidos_group")
        self.vidos_group.setEnabled(True)
        self.vidos_group.setStyleSheet(u"")
        self.verticalLayout_16 = QVBoxLayout(self.vidos_group)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.watch_videos = QCheckBox(self.vidos_group)
        self.watch_videos.setObjectName(u"watch_videos")
        self.watch_videos.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.watch_videos.setIconSize(QSize(30, 30))
        self.watch_videos.setChecked(False)

        self.horizontalLayout_32.addWidget(self.watch_videos)

        self.from_16 = QLabel(self.vidos_group)
        self.from_16.setObjectName(u"from_16")
        self.from_16.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_32.addWidget(self.from_16)

        self.watch_videos_from = QSpinBox(self.vidos_group)
        self.watch_videos_from.setObjectName(u"watch_videos_from")
        self.watch_videos_from.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_32.addWidget(self.watch_videos_from)

        self.to_16 = QLabel(self.vidos_group)
        self.to_16.setObjectName(u"to_16")
        self.to_16.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_16.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_32.addWidget(self.to_16)

        self.watch_videos_to = QSpinBox(self.vidos_group)
        self.watch_videos_to.setObjectName(u"watch_videos_to")
        self.watch_videos_to.setMinimumSize(QSize(100, 0))
        self.watch_videos_to.setMinimum(1)

        self.horizontalLayout_32.addWidget(self.watch_videos_to)

        self.horizontalLayout_32.setStretch(0, 1)

        self.horizontalLayout_31.addLayout(self.horizontalLayout_32)


        self.verticalLayout_16.addLayout(self.horizontalLayout_31)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.label_24 = QLabel(self.vidos_group)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_33.addWidget(self.label_24)

        self.from_17 = QLabel(self.vidos_group)
        self.from_17.setObjectName(u"from_17")
        self.from_17.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_33.addWidget(self.from_17)

        self.delay_watch_video_from = QSpinBox(self.vidos_group)
        self.delay_watch_video_from.setObjectName(u"delay_watch_video_from")
        self.delay_watch_video_from.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_33.addWidget(self.delay_watch_video_from)

        self.to_17 = QLabel(self.vidos_group)
        self.to_17.setObjectName(u"to_17")
        self.to_17.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_17.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_33.addWidget(self.to_17)

        self.delay_watch_video_to = QSpinBox(self.vidos_group)
        self.delay_watch_video_to.setObjectName(u"delay_watch_video_to")
        self.delay_watch_video_to.setMinimumSize(QSize(100, 0))
        self.delay_watch_video_to.setMinimum(1)

        self.horizontalLayout_33.addWidget(self.delay_watch_video_to)


        self.verticalLayout_16.addLayout(self.horizontalLayout_33)

        self.verticalLayout_22 = QVBoxLayout()
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.videos_no_emoji = QRadioButton(self.vidos_group)
        self.videos_no_emoji.setObjectName(u"videos_no_emoji")
        self.videos_no_emoji.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.videos_no_emoji.setChecked(True)

        self.verticalLayout_22.addWidget(self.videos_no_emoji)

        self.videos_alway_emoji = QRadioButton(self.vidos_group)
        self.videos_alway_emoji.setObjectName(u"videos_alway_emoji")
        self.videos_alway_emoji.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.verticalLayout_22.addWidget(self.videos_alway_emoji)

        self.videos_random_emoji = QRadioButton(self.vidos_group)
        self.videos_random_emoji.setObjectName(u"videos_random_emoji")
        self.videos_random_emoji.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.verticalLayout_22.addWidget(self.videos_random_emoji)


        self.verticalLayout_16.addLayout(self.verticalLayout_22)


        self.horizontalLayout_38.addWidget(self.vidos_group)

        self.react_group_3 = QGroupBox(self.tab_3)
        self.react_group_3.setObjectName(u"react_group_3")
        self.react_group_3.setStyleSheet(u"background-color: rgb(213, 242, 250);")
        self.verticalLayout_15 = QVBoxLayout(self.react_group_3)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_49 = QHBoxLayout()
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.videos_like = QCheckBox(self.react_group_3)
        self.videos_like.setObjectName(u"videos_like")
        self.videos_like.setStyleSheet(u"")
        self.videos_like.setIcon(icon10)
        self.videos_like.setIconSize(QSize(30, 30))
        self.videos_like.setChecked(False)

        self.horizontalLayout_49.addWidget(self.videos_like)

        self.from_label_3 = QLabel(self.react_group_3)
        self.from_label_3.setObjectName(u"from_label_3")
        self.from_label_3.setStyleSheet(u"")

        self.horizontalLayout_49.addWidget(self.from_label_3)

        self.videos_like_from = QSpinBox(self.react_group_3)
        self.videos_like_from.setObjectName(u"videos_like_from")
        self.videos_like_from.setMinimumSize(QSize(100, 0))
        self.videos_like_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_49.addWidget(self.videos_like_from)

        self.to_label_3 = QLabel(self.react_group_3)
        self.to_label_3.setObjectName(u"to_label_3")
        self.to_label_3.setStyleSheet(u"")
        self.to_label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_49.addWidget(self.to_label_3)

        self.videos_like_to = QSpinBox(self.react_group_3)
        self.videos_like_to.setObjectName(u"videos_like_to")
        self.videos_like_to.setMinimumSize(QSize(100, 0))
        self.videos_like_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.videos_like_to.setMinimum(1)

        self.horizontalLayout_49.addWidget(self.videos_like_to)


        self.verticalLayout_15.addLayout(self.horizontalLayout_49)

        self.horizontalLayout_50 = QHBoxLayout()
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.videos_love = QCheckBox(self.react_group_3)
        self.videos_love.setObjectName(u"videos_love")
        self.videos_love.setStyleSheet(u"")
        self.videos_love.setIcon(icon11)
        self.videos_love.setIconSize(QSize(30, 30))
        self.videos_love.setChecked(False)

        self.horizontalLayout_50.addWidget(self.videos_love)

        self.from_10 = QLabel(self.react_group_3)
        self.from_10.setObjectName(u"from_10")
        self.from_10.setStyleSheet(u"")

        self.horizontalLayout_50.addWidget(self.from_10)

        self.videos_love_from = QSpinBox(self.react_group_3)
        self.videos_love_from.setObjectName(u"videos_love_from")
        self.videos_love_from.setMinimumSize(QSize(100, 0))
        self.videos_love_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_50.addWidget(self.videos_love_from)

        self.to_10 = QLabel(self.react_group_3)
        self.to_10.setObjectName(u"to_10")
        self.to_10.setStyleSheet(u"")
        self.to_10.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_50.addWidget(self.to_10)

        self.videos_love_to = QSpinBox(self.react_group_3)
        self.videos_love_to.setObjectName(u"videos_love_to")
        self.videos_love_to.setMinimumSize(QSize(100, 0))
        self.videos_love_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.videos_love_to.setMinimum(1)

        self.horizontalLayout_50.addWidget(self.videos_love_to)


        self.verticalLayout_15.addLayout(self.horizontalLayout_50)

        self.horizontalLayout_51 = QHBoxLayout()
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.videos_haha = QCheckBox(self.react_group_3)
        self.videos_haha.setObjectName(u"videos_haha")
        self.videos_haha.setStyleSheet(u"")
        self.videos_haha.setIcon(icon12)
        self.videos_haha.setIconSize(QSize(30, 30))
        self.videos_haha.setChecked(False)

        self.horizontalLayout_51.addWidget(self.videos_haha)

        self.from_11 = QLabel(self.react_group_3)
        self.from_11.setObjectName(u"from_11")
        self.from_11.setStyleSheet(u"")

        self.horizontalLayout_51.addWidget(self.from_11)

        self.videos_haha_from = QSpinBox(self.react_group_3)
        self.videos_haha_from.setObjectName(u"videos_haha_from")
        self.videos_haha_from.setMinimumSize(QSize(100, 0))
        self.videos_haha_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_51.addWidget(self.videos_haha_from)

        self.to_11 = QLabel(self.react_group_3)
        self.to_11.setObjectName(u"to_11")
        self.to_11.setStyleSheet(u"")
        self.to_11.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_51.addWidget(self.to_11)

        self.videos_haha_to = QSpinBox(self.react_group_3)
        self.videos_haha_to.setObjectName(u"videos_haha_to")
        self.videos_haha_to.setMinimumSize(QSize(100, 0))
        self.videos_haha_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.videos_haha_to.setMinimum(1)

        self.horizontalLayout_51.addWidget(self.videos_haha_to)


        self.verticalLayout_15.addLayout(self.horizontalLayout_51)

        self.horizontalLayout_52 = QHBoxLayout()
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.videos_cry = QCheckBox(self.react_group_3)
        self.videos_cry.setObjectName(u"videos_cry")
        self.videos_cry.setStyleSheet(u"")
        self.videos_cry.setIcon(icon13)
        self.videos_cry.setIconSize(QSize(30, 30))
        self.videos_cry.setChecked(False)

        self.horizontalLayout_52.addWidget(self.videos_cry)

        self.from_18 = QLabel(self.react_group_3)
        self.from_18.setObjectName(u"from_18")
        self.from_18.setStyleSheet(u"")

        self.horizontalLayout_52.addWidget(self.from_18)

        self.videos_cry_from = QSpinBox(self.react_group_3)
        self.videos_cry_from.setObjectName(u"videos_cry_from")
        self.videos_cry_from.setMinimumSize(QSize(100, 0))
        self.videos_cry_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_52.addWidget(self.videos_cry_from)

        self.to_18 = QLabel(self.react_group_3)
        self.to_18.setObjectName(u"to_18")
        self.to_18.setStyleSheet(u"")
        self.to_18.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_52.addWidget(self.to_18)

        self.videos_cry_to = QSpinBox(self.react_group_3)
        self.videos_cry_to.setObjectName(u"videos_cry_to")
        self.videos_cry_to.setMinimumSize(QSize(100, 0))
        self.videos_cry_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.videos_cry_to.setMinimum(1)

        self.horizontalLayout_52.addWidget(self.videos_cry_to)


        self.verticalLayout_15.addLayout(self.horizontalLayout_52)

        self.horizontalLayout_53 = QHBoxLayout()
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.videos_angry = QCheckBox(self.react_group_3)
        self.videos_angry.setObjectName(u"videos_angry")
        self.videos_angry.setStyleSheet(u"")
        self.videos_angry.setIcon(icon14)
        self.videos_angry.setIconSize(QSize(30, 30))
        self.videos_angry.setChecked(False)

        self.horizontalLayout_53.addWidget(self.videos_angry)

        self.from_24 = QLabel(self.react_group_3)
        self.from_24.setObjectName(u"from_24")
        self.from_24.setStyleSheet(u"")

        self.horizontalLayout_53.addWidget(self.from_24)

        self.videos_angry_from = QSpinBox(self.react_group_3)
        self.videos_angry_from.setObjectName(u"videos_angry_from")
        self.videos_angry_from.setMinimumSize(QSize(100, 0))
        self.videos_angry_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_53.addWidget(self.videos_angry_from)

        self.to_24 = QLabel(self.react_group_3)
        self.to_24.setObjectName(u"to_24")
        self.to_24.setStyleSheet(u"")
        self.to_24.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_53.addWidget(self.to_24)

        self.videos_angry_to = QSpinBox(self.react_group_3)
        self.videos_angry_to.setObjectName(u"videos_angry_to")
        self.videos_angry_to.setMinimumSize(QSize(100, 0))
        self.videos_angry_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.videos_angry_to.setMinimum(1)

        self.horizontalLayout_53.addWidget(self.videos_angry_to)


        self.verticalLayout_15.addLayout(self.horizontalLayout_53)


        self.horizontalLayout_38.addWidget(self.react_group_3)

        self.tabWidget_3.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.horizontalLayout_35 = QHBoxLayout(self.tab_4)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.reels_group_2 = QGroupBox(self.tab_4)
        self.reels_group_2.setObjectName(u"reels_group_2")
        self.reels_group_2.setEnabled(True)
        self.reels_group_2.setStyleSheet(u"background-color: rgb(213, 242, 250);")
        self.verticalLayout_20 = QVBoxLayout(self.reels_group_2)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.horizontalLayout_63 = QHBoxLayout()
        self.horizontalLayout_63.setObjectName(u"horizontalLayout_63")
        self.horizontalLayout_64 = QHBoxLayout()
        self.horizontalLayout_64.setObjectName(u"horizontalLayout_64")
        self.story = QCheckBox(self.reels_group_2)
        self.story.setObjectName(u"story")

        self.horizontalLayout_64.addWidget(self.story)

        self.from_31 = QLabel(self.reels_group_2)
        self.from_31.setObjectName(u"from_31")
        self.from_31.setLayoutDirection(Qt.LeftToRight)
        self.from_31.setStyleSheet(u"")

        self.horizontalLayout_64.addWidget(self.from_31)

        self.story_from = QSpinBox(self.reels_group_2)
        self.story_from.setObjectName(u"story_from")
        self.story_from.setMinimumSize(QSize(100, 0))
        self.story_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_64.addWidget(self.story_from)

        self.to_31 = QLabel(self.reels_group_2)
        self.to_31.setObjectName(u"to_31")
        self.to_31.setStyleSheet(u"")
        self.to_31.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_64.addWidget(self.to_31)

        self.story_to = QSpinBox(self.reels_group_2)
        self.story_to.setObjectName(u"story_to")
        self.story_to.setMinimumSize(QSize(100, 0))
        self.story_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_64.addWidget(self.story_to)

        self.horizontalLayout_64.setStretch(0, 10)

        self.horizontalLayout_63.addLayout(self.horizontalLayout_64)


        self.verticalLayout_20.addLayout(self.horizontalLayout_63)

        self.frame_3 = QFrame(self.reels_group_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_3)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.reply_story = QCheckBox(self.frame_3)
        self.reply_story.setObjectName(u"reply_story")
        self.reply_story.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.reply_story, 0, 0, 1, 1)

        self.from_32 = QLabel(self.frame_3)
        self.from_32.setObjectName(u"from_32")
        self.from_32.setLayoutDirection(Qt.LeftToRight)
        self.from_32.setStyleSheet(u"")

        self.gridLayout_8.addWidget(self.from_32, 0, 1, 1, 1)

        self.reply_story_from = QSpinBox(self.frame_3)
        self.reply_story_from.setObjectName(u"reply_story_from")
        self.reply_story_from.setMinimumSize(QSize(100, 0))
        self.reply_story_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.gridLayout_8.addWidget(self.reply_story_from, 0, 2, 1, 1)

        self.to_32 = QLabel(self.frame_3)
        self.to_32.setObjectName(u"to_32")
        self.to_32.setStyleSheet(u"")
        self.to_32.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.to_32, 0, 3, 1, 1)

        self.reply_story_to = QSpinBox(self.frame_3)
        self.reply_story_to.setObjectName(u"reply_story_to")
        self.reply_story_to.setMinimumSize(QSize(100, 0))
        self.reply_story_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.gridLayout_8.addWidget(self.reply_story_to, 0, 4, 1, 1)

        self.gridLayout_8.setColumnStretch(0, 10)

        self.verticalLayout_20.addWidget(self.frame_3)

        self.reply_story_text = QPlainTextEdit(self.reels_group_2)
        self.reply_story_text.setObjectName(u"reply_story_text")
        self.reply_story_text.setFont(font2)
        self.reply_story_text.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_20.addWidget(self.reply_story_text)

        self.gridLayout_26 = QGridLayout()
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.reply_story_no_emoji = QRadioButton(self.reels_group_2)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.reply_story_no_emoji)
        self.reply_story_no_emoji.setObjectName(u"reply_story_no_emoji")
        self.reply_story_no_emoji.setStyleSheet(u"")
        self.reply_story_no_emoji.setChecked(True)

        self.gridLayout_26.addWidget(self.reply_story_no_emoji, 0, 0, 1, 1)

        self.reply_story_alway_emoji = QRadioButton(self.reels_group_2)
        self.buttonGroup.addButton(self.reply_story_alway_emoji)
        self.reply_story_alway_emoji.setObjectName(u"reply_story_alway_emoji")
        self.reply_story_alway_emoji.setStyleSheet(u"")

        self.gridLayout_26.addWidget(self.reply_story_alway_emoji, 0, 1, 1, 1)

        self.reply_story_ramdom_emoji = QRadioButton(self.reels_group_2)
        self.buttonGroup.addButton(self.reply_story_ramdom_emoji)
        self.reply_story_ramdom_emoji.setObjectName(u"reply_story_ramdom_emoji")
        self.reply_story_ramdom_emoji.setStyleSheet(u"")

        self.gridLayout_26.addWidget(self.reply_story_ramdom_emoji, 0, 2, 1, 1)


        self.verticalLayout_20.addLayout(self.gridLayout_26)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_20.addItem(self.verticalSpacer_5)


        self.horizontalLayout_35.addWidget(self.reels_group_2)

        self.react_group_5 = QGroupBox(self.tab_4)
        self.react_group_5.setObjectName(u"react_group_5")
        self.react_group_5.setStyleSheet(u"background-color: rgb(213, 242, 250);")
        self.verticalLayout_21 = QVBoxLayout(self.react_group_5)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.horizontalLayout_66 = QHBoxLayout()
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.reply_story_like = QCheckBox(self.react_group_5)
        self.reply_story_like.setObjectName(u"reply_story_like")
        self.reply_story_like.setStyleSheet(u"")
        self.reply_story_like.setIcon(icon10)
        self.reply_story_like.setIconSize(QSize(30, 30))
        self.reply_story_like.setChecked(False)

        self.horizontalLayout_66.addWidget(self.reply_story_like)

        self.from_label_5 = QLabel(self.react_group_5)
        self.from_label_5.setObjectName(u"from_label_5")
        self.from_label_5.setStyleSheet(u"")

        self.horizontalLayout_66.addWidget(self.from_label_5)

        self.reply_story_like_from = QSpinBox(self.react_group_5)
        self.reply_story_like_from.setObjectName(u"reply_story_like_from")
        self.reply_story_like_from.setMinimumSize(QSize(100, 0))
        self.reply_story_like_from.setStyleSheet(u"\n"
"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_66.addWidget(self.reply_story_like_from)

        self.to_label_5 = QLabel(self.react_group_5)
        self.to_label_5.setObjectName(u"to_label_5")
        self.to_label_5.setStyleSheet(u"")
        self.to_label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_66.addWidget(self.to_label_5)

        self.reply_story_like_to = QSpinBox(self.react_group_5)
        self.reply_story_like_to.setObjectName(u"reply_story_like_to")
        self.reply_story_like_to.setMinimumSize(QSize(100, 0))
        self.reply_story_like_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_66.addWidget(self.reply_story_like_to)


        self.verticalLayout_21.addLayout(self.horizontalLayout_66)

        self.horizontalLayout_67 = QHBoxLayout()
        self.horizontalLayout_67.setObjectName(u"horizontalLayout_67")
        self.reply_story_love = QCheckBox(self.react_group_5)
        self.reply_story_love.setObjectName(u"reply_story_love")
        self.reply_story_love.setStyleSheet(u"")
        self.reply_story_love.setIcon(icon11)
        self.reply_story_love.setIconSize(QSize(30, 30))
        self.reply_story_love.setChecked(False)

        self.horizontalLayout_67.addWidget(self.reply_story_love)

        self.from_33 = QLabel(self.react_group_5)
        self.from_33.setObjectName(u"from_33")
        self.from_33.setStyleSheet(u"")

        self.horizontalLayout_67.addWidget(self.from_33)

        self.reply_story_love_from = QSpinBox(self.react_group_5)
        self.reply_story_love_from.setObjectName(u"reply_story_love_from")
        self.reply_story_love_from.setMinimumSize(QSize(100, 0))
        self.reply_story_love_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_67.addWidget(self.reply_story_love_from)

        self.to_33 = QLabel(self.react_group_5)
        self.to_33.setObjectName(u"to_33")
        self.to_33.setStyleSheet(u"")
        self.to_33.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_67.addWidget(self.to_33)

        self.reply_story_love_to = QSpinBox(self.react_group_5)
        self.reply_story_love_to.setObjectName(u"reply_story_love_to")
        self.reply_story_love_to.setMinimumSize(QSize(100, 0))
        self.reply_story_love_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_67.addWidget(self.reply_story_love_to)


        self.verticalLayout_21.addLayout(self.horizontalLayout_67)

        self.horizontalLayout_68 = QHBoxLayout()
        self.horizontalLayout_68.setObjectName(u"horizontalLayout_68")
        self.reply_story_haha = QCheckBox(self.react_group_5)
        self.reply_story_haha.setObjectName(u"reply_story_haha")
        self.reply_story_haha.setStyleSheet(u"")
        self.reply_story_haha.setIcon(icon12)
        self.reply_story_haha.setIconSize(QSize(30, 30))
        self.reply_story_haha.setChecked(False)

        self.horizontalLayout_68.addWidget(self.reply_story_haha)

        self.from_34 = QLabel(self.react_group_5)
        self.from_34.setObjectName(u"from_34")
        self.from_34.setStyleSheet(u"")

        self.horizontalLayout_68.addWidget(self.from_34)

        self.reply_story_haha_from = QSpinBox(self.react_group_5)
        self.reply_story_haha_from.setObjectName(u"reply_story_haha_from")
        self.reply_story_haha_from.setMinimumSize(QSize(100, 0))
        self.reply_story_haha_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_68.addWidget(self.reply_story_haha_from)

        self.to_34 = QLabel(self.react_group_5)
        self.to_34.setObjectName(u"to_34")
        self.to_34.setStyleSheet(u"")
        self.to_34.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_68.addWidget(self.to_34)

        self.reply_story_haha_to = QSpinBox(self.react_group_5)
        self.reply_story_haha_to.setObjectName(u"reply_story_haha_to")
        self.reply_story_haha_to.setMinimumSize(QSize(100, 0))
        self.reply_story_haha_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_68.addWidget(self.reply_story_haha_to)


        self.verticalLayout_21.addLayout(self.horizontalLayout_68)

        self.horizontalLayout_69 = QHBoxLayout()
        self.horizontalLayout_69.setObjectName(u"horizontalLayout_69")
        self.reply_story_cry = QCheckBox(self.react_group_5)
        self.reply_story_cry.setObjectName(u"reply_story_cry")
        self.reply_story_cry.setStyleSheet(u"")
        self.reply_story_cry.setIcon(icon13)
        self.reply_story_cry.setIconSize(QSize(30, 30))
        self.reply_story_cry.setChecked(False)

        self.horizontalLayout_69.addWidget(self.reply_story_cry)

        self.from_35 = QLabel(self.react_group_5)
        self.from_35.setObjectName(u"from_35")
        self.from_35.setStyleSheet(u"")

        self.horizontalLayout_69.addWidget(self.from_35)

        self.reply_story_cry_from = QSpinBox(self.react_group_5)
        self.reply_story_cry_from.setObjectName(u"reply_story_cry_from")
        self.reply_story_cry_from.setMinimumSize(QSize(100, 0))
        self.reply_story_cry_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_69.addWidget(self.reply_story_cry_from)

        self.to_35 = QLabel(self.react_group_5)
        self.to_35.setObjectName(u"to_35")
        self.to_35.setStyleSheet(u"")
        self.to_35.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_69.addWidget(self.to_35)

        self.reply_story_cry_to = QSpinBox(self.react_group_5)
        self.reply_story_cry_to.setObjectName(u"reply_story_cry_to")
        self.reply_story_cry_to.setMinimumSize(QSize(100, 0))
        self.reply_story_cry_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_69.addWidget(self.reply_story_cry_to)


        self.verticalLayout_21.addLayout(self.horizontalLayout_69)

        self.horizontalLayout_70 = QHBoxLayout()
        self.horizontalLayout_70.setObjectName(u"horizontalLayout_70")
        self.reply_story_angry = QCheckBox(self.react_group_5)
        self.reply_story_angry.setObjectName(u"reply_story_angry")
        self.reply_story_angry.setStyleSheet(u"")
        self.reply_story_angry.setIcon(icon14)
        self.reply_story_angry.setIconSize(QSize(30, 30))
        self.reply_story_angry.setChecked(False)

        self.horizontalLayout_70.addWidget(self.reply_story_angry)

        self.from_36 = QLabel(self.react_group_5)
        self.from_36.setObjectName(u"from_36")
        self.from_36.setStyleSheet(u"")

        self.horizontalLayout_70.addWidget(self.from_36)

        self.reply_story_angry_from = QSpinBox(self.react_group_5)
        self.reply_story_angry_from.setObjectName(u"reply_story_angry_from")
        self.reply_story_angry_from.setMinimumSize(QSize(100, 0))
        self.reply_story_angry_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_70.addWidget(self.reply_story_angry_from)

        self.to_36 = QLabel(self.react_group_5)
        self.to_36.setObjectName(u"to_36")
        self.to_36.setStyleSheet(u"")
        self.to_36.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_70.addWidget(self.to_36)

        self.reply_story_angry_to = QSpinBox(self.react_group_5)
        self.reply_story_angry_to.setObjectName(u"reply_story_angry_to")
        self.reply_story_angry_to.setMinimumSize(QSize(100, 0))
        self.reply_story_angry_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_70.addWidget(self.reply_story_angry_to)


        self.verticalLayout_21.addLayout(self.horizontalLayout_70)


        self.horizontalLayout_35.addWidget(self.react_group_5)

        self.tabWidget_3.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_27 = QVBoxLayout(self.tab_5)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(-1, -1, -1, 6)
        self.comments = QCheckBox(self.tab_5)
        self.comments.setObjectName(u"comments")

        self.gridLayout_9.addWidget(self.comments, 0, 1, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_13, 0, 3, 1, 1)

        self.chat = QCheckBox(self.tab_5)
        self.chat.setObjectName(u"chat")

        self.gridLayout_9.addWidget(self.chat, 0, 0, 1, 1)


        self.verticalLayout_27.addLayout(self.gridLayout_9)

        self.tabWidget = QTabWidget(self.tab_5)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.Comments = QWidget()
        self.Comments.setObjectName(u"Comments")
        self.horizontalLayout_15 = QHBoxLayout(self.Comments)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_54 = QHBoxLayout()
        self.horizontalLayout_54.setObjectName(u"horizontalLayout_54")
        self.frame_6 = QFrame(self.Comments)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame_6)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.horizontalLayout_55 = QHBoxLayout()
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.comments_by_text = QCheckBox(self.frame_6)
        self.comments_by_text.setObjectName(u"comments_by_text")
        self.comments_by_text.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.comments_by_text.setIconSize(QSize(30, 30))
        self.comments_by_text.setChecked(False)

        self.horizontalLayout_55.addWidget(self.comments_by_text)

        self.from_25 = QLabel(self.frame_6)
        self.from_25.setObjectName(u"from_25")
        self.from_25.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_55.addWidget(self.from_25)

        self.comments_by_text_from = QSpinBox(self.frame_6)
        self.comments_by_text_from.setObjectName(u"comments_by_text_from")
        self.comments_by_text_from.setMinimumSize(QSize(100, 0))
        self.comments_by_text_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_55.addWidget(self.comments_by_text_from)

        self.to_25 = QLabel(self.frame_6)
        self.to_25.setObjectName(u"to_25")
        self.to_25.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_25.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_55.addWidget(self.to_25)

        self.comments_by_text_to = QSpinBox(self.frame_6)
        self.comments_by_text_to.setObjectName(u"comments_by_text_to")
        self.comments_by_text_to.setMinimumSize(QSize(100, 0))
        self.comments_by_text_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_55.addWidget(self.comments_by_text_to)


        self.gridLayout_14.addLayout(self.horizontalLayout_55, 0, 0, 1, 1)

        self.comments_text = QPlainTextEdit(self.frame_6)
        self.comments_text.setObjectName(u"comments_text")
        self.comments_text.setFont(font2)
        self.comments_text.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout_14.addWidget(self.comments_text, 1, 0, 1, 1)


        self.horizontalLayout_54.addWidget(self.frame_6)

        self.frame_7 = QFrame(self.Comments)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.gridLayout_19 = QGridLayout(self.frame_7)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.horizontalLayout_56 = QHBoxLayout()
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.comments_sticker = QCheckBox(self.frame_7)
        self.comments_sticker.setObjectName(u"comments_sticker")
        self.comments_sticker.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.comments_sticker.setIconSize(QSize(30, 30))
        self.comments_sticker.setChecked(False)

        self.horizontalLayout_56.addWidget(self.comments_sticker)

        self.from_26 = QLabel(self.frame_7)
        self.from_26.setObjectName(u"from_26")
        self.from_26.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_56.addWidget(self.from_26)

        self.comments_sticker_from = QSpinBox(self.frame_7)
        self.comments_sticker_from.setObjectName(u"comments_sticker_from")
        self.comments_sticker_from.setMinimumSize(QSize(100, 0))
        self.comments_sticker_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_56.addWidget(self.comments_sticker_from)

        self.to_26 = QLabel(self.frame_7)
        self.to_26.setObjectName(u"to_26")
        self.to_26.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_26.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_56.addWidget(self.to_26)

        self.comments_sticker_to = QSpinBox(self.frame_7)
        self.comments_sticker_to.setObjectName(u"comments_sticker_to")
        self.comments_sticker_to.setMinimumSize(QSize(100, 0))
        self.comments_sticker_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_56.addWidget(self.comments_sticker_to)


        self.gridLayout_19.addLayout(self.horizontalLayout_56, 0, 0, 1, 1)

        self.plainTextEdit_4 = QPlainTextEdit(self.frame_7)
        self.plainTextEdit_4.setObjectName(u"plainTextEdit_4")
        self.plainTextEdit_4.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout_19.addWidget(self.plainTextEdit_4, 1, 0, 1, 1)


        self.horizontalLayout_54.addWidget(self.frame_7)


        self.horizontalLayout_15.addLayout(self.horizontalLayout_54)

        self.tabWidget.addTab(self.Comments, "")
        self.Chat = QWidget()
        self.Chat.setObjectName(u"Chat")
        self.horizontalLayout_65 = QHBoxLayout(self.Chat)
        self.horizontalLayout_65.setObjectName(u"horizontalLayout_65")
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.frame = QFrame(self.Chat)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.frame)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.horizontalLayout_44 = QHBoxLayout()
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.chat_by_text = QCheckBox(self.frame)
        self.chat_by_text.setObjectName(u"chat_by_text")
        self.chat_by_text.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.chat_by_text.setIconSize(QSize(30, 30))
        self.chat_by_text.setChecked(False)

        self.horizontalLayout_44.addWidget(self.chat_by_text)

        self.from_21 = QLabel(self.frame)
        self.from_21.setObjectName(u"from_21")
        self.from_21.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_44.addWidget(self.from_21)

        self.chat_by_text_from = QSpinBox(self.frame)
        self.chat_by_text_from.setObjectName(u"chat_by_text_from")
        self.chat_by_text_from.setMinimumSize(QSize(100, 0))
        self.chat_by_text_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_44.addWidget(self.chat_by_text_from)

        self.to_21 = QLabel(self.frame)
        self.to_21.setObjectName(u"to_21")
        self.to_21.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_21.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_44.addWidget(self.to_21)

        self.chat_by_text_to = QSpinBox(self.frame)
        self.chat_by_text_to.setObjectName(u"chat_by_text_to")
        self.chat_by_text_to.setMinimumSize(QSize(100, 0))
        self.chat_by_text_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_44.addWidget(self.chat_by_text_to)


        self.gridLayout_10.addLayout(self.horizontalLayout_44, 0, 0, 1, 1)

        self.chat_text = QPlainTextEdit(self.frame)
        self.chat_text.setObjectName(u"chat_text")
        self.chat_text.setFont(font2)
        self.chat_text.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout_10.addWidget(self.chat_text, 1, 0, 1, 1)


        self.horizontalLayout_18.addWidget(self.frame)

        self.frame_5 = QFrame(self.Chat)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_18 = QGridLayout(self.frame_5)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.plainTextEdit_2 = QPlainTextEdit(self.frame_5)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")
        self.plainTextEdit_2.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout_18.addWidget(self.plainTextEdit_2, 1, 0, 1, 1)

        self.horizontalLayout_45 = QHBoxLayout()
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.chat_sticker = QCheckBox(self.frame_5)
        self.chat_sticker.setObjectName(u"chat_sticker")
        self.chat_sticker.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.chat_sticker.setIconSize(QSize(30, 30))
        self.chat_sticker.setChecked(False)

        self.horizontalLayout_45.addWidget(self.chat_sticker)

        self.from_23 = QLabel(self.frame_5)
        self.from_23.setObjectName(u"from_23")
        self.from_23.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_45.addWidget(self.from_23)

        self.chat_sticker_from = QSpinBox(self.frame_5)
        self.chat_sticker_from.setObjectName(u"chat_sticker_from")
        self.chat_sticker_from.setMinimumSize(QSize(100, 0))
        self.chat_sticker_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_45.addWidget(self.chat_sticker_from)

        self.to_23 = QLabel(self.frame_5)
        self.to_23.setObjectName(u"to_23")
        self.to_23.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_23.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_45.addWidget(self.to_23)

        self.chat_sticker_to = QSpinBox(self.frame_5)
        self.chat_sticker_to.setObjectName(u"chat_sticker_to")
        self.chat_sticker_to.setMinimumSize(QSize(100, 0))
        self.chat_sticker_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_45.addWidget(self.chat_sticker_to)


        self.gridLayout_18.addLayout(self.horizontalLayout_45, 0, 0, 1, 1)


        self.horizontalLayout_18.addWidget(self.frame_5)


        self.horizontalLayout_65.addLayout(self.horizontalLayout_18)

        self.tabWidget.addTab(self.Chat, "")

        self.verticalLayout_27.addWidget(self.tabWidget)

        self.tabWidget_3.addTab(self.tab_5, "")

        self.gridLayout_23.addWidget(self.tabWidget_3, 0, 0, 1, 1)


        self.gridLayout_25.addWidget(self.Watch_GroupBox, 1, 0, 1, 1)

        self.GeneralAction_GroupBox = QFrame(self.groupBox)
        self.GeneralAction_GroupBox.setObjectName(u"GeneralAction_GroupBox")
        self.GeneralAction_GroupBox.setStyleSheet(u"")
        self.GeneralAction_GroupBox.setFrameShape(QFrame.StyledPanel)
        self.GeneralAction_GroupBox.setFrameShadow(QFrame.Raised)
        self.gridLayout_24 = QGridLayout(self.GeneralAction_GroupBox)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.general_option_group = QGroupBox(self.GeneralAction_GroupBox)
        self.general_option_group.setObjectName(u"general_option_group")
        self.general_option_group.setEnabled(True)
        self.general_option_group.setStyleSheet(u"")
        self.verticalLayout_8 = QVBoxLayout(self.general_option_group)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.get_account_info = QCheckBox(self.general_option_group)
        self.get_account_info.setObjectName(u"get_account_info")
        self.get_account_info.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.get_account_info.setIconSize(QSize(30, 30))
        self.get_account_info.setChecked(False)

        self.horizontalLayout_21.addWidget(self.get_account_info)

        self.scrape_group = QCheckBox(self.general_option_group)
        self.scrape_group.setObjectName(u"scrape_group")
        self.scrape_group.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_21.addWidget(self.scrape_group)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_14)


        self.verticalLayout_8.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.add_friends = QCheckBox(self.general_option_group)
        self.add_friends.setObjectName(u"add_friends")
        self.add_friends.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.add_friends.setIconSize(QSize(30, 30))
        self.add_friends.setChecked(False)

        self.horizontalLayout_26.addWidget(self.add_friends)

        self.from_13 = QLabel(self.general_option_group)
        self.from_13.setObjectName(u"from_13")
        self.from_13.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_26.addWidget(self.from_13)

        self.add_friends_from = QSpinBox(self.general_option_group)
        self.add_friends_from.setObjectName(u"add_friends_from")
        self.add_friends_from.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_26.addWidget(self.add_friends_from)

        self.to_13 = QLabel(self.general_option_group)
        self.to_13.setObjectName(u"to_13")
        self.to_13.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_13.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_26.addWidget(self.to_13)

        self.add_friends_to = QSpinBox(self.general_option_group)
        self.add_friends_to.setObjectName(u"add_friends_to")
        self.add_friends_to.setMinimumSize(QSize(100, 0))
        self.add_friends_to.setMinimum(1)

        self.horizontalLayout_26.addWidget(self.add_friends_to)

        self.horizontalLayout_26.setStretch(0, 1)

        self.horizontalLayout_25.addLayout(self.horizontalLayout_26)


        self.verticalLayout_8.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.confirm_friends = QCheckBox(self.general_option_group)
        self.confirm_friends.setObjectName(u"confirm_friends")
        self.confirm_friends.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.confirm_friends.setIconSize(QSize(30, 30))
        self.confirm_friends.setChecked(False)

        self.horizontalLayout_27.addWidget(self.confirm_friends)

        self.from_15 = QLabel(self.general_option_group)
        self.from_15.setObjectName(u"from_15")
        self.from_15.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_27.addWidget(self.from_15)

        self.confirm_friends_from = QSpinBox(self.general_option_group)
        self.confirm_friends_from.setObjectName(u"confirm_friends_from")
        self.confirm_friends_from.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_27.addWidget(self.confirm_friends_from)

        self.to_15 = QLabel(self.general_option_group)
        self.to_15.setObjectName(u"to_15")
        self.to_15.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_15.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_27.addWidget(self.to_15)

        self.confirm_friends_to = QSpinBox(self.general_option_group)
        self.confirm_friends_to.setObjectName(u"confirm_friends_to")
        self.confirm_friends_to.setMinimumSize(QSize(100, 0))
        self.confirm_friends_to.setMinimum(1)

        self.horizontalLayout_27.addWidget(self.confirm_friends_to)

        self.horizontalLayout_27.setStretch(0, 1)

        self.verticalLayout_8.addLayout(self.horizontalLayout_27)

        self.groupBox_3 = QGroupBox(self.general_option_group)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setStyleSheet(u"background-color: rgb(204, 211, 250);\n"
"background-color: rgb(213, 242, 250);")
        self.verticalLayout_17 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.check_notifycation = QCheckBox(self.groupBox_3)
        self.check_notifycation.setObjectName(u"check_notifycation")
        self.check_notifycation.setStyleSheet(u"")
        self.check_notifycation.setIconSize(QSize(30, 30))
        self.check_notifycation.setChecked(False)

        self.verticalLayout_17.addWidget(self.check_notifycation)

        self.click_join_group_in_notification = QCheckBox(self.groupBox_3)
        self.click_join_group_in_notification.setObjectName(u"click_join_group_in_notification")
        self.click_join_group_in_notification.setStyleSheet(u"")
        self.click_join_group_in_notification.setIconSize(QSize(30, 30))
        self.click_join_group_in_notification.setChecked(False)

        self.verticalLayout_17.addWidget(self.click_join_group_in_notification)

        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.total_click_notification = QCheckBox(self.groupBox_3)
        self.total_click_notification.setObjectName(u"total_click_notification")
        self.total_click_notification.setStyleSheet(u"")
        self.total_click_notification.setIconSize(QSize(30, 30))
        self.total_click_notification.setChecked(False)

        self.horizontalLayout_36.addWidget(self.total_click_notification)

        self.from_22 = QLabel(self.groupBox_3)
        self.from_22.setObjectName(u"from_22")
        self.from_22.setStyleSheet(u"")

        self.horizontalLayout_36.addWidget(self.from_22)

        self.total_click_notification_from = QSpinBox(self.groupBox_3)
        self.total_click_notification_from.setObjectName(u"total_click_notification_from")
        self.total_click_notification_from.setMinimumSize(QSize(100, 0))
        self.total_click_notification_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_36.addWidget(self.total_click_notification_from)

        self.to_22 = QLabel(self.groupBox_3)
        self.to_22.setObjectName(u"to_22")
        self.to_22.setStyleSheet(u"")
        self.to_22.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_36.addWidget(self.to_22)

        self.total_click_notification_to = QSpinBox(self.groupBox_3)
        self.total_click_notification_to.setObjectName(u"total_click_notification_to")
        self.total_click_notification_to.setMinimumSize(QSize(100, 0))
        self.total_click_notification_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.total_click_notification_to.setMinimum(1)

        self.horizontalLayout_36.addWidget(self.total_click_notification_to)

        self.horizontalLayout_36.setStretch(0, 1)

        self.verticalLayout_17.addLayout(self.horizontalLayout_36)


        self.verticalLayout_8.addWidget(self.groupBox_3)


        self.gridLayout_24.addWidget(self.general_option_group, 1, 1, 1, 1)

        self.react_group = QGroupBox(self.GeneralAction_GroupBox)
        self.react_group.setObjectName(u"react_group")
        self.react_group.setStyleSheet(u"")
        self.verticalLayout_7 = QVBoxLayout(self.react_group)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.like = QCheckBox(self.react_group)
        self.like.setObjectName(u"like")
        self.like.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.like.setIcon(icon10)
        self.like.setIconSize(QSize(30, 30))
        self.like.setChecked(False)

        self.horizontalLayout.addWidget(self.like)

        self.from_label = QLabel(self.react_group)
        self.from_label.setObjectName(u"from_label")
        self.from_label.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout.addWidget(self.from_label)

        self.like_from = QSpinBox(self.react_group)
        self.like_from.setObjectName(u"like_from")
        self.like_from.setMinimumSize(QSize(100, 0))
        self.like_from.setMinimum(0)
        self.like_from.setValue(0)

        self.horizontalLayout.addWidget(self.like_from)

        self.to_label = QLabel(self.react_group)
        self.to_label.setObjectName(u"to_label")
        self.to_label.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.to_label)

        self.like_to = QSpinBox(self.react_group)
        self.like_to.setObjectName(u"like_to")
        self.like_to.setMinimumSize(QSize(100, 0))
        self.like_to.setMinimum(1)

        self.horizontalLayout.addWidget(self.like_to)


        self.verticalLayout_7.addLayout(self.horizontalLayout)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.love = QCheckBox(self.react_group)
        self.love.setObjectName(u"love")
        self.love.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.love.setIcon(icon11)
        self.love.setIconSize(QSize(30, 30))
        self.love.setChecked(False)

        self.horizontalLayout_11.addWidget(self.love)

        self.from_2 = QLabel(self.react_group)
        self.from_2.setObjectName(u"from_2")
        self.from_2.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_11.addWidget(self.from_2)

        self.love_from = QSpinBox(self.react_group)
        self.love_from.setObjectName(u"love_from")
        self.love_from.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_11.addWidget(self.love_from)

        self.to_2 = QLabel(self.react_group)
        self.to_2.setObjectName(u"to_2")
        self.to_2.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.to_2)

        self.love_to = QSpinBox(self.react_group)
        self.love_to.setObjectName(u"love_to")
        self.love_to.setMinimumSize(QSize(100, 0))
        self.love_to.setMinimum(1)

        self.horizontalLayout_11.addWidget(self.love_to)


        self.verticalLayout_7.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.haha = QCheckBox(self.react_group)
        self.haha.setObjectName(u"haha")
        self.haha.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.haha.setIcon(icon12)
        self.haha.setIconSize(QSize(30, 30))
        self.haha.setChecked(False)

        self.horizontalLayout_13.addWidget(self.haha)

        self.from_3 = QLabel(self.react_group)
        self.from_3.setObjectName(u"from_3")
        self.from_3.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_13.addWidget(self.from_3)

        self.haha_from = QSpinBox(self.react_group)
        self.haha_from.setObjectName(u"haha_from")
        self.haha_from.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_13.addWidget(self.haha_from)

        self.to_3 = QLabel(self.react_group)
        self.to_3.setObjectName(u"to_3")
        self.to_3.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_13.addWidget(self.to_3)

        self.haha_to = QSpinBox(self.react_group)
        self.haha_to.setObjectName(u"haha_to")
        self.haha_to.setMinimumSize(QSize(100, 0))
        self.haha_to.setMinimum(1)

        self.horizontalLayout_13.addWidget(self.haha_to)


        self.verticalLayout_7.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.cry = QCheckBox(self.react_group)
        self.cry.setObjectName(u"cry")
        self.cry.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.cry.setIcon(icon13)
        self.cry.setIconSize(QSize(30, 30))
        self.cry.setChecked(False)

        self.horizontalLayout_16.addWidget(self.cry)

        self.from_6 = QLabel(self.react_group)
        self.from_6.setObjectName(u"from_6")
        self.from_6.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_16.addWidget(self.from_6)

        self.cry_from = QSpinBox(self.react_group)
        self.cry_from.setObjectName(u"cry_from")
        self.cry_from.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_16.addWidget(self.cry_from)

        self.to_6 = QLabel(self.react_group)
        self.to_6.setObjectName(u"to_6")
        self.to_6.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_16.addWidget(self.to_6)

        self.cry_to = QSpinBox(self.react_group)
        self.cry_to.setObjectName(u"cry_to")
        self.cry_to.setMinimumSize(QSize(100, 0))
        self.cry_to.setMinimum(1)

        self.horizontalLayout_16.addWidget(self.cry_to)


        self.verticalLayout_7.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.angry = QCheckBox(self.react_group)
        self.angry.setObjectName(u"angry")
        self.angry.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.angry.setIcon(icon14)
        self.angry.setIconSize(QSize(30, 30))
        self.angry.setChecked(False)

        self.horizontalLayout_17.addWidget(self.angry)

        self.from_7 = QLabel(self.react_group)
        self.from_7.setObjectName(u"from_7")
        self.from_7.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_17.addWidget(self.from_7)

        self.angry_from = QSpinBox(self.react_group)
        self.angry_from.setObjectName(u"angry_from")
        self.angry_from.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_17.addWidget(self.angry_from)

        self.to_7 = QLabel(self.react_group)
        self.to_7.setObjectName(u"to_7")
        self.to_7.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_17.addWidget(self.to_7)

        self.angry_to = QSpinBox(self.react_group)
        self.angry_to.setObjectName(u"angry_to")
        self.angry_to.setMinimumSize(QSize(100, 0))
        self.angry_to.setMinimum(1)

        self.horizontalLayout_17.addWidget(self.angry_to)


        self.verticalLayout_7.addLayout(self.horizontalLayout_17)


        self.gridLayout_24.addWidget(self.react_group, 1, 0, 1, 1)


        self.gridLayout_25.addWidget(self.GeneralAction_GroupBox, 0, 0, 1, 1)

        self.Connect_Community = QGroupBox(self.groupBox)
        self.Connect_Community.setObjectName(u"Connect_Community")
        self.Connect_Community.setStyleSheet(u"background-color: rgb(213, 242, 250);")
        self.gridLayout_12 = QGridLayout(self.Connect_Community)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setVerticalSpacing(0)
        self.full_verify_yandex_2 = QGroupBox(self.Connect_Community)
        self.full_verify_yandex_2.setObjectName(u"full_verify_yandex_2")
        self.full_verify_yandex_2.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.gridLayout_13 = QGridLayout(self.full_verify_yandex_2)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_83 = QGridLayout()
        self.gridLayout_83.setObjectName(u"gridLayout_83")
        self.add_email_yandex = QRadioButton(self.full_verify_yandex_2)
        self.add_email_yandex.setObjectName(u"add_email_yandex")
        self.add_email_yandex.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.add_email_yandex.setChecked(True)

        self.gridLayout_83.addWidget(self.add_email_yandex, 0, 0, 1, 1)

        self.horizontalSpacer_47 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_83.addItem(self.horizontalSpacer_47, 0, 3, 1, 1)

        self.add_mail_with_two_fa = QRadioButton(self.full_verify_yandex_2)
        self.add_mail_with_two_fa.setObjectName(u"add_mail_with_two_fa")
        self.add_mail_with_two_fa.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.gridLayout_83.addWidget(self.add_mail_with_two_fa, 0, 1, 1, 1)

        self.two_fa = QRadioButton(self.full_verify_yandex_2)
        self.two_fa.setObjectName(u"two_fa")
        self.two_fa.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.gridLayout_83.addWidget(self.two_fa, 0, 2, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_83, 0, 0, 1, 1)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_56 = QLabel(self.full_verify_yandex_2)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.horizontalLayout_14.addWidget(self.label_56)

        self.yandex_mail = QLineEdit(self.full_verify_yandex_2)
        self.yandex_mail.setObjectName(u"yandex_mail")
        self.yandex_mail.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_14.addWidget(self.yandex_mail)

        self.app_passss = QLabel(self.full_verify_yandex_2)
        self.app_passss.setObjectName(u"app_passss")
        self.app_passss.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.horizontalLayout_14.addWidget(self.app_passss)

        self.app_password_yandex = QLineEdit(self.full_verify_yandex_2)
        self.app_password_yandex.setObjectName(u"app_password_yandex")
        self.app_password_yandex.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_14.addWidget(self.app_password_yandex)


        self.gridLayout_13.addLayout(self.horizontalLayout_14, 1, 0, 1, 1)

        self.horizontalLayout_75 = QHBoxLayout()
        self.horizontalLayout_75.setObjectName(u"horizontalLayout_75")
        self.app_passss_2 = QLabel(self.full_verify_yandex_2)
        self.app_passss_2.setObjectName(u"app_passss_2")
        self.app_passss_2.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.horizontalLayout_75.addWidget(self.app_passss_2)

        self.yandex_start = QLineEdit(self.full_verify_yandex_2)
        self.yandex_start.setObjectName(u"yandex_start")
        self.yandex_start.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_75.addWidget(self.yandex_start)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_75.addItem(self.horizontalSpacer_10)


        self.gridLayout_13.addLayout(self.horizontalLayout_75, 2, 0, 1, 1)


        self.gridLayout_12.addWidget(self.full_verify_yandex_2, 1, 0, 1, 1)

        self.set_up_mail = QCheckBox(self.Connect_Community)
        self.set_up_mail.setObjectName(u"set_up_mail")

        self.gridLayout_12.addWidget(self.set_up_mail, 0, 0, 1, 1)


        self.gridLayout_25.addWidget(self.Connect_Community, 2, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox, 0, 0, 1, 1)

        self.stacked_main.addWidget(self.active_page)
        self.reg_page = QWidget()
        self.reg_page.setObjectName(u"reg_page")
        self.gridLayout_44 = QGridLayout(self.reg_page)
        self.gridLayout_44.setSpacing(0)
        self.gridLayout_44.setObjectName(u"gridLayout_44")
        self.gridLayout_44.setContentsMargins(0, 0, 0, 0)
        self.Accounts_widget_2 = QGroupBox(self.reg_page)
        self.Accounts_widget_2.setObjectName(u"Accounts_widget_2")
        self.Accounts_widget_2.setFont(font4)
        self.verticalLayout_9 = QVBoxLayout(self.Accounts_widget_2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.bg_options_2 = QWidget(self.Accounts_widget_2)
        self.bg_options_2.setObjectName(u"bg_options_2")
        self.bg_options_2.setStyleSheet(u"")
        self.gridLayout_11 = QGridLayout(self.bg_options_2)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setHorizontalSpacing(0)
        self.gridLayout_11.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setSpacing(12)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.category_reg_accounts = QComboBox(self.bg_options_2)
        self.category_reg_accounts.addItem("")
        self.category_reg_accounts.addItem("")
        self.category_reg_accounts.addItem("")
        self.category_reg_accounts.setObjectName(u"category_reg_accounts")
        self.category_reg_accounts.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.category_reg_accounts.setStyleSheet(u"background-color: rgb(125, 115, 127);")

        self.horizontalLayout_19.addWidget(self.category_reg_accounts)

        self.reload_reg_accounts = QPushButton(self.bg_options_2)
        self.reload_reg_accounts.setObjectName(u"reload_reg_accounts")
        self.reload_reg_accounts.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.reload_reg_accounts.setStyleSheet(u"background-color: rgb(85, 170, 0);")
        self.reload_reg_accounts.setIcon(icon7)
        self.reload_reg_accounts.setIconSize(QSize(20, 20))

        self.horizontalLayout_19.addWidget(self.reload_reg_accounts)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_7)

        self.horizontalLayout_42 = QHBoxLayout()
        self.horizontalLayout_42.setSpacing(4)
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.seleted_accounts_9 = QLabel(self.bg_options_2)
        self.seleted_accounts_9.setObjectName(u"seleted_accounts_9")
        self.seleted_accounts_9.setFont(font5)
        self.seleted_accounts_9.setStyleSheet(u"background-color: rgb(255, 188, 218);")

        self.horizontalLayout_42.addWidget(self.seleted_accounts_9)

        self.seleted_accounts_10 = QLabel(self.bg_options_2)
        self.seleted_accounts_10.setObjectName(u"seleted_accounts_10")
        font9 = QFont()
        font9.setPointSize(11)
        font9.setBold(True)
        self.seleted_accounts_10.setFont(font9)
        self.seleted_accounts_10.setStyleSheet(u"background-color: rgb(255, 188, 218);\n"
"color: rgb(0, 198, 0);")

        self.horizontalLayout_42.addWidget(self.seleted_accounts_10)


        self.horizontalLayout_19.addLayout(self.horizontalLayout_42)

        self.horizontalLayout_41 = QHBoxLayout()
        self.horizontalLayout_41.setSpacing(4)
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.seleted_accounts_7 = QLabel(self.bg_options_2)
        self.seleted_accounts_7.setObjectName(u"seleted_accounts_7")
        self.seleted_accounts_7.setFont(font5)
        self.seleted_accounts_7.setStyleSheet(u"background-color: rgb(255, 188, 218);")

        self.horizontalLayout_41.addWidget(self.seleted_accounts_7)

        self.seleted_accounts_8 = QLabel(self.bg_options_2)
        self.seleted_accounts_8.setObjectName(u"seleted_accounts_8")
        self.seleted_accounts_8.setFont(font9)
        self.seleted_accounts_8.setStyleSheet(u"background-color: rgb(255, 188, 218);\n"
"color: rgb(208, 0, 0);")

        self.horizontalLayout_41.addWidget(self.seleted_accounts_8)


        self.horizontalLayout_19.addLayout(self.horizontalLayout_41)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setSpacing(4)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.seleted_accounts_3 = QLabel(self.bg_options_2)
        self.seleted_accounts_3.setObjectName(u"seleted_accounts_3")
        self.seleted_accounts_3.setFont(font5)
        self.seleted_accounts_3.setStyleSheet(u"background-color: rgb(255, 188, 218);")

        self.horizontalLayout_20.addWidget(self.seleted_accounts_3)

        self.seleted_accounts_4 = QLabel(self.bg_options_2)
        self.seleted_accounts_4.setObjectName(u"seleted_accounts_4")
        self.seleted_accounts_4.setFont(font5)
        self.seleted_accounts_4.setStyleSheet(u"background-color: rgb(255, 188, 218);")

        self.horizontalLayout_20.addWidget(self.seleted_accounts_4)


        self.horizontalLayout_19.addLayout(self.horizontalLayout_20)


        self.gridLayout_11.addLayout(self.horizontalLayout_19, 0, 0, 1, 1)


        self.verticalLayout_9.addWidget(self.bg_options_2)

        self.stacked_accounts_2 = QStackedWidget(self.Accounts_widget_2)
        self.stacked_accounts_2.setObjectName(u"stacked_accounts_2")
        self.profile_details_table_widget_2 = QWidget()
        self.profile_details_table_widget_2.setObjectName(u"profile_details_table_widget_2")
        self.formLayout_5 = QFormLayout(self.profile_details_table_widget_2)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.formLayout_5.setHorizontalSpacing(0)
        self.formLayout_5.setVerticalSpacing(0)
        self.formLayout_5.setContentsMargins(0, 0, 0, 0)
        self.accounts_reg_table = QTableWidget(self.profile_details_table_widget_2)
        if (self.accounts_reg_table.columnCount() < 14):
            self.accounts_reg_table.setColumnCount(14)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(3, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(4, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(5, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(6, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(7, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(8, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(9, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(10, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(11, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(12, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.accounts_reg_table.setHorizontalHeaderItem(13, __qtablewidgetitem19)
        self.accounts_reg_table.setObjectName(u"accounts_reg_table")
        self.accounts_reg_table.setFont(font8)
        self.accounts_reg_table.setFocusPolicy(Qt.NoFocus)
        self.accounts_reg_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.accounts_reg_table.setLayoutDirection(Qt.LeftToRight)
        self.accounts_reg_table.setAutoFillBackground(False)
        self.accounts_reg_table.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.accounts_reg_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.accounts_reg_table.setDragDropOverwriteMode(False)
        self.accounts_reg_table.setAlternatingRowColors(True)
        self.accounts_reg_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.accounts_reg_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.accounts_reg_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.accounts_reg_table.setShowGrid(True)
        self.accounts_reg_table.setSortingEnabled(True)
        self.accounts_reg_table.horizontalHeader().setVisible(True)
        self.accounts_reg_table.horizontalHeader().setCascadingSectionResizes(True)
        self.accounts_reg_table.horizontalHeader().setStretchLastSection(True)
        self.accounts_reg_table.verticalHeader().setProperty(u"showSortIndicator", True)

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.accounts_reg_table)

        self.option_reg = QGroupBox(self.profile_details_table_widget_2)
        self.option_reg.setObjectName(u"option_reg")
        self.option_reg.setStyleSheet(u"")
        self.verticalLayout_10 = QVBoxLayout(self.option_reg)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.option1 = QGroupBox(self.option_reg)
        self.option1.setObjectName(u"option1")
        self.gridLayout_77 = QGridLayout(self.option1)
        self.gridLayout_77.setObjectName(u"gridLayout_77")
        self.gridLayout_77.setContentsMargins(0, 0, 0, 0)
        self.create_type_verify_or_no_verify = QFrame(self.option1)
        self.create_type_verify_or_no_verify.setObjectName(u"create_type_verify_or_no_verify")
        self.create_type_verify_or_no_verify.setFrameShape(QFrame.StyledPanel)
        self.create_type_verify_or_no_verify.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.create_type_verify_or_no_verify)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_39 = QHBoxLayout()
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.label_34 = QLabel(self.create_type_verify_or_no_verify)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.horizontalLayout_39.addWidget(self.label_34)

        self.no_verify_radio = QRadioButton(self.create_type_verify_or_no_verify)
        self.no_verify_radio.setObjectName(u"no_verify_radio")
        self.no_verify_radio.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.no_verify_radio.setChecked(True)

        self.horizontalLayout_39.addWidget(self.no_verify_radio)

        self.full_verify_radio = QRadioButton(self.create_type_verify_or_no_verify)
        self.full_verify_radio.setObjectName(u"full_verify_radio")
        self.full_verify_radio.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.horizontalLayout_39.addWidget(self.full_verify_radio)

        self.horizontalSpacer_26 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_39.addItem(self.horizontalSpacer_26)


        self.verticalLayout_11.addLayout(self.horizontalLayout_39)

        self.horizontalLayout_43 = QHBoxLayout()
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.label_35 = QLabel(self.create_type_verify_or_no_verify)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.horizontalLayout_43.addWidget(self.label_35)

        self.groupBox_2 = QGroupBox(self.create_type_verify_or_no_verify)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setStyleSheet(u"padding: 0;\n"
"margin: 0;\n"
"border: none;\n"
"background-color: rgb(204, 211, 250);")
        self.gridLayout_45 = QGridLayout(self.groupBox_2)
        self.gridLayout_45.setObjectName(u"gridLayout_45")
        self.gridLayout_45.setContentsMargins(0, 0, 0, 0)
        self.gender_male = QRadioButton(self.groupBox_2)
        self.gender_male.setObjectName(u"gender_male")
        self.gender_male.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.gender_male.setChecked(True)

        self.gridLayout_45.addWidget(self.gender_male, 0, 0, 1, 1)

        self.gender_female = QRadioButton(self.groupBox_2)
        self.gender_female.setObjectName(u"gender_female")
        self.gender_female.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.gridLayout_45.addWidget(self.gender_female, 0, 1, 1, 1)

        self.gender_random = QRadioButton(self.groupBox_2)
        self.gender_random.setObjectName(u"gender_random")
        self.gender_random.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.gridLayout_45.addWidget(self.gender_random, 0, 2, 1, 1)


        self.horizontalLayout_43.addWidget(self.groupBox_2)

        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_43.addItem(self.horizontalSpacer_27)


        self.verticalLayout_11.addLayout(self.horizontalLayout_43)

        self.ldplayer_path_line_edit_14 = QHBoxLayout()
        self.ldplayer_path_line_edit_14.setObjectName(u"ldplayer_path_line_edit_14")
        self.label_33 = QLabel(self.create_type_verify_or_no_verify)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.ldplayer_path_line_edit_14.addWidget(self.label_33)

        self.name_path_input = QLineEdit(self.create_type_verify_or_no_verify)
        self.name_path_input.setObjectName(u"name_path_input")

        self.ldplayer_path_line_edit_14.addWidget(self.name_path_input)

        self.name_path_btn = QPushButton(self.create_type_verify_or_no_verify)
        self.name_path_btn.setObjectName(u"name_path_btn")
        self.name_path_btn.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        self.name_path_btn.setIcon(icon5)
        self.name_path_btn.setIconSize(QSize(20, 24))

        self.ldplayer_path_line_edit_14.addWidget(self.name_path_btn)


        self.verticalLayout_11.addLayout(self.ldplayer_path_line_edit_14)


        self.gridLayout_77.addWidget(self.create_type_verify_or_no_verify, 0, 0, 1, 1)

        self.frame_2 = QFrame(self.option1)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_2)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.gridLayout_78 = QGridLayout()
        self.gridLayout_78.setObjectName(u"gridLayout_78")
        self.enable_vpn_checkbox = QCheckBox(self.frame_2)
        self.enable_vpn_checkbox.setObjectName(u"enable_vpn_checkbox")
        self.enable_vpn_checkbox.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.gridLayout_78.addWidget(self.enable_vpn_checkbox, 0, 0, 1, 1)

        self.enable_fake_location_checkbox = QCheckBox(self.frame_2)
        self.enable_fake_location_checkbox.setObjectName(u"enable_fake_location_checkbox")
        self.enable_fake_location_checkbox.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.gridLayout_78.addWidget(self.enable_fake_location_checkbox, 0, 1, 1, 1)


        self.verticalLayout_12.addLayout(self.gridLayout_78)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.label_50 = QLabel(self.frame_4)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.horizontalLayout_28.addWidget(self.label_50)

        self.vpn_combobox = QComboBox(self.frame_4)
        self.vpn_combobox.setObjectName(u"vpn_combobox")
        self.vpn_combobox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.vpn_combobox.setStyleSheet(u"")
        self.vpn_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_28.addWidget(self.vpn_combobox)

        self.label_54 = QLabel(self.frame_4)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.horizontalLayout_28.addWidget(self.label_54)

        self.vpn_city = QComboBox(self.frame_4)
        self.vpn_city.setObjectName(u"vpn_city")
        self.vpn_city.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.vpn_city.setStyleSheet(u"")
        self.vpn_city.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_28.addWidget(self.vpn_city)

        self.label_57 = QLabel(self.frame_4)
        self.label_57.setObjectName(u"label_57")
        self.label_57.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.horizontalLayout_28.addWidget(self.label_57)

        self.time_zone = QComboBox(self.frame_4)
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.time_zone.setObjectName(u"time_zone")
        self.time_zone.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.time_zone.setStyleSheet(u"")
        self.time_zone.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_28.addWidget(self.time_zone)


        self.verticalLayout_12.addWidget(self.frame_4)

        self.gridLayout_82 = QGridLayout()
        self.gridLayout_82.setObjectName(u"gridLayout_82")
        self.label_52 = QLabel(self.frame_2)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.gridLayout_82.addWidget(self.label_52, 0, 0, 1, 1)

        self.fake_location_input = QPlainTextEdit(self.frame_2)
        self.fake_location_input.setObjectName(u"fake_location_input")
        self.fake_location_input.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_82.addWidget(self.fake_location_input, 0, 1, 1, 1)


        self.verticalLayout_12.addLayout(self.gridLayout_82)


        self.gridLayout_77.addWidget(self.frame_2, 0, 1, 1, 1)


        self.verticalLayout_10.addWidget(self.option1)

        self.tabWidget_2 = QTabWidget(self.option_reg)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setStyleSheet(u"")
        self.no_verify_tab = QWidget()
        self.no_verify_tab.setObjectName(u"no_verify_tab")
        self.gridLayout_60 = QGridLayout(self.no_verify_tab)
        self.gridLayout_60.setObjectName(u"gridLayout_60")
        self.no_veriry_group = QGroupBox(self.no_verify_tab)
        self.no_veriry_group.setObjectName(u"no_veriry_group")
        self.gridLayout_61 = QGridLayout(self.no_veriry_group)
        self.gridLayout_61.setObjectName(u"gridLayout_61")
        self.gridLayout_79 = QGridLayout()
        self.gridLayout_79.setObjectName(u"gridLayout_79")
        self.fake_phone_input2 = QLineEdit(self.no_veriry_group)
        self.fake_phone_input2.setObjectName(u"fake_phone_input2")

        self.gridLayout_79.addWidget(self.fake_phone_input2, 0, 2, 1, 1)

        self.horizontalSpacer_46 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_79.addItem(self.horizontalSpacer_46, 0, 4, 1, 1)

        self.fake_phone_input3 = QLineEdit(self.no_veriry_group)
        self.fake_phone_input3.setObjectName(u"fake_phone_input3")

        self.gridLayout_79.addWidget(self.fake_phone_input3, 0, 3, 1, 1)

        self.label_51 = QLabel(self.no_veriry_group)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.gridLayout_79.addWidget(self.label_51, 0, 0, 1, 1)

        self.fake_phone_input1 = QLineEdit(self.no_veriry_group)
        self.fake_phone_input1.setObjectName(u"fake_phone_input1")

        self.gridLayout_79.addWidget(self.fake_phone_input1, 0, 1, 1, 1)


        self.gridLayout_61.addLayout(self.gridLayout_79, 1, 0, 1, 1)

        self.gridLayout_63 = QGridLayout()
        self.gridLayout_63.setObjectName(u"gridLayout_63")
        self.fake_email = QLineEdit(self.no_veriry_group)
        self.fake_email.setObjectName(u"fake_email")

        self.gridLayout_63.addWidget(self.fake_email, 0, 1, 1, 1)

        self.horizontalSpacer_37 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_63.addItem(self.horizontalSpacer_37, 0, 2, 1, 1)

        self.label_44 = QLabel(self.no_veriry_group)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.gridLayout_63.addWidget(self.label_44, 0, 0, 1, 1)


        self.gridLayout_61.addLayout(self.gridLayout_63, 0, 0, 1, 1)


        self.gridLayout_60.addWidget(self.no_veriry_group, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.no_verify_tab, "")
        self.full_verify_tab = QWidget()
        self.full_verify_tab.setObjectName(u"full_verify_tab")
        self.gridLayout_33 = QGridLayout(self.full_verify_tab)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.gridLayout_33.setHorizontalSpacing(6)
        self.gridLayout_33.setVerticalSpacing(0)
        self.gridLayout_33.setContentsMargins(9, 0, 9, 9)
        self.full_verify_yandex = QGroupBox(self.full_verify_tab)
        self.full_verify_yandex.setObjectName(u"full_verify_yandex")
        self.gridLayout_76 = QGridLayout(self.full_verify_yandex)
        self.gridLayout_76.setObjectName(u"gridLayout_76")
        self.gridLayout_73 = QGridLayout()
        self.gridLayout_73.setObjectName(u"gridLayout_73")
        self.five_sim = QRadioButton(self.full_verify_yandex)
        self.buttonGroup_3 = QButtonGroup(MainWindow)
        self.buttonGroup_3.setObjectName(u"buttonGroup_3")
        self.buttonGroup_3.addButton(self.five_sim)
        self.five_sim.setObjectName(u"five_sim")
        self.five_sim.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.gridLayout_73.addWidget(self.five_sim, 0, 1, 1, 1)

        self.horizontalSpacer_43 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_73.addItem(self.horizontalSpacer_43, 0, 2, 1, 1)

        self.yandex = QRadioButton(self.full_verify_yandex)
        self.buttonGroup_3.addButton(self.yandex)
        self.yandex.setObjectName(u"yandex")
        self.yandex.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.yandex.setChecked(True)

        self.gridLayout_73.addWidget(self.yandex, 0, 0, 1, 1)


        self.gridLayout_76.addLayout(self.gridLayout_73, 0, 0, 1, 1)

        self.ldplayer_path_line_edit_19 = QHBoxLayout()
        self.ldplayer_path_line_edit_19.setObjectName(u"ldplayer_path_line_edit_19")
        self.label_49 = QLabel(self.full_verify_yandex)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.ldplayer_path_line_edit_19.addWidget(self.label_49)

        self.phone_input1 = QLineEdit(self.full_verify_yandex)
        self.phone_input1.setObjectName(u"phone_input1")

        self.ldplayer_path_line_edit_19.addWidget(self.phone_input1)

        self.phone_input2 = QLineEdit(self.full_verify_yandex)
        self.phone_input2.setObjectName(u"phone_input2")

        self.ldplayer_path_line_edit_19.addWidget(self.phone_input2)

        self.phone_input3 = QLineEdit(self.full_verify_yandex)
        self.phone_input3.setObjectName(u"phone_input3")

        self.ldplayer_path_line_edit_19.addWidget(self.phone_input3)


        self.gridLayout_76.addLayout(self.ldplayer_path_line_edit_19, 1, 0, 1, 1)

        self.ldplayer_path_line_edit_20 = QHBoxLayout()
        self.ldplayer_path_line_edit_20.setObjectName(u"ldplayer_path_line_edit_20")
        self.label_53 = QLabel(self.full_verify_yandex)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.ldplayer_path_line_edit_20.addWidget(self.label_53)

        self.password_input1_reg = QLineEdit(self.full_verify_yandex)
        self.password_input1_reg.setObjectName(u"password_input1_reg")

        self.ldplayer_path_line_edit_20.addWidget(self.password_input1_reg)

        self.password_input2_reg = QLineEdit(self.full_verify_yandex)
        self.password_input2_reg.setObjectName(u"password_input2_reg")

        self.ldplayer_path_line_edit_20.addWidget(self.password_input2_reg)


        self.gridLayout_76.addLayout(self.ldplayer_path_line_edit_20, 3, 0, 1, 1)

        self.gridLayout_80 = QGridLayout()
        self.gridLayout_80.setObjectName(u"gridLayout_80")
        self.random_password = QRadioButton(self.full_verify_yandex)
        self.buttonGroup_2 = QButtonGroup(MainWindow)
        self.buttonGroup_2.setObjectName(u"buttonGroup_2")
        self.buttonGroup_2.addButton(self.random_password)
        self.random_password.setObjectName(u"random_password")
        self.random_password.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.gridLayout_80.addWidget(self.random_password, 0, 1, 1, 1)

        self.horizontalSpacer_45 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_80.addItem(self.horizontalSpacer_45, 0, 2, 1, 1)

        self.fixed_password = QRadioButton(self.full_verify_yandex)
        self.buttonGroup_2.addButton(self.fixed_password)
        self.fixed_password.setObjectName(u"fixed_password")
        self.fixed_password.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.fixed_password.setChecked(True)

        self.gridLayout_80.addWidget(self.fixed_password, 0, 0, 1, 1)


        self.gridLayout_76.addLayout(self.gridLayout_80, 2, 0, 1, 1)


        self.gridLayout_33.addWidget(self.full_verify_yandex, 0, 0, 1, 1)

        self.full_verify_upload = QGroupBox(self.full_verify_tab)
        self.full_verify_upload.setObjectName(u"full_verify_upload")
        self.gridLayout_74 = QGridLayout(self.full_verify_upload)
        self.gridLayout_74.setObjectName(u"gridLayout_74")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_74.addItem(self.verticalSpacer_3, 2, 0, 1, 1)

        self.ldplayer_path_line_edit_15 = QHBoxLayout()
        self.ldplayer_path_line_edit_15.setObjectName(u"ldplayer_path_line_edit_15")
        self.label_36 = QLabel(self.full_verify_upload)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.ldplayer_path_line_edit_15.addWidget(self.label_36)

        self.profile_img_input = QLineEdit(self.full_verify_upload)
        self.profile_img_input.setObjectName(u"profile_img_input")

        self.ldplayer_path_line_edit_15.addWidget(self.profile_img_input)

        self.profile_img_btn = QPushButton(self.full_verify_upload)
        self.profile_img_btn.setObjectName(u"profile_img_btn")
        self.profile_img_btn.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        self.profile_img_btn.setIcon(icon5)
        self.profile_img_btn.setIconSize(QSize(20, 24))

        self.ldplayer_path_line_edit_15.addWidget(self.profile_img_btn)


        self.gridLayout_74.addLayout(self.ldplayer_path_line_edit_15, 1, 0, 1, 1)

        self.gridLayout_75 = QGridLayout()
        self.gridLayout_75.setObjectName(u"gridLayout_75")
        self.horizontalSpacer_44 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_75.addItem(self.horizontalSpacer_44, 0, 1, 1, 1)

        self.upload_profile_checkbox = QCheckBox(self.full_verify_upload)
        self.upload_profile_checkbox.setObjectName(u"upload_profile_checkbox")
        self.upload_profile_checkbox.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.gridLayout_75.addWidget(self.upload_profile_checkbox, 0, 0, 1, 1)


        self.gridLayout_74.addLayout(self.gridLayout_75, 0, 0, 1, 1)


        self.gridLayout_33.addWidget(self.full_verify_upload, 0, 1, 1, 1)

        self.tabWidget_2.addTab(self.full_verify_tab, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_5 = QGridLayout(self.tab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.groupBox_5sim_key = QGroupBox(self.tab)
        self.groupBox_5sim_key.setObjectName(u"groupBox_5sim_key")
        self.groupBox_5sim_key.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.verticalLayout_18 = QVBoxLayout(self.groupBox_5sim_key)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.horizontalLayout_58 = QHBoxLayout()
        self.horizontalLayout_58.setObjectName(u"horizontalLayout_58")
        self.label_55 = QLabel(self.groupBox_5sim_key)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.horizontalLayout_58.addWidget(self.label_55)

        self.five_sim_api = QLineEdit(self.groupBox_5sim_key)
        self.five_sim_api.setObjectName(u"five_sim_api")
        self.five_sim_api.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_58.addWidget(self.five_sim_api)

        self.refresh_five_sim_btn = QPushButton(self.groupBox_5sim_key)
        self.refresh_five_sim_btn.setObjectName(u"refresh_five_sim_btn")
        self.refresh_five_sim_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.refresh_five_sim_btn.setStyleSheet(u"background-color: rgb(74, 81, 127);")
        icon15 = QIcon()
        icon15.addFile(u":/icons/images/reload.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.refresh_five_sim_btn.setIcon(icon15)
        self.refresh_five_sim_btn.setIconSize(QSize(20, 20))

        self.horizontalLayout_58.addWidget(self.refresh_five_sim_btn)


        self.verticalLayout_18.addLayout(self.horizontalLayout_58)

        self.frame_8 = QFrame(self.groupBox_5sim_key)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_37 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.label_7 = QLabel(self.frame_8)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_37.addWidget(self.label_7)

        self.five_sim_country = QComboBox(self.frame_8)
        self.five_sim_country.setObjectName(u"five_sim_country")
        self.five_sim_country.setStyleSheet(u"background-color: rgb(85, 170, 255);")
        self.five_sim_country.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_37.addWidget(self.five_sim_country)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_37.addItem(self.horizontalSpacer_5)


        self.verticalLayout_18.addWidget(self.frame_8)


        self.gridLayout_5.addWidget(self.groupBox_5sim_key, 0, 0, 1, 1)

        self.groupBox5simusername = QGroupBox(self.tab)
        self.groupBox5simusername.setObjectName(u"groupBox5simusername")
        self.groupBox5simusername.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.verticalLayout_19 = QVBoxLayout(self.groupBox5simusername)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.frame_10 = QFrame(self.groupBox5simusername)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_10)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.five_sim_username = QLabel(self.frame_10)
        self.five_sim_username.setObjectName(u"five_sim_username")
        self.five_sim_username.setMinimumSize(QSize(150, 0))
        self.five_sim_username.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.five_sim_username.setMargin(5)

        self.gridLayout_7.addWidget(self.five_sim_username, 0, 1, 1, 1)

        self.label_9 = QLabel(self.frame_10)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_7.addWidget(self.label_9, 0, 0, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_8, 0, 2, 1, 1)


        self.verticalLayout_19.addWidget(self.frame_10)

        self.frame_11 = QFrame(self.groupBox5simusername)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_40 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.label_11 = QLabel(self.frame_11)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_40.addWidget(self.label_11)

        self.five_sim_balance = QLabel(self.frame_11)
        self.five_sim_balance.setObjectName(u"five_sim_balance")
        self.five_sim_balance.setMinimumSize(QSize(150, 0))
        self.five_sim_balance.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.five_sim_balance.setMargin(5)

        self.horizontalLayout_40.addWidget(self.five_sim_balance)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_40.addItem(self.horizontalSpacer_9)


        self.verticalLayout_19.addWidget(self.frame_11)


        self.gridLayout_5.addWidget(self.groupBox5simusername, 0, 1, 1, 1)

        self.gridLayout_5.setColumnStretch(0, 1)
        self.gridLayout_5.setColumnStretch(1, 1)
        self.gridLayout_5.setColumnMinimumWidth(1, 1)
        self.tabWidget_2.addTab(self.tab, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_15 = QGridLayout(self.tab_6)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.groupBox_4 = QGroupBox(self.tab_6)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.verticalLayout_24 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.horizontalLayout_61 = QHBoxLayout()
        self.horizontalLayout_61.setObjectName(u"horizontalLayout_61")
        self.label_58 = QLabel(self.groupBox_4)
        self.label_58.setObjectName(u"label_58")
        self.label_58.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.horizontalLayout_61.addWidget(self.label_58)

        self.yandex_mail_reg = QLineEdit(self.groupBox_4)
        self.yandex_mail_reg.setObjectName(u"yandex_mail_reg")
        self.yandex_mail_reg.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_61.addWidget(self.yandex_mail_reg)

        self.app_passss_4 = QLabel(self.groupBox_4)
        self.app_passss_4.setObjectName(u"app_passss_4")
        self.app_passss_4.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.horizontalLayout_61.addWidget(self.app_passss_4)

        self.app_password_yandex_reg = QLineEdit(self.groupBox_4)
        self.app_password_yandex_reg.setObjectName(u"app_password_yandex_reg")
        self.app_password_yandex_reg.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_61.addWidget(self.app_password_yandex_reg)


        self.verticalLayout_24.addLayout(self.horizontalLayout_61)

        self.horizontalLayout_76 = QHBoxLayout()
        self.horizontalLayout_76.setObjectName(u"horizontalLayout_76")
        self.app_passss_3 = QLabel(self.groupBox_4)
        self.app_passss_3.setObjectName(u"app_passss_3")
        self.app_passss_3.setStyleSheet(u"background-color: rgb(194, 202, 250);")

        self.horizontalLayout_76.addWidget(self.app_passss_3)

        self.yandex_start_reg = QLineEdit(self.groupBox_4)
        self.yandex_start_reg.setObjectName(u"yandex_start_reg")
        self.yandex_start_reg.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_76.addWidget(self.yandex_start_reg)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_76.addItem(self.horizontalSpacer_11)


        self.verticalLayout_24.addLayout(self.horizontalLayout_76)


        self.gridLayout_15.addWidget(self.groupBox_4, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_6, "")

        self.verticalLayout_10.addWidget(self.tabWidget_2)

        self.verticalSpacer_4 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_4)


        self.formLayout_5.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.option_reg)

        self.stacked_accounts_2.addWidget(self.profile_details_table_widget_2)

        self.verticalLayout_9.addWidget(self.stacked_accounts_2)


        self.gridLayout_44.addWidget(self.Accounts_widget_2, 0, 0, 1, 1)

        self.gridLayout_44.setRowStretch(0, 5000)
        self.stacked_main.addWidget(self.reg_page)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.label_8 = QLabel(self.page_4)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(70, 200, 291, 141))
        font10 = QFont()
        font10.setPointSize(20)
        font10.setBold(True)
        self.label_8.setFont(font10)
        self.stacked_main.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.label_5 = QLabel(self.page_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(150, 170, 291, 141))
        self.label_5.setFont(font10)
        self.stacked_main.addWidget(self.page_5)

        self.verticalLayout_5.addWidget(self.stacked_main)


        self.gridLayout_32.addWidget(self.name_menu, 0, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.menu.toggled.connect(self.icon_only_widget.setVisible)
        self.menu.toggled.connect(self.icon_name_widget.setHidden)
        self.page5_1.toggled.connect(self.page5_2.setChecked)
        self.page4_1.toggled.connect(self.page4_2.setChecked)
        self.reg_1.toggled.connect(self.reg_2.setChecked)
        self.active_menu_1.toggled.connect(self.active_menu_2.setChecked)
        self.dashboard_1.toggled.connect(self.dashboard_2.setChecked)
        self.dashboard_2.toggled.connect(self.dashboard_1.setChecked)
        self.active_menu_2.toggled.connect(self.active_menu_1.setChecked)
        self.reg_2.toggled.connect(self.reg_1.setChecked)
        self.page4_2.toggled.connect(self.page4_1.setChecked)
        self.page5_2.toggled.connect(self.page5_1.setChecked)
        self.pushButton_6.toggled.connect(MainWindow.close)
        self.pushButton_16.toggled.connect(MainWindow.close)

        self.stacked_main.setCurrentIndex(0)
        self.stacked_accounts.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(3)
        self.tabWidget.setCurrentIndex(1)
        self.stacked_accounts_2.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionjlj.setText(QCoreApplication.translate("MainWindow", u"jlj", None))
        self.actionsfdsf.setText(QCoreApplication.translate("MainWindow", u"sfdsf", None))
        self.label.setText("")
        self.dashboard_1.setText("")
        self.active_menu_1.setText("")
        self.reg_1.setText("")
        self.page4_1.setText("")
        self.page5_1.setText("")
        self.pushButton_6.setText("")
        self.label_4.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"SP-Farm", None))
        self.dashboard_2.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.active_menu_2.setText(QCoreApplication.translate("MainWindow", u"Active", None))
        self.reg_2.setText(QCoreApplication.translate("MainWindow", u"Reg", None))
        self.page4_2.setText(QCoreApplication.translate("MainWindow", u"Page4", None))
        self.page5_2.setText(QCoreApplication.translate("MainWindow", u"Page5", None))
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.menu.setText("")
        self.start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.time.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.stop.setText(QCoreApplication.translate("MainWindow", u"Stop All", None))
        self.gif_label.setText("")
        self.ldplayer_list_widget.setTitle(QCoreApplication.translate("MainWindow", u"LDPlayer", None))
        ___qtablewidgetitem = self.ldplayer_list.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"ID", None));
        ___qtablewidgetitem1 = self.ldplayer_list.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"LDPlayer Name", None));
        ___qtablewidgetitem2 = self.ldplayer_list.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Status", None));

        __sortingEnabled = self.ldplayer_list.isSortingEnabled()
        self.ldplayer_list.setSortingEnabled(False)
        ___qtablewidgetitem3 = self.ldplayer_list.item(0, 1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"SP1", None));
        ___qtablewidgetitem4 = self.ldplayer_list.item(0, 2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Click add", None));
        self.ldplayer_list.setSortingEnabled(__sortingEnabled)

        self.ldplayer_controller_widget.setTitle(QCoreApplication.translate("MainWindow", u"LDPlayer Controller", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"LD Per Rows", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"LD Per Rows", None))
        self.active_accounts.setText(QCoreApplication.translate("MainWindow", u"Active Accounts", None))
        self.reg_accounts.setText(QCoreApplication.translate("MainWindow", u"Reg Accounts", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Delay Per LD", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"LD Per Column", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"LD Sleep        ", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Loop", None))
        self.auto_expand_fit_active.setText(QCoreApplication.translate("MainWindow", u"Auto Run Until All Accounts", None))
        self.backup_data_fb_ld.setText(QCoreApplication.translate("MainWindow", u"Backup Data FB/LD", None))
        self.auto_arrange_ldplayer.setText(QCoreApplication.translate("MainWindow", u"Auto Arrage LDPlayer", None))
        self.run_schedule_checkbox.setText(QCoreApplication.translate("MainWindow", u"Run Schedulce", None))
        self.shop_tool_if_no_internet.setText(QCoreApplication.translate("MainWindow", u"Stop Tool if No Internet", None))
        self.runing_ld_counter.setText(QCoreApplication.translate("MainWindow", u"running: 0/0", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"LDPlayer Path", None))
        self.browse_ld_path_btn.setText(QCoreApplication.translate("MainWindow", u"Folder", None))
        self.refresh_ld.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.Accounts_widget.setTitle(QCoreApplication.translate("MainWindow", u"Accounts", None))
        self.switch_profile_page_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"Profile", None))
        self.switch_profile_page_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"Page", None))

        self.refresh_table_accounts_dashboard.setText(QCoreApplication.translate("MainWindow", u"Reload", None))
        self.seleted_accounts_2.setText(QCoreApplication.translate("MainWindow", u"Seleted: ", None))
        self.seleted_accounts.setText(QCoreApplication.translate("MainWindow", u"0/0", None))
        self.show_details.setText(QCoreApplication.translate("MainWindow", u"Show Details", None))
        self.category_filter_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"All", None))
        self.category_filter_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"Check Point", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Search:    ", None))
        self.search_accs.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search...", None))
        self.enter_category_line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter Category Name", None))
        self.add_new_category_btn.setText(QCoreApplication.translate("MainWindow", u"Add New Category", None))
        self.delete_category_btn.setText(QCoreApplication.translate("MainWindow", u"Delete Category", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Active Functions", None))
        self.reels_group.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.watch_feeds.setText(QCoreApplication.translate("MainWindow", u"Watch Reels", None))
        self.from_12.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_12.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Delay Per Scroll Reels", None))
        self.from_14.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_14.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.feeds_no_emoji.setText(QCoreApplication.translate("MainWindow", u"No use Emoji", None))
        self.feeds_alway_emoji.setText(QCoreApplication.translate("MainWindow", u"Alway Use Emoji", None))
        self.feeds_random_emoji.setText(QCoreApplication.translate("MainWindow", u"Random Use Or None", None))
        self.react_group_2.setTitle(QCoreApplication.translate("MainWindow", u"Emoji", None))
        self.feeds_like.setText("")
        self.from_label_2.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_label_2.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.feeds_love.setText("")
        self.from_4.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_4.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.feeds_haha.setText("")
        self.from_5.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_5.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.feeds_cry.setText("")
        self.from_8.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_8.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.feeds_angry.setText("")
        self.from_9.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_9.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Watch Reels", None))
        self.vidos_group.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.watch_videos.setText(QCoreApplication.translate("MainWindow", u"Watch Videos", None))
        self.from_16.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_16.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Delay Per Scroll Videos", None))
        self.from_17.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_17.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.videos_no_emoji.setText(QCoreApplication.translate("MainWindow", u"No Emoji", None))
        self.videos_alway_emoji.setText(QCoreApplication.translate("MainWindow", u"Alway Emoji", None))
        self.videos_random_emoji.setText(QCoreApplication.translate("MainWindow", u"Random Emoji Or None", None))
        self.react_group_3.setTitle(QCoreApplication.translate("MainWindow", u"Emoji", None))
        self.videos_like.setText("")
        self.from_label_3.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_label_3.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.videos_love.setText("")
        self.from_10.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_10.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.videos_haha.setText("")
        self.from_11.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_11.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.videos_cry.setText("")
        self.from_18.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_18.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.videos_angry.setText("")
        self.from_24.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_24.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Watch Videos", None))
        self.reels_group_2.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.story.setText(QCoreApplication.translate("MainWindow", u"Watch Story", None))
        self.from_31.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_31.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.reply_story.setText(QCoreApplication.translate("MainWindow", u"Reply Story :", None))
        self.from_32.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_32.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.reply_story_text.setPlainText("")
        self.reply_story_no_emoji.setText(QCoreApplication.translate("MainWindow", u"No use Emoji", None))
        self.reply_story_alway_emoji.setText(QCoreApplication.translate("MainWindow", u"Alway Use Emoji", None))
        self.reply_story_ramdom_emoji.setText(QCoreApplication.translate("MainWindow", u"Random Use Or None", None))
        self.react_group_5.setTitle(QCoreApplication.translate("MainWindow", u"Emoji", None))
        self.reply_story_like.setText("")
        self.from_label_5.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_label_5.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.reply_story_love.setText("")
        self.from_33.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_33.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.reply_story_haha.setText("")
        self.from_34.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_34.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.reply_story_cry.setText("")
        self.from_35.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_35.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.reply_story_angry.setText("")
        self.from_36.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_36.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Watch Story", None))
        self.comments.setText(QCoreApplication.translate("MainWindow", u"Comments", None))
        self.chat.setText(QCoreApplication.translate("MainWindow", u"Chat", None))
        self.comments_by_text.setText(QCoreApplication.translate("MainWindow", u"Comments By Text", None))
        self.from_25.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_25.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.comments_sticker.setText(QCoreApplication.translate("MainWindow", u"Comments Sticker", None))
        self.from_26.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_26.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Comments), QCoreApplication.translate("MainWindow", u"Comments", None))
        self.chat_by_text.setText(QCoreApplication.translate("MainWindow", u"Chat By Text", None))
        self.from_21.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_21.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.chat_text.setPlainText("")
        self.chat_sticker.setText(QCoreApplication.translate("MainWindow", u"Chat Sticker", None))
        self.from_23.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_23.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Chat), QCoreApplication.translate("MainWindow", u"Chat", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Community", None))
        self.general_option_group.setTitle(QCoreApplication.translate("MainWindow", u"General Action", None))
        self.get_account_info.setText(QCoreApplication.translate("MainWindow", u"Get Account Info Name", None))
        self.scrape_group.setText(QCoreApplication.translate("MainWindow", u"Scrape Groups", None))
        self.add_friends.setText(QCoreApplication.translate("MainWindow", u"Add Friends", None))
        self.from_13.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_13.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.confirm_friends.setText(QCoreApplication.translate("MainWindow", u"Confirm Friends", None))
        self.from_15.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_15.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Check Notification", None))
        self.check_notifycation.setText(QCoreApplication.translate("MainWindow", u"Check Notification", None))
        self.click_join_group_in_notification.setText(QCoreApplication.translate("MainWindow", u"If See Invite Join Group Click Join", None))
        self.total_click_notification.setText(QCoreApplication.translate("MainWindow", u"Total Click to Notification", None))
        self.from_22.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_22.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.react_group.setTitle(QCoreApplication.translate("MainWindow", u"Auto Scroll With Emoji", None))
        self.like.setText("")
        self.from_label.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_label.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.love.setText("")
        self.from_2.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_2.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.haha.setText("")
        self.from_3.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_3.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.cry.setText("")
        self.from_6.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_6.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.angry.setText("")
        self.from_7.setText(QCoreApplication.translate("MainWindow", u"From :", None))
        self.to_7.setText(QCoreApplication.translate("MainWindow", u"To :", None))
        self.Connect_Community.setTitle(QCoreApplication.translate("MainWindow", u"Mail", None))
        self.full_verify_yandex_2.setTitle("")
        self.add_email_yandex.setText(QCoreApplication.translate("MainWindow", u"Add Yandex Mail", None))
        self.add_mail_with_two_fa.setText(QCoreApplication.translate("MainWindow", u"Add Mail With Setup 2FA", None))
        self.two_fa.setText(QCoreApplication.translate("MainWindow", u"Setup 2FA", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"Yandex Mail:", None))
        self.yandex_mail.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Spfarm123@yandex.com", None))
        self.app_passss.setText(QCoreApplication.translate("MainWindow", u"App Password : ", None))
        self.app_password_yandex.setPlaceholderText(QCoreApplication.translate("MainWindow", u"bxnpshzhiwvgfggk", None))
        self.app_passss_2.setText(QCoreApplication.translate("MainWindow", u"Yanex Mail Start :", None))
        self.yandex_start.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Spfarm123+10@yandex.com", None))
        self.set_up_mail.setText(QCoreApplication.translate("MainWindow", u"Setup Mail", None))
        self.Accounts_widget_2.setTitle(QCoreApplication.translate("MainWindow", u"Create Accounts", None))
        self.category_reg_accounts.setItemText(0, QCoreApplication.translate("MainWindow", u"All", None))
        self.category_reg_accounts.setItemText(1, QCoreApplication.translate("MainWindow", u"Live", None))
        self.category_reg_accounts.setItemText(2, QCoreApplication.translate("MainWindow", u"Die", None))

        self.reload_reg_accounts.setText(QCoreApplication.translate("MainWindow", u"Reload", None))
        self.seleted_accounts_9.setText(QCoreApplication.translate("MainWindow", u"Total Live :", None))
        self.seleted_accounts_10.setText(QCoreApplication.translate("MainWindow", u"0/0", None))
        self.seleted_accounts_7.setText(QCoreApplication.translate("MainWindow", u"Total Die :", None))
        self.seleted_accounts_8.setText(QCoreApplication.translate("MainWindow", u"0/0", None))
        self.seleted_accounts_3.setText(QCoreApplication.translate("MainWindow", u"Seleted: ", None))
        self.seleted_accounts_4.setText(QCoreApplication.translate("MainWindow", u"0/0", None))
        ___qtablewidgetitem5 = self.accounts_reg_table.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"ID", None));
        ___qtablewidgetitem6 = self.accounts_reg_table.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem7 = self.accounts_reg_table.horizontalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"UID", None));
        ___qtablewidgetitem8 = self.accounts_reg_table.horizontalHeaderItem(3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Email", None));
        ___qtablewidgetitem9 = self.accounts_reg_table.horizontalHeaderItem(4)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Phone Number", None));
        ___qtablewidgetitem10 = self.accounts_reg_table.horizontalHeaderItem(5)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Password", None));
        ___qtablewidgetitem11 = self.accounts_reg_table.horizontalHeaderItem(6)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Fake GPS", None));
        ___qtablewidgetitem12 = self.accounts_reg_table.horizontalHeaderItem(7)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Set Fake GPS", None));
        ___qtablewidgetitem13 = self.accounts_reg_table.horizontalHeaderItem(8)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"VPN", None));
        ___qtablewidgetitem14 = self.accounts_reg_table.horizontalHeaderItem(9)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Set VPN", None));
        ___qtablewidgetitem15 = self.accounts_reg_table.horizontalHeaderItem(10)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem16 = self.accounts_reg_table.horizontalHeaderItem(11)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Model Name", None));
        ___qtablewidgetitem17 = self.accounts_reg_table.horizontalHeaderItem(12)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Cookies", None));
        ___qtablewidgetitem18 = self.accounts_reg_table.horizontalHeaderItem(13)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Date", None));
        self.option_reg.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.option1.setTitle("")
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Create Type   ", None))
        self.no_verify_radio.setText(QCoreApplication.translate("MainWindow", u"No Verify", None))
        self.full_verify_radio.setText(QCoreApplication.translate("MainWindow", u"Full Verify", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Gender           ", None))
        self.groupBox_2.setTitle("")
        self.gender_male.setText(QCoreApplication.translate("MainWindow", u"Male", None))
        self.gender_female.setText(QCoreApplication.translate("MainWindow", u"Female", None))
        self.gender_random.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Name Path    ", None))
        self.name_path_btn.setText(QCoreApplication.translate("MainWindow", u"Folder", None))
        self.enable_vpn_checkbox.setText(QCoreApplication.translate("MainWindow", u"Enable VPN", None))
        self.enable_fake_location_checkbox.setText(QCoreApplication.translate("MainWindow", u"Enable Fake Location", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"VPN :", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"City : ", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"Time Zone : ", None))
        self.time_zone.setItemText(0, QCoreApplication.translate("MainWindow", u"America/New_York", None))
        self.time_zone.setItemText(1, QCoreApplication.translate("MainWindow", u"America/Chicago", None))
        self.time_zone.setItemText(2, QCoreApplication.translate("MainWindow", u"America/Los_Angeles", None))
        self.time_zone.setItemText(3, QCoreApplication.translate("MainWindow", u"America/Toronto", None))
        self.time_zone.setItemText(4, QCoreApplication.translate("MainWindow", u"America/Vancouver", None))
        self.time_zone.setItemText(5, QCoreApplication.translate("MainWindow", u"America/Mexico_City", None))
        self.time_zone.setItemText(6, QCoreApplication.translate("MainWindow", u"Europe/London", None))
        self.time_zone.setItemText(7, QCoreApplication.translate("MainWindow", u"Europe/Belfast", None))
        self.time_zone.setItemText(8, QCoreApplication.translate("MainWindow", u"Europe/Berlin", None))
        self.time_zone.setItemText(9, QCoreApplication.translate("MainWindow", u"Europe/Paris", None))
        self.time_zone.setItemText(10, QCoreApplication.translate("MainWindow", u"Europe/Madrid", None))
        self.time_zone.setItemText(11, QCoreApplication.translate("MainWindow", u"Europe/Rome", None))
        self.time_zone.setItemText(12, QCoreApplication.translate("MainWindow", u"Europe/Amsterdam", None))
        self.time_zone.setItemText(13, QCoreApplication.translate("MainWindow", u"Asia/Bangkok", None))
        self.time_zone.setItemText(14, QCoreApplication.translate("MainWindow", u"Asia/Phnom_Penh", None))
        self.time_zone.setItemText(15, QCoreApplication.translate("MainWindow", u"Asia/Ho_Chi_Minh", None))
        self.time_zone.setItemText(16, QCoreApplication.translate("MainWindow", u"Asia/Manila", None))
        self.time_zone.setItemText(17, QCoreApplication.translate("MainWindow", u"Asia/Jakarta", None))
        self.time_zone.setItemText(18, QCoreApplication.translate("MainWindow", u"Asia/Kuala_Lumpur", None))
        self.time_zone.setItemText(19, QCoreApplication.translate("MainWindow", u"Asia/Singapore", None))
        self.time_zone.setItemText(20, QCoreApplication.translate("MainWindow", u"Asia/Tokyo", None))
        self.time_zone.setItemText(21, QCoreApplication.translate("MainWindow", u"Asia/Seoul", None))
        self.time_zone.setItemText(22, QCoreApplication.translate("MainWindow", u"Asia/Kolkata", None))
        self.time_zone.setItemText(23, QCoreApplication.translate("MainWindow", u"Australia/Sydney", None))
        self.time_zone.setItemText(24, QCoreApplication.translate("MainWindow", u"Australia/Melbourne", None))
        self.time_zone.setItemText(25, QCoreApplication.translate("MainWindow", u"America/Sao_Paulo", None))
        self.time_zone.setItemText(26, QCoreApplication.translate("MainWindow", u"America/Argentina/Buenos_Aires", None))
        self.time_zone.setItemText(27, QCoreApplication.translate("MainWindow", u"Africa/Johannesburg", None))

        self.label_52.setText(QCoreApplication.translate("MainWindow", u"Fake Location :", None))
        self.no_veriry_group.setTitle("")
        self.fake_phone_input2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"96", None))
        self.fake_phone_input3.setPlaceholderText(QCoreApplication.translate("MainWindow", u"9845456", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Fake Phone Number :   ", None))
        self.fake_phone_input1.setPlaceholderText(QCoreApplication.translate("MainWindow", u"+855", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Fake Email :                    ", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.no_verify_tab), QCoreApplication.translate("MainWindow", u"No Verify", None))
        self.full_verify_yandex.setTitle("")
        self.five_sim.setText(QCoreApplication.translate("MainWindow", u"5sim", None))
        self.yandex.setText(QCoreApplication.translate("MainWindow", u"Yandex", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Phone Number :", None))
        self.phone_input1.setPlaceholderText(QCoreApplication.translate("MainWindow", u"+855", None))
        self.phone_input2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"96", None))
        self.phone_input3.setPlaceholderText(QCoreApplication.translate("MainWindow", u"123456", None))
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"Password : ", None))
        self.password_input1_reg.setPlaceholderText(QCoreApplication.translate("MainWindow", u"96", None))
        self.password_input2_reg.setPlaceholderText(QCoreApplication.translate("MainWindow", u"123456", None))
        self.random_password.setText(QCoreApplication.translate("MainWindow", u"Random Password", None))
        self.fixed_password.setText(QCoreApplication.translate("MainWindow", u"Fixed Password", None))
        self.full_verify_upload.setTitle("")
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Profile Image :", None))
        self.profile_img_btn.setText(QCoreApplication.translate("MainWindow", u"Folder", None))
        self.upload_profile_checkbox.setText(QCoreApplication.translate("MainWindow", u"Upload Profile Image", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.full_verify_tab), QCoreApplication.translate("MainWindow", u"Full Verify", None))
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"5Sim Key", None))
        self.refresh_five_sim_btn.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Country : ", None))
        self.five_sim_username.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"User Name: ", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Balance :      ", None))
        self.five_sim_balance.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"5 Sim", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.label_58.setText(QCoreApplication.translate("MainWindow", u"Yandex Mail:", None))
        self.yandex_mail_reg.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Spfarm123@yandex.com", None))
        self.app_passss_4.setText(QCoreApplication.translate("MainWindow", u"App Password : ", None))
        self.app_password_yandex_reg.setPlaceholderText(QCoreApplication.translate("MainWindow", u"bxnpshzhiwvgfggk", None))
        self.app_passss_3.setText(QCoreApplication.translate("MainWindow", u"Yanex Mail Start :", None))
        self.yandex_start_reg.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Spfarm123+10@yandex.com", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"Yandex", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Page4", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Page5", None))
    # retranslateUi

