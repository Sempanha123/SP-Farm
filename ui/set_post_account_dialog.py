# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_post_account_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QButtonGroup, QCheckBox,
    QDialog, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPlainTextEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
from . import resources_rc

class Ui_Post(object):
    def setupUi(self, Post):
        if not Post.objectName():
            Post.setObjectName(u"Post")
        Post.resize(1222, 974)
        Post.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setFamilies([u"Noto Sans Khmer"])
        Post.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icons/images/vpn_loaction.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Post.setWindowIcon(icon)
        Post.setStyleSheet(u"QWidget, #post_group {\n"
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
"/* Style for the checkbox indicator inside the table */\n"
"QTableWidget::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    background-color: white;\n"
"    border: 2px solid rgb(136, 199, 247);\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"/* Style for when the mouse is hovering over the indicator */\n"
"QTableWidget::indicator:hover {\n"
"    border: 2px solid rgb(42, 126, 0); \n"
"}\n"
"\n"
"/* Style for when the checkbox is checked */\n"
"QTableWidget::indicator:checked {\n"
"    image: url(:/icons/images/checkmark.png);\n"
"    background-color: white; /* Keeps background white when checked */\n"
"    border: 2px solid rgb(136, 199, 247);\n"
"}\n"
"\n"
"/* Style for when a checked checkbox is hovered */\n"
"QTableWidget::indicator:checked:hover {\n"
"    border: 2px solid rgb(42, 126, 0);\n"
"}\n"
"\n"
"/* Style for when the checkbox is disabled */\n"
"QTableWidget::indicator:disabled {\n"
"    background-"
                        "color: #3B4252;\n"
"    border: 1px solid #434C5E;\n"
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
"	background-color: rgb(213, 242, 250);\n"
"    border: none;\n"
"    text-align: center; /* Ensure text is aligned left */\n"
"padding: 1px;\n"
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
"/*"
                        " ---------------------------------------------------------------------------\n"
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
"QScrollBar::handle:hor"
                        "izontal {\n"
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
" * QSpinBox -- Professional Dark Theme Style\n"
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
""
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
"/* Style for when hovering over the buttons */\n"
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
"/* -------"
                        "--------------------------------------------------------------------\n"
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
"    /* This displays a checkmark icon from your resources"
                        " */\n"
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
"\n"
"\n"
"/* ---------------------------------------------------------------------------\n"
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
"    border: 2"
                        "px solid rgb(136, 199, 247);   /* Same blue tone as QCheckBox */\n"
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
"    background-color: qradialgradient(\n"
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
"    border: 2px solid rgb(157"
                        ", 178, 255);\n"
"}\n"
"\n"
"\n"
"/* ---------------------------------------------------------------------------\n"
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
""
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
"    border: 2px solid  rgb(157, 178, 255);        /* Light mint border */\n"
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
"     "
                        "   stop: 0 #e8f5e9,\n"
"        stop: 1 #c8e6c9\n"
"    );\n"
"    border: 1px solid  rgb(157, 178, 255);\n"
"    border-bottom: none;               /* So selected tab merges with pane */\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 100px;\n"
"    padding: 4px 7px;\n"
"    color: #2e7d32;                    /* Dark green text */\n"
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
"    "
                        "border-color: #66bb6a;\n"
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
"}")
        self.gridLayout = QGridLayout(Post)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(Post)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame = QFrame(self.groupBox)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
        font1 = QFont()
        font1.setBold(False)
        self.tabWidget.setFont(font1)
        self.tabWidget.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.tabWidget.setStyleSheet(u"")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setElideMode(Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setMovable(True)
        self.PostReel = QWidget()
        self.PostReel.setObjectName(u"PostReel")
        self.gridLayout_2 = QGridLayout(self.PostReel)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox_7 = QGroupBox(self.PostReel)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.gridLayout_9 = QGridLayout(self.groupBox_7)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.post = QCheckBox(self.groupBox_7)
        self.post.setObjectName(u"post")
        self.post.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_22.addWidget(self.post)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_2)

        self.label_6 = QLabel(self.groupBox_7)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_22.addWidget(self.label_6)

        self.total_posts = QSpinBox(self.groupBox_7)
        self.total_posts.setObjectName(u"total_posts")
        self.total_posts.setMinimumSize(QSize(100, 0))
        self.total_posts.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.total_posts.setMinimum(1)

        self.horizontalLayout_22.addWidget(self.total_posts)

        self.label_5 = QLabel(self.groupBox_7)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_22.addWidget(self.label_5)


        self.gridLayout_9.addLayout(self.horizontalLayout_22, 0, 0, 1, 1)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.tag = QCheckBox(self.groupBox_7)
        self.tag.setObjectName(u"tag")
        self.tag.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_24.addWidget(self.tag)

        self.from_14 = QLabel(self.groupBox_7)
        self.from_14.setObjectName(u"from_14")
        self.from_14.setLayoutDirection(Qt.LeftToRight)
        self.from_14.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_24.addWidget(self.from_14)

        self.tag_from = QSpinBox(self.groupBox_7)
        self.tag_from.setObjectName(u"tag_from")
        self.tag_from.setMinimumSize(QSize(100, 0))
        self.tag_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_24.addWidget(self.tag_from)

        self.to_14 = QLabel(self.groupBox_7)
        self.to_14.setObjectName(u"to_14")
        self.to_14.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_14.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_24.addWidget(self.to_14)

        self.tag_to = QSpinBox(self.groupBox_7)
        self.tag_to.setObjectName(u"tag_to")
        self.tag_to.setMinimumSize(QSize(100, 0))
        self.tag_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.tag_to.setMinimum(1)

        self.horizontalLayout_24.addWidget(self.tag_to)

        self.horizontalLayout_24.setStretch(0, 11)
        self.horizontalLayout_24.setStretch(1, 1)

        self.gridLayout_9.addLayout(self.horizontalLayout_24, 1, 0, 1, 1)

        self.ai_label_reels = QCheckBox(self.groupBox_7)
        self.ai_label_reels.setObjectName(u"ai_label_reels")

        self.gridLayout_9.addWidget(self.ai_label_reels, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_7, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.PostReel)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setStyleSheet(u"background-color: rgb(194, 202, 250);\n"
"background-color: rgb(204, 211, 250);")
        self.gridLayout_3 = QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.share_to_group = QCheckBox(self.groupBox_3)
        self.share_to_group.setObjectName(u"share_to_group")
        self.share_to_group.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_23.addWidget(self.share_to_group)

        self.from_13 = QLabel(self.groupBox_3)
        self.from_13.setObjectName(u"from_13")
        self.from_13.setLayoutDirection(Qt.LeftToRight)
        self.from_13.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_23.addWidget(self.from_13)

        self.share_to_group_from = QSpinBox(self.groupBox_3)
        self.share_to_group_from.setObjectName(u"share_to_group_from")
        self.share_to_group_from.setMinimumSize(QSize(100, 0))
        self.share_to_group_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_23.addWidget(self.share_to_group_from)

        self.to_13 = QLabel(self.groupBox_3)
        self.to_13.setObjectName(u"to_13")
        self.to_13.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_13.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_23.addWidget(self.to_13)

        self.share_to_group_to = QSpinBox(self.groupBox_3)
        self.share_to_group_to.setObjectName(u"share_to_group_to")
        self.share_to_group_to.setMinimumSize(QSize(100, 0))
        self.share_to_group_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.share_to_group_to.setMinimum(1)

        self.horizontalLayout_23.addWidget(self.share_to_group_to)

        self.horizontalLayout_23.setStretch(0, 11)
        self.horizontalLayout_23.setStretch(1, 1)

        self.gridLayout_3.addLayout(self.horizontalLayout_23, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.groupBox_3)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.share_to_group_use_by_suggest = QRadioButton(self.frame_3)
        self.buttonGroup_2 = QButtonGroup(Post)
        self.buttonGroup_2.setObjectName(u"buttonGroup_2")
        self.buttonGroup_2.addButton(self.share_to_group_use_by_suggest)
        self.share_to_group_use_by_suggest.setObjectName(u"share_to_group_use_by_suggest")

        self.horizontalLayout_8.addWidget(self.share_to_group_use_by_suggest)

        self.share_to_group_use_by_seleted = QRadioButton(self.frame_3)
        self.buttonGroup_2.addButton(self.share_to_group_use_by_seleted)
        self.share_to_group_use_by_seleted.setObjectName(u"share_to_group_use_by_seleted")

        self.horizontalLayout_8.addWidget(self.share_to_group_use_by_seleted)


        self.gridLayout_3.addWidget(self.frame_3, 1, 0, 1, 1)

        self.share_to_group_word = QPlainTextEdit(self.groupBox_3)
        self.share_to_group_word.setObjectName(u"share_to_group_word")
        self.share_to_group_word.setFont(font)
        self.share_to_group_word.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout_3.addWidget(self.share_to_group_word, 3, 0, 1, 1)

        self.frame_9 = QFrame(self.groupBox_3)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.share_to_group_tittle = QCheckBox(self.frame_9)
        self.share_to_group_tittle.setObjectName(u"share_to_group_tittle")

        self.horizontalLayout_18.addWidget(self.share_to_group_tittle)

        self.widget_9 = QWidget(self.frame_9)
        self.widget_9.setObjectName(u"widget_9")
        self.horizontalLayout_19 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.use_fixed_share_group_tittle = QRadioButton(self.widget_9)
        self.use_fixed_share_group_tittle.setObjectName(u"use_fixed_share_group_tittle")
        self.use_fixed_share_group_tittle.setChecked(True)

        self.horizontalLayout_19.addWidget(self.use_fixed_share_group_tittle)

        self.use_random_share_group_tittle = QRadioButton(self.widget_9)
        self.use_random_share_group_tittle.setObjectName(u"use_random_share_group_tittle")

        self.horizontalLayout_19.addWidget(self.use_random_share_group_tittle)


        self.horizontalLayout_18.addWidget(self.widget_9)


        self.gridLayout_3.addWidget(self.frame_9, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_3, 0, 1, 2, 1)

        self.groupBox_8 = QGroupBox(self.PostReel)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.gridLayout_5 = QGridLayout(self.groupBox_8)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.post_reels_group = QTableWidget(self.groupBox_8)
        if (self.post_reels_group.columnCount() < 2):
            self.post_reels_group.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.post_reels_group.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.post_reels_group.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.post_reels_group.rowCount() < 1):
            self.post_reels_group.setRowCount(1)
        font2 = QFont()
        font2.setPointSize(10)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font2);
        self.post_reels_group.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.post_reels_group.setItem(0, 0, __qtablewidgetitem3)
        self.post_reels_group.setObjectName(u"post_reels_group")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.post_reels_group.sizePolicy().hasHeightForWidth())
        self.post_reels_group.setSizePolicy(sizePolicy)
        self.post_reels_group.setMinimumSize(QSize(0, 0))
        font3 = QFont()
        font3.setFamilies([u"Noto Sans Khmer"])
        font3.setPointSize(10)
        self.post_reels_group.setFont(font3)
        self.post_reels_group.setFocusPolicy(Qt.NoFocus)
        self.post_reels_group.setAutoFillBackground(True)
        self.post_reels_group.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.post_reels_group.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.post_reels_group.setDragDropOverwriteMode(False)
        self.post_reels_group.setSelectionMode(QAbstractItemView.NoSelection)
        self.post_reels_group.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.post_reels_group.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.post_reels_group.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.post_reels_group.setShowGrid(False)
        self.post_reels_group.setGridStyle(Qt.NoPen)
        self.post_reels_group.setSortingEnabled(True)
        self.post_reels_group.setCornerButtonEnabled(True)
        self.post_reels_group.setColumnCount(2)
        self.post_reels_group.horizontalHeader().setStretchLastSection(True)
        self.post_reels_group.verticalHeader().setProperty(u"showSortIndicator", True)
        self.post_reels_group.verticalHeader().setStretchLastSection(False)

        self.gridLayout_5.addWidget(self.post_reels_group, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_8, 0, 2, 5, 1)

        self.groupBox_5 = QGroupBox(self.PostReel)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget = QWidget(self.groupBox_5)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.use_tittle_from_videos = QRadioButton(self.widget)
        self.buttonGroup_3 = QButtonGroup(Post)
        self.buttonGroup_3.setObjectName(u"buttonGroup_3")
        self.buttonGroup_3.addButton(self.use_tittle_from_videos)
        self.use_tittle_from_videos.setObjectName(u"use_tittle_from_videos")
        self.use_tittle_from_videos.setChecked(True)

        self.horizontalLayout.addWidget(self.use_tittle_from_videos)

        self.use_fixed_tittle = QRadioButton(self.widget)
        self.buttonGroup_3.addButton(self.use_fixed_tittle)
        self.use_fixed_tittle.setObjectName(u"use_fixed_tittle")

        self.horizontalLayout.addWidget(self.use_fixed_tittle)


        self.verticalLayout_4.addWidget(self.widget)

        self.tittle_text = QPlainTextEdit(self.groupBox_5)
        self.tittle_text.setObjectName(u"tittle_text")
        self.tittle_text.setFont(font)
        self.tittle_text.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_4.addWidget(self.tittle_text)


        self.gridLayout_2.addWidget(self.groupBox_5, 1, 0, 2, 1)

        self.groupBox_9 = QGroupBox(self.PostReel)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_4 = QFrame(self.groupBox_9)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.comments = QCheckBox(self.frame_4)
        self.comments.setObjectName(u"comments")

        self.horizontalLayout_9.addWidget(self.comments)

        self.widget_6 = QWidget(self.frame_4)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.comments_use_fixed = QRadioButton(self.widget_6)
        self.comments_use_fixed.setObjectName(u"comments_use_fixed")
        self.comments_use_fixed.setChecked(True)

        self.horizontalLayout_10.addWidget(self.comments_use_fixed)

        self.comments_use_random = QRadioButton(self.widget_6)
        self.comments_use_random.setObjectName(u"comments_use_random")

        self.horizontalLayout_10.addWidget(self.comments_use_random)


        self.horizontalLayout_9.addWidget(self.widget_6)


        self.verticalLayout_6.addWidget(self.frame_4)

        self.comments_text = QPlainTextEdit(self.groupBox_9)
        self.comments_text.setObjectName(u"comments_text")
        self.comments_text.setFont(font)
        self.comments_text.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_6.addWidget(self.comments_text)


        self.gridLayout_2.addWidget(self.groupBox_9, 2, 1, 2, 1)

        self.groupBox_4 = QGroupBox(self.PostReel)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_2 = QFrame(self.groupBox_4)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.hastag = QCheckBox(self.frame_2)
        self.hastag.setObjectName(u"hastag")

        self.horizontalLayout_7.addWidget(self.hastag)

        self.widget_5 = QWidget(self.frame_2)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.use_fixed_hastag = QRadioButton(self.widget_5)
        self.buttonGroup_4 = QButtonGroup(Post)
        self.buttonGroup_4.setObjectName(u"buttonGroup_4")
        self.buttonGroup_4.addButton(self.use_fixed_hastag)
        self.use_fixed_hastag.setObjectName(u"use_fixed_hastag")
        self.use_fixed_hastag.setChecked(True)

        self.horizontalLayout_6.addWidget(self.use_fixed_hastag)

        self.use_random_hastag = QRadioButton(self.widget_5)
        self.buttonGroup_4.addButton(self.use_random_hastag)
        self.use_random_hastag.setObjectName(u"use_random_hastag")

        self.horizontalLayout_6.addWidget(self.use_random_hastag)


        self.horizontalLayout_7.addWidget(self.widget_5)


        self.verticalLayout_3.addWidget(self.frame_2)

        self.post_reels_hastag = QPlainTextEdit(self.groupBox_4)
        self.post_reels_hastag.setObjectName(u"post_reels_hastag")
        self.post_reels_hastag.setFont(font)
        self.post_reels_hastag.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_3.addWidget(self.post_reels_hastag)


        self.gridLayout_2.addWidget(self.groupBox_4, 3, 0, 2, 1)

        self.groupBox_6 = QGroupBox(self.PostReel)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.check_in = QCheckBox(self.groupBox_6)
        self.check_in.setObjectName(u"check_in")

        self.verticalLayout_2.addWidget(self.check_in)

        self.check_in_word = QPlainTextEdit(self.groupBox_6)
        self.check_in_word.setObjectName(u"check_in_word")
        self.check_in_word.setFont(font)
        self.check_in_word.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_2.addWidget(self.check_in_word)


        self.gridLayout_2.addWidget(self.groupBox_6, 4, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.PostReel)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(0, 300))
        self.groupBox_2.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.widget_2 = QWidget(self.groupBox_2)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_13 = QLabel(self.widget_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.label_13)

        self.videos_reel_path = QLineEdit(self.widget_2)
        self.videos_reel_path.setObjectName(u"videos_reel_path")
        self.videos_reel_path.setMinimumSize(QSize(300, 0))
        self.videos_reel_path.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_3.addWidget(self.videos_reel_path)

        self.browse_video_reel_path = QPushButton(self.widget_2)
        self.browse_video_reel_path.setObjectName(u"browse_video_reel_path")
        self.browse_video_reel_path.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.browse_video_reel_path.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/folder.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.browse_video_reel_path.setIcon(icon1)
        self.browse_video_reel_path.setIconSize(QSize(20, 24))

        self.horizontalLayout_3.addWidget(self.browse_video_reel_path)

        self.refresh_video_reel_path = QPushButton(self.widget_2)
        self.refresh_video_reel_path.setObjectName(u"refresh_video_reel_path")
        self.refresh_video_reel_path.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.refresh_video_reel_path.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/refresh.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.refresh_video_reel_path.setIcon(icon2)
        self.refresh_video_reel_path.setIconSize(QSize(20, 24))

        self.horizontalLayout_3.addWidget(self.refresh_video_reel_path)

        self.open_location_videos_reel = QPushButton(self.widget_2)
        self.open_location_videos_reel.setObjectName(u"open_location_videos_reel")
        self.open_location_videos_reel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.open_location_videos_reel.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/1333974.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.open_location_videos_reel.setIcon(icon3)
        self.open_location_videos_reel.setIconSize(QSize(20, 24))

        self.horizontalLayout_3.addWidget(self.open_location_videos_reel)

        self.horizontalSpacer = QSpacerItem(219, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(True)
        self.label_3.setFont(font4)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.videos_reel_post_ready = QLabel(self.widget_2)
        self.videos_reel_post_ready.setObjectName(u"videos_reel_post_ready")
        self.videos_reel_post_ready.setFont(font4)

        self.horizontalLayout_3.addWidget(self.videos_reel_post_ready)


        self.verticalLayout_5.addWidget(self.widget_2)

        self.video_reel_table = QTableWidget(self.groupBox_2)
        if (self.video_reel_table.columnCount() < 6):
            self.video_reel_table.setColumnCount(6)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.video_reel_table.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.video_reel_table.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.video_reel_table.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.video_reel_table.setHorizontalHeaderItem(3, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.video_reel_table.setHorizontalHeaderItem(4, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.video_reel_table.setHorizontalHeaderItem(5, __qtablewidgetitem9)
        self.video_reel_table.setObjectName(u"video_reel_table")
        self.video_reel_table.setMinimumSize(QSize(0, 0))
        self.video_reel_table.setFont(font)
        self.video_reel_table.setFocusPolicy(Qt.NoFocus)
        self.video_reel_table.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.video_reel_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.video_reel_table.setDragDropOverwriteMode(False)
        self.video_reel_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.video_reel_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.video_reel_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.video_reel_table.setShowGrid(False)
        self.video_reel_table.setGridStyle(Qt.NoPen)
        self.video_reel_table.setSortingEnabled(True)
        self.video_reel_table.setCornerButtonEnabled(True)
        self.video_reel_table.horizontalHeader().setStretchLastSection(True)
        self.video_reel_table.verticalHeader().setProperty(u"showSortIndicator", True)
        self.video_reel_table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_5.addWidget(self.video_reel_table)


        self.gridLayout_2.addWidget(self.groupBox_2, 5, 0, 1, 3)

        self.tabWidget.addTab(self.PostReel, "")
        self.PostVideos = QWidget()
        self.PostVideos.setObjectName(u"PostVideos")
        self.gridLayout_8 = QGridLayout(self.PostVideos)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.groupBox_15 = QGroupBox(self.PostVideos)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.groupBox_15.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_15)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.post_video = QCheckBox(self.groupBox_15)
        self.post_video.setObjectName(u"post_video")
        self.post_video.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_26.addWidget(self.post_video)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_4)

        self.label_7 = QLabel(self.groupBox_15)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_26.addWidget(self.label_7)

        self.total_posts_video = QSpinBox(self.groupBox_15)
        self.total_posts_video.setObjectName(u"total_posts_video")
        self.total_posts_video.setMinimumSize(QSize(100, 0))
        self.total_posts_video.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.total_posts_video.setMinimum(1)

        self.horizontalLayout_26.addWidget(self.total_posts_video)

        self.label_8 = QLabel(self.groupBox_15)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_26.addWidget(self.label_8)


        self.verticalLayout_10.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.video_tag = QCheckBox(self.groupBox_15)
        self.video_tag.setObjectName(u"video_tag")
        self.video_tag.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_27.addWidget(self.video_tag)

        self.from_16 = QLabel(self.groupBox_15)
        self.from_16.setObjectName(u"from_16")
        self.from_16.setLayoutDirection(Qt.LeftToRight)
        self.from_16.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_27.addWidget(self.from_16)

        self.video_tag_from = QSpinBox(self.groupBox_15)
        self.video_tag_from.setObjectName(u"video_tag_from")
        self.video_tag_from.setMinimumSize(QSize(100, 0))
        self.video_tag_from.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_27.addWidget(self.video_tag_from)

        self.to_16 = QLabel(self.groupBox_15)
        self.to_16.setObjectName(u"to_16")
        self.to_16.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_16.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_27.addWidget(self.to_16)

        self.video_tag_to = QSpinBox(self.groupBox_15)
        self.video_tag_to.setObjectName(u"video_tag_to")
        self.video_tag_to.setMinimumSize(QSize(100, 0))
        self.video_tag_to.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.video_tag_to.setMinimum(1)

        self.horizontalLayout_27.addWidget(self.video_tag_to)

        self.horizontalLayout_27.setStretch(0, 11)
        self.horizontalLayout_27.setStretch(1, 1)

        self.verticalLayout_10.addLayout(self.horizontalLayout_27)

        self.ai_label_videos = QCheckBox(self.groupBox_15)
        self.ai_label_videos.setObjectName(u"ai_label_videos")

        self.verticalLayout_10.addWidget(self.ai_label_videos)


        self.gridLayout_8.addWidget(self.groupBox_15, 0, 0, 1, 1)

        self.groupBox_14 = QGroupBox(self.PostVideos)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setStyleSheet(u"background-color: rgb(194, 202, 250);\n"
"background-color: rgb(204, 211, 250);")
        self.verticalLayout = QVBoxLayout(self.groupBox_14)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.share_to_group_video = QCheckBox(self.groupBox_14)
        self.share_to_group_video.setObjectName(u"share_to_group_video")
        self.share_to_group_video.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_25.addWidget(self.share_to_group_video)

        self.from_15 = QLabel(self.groupBox_14)
        self.from_15.setObjectName(u"from_15")
        self.from_15.setLayoutDirection(Qt.LeftToRight)
        self.from_15.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_25.addWidget(self.from_15)

        self.share_to_group_from_video = QSpinBox(self.groupBox_14)
        self.share_to_group_from_video.setObjectName(u"share_to_group_from_video")
        self.share_to_group_from_video.setMinimumSize(QSize(100, 0))
        self.share_to_group_from_video.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_25.addWidget(self.share_to_group_from_video)

        self.to_15 = QLabel(self.groupBox_14)
        self.to_15.setObjectName(u"to_15")
        self.to_15.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_15.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_25.addWidget(self.to_15)

        self.share_to_group_to_video = QSpinBox(self.groupBox_14)
        self.share_to_group_to_video.setObjectName(u"share_to_group_to_video")
        self.share_to_group_to_video.setMinimumSize(QSize(100, 0))
        self.share_to_group_to_video.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.share_to_group_to_video.setMinimum(1)

        self.horizontalLayout_25.addWidget(self.share_to_group_to_video)

        self.horizontalLayout_25.setStretch(0, 11)
        self.horizontalLayout_25.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_25)

        self.frame_6 = QFrame(self.groupBox_14)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.share_to_group_use_by_suggest_video = QRadioButton(self.frame_6)
        self.share_to_group_use_by_suggest_video.setObjectName(u"share_to_group_use_by_suggest_video")
        self.share_to_group_use_by_suggest_video.setChecked(True)

        self.horizontalLayout_13.addWidget(self.share_to_group_use_by_suggest_video)

        self.share_to_group_use_by_seleted_video = QRadioButton(self.frame_6)
        self.share_to_group_use_by_seleted_video.setObjectName(u"share_to_group_use_by_seleted_video")

        self.horizontalLayout_13.addWidget(self.share_to_group_use_by_seleted_video)


        self.verticalLayout.addWidget(self.frame_6)

        self.frame_10 = QFrame(self.groupBox_14)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.share_to_group_tittle_videos = QCheckBox(self.frame_10)
        self.share_to_group_tittle_videos.setObjectName(u"share_to_group_tittle_videos")
        self.share_to_group_tittle_videos.setChecked(True)

        self.horizontalLayout_20.addWidget(self.share_to_group_tittle_videos)

        self.widget_10 = QWidget(self.frame_10)
        self.widget_10.setObjectName(u"widget_10")
        self.horizontalLayout_21 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.use_fixed_share_group_tittle_videos = QRadioButton(self.widget_10)
        self.use_fixed_share_group_tittle_videos.setObjectName(u"use_fixed_share_group_tittle_videos")
        self.use_fixed_share_group_tittle_videos.setChecked(True)

        self.horizontalLayout_21.addWidget(self.use_fixed_share_group_tittle_videos)

        self.use_random_share_group_tittle_videos = QRadioButton(self.widget_10)
        self.use_random_share_group_tittle_videos.setObjectName(u"use_random_share_group_tittle_videos")

        self.horizontalLayout_21.addWidget(self.use_random_share_group_tittle_videos)


        self.horizontalLayout_20.addWidget(self.widget_10)


        self.verticalLayout.addWidget(self.frame_10)

        self.share_group_tittle_videos_words = QPlainTextEdit(self.groupBox_14)
        self.share_group_tittle_videos_words.setObjectName(u"share_group_tittle_videos_words")
        self.share_group_tittle_videos_words.setFont(font)
        self.share_group_tittle_videos_words.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout.addWidget(self.share_group_tittle_videos_words)


        self.gridLayout_8.addWidget(self.groupBox_14, 0, 1, 2, 1)

        self.groupBox_10 = QGroupBox(self.PostVideos)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_10)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget_3 = QWidget(self.groupBox_10)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.video_use_tittle_from_videos = QRadioButton(self.widget_3)
        self.video_use_tittle_from_videos.setObjectName(u"video_use_tittle_from_videos")
        self.video_use_tittle_from_videos.setChecked(True)

        self.horizontalLayout_4.addWidget(self.video_use_tittle_from_videos)

        self.video_use_fixed_tittle = QRadioButton(self.widget_3)
        self.video_use_fixed_tittle.setObjectName(u"video_use_fixed_tittle")

        self.horizontalLayout_4.addWidget(self.video_use_fixed_tittle)


        self.verticalLayout_7.addWidget(self.widget_3)

        self.video_tittle_text = QPlainTextEdit(self.groupBox_10)
        self.video_tittle_text.setObjectName(u"video_tittle_text")
        self.video_tittle_text.setFont(font)
        self.video_tittle_text.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_7.addWidget(self.video_tittle_text)


        self.gridLayout_8.addWidget(self.groupBox_10, 1, 0, 1, 1)

        self.groupBox_13 = QGroupBox(self.PostVideos)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.gridLayout_7 = QGridLayout(self.groupBox_13)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.feeling_random_video = QRadioButton(self.groupBox_13)
        self.feeling_random_video.setObjectName(u"feeling_random_video")
        self.feeling_random_video.setChecked(True)

        self.gridLayout_7.addWidget(self.feeling_random_video, 0, 1, 1, 1)

        self.feeling_inlove_video = QRadioButton(self.groupBox_13)
        self.feeling_inlove_video.setObjectName(u"feeling_inlove_video")
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/loved.PNG", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.feeling_inlove_video.setIcon(icon4)
        self.feeling_inlove_video.setIconSize(QSize(25, 25))

        self.gridLayout_7.addWidget(self.feeling_inlove_video, 3, 2, 2, 2)

        self.feeling_lovely_video = QRadioButton(self.groupBox_13)
        self.feeling_lovely_video.setObjectName(u"feeling_lovely_video")
        self.feeling_lovely_video.setIcon(icon4)
        self.feeling_lovely_video.setIconSize(QSize(25, 25))

        self.gridLayout_7.addWidget(self.feeling_lovely_video, 4, 1, 1, 1)

        self.frame_5 = QFrame(self.groupBox_13)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.use_feeling_video = QCheckBox(self.frame_5)
        self.use_feeling_video.setObjectName(u"use_feeling_video")

        self.horizontalLayout_11.addWidget(self.use_feeling_video)

        self.widget_7 = QWidget(self.frame_5)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_12 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_11.addWidget(self.widget_7)


        self.gridLayout_7.addWidget(self.frame_5, 0, 0, 1, 1)

        self.feeling_blessed_video = QRadioButton(self.groupBox_13)
        self.feeling_blessed_video.setObjectName(u"feeling_blessed_video")
        icon5 = QIcon()
        icon5.addFile(u":/icons/images/blessed.PNG", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.feeling_blessed_video.setIcon(icon5)
        self.feeling_blessed_video.setIconSize(QSize(25, 25))

        self.gridLayout_7.addWidget(self.feeling_blessed_video, 4, 0, 1, 1)

        self.feeling_sad_video = QRadioButton(self.groupBox_13)
        self.feeling_sad_video.setObjectName(u"feeling_sad_video")
        icon6 = QIcon()
        icon6.addFile(u":/icons/images/sad.PNG", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.feeling_sad_video.setIcon(icon6)
        self.feeling_sad_video.setIconSize(QSize(25, 25))

        self.gridLayout_7.addWidget(self.feeling_sad_video, 1, 1, 3, 1)

        self.feeling_happy_video = QRadioButton(self.groupBox_13)
        self.feeling_happy_video.setObjectName(u"feeling_happy_video")
        icon7 = QIcon()
        icon7.addFile(u":/icons/images/happy.PNG", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.feeling_happy_video.setIcon(icon7)
        self.feeling_happy_video.setIconSize(QSize(25, 25))

        self.gridLayout_7.addWidget(self.feeling_happy_video, 1, 0, 3, 1)

        self.feeling_excited_video = QRadioButton(self.groupBox_13)
        self.feeling_excited_video.setObjectName(u"feeling_excited_video")
        icon8 = QIcon()
        icon8.addFile(u":/icons/images/excited.PNG", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.feeling_excited_video.setIcon(icon8)
        self.feeling_excited_video.setIconSize(QSize(25, 25))

        self.gridLayout_7.addWidget(self.feeling_excited_video, 5, 2, 1, 1)

        self.feeling_loved_video = QRadioButton(self.groupBox_13)
        self.feeling_loved_video.setObjectName(u"feeling_loved_video")
        self.feeling_loved_video.setIcon(icon4)
        self.feeling_loved_video.setIconSize(QSize(25, 25))

        self.gridLayout_7.addWidget(self.feeling_loved_video, 5, 0, 1, 1)

        self.feeling_crazy_video = QRadioButton(self.groupBox_13)
        self.feeling_crazy_video.setObjectName(u"feeling_crazy_video")
        icon9 = QIcon()
        icon9.addFile(u":/icons/images/crazy.PNG", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.feeling_crazy_video.setIcon(icon9)
        self.feeling_crazy_video.setIconSize(QSize(25, 25))

        self.gridLayout_7.addWidget(self.feeling_crazy_video, 5, 1, 1, 1)

        self.feeling_thankful_video = QRadioButton(self.groupBox_13)
        self.feeling_thankful_video.setObjectName(u"feeling_thankful_video")
        icon10 = QIcon()
        icon10.addFile(u":/icons/images/thankful.PNG", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.feeling_thankful_video.setIcon(icon10)
        self.feeling_thankful_video.setIconSize(QSize(25, 25))

        self.gridLayout_7.addWidget(self.feeling_thankful_video, 2, 2, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_13, 4, 0, 1, 1)

        self.groupBox_16 = QGroupBox(self.PostVideos)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.groupBox_16.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_16)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.video_check_in = QCheckBox(self.groupBox_16)
        self.video_check_in.setObjectName(u"video_check_in")

        self.verticalLayout_11.addWidget(self.video_check_in)

        self.video_check_in_word = QPlainTextEdit(self.groupBox_16)
        self.video_check_in_word.setObjectName(u"video_check_in_word")
        self.video_check_in_word.setFont(font)
        self.video_check_in_word.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_11.addWidget(self.video_check_in_word)


        self.gridLayout_8.addWidget(self.groupBox_16, 4, 1, 1, 1)

        self.groupBox_11 = QGroupBox(self.PostVideos)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setMinimumSize(QSize(0, 300))
        self.groupBox_11.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.widget_11 = QWidget(self.groupBox_11)
        self.widget_11.setObjectName(u"widget_11")
        self.widget_11.setStyleSheet(u"")
        self.horizontalLayout_17 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_15 = QLabel(self.widget_11)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setStyleSheet(u"")

        self.horizontalLayout_17.addWidget(self.label_15)

        self.videos_tab_videos_path = QLineEdit(self.widget_11)
        self.videos_tab_videos_path.setObjectName(u"videos_tab_videos_path")
        self.videos_tab_videos_path.setMinimumSize(QSize(300, 0))
        self.videos_tab_videos_path.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_17.addWidget(self.videos_tab_videos_path)

        self.browse_video_path = QPushButton(self.widget_11)
        self.browse_video_path.setObjectName(u"browse_video_path")
        self.browse_video_path.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.browse_video_path.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        self.browse_video_path.setIcon(icon1)
        self.browse_video_path.setIconSize(QSize(20, 24))

        self.horizontalLayout_17.addWidget(self.browse_video_path)

        self.refresh_video_path = QPushButton(self.widget_11)
        self.refresh_video_path.setObjectName(u"refresh_video_path")
        self.refresh_video_path.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.refresh_video_path.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        self.refresh_video_path.setIcon(icon2)
        self.refresh_video_path.setIconSize(QSize(20, 24))

        self.horizontalLayout_17.addWidget(self.refresh_video_path)

        self.open_location_videos = QPushButton(self.widget_11)
        self.open_location_videos.setObjectName(u"open_location_videos")
        self.open_location_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.open_location_videos.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        self.open_location_videos.setIcon(icon3)
        self.open_location_videos.setIconSize(QSize(20, 24))

        self.horizontalLayout_17.addWidget(self.open_location_videos)

        self.horizontalSpacer_5 = QSpacerItem(219, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_5)

        self.label_9 = QLabel(self.widget_11)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font4)

        self.horizontalLayout_17.addWidget(self.label_9)

        self.videos_post_ready = QLabel(self.widget_11)
        self.videos_post_ready.setObjectName(u"videos_post_ready")
        self.videos_post_ready.setFont(font4)

        self.horizontalLayout_17.addWidget(self.videos_post_ready)


        self.verticalLayout_8.addWidget(self.widget_11)

        self.video_table = QTableWidget(self.groupBox_11)
        if (self.video_table.columnCount() < 3):
            self.video_table.setColumnCount(3)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.video_table.setHorizontalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.video_table.setHorizontalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.video_table.setHorizontalHeaderItem(2, __qtablewidgetitem12)
        self.video_table.setObjectName(u"video_table")
        self.video_table.setMinimumSize(QSize(0, 0))
        self.video_table.setFont(font)
        self.video_table.setFocusPolicy(Qt.NoFocus)
        self.video_table.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.video_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.video_table.setDragDropOverwriteMode(False)
        self.video_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.video_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.video_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.video_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.video_table.setShowGrid(False)
        self.video_table.setGridStyle(Qt.NoPen)
        self.video_table.setSortingEnabled(True)
        self.video_table.setCornerButtonEnabled(True)
        self.video_table.horizontalHeader().setStretchLastSection(True)
        self.video_table.verticalHeader().setProperty(u"showSortIndicator", True)
        self.video_table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_8.addWidget(self.video_table)


        self.gridLayout_8.addWidget(self.groupBox_11, 5, 0, 1, 3)

        self.groupBox_18 = QGroupBox(self.PostVideos)
        self.groupBox_18.setObjectName(u"groupBox_18")
        self.groupBox_18.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_18)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frame_8 = QFrame(self.groupBox_18)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_30 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_30.setSpacing(0)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.hastag_video = QCheckBox(self.frame_8)
        self.hastag_video.setObjectName(u"hastag_video")

        self.horizontalLayout_30.addWidget(self.hastag_video)

        self.widget_13 = QWidget(self.frame_8)
        self.widget_13.setObjectName(u"widget_13")
        self.horizontalLayout_31 = QHBoxLayout(self.widget_13)
        self.horizontalLayout_31.setSpacing(0)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(0, 0, 0, 0)
        self.video_use_fixed_hastag = QRadioButton(self.widget_13)
        self.video_use_fixed_hastag.setObjectName(u"video_use_fixed_hastag")
        self.video_use_fixed_hastag.setChecked(True)

        self.horizontalLayout_31.addWidget(self.video_use_fixed_hastag)

        self.video_use_random_hastag = QRadioButton(self.widget_13)
        self.video_use_random_hastag.setObjectName(u"video_use_random_hastag")

        self.horizontalLayout_31.addWidget(self.video_use_random_hastag)


        self.horizontalLayout_30.addWidget(self.widget_13)


        self.verticalLayout_9.addWidget(self.frame_8)

        self.post_videos_hastag = QPlainTextEdit(self.groupBox_18)
        self.post_videos_hastag.setObjectName(u"post_videos_hastag")
        self.post_videos_hastag.setFont(font)
        self.post_videos_hastag.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_9.addWidget(self.post_videos_hastag)


        self.gridLayout_8.addWidget(self.groupBox_18, 2, 0, 2, 1)

        self.groupBox_17 = QGroupBox(self.PostVideos)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.groupBox_17.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_17)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.frame_7 = QFrame(self.groupBox_17)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.video_comments = QCheckBox(self.frame_7)
        self.video_comments.setObjectName(u"video_comments")

        self.horizontalLayout_14.addWidget(self.video_comments)

        self.widget_8 = QWidget(self.frame_7)
        self.widget_8.setObjectName(u"widget_8")
        self.horizontalLayout_15 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.video_comments_use_fixed = QRadioButton(self.widget_8)
        self.video_comments_use_fixed.setObjectName(u"video_comments_use_fixed")
        self.video_comments_use_fixed.setChecked(True)

        self.horizontalLayout_15.addWidget(self.video_comments_use_fixed)

        self.video_comments_use_random = QRadioButton(self.widget_8)
        self.video_comments_use_random.setObjectName(u"video_comments_use_random")

        self.horizontalLayout_15.addWidget(self.video_comments_use_random)


        self.horizontalLayout_14.addWidget(self.widget_8)


        self.verticalLayout_12.addWidget(self.frame_7)

        self.video_comments_text = QPlainTextEdit(self.groupBox_17)
        self.video_comments_text.setObjectName(u"video_comments_text")
        self.video_comments_text.setFont(font)
        self.video_comments_text.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_12.addWidget(self.video_comments_text)


        self.gridLayout_8.addWidget(self.groupBox_17, 2, 1, 1, 1)

        self.groupBox_12 = QGroupBox(self.PostVideos)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.gridLayout_6 = QGridLayout(self.groupBox_12)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.post_videos_group = QTableWidget(self.groupBox_12)
        if (self.post_videos_group.columnCount() < 2):
            self.post_videos_group.setColumnCount(2)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.post_videos_group.setHorizontalHeaderItem(0, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.post_videos_group.setHorizontalHeaderItem(1, __qtablewidgetitem14)
        self.post_videos_group.setObjectName(u"post_videos_group")
        self.post_videos_group.setMinimumSize(QSize(0, 0))
        self.post_videos_group.setFont(font)
        self.post_videos_group.setFocusPolicy(Qt.NoFocus)
        self.post_videos_group.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.post_videos_group.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.post_videos_group.setDragDropOverwriteMode(False)
        self.post_videos_group.setSelectionMode(QAbstractItemView.NoSelection)
        self.post_videos_group.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.post_videos_group.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.post_videos_group.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.post_videos_group.setShowGrid(False)
        self.post_videos_group.setGridStyle(Qt.NoPen)
        self.post_videos_group.setSortingEnabled(True)
        self.post_videos_group.setCornerButtonEnabled(True)
        self.post_videos_group.horizontalHeader().setStretchLastSection(True)
        self.post_videos_group.verticalHeader().setProperty(u"showSortIndicator", True)
        self.post_videos_group.verticalHeader().setStretchLastSection(False)

        self.gridLayout_6.addWidget(self.post_videos_group, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_12, 0, 2, 5, 1)

        self.tabWidget.addTab(self.PostVideos, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_11 = QGridLayout(self.tab)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.groupBox_19 = QGroupBox(self.tab)
        self.groupBox_19.setObjectName(u"groupBox_19")
        self.groupBox_19.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.gridLayout_10 = QGridLayout(self.groupBox_19)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.feeling_random_image = QRadioButton(self.groupBox_19)
        self.feeling_random_image.setObjectName(u"feeling_random_image")
        self.feeling_random_image.setChecked(True)

        self.gridLayout_10.addWidget(self.feeling_random_image, 0, 1, 1, 1)

        self.feeling_inlove_image = QRadioButton(self.groupBox_19)
        self.feeling_inlove_image.setObjectName(u"feeling_inlove_image")
        self.feeling_inlove_image.setIcon(icon4)
        self.feeling_inlove_image.setIconSize(QSize(25, 25))

        self.gridLayout_10.addWidget(self.feeling_inlove_image, 3, 2, 2, 2)

        self.feeling_lovely_image = QRadioButton(self.groupBox_19)
        self.feeling_lovely_image.setObjectName(u"feeling_lovely_image")
        self.feeling_lovely_image.setIcon(icon4)
        self.feeling_lovely_image.setIconSize(QSize(25, 25))

        self.gridLayout_10.addWidget(self.feeling_lovely_image, 4, 1, 1, 1)

        self.frame_12 = QFrame(self.groupBox_19)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_32 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_32.setSpacing(0)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.use_feeling_image = QCheckBox(self.frame_12)
        self.use_feeling_image.setObjectName(u"use_feeling_image")

        self.horizontalLayout_32.addWidget(self.use_feeling_image)

        self.widget_14 = QWidget(self.frame_12)
        self.widget_14.setObjectName(u"widget_14")
        self.horizontalLayout_33 = QHBoxLayout(self.widget_14)
        self.horizontalLayout_33.setSpacing(0)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_32.addWidget(self.widget_14)


        self.gridLayout_10.addWidget(self.frame_12, 0, 0, 1, 1)

        self.feeling_blessed_image = QRadioButton(self.groupBox_19)
        self.feeling_blessed_image.setObjectName(u"feeling_blessed_image")
        self.feeling_blessed_image.setIcon(icon5)
        self.feeling_blessed_image.setIconSize(QSize(25, 25))

        self.gridLayout_10.addWidget(self.feeling_blessed_image, 4, 0, 1, 1)

        self.feeling_sad_image = QRadioButton(self.groupBox_19)
        self.feeling_sad_image.setObjectName(u"feeling_sad_image")
        self.feeling_sad_image.setIcon(icon6)
        self.feeling_sad_image.setIconSize(QSize(25, 25))

        self.gridLayout_10.addWidget(self.feeling_sad_image, 1, 1, 3, 1)

        self.feeling_happy_image = QRadioButton(self.groupBox_19)
        self.feeling_happy_image.setObjectName(u"feeling_happy_image")
        self.feeling_happy_image.setIcon(icon7)
        self.feeling_happy_image.setIconSize(QSize(25, 25))

        self.gridLayout_10.addWidget(self.feeling_happy_image, 1, 0, 3, 1)

        self.feeling_excited_image = QRadioButton(self.groupBox_19)
        self.feeling_excited_image.setObjectName(u"feeling_excited_image")
        self.feeling_excited_image.setIcon(icon8)
        self.feeling_excited_image.setIconSize(QSize(25, 25))

        self.gridLayout_10.addWidget(self.feeling_excited_image, 5, 2, 1, 1)

        self.feeling_loved_image = QRadioButton(self.groupBox_19)
        self.feeling_loved_image.setObjectName(u"feeling_loved_image")
        self.feeling_loved_image.setIcon(icon4)
        self.feeling_loved_image.setIconSize(QSize(25, 25))

        self.gridLayout_10.addWidget(self.feeling_loved_image, 5, 0, 1, 1)

        self.feeling_crazy_image = QRadioButton(self.groupBox_19)
        self.feeling_crazy_image.setObjectName(u"feeling_crazy_image")
        self.feeling_crazy_image.setIcon(icon9)
        self.feeling_crazy_image.setIconSize(QSize(25, 25))

        self.gridLayout_10.addWidget(self.feeling_crazy_image, 5, 1, 1, 1)

        self.feeling_thankful_image = QRadioButton(self.groupBox_19)
        self.feeling_thankful_image.setObjectName(u"feeling_thankful_image")
        self.feeling_thankful_image.setIcon(icon10)
        self.feeling_thankful_image.setIconSize(QSize(25, 25))

        self.gridLayout_10.addWidget(self.feeling_thankful_image, 2, 2, 1, 1)


        self.gridLayout_11.addWidget(self.groupBox_19, 5, 0, 1, 1)

        self.groupBox_42 = QGroupBox(self.tab)
        self.groupBox_42.setObjectName(u"groupBox_42")
        self.groupBox_42.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_31 = QVBoxLayout(self.groupBox_42)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.check_in_image = QCheckBox(self.groupBox_42)
        self.check_in_image.setObjectName(u"check_in_image")

        self.verticalLayout_31.addWidget(self.check_in_image)

        self.check_in_image_word = QPlainTextEdit(self.groupBox_42)
        self.check_in_image_word.setObjectName(u"check_in_image_word")
        self.check_in_image_word.setFont(font)
        self.check_in_image_word.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_31.addWidget(self.check_in_image_word)


        self.gridLayout_11.addWidget(self.groupBox_42, 5, 1, 1, 1)

        self.groupBox_35 = QGroupBox(self.tab)
        self.groupBox_35.setObjectName(u"groupBox_35")
        self.groupBox_35.setMinimumSize(QSize(0, 300))
        self.groupBox_35.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_26 = QVBoxLayout(self.groupBox_35)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.widget_20 = QWidget(self.groupBox_35)
        self.widget_20.setObjectName(u"widget_20")
        self.widget_20.setStyleSheet(u"")
        self.horizontalLayout_16 = QHBoxLayout(self.widget_20)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_19 = QLabel(self.widget_20)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setStyleSheet(u"")

        self.horizontalLayout_16.addWidget(self.label_19)

        self.image_path = QLineEdit(self.widget_20)
        self.image_path.setObjectName(u"image_path")
        self.image_path.setMinimumSize(QSize(300, 0))
        self.image_path.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_16.addWidget(self.image_path)

        self.browse_image_path = QPushButton(self.widget_20)
        self.browse_image_path.setObjectName(u"browse_image_path")
        self.browse_image_path.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.browse_image_path.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        self.browse_image_path.setIcon(icon1)
        self.browse_image_path.setIconSize(QSize(20, 24))

        self.horizontalLayout_16.addWidget(self.browse_image_path)

        self.refresh_image_path = QPushButton(self.widget_20)
        self.refresh_image_path.setObjectName(u"refresh_image_path")
        self.refresh_image_path.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.refresh_image_path.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        self.refresh_image_path.setIcon(icon2)
        self.refresh_image_path.setIconSize(QSize(20, 24))

        self.horizontalLayout_16.addWidget(self.refresh_image_path)

        self.open_location_image = QPushButton(self.widget_20)
        self.open_location_image.setObjectName(u"open_location_image")
        self.open_location_image.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.open_location_image.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        self.open_location_image.setIcon(icon3)
        self.open_location_image.setIconSize(QSize(20, 24))

        self.horizontalLayout_16.addWidget(self.open_location_image)

        self.horizontalSpacer_13 = QSpacerItem(231, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_13)

        self.label_20 = QLabel(self.widget_20)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font4)

        self.horizontalLayout_16.addWidget(self.label_20)

        self.images_post_ready = QLabel(self.widget_20)
        self.images_post_ready.setObjectName(u"images_post_ready")
        self.images_post_ready.setFont(font4)

        self.horizontalLayout_16.addWidget(self.images_post_ready)


        self.verticalLayout_26.addWidget(self.widget_20)

        self.images_table = QTableWidget(self.groupBox_35)
        if (self.images_table.columnCount() < 5):
            self.images_table.setColumnCount(5)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.images_table.setHorizontalHeaderItem(0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.images_table.setHorizontalHeaderItem(1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.images_table.setHorizontalHeaderItem(2, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.images_table.setHorizontalHeaderItem(3, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.images_table.setHorizontalHeaderItem(4, __qtablewidgetitem19)
        self.images_table.setObjectName(u"images_table")
        self.images_table.setMinimumSize(QSize(0, 0))
        self.images_table.setFont(font)
        self.images_table.setFocusPolicy(Qt.NoFocus)
        self.images_table.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.images_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.images_table.setDragDropOverwriteMode(False)
        self.images_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.images_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.images_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.images_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.images_table.setShowGrid(False)
        self.images_table.setGridStyle(Qt.NoPen)
        self.images_table.setSortingEnabled(True)
        self.images_table.setCornerButtonEnabled(True)
        self.images_table.horizontalHeader().setStretchLastSection(True)
        self.images_table.verticalHeader().setProperty(u"showSortIndicator", True)
        self.images_table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_26.addWidget(self.images_table)


        self.gridLayout_11.addWidget(self.groupBox_35, 6, 0, 1, 3)

        self.groupBox_39 = QGroupBox(self.tab)
        self.groupBox_39.setObjectName(u"groupBox_39")
        self.groupBox_39.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_28 = QVBoxLayout(self.groupBox_39)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.horizontalLayout_52 = QHBoxLayout()
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.post_image = QCheckBox(self.groupBox_39)
        self.post_image.setObjectName(u"post_image")
        self.post_image.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_52.addWidget(self.post_image)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_52.addItem(self.horizontalSpacer_14)

        self.label_21 = QLabel(self.groupBox_39)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_52.addWidget(self.label_21)

        self.total_posts_image = QSpinBox(self.groupBox_39)
        self.total_posts_image.setObjectName(u"total_posts_image")
        self.total_posts_image.setMinimumSize(QSize(100, 0))
        self.total_posts_image.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.total_posts_image.setMinimum(1)

        self.horizontalLayout_52.addWidget(self.total_posts_image)


        self.verticalLayout_28.addLayout(self.horizontalLayout_52)

        self.horizontalLayout_53 = QHBoxLayout()
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.tag_image = QCheckBox(self.groupBox_39)
        self.tag_image.setObjectName(u"tag_image")
        self.tag_image.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_53.addWidget(self.tag_image)

        self.from_22 = QLabel(self.groupBox_39)
        self.from_22.setObjectName(u"from_22")
        self.from_22.setLayoutDirection(Qt.LeftToRight)
        self.from_22.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_53.addWidget(self.from_22)

        self.tag_from_image = QSpinBox(self.groupBox_39)
        self.tag_from_image.setObjectName(u"tag_from_image")
        self.tag_from_image.setMinimumSize(QSize(100, 0))
        self.tag_from_image.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_53.addWidget(self.tag_from_image)

        self.to_22 = QLabel(self.groupBox_39)
        self.to_22.setObjectName(u"to_22")
        self.to_22.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_22.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_53.addWidget(self.to_22)

        self.tag_to_image = QSpinBox(self.groupBox_39)
        self.tag_to_image.setObjectName(u"tag_to_image")
        self.tag_to_image.setMinimumSize(QSize(100, 0))
        self.tag_to_image.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.tag_to_image.setMinimum(1)

        self.horizontalLayout_53.addWidget(self.tag_to_image)

        self.horizontalLayout_53.setStretch(0, 11)
        self.horizontalLayout_53.setStretch(1, 1)

        self.verticalLayout_28.addLayout(self.horizontalLayout_53)

        self.horizontalLayout_56 = QHBoxLayout()
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.label_23 = QLabel(self.groupBox_39)
        self.label_23.setObjectName(u"label_23")

        self.horizontalLayout_56.addWidget(self.label_23)

        self.total_per_post_image = QSpinBox(self.groupBox_39)
        self.total_per_post_image.setObjectName(u"total_per_post_image")
        self.total_per_post_image.setMinimumSize(QSize(100, 0))
        self.total_per_post_image.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.total_per_post_image.setMinimum(1)

        self.horizontalLayout_56.addWidget(self.total_per_post_image)


        self.verticalLayout_28.addLayout(self.horizontalLayout_56)

        self.ai_label_image = QCheckBox(self.groupBox_39)
        self.ai_label_image.setObjectName(u"ai_label_image")

        self.verticalLayout_28.addWidget(self.ai_label_image)


        self.gridLayout_11.addWidget(self.groupBox_39, 0, 0, 1, 1)

        self.groupBox_37 = QGroupBox(self.tab)
        self.groupBox_37.setObjectName(u"groupBox_37")
        self.groupBox_37.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_27 = QVBoxLayout(self.groupBox_37)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.frame_14 = QFrame(self.groupBox_37)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_46 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_46.setSpacing(0)
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.horizontalLayout_46.setContentsMargins(0, 0, 0, 0)
        self.hastag_image = QCheckBox(self.frame_14)
        self.hastag_image.setObjectName(u"hastag_image")

        self.horizontalLayout_46.addWidget(self.hastag_image)

        self.widget_21 = QWidget(self.frame_14)
        self.widget_21.setObjectName(u"widget_21")
        self.horizontalLayout_47 = QHBoxLayout(self.widget_21)
        self.horizontalLayout_47.setSpacing(0)
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.horizontalLayout_47.setContentsMargins(0, 0, 0, 0)
        self.use_fixed_hastag_image = QRadioButton(self.widget_21)
        self.use_fixed_hastag_image.setObjectName(u"use_fixed_hastag_image")
        self.use_fixed_hastag_image.setChecked(True)

        self.horizontalLayout_47.addWidget(self.use_fixed_hastag_image)

        self.use_random_hastag_image = QRadioButton(self.widget_21)
        self.use_random_hastag_image.setObjectName(u"use_random_hastag_image")

        self.horizontalLayout_47.addWidget(self.use_random_hastag_image)


        self.horizontalLayout_46.addWidget(self.widget_21)


        self.verticalLayout_27.addWidget(self.frame_14)

        self.image_hastag_word = QPlainTextEdit(self.groupBox_37)
        self.image_hastag_word.setObjectName(u"image_hastag_word")
        self.image_hastag_word.setFont(font)
        self.image_hastag_word.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_27.addWidget(self.image_hastag_word)


        self.gridLayout_11.addWidget(self.groupBox_37, 4, 0, 1, 1)

        self.groupBox_43 = QGroupBox(self.tab)
        self.groupBox_43.setObjectName(u"groupBox_43")
        self.groupBox_43.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_32 = QVBoxLayout(self.groupBox_43)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.frame_16 = QFrame(self.groupBox_43)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_54 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_54.setSpacing(0)
        self.horizontalLayout_54.setObjectName(u"horizontalLayout_54")
        self.horizontalLayout_54.setContentsMargins(0, 0, 0, 0)
        self.comments_image = QCheckBox(self.frame_16)
        self.comments_image.setObjectName(u"comments_image")

        self.horizontalLayout_54.addWidget(self.comments_image)

        self.widget_22 = QWidget(self.frame_16)
        self.widget_22.setObjectName(u"widget_22")
        self.horizontalLayout_55 = QHBoxLayout(self.widget_22)
        self.horizontalLayout_55.setSpacing(0)
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.horizontalLayout_55.setContentsMargins(0, 0, 0, 0)
        self.comments_use_fixed_image = QRadioButton(self.widget_22)
        self.comments_use_fixed_image.setObjectName(u"comments_use_fixed_image")
        self.comments_use_fixed_image.setChecked(True)

        self.horizontalLayout_55.addWidget(self.comments_use_fixed_image)

        self.comments_use_random_image = QRadioButton(self.widget_22)
        self.comments_use_random_image.setObjectName(u"comments_use_random_image")

        self.horizontalLayout_55.addWidget(self.comments_use_random_image)


        self.horizontalLayout_54.addWidget(self.widget_22)


        self.verticalLayout_32.addWidget(self.frame_16)

        self.comments_image_word = QPlainTextEdit(self.groupBox_43)
        self.comments_image_word.setObjectName(u"comments_image_word")
        self.comments_image_word.setFont(font)
        self.comments_image_word.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_32.addWidget(self.comments_image_word)


        self.gridLayout_11.addWidget(self.groupBox_43, 3, 1, 2, 1)

        self.groupBox_38 = QGroupBox(self.tab)
        self.groupBox_38.setObjectName(u"groupBox_38")
        self.groupBox_38.setStyleSheet(u"background-color: rgb(194, 202, 250);\n"
"background-color: rgb(204, 211, 250);")
        self.verticalLayout_13 = QVBoxLayout(self.groupBox_38)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout_50 = QHBoxLayout()
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.share_to_group_image = QCheckBox(self.groupBox_38)
        self.share_to_group_image.setObjectName(u"share_to_group_image")
        self.share_to_group_image.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_50.addWidget(self.share_to_group_image)

        self.from_21 = QLabel(self.groupBox_38)
        self.from_21.setObjectName(u"from_21")
        self.from_21.setLayoutDirection(Qt.LeftToRight)
        self.from_21.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_50.addWidget(self.from_21)

        self.share_to_group_from_image = QSpinBox(self.groupBox_38)
        self.share_to_group_from_image.setObjectName(u"share_to_group_from_image")
        self.share_to_group_from_image.setMinimumSize(QSize(100, 0))
        self.share_to_group_from_image.setStyleSheet(u"background-color: rgb(136, 199, 247);")

        self.horizontalLayout_50.addWidget(self.share_to_group_from_image)

        self.to_21 = QLabel(self.groupBox_38)
        self.to_21.setObjectName(u"to_21")
        self.to_21.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.to_21.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_50.addWidget(self.to_21)

        self.share_to_group_to_image = QSpinBox(self.groupBox_38)
        self.share_to_group_to_image.setObjectName(u"share_to_group_to_image")
        self.share_to_group_to_image.setMinimumSize(QSize(100, 0))
        self.share_to_group_to_image.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.share_to_group_to_image.setMinimum(1)

        self.horizontalLayout_50.addWidget(self.share_to_group_to_image)

        self.horizontalLayout_50.setStretch(0, 11)
        self.horizontalLayout_50.setStretch(1, 1)

        self.verticalLayout_13.addLayout(self.horizontalLayout_50)

        self.frame_15 = QFrame(self.groupBox_38)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_51 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_51.setSpacing(0)
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.horizontalLayout_51.setContentsMargins(0, 0, 0, 0)
        self.share_to_group_use_by_suggest_image = QRadioButton(self.frame_15)
        self.share_to_group_use_by_suggest_image.setObjectName(u"share_to_group_use_by_suggest_image")
        self.share_to_group_use_by_suggest_image.setChecked(True)

        self.horizontalLayout_51.addWidget(self.share_to_group_use_by_suggest_image)

        self.share_to_group_use_by_seleted_image = QRadioButton(self.frame_15)
        self.share_to_group_use_by_seleted_image.setObjectName(u"share_to_group_use_by_seleted_image")

        self.horizontalLayout_51.addWidget(self.share_to_group_use_by_seleted_image)


        self.verticalLayout_13.addWidget(self.frame_15)

        self.frame_11 = QFrame(self.groupBox_38)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.share_to_group_tittle_image = QCheckBox(self.frame_11)
        self.share_to_group_tittle_image.setObjectName(u"share_to_group_tittle_image")
        self.share_to_group_tittle_image.setChecked(True)

        self.horizontalLayout_28.addWidget(self.share_to_group_tittle_image)

        self.widget_12 = QWidget(self.frame_11)
        self.widget_12.setObjectName(u"widget_12")
        self.horizontalLayout_29 = QHBoxLayout(self.widget_12)
        self.horizontalLayout_29.setSpacing(0)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.use_fixed_share_group_tittle_image = QRadioButton(self.widget_12)
        self.use_fixed_share_group_tittle_image.setObjectName(u"use_fixed_share_group_tittle_image")
        self.use_fixed_share_group_tittle_image.setChecked(True)

        self.horizontalLayout_29.addWidget(self.use_fixed_share_group_tittle_image)

        self.use_random_share_group_tittle_image = QRadioButton(self.widget_12)
        self.use_random_share_group_tittle_image.setObjectName(u"use_random_share_group_tittle_image")

        self.horizontalLayout_29.addWidget(self.use_random_share_group_tittle_image)


        self.horizontalLayout_28.addWidget(self.widget_12)


        self.verticalLayout_13.addWidget(self.frame_11)

        self.share_to_group_word_image = QPlainTextEdit(self.groupBox_38)
        self.share_to_group_word_image.setObjectName(u"share_to_group_word_image")
        self.share_to_group_word_image.setFont(font)
        self.share_to_group_word_image.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_13.addWidget(self.share_to_group_word_image)


        self.gridLayout_11.addWidget(self.groupBox_38, 0, 1, 2, 1)

        self.groupBox_34 = QGroupBox(self.tab)
        self.groupBox_34.setObjectName(u"groupBox_34")
        self.groupBox_34.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_25 = QVBoxLayout(self.groupBox_34)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.widget_19 = QWidget(self.groupBox_34)
        self.widget_19.setObjectName(u"widget_19")
        self.horizontalLayout_44 = QHBoxLayout(self.widget_19)
        self.horizontalLayout_44.setSpacing(0)
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.horizontalLayout_44.setContentsMargins(0, 0, 0, 0)
        self.use_tittle_from_image = QRadioButton(self.widget_19)
        self.use_tittle_from_image.setObjectName(u"use_tittle_from_image")
        self.use_tittle_from_image.setChecked(True)

        self.horizontalLayout_44.addWidget(self.use_tittle_from_image)

        self.use_fixed_tittle_image = QRadioButton(self.widget_19)
        self.use_fixed_tittle_image.setObjectName(u"use_fixed_tittle_image")

        self.horizontalLayout_44.addWidget(self.use_fixed_tittle_image)


        self.verticalLayout_25.addWidget(self.widget_19)

        self.tittle_image_word = QPlainTextEdit(self.groupBox_34)
        self.tittle_image_word.setObjectName(u"tittle_image_word")
        self.tittle_image_word.setFont(font)
        self.tittle_image_word.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.verticalLayout_25.addWidget(self.tittle_image_word)


        self.gridLayout_11.addWidget(self.groupBox_34, 1, 0, 3, 1)

        self.groupBox_36 = QGroupBox(self.tab)
        self.groupBox_36.setObjectName(u"groupBox_36")
        self.groupBox_36.setStyleSheet(u"background-color: rgb(194, 202, 250);")
        self.gridLayout_15 = QGridLayout(self.groupBox_36)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.post_image_group = QTableWidget(self.groupBox_36)
        if (self.post_image_group.columnCount() < 2):
            self.post_image_group.setColumnCount(2)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.post_image_group.setHorizontalHeaderItem(0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.post_image_group.setHorizontalHeaderItem(1, __qtablewidgetitem21)
        self.post_image_group.setObjectName(u"post_image_group")
        self.post_image_group.setMinimumSize(QSize(0, 0))
        self.post_image_group.setFont(font)
        self.post_image_group.setFocusPolicy(Qt.NoFocus)
        self.post_image_group.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.post_image_group.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.post_image_group.setDragDropOverwriteMode(False)
        self.post_image_group.setSelectionMode(QAbstractItemView.NoSelection)
        self.post_image_group.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.post_image_group.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.post_image_group.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.post_image_group.setShowGrid(False)
        self.post_image_group.setGridStyle(Qt.NoPen)
        self.post_image_group.setSortingEnabled(True)
        self.post_image_group.setCornerButtonEnabled(True)
        self.post_image_group.horizontalHeader().setStretchLastSection(True)
        self.post_image_group.verticalHeader().setProperty(u"showSortIndicator", True)
        self.post_image_group.verticalHeader().setStretchLastSection(False)

        self.gridLayout_15.addWidget(self.post_image_group, 0, 0, 1, 1)


        self.gridLayout_11.addWidget(self.groupBox_36, 0, 2, 6, 1)

        self.groupBox_44 = QGroupBox(self.tab)
        self.groupBox_44.setObjectName(u"groupBox_44")
        self.groupBox_44.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_33 = QVBoxLayout(self.groupBox_44)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.frame_17 = QFrame(self.groupBox_44)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_57 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_57.setSpacing(0)
        self.horizontalLayout_57.setObjectName(u"horizontalLayout_57")
        self.horizontalLayout_57.setContentsMargins(0, 0, 0, 0)
        self.widget_23 = QWidget(self.frame_17)
        self.widget_23.setObjectName(u"widget_23")
        self.horizontalLayout_58 = QHBoxLayout(self.widget_23)
        self.horizontalLayout_58.setSpacing(0)
        self.horizontalLayout_58.setObjectName(u"horizontalLayout_58")
        self.horizontalLayout_58.setContentsMargins(0, 0, 0, 0)
        self.classic = QRadioButton(self.widget_23)
        self.classic.setObjectName(u"classic")
        self.classic.setChecked(True)

        self.horizontalLayout_58.addWidget(self.classic)

        self.column = QRadioButton(self.widget_23)
        self.column.setObjectName(u"column")

        self.horizontalLayout_58.addWidget(self.column)

        self.banner = QRadioButton(self.widget_23)
        self.banner.setObjectName(u"banner")

        self.horizontalLayout_58.addWidget(self.banner)

        self.frame_layout = QRadioButton(self.widget_23)
        self.frame_layout.setObjectName(u"frame_layout")

        self.horizontalLayout_58.addWidget(self.frame_layout)


        self.horizontalLayout_57.addWidget(self.widget_23)


        self.verticalLayout_33.addWidget(self.frame_17)


        self.gridLayout_11.addWidget(self.groupBox_44, 2, 1, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.gridLayout_25 = QGridLayout(self.tab_5)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.groupBox_40 = QGroupBox(self.tab_5)
        self.groupBox_40.setObjectName(u"groupBox_40")
        self.groupBox_40.setStyleSheet(u"background-color: rgb(204, 211, 250);")
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_40)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_48 = QHBoxLayout()
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.post_story = QCheckBox(self.groupBox_40)
        self.post_story.setObjectName(u"post_story")
        self.post_story.setStyleSheet(u"background-color: rgb(204, 211, 250);")

        self.horizontalLayout_48.addWidget(self.post_story)

        self.label_25 = QLabel(self.groupBox_40)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_48.addWidget(self.label_25)

        self.total_post_story = QSpinBox(self.groupBox_40)
        self.total_post_story.setObjectName(u"total_post_story")
        self.total_post_story.setMinimumSize(QSize(100, 0))
        self.total_post_story.setStyleSheet(u"background-color: rgb(136, 199, 247);")
        self.total_post_story.setMinimum(1)

        self.horizontalLayout_48.addWidget(self.total_post_story)

        self.label_26 = QLabel(self.groupBox_40)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_48.addWidget(self.label_26)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_48.addItem(self.horizontalSpacer_3)


        self.verticalLayout_14.addLayout(self.horizontalLayout_48)

        self.widget_24 = QWidget(self.groupBox_40)
        self.widget_24.setObjectName(u"widget_24")
        self.widget_24.setStyleSheet(u"")
        self.horizontalLayout_34 = QHBoxLayout(self.widget_24)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.label_22 = QLabel(self.widget_24)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setStyleSheet(u"")

        self.horizontalLayout_34.addWidget(self.label_22)

        self.story_path = QLineEdit(self.widget_24)
        self.story_path.setObjectName(u"story_path")
        self.story_path.setMinimumSize(QSize(300, 0))
        self.story_path.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_34.addWidget(self.story_path)

        self.browse_story_path = QPushButton(self.widget_24)
        self.browse_story_path.setObjectName(u"browse_story_path")
        self.browse_story_path.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.browse_story_path.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        self.browse_story_path.setIcon(icon1)
        self.browse_story_path.setIconSize(QSize(20, 24))

        self.horizontalLayout_34.addWidget(self.browse_story_path)

        self.refresh_story_path = QPushButton(self.widget_24)
        self.refresh_story_path.setObjectName(u"refresh_story_path")
        self.refresh_story_path.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.refresh_story_path.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        self.refresh_story_path.setIcon(icon2)
        self.refresh_story_path.setIconSize(QSize(20, 24))

        self.horizontalLayout_34.addWidget(self.refresh_story_path)

        self.open_location_story = QPushButton(self.widget_24)
        self.open_location_story.setObjectName(u"open_location_story")
        self.open_location_story.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.open_location_story.setStyleSheet(u"background-color: rgb(85, 85, 127);")
        self.open_location_story.setIcon(icon3)
        self.open_location_story.setIconSize(QSize(20, 24))

        self.horizontalLayout_34.addWidget(self.open_location_story)

        self.horizontalSpacer_15 = QSpacerItem(231, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_34.addItem(self.horizontalSpacer_15)

        self.label_24 = QLabel(self.widget_24)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font4)

        self.horizontalLayout_34.addWidget(self.label_24)

        self.story_post_ready = QLabel(self.widget_24)
        self.story_post_ready.setObjectName(u"story_post_ready")
        self.story_post_ready.setFont(font4)

        self.horizontalLayout_34.addWidget(self.story_post_ready)


        self.verticalLayout_14.addWidget(self.widget_24)

        self.story_table = QTableWidget(self.groupBox_40)
        if (self.story_table.columnCount() < 3):
            self.story_table.setColumnCount(3)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.story_table.setHorizontalHeaderItem(0, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.story_table.setHorizontalHeaderItem(1, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.story_table.setHorizontalHeaderItem(2, __qtablewidgetitem24)
        self.story_table.setObjectName(u"story_table")
        self.story_table.setMinimumSize(QSize(0, 300))
        self.story_table.setFont(font)
        self.story_table.setFocusPolicy(Qt.NoFocus)
        self.story_table.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.story_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.story_table.setDragDropOverwriteMode(False)
        self.story_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.story_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.story_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.story_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.story_table.setShowGrid(False)
        self.story_table.setGridStyle(Qt.NoPen)
        self.story_table.setSortingEnabled(True)
        self.story_table.setCornerButtonEnabled(True)
        self.story_table.horizontalHeader().setStretchLastSection(True)
        self.story_table.verticalHeader().setProperty(u"showSortIndicator", True)
        self.story_table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_14.addWidget(self.story_table)


        self.gridLayout_25.addWidget(self.groupBox_40, 2, 0, 2, 2)

        self.tabWidget.addTab(self.tab_5, "")

        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.horizontalLayout_2.addWidget(self.frame)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)


        self.retranslateUi(Post)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Post)
    # setupUi

    def retranslateUi(self, Post):
        Post.setWindowTitle(QCoreApplication.translate("Post", u"Post", None))
        self.groupBox.setTitle(QCoreApplication.translate("Post", u"Post", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Post", u"Post", None))
        self.post.setText(QCoreApplication.translate("Post", u"Post", None))
        self.label_6.setText(QCoreApplication.translate("Post", u"Total Posts", None))
        self.label_5.setText(QCoreApplication.translate("Post", u"Videos", None))
        self.tag.setText(QCoreApplication.translate("Post", u"Tag Peoples", None))
        self.from_14.setText(QCoreApplication.translate("Post", u"From :", None))
        self.to_14.setText(QCoreApplication.translate("Post", u"To :", None))
        self.ai_label_reels.setText(QCoreApplication.translate("Post", u"AI Label", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Post", u"Share", None))
        self.share_to_group.setText(QCoreApplication.translate("Post", u"Share To Groups", None))
        self.from_13.setText(QCoreApplication.translate("Post", u"From :", None))
        self.to_13.setText(QCoreApplication.translate("Post", u"To :", None))
        self.share_to_group_use_by_suggest.setText(QCoreApplication.translate("Post", u"Group Suggest   ", None))
        self.share_to_group_use_by_seleted.setText(QCoreApplication.translate("Post", u"Group by Seleted", None))
        self.share_to_group_word.setPlaceholderText(QCoreApplication.translate("Post", u"Cooking, Group 24H", None))
        self.share_to_group_tittle.setText(QCoreApplication.translate("Post", u"Tittle", None))
        self.use_fixed_share_group_tittle.setText(QCoreApplication.translate("Post", u"Use Fixed", None))
        self.use_random_share_group_tittle.setText(QCoreApplication.translate("Post", u"Use Random", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Post", u"Group", None))
        ___qtablewidgetitem = self.post_reels_group.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Post", u"ALL", None));
        ___qtablewidgetitem1 = self.post_reels_group.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Post", u"Group Name", None));

        __sortingEnabled = self.post_reels_group.isSortingEnabled()
        self.post_reels_group.setSortingEnabled(False)
        ___qtablewidgetitem2 = self.post_reels_group.item(0, 0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Post", u"SP1", None));
        self.post_reels_group.setSortingEnabled(__sortingEnabled)

        self.groupBox_5.setTitle(QCoreApplication.translate("Post", u"Set Up Tittle", None))
        self.use_tittle_from_videos.setText(QCoreApplication.translate("Post", u"Use Title From Videos", None))
        self.use_fixed_tittle.setText(QCoreApplication.translate("Post", u"Use Fixed Tittle", None))
        self.tittle_text.setPlaceholderText(QCoreApplication.translate("Post", u"Cooking Mokbang 2026", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("Post", u"Set Comments", None))
        self.comments.setText(QCoreApplication.translate("Post", u"Comments", None))
        self.comments_use_fixed.setText(QCoreApplication.translate("Post", u"Use Fixed", None))
        self.comments_use_random.setText(QCoreApplication.translate("Post", u"Use Random", None))
        self.comments_text.setPlaceholderText(QCoreApplication.translate("Post", u"#hastage, #Cooking", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Post", u"Set Up Hastag", None))
        self.hastag.setText(QCoreApplication.translate("Post", u"Hastag", None))
        self.use_fixed_hastag.setText(QCoreApplication.translate("Post", u"Use Fixed", None))
        self.use_random_hastag.setText(QCoreApplication.translate("Post", u"Use Random", None))
        self.post_reels_hastag.setPlaceholderText(QCoreApplication.translate("Post", u"#hastage, #Cooking", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Post", u"Set Up Location", None))
        self.check_in.setText(QCoreApplication.translate("Post", u"Location (Check In)", None))
        self.check_in_word.setPlaceholderText(QCoreApplication.translate("Post", u"Phnom Penh", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Post", u"Videos", None))
        self.label_13.setText(QCoreApplication.translate("Post", u"Path", None))
        self.browse_video_reel_path.setText(QCoreApplication.translate("Post", u"Folder", None))
        self.refresh_video_reel_path.setText(QCoreApplication.translate("Post", u"Refresh", None))
        self.open_location_videos_reel.setText(QCoreApplication.translate("Post", u"Open", None))
        self.label_3.setText(QCoreApplication.translate("Post", u"      Video Post Already :   ", None))
        self.videos_reel_post_ready.setText(QCoreApplication.translate("Post", u"0/0", None))
        ___qtablewidgetitem3 = self.video_reel_table.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Post", u"ID", None));
        ___qtablewidgetitem4 = self.video_reel_table.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Post", u"Thumbnail", None));
        ___qtablewidgetitem5 = self.video_reel_table.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Post", u"File Name", None));
        ___qtablewidgetitem6 = self.video_reel_table.horizontalHeaderItem(3)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Post", u"Duration", None));
        ___qtablewidgetitem7 = self.video_reel_table.horizontalHeaderItem(4)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Post", u"Size", None));
        ___qtablewidgetitem8 = self.video_reel_table.horizontalHeaderItem(5)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Post", u"Status", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PostReel), QCoreApplication.translate("Post", u"Post Reels", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("Post", u"Post", None))
        self.post_video.setText(QCoreApplication.translate("Post", u"Post", None))
        self.label_7.setText(QCoreApplication.translate("Post", u"Total Posts", None))
        self.label_8.setText(QCoreApplication.translate("Post", u"Videos", None))
        self.video_tag.setText(QCoreApplication.translate("Post", u"Tag Peoples", None))
        self.from_16.setText(QCoreApplication.translate("Post", u"From :", None))
        self.to_16.setText(QCoreApplication.translate("Post", u"To :", None))
        self.ai_label_videos.setText(QCoreApplication.translate("Post", u"AI Label", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("Post", u"Share", None))
        self.share_to_group_video.setText(QCoreApplication.translate("Post", u"Share To Groups", None))
        self.from_15.setText(QCoreApplication.translate("Post", u"From :", None))
        self.to_15.setText(QCoreApplication.translate("Post", u"To :", None))
        self.share_to_group_use_by_suggest_video.setText(QCoreApplication.translate("Post", u"Group Suggest   ", None))
        self.share_to_group_use_by_seleted_video.setText(QCoreApplication.translate("Post", u"Group by Seleted", None))
        self.share_to_group_tittle_videos.setText(QCoreApplication.translate("Post", u"Tittle", None))
        self.use_fixed_share_group_tittle_videos.setText(QCoreApplication.translate("Post", u"Use Fixed", None))
        self.use_random_share_group_tittle_videos.setText(QCoreApplication.translate("Post", u"Use Random", None))
        self.share_group_tittle_videos_words.setPlaceholderText(QCoreApplication.translate("Post", u"Cooking, Group 24H", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("Post", u"Set Up Tittle", None))
        self.video_use_tittle_from_videos.setText(QCoreApplication.translate("Post", u"Use Title From Videos", None))
        self.video_use_fixed_tittle.setText(QCoreApplication.translate("Post", u"Use Fixed Tittle", None))
        self.video_tittle_text.setPlaceholderText(QCoreApplication.translate("Post", u"Cooking Mokbang 2026", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("Post", u"Set Up Feelings", None))
        self.feeling_random_video.setText(QCoreApplication.translate("Post", u"Use Random", None))
        self.feeling_inlove_video.setText(QCoreApplication.translate("Post", u"in Love", None))
        self.feeling_lovely_video.setText(QCoreApplication.translate("Post", u"Lovely", None))
        self.use_feeling_video.setText(QCoreApplication.translate("Post", u"Feeling", None))
        self.feeling_blessed_video.setText(QCoreApplication.translate("Post", u"Blessed", None))
        self.feeling_sad_video.setText(QCoreApplication.translate("Post", u"Sad", None))
        self.feeling_happy_video.setText(QCoreApplication.translate("Post", u"Happy", None))
        self.feeling_excited_video.setText(QCoreApplication.translate("Post", u"Excited", None))
        self.feeling_loved_video.setText(QCoreApplication.translate("Post", u"Loved", None))
        self.feeling_crazy_video.setText(QCoreApplication.translate("Post", u"Crazy", None))
        self.feeling_thankful_video.setText(QCoreApplication.translate("Post", u"Thankful", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("Post", u"Set Up Location", None))
        self.video_check_in.setText(QCoreApplication.translate("Post", u"Location (Check In)", None))
        self.video_check_in_word.setPlaceholderText(QCoreApplication.translate("Post", u"Phnom Penh", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("Post", u"Videos", None))
        self.label_15.setText(QCoreApplication.translate("Post", u"Path", None))
        self.browse_video_path.setText(QCoreApplication.translate("Post", u"Folder", None))
        self.refresh_video_path.setText(QCoreApplication.translate("Post", u"Refresh", None))
        self.open_location_videos.setText(QCoreApplication.translate("Post", u"Open", None))
        self.label_9.setText(QCoreApplication.translate("Post", u"      Video Post Already :   ", None))
        self.videos_post_ready.setText(QCoreApplication.translate("Post", u"0/0", None))
        ___qtablewidgetitem9 = self.video_table.horizontalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Post", u"ID", None));
        ___qtablewidgetitem10 = self.video_table.horizontalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Post", u"Tittle", None));
        ___qtablewidgetitem11 = self.video_table.horizontalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Post", u"Status", None));
        self.groupBox_18.setTitle(QCoreApplication.translate("Post", u"Set Up Hastag", None))
        self.hastag_video.setText(QCoreApplication.translate("Post", u"Hastag", None))
        self.video_use_fixed_hastag.setText(QCoreApplication.translate("Post", u"Use Fixed", None))
        self.video_use_random_hastag.setText(QCoreApplication.translate("Post", u"Use Random", None))
        self.post_videos_hastag.setPlaceholderText(QCoreApplication.translate("Post", u"#hastage, #Cooking", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("Post", u"Set Comments", None))
        self.video_comments.setText(QCoreApplication.translate("Post", u"Comments", None))
        self.video_comments_use_fixed.setText(QCoreApplication.translate("Post", u"Use Fixed", None))
        self.video_comments_use_random.setText(QCoreApplication.translate("Post", u"Use Random", None))
        self.video_comments_text.setPlaceholderText(QCoreApplication.translate("Post", u"Hello every one", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("Post", u"Group", None))
        ___qtablewidgetitem12 = self.post_videos_group.horizontalHeaderItem(0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Post", u"ID", None));
        ___qtablewidgetitem13 = self.post_videos_group.horizontalHeaderItem(1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Post", u"Name", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PostVideos), QCoreApplication.translate("Post", u"Post Videos", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("Post", u"Set Up Feelings", None))
        self.feeling_random_image.setText(QCoreApplication.translate("Post", u"Use Random", None))
        self.feeling_inlove_image.setText(QCoreApplication.translate("Post", u"in Love", None))
        self.feeling_lovely_image.setText(QCoreApplication.translate("Post", u"Lovely", None))
        self.use_feeling_image.setText(QCoreApplication.translate("Post", u"Feeling", None))
        self.feeling_blessed_image.setText(QCoreApplication.translate("Post", u"Blessed", None))
        self.feeling_sad_image.setText(QCoreApplication.translate("Post", u"Sad", None))
        self.feeling_happy_image.setText(QCoreApplication.translate("Post", u"Happy", None))
        self.feeling_excited_image.setText(QCoreApplication.translate("Post", u"Excited", None))
        self.feeling_loved_image.setText(QCoreApplication.translate("Post", u"Loved", None))
        self.feeling_crazy_image.setText(QCoreApplication.translate("Post", u"Crazy", None))
        self.feeling_thankful_image.setText(QCoreApplication.translate("Post", u"Thankful", None))
        self.groupBox_42.setTitle(QCoreApplication.translate("Post", u"Set Up Location", None))
        self.check_in_image.setText(QCoreApplication.translate("Post", u"Location (Check In)", None))
        self.check_in_image_word.setPlaceholderText(QCoreApplication.translate("Post", u"Phnom Penh", None))
        self.groupBox_35.setTitle(QCoreApplication.translate("Post", u"Image", None))
        self.label_19.setText(QCoreApplication.translate("Post", u"Path", None))
        self.browse_image_path.setText(QCoreApplication.translate("Post", u"Folder", None))
        self.refresh_image_path.setText(QCoreApplication.translate("Post", u"Refresh", None))
        self.open_location_image.setText(QCoreApplication.translate("Post", u"Open", None))
        self.label_20.setText(QCoreApplication.translate("Post", u" Images Post Already :   ", None))
        self.images_post_ready.setText(QCoreApplication.translate("Post", u"0/0", None))
        ___qtablewidgetitem14 = self.images_table.horizontalHeaderItem(0)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Post", u"ID", None));
        ___qtablewidgetitem15 = self.images_table.horizontalHeaderItem(1)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Post", u"Thumbnail", None));
        ___qtablewidgetitem16 = self.images_table.horizontalHeaderItem(2)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("Post", u"Image Name", None));
        ___qtablewidgetitem17 = self.images_table.horizontalHeaderItem(3)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("Post", u"Size", None));
        ___qtablewidgetitem18 = self.images_table.horizontalHeaderItem(4)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("Post", u"Status", None));
        self.groupBox_39.setTitle(QCoreApplication.translate("Post", u"Post", None))
        self.post_image.setText(QCoreApplication.translate("Post", u"Post", None))
        self.label_21.setText(QCoreApplication.translate("Post", u"Total Posts", None))
        self.tag_image.setText(QCoreApplication.translate("Post", u"Tag Peoples", None))
        self.from_22.setText(QCoreApplication.translate("Post", u"From :", None))
        self.to_22.setText(QCoreApplication.translate("Post", u"To :", None))
        self.label_23.setText(QCoreApplication.translate("Post", u"Total Per Posts", None))
        self.ai_label_image.setText(QCoreApplication.translate("Post", u"AI Label", None))
        self.groupBox_37.setTitle(QCoreApplication.translate("Post", u"Set Up Hastag", None))
        self.hastag_image.setText(QCoreApplication.translate("Post", u"Hastag", None))
        self.use_fixed_hastag_image.setText(QCoreApplication.translate("Post", u"Use Fixed", None))
        self.use_random_hastag_image.setText(QCoreApplication.translate("Post", u"Use Random", None))
        self.image_hastag_word.setPlaceholderText(QCoreApplication.translate("Post", u"#hastage, #Cooking", None))
        self.groupBox_43.setTitle(QCoreApplication.translate("Post", u"Set Comments", None))
        self.comments_image.setText(QCoreApplication.translate("Post", u"Comments", None))
        self.comments_use_fixed_image.setText(QCoreApplication.translate("Post", u"Use Fixed", None))
        self.comments_use_random_image.setText(QCoreApplication.translate("Post", u"Use Random", None))
        self.comments_image_word.setPlaceholderText(QCoreApplication.translate("Post", u"Hello Every One", None))
        self.groupBox_38.setTitle(QCoreApplication.translate("Post", u"Share", None))
        self.share_to_group_image.setText(QCoreApplication.translate("Post", u"Share To Groups", None))
        self.from_21.setText(QCoreApplication.translate("Post", u"From :", None))
        self.to_21.setText(QCoreApplication.translate("Post", u"To :", None))
        self.share_to_group_use_by_suggest_image.setText(QCoreApplication.translate("Post", u"Group Suggest   ", None))
        self.share_to_group_use_by_seleted_image.setText(QCoreApplication.translate("Post", u"Group by Seleted", None))
        self.share_to_group_tittle_image.setText(QCoreApplication.translate("Post", u"Tittle", None))
        self.use_fixed_share_group_tittle_image.setText(QCoreApplication.translate("Post", u"Use Fixed", None))
        self.use_random_share_group_tittle_image.setText(QCoreApplication.translate("Post", u"Use Random", None))
        self.share_to_group_word_image.setPlaceholderText(QCoreApplication.translate("Post", u"Cooking, Group 24H", None))
        self.groupBox_34.setTitle(QCoreApplication.translate("Post", u"Set Up Tittle", None))
        self.use_tittle_from_image.setText(QCoreApplication.translate("Post", u"Use Title From Image", None))
        self.use_fixed_tittle_image.setText(QCoreApplication.translate("Post", u"Use Fixed Tittle", None))
        self.tittle_image_word.setPlaceholderText(QCoreApplication.translate("Post", u"Cooking Mokbang 2026", None))
        self.groupBox_36.setTitle(QCoreApplication.translate("Post", u"Group", None))
        ___qtablewidgetitem19 = self.post_image_group.horizontalHeaderItem(0)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("Post", u"ID", None));
        ___qtablewidgetitem20 = self.post_image_group.horizontalHeaderItem(1)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("Post", u"Name", None));
        self.groupBox_44.setTitle(QCoreApplication.translate("Post", u"Layout", None))
        self.classic.setText(QCoreApplication.translate("Post", u"Classic", None))
        self.column.setText(QCoreApplication.translate("Post", u"Column", None))
        self.banner.setText(QCoreApplication.translate("Post", u"Banner", None))
        self.frame_layout.setText(QCoreApplication.translate("Post", u"Frame", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Post", u"Post Image", None))
        self.groupBox_40.setTitle("")
        self.post_story.setText(QCoreApplication.translate("Post", u"Post", None))
        self.label_25.setText(QCoreApplication.translate("Post", u"Total Posts", None))
        self.label_26.setText(QCoreApplication.translate("Post", u"Videos", None))
        self.label_22.setText(QCoreApplication.translate("Post", u"Path", None))
        self.browse_story_path.setText(QCoreApplication.translate("Post", u"Folder", None))
        self.refresh_story_path.setText(QCoreApplication.translate("Post", u"Refresh", None))
        self.open_location_story.setText(QCoreApplication.translate("Post", u"Open", None))
        self.label_24.setText(QCoreApplication.translate("Post", u"Post Already :   ", None))
        self.story_post_ready.setText(QCoreApplication.translate("Post", u"0/0", None))
        ___qtablewidgetitem21 = self.story_table.horizontalHeaderItem(0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("Post", u"ID", None));
        ___qtablewidgetitem22 = self.story_table.horizontalHeaderItem(1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("Post", u"Tittle", None));
        ___qtablewidgetitem23 = self.story_table.horizontalHeaderItem(2)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("Post", u"Status", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("Post", u"Post Story", None))
    # retranslateUi

