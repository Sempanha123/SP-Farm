# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_vpn_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)
from . import resources_rc

class Ui_SetVPN(object):
    def setupUi(self, SetVPN):
        if not SetVPN.objectName():
            SetVPN.setObjectName(u"SetVPN")
        SetVPN.resize(298, 172)
        icon = QIcon()
        icon.addFile(u":/icons/images/vpn_loaction.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        SetVPN.setWindowIcon(icon)
        SetVPN.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(226, 241, 255);\n"
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
"    background-color: #FBD8E4;  /* faded "
                        "pink for disabled state */\n"
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
"	image: url(:/icons/images/down-arrow.png);\n"
"    width: 16px;\n"
"    height: 1"
                        "6px;\n"
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
" * ----------------------------------"
                        "----------------------------------------- */\n"
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
"	background-color: rgb(162, 206, 234);\n"
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
"/* Each individual section/column in the header */\n"
"QHeaderView::section {\n"
"	ba"
                        "ckground-color: rgb(213, 242, 250);\n"
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
"QScrollBar::handle:vertical {\n"
"    backgro"
                        "und: #4C566A; /* Handle color */\n"
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
" * QSpinBox -- Professional Dark Theme Style"
                        "\n"
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
"/* Style for when hovering over the button"
                        "s */\n"
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
"/* Style for the checkable box itself */\n"
"QCheckBox::indicator "
                        "{\n"
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
"/* -------------------------------------------------------"
                        "--------------------\n"
" * QMenu -- Style for multi-level context menus\n"
" * --------------------------------------------------------------------------- */\n"
"\n"
"QMenu {\n"
"    background-color: #3B4252; /* Dark grey background */\n"
"    color: #ECEFF4; /* Light text */\n"
"    border: 1px solid #4C566A;\n"
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
"    image: url(:/icon"
                        "s/images/right-arrow-48.png); /* You need a right-arrow icon */\n"
"    width: 16px;\n"
"    height: 16px;\n"
"padding-right: 10px;\n"
"}\n"
"\n"
"#bg_options, #show_details{\n"
"	background-color: rgb(255, 188, 218);\n"
"}\n"
"#ldplayer_controller_widget{\n"
"	background-color: rgb(204, 211, 250);\n"
"}\n"
"#thread_option, #ld_sleep, #option_checkbox, #option_checkbox_2, #run_schedule_checkbox, #shop_tool_if_no_internet, #auto_shutdown, #auto_arrage_ld, #backup_data_fb, #label_9{\n"
"	background-color: rgb(204, 211, 250);\n"
"}\n"
"#save{\n"
"	\n"
"	background-color: rgb(85, 170, 0);\n"
"}\n"
"#cancel{\n"
"	background-color: rgb(255, 93, 158);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.gridLayout = QGridLayout(SetVPN)
        self.gridLayout.setObjectName(u"gridLayout")
        self.enable = QCheckBox(SetVPN)
        self.enable.setObjectName(u"enable")

        self.gridLayout.addWidget(self.enable, 0, 0, 1, 1)

        self.frame_3 = QFrame(SetVPN)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.save = QPushButton(self.frame_3)
        self.save.setObjectName(u"save")
        self.save.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.save.setIcon(icon1)
        self.save.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.save)

        self.cancel = QPushButton(self.frame_3)
        self.cancel.setObjectName(u"cancel")
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cancel.setIcon(icon2)
        self.cancel.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.cancel)


        self.gridLayout.addWidget(self.frame_3, 4, 0, 1, 1)

        self.frame = QFrame(SetVPN)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.vpn_comboBox = QComboBox(self.frame)
        self.vpn_comboBox.addItem("")
        self.vpn_comboBox.addItem("")
        self.vpn_comboBox.setObjectName(u"vpn_comboBox")

        self.gridLayout_2.addWidget(self.vpn_comboBox, 0, 1, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 3)

        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.frame_2 = QFrame(SetVPN)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)

        self.city_comboBox = QComboBox(self.frame_2)
        self.city_comboBox.addItem("")
        self.city_comboBox.addItem("")
        self.city_comboBox.setObjectName(u"city_comboBox")

        self.gridLayout_3.addWidget(self.city_comboBox, 0, 1, 1, 1)

        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 3)

        self.gridLayout.addWidget(self.frame_2, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.retranslateUi(SetVPN)

        QMetaObject.connectSlotsByName(SetVPN)
    # setupUi

    def retranslateUi(self, SetVPN):
        SetVPN.setWindowTitle(QCoreApplication.translate("SetVPN", u"Set VPN", None))
        self.enable.setText(QCoreApplication.translate("SetVPN", u"Enable", None))
        self.save.setText(QCoreApplication.translate("SetVPN", u"Save", None))
        self.cancel.setText(QCoreApplication.translate("SetVPN", u"Cancel", None))
        self.vpn_comboBox.setItemText(0, QCoreApplication.translate("SetVPN", u"Express VPN", None))
        self.vpn_comboBox.setItemText(1, QCoreApplication.translate("SetVPN", u"surfshark", None))

        self.label.setText(QCoreApplication.translate("SetVPN", u"VPN", None))
        self.label_2.setText(QCoreApplication.translate("SetVPN", u"City", None))
        self.city_comboBox.setItemText(0, QCoreApplication.translate("SetVPN", u"New York", None))
        self.city_comboBox.setItemText(1, QCoreApplication.translate("SetVPN", u"Califonia", None))

    # retranslateUi

