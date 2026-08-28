# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDial,
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPlainTextEdit, QProgressBar,
    QPushButton, QScrollArea, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QTabWidget, QTableView,
    QVBoxLayout, QWidget)

from qplaintextsub import QPlainTextSub

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1213, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Widget.sizePolicy().hasHeightForWidth())
        Widget.setSizePolicy(sizePolicy)
        Widget.setMinimumSize(QSize(1110, 700))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush2 = QBrush(QColor(0, 0, 0, 128))
        brush2.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush2)
#endif
        Widget.setPalette(palette)
        Widget.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        Widget.setStyleSheet(u"QWidget {\n"
"	background-color: white;\n"
"	font-family: cantarell;\n"
"	font-size: 13px;\n"
"	color: black;\n"
"}\n"
"\n"
"QLabel {\n"
"	font-size: 16px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    border: 1px solid black; /* Black border */\n"
"    background-color: lightgray; /* Light gray background */\n"
"	font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: darkgray; /* Slightly darker background on hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: gray; /* Even darker background when pressed */\n"
"}\n"
"\n"
"QGroupBox {\n"
"	font-size: 20px;\n"
"    border: none; /* Removes the default border */\n"
"    border-top: 1px dashed black; /* Adds a border under the title */\n"
"    margin-top: 30px; /* Ensures space for the title */\n"
"    padding-top: 10px; /* Creates space above the border for the title */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin; /* Aligns the title with the margin */\n"
"    subcontrol-position: top left; /* Moves the"
                        " title to the top-left corner */\n"
"    padding: -5px; /* Adds padding around the title */\n"
"    background-color: white; /* Optional: matches the background */\n"
"}\n"
"\n"
"QTableView {\n"
"	border: none;\n"
"}\n"
"\n"
"QComboBox {\n"
"    background-color: white; /* Default background */\n"
"    color: black; /* Default text color */\n"
"    border: 1px solid black; /* Border around the combobox */\n"
"    padding: 2px 10px; /* Padding for text alignment */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: lightgray; /* Background of the dropdown */\n"
"    color: black; /* Text color of items in the dropdown */\n"
"    selection-background-color: darkgray; /* Background color when an item is selected */\n"
"    selection-color: white; /* Text color when an item is selected */\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"	alignment: left;\n"
"}\n"
"\n"
"QTabWidget {\n"
"	border: none;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"	width: 80px;\n"
"	height: 80px;\n"
"	margin: 0px;\n"
"	text-align: c"
                        "enter;\n"
"   border: none;\n"
"	border-right: 1px solid black;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"	background-color: #e0e0e0;\n"
"}\n"
"\n"
"#tab_basic {\n"
"	\n"
"}\n"
"\n"
"QDial {\n"
"    background-color: white;\n"
"    border: none;\n"
"}")
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.baseHeaderLayout = QHBoxLayout()
        self.baseHeaderLayout.setObjectName(u"baseHeaderLayout")
        self.baseHeaderLayout.setContentsMargins(10, 10, 10, -1)
        self.baseHeaderLeftLayout = QHBoxLayout()
        self.baseHeaderLeftLayout.setObjectName(u"baseHeaderLeftLayout")
        self.baseHeaderLeftLayout.setContentsMargins(0, -1, 0, -1)
        self.comboBoxSerialPorts = QComboBox(Widget)
        self.comboBoxSerialPorts.setObjectName(u"comboBoxSerialPorts")
        self.comboBoxSerialPorts.setMinimumSize(QSize(300, 0))

        self.baseHeaderLeftLayout.addWidget(self.comboBoxSerialPorts)

        self.pushButtonConnectDisconnect = QPushButton(Widget)
        self.pushButtonConnectDisconnect.setObjectName(u"pushButtonConnectDisconnect")

        self.baseHeaderLeftLayout.addWidget(self.pushButtonConnectDisconnect)

        self.line_4 = QFrame(Widget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShadow(QFrame.Plain)
        self.line_4.setFrameShape(QFrame.Shape.VLine)

        self.baseHeaderLeftLayout.addWidget(self.line_4)

        self.pushButtonSaveToModule = QPushButton(Widget)
        self.pushButtonSaveToModule.setObjectName(u"pushButtonSaveToModule")

        self.baseHeaderLeftLayout.addWidget(self.pushButtonSaveToModule)

        self.line_5 = QFrame(Widget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShadow(QFrame.Plain)
        self.line_5.setFrameShape(QFrame.Shape.VLine)

        self.baseHeaderLeftLayout.addWidget(self.line_5)

        self.checkBoxContinuousSMData = QCheckBox(Widget)
        self.checkBoxContinuousSMData.setObjectName(u"checkBoxContinuousSMData")

        self.baseHeaderLeftLayout.addWidget(self.checkBoxContinuousSMData)

        self.pushButtonLoadFromModule = QPushButton(Widget)
        self.pushButtonLoadFromModule.setObjectName(u"pushButtonLoadFromModule")

        self.baseHeaderLeftLayout.addWidget(self.pushButtonLoadFromModule)


        self.baseHeaderLayout.addLayout(self.baseHeaderLeftLayout)

        self.baseHeaderHorizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.baseHeaderLayout.addItem(self.baseHeaderHorizontalSpacer)

        self.baseHeaderRightLayout = QHBoxLayout()
        self.baseHeaderRightLayout.setObjectName(u"baseHeaderRightLayout")
        self.pushButtonShowConsole = QPushButton(Widget)
        self.pushButtonShowConsole.setObjectName(u"pushButtonShowConsole")
        self.pushButtonShowConsole.setMinimumSize(QSize(1, 0))
        self.pushButtonShowConsole.setMaximumSize(QSize(1, 16777215))

        self.baseHeaderRightLayout.addWidget(self.pushButtonShowConsole)

        self.pushButtonShowReference = QPushButton(Widget)
        self.pushButtonShowReference.setObjectName(u"pushButtonShowReference")
        self.pushButtonShowReference.setMinimumSize(QSize(1, 0))
        self.pushButtonShowReference.setMaximumSize(QSize(1, 16777215))

        self.baseHeaderRightLayout.addWidget(self.pushButtonShowReference)

        self.pushButtonPreferences = QPushButton(Widget)
        self.pushButtonPreferences.setObjectName(u"pushButtonPreferences")

        self.baseHeaderRightLayout.addWidget(self.pushButtonPreferences)

        self.pushButtonToggleSidebar = QPushButton(Widget)
        self.pushButtonToggleSidebar.setObjectName(u"pushButtonToggleSidebar")

        self.baseHeaderRightLayout.addWidget(self.pushButtonToggleSidebar)


        self.baseHeaderLayout.addLayout(self.baseHeaderRightLayout)


        self.verticalLayout.addLayout(self.baseHeaderLayout)

        self.line = QFrame(Widget)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 2))
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout.addWidget(self.line)

        self.baseMainLayout = QHBoxLayout()
        self.baseMainLayout.setObjectName(u"baseMainLayout")
        self.tabWidgetMain = QTabWidget(Widget)
        self.tabWidgetMain.setObjectName(u"tabWidgetMain")
        self.tabWidgetMain.setEnabled(True)
        self.tabWidgetMain.setMinimumSize(QSize(934, 0))
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush3 = QBrush(QColor(204, 215, 196, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Light, brush3)
        brush4 = QBrush(QColor(229, 235, 225, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Midlight, brush4)
        brush5 = QBrush(QColor(102, 108, 98, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Dark, brush5)
        brush6 = QBrush(QColor(136, 143, 130, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Mid, brush6)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush)
        palette1.setBrush(QPalette.Active, QPalette.BrightText, brush1)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette1.setBrush(QPalette.Active, QPalette.AlternateBase, brush4)
        brush7 = QBrush(QColor(255, 255, 220, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.ToolTipBase, brush7)
        palette1.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette1.setBrush(QPalette.Active, QPalette.Accent, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Light, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.Midlight, brush4)
        palette1.setBrush(QPalette.Inactive, QPalette.Dark, brush5)
        palette1.setBrush(QPalette.Inactive, QPalette.Mid, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.BrightText, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush4)
        palette1.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush7)
        palette1.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        palette1.setBrush(QPalette.Inactive, QPalette.Accent, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Light, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.Midlight, brush4)
        palette1.setBrush(QPalette.Disabled, QPalette.Dark, brush5)
        palette1.setBrush(QPalette.Disabled, QPalette.Mid, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.BrightText, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush7)
        palette1.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush2)
#endif
        palette1.setBrush(QPalette.Disabled, QPalette.Accent, brush3)
        self.tabWidgetMain.setPalette(palette1)
        self.tabWidgetMain.setAutoFillBackground(False)
        self.tabWidgetMain.setStyleSheet(u"")
        self.tabWidgetMain.setTabPosition(QTabWidget.West)
        self.tabWidgetMain.setTabShape(QTabWidget.Rounded)
        self.tabWidgetMain.setIconSize(QSize(70, 70))
        self.tab_basic = QWidget()
        self.tab_basic.setObjectName(u"tab_basic")
        self.horizontalLayout_5 = QHBoxLayout(self.tab_basic)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.tabBasicVerticaLayout = QVBoxLayout()
        self.tabBasicVerticaLayout.setObjectName(u"tabBasicVerticaLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox_2 = QGroupBox(self.tab_basic)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(359, 150))
        self.groupBox_2.setMaximumSize(QSize(16777215, 150))
        self.groupBox_2.setStyleSheet(u"")
        self.labelAnalyzeNote = QLabel(self.groupBox_2)
        self.labelAnalyzeNote.setObjectName(u"labelAnalyzeNote")
        self.labelAnalyzeNote.setGeometry(QRect(-20, 40, 71, 21))
        self.labelAnalyzeNote.setTextFormat(Qt.AutoText)
        self.labelAnalyzeNote.setAlignment(Qt.AlignCenter)
        self.labelAnalyzeCents = QLabel(self.groupBox_2)
        self.labelAnalyzeCents.setObjectName(u"labelAnalyzeCents")
        self.labelAnalyzeCents.setGeometry(QRect(40, 40, 51, 21))
        self.labelAnalyzeCents.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.horizontalSliderStringFrequency = QSlider(self.groupBox_2)
        self.horizontalSliderStringFrequency.setObjectName(u"horizontalSliderStringFrequency")
        self.horizontalSliderStringFrequency.setEnabled(True)
        self.horizontalSliderStringFrequency.setGeometry(QRect(10, 60, 226, 21))
        self.horizontalSliderStringFrequency.setStyleSheet(u"QSlider::groove:horizontal {\n"
"    border: none;\n"
"    height: 1px; /* Set the line thickness */\n"
"    background: black; /* Set the line color */\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: black; /* Set the triangle color */\n"
"    border: none;\n"
"    width: 10px; /* Width of the triangle */\n"
"    height: 10px; /* Height of the triangle */\n"
"    margin: -5px 0; /* Centers the triangle on the groove */\n"
"}")
        self.horizontalSliderStringFrequency.setMinimum(-50)
        self.horizontalSliderStringFrequency.setMaximum(50)
        self.horizontalSliderStringFrequency.setValue(0)
        self.horizontalSliderStringFrequency.setTracking(True)
        self.horizontalSliderStringFrequency.setOrientation(Qt.Horizontal)
        self.horizontalSliderStringFrequency.setInvertedAppearance(False)
        self.horizontalSliderStringFrequency.setInvertedControls(False)
        self.horizontalSliderStringFrequency.setTickPosition(QSlider.TicksBelow)
        self.labelAnalyzeFreq = QLabel(self.groupBox_2)
        self.labelAnalyzeFreq.setObjectName(u"labelAnalyzeFreq")
        self.labelAnalyzeFreq.setGeometry(QRect(160, 40, 61, 21))
        self.labelAnalyzeFreq.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_35 = QLabel(self.groupBox_2)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setGeometry(QRect(220, 40, 21, 21))
        self.label_35.setAlignment(Qt.AlignCenter)
        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(100, 41, 41, 20))
        self.label_15.setAlignment(Qt.AlignCenter)
        self.pushButtonPickupAnalyse = QPushButton(self.groupBox_2)
        self.pushButtonPickupAnalyse.setObjectName(u"pushButtonPickupAnalyse")
        self.pushButtonPickupAnalyse.setGeometry(QRect(260, 60, 91, 21))
        self.label_35.raise_()
        self.labelAnalyzeNote.raise_()
        self.labelAnalyzeCents.raise_()
        self.horizontalSliderStringFrequency.raise_()
        self.labelAnalyzeFreq.raise_()
        self.label_15.raise_()
        self.pushButtonPickupAnalyse.raise_()

        self.horizontalLayout.addWidget(self.groupBox_2, 0, Qt.AlignTop)

        self.groupBoxBasicTuningParameters = QGroupBox(self.tab_basic)
        self.groupBoxBasicTuningParameters.setObjectName(u"groupBoxBasicTuningParameters")
        self.groupBoxBasicTuningParameters.setMinimumSize(QSize(468, 150))
        self.groupBoxBasicTuningParameters.setMaximumSize(QSize(16777215, 150))
        self.comboBoxBaseNote = QComboBox(self.groupBoxBasicTuningParameters)
        self.comboBoxBaseNote.setObjectName(u"comboBoxBaseNote")
        self.comboBoxBaseNote.setGeometry(QRect(130, 100, 91, 20))
        self.label_7 = QLabel(self.groupBoxBasicTuningParameters)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 40, 101, 41))
        self.label_7.setWordWrap(True)
        self.label_8 = QLabel(self.groupBoxBasicTuningParameters)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 100, 91, 16))
        self.doubleSpinBoxFundamentalFrequency = QDoubleSpinBox(self.groupBoxBasicTuningParameters)
        self.doubleSpinBoxFundamentalFrequency.setObjectName(u"doubleSpinBoxFundamentalFrequency")
        self.doubleSpinBoxFundamentalFrequency.setGeometry(QRect(130, 50, 91, 21))
        self.doubleSpinBoxFundamentalFrequency.setAccelerated(True)
        self.doubleSpinBoxFundamentalFrequency.setDecimals(3)
        self.doubleSpinBoxFundamentalFrequency.setMaximum(1000.000000000000000)
        self.doubleSpinBoxFundamentalFrequency.setSingleStep(0.100000000000000)
        self.comboBoxFundamentalFrequency = QComboBox(self.groupBoxBasicTuningParameters)
        self.comboBoxFundamentalFrequency.addItem("")
        self.comboBoxFundamentalFrequency.setObjectName(u"comboBoxFundamentalFrequency")
        self.comboBoxFundamentalFrequency.setGeometry(QRect(230, 50, 121, 20))
        self.comboBoxFundamentalFrequency.setEditable(True)
        self.pushButtonDetectFundamental = QPushButton(self.groupBoxBasicTuningParameters)
        self.pushButtonDetectFundamental.setObjectName(u"pushButtonDetectFundamental")
        self.pushButtonDetectFundamental.setGeometry(QRect(370, 50, 91, 21))

        self.horizontalLayout.addWidget(self.groupBoxBasicTuningParameters, 0, Qt.AlignTop)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

        self.tabBasicVerticaLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.groupBox_15 = QGroupBox(self.tab_basic)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.groupBox_15.setMinimumSize(QSize(0, 100))
        self.groupBox_15.setMaximumSize(QSize(16777215, 100))
        self.groupBox_15.setStyleSheet(u"")
        self.horizontalLayout_53 = QHBoxLayout(self.groupBox_15)
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.horizontalLayout_53.setContentsMargins(0, 0, 0, 0)
        self.pushButtonCalibrateAll = QPushButton(self.groupBox_15)
        self.pushButtonCalibrateAll.setObjectName(u"pushButtonCalibrateAll")
        self.pushButtonCalibrateAll.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_53.addWidget(self.pushButtonCalibrateAll)

        self.line_10 = QFrame(self.groupBox_15)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setMinimumSize(QSize(0, 15))
        self.line_10.setMaximumSize(QSize(16777215, 15))
        self.line_10.setFrameShadow(QFrame.Plain)
        self.line_10.setFrameShape(QFrame.Shape.VLine)

        self.horizontalLayout_53.addWidget(self.line_10)

        self.pushButtonCalibratePressure = QPushButton(self.groupBox_15)
        self.pushButtonCalibratePressure.setObjectName(u"pushButtonCalibratePressure")
        self.pushButtonCalibratePressure.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_53.addWidget(self.pushButtonCalibratePressure)

        self.pushButtonCalibrateMute = QPushButton(self.groupBox_15)
        self.pushButtonCalibrateMute.setObjectName(u"pushButtonCalibrateMute")
        self.pushButtonCalibrateMute.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_53.addWidget(self.pushButtonCalibrateMute)

        self.pushButtonCalibrateHammer = QPushButton(self.groupBox_15)
        self.pushButtonCalibrateHammer.setObjectName(u"pushButtonCalibrateHammer")
        self.pushButtonCalibrateHammer.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_53.addWidget(self.pushButtonCalibrateHammer)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_53.addItem(self.horizontalSpacer_16)


        self.horizontalLayout_10.addWidget(self.groupBox_15)


        self.tabBasicVerticaLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.groupBox_3 = QGroupBox(self.tab_basic)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy1)
        self.groupBox_3.setMinimumSize(QSize(0, 200))
        self.groupBox_3.setMaximumSize(QSize(16777215, 200))
        self.horizontalLayout_11 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_16 = QLabel(self.groupBox_3)
        self.label_16.setObjectName(u"label_16")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.label_16)

        self.comboBoxHarmonicList = QComboBox(self.groupBox_3)
        self.comboBoxHarmonicList.setObjectName(u"comboBoxHarmonicList")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboBoxHarmonicList.sizePolicy().hasHeightForWidth())
        self.comboBoxHarmonicList.setSizePolicy(sizePolicy3)
        self.comboBoxHarmonicList.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_2.addWidget(self.comboBoxHarmonicList)

        self.line_20 = QFrame(self.groupBox_3)
        self.line_20.setObjectName(u"line_20")
        self.line_20.setFrameShadow(QFrame.Plain)
        self.line_20.setFrameShape(QFrame.Shape.VLine)

        self.horizontalLayout_2.addWidget(self.line_20)

        self.pushButtonAddHarmonicList = QPushButton(self.groupBox_3)
        self.pushButtonAddHarmonicList.setObjectName(u"pushButtonAddHarmonicList")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButtonAddHarmonicList.sizePolicy().hasHeightForWidth())
        self.pushButtonAddHarmonicList.setSizePolicy(sizePolicy4)
        self.pushButtonAddHarmonicList.setMinimumSize(QSize(75, 0))
        self.pushButtonAddHarmonicList.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_2.addWidget(self.pushButtonAddHarmonicList)

        self.pushButtonRemoveHarmonicList = QPushButton(self.groupBox_3)
        self.pushButtonRemoveHarmonicList.setObjectName(u"pushButtonRemoveHarmonicList")
        sizePolicy4.setHeightForWidth(self.pushButtonRemoveHarmonicList.sizePolicy().hasHeightForWidth())
        self.pushButtonRemoveHarmonicList.setSizePolicy(sizePolicy4)
        self.pushButtonRemoveHarmonicList.setMinimumSize(QSize(75, 0))

        self.horizontalLayout_2.addWidget(self.pushButtonRemoveHarmonicList)

        self.pushButtonRenameHarmonicList = QPushButton(self.groupBox_3)
        self.pushButtonRenameHarmonicList.setObjectName(u"pushButtonRenameHarmonicList")
        sizePolicy4.setHeightForWidth(self.pushButtonRenameHarmonicList.sizePolicy().hasHeightForWidth())
        self.pushButtonRenameHarmonicList.setSizePolicy(sizePolicy4)
        self.pushButtonRenameHarmonicList.setMinimumSize(QSize(75, 0))

        self.horizontalLayout_2.addWidget(self.pushButtonRenameHarmonicList)

        self.pushButtonAddHarmonicListFile = QPushButton(self.groupBox_3)
        self.pushButtonAddHarmonicListFile.setObjectName(u"pushButtonAddHarmonicListFile")
        sizePolicy4.setHeightForWidth(self.pushButtonAddHarmonicListFile.sizePolicy().hasHeightForWidth())
        self.pushButtonAddHarmonicListFile.setSizePolicy(sizePolicy4)
        self.pushButtonAddHarmonicListFile.setMinimumSize(QSize(75, 0))

        self.horizontalLayout_2.addWidget(self.pushButtonAddHarmonicListFile)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.layoutHarmonicTable = QVBoxLayout()
        self.layoutHarmonicTable.setSpacing(15)
        self.layoutHarmonicTable.setObjectName(u"layoutHarmonicTable")
        self.xtableViewScale = QTableView(self.groupBox_3)
        self.xtableViewScale.setObjectName(u"xtableViewScale")
        self.xtableViewScale.setStyleSheet(u"")
        self.xtableViewScale.horizontalHeader().setDefaultSectionSize(70)

        self.layoutHarmonicTable.addWidget(self.xtableViewScale)


        self.horizontalLayout_3.addLayout(self.layoutHarmonicTable)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButtonAddHarmonic = QPushButton(self.groupBox_3)
        self.pushButtonAddHarmonic.setObjectName(u"pushButtonAddHarmonic")
        sizePolicy4.setHeightForWidth(self.pushButtonAddHarmonic.sizePolicy().hasHeightForWidth())
        self.pushButtonAddHarmonic.setSizePolicy(sizePolicy4)
        self.pushButtonAddHarmonic.setMinimumSize(QSize(60, 0))
        self.pushButtonAddHarmonic.setMaximumSize(QSize(60, 16777215))

        self.verticalLayout_3.addWidget(self.pushButtonAddHarmonic)

        self.pushButtonRemoveHarmonic = QPushButton(self.groupBox_3)
        self.pushButtonRemoveHarmonic.setObjectName(u"pushButtonRemoveHarmonic")
        sizePolicy4.setHeightForWidth(self.pushButtonRemoveHarmonic.sizePolicy().hasHeightForWidth())
        self.pushButtonRemoveHarmonic.setSizePolicy(sizePolicy4)
        self.pushButtonRemoveHarmonic.setMinimumSize(QSize(60, 0))
        self.pushButtonRemoveHarmonic.setMaximumSize(QSize(60, 16777215))

        self.verticalLayout_3.addWidget(self.pushButtonRemoveHarmonic)

        self.verticalSpacer = QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(15)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_23 = QLabel(self.groupBox_3)
        self.label_23.setObjectName(u"label_23")
        sizePolicy2.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.label_23)

        self.comboBoxHarmonicPresets = QComboBox(self.groupBox_3)
        self.comboBoxHarmonicPresets.setObjectName(u"comboBoxHarmonicPresets")
        sizePolicy3.setHeightForWidth(self.comboBoxHarmonicPresets.sizePolicy().hasHeightForWidth())
        self.comboBoxHarmonicPresets.setSizePolicy(sizePolicy3)
        self.comboBoxHarmonicPresets.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_4.addWidget(self.comboBoxHarmonicPresets)

        self.pushButtonLoadHarmonicPreset = QPushButton(self.groupBox_3)
        self.pushButtonLoadHarmonicPreset.setObjectName(u"pushButtonLoadHarmonicPreset")
        sizePolicy4.setHeightForWidth(self.pushButtonLoadHarmonicPreset.sizePolicy().hasHeightForWidth())
        self.pushButtonLoadHarmonicPreset.setSizePolicy(sizePolicy4)
        self.pushButtonLoadHarmonicPreset.setMinimumSize(QSize(89, 0))

        self.horizontalLayout_4.addWidget(self.pushButtonLoadHarmonicPreset)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_11.addLayout(self.verticalLayout_2)


        self.horizontalLayout_6.addWidget(self.groupBox_3, 0, Qt.AlignBottom)


        self.tabBasicVerticaLayout.addLayout(self.horizontalLayout_6)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.tabBasicVerticaLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout_5.addLayout(self.tabBasicVerticaLayout)

        self.tabWidgetMain.addTab(self.tab_basic, "")
        self.tab_midiSettings = QWidget()
        self.tab_midiSettings.setObjectName(u"tab_midiSettings")
        self.verticalLayout_10 = QVBoxLayout(self.tab_midiSettings)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_29 = QLabel(self.tab_midiSettings)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMinimumSize(QSize(100, 0))
        self.label_29.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_7.addWidget(self.label_29)

        self.comboBoxConfiguration = QComboBox(self.tab_midiSettings)
        self.comboBoxConfiguration.setObjectName(u"comboBoxConfiguration")
        self.comboBoxConfiguration.setMinimumSize(QSize(200, 0))
        self.comboBoxConfiguration.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_7.addWidget(self.comboBoxConfiguration)

        self.pushButtonConfigurationAdd = QPushButton(self.tab_midiSettings)
        self.pushButtonConfigurationAdd.setObjectName(u"pushButtonConfigurationAdd")
        self.pushButtonConfigurationAdd.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_7.addWidget(self.pushButtonConfigurationAdd)

        self.pushButtonConfigurationRemove = QPushButton(self.tab_midiSettings)
        self.pushButtonConfigurationRemove.setObjectName(u"pushButtonConfigurationRemove")
        self.pushButtonConfigurationRemove.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_7.addWidget(self.pushButtonConfigurationRemove)

        self.pushButtonConfigurationName = QPushButton(self.tab_midiSettings)
        self.pushButtonConfigurationName.setObjectName(u"pushButtonConfigurationName")
        self.pushButtonConfigurationName.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_7.addWidget(self.pushButtonConfigurationName)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)


        self.verticalLayout_10.addLayout(self.horizontalLayout_7)

        self.line_11 = QFrame(self.tab_midiSettings)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShape(QFrame.Shape.HLine)
        self.line_11.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_10.addWidget(self.line_11)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_36 = QLabel(self.tab_midiSettings)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setMinimumSize(QSize(120, 0))
        self.label_36.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout_8.addWidget(self.label_36)

        self.comboBoxMidiChannel = QComboBox(self.tab_midiSettings)
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.addItem("")
        self.comboBoxMidiChannel.setObjectName(u"comboBoxMidiChannel")
        self.comboBoxMidiChannel.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_8.addWidget(self.comboBoxMidiChannel)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)

        self.pushButtonMidiRestoreDefaults = QPushButton(self.tab_midiSettings)
        self.pushButtonMidiRestoreDefaults.setObjectName(u"pushButtonMidiRestoreDefaults")
        self.pushButtonMidiRestoreDefaults.setMinimumSize(QSize(230, 0))
        self.pushButtonMidiRestoreDefaults.setMaximumSize(QSize(230, 16777215))

        self.horizontalLayout_8.addWidget(self.pushButtonMidiRestoreDefaults)


        self.verticalLayout_10.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox_5 = QGroupBox(self.tab_midiSettings)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMinimumSize(QSize(275, 140))
        self.label_44 = QLabel(self.groupBox_5)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setGeometry(QRect(0, 40, 151, 21))
        self.midiNoteOnVelToHammer = QSlider(self.groupBox_5)
        self.midiNoteOnVelToHammer.setObjectName(u"midiNoteOnVelToHammer")
        self.midiNoteOnVelToHammer.setGeometry(QRect(120, 43, 141, 21))
        self.midiNoteOnVelToHammer.setMaximum(512)
        self.midiNoteOnVelToHammer.setOrientation(Qt.Horizontal)
        self.midiNoteOnSendMuteRest = QCheckBox(self.groupBox_5)
        self.midiNoteOnSendMuteRest.setObjectName(u"midiNoteOnSendMuteRest")
        self.midiNoteOnSendMuteRest.setGeometry(QRect(0, 100, 251, 23))
        self.midiNoteOnHammerStaccato = QCheckBox(self.groupBox_5)
        self.midiNoteOnHammerStaccato.setObjectName(u"midiNoteOnHammerStaccato")
        self.midiNoteOnHammerStaccato.setGeometry(QRect(0, 70, 261, 21))

        self.gridLayout.addWidget(self.groupBox_5, 0, 0, 1, 1)

        self.groupBox_6 = QGroupBox(self.tab_midiSettings)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMinimumSize(QSize(275, 0))
        self.midiNoteOffSendFullMute = QCheckBox(self.groupBox_6)
        self.midiNoteOffSendFullMute.setObjectName(u"midiNoteOffSendFullMute")
        self.midiNoteOffSendFullMute.setGeometry(QRect(0, 40, 291, 23))
        self.midiNoteOffMotorOff = QCheckBox(self.groupBox_6)
        self.midiNoteOffMotorOff.setObjectName(u"midiNoteOffMotorOff")
        self.midiNoteOffMotorOff.setGeometry(QRect(0, 70, 291, 23))

        self.gridLayout.addWidget(self.groupBox_6, 0, 1, 1, 1)

        self.groupBox_10 = QGroupBox(self.tab_midiSettings)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setMinimumSize(QSize(275, 0))
        self.midiSustainSend = QComboBox(self.groupBox_10)
        self.midiSustainSend.addItem("")
        self.midiSustainSend.addItem("")
        self.midiSustainSend.addItem("")
        self.midiSustainSend.addItem("")
        self.midiSustainSend.setObjectName(u"midiSustainSend")
        self.midiSustainSend.setGeometry(QRect(70, 40, 191, 25))
        self.label_54 = QLabel(self.groupBox_10)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setGeometry(QRect(0, 40, 61, 21))
        self.midiSustainInvert = QCheckBox(self.groupBox_10)
        self.midiSustainInvert.setObjectName(u"midiSustainInvert")
        self.midiSustainInvert.setGeometry(QRect(0, 70, 92, 23))

        self.gridLayout.addWidget(self.groupBox_10, 1, 1, 1, 1)

        self.groupBox_8 = QGroupBox(self.tab_midiSettings)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setMinimumSize(QSize(275, 100))
        self.label_49 = QLabel(self.groupBox_8)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setGeometry(QRect(0, 70, 51, 21))
        self.midiPitchbendRatio = QSlider(self.groupBox_8)
        self.midiPitchbendRatio.setObjectName(u"midiPitchbendRatio")
        self.midiPitchbendRatio.setGeometry(QRect(59, 70, 201, 31))
        self.midiPitchbendRatio.setMaximum(512)
        self.midiPitchbendRatio.setOrientation(Qt.Horizontal)
        self.midiPitchbendSend = QComboBox(self.groupBox_8)
        self.midiPitchbendSend.addItem("")
        self.midiPitchbendSend.addItem("")
        self.midiPitchbendSend.addItem("")
        self.midiPitchbendSend.addItem("")
        self.midiPitchbendSend.addItem("")
        self.midiPitchbendSend.addItem("")
        self.midiPitchbendSend.setObjectName(u"midiPitchbendSend")
        self.midiPitchbendSend.setGeometry(QRect(70, 40, 191, 25))
        self.label_50 = QLabel(self.groupBox_8)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setGeometry(QRect(0, 40, 61, 21))

        self.gridLayout.addWidget(self.groupBox_8, 1, 0, 1, 1)

        self.groupBox_9 = QGroupBox(self.tab_midiSettings)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setMinimumSize(QSize(275, 0))
        self.label_51 = QLabel(self.groupBox_9)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setGeometry(QRect(1, 70, 51, 21))
        self.midiChannelATRatio = QSlider(self.groupBox_9)
        self.midiChannelATRatio.setObjectName(u"midiChannelATRatio")
        self.midiChannelATRatio.setGeometry(QRect(50, 74, 211, 21))
        self.midiChannelATRatio.setMaximum(512)
        self.midiChannelATRatio.setOrientation(Qt.Horizontal)
        self.midiChannelATSend = QComboBox(self.groupBox_9)
        self.midiChannelATSend.addItem("")
        self.midiChannelATSend.addItem("")
        self.midiChannelATSend.addItem("")
        self.midiChannelATSend.addItem("")
        self.midiChannelATSend.addItem("")
        self.midiChannelATSend.addItem("")
        self.midiChannelATSend.setObjectName(u"midiChannelATSend")
        self.midiChannelATSend.setGeometry(QRect(71, 40, 191, 25))
        self.label_52 = QLabel(self.groupBox_9)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setGeometry(QRect(1, 40, 61, 21))

        self.gridLayout.addWidget(self.groupBox_9, 2, 1, 1, 1)

        self.groupBox_7 = QGroupBox(self.tab_midiSettings)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setMinimumSize(QSize(275, 100))
        self.label_45 = QLabel(self.groupBox_7)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setGeometry(QRect(0, 70, 51, 21))
        self.midiPolyATRatio = QSlider(self.groupBox_7)
        self.midiPolyATRatio.setObjectName(u"midiPolyATRatio")
        self.midiPolyATRatio.setGeometry(QRect(59, 74, 201, 21))
        self.midiPolyATRatio.setMaximum(512)
        self.midiPolyATRatio.setOrientation(Qt.Horizontal)
        self.midiPolyATSend = QComboBox(self.groupBox_7)
        self.midiPolyATSend.addItem("")
        self.midiPolyATSend.addItem("")
        self.midiPolyATSend.addItem("")
        self.midiPolyATSend.addItem("")
        self.midiPolyATSend.addItem("")
        self.midiPolyATSend.addItem("")
        self.midiPolyATSend.setObjectName(u"midiPolyATSend")
        self.midiPolyATSend.setGeometry(QRect(70, 40, 191, 25))
        self.label_46 = QLabel(self.groupBox_7)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setGeometry(QRect(0, 40, 61, 21))

        self.gridLayout.addWidget(self.groupBox_7, 2, 0, 1, 1)


        self.horizontalLayout_9.addLayout(self.gridLayout)

        self.groupBox = QGroupBox(self.tab_midiSettings)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy5)
        self.verticalLayout_9 = QVBoxLayout(self.groupBox)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.listWidgetMidiEvents = QListWidget(self.groupBox)
        self.listWidgetMidiEvents.setObjectName(u"listWidgetMidiEvents")

        self.verticalLayout_4.addWidget(self.listWidgetMidiEvents)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.pushButtonCCAddLearn = QPushButton(self.groupBox)
        self.pushButtonCCAddLearn.setObjectName(u"pushButtonCCAddLearn")

        self.horizontalLayout_12.addWidget(self.pushButtonCCAddLearn)

        self.pushButtonCCAdd = QPushButton(self.groupBox)
        self.pushButtonCCAdd.setObjectName(u"pushButtonCCAdd")

        self.horizontalLayout_12.addWidget(self.pushButtonCCAdd)

        self.pushButtonCCRemove = QPushButton(self.groupBox)
        self.pushButtonCCRemove.setObjectName(u"pushButtonCCRemove")

        self.horizontalLayout_12.addWidget(self.pushButtonCCRemove)


        self.verticalLayout_4.addLayout(self.horizontalLayout_12)


        self.verticalLayout_7.addLayout(self.verticalLayout_4)


        self.horizontalLayout_13.addLayout(self.verticalLayout_7)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_6.addWidget(self.label_11)

        self.plainTextEditEventDescription = QPlainTextEdit(self.groupBox)
        self.plainTextEditEventDescription.setObjectName(u"plainTextEditEventDescription")
        self.plainTextEditEventDescription.setEnabled(False)

        self.verticalLayout_6.addWidget(self.plainTextEditEventDescription)


        self.horizontalLayout_13.addLayout(self.verticalLayout_6)


        self.verticalLayout_9.addLayout(self.horizontalLayout_13)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_28 = QLabel(self.groupBox)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(0, 20))
        self.label_28.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_8.addWidget(self.label_28)

        self.lineEditMidiEventCommand = QLineEdit(self.groupBox)
        self.lineEditMidiEventCommand.setObjectName(u"lineEditMidiEventCommand")
        self.lineEditMidiEventCommand.setMinimumSize(QSize(0, 30))
        self.lineEditMidiEventCommand.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_8.addWidget(self.lineEditMidiEventCommand)


        self.verticalLayout_9.addLayout(self.verticalLayout_8)


        self.horizontalLayout_9.addWidget(self.groupBox)


        self.verticalLayout_10.addLayout(self.horizontalLayout_9)

        self.tabWidgetMain.addTab(self.tab_midiSettings, "")
        self.tab_cvmapping = QWidget()
        self.tab_cvmapping.setObjectName(u"tab_cvmapping")
        self.tab_cvmapping.setEnabled(True)
        self.verticalLayout_28 = QVBoxLayout(self.tab_cvmapping)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBoxCV1 = QGroupBox(self.tab_cvmapping)
        self.groupBoxCV1.setObjectName(u"groupBoxCV1")
        sizePolicy.setHeightForWidth(self.groupBoxCV1.sizePolicy().hasHeightForWidth())
        self.groupBoxCV1.setSizePolicy(sizePolicy)
        self.groupBoxCV1.setMinimumSize(QSize(500, 150))
        self.horizontalLayout_20 = QHBoxLayout(self.groupBoxCV1)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.labelCV1_2 = QLabel(self.groupBoxCV1)
        self.labelCV1_2.setObjectName(u"labelCV1_2")
        sizePolicy4.setHeightForWidth(self.labelCV1_2.sizePolicy().hasHeightForWidth())
        self.labelCV1_2.setSizePolicy(sizePolicy4)
        self.labelCV1_2.setMinimumSize(QSize(66, 15))
        self.labelCV1_2.setMaximumSize(QSize(66, 15))
        self.labelCV1_2.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_19.addWidget(self.labelCV1_2)

        self.dialCVHarmonic = QDial(self.groupBoxCV1)
        self.dialCVHarmonic.setObjectName(u"dialCVHarmonic")
        self.dialCVHarmonic.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.dialCVHarmonic.sizePolicy().hasHeightForWidth())
        self.dialCVHarmonic.setSizePolicy(sizePolicy4)
        self.dialCVHarmonic.setMinimumSize(QSize(66, 61))
        self.dialCVHarmonic.setMaximumSize(QSize(66, 61))
        self.dialCVHarmonic.setMaximum(65535)
        self.dialCVHarmonic.setSingleStep(100)
        self.dialCVHarmonic.setPageStep(1000)
        self.dialCVHarmonic.setNotchesVisible(True)

        self.verticalLayout_19.addWidget(self.dialCVHarmonic)

        self.labelCVHarmonic = QLabel(self.groupBoxCV1)
        self.labelCVHarmonic.setObjectName(u"labelCVHarmonic")
        sizePolicy2.setHeightForWidth(self.labelCVHarmonic.sizePolicy().hasHeightForWidth())
        self.labelCVHarmonic.setSizePolicy(sizePolicy2)
        self.labelCVHarmonic.setMinimumSize(QSize(66, 0))
        self.labelCVHarmonic.setMaximumSize(QSize(66, 16777215))
        self.labelCVHarmonic.setStyleSheet(u"QLabel {\n"
"	font-size: 10px;\n"
"}")
        self.labelCVHarmonic.setAlignment(Qt.AlignCenter)

        self.verticalLayout_19.addWidget(self.labelCVHarmonic)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_19.addItem(self.verticalSpacer_7)


        self.horizontalLayout_20.addLayout(self.verticalLayout_19)

        self.line_12 = QFrame(self.groupBoxCV1)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setFrameShape(QFrame.Shape.VLine)
        self.line_12.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_20.addWidget(self.line_12)

        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setSpacing(6)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.labelCV1_4 = QLabel(self.groupBoxCV1)
        self.labelCV1_4.setObjectName(u"labelCV1_4")
        sizePolicy4.setHeightForWidth(self.labelCV1_4.sizePolicy().hasHeightForWidth())
        self.labelCV1_4.setSizePolicy(sizePolicy4)
        self.labelCV1_4.setMinimumSize(QSize(60, 20))
        self.labelCV1_4.setMaximumSize(QSize(60, 20))
        self.labelCV1_4.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_19.addWidget(self.labelCV1_4)

        self.dialCVHarmonicScale = QDoubleSpinBox(self.groupBoxCV1)
        self.dialCVHarmonicScale.setObjectName(u"dialCVHarmonicScale")
        sizePolicy3.setHeightForWidth(self.dialCVHarmonicScale.sizePolicy().hasHeightForWidth())
        self.dialCVHarmonicScale.setSizePolicy(sizePolicy3)
        self.dialCVHarmonicScale.setMinimumSize(QSize(0, 20))
        self.dialCVHarmonicScale.setMaximumSize(QSize(16777215, 20))
        self.dialCVHarmonicScale.setDecimals(3)
        self.dialCVHarmonicScale.setMinimum(0.500000000000000)
        self.dialCVHarmonicScale.setMaximum(2.000000000000000)
        self.dialCVHarmonicScale.setSingleStep(0.010000000000000)

        self.horizontalLayout_19.addWidget(self.dialCVHarmonicScale)

        self.horizontalSpacer_18 = QSpacerItem(10, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_18)

        self.labelCV1_5 = QLabel(self.groupBoxCV1)
        self.labelCV1_5.setObjectName(u"labelCV1_5")
        sizePolicy4.setHeightForWidth(self.labelCV1_5.sizePolicy().hasHeightForWidth())
        self.labelCV1_5.setSizePolicy(sizePolicy4)
        self.labelCV1_5.setMinimumSize(QSize(70, 20))
        self.labelCV1_5.setMaximumSize(QSize(70, 20))
        self.labelCV1_5.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_19.addWidget(self.labelCV1_5)

        self.widgetCVHarmonicNoteOffset = QDoubleSpinBox(self.groupBoxCV1)
        self.widgetCVHarmonicNoteOffset.setObjectName(u"widgetCVHarmonicNoteOffset")
        self.widgetCVHarmonicNoteOffset.setMinimumSize(QSize(0, 20))
        self.widgetCVHarmonicNoteOffset.setMaximumSize(QSize(16777215, 20))
        self.widgetCVHarmonicNoteOffset.setDecimals(0)
        self.widgetCVHarmonicNoteOffset.setMinimum(-664.000000000000000)
        self.widgetCVHarmonicNoteOffset.setMaximum(664.000000000000000)

        self.horizontalLayout_19.addWidget(self.widgetCVHarmonicNoteOffset)

        self.horizontalSpacer_26 = QSpacerItem(10, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_26)

        self.labelCV1_7 = QLabel(self.groupBoxCV1)
        self.labelCV1_7.setObjectName(u"labelCV1_7")
        sizePolicy4.setHeightForWidth(self.labelCV1_7.sizePolicy().hasHeightForWidth())
        self.labelCV1_7.setSizePolicy(sizePolicy4)
        self.labelCV1_7.setMinimumSize(QSize(70, 20))
        self.labelCV1_7.setMaximumSize(QSize(70, 20))
        self.labelCV1_7.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_19.addWidget(self.labelCV1_7)

        self.widgetCVHarmonicZero = QDoubleSpinBox(self.groupBoxCV1)
        self.widgetCVHarmonicZero.setObjectName(u"widgetCVHarmonicZero")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.widgetCVHarmonicZero.sizePolicy().hasHeightForWidth())
        self.widgetCVHarmonicZero.setSizePolicy(sizePolicy6)
        self.widgetCVHarmonicZero.setMinimumSize(QSize(0, 20))
        self.widgetCVHarmonicZero.setMaximumSize(QSize(16777215, 20))
        self.widgetCVHarmonicZero.setDecimals(0)
        self.widgetCVHarmonicZero.setMinimum(-1327.000000000000000)
        self.widgetCVHarmonicZero.setMaximum(1327.000000000000000)
        self.widgetCVHarmonicZero.setValue(-50.000000000000000)

        self.horizontalLayout_19.addWidget(self.widgetCVHarmonicZero)


        self.verticalLayout_18.addLayout(self.horizontalLayout_19)

        self.label_53 = QLabel(self.groupBoxCV1)
        self.label_53.setObjectName(u"label_53")
        sizePolicy6.setHeightForWidth(self.label_53.sizePolicy().hasHeightForWidth())
        self.label_53.setSizePolicy(sizePolicy6)
        self.label_53.setMinimumSize(QSize(0, 15))
        self.label_53.setMaximumSize(QSize(16777215, 15))
        self.label_53.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")

        self.verticalLayout_18.addWidget(self.label_53)

        self.plainTextEditCVHarmonicCommands = QPlainTextSub(self.groupBoxCV1)
        self.plainTextEditCVHarmonicCommands.setObjectName(u"plainTextEditCVHarmonicCommands")

        self.verticalLayout_18.addWidget(self.plainTextEditCVHarmonicCommands)


        self.horizontalLayout_20.addLayout(self.verticalLayout_18)


        self.gridLayout_2.addWidget(self.groupBoxCV1, 0, 0, 1, 1)

        self.groupBoxCV1_2 = QGroupBox(self.tab_cvmapping)
        self.groupBoxCV1_2.setObjectName(u"groupBoxCV1_2")
        sizePolicy.setHeightForWidth(self.groupBoxCV1_2.sizePolicy().hasHeightForWidth())
        self.groupBoxCV1_2.setSizePolicy(sizePolicy)
        self.groupBoxCV1_2.setMinimumSize(QSize(500, 150))
        self.horizontalLayout_25 = QHBoxLayout(self.groupBoxCV1_2)
        self.horizontalLayout_25.setSpacing(6)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.labelCV1_8 = QLabel(self.groupBoxCV1_2)
        self.labelCV1_8.setObjectName(u"labelCV1_8")
        sizePolicy4.setHeightForWidth(self.labelCV1_8.sizePolicy().hasHeightForWidth())
        self.labelCV1_8.setSizePolicy(sizePolicy4)
        self.labelCV1_8.setMinimumSize(QSize(66, 15))
        self.labelCV1_8.setMaximumSize(QSize(66, 15))
        self.labelCV1_8.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_8.setAlignment(Qt.AlignCenter)

        self.verticalLayout_27.addWidget(self.labelCV1_8)

        self.dialCVHarmonicShift = QDial(self.groupBoxCV1_2)
        self.dialCVHarmonicShift.setObjectName(u"dialCVHarmonicShift")
        self.dialCVHarmonicShift.setEnabled(False)
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.dialCVHarmonicShift.sizePolicy().hasHeightForWidth())
        self.dialCVHarmonicShift.setSizePolicy(sizePolicy7)
        self.dialCVHarmonicShift.setMinimumSize(QSize(66, 61))
        self.dialCVHarmonicShift.setMaximumSize(QSize(66, 61))
        self.dialCVHarmonicShift.setMaximum(65535)
        self.dialCVHarmonicShift.setSingleStep(100)
        self.dialCVHarmonicShift.setPageStep(1000)
        self.dialCVHarmonicShift.setNotchesVisible(True)

        self.verticalLayout_27.addWidget(self.dialCVHarmonicShift)

        self.labelCVHarmonicShift = QLabel(self.groupBoxCV1_2)
        self.labelCVHarmonicShift.setObjectName(u"labelCVHarmonicShift")
        self.labelCVHarmonicShift.setStyleSheet(u"QLabel {\n"
"	font-size: 10px;\n"
"}")
        self.labelCVHarmonicShift.setAlignment(Qt.AlignCenter)

        self.verticalLayout_27.addWidget(self.labelCVHarmonicShift)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_27.addItem(self.verticalSpacer_11)


        self.horizontalLayout_25.addLayout(self.verticalLayout_27)

        self.line_13 = QFrame(self.groupBoxCV1_2)
        self.line_13.setObjectName(u"line_13")
        self.line_13.setFrameShape(QFrame.Shape.VLine)
        self.line_13.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_25.addWidget(self.line_13)

        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.labelCV1_10 = QLabel(self.groupBoxCV1_2)
        self.labelCV1_10.setObjectName(u"labelCV1_10")
        self.labelCV1_10.setMaximumSize(QSize(60, 16777215))
        self.labelCV1_10.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_10.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_24.addWidget(self.labelCV1_10)

        self.dialCVHarmonicShiftScale = QDoubleSpinBox(self.groupBoxCV1_2)
        self.dialCVHarmonicShiftScale.setObjectName(u"dialCVHarmonicShiftScale")
        self.dialCVHarmonicShiftScale.setDecimals(3)
        self.dialCVHarmonicShiftScale.setMinimum(0.500000000000000)
        self.dialCVHarmonicShiftScale.setMaximum(2.000000000000000)
        self.dialCVHarmonicShiftScale.setSingleStep(0.010000000000000)

        self.horizontalLayout_24.addWidget(self.dialCVHarmonicShiftScale)

        self.horizontalSpacer_29 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_29)

        self.labelCV1_11 = QLabel(self.groupBoxCV1_2)
        self.labelCV1_11.setObjectName(u"labelCV1_11")
        self.labelCV1_11.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_11.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_24.addWidget(self.labelCV1_11)

        self.dialCVHarmonicShiftZero = QDoubleSpinBox(self.groupBoxCV1_2)
        self.dialCVHarmonicShiftZero.setObjectName(u"dialCVHarmonicShiftZero")
        self.dialCVHarmonicShiftZero.setDecimals(0)
        self.dialCVHarmonicShiftZero.setMinimum(-1327.000000000000000)
        self.dialCVHarmonicShiftZero.setMaximum(1327.000000000000000)

        self.horizontalLayout_24.addWidget(self.dialCVHarmonicShiftZero)

        self.pushButtonCVHarmonicShiftZeroCalibrate = QPushButton(self.groupBoxCV1_2)
        self.pushButtonCVHarmonicShiftZeroCalibrate.setObjectName(u"pushButtonCVHarmonicShiftZeroCalibrate")

        self.horizontalLayout_24.addWidget(self.pushButtonCVHarmonicShiftZeroCalibrate)


        self.verticalLayout_26.addLayout(self.horizontalLayout_24)

        self.label_55 = QLabel(self.groupBoxCV1_2)
        self.label_55.setObjectName(u"label_55")
        sizePolicy6.setHeightForWidth(self.label_55.sizePolicy().hasHeightForWidth())
        self.label_55.setSizePolicy(sizePolicy6)
        self.label_55.setMinimumSize(QSize(0, 15))
        self.label_55.setMaximumSize(QSize(16777215, 15))
        self.label_55.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")

        self.verticalLayout_26.addWidget(self.label_55)

        self.plainTextEditCVHarmonicShiftCommands = QPlainTextSub(self.groupBoxCV1_2)
        self.plainTextEditCVHarmonicShiftCommands.setObjectName(u"plainTextEditCVHarmonicShiftCommands")

        self.verticalLayout_26.addWidget(self.plainTextEditCVHarmonicShiftCommands)


        self.horizontalLayout_25.addLayout(self.verticalLayout_26)


        self.gridLayout_2.addWidget(self.groupBoxCV1_2, 0, 1, 1, 1)

        self.groupBoxCV1_7 = QGroupBox(self.tab_cvmapping)
        self.groupBoxCV1_7.setObjectName(u"groupBoxCV1_7")
        sizePolicy.setHeightForWidth(self.groupBoxCV1_7.sizePolicy().hasHeightForWidth())
        self.groupBoxCV1_7.setSizePolicy(sizePolicy)
        self.groupBoxCV1_7.setMinimumSize(QSize(500, 150))
        self.horizontalLayout_18 = QHBoxLayout(self.groupBoxCV1_7)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.labelCV1_15 = QLabel(self.groupBoxCV1_7)
        self.labelCV1_15.setObjectName(u"labelCV1_15")
        sizePolicy4.setHeightForWidth(self.labelCV1_15.sizePolicy().hasHeightForWidth())
        self.labelCV1_15.setSizePolicy(sizePolicy4)
        self.labelCV1_15.setMinimumSize(QSize(66, 15))
        self.labelCV1_15.setMaximumSize(QSize(66, 15))
        self.labelCV1_15.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_15.setAlignment(Qt.AlignCenter)

        self.verticalLayout_17.addWidget(self.labelCV1_15)

        self.dialCVFineTune = QDial(self.groupBoxCV1_7)
        self.dialCVFineTune.setObjectName(u"dialCVFineTune")
        self.dialCVFineTune.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.dialCVFineTune.sizePolicy().hasHeightForWidth())
        self.dialCVFineTune.setSizePolicy(sizePolicy4)
        self.dialCVFineTune.setMinimumSize(QSize(66, 61))
        self.dialCVFineTune.setMaximumSize(QSize(66, 61))
        self.dialCVFineTune.setMaximum(65535)
        self.dialCVFineTune.setSingleStep(100)
        self.dialCVFineTune.setPageStep(1000)
        self.dialCVFineTune.setInvertedAppearance(False)
        self.dialCVFineTune.setInvertedControls(False)
        self.dialCVFineTune.setNotchesVisible(True)

        self.verticalLayout_17.addWidget(self.dialCVFineTune)

        self.labelCVFineTune = QLabel(self.groupBoxCV1_7)
        self.labelCVFineTune.setObjectName(u"labelCVFineTune")
        sizePolicy2.setHeightForWidth(self.labelCVFineTune.sizePolicy().hasHeightForWidth())
        self.labelCVFineTune.setSizePolicy(sizePolicy2)
        self.labelCVFineTune.setMinimumSize(QSize(66, 0))
        self.labelCVFineTune.setMaximumSize(QSize(66, 16777215))
        self.labelCVFineTune.setStyleSheet(u"QLabel {\n"
"	font-size: 10px;\n"
"}")
        self.labelCVFineTune.setAlignment(Qt.AlignCenter)

        self.verticalLayout_17.addWidget(self.labelCVFineTune)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer_6)


        self.horizontalLayout_18.addLayout(self.verticalLayout_17)

        self.line_18 = QFrame(self.groupBoxCV1_7)
        self.line_18.setObjectName(u"line_18")
        self.line_18.setFrameShape(QFrame.Shape.VLine)
        self.line_18.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_18.addWidget(self.line_18)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.labelCV1_13 = QLabel(self.groupBoxCV1_7)
        self.labelCV1_13.setObjectName(u"labelCV1_13")
        self.labelCV1_13.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_13.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_17.addWidget(self.labelCV1_13)

        self.dialCVFineTuneCenter = QDoubleSpinBox(self.groupBoxCV1_7)
        self.dialCVFineTuneCenter.setObjectName(u"dialCVFineTuneCenter")
        self.dialCVFineTuneCenter.setDecimals(0)
        self.dialCVFineTuneCenter.setMinimum(-5000.000000000000000)
        self.dialCVFineTuneCenter.setMaximum(5000.000000000000000)

        self.horizontalLayout_17.addWidget(self.dialCVFineTuneCenter)

        self.pushButtonCVFinetuneCalibrate = QPushButton(self.groupBoxCV1_7)
        self.pushButtonCVFinetuneCalibrate.setObjectName(u"pushButtonCVFinetuneCalibrate")

        self.horizontalLayout_17.addWidget(self.pushButtonCVFinetuneCalibrate)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_7)


        self.verticalLayout_16.addLayout(self.horizontalLayout_17)

        self.label_60 = QLabel(self.groupBoxCV1_7)
        self.label_60.setObjectName(u"label_60")
        sizePolicy6.setHeightForWidth(self.label_60.sizePolicy().hasHeightForWidth())
        self.label_60.setSizePolicy(sizePolicy6)
        self.label_60.setMinimumSize(QSize(0, 15))
        self.label_60.setMaximumSize(QSize(16777215, 15))
        self.label_60.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")

        self.verticalLayout_16.addWidget(self.label_60)

        self.plainTextEditCVFineTuneCommands = QPlainTextSub(self.groupBoxCV1_7)
        self.plainTextEditCVFineTuneCommands.setObjectName(u"plainTextEditCVFineTuneCommands")

        self.verticalLayout_16.addWidget(self.plainTextEditCVFineTuneCommands)


        self.horizontalLayout_18.addLayout(self.verticalLayout_16)


        self.gridLayout_2.addWidget(self.groupBoxCV1_7, 1, 0, 1, 1)

        self.groupBoxCV1_4 = QGroupBox(self.tab_cvmapping)
        self.groupBoxCV1_4.setObjectName(u"groupBoxCV1_4")
        sizePolicy.setHeightForWidth(self.groupBoxCV1_4.sizePolicy().hasHeightForWidth())
        self.groupBoxCV1_4.setSizePolicy(sizePolicy)
        self.groupBoxCV1_4.setMinimumSize(QSize(500, 150))
        self.horizontalLayout_23 = QHBoxLayout(self.groupBoxCV1_4)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_25 = QVBoxLayout()
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.labelCV1_20 = QLabel(self.groupBoxCV1_4)
        self.labelCV1_20.setObjectName(u"labelCV1_20")
        sizePolicy4.setHeightForWidth(self.labelCV1_20.sizePolicy().hasHeightForWidth())
        self.labelCV1_20.setSizePolicy(sizePolicy4)
        self.labelCV1_20.setMinimumSize(QSize(66, 15))
        self.labelCV1_20.setMaximumSize(QSize(66, 15))
        self.labelCV1_20.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_20.setAlignment(Qt.AlignCenter)

        self.verticalLayout_25.addWidget(self.labelCV1_20)

        self.dialCVPressure = QDial(self.groupBoxCV1_4)
        self.dialCVPressure.setObjectName(u"dialCVPressure")
        self.dialCVPressure.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.dialCVPressure.sizePolicy().hasHeightForWidth())
        self.dialCVPressure.setSizePolicy(sizePolicy4)
        self.dialCVPressure.setMinimumSize(QSize(66, 61))
        self.dialCVPressure.setMaximumSize(QSize(66, 61))
        self.dialCVPressure.setMaximum(65535)
        self.dialCVPressure.setSingleStep(100)
        self.dialCVPressure.setPageStep(1000)
        self.dialCVPressure.setNotchesVisible(True)

        self.verticalLayout_25.addWidget(self.dialCVPressure)

        self.labelCVPressure = QLabel(self.groupBoxCV1_4)
        self.labelCVPressure.setObjectName(u"labelCVPressure")
        self.labelCVPressure.setStyleSheet(u"QLabel {\n"
"	font-size: 10px;\n"
"}")
        self.labelCVPressure.setAlignment(Qt.AlignCenter)

        self.verticalLayout_25.addWidget(self.labelCVPressure)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_25.addItem(self.verticalSpacer_10)


        self.horizontalLayout_23.addLayout(self.verticalLayout_25)

        self.line_15 = QFrame(self.groupBoxCV1_4)
        self.line_15.setObjectName(u"line_15")
        self.line_15.setFrameShape(QFrame.Shape.VLine)
        self.line_15.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_23.addWidget(self.line_15)

        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.label_57 = QLabel(self.groupBoxCV1_4)
        self.label_57.setObjectName(u"label_57")
        sizePolicy6.setHeightForWidth(self.label_57.sizePolicy().hasHeightForWidth())
        self.label_57.setSizePolicy(sizePolicy6)
        self.label_57.setMinimumSize(QSize(0, 15))
        self.label_57.setMaximumSize(QSize(16777215, 15))
        self.label_57.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")

        self.verticalLayout_24.addWidget(self.label_57)

        self.plainTextEditCVPressureCommands = QPlainTextSub(self.groupBoxCV1_4)
        self.plainTextEditCVPressureCommands.setObjectName(u"plainTextEditCVPressureCommands")

        self.verticalLayout_24.addWidget(self.plainTextEditCVPressureCommands)


        self.horizontalLayout_23.addLayout(self.verticalLayout_24)


        self.gridLayout_2.addWidget(self.groupBoxCV1_4, 1, 1, 1, 1)

        self.groupBoxCV1_3 = QGroupBox(self.tab_cvmapping)
        self.groupBoxCV1_3.setObjectName(u"groupBoxCV1_3")
        sizePolicy.setHeightForWidth(self.groupBoxCV1_3.sizePolicy().hasHeightForWidth())
        self.groupBoxCV1_3.setSizePolicy(sizePolicy)
        self.groupBoxCV1_3.setMinimumSize(QSize(500, 150))
        self.horizontalLayout_16 = QHBoxLayout(self.groupBoxCV1_3)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.labelCV1_14 = QLabel(self.groupBoxCV1_3)
        self.labelCV1_14.setObjectName(u"labelCV1_14")
        sizePolicy4.setHeightForWidth(self.labelCV1_14.sizePolicy().hasHeightForWidth())
        self.labelCV1_14.setSizePolicy(sizePolicy4)
        self.labelCV1_14.setMinimumSize(QSize(66, 15))
        self.labelCV1_14.setMaximumSize(QSize(66, 15))
        self.labelCV1_14.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_14.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.labelCV1_14)

        self.dialCVMute = QDial(self.groupBoxCV1_3)
        self.dialCVMute.setObjectName(u"dialCVMute")
        self.dialCVMute.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.dialCVMute.sizePolicy().hasHeightForWidth())
        self.dialCVMute.setSizePolicy(sizePolicy4)
        self.dialCVMute.setMinimumSize(QSize(66, 60))
        self.dialCVMute.setMaximumSize(QSize(66, 60))
        self.dialCVMute.setMaximum(65535)
        self.dialCVMute.setSingleStep(100)
        self.dialCVMute.setPageStep(1000)
        self.dialCVMute.setNotchesVisible(True)

        self.verticalLayout_14.addWidget(self.dialCVMute)

        self.labelCVMute = QLabel(self.groupBoxCV1_3)
        self.labelCVMute.setObjectName(u"labelCVMute")
        sizePolicy6.setHeightForWidth(self.labelCVMute.sizePolicy().hasHeightForWidth())
        self.labelCVMute.setSizePolicy(sizePolicy6)
        self.labelCVMute.setStyleSheet(u"QLabel {\n"
"	font-size: 10px;\n"
"}")
        self.labelCVMute.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.labelCVMute)

        self.verticalSpacer_5 = QSpacerItem(20, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_5)


        self.horizontalLayout_16.addLayout(self.verticalLayout_14)

        self.line_14 = QFrame(self.groupBoxCV1_3)
        self.line_14.setObjectName(u"line_14")
        self.line_14.setFrameShape(QFrame.Shape.VLine)
        self.line_14.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_16.addWidget(self.line_14)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.label_56 = QLabel(self.groupBoxCV1_3)
        self.label_56.setObjectName(u"label_56")
        sizePolicy6.setHeightForWidth(self.label_56.sizePolicy().hasHeightForWidth())
        self.label_56.setSizePolicy(sizePolicy6)
        self.label_56.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")

        self.verticalLayout_15.addWidget(self.label_56)

        self.plainTextEditCVMuteCommands = QPlainTextSub(self.groupBoxCV1_3)
        self.plainTextEditCVMuteCommands.setObjectName(u"plainTextEditCVMuteCommands")

        self.verticalLayout_15.addWidget(self.plainTextEditCVMuteCommands)


        self.horizontalLayout_16.addLayout(self.verticalLayout_15)


        self.gridLayout_2.addWidget(self.groupBoxCV1_3, 2, 0, 1, 1)

        self.groupBoxCV1_8 = QGroupBox(self.tab_cvmapping)
        self.groupBoxCV1_8.setObjectName(u"groupBoxCV1_8")
        sizePolicy.setHeightForWidth(self.groupBoxCV1_8.sizePolicy().hasHeightForWidth())
        self.groupBoxCV1_8.setSizePolicy(sizePolicy)
        self.groupBoxCV1_8.setMinimumSize(QSize(500, 150))
        self.horizontalLayout_22 = QHBoxLayout(self.groupBoxCV1_8)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_23 = QVBoxLayout()
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.labelCV1_16 = QLabel(self.groupBoxCV1_8)
        self.labelCV1_16.setObjectName(u"labelCV1_16")
        sizePolicy4.setHeightForWidth(self.labelCV1_16.sizePolicy().hasHeightForWidth())
        self.labelCV1_16.setSizePolicy(sizePolicy4)
        self.labelCV1_16.setMinimumSize(QSize(66, 15))
        self.labelCV1_16.setMaximumSize(QSize(66, 15))
        self.labelCV1_16.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_16.setAlignment(Qt.AlignCenter)

        self.verticalLayout_23.addWidget(self.labelCV1_16)

        self.dialCVHammerScale = QDial(self.groupBoxCV1_8)
        self.dialCVHammerScale.setObjectName(u"dialCVHammerScale")
        self.dialCVHammerScale.setEnabled(False)
        sizePolicy7.setHeightForWidth(self.dialCVHammerScale.sizePolicy().hasHeightForWidth())
        self.dialCVHammerScale.setSizePolicy(sizePolicy7)
        self.dialCVHammerScale.setMinimumSize(QSize(66, 61))
        self.dialCVHammerScale.setMaximumSize(QSize(66, 61))
        self.dialCVHammerScale.setMaximum(65535)
        self.dialCVHammerScale.setSingleStep(100)
        self.dialCVHammerScale.setPageStep(1000)
        self.dialCVHammerScale.setNotchesVisible(True)

        self.verticalLayout_23.addWidget(self.dialCVHammerScale)

        self.labelCVHammerScale = QLabel(self.groupBoxCV1_8)
        self.labelCVHammerScale.setObjectName(u"labelCVHammerScale")
        self.labelCVHammerScale.setStyleSheet(u"QLabel {\n"
"	font-size: 10px;\n"
"}")
        self.labelCVHammerScale.setAlignment(Qt.AlignCenter)

        self.verticalLayout_23.addWidget(self.labelCVHammerScale)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_23.addItem(self.verticalSpacer_9)


        self.horizontalLayout_22.addLayout(self.verticalLayout_23)

        self.line_19 = QFrame(self.groupBoxCV1_8)
        self.line_19.setObjectName(u"line_19")
        self.line_19.setFrameShape(QFrame.Shape.VLine)
        self.line_19.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_22.addWidget(self.line_19)

        self.verticalLayout_22 = QVBoxLayout()
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.label_61 = QLabel(self.groupBoxCV1_8)
        self.label_61.setObjectName(u"label_61")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.label_61.sizePolicy().hasHeightForWidth())
        self.label_61.setSizePolicy(sizePolicy8)
        self.label_61.setMinimumSize(QSize(0, 15))
        self.label_61.setMaximumSize(QSize(16777215, 15))
        self.label_61.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")

        self.verticalLayout_22.addWidget(self.label_61)

        self.plainTextEditCVHammerScaleCommands = QPlainTextSub(self.groupBoxCV1_8)
        self.plainTextEditCVHammerScaleCommands.setObjectName(u"plainTextEditCVHammerScaleCommands")

        self.verticalLayout_22.addWidget(self.plainTextEditCVHammerScaleCommands)


        self.horizontalLayout_22.addLayout(self.verticalLayout_22)


        self.gridLayout_2.addWidget(self.groupBoxCV1_8, 2, 1, 1, 1)

        self.groupBoxCV1_6 = QGroupBox(self.tab_cvmapping)
        self.groupBoxCV1_6.setObjectName(u"groupBoxCV1_6")
        sizePolicy.setHeightForWidth(self.groupBoxCV1_6.sizePolicy().hasHeightForWidth())
        self.groupBoxCV1_6.setSizePolicy(sizePolicy)
        self.groupBoxCV1_6.setMinimumSize(QSize(500, 150))
        self.horizontalLayout_15 = QHBoxLayout(self.groupBoxCV1_6)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.labelCV1_32 = QLabel(self.groupBoxCV1_6)
        self.labelCV1_32.setObjectName(u"labelCV1_32")
        sizePolicy4.setHeightForWidth(self.labelCV1_32.sizePolicy().hasHeightForWidth())
        self.labelCV1_32.setSizePolicy(sizePolicy4)
        self.labelCV1_32.setMinimumSize(QSize(66, 15))
        self.labelCV1_32.setMaximumSize(QSize(66, 15))
        self.labelCV1_32.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_32.setAlignment(Qt.AlignCenter)

        self.verticalLayout_13.addWidget(self.labelCV1_32)

        self.dialCVGate = QDial(self.groupBoxCV1_6)
        self.dialCVGate.setObjectName(u"dialCVGate")
        self.dialCVGate.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.dialCVGate.sizePolicy().hasHeightForWidth())
        self.dialCVGate.setSizePolicy(sizePolicy4)
        self.dialCVGate.setMinimumSize(QSize(66, 60))
        self.dialCVGate.setMaximumSize(QSize(66, 60))
        self.dialCVGate.setMaximum(65535)
        self.dialCVGate.setSingleStep(100)
        self.dialCVGate.setPageStep(1000)
        self.dialCVGate.setNotchesVisible(True)

        self.verticalLayout_13.addWidget(self.dialCVGate)

        self.labelCVGate = QLabel(self.groupBoxCV1_6)
        self.labelCVGate.setObjectName(u"labelCVGate")
        sizePolicy6.setHeightForWidth(self.labelCVGate.sizePolicy().hasHeightForWidth())
        self.labelCVGate.setSizePolicy(sizePolicy6)
        self.labelCVGate.setMinimumSize(QSize(0, 15))
        self.labelCVGate.setMaximumSize(QSize(16777215, 15))
        self.labelCVGate.setStyleSheet(u"QLabel {\n"
"	font-size: 10px;\n"
"}")
        self.labelCVGate.setAlignment(Qt.AlignCenter)
        self.labelCVGate.setMargin(0)

        self.verticalLayout_13.addWidget(self.labelCVGate)

        self.verticalSpacer_4 = QSpacerItem(20, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_4)


        self.horizontalLayout_15.addLayout(self.verticalLayout_13)

        self.line_17 = QFrame(self.groupBoxCV1_6)
        self.line_17.setObjectName(u"line_17")
        self.line_17.setFrameShape(QFrame.Shape.VLine)
        self.line_17.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_15.addWidget(self.line_17)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_111 = QLabel(self.groupBoxCV1_6)
        self.label_111.setObjectName(u"label_111")
        self.label_111.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")

        self.horizontalLayout_14.addWidget(self.label_111, 0, Qt.AlignTop)

        self.widgetCVGateThreshold = QDoubleSpinBox(self.groupBoxCV1_6)
        self.widgetCVGateThreshold.setObjectName(u"widgetCVGateThreshold")
        self.widgetCVGateThreshold.setDecimals(0)
        self.widgetCVGateThreshold.setMinimum(10.000000000000000)
        self.widgetCVGateThreshold.setMaximum(5000.000000000000000)
        self.widgetCVGateThreshold.setSingleStep(100.000000000000000)
        self.widgetCVGateThreshold.setValue(2000.000000000000000)

        self.horizontalLayout_14.addWidget(self.widgetCVGateThreshold, 0, Qt.AlignTop)

        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_27)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.checkBoxCVGateEngage = QCheckBox(self.groupBoxCV1_6)
        self.checkBoxCVGateEngage.setObjectName(u"checkBoxCVGateEngage")

        self.verticalLayout_11.addWidget(self.checkBoxCVGateEngage)

        self.checkBoxCVGatePowerMotor = QCheckBox(self.groupBoxCV1_6)
        self.checkBoxCVGatePowerMotor.setObjectName(u"checkBoxCVGatePowerMotor")

        self.verticalLayout_11.addWidget(self.checkBoxCVGatePowerMotor)


        self.horizontalLayout_14.addLayout(self.verticalLayout_11)

        self.horizontalSpacer_28 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_28)

        self.checkBoxCVGateHold = QCheckBox(self.groupBoxCV1_6)
        self.checkBoxCVGateHold.setObjectName(u"checkBoxCVGateHold")

        self.horizontalLayout_14.addWidget(self.checkBoxCVGateHold, 0, Qt.AlignTop)


        self.verticalLayout_12.addLayout(self.horizontalLayout_14)

        self.label_59 = QLabel(self.groupBoxCV1_6)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setMaximumSize(QSize(16777215, 20))
        self.label_59.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")

        self.verticalLayout_12.addWidget(self.label_59)

        self.plainTextEditCVGateCommands = QPlainTextSub(self.groupBoxCV1_6)
        self.plainTextEditCVGateCommands.setObjectName(u"plainTextEditCVGateCommands")

        self.verticalLayout_12.addWidget(self.plainTextEditCVGateCommands)


        self.horizontalLayout_15.addLayout(self.verticalLayout_12)


        self.gridLayout_2.addWidget(self.groupBoxCV1_6, 3, 0, 1, 1)

        self.groupBoxCV1_5 = QGroupBox(self.tab_cvmapping)
        self.groupBoxCV1_5.setObjectName(u"groupBoxCV1_5")
        sizePolicy.setHeightForWidth(self.groupBoxCV1_5.sizePolicy().hasHeightForWidth())
        self.groupBoxCV1_5.setSizePolicy(sizePolicy)
        self.groupBoxCV1_5.setMinimumSize(QSize(500, 150))
        self.horizontalLayout_21 = QHBoxLayout(self.groupBoxCV1_5)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.labelCV1_26 = QLabel(self.groupBoxCV1_5)
        self.labelCV1_26.setObjectName(u"labelCV1_26")
        sizePolicy4.setHeightForWidth(self.labelCV1_26.sizePolicy().hasHeightForWidth())
        self.labelCV1_26.setSizePolicy(sizePolicy4)
        self.labelCV1_26.setMinimumSize(QSize(66, 15))
        self.labelCV1_26.setMaximumSize(QSize(66, 15))
        self.labelCV1_26.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")
        self.labelCV1_26.setAlignment(Qt.AlignCenter)

        self.verticalLayout_21.addWidget(self.labelCV1_26)

        self.dialCVHammerTrigger = QDial(self.groupBoxCV1_5)
        self.dialCVHammerTrigger.setObjectName(u"dialCVHammerTrigger")
        self.dialCVHammerTrigger.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.dialCVHammerTrigger.sizePolicy().hasHeightForWidth())
        self.dialCVHammerTrigger.setSizePolicy(sizePolicy4)
        self.dialCVHammerTrigger.setMinimumSize(QSize(66, 61))
        self.dialCVHammerTrigger.setMaximumSize(QSize(66, 61))
        self.dialCVHammerTrigger.setMaximum(65535)
        self.dialCVHammerTrigger.setSingleStep(100)
        self.dialCVHammerTrigger.setPageStep(1000)
        self.dialCVHammerTrigger.setNotchesVisible(True)

        self.verticalLayout_21.addWidget(self.dialCVHammerTrigger)

        self.labelCVHammerTrigger = QLabel(self.groupBoxCV1_5)
        self.labelCVHammerTrigger.setObjectName(u"labelCVHammerTrigger")
        self.labelCVHammerTrigger.setStyleSheet(u"QLabel {\n"
"	font-size: 10px;\n"
"}")
        self.labelCVHammerTrigger.setAlignment(Qt.AlignCenter)

        self.verticalLayout_21.addWidget(self.labelCVHammerTrigger)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_21.addItem(self.verticalSpacer_8)


        self.horizontalLayout_21.addLayout(self.verticalLayout_21)

        self.line_16 = QFrame(self.groupBoxCV1_5)
        self.line_16.setObjectName(u"line_16")
        self.line_16.setFrameShape(QFrame.Shape.VLine)
        self.line_16.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_21.addWidget(self.line_16)

        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.label_58 = QLabel(self.groupBoxCV1_5)
        self.label_58.setObjectName(u"label_58")
        sizePolicy4.setHeightForWidth(self.label_58.sizePolicy().hasHeightForWidth())
        self.label_58.setSizePolicy(sizePolicy4)
        self.label_58.setMinimumSize(QSize(0, 15))
        self.label_58.setMaximumSize(QSize(16777215, 15))
        self.label_58.setStyleSheet(u"QLabel {\n"
"	font-size: 13px;\n"
"}")

        self.verticalLayout_20.addWidget(self.label_58)

        self.plainTextEditCVHammerTriggerCommands = QPlainTextSub(self.groupBoxCV1_5)
        self.plainTextEditCVHammerTriggerCommands.setObjectName(u"plainTextEditCVHammerTriggerCommands")

        self.verticalLayout_20.addWidget(self.plainTextEditCVHammerTriggerCommands)


        self.horizontalLayout_21.addLayout(self.verticalLayout_20)


        self.gridLayout_2.addWidget(self.groupBoxCV1_5, 3, 1, 1, 1)


        self.verticalLayout_28.addLayout(self.gridLayout_2)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_8)

        self.pushButtonResetADCSettings = QPushButton(self.tab_cvmapping)
        self.pushButtonResetADCSettings.setObjectName(u"pushButtonResetADCSettings")

        self.horizontalLayout_26.addWidget(self.pushButtonResetADCSettings)


        self.verticalLayout_28.addLayout(self.horizontalLayout_26)

        self.tabWidgetMain.addTab(self.tab_cvmapping, "")
        self.tab_advanced = QWidget()
        self.tab_advanced.setObjectName(u"tab_advanced")
        self.verticalLayout_30 = QVBoxLayout(self.tab_advanced)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.groupBox_12 = QGroupBox(self.tab_advanced)
        self.groupBox_12.setObjectName(u"groupBox_12")
        sizePolicy6.setHeightForWidth(self.groupBox_12.sizePolicy().hasHeightForWidth())
        self.groupBox_12.setSizePolicy(sizePolicy6)
        self.gridLayout_3 = QGridLayout(self.groupBox_12)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.label_64 = QLabel(self.groupBox_12)
        self.label_64.setObjectName(u"label_64")

        self.horizontalLayout_33.addWidget(self.label_64)

        self.doubleSpinBoxBowMotorPIDie = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBoxBowMotorPIDie.setObjectName(u"doubleSpinBoxBowMotorPIDie")
        self.doubleSpinBoxBowMotorPIDie.setEnabled(True)
        self.doubleSpinBoxBowMotorPIDie.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxBowMotorPIDie.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxBowMotorPIDie.setMaximum(1000.000000000000000)
        self.doubleSpinBoxBowMotorPIDie.setSingleStep(0.010000000000000)

        self.horizontalLayout_33.addWidget(self.doubleSpinBoxBowMotorPIDie)


        self.gridLayout_3.addLayout(self.horizontalLayout_33, 1, 4, 1, 1)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.label_65 = QLabel(self.groupBox_12)
        self.label_65.setObjectName(u"label_65")

        self.horizontalLayout_34.addWidget(self.label_65)

        self.doubleSpinBoxBowMotorMaxError = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBoxBowMotorMaxError.setObjectName(u"doubleSpinBoxBowMotorMaxError")
        self.doubleSpinBoxBowMotorMaxError.setEnabled(True)
        self.doubleSpinBoxBowMotorMaxError.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxBowMotorMaxError.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxBowMotorMaxError.setMaximum(1000.000000000000000)

        self.horizontalLayout_34.addWidget(self.doubleSpinBoxBowMotorMaxError)


        self.gridLayout_3.addLayout(self.horizontalLayout_34, 2, 4, 1, 1)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_13 = QLabel(self.groupBox_12)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_27.addWidget(self.label_13)

        self.doubleSpinBoxBowMotorMaxSpeed = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBoxBowMotorMaxSpeed.setObjectName(u"doubleSpinBoxBowMotorMaxSpeed")
        self.doubleSpinBoxBowMotorMaxSpeed.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.doubleSpinBoxBowMotorMaxSpeed.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxBowMotorMaxSpeed.setSizePolicy(sizePolicy4)
        self.doubleSpinBoxBowMotorMaxSpeed.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxBowMotorMaxSpeed.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxBowMotorMaxSpeed.setMaximum(1000.000000000000000)

        self.horizontalLayout_27.addWidget(self.doubleSpinBoxBowMotorMaxSpeed)


        self.gridLayout_3.addLayout(self.horizontalLayout_27, 0, 0, 1, 1)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_18 = QLabel(self.groupBox_12)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_29.addWidget(self.label_18)

        self.doubleSpinBoxBowMotorVoltage = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBoxBowMotorVoltage.setObjectName(u"doubleSpinBoxBowMotorVoltage")
        self.doubleSpinBoxBowMotorVoltage.setEnabled(True)
        self.doubleSpinBoxBowMotorVoltage.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxBowMotorVoltage.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxBowMotorVoltage.setMaximum(10.000000000000000)
        self.doubleSpinBoxBowMotorVoltage.setSingleStep(0.100000000000000)

        self.horizontalLayout_29.addWidget(self.doubleSpinBoxBowMotorVoltage)


        self.gridLayout_3.addLayout(self.horizontalLayout_29, 2, 0, 1, 1)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_20, 1, 3, 1, 1)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.label_40 = QLabel(self.groupBox_12)
        self.label_40.setObjectName(u"label_40")

        self.horizontalLayout_30.addWidget(self.label_40)

        self.doubleSpinBoxBowMotorPIDKp = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBoxBowMotorPIDKp.setObjectName(u"doubleSpinBoxBowMotorPIDKp")
        self.doubleSpinBoxBowMotorPIDKp.setEnabled(True)
        self.doubleSpinBoxBowMotorPIDKp.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxBowMotorPIDKp.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxBowMotorPIDKp.setMaximum(1000.000000000000000)
        self.doubleSpinBoxBowMotorPIDKp.setSingleStep(10.000000000000000)

        self.horizontalLayout_30.addWidget(self.doubleSpinBoxBowMotorPIDKp)


        self.gridLayout_3.addLayout(self.horizontalLayout_30, 0, 2, 1, 1)

        self.pushButtonCalibrateMotorSpeed = QPushButton(self.groupBox_12)
        self.pushButtonCalibrateMotorSpeed.setObjectName(u"pushButtonCalibrateMotorSpeed")
        sizePolicy4.setHeightForWidth(self.pushButtonCalibrateMotorSpeed.sizePolicy().hasHeightForWidth())
        self.pushButtonCalibrateMotorSpeed.setSizePolicy(sizePolicy4)

        self.gridLayout_3.addWidget(self.pushButtonCalibrateMotorSpeed, 2, 6, 1, 1, Qt.AlignRight)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_17 = QLabel(self.groupBox_12)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_28.addWidget(self.label_17)

        self.doubleSpinBoxBowMotorMinSpeed = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBoxBowMotorMinSpeed.setObjectName(u"doubleSpinBoxBowMotorMinSpeed")
        self.doubleSpinBoxBowMotorMinSpeed.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.doubleSpinBoxBowMotorMinSpeed.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxBowMotorMinSpeed.setSizePolicy(sizePolicy4)
        self.doubleSpinBoxBowMotorMinSpeed.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxBowMotorMinSpeed.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxBowMotorMinSpeed.setMaximum(150.000000000000000)

        self.horizontalLayout_28.addWidget(self.doubleSpinBoxBowMotorMinSpeed)


        self.gridLayout_3.addLayout(self.horizontalLayout_28, 1, 0, 1, 1)

        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.label_37 = QLabel(self.groupBox_12)
        self.label_37.setObjectName(u"label_37")

        self.horizontalLayout_35.addWidget(self.label_37)

        self.doubleSpinBoxBowMotorTimeout = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBoxBowMotorTimeout.setObjectName(u"doubleSpinBoxBowMotorTimeout")
        self.doubleSpinBoxBowMotorTimeout.setEnabled(True)
        self.doubleSpinBoxBowMotorTimeout.setDecimals(0)
        self.doubleSpinBoxBowMotorTimeout.setMaximum(65535.000000000000000)
        self.doubleSpinBoxBowMotorTimeout.setSingleStep(1000.000000000000000)

        self.horizontalLayout_35.addWidget(self.doubleSpinBoxBowMotorTimeout)


        self.gridLayout_3.addLayout(self.horizontalLayout_35, 0, 6, 1, 1)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.label_63 = QLabel(self.groupBox_12)
        self.label_63.setObjectName(u"label_63")

        self.horizontalLayout_32.addWidget(self.label_63)

        self.doubleSpinBoxBowMotorPIDKd = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBoxBowMotorPIDKd.setObjectName(u"doubleSpinBoxBowMotorPIDKd")
        self.doubleSpinBoxBowMotorPIDKd.setEnabled(True)
        self.doubleSpinBoxBowMotorPIDKd.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxBowMotorPIDKd.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxBowMotorPIDKd.setMaximum(1000.000000000000000)
        self.doubleSpinBoxBowMotorPIDKd.setSingleStep(10.000000000000000)

        self.horizontalLayout_32.addWidget(self.doubleSpinBoxBowMotorPIDKd)


        self.gridLayout_3.addLayout(self.horizontalLayout_32, 2, 2, 1, 1)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_21, 1, 1, 1, 1)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.label_41 = QLabel(self.groupBox_12)
        self.label_41.setObjectName(u"label_41")

        self.horizontalLayout_31.addWidget(self.label_41)

        self.doubleSpinBoxBowMotorPIDKi = QDoubleSpinBox(self.groupBox_12)
        self.doubleSpinBoxBowMotorPIDKi.setObjectName(u"doubleSpinBoxBowMotorPIDKi")
        self.doubleSpinBoxBowMotorPIDKi.setEnabled(True)
        self.doubleSpinBoxBowMotorPIDKi.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxBowMotorPIDKi.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxBowMotorPIDKi.setMaximum(1000.000000000000000)
        self.doubleSpinBoxBowMotorPIDKi.setSingleStep(0.500000000000000)

        self.horizontalLayout_31.addWidget(self.doubleSpinBoxBowMotorPIDKi)


        self.gridLayout_3.addLayout(self.horizontalLayout_31, 1, 2, 1, 1)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_22, 0, 5, 1, 1)

        self.pushButtonCalibrateMotorSpeed.raise_()

        self.verticalLayout_30.addWidget(self.groupBox_12)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_30.addItem(self.verticalSpacer_12)

        self.groupBoxBowParameters = QGroupBox(self.tab_advanced)
        self.groupBoxBowParameters.setObjectName(u"groupBoxBowParameters")
        sizePolicy6.setHeightForWidth(self.groupBoxBowParameters.sizePolicy().hasHeightForWidth())
        self.groupBoxBowParameters.setSizePolicy(sizePolicy6)
        self.gridLayout_4 = QGridLayout(self.groupBoxBowParameters)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_38 = QHBoxLayout()
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.label_21 = QLabel(self.groupBoxBowParameters)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_38.addWidget(self.label_21)

        self.doubleSpinBoxBowRestPosition = QDoubleSpinBox(self.groupBoxBowParameters)
        self.doubleSpinBoxBowRestPosition.setObjectName(u"doubleSpinBoxBowRestPosition")
        self.doubleSpinBoxBowRestPosition.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxBowRestPosition.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxBowRestPosition.setDecimals(0)
        self.doubleSpinBoxBowRestPosition.setMaximum(65536.000000000000000)
        self.doubleSpinBoxBowRestPosition.setSingleStep(1000.000000000000000)
        self.doubleSpinBoxBowRestPosition.setValue(65535.000000000000000)

        self.horizontalLayout_38.addWidget(self.doubleSpinBoxBowRestPosition)

        self.pushButtonBowRestPressureTest = QPushButton(self.groupBoxBowParameters)
        self.pushButtonBowRestPressureTest.setObjectName(u"pushButtonBowRestPressureTest")
        self.pushButtonBowRestPressureTest.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.pushButtonBowRestPressureTest.sizePolicy().hasHeightForWidth())
        self.pushButtonBowRestPressureTest.setSizePolicy(sizePolicy4)
        self.pushButtonBowRestPressureTest.setMinimumSize(QSize(11, 0))
        self.pushButtonBowRestPressureTest.setMaximumSize(QSize(11, 16777215))
        self.pushButtonBowRestPressureTest.setFlat(False)

        self.horizontalLayout_38.addWidget(self.pushButtonBowRestPressureTest)


        self.gridLayout_4.addLayout(self.horizontalLayout_38, 3, 0, 2, 1)

        self.horizontalLayout_39 = QHBoxLayout()
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_39.addItem(self.horizontalSpacer_10)

        self.label_3 = QLabel(self.groupBoxBowParameters)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(50, 0))
        self.label_3.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_39.addWidget(self.label_3)

        self.comboBoxActuatorPreset = QComboBox(self.groupBoxBowParameters)
        self.comboBoxActuatorPreset.setObjectName(u"comboBoxActuatorPreset")
        sizePolicy8.setHeightForWidth(self.comboBoxActuatorPreset.sizePolicy().hasHeightForWidth())
        self.comboBoxActuatorPreset.setSizePolicy(sizePolicy8)
        self.comboBoxActuatorPreset.setMinimumSize(QSize(150, 0))
        self.comboBoxActuatorPreset.setMaximumSize(QSize(300, 16777215))
        self.comboBoxActuatorPreset.setEditable(False)

        self.horizontalLayout_39.addWidget(self.comboBoxActuatorPreset)


        self.gridLayout_4.addLayout(self.horizontalLayout_39, 0, 4, 1, 1)

        self.pushButtonActuatorLoad = QPushButton(self.groupBoxBowParameters)
        self.pushButtonActuatorLoad.setObjectName(u"pushButtonActuatorLoad")
        self.pushButtonActuatorLoad.setMinimumSize(QSize(80, 0))
        self.pushButtonActuatorLoad.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_4.addWidget(self.pushButtonActuatorLoad, 4, 4, 1, 1)

        self.horizontalLayout_40 = QHBoxLayout()
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_40.addItem(self.horizontalSpacer_9)

        self.pushButtonActuatorAdd = QPushButton(self.groupBoxBowParameters)
        self.pushButtonActuatorAdd.setObjectName(u"pushButtonActuatorAdd")
        sizePolicy4.setHeightForWidth(self.pushButtonActuatorAdd.sizePolicy().hasHeightForWidth())
        self.pushButtonActuatorAdd.setSizePolicy(sizePolicy4)
        self.pushButtonActuatorAdd.setMinimumSize(QSize(60, 0))
        self.pushButtonActuatorAdd.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_40.addWidget(self.pushButtonActuatorAdd)

        self.pushButtonActuatorRemove = QPushButton(self.groupBoxBowParameters)
        self.pushButtonActuatorRemove.setObjectName(u"pushButtonActuatorRemove")
        sizePolicy4.setHeightForWidth(self.pushButtonActuatorRemove.sizePolicy().hasHeightForWidth())
        self.pushButtonActuatorRemove.setSizePolicy(sizePolicy4)
        self.pushButtonActuatorRemove.setMinimumSize(QSize(60, 0))
        self.pushButtonActuatorRemove.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_40.addWidget(self.pushButtonActuatorRemove)

        self.pushButtonActuatorRename = QPushButton(self.groupBoxBowParameters)
        self.pushButtonActuatorRename.setObjectName(u"pushButtonActuatorRename")
        sizePolicy4.setHeightForWidth(self.pushButtonActuatorRename.sizePolicy().hasHeightForWidth())
        self.pushButtonActuatorRename.setSizePolicy(sizePolicy4)
        self.pushButtonActuatorRename.setMinimumSize(QSize(60, 0))
        self.pushButtonActuatorRename.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_40.addWidget(self.pushButtonActuatorRename)


        self.gridLayout_4.addLayout(self.horizontalLayout_40, 2, 4, 2, 1)

        self.pushButtonRestBow = QPushButton(self.groupBoxBowParameters)
        self.pushButtonRestBow.setObjectName(u"pushButtonRestBow")
        sizePolicy4.setHeightForWidth(self.pushButtonRestBow.sizePolicy().hasHeightForWidth())
        self.pushButtonRestBow.setSizePolicy(sizePolicy4)

        self.gridLayout_4.addWidget(self.pushButtonRestBow, 0, 2, 2, 1)

        self.horizontalSpacer_23 = QSpacerItem(20, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_23, 0, 1, 1, 1)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.label_20 = QLabel(self.groupBoxBowParameters)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_37.addWidget(self.label_20)

        self.doubleSpinBoxBowMinPressure = QDoubleSpinBox(self.groupBoxBowParameters)
        self.doubleSpinBoxBowMinPressure.setObjectName(u"doubleSpinBoxBowMinPressure")
        self.doubleSpinBoxBowMinPressure.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxBowMinPressure.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxBowMinPressure.setDecimals(0)
        self.doubleSpinBoxBowMinPressure.setMaximum(65536.000000000000000)
        self.doubleSpinBoxBowMinPressure.setSingleStep(1000.000000000000000)
        self.doubleSpinBoxBowMinPressure.setValue(65535.000000000000000)

        self.horizontalLayout_37.addWidget(self.doubleSpinBoxBowMinPressure)

        self.pushButtonBowEngagePressureTest = QPushButton(self.groupBoxBowParameters)
        self.pushButtonBowEngagePressureTest.setObjectName(u"pushButtonBowEngagePressureTest")
        self.pushButtonBowEngagePressureTest.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.pushButtonBowEngagePressureTest.sizePolicy().hasHeightForWidth())
        self.pushButtonBowEngagePressureTest.setSizePolicy(sizePolicy4)
        self.pushButtonBowEngagePressureTest.setFlat(False)

        self.horizontalLayout_37.addWidget(self.pushButtonBowEngagePressureTest)


        self.gridLayout_4.addLayout(self.horizontalLayout_37, 1, 0, 2, 1)

        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.label_19 = QLabel(self.groupBoxBowParameters)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_36.addWidget(self.label_19)

        self.doubleSpinBoxBowMaxPressure = QDoubleSpinBox(self.groupBoxBowParameters)
        self.doubleSpinBoxBowMaxPressure.setObjectName(u"doubleSpinBoxBowMaxPressure")
        self.doubleSpinBoxBowMaxPressure.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxBowMaxPressure.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxBowMaxPressure.setDecimals(0)
        self.doubleSpinBoxBowMaxPressure.setMaximum(65536.000000000000000)
        self.doubleSpinBoxBowMaxPressure.setSingleStep(1000.000000000000000)
        self.doubleSpinBoxBowMaxPressure.setValue(65535.000000000000000)

        self.horizontalLayout_36.addWidget(self.doubleSpinBoxBowMaxPressure)

        self.pushButtonBowMaxPressureTest = QPushButton(self.groupBoxBowParameters)
        self.pushButtonBowMaxPressureTest.setObjectName(u"pushButtonBowMaxPressureTest")
        self.pushButtonBowMaxPressureTest.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.pushButtonBowMaxPressureTest.sizePolicy().hasHeightForWidth())
        self.pushButtonBowMaxPressureTest.setSizePolicy(sizePolicy4)
        self.pushButtonBowMaxPressureTest.setFlat(False)

        self.horizontalLayout_36.addWidget(self.pushButtonBowMaxPressureTest)


        self.gridLayout_4.addLayout(self.horizontalLayout_36, 0, 0, 1, 1)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_24, 0, 3, 1, 1)


        self.verticalLayout_30.addWidget(self.groupBoxBowParameters)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_30.addItem(self.verticalSpacer_13)

        self.groupBoxMuteParameters = QGroupBox(self.tab_advanced)
        self.groupBoxMuteParameters.setObjectName(u"groupBoxMuteParameters")
        sizePolicy6.setHeightForWidth(self.groupBoxMuteParameters.sizePolicy().hasHeightForWidth())
        self.groupBoxMuteParameters.setSizePolicy(sizePolicy6)
        self.verticalLayout_29 = QVBoxLayout(self.groupBoxMuteParameters)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_45 = QHBoxLayout()
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.horizontalLayout_41 = QHBoxLayout()
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.label_25 = QLabel(self.groupBoxMuteParameters)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_41.addWidget(self.label_25)

        self.doubleSpinBoxMuteRestPosition = QDoubleSpinBox(self.groupBoxMuteParameters)
        self.doubleSpinBoxMuteRestPosition.setObjectName(u"doubleSpinBoxMuteRestPosition")
        self.doubleSpinBoxMuteRestPosition.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxMuteRestPosition.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxMuteRestPosition.setDecimals(0)
        self.doubleSpinBoxMuteRestPosition.setMaximum(65536.000000000000000)
        self.doubleSpinBoxMuteRestPosition.setSingleStep(1000.000000000000000)
        self.doubleSpinBoxMuteRestPosition.setValue(65535.000000000000000)

        self.horizontalLayout_41.addWidget(self.doubleSpinBoxMuteRestPosition)

        self.pushButtonMuteRestTest = QPushButton(self.groupBoxMuteParameters)
        self.pushButtonMuteRestTest.setObjectName(u"pushButtonMuteRestTest")
        self.pushButtonMuteRestTest.setEnabled(True)
        self.pushButtonMuteRestTest.setMinimumSize(QSize(11, 0))
        self.pushButtonMuteRestTest.setMaximumSize(QSize(11, 16777215))
        self.pushButtonMuteRestTest.setFlat(False)

        self.horizontalLayout_41.addWidget(self.pushButtonMuteRestTest)


        self.horizontalLayout_45.addLayout(self.horizontalLayout_41)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_45.addItem(self.horizontalSpacer_25)

        self.horizontalLayout_42 = QHBoxLayout()
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.label_26 = QLabel(self.groupBoxMuteParameters)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_42.addWidget(self.label_26)

        self.doubleSpinBoxMuteFullMutePosition = QDoubleSpinBox(self.groupBoxMuteParameters)
        self.doubleSpinBoxMuteFullMutePosition.setObjectName(u"doubleSpinBoxMuteFullMutePosition")
        self.doubleSpinBoxMuteFullMutePosition.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxMuteFullMutePosition.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxMuteFullMutePosition.setDecimals(0)
        self.doubleSpinBoxMuteFullMutePosition.setMaximum(65536.000000000000000)
        self.doubleSpinBoxMuteFullMutePosition.setSingleStep(1000.000000000000000)
        self.doubleSpinBoxMuteFullMutePosition.setValue(65535.000000000000000)

        self.horizontalLayout_42.addWidget(self.doubleSpinBoxMuteFullMutePosition)

        self.pushButtonMuteFullTest = QPushButton(self.groupBoxMuteParameters)
        self.pushButtonMuteFullTest.setObjectName(u"pushButtonMuteFullTest")
        self.pushButtonMuteFullTest.setEnabled(True)
        self.pushButtonMuteFullTest.setMinimumSize(QSize(11, 0))
        self.pushButtonMuteFullTest.setMaximumSize(QSize(11, 16777215))
        self.pushButtonMuteFullTest.setFlat(False)

        self.horizontalLayout_42.addWidget(self.pushButtonMuteFullTest)


        self.horizontalLayout_45.addLayout(self.horizontalLayout_42)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_45.addItem(self.horizontalSpacer_11)

        self.horizontalLayout_43 = QHBoxLayout()
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.label_27 = QLabel(self.groupBoxMuteParameters)
        self.label_27.setObjectName(u"label_27")

        self.horizontalLayout_43.addWidget(self.label_27)

        self.doubleSpinBoxMuteHalfMutePosition = QDoubleSpinBox(self.groupBoxMuteParameters)
        self.doubleSpinBoxMuteHalfMutePosition.setObjectName(u"doubleSpinBoxMuteHalfMutePosition")
        self.doubleSpinBoxMuteHalfMutePosition.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxMuteHalfMutePosition.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxMuteHalfMutePosition.setDecimals(0)
        self.doubleSpinBoxMuteHalfMutePosition.setMaximum(65536.000000000000000)
        self.doubleSpinBoxMuteHalfMutePosition.setSingleStep(1000.000000000000000)
        self.doubleSpinBoxMuteHalfMutePosition.setValue(65535.000000000000000)

        self.horizontalLayout_43.addWidget(self.doubleSpinBoxMuteHalfMutePosition)

        self.pushButtonMuteHalfTest = QPushButton(self.groupBoxMuteParameters)
        self.pushButtonMuteHalfTest.setObjectName(u"pushButtonMuteHalfTest")
        self.pushButtonMuteHalfTest.setEnabled(True)
        self.pushButtonMuteHalfTest.setMinimumSize(QSize(11, 0))
        self.pushButtonMuteHalfTest.setMaximumSize(QSize(11, 16777215))
        self.pushButtonMuteHalfTest.setFlat(False)

        self.horizontalLayout_43.addWidget(self.pushButtonMuteHalfTest)


        self.horizontalLayout_45.addLayout(self.horizontalLayout_43)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_45.addItem(self.horizontalSpacer_12)

        self.horizontalLayout_44 = QHBoxLayout()
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.label_42 = QLabel(self.groupBoxMuteParameters)
        self.label_42.setObjectName(u"label_42")

        self.horizontalLayout_44.addWidget(self.label_42)

        self.doubleSpinBoxMuteBackoff = QDoubleSpinBox(self.groupBoxMuteParameters)
        self.doubleSpinBoxMuteBackoff.setObjectName(u"doubleSpinBoxMuteBackoff")
        self.doubleSpinBoxMuteBackoff.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxMuteBackoff.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxMuteBackoff.setDecimals(0)
        self.doubleSpinBoxMuteBackoff.setMaximum(65536.000000000000000)
        self.doubleSpinBoxMuteBackoff.setSingleStep(1000.000000000000000)
        self.doubleSpinBoxMuteBackoff.setValue(65535.000000000000000)

        self.horizontalLayout_44.addWidget(self.doubleSpinBoxMuteBackoff)

        self.label_43 = QLabel(self.groupBoxMuteParameters)
        self.label_43.setObjectName(u"label_43")

        self.horizontalLayout_44.addWidget(self.label_43)


        self.horizontalLayout_45.addLayout(self.horizontalLayout_44)


        self.verticalLayout_29.addLayout(self.horizontalLayout_45)

        self.pushButtonRestMute = QPushButton(self.groupBoxMuteParameters)
        self.pushButtonRestMute.setObjectName(u"pushButtonRestMute")
        sizePolicy4.setHeightForWidth(self.pushButtonRestMute.sizePolicy().hasHeightForWidth())
        self.pushButtonRestMute.setSizePolicy(sizePolicy4)

        self.verticalLayout_29.addWidget(self.pushButtonRestMute, 0, Qt.AlignRight)


        self.verticalLayout_30.addWidget(self.groupBoxMuteParameters)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_30.addItem(self.verticalSpacer_14)

        self.groupBoxSolenoidParameters = QGroupBox(self.tab_advanced)
        self.groupBoxSolenoidParameters.setObjectName(u"groupBoxSolenoidParameters")
        sizePolicy6.setHeightForWidth(self.groupBoxSolenoidParameters.sizePolicy().hasHeightForWidth())
        self.groupBoxSolenoidParameters.setSizePolicy(sizePolicy6)
        self.horizontalLayout_49 = QHBoxLayout(self.groupBoxSolenoidParameters)
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.horizontalLayout_49.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_46 = QHBoxLayout()
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.label_32 = QLabel(self.groupBoxSolenoidParameters)
        self.label_32.setObjectName(u"label_32")

        self.horizontalLayout_46.addWidget(self.label_32)

        self.doubleSpinBoxSolenoidMinForce = QDoubleSpinBox(self.groupBoxSolenoidParameters)
        self.doubleSpinBoxSolenoidMinForce.setObjectName(u"doubleSpinBoxSolenoidMinForce")
        self.doubleSpinBoxSolenoidMinForce.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxSolenoidMinForce.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxSolenoidMinForce.setDecimals(0)
        self.doubleSpinBoxSolenoidMinForce.setMaximum(65536.000000000000000)
        self.doubleSpinBoxSolenoidMinForce.setSingleStep(1000.000000000000000)
        self.doubleSpinBoxSolenoidMinForce.setValue(65535.000000000000000)

        self.horizontalLayout_46.addWidget(self.doubleSpinBoxSolenoidMinForce)

        self.pushButtonSolenoidMinForceTest = QPushButton(self.groupBoxSolenoidParameters)
        self.pushButtonSolenoidMinForceTest.setObjectName(u"pushButtonSolenoidMinForceTest")
        self.pushButtonSolenoidMinForceTest.setEnabled(True)
        self.pushButtonSolenoidMinForceTest.setMinimumSize(QSize(11, 0))
        self.pushButtonSolenoidMinForceTest.setMaximumSize(QSize(11, 16777215))
        self.pushButtonSolenoidMinForceTest.setFlat(False)

        self.horizontalLayout_46.addWidget(self.pushButtonSolenoidMinForceTest)


        self.horizontalLayout_49.addLayout(self.horizontalLayout_46)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_49.addItem(self.horizontalSpacer_13)

        self.horizontalLayout_47 = QHBoxLayout()
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.label_33 = QLabel(self.groupBoxSolenoidParameters)
        self.label_33.setObjectName(u"label_33")

        self.horizontalLayout_47.addWidget(self.label_33)

        self.doubleSpinBoxSolenoidMaxForce = QDoubleSpinBox(self.groupBoxSolenoidParameters)
        self.doubleSpinBoxSolenoidMaxForce.setObjectName(u"doubleSpinBoxSolenoidMaxForce")
        self.doubleSpinBoxSolenoidMaxForce.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxSolenoidMaxForce.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxSolenoidMaxForce.setDecimals(0)
        self.doubleSpinBoxSolenoidMaxForce.setMaximum(65536.000000000000000)
        self.doubleSpinBoxSolenoidMaxForce.setSingleStep(1000.000000000000000)
        self.doubleSpinBoxSolenoidMaxForce.setValue(65535.000000000000000)

        self.horizontalLayout_47.addWidget(self.doubleSpinBoxSolenoidMaxForce)

        self.pushButtonSolenoidMaxForceTest = QPushButton(self.groupBoxSolenoidParameters)
        self.pushButtonSolenoidMaxForceTest.setObjectName(u"pushButtonSolenoidMaxForceTest")
        self.pushButtonSolenoidMaxForceTest.setEnabled(True)
        self.pushButtonSolenoidMaxForceTest.setMinimumSize(QSize(11, 0))
        self.pushButtonSolenoidMaxForceTest.setMaximumSize(QSize(11, 16777215))
        self.pushButtonSolenoidMaxForceTest.setFlat(False)

        self.horizontalLayout_47.addWidget(self.pushButtonSolenoidMaxForceTest)


        self.horizontalLayout_49.addLayout(self.horizontalLayout_47)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_49.addItem(self.horizontalSpacer_14)

        self.horizontalLayout_48 = QHBoxLayout()
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.label_39 = QLabel(self.groupBoxSolenoidParameters)
        self.label_39.setObjectName(u"label_39")

        self.horizontalLayout_48.addWidget(self.label_39)

        self.doubleSpinBoxSolenoidEngageDuration = QDoubleSpinBox(self.groupBoxSolenoidParameters)
        self.doubleSpinBoxSolenoidEngageDuration.setObjectName(u"doubleSpinBoxSolenoidEngageDuration")
        self.doubleSpinBoxSolenoidEngageDuration.setMinimumSize(QSize(90, 0))
        self.doubleSpinBoxSolenoidEngageDuration.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBoxSolenoidEngageDuration.setDecimals(0)
        self.doubleSpinBoxSolenoidEngageDuration.setMaximum(65536.000000000000000)
        self.doubleSpinBoxSolenoidEngageDuration.setSingleStep(1000.000000000000000)
        self.doubleSpinBoxSolenoidEngageDuration.setValue(65535.000000000000000)

        self.horizontalLayout_48.addWidget(self.doubleSpinBoxSolenoidEngageDuration)

        self.label_62 = QLabel(self.groupBoxSolenoidParameters)
        self.label_62.setObjectName(u"label_62")

        self.horizontalLayout_48.addWidget(self.label_62)

        self.pushButtonHammerDurationTest = QPushButton(self.groupBoxSolenoidParameters)
        self.pushButtonHammerDurationTest.setObjectName(u"pushButtonHammerDurationTest")
        self.pushButtonHammerDurationTest.setEnabled(True)
        self.pushButtonHammerDurationTest.setMinimumSize(QSize(11, 0))
        self.pushButtonHammerDurationTest.setMaximumSize(QSize(11, 16777215))
        self.pushButtonHammerDurationTest.setFlat(False)

        self.horizontalLayout_48.addWidget(self.pushButtonHammerDurationTest)


        self.horizontalLayout_49.addLayout(self.horizontalLayout_48)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_49.addItem(self.horizontalSpacer_15)

        self.pushButtonEngageHammer = QPushButton(self.groupBoxSolenoidParameters)
        self.pushButtonEngageHammer.setObjectName(u"pushButtonEngageHammer")
        sizePolicy4.setHeightForWidth(self.pushButtonEngageHammer.sizePolicy().hasHeightForWidth())
        self.pushButtonEngageHammer.setSizePolicy(sizePolicy4)

        self.horizontalLayout_49.addWidget(self.pushButtonEngageHammer)


        self.verticalLayout_30.addWidget(self.groupBoxSolenoidParameters)

        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_30.addItem(self.verticalSpacer_15)

        self.groupBox_4 = QGroupBox(self.tab_advanced)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy6.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy6)
        self.horizontalLayout_52 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.horizontalLayout_52.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_50 = QHBoxLayout()
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.label_47 = QLabel(self.groupBox_4)
        self.label_47.setObjectName(u"label_47")

        self.horizontalLayout_50.addWidget(self.label_47)

        self.spinBoxHarmonicShiftRange = QSpinBox(self.groupBox_4)
        self.spinBoxHarmonicShiftRange.setObjectName(u"spinBoxHarmonicShiftRange")
        self.spinBoxHarmonicShiftRange.setMaximum(36)
        self.spinBoxHarmonicShiftRange.setValue(12)

        self.horizontalLayout_50.addWidget(self.spinBoxHarmonicShiftRange)


        self.horizontalLayout_52.addLayout(self.horizontalLayout_50)

        self.horizontalLayout_51 = QHBoxLayout()
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_51.addItem(self.horizontalSpacer_17)

        self.label_22 = QLabel(self.groupBox_4)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_51.addWidget(self.label_22)

        self.comboBoxCurrentlySelectedModule = QComboBox(self.groupBox_4)
        self.comboBoxCurrentlySelectedModule.setObjectName(u"comboBoxCurrentlySelectedModule")

        self.horizontalLayout_51.addWidget(self.comboBoxCurrentlySelectedModule)


        self.horizontalLayout_52.addLayout(self.horizontalLayout_51)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_52.addItem(self.horizontalSpacer_19)

        self.pushButtonHomeBow = QPushButton(self.groupBox_4)
        self.pushButtonHomeBow.setObjectName(u"pushButtonHomeBow")
        sizePolicy4.setHeightForWidth(self.pushButtonHomeBow.sizePolicy().hasHeightForWidth())
        self.pushButtonHomeBow.setSizePolicy(sizePolicy4)

        self.horizontalLayout_52.addWidget(self.pushButtonHomeBow)

        self.pushButtonHomeMute = QPushButton(self.groupBox_4)
        self.pushButtonHomeMute.setObjectName(u"pushButtonHomeMute")
        sizePolicy4.setHeightForWidth(self.pushButtonHomeMute.sizePolicy().hasHeightForWidth())
        self.pushButtonHomeMute.setSizePolicy(sizePolicy4)

        self.horizontalLayout_52.addWidget(self.pushButtonHomeMute)

        self.pushButtonResetAllSettings = QPushButton(self.groupBox_4)
        self.pushButtonResetAllSettings.setObjectName(u"pushButtonResetAllSettings")
        sizePolicy4.setHeightForWidth(self.pushButtonResetAllSettings.sizePolicy().hasHeightForWidth())
        self.pushButtonResetAllSettings.setSizePolicy(sizePolicy4)

        self.horizontalLayout_52.addWidget(self.pushButtonResetAllSettings)


        self.verticalLayout_30.addWidget(self.groupBox_4)

        self.verticalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_30.addItem(self.verticalSpacer_16)

        self.tabWidgetMain.addTab(self.tab_advanced, "")
        self.tab_debugging = QWidget()
        self.tab_debugging.setObjectName(u"tab_debugging")
        self.verticalLayout_32 = QVBoxLayout(self.tab_debugging)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.horizontalLayout_55 = QHBoxLayout()
        self.horizontalLayout_55.setSpacing(0)
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.label_34 = QLabel(self.tab_debugging)
        self.label_34.setObjectName(u"label_34")
        sizePolicy6.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy6)
        self.label_34.setMinimumSize(QSize(0, 15))
        self.label_34.setMaximumSize(QSize(16777215, 15))
        self.label_34.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_55.addWidget(self.label_34)

        self.labelSetFrequency = QLabel(self.tab_debugging)
        self.labelSetFrequency.setObjectName(u"labelSetFrequency")
        sizePolicy6.setHeightForWidth(self.labelSetFrequency.sizePolicy().hasHeightForWidth())
        self.labelSetFrequency.setSizePolicy(sizePolicy6)
        self.labelSetFrequency.setMinimumSize(QSize(0, 15))
        self.labelSetFrequency.setMaximumSize(QSize(16777215, 15))
        self.labelSetFrequency.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_55.addWidget(self.labelSetFrequency)

        self.line_8 = QFrame(self.tab_debugging)
        self.line_8.setObjectName(u"line_8")
        sizePolicy6.setHeightForWidth(self.line_8.sizePolicy().hasHeightForWidth())
        self.line_8.setSizePolicy(sizePolicy6)
        self.line_8.setMinimumSize(QSize(0, 15))
        self.line_8.setMaximumSize(QSize(16777215, 15))
        self.line_8.setFrameShadow(QFrame.Plain)
        self.line_8.setFrameShape(QFrame.Shape.VLine)

        self.horizontalLayout_55.addWidget(self.line_8)

        self.label_10 = QLabel(self.tab_debugging)
        self.label_10.setObjectName(u"label_10")
        sizePolicy6.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy6)
        self.label_10.setMinimumSize(QSize(0, 15))
        self.label_10.setMaximumSize(QSize(16777215, 15))
        self.label_10.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_55.addWidget(self.label_10)

        self.labelBowFrequency = QLabel(self.tab_debugging)
        self.labelBowFrequency.setObjectName(u"labelBowFrequency")
        sizePolicy6.setHeightForWidth(self.labelBowFrequency.sizePolicy().hasHeightForWidth())
        self.labelBowFrequency.setSizePolicy(sizePolicy6)
        self.labelBowFrequency.setMinimumSize(QSize(0, 15))
        self.labelBowFrequency.setMaximumSize(QSize(16777215, 15))
        self.labelBowFrequency.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_55.addWidget(self.labelBowFrequency)

        self.line_9 = QFrame(self.tab_debugging)
        self.line_9.setObjectName(u"line_9")
        sizePolicy6.setHeightForWidth(self.line_9.sizePolicy().hasHeightForWidth())
        self.line_9.setSizePolicy(sizePolicy6)
        self.line_9.setMinimumSize(QSize(0, 15))
        self.line_9.setMaximumSize(QSize(16777215, 15))
        self.line_9.setFrameShadow(QFrame.Plain)
        self.line_9.setFrameShape(QFrame.Shape.VLine)

        self.horizontalLayout_55.addWidget(self.line_9)

        self.label_30 = QLabel(self.tab_debugging)
        self.label_30.setObjectName(u"label_30")
        sizePolicy6.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy6)
        self.label_30.setMinimumSize(QSize(0, 15))
        self.label_30.setMaximumSize(QSize(16777215, 15))
        self.label_30.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_55.addWidget(self.label_30)

        self.labelBowCurrent = QLabel(self.tab_debugging)
        self.labelBowCurrent.setObjectName(u"labelBowCurrent")
        sizePolicy6.setHeightForWidth(self.labelBowCurrent.sizePolicy().hasHeightForWidth())
        self.labelBowCurrent.setSizePolicy(sizePolicy6)
        self.labelBowCurrent.setMinimumSize(QSize(0, 15))
        self.labelBowCurrent.setMaximumSize(QSize(16777215, 15))
        self.labelBowCurrent.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_55.addWidget(self.labelBowCurrent)


        self.verticalLayout_32.addLayout(self.horizontalLayout_55)

        self.layoutChart = QHBoxLayout()
        self.layoutChart.setSpacing(0)
        self.layoutChart.setObjectName(u"layoutChart")

        self.verticalLayout_32.addLayout(self.layoutChart)

        self.groupBox_14 = QGroupBox(self.tab_debugging)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setMaximumSize(QSize(16777215, 100))
        self.groupBox_14.setStyleSheet(u"QLabel {\n"
"	font-size: 12px;\n"
"}")
        self.pushButtonClearAverages = QPushButton(self.groupBox_14)
        self.pushButtonClearAverages.setObjectName(u"pushButtonClearAverages")
        self.pushButtonClearAverages.setGeometry(QRect(1040, 70, 101, 25))
        self.label_71 = QLabel(self.groupBox_14)
        self.label_71.setObjectName(u"label_71")
        self.label_71.setGeometry(QRect(10, 35, 67, 17))
        self.label_72 = QLabel(self.groupBox_14)
        self.label_72.setObjectName(u"label_72")
        self.label_72.setGeometry(QRect(70, 35, 67, 17))
        self.label_73 = QLabel(self.groupBox_14)
        self.label_73.setObjectName(u"label_73")
        self.label_73.setGeometry(QRect(10, 50, 67, 17))
        self.label_74 = QLabel(self.groupBox_14)
        self.label_74.setObjectName(u"label_74")
        self.label_74.setGeometry(QRect(10, 65, 67, 17))
        self.label_75 = QLabel(self.groupBox_14)
        self.label_75.setObjectName(u"label_75")
        self.label_75.setGeometry(QRect(10, 80, 51, 17))
        self.labelADC0Avg = QLabel(self.groupBox_14)
        self.labelADC0Avg.setObjectName(u"labelADC0Avg")
        self.labelADC0Avg.setGeometry(QRect(140, 35, 51, 17))
        self.labelADC0Max = QLabel(self.groupBox_14)
        self.labelADC0Max.setObjectName(u"labelADC0Max")
        self.labelADC0Max.setGeometry(QRect(240, 35, 51, 17))
        self.label_78 = QLabel(self.groupBox_14)
        self.label_78.setObjectName(u"label_78")
        self.label_78.setGeometry(QRect(200, 35, 31, 17))
        self.labelADC0Min = QLabel(self.groupBox_14)
        self.labelADC0Min.setObjectName(u"labelADC0Min")
        self.labelADC0Min.setGeometry(QRect(340, 35, 51, 17))
        self.label_80 = QLabel(self.groupBox_14)
        self.label_80.setObjectName(u"label_80")
        self.label_80.setGeometry(QRect(300, 35, 31, 17))
        self.label_85 = QLabel(self.groupBox_14)
        self.label_85.setObjectName(u"label_85")
        self.label_85.setGeometry(QRect(520, 35, 67, 17))
        self.label_92 = QLabel(self.groupBox_14)
        self.label_92.setObjectName(u"label_92")
        self.label_92.setGeometry(QRect(520, 50, 67, 17))
        self.label_99 = QLabel(self.groupBox_14)
        self.label_99.setObjectName(u"label_99")
        self.label_99.setGeometry(QRect(520, 65, 67, 17))
        self.label_106 = QLabel(self.groupBox_14)
        self.label_106.setObjectName(u"label_106")
        self.label_106.setGeometry(QRect(520, 80, 51, 17))
        self.labelADC1Avg = QLabel(self.groupBox_14)
        self.labelADC1Avg.setObjectName(u"labelADC1Avg")
        self.labelADC1Avg.setGeometry(QRect(140, 50, 51, 17))
        self.labelADC1Max = QLabel(self.groupBox_14)
        self.labelADC1Max.setObjectName(u"labelADC1Max")
        self.labelADC1Max.setGeometry(QRect(240, 50, 51, 17))
        self.labelADC1Min = QLabel(self.groupBox_14)
        self.labelADC1Min.setObjectName(u"labelADC1Min")
        self.labelADC1Min.setGeometry(QRect(340, 50, 51, 17))
        self.label_76 = QLabel(self.groupBox_14)
        self.label_76.setObjectName(u"label_76")
        self.label_76.setGeometry(QRect(70, 50, 67, 17))
        self.label_81 = QLabel(self.groupBox_14)
        self.label_81.setObjectName(u"label_81")
        self.label_81.setGeometry(QRect(300, 50, 31, 17))
        self.label_79 = QLabel(self.groupBox_14)
        self.label_79.setObjectName(u"label_79")
        self.label_79.setGeometry(QRect(200, 50, 31, 17))
        self.labelADC2Avg = QLabel(self.groupBox_14)
        self.labelADC2Avg.setObjectName(u"labelADC2Avg")
        self.labelADC2Avg.setGeometry(QRect(140, 65, 51, 17))
        self.labelADC2Max = QLabel(self.groupBox_14)
        self.labelADC2Max.setObjectName(u"labelADC2Max")
        self.labelADC2Max.setGeometry(QRect(240, 65, 51, 17))
        self.labelADC2Min = QLabel(self.groupBox_14)
        self.labelADC2Min.setObjectName(u"labelADC2Min")
        self.labelADC2Min.setGeometry(QRect(340, 65, 51, 17))
        self.label_77 = QLabel(self.groupBox_14)
        self.label_77.setObjectName(u"label_77")
        self.label_77.setGeometry(QRect(70, 65, 67, 17))
        self.label_82 = QLabel(self.groupBox_14)
        self.label_82.setObjectName(u"label_82")
        self.label_82.setGeometry(QRect(300, 65, 31, 17))
        self.label_83 = QLabel(self.groupBox_14)
        self.label_83.setObjectName(u"label_83")
        self.label_83.setGeometry(QRect(200, 65, 31, 17))
        self.labelADC3Avg = QLabel(self.groupBox_14)
        self.labelADC3Avg.setObjectName(u"labelADC3Avg")
        self.labelADC3Avg.setGeometry(QRect(140, 80, 51, 17))
        self.labelADC3Max = QLabel(self.groupBox_14)
        self.labelADC3Max.setObjectName(u"labelADC3Max")
        self.labelADC3Max.setGeometry(QRect(240, 80, 51, 17))
        self.labelADC3Min = QLabel(self.groupBox_14)
        self.labelADC3Min.setObjectName(u"labelADC3Min")
        self.labelADC3Min.setGeometry(QRect(340, 80, 51, 17))
        self.label_84 = QLabel(self.groupBox_14)
        self.label_84.setObjectName(u"label_84")
        self.label_84.setGeometry(QRect(70, 80, 51, 17))
        self.label_86 = QLabel(self.groupBox_14)
        self.label_86.setObjectName(u"label_86")
        self.label_86.setGeometry(QRect(300, 80, 31, 17))
        self.label_87 = QLabel(self.groupBox_14)
        self.label_87.setObjectName(u"label_87")
        self.label_87.setGeometry(QRect(200, 80, 31, 17))
        self.labelADC5Avg = QLabel(self.groupBox_14)
        self.labelADC5Avg.setObjectName(u"labelADC5Avg")
        self.labelADC5Avg.setGeometry(QRect(650, 50, 51, 17))
        self.labelADC5Max = QLabel(self.groupBox_14)
        self.labelADC5Max.setObjectName(u"labelADC5Max")
        self.labelADC5Max.setGeometry(QRect(750, 50, 51, 17))
        self.labelADC5Min = QLabel(self.groupBox_14)
        self.labelADC5Min.setObjectName(u"labelADC5Min")
        self.labelADC5Min.setGeometry(QRect(850, 50, 51, 17))
        self.label_91 = QLabel(self.groupBox_14)
        self.label_91.setObjectName(u"label_91")
        self.label_91.setGeometry(QRect(580, 50, 67, 17))
        self.label_93 = QLabel(self.groupBox_14)
        self.label_93.setObjectName(u"label_93")
        self.label_93.setGeometry(QRect(810, 50, 31, 17))
        self.label_94 = QLabel(self.groupBox_14)
        self.label_94.setObjectName(u"label_94")
        self.label_94.setGeometry(QRect(710, 50, 31, 17))
        self.labelADC6Avg = QLabel(self.groupBox_14)
        self.labelADC6Avg.setObjectName(u"labelADC6Avg")
        self.labelADC6Avg.setGeometry(QRect(650, 65, 51, 17))
        self.labelADC6Max = QLabel(self.groupBox_14)
        self.labelADC6Max.setObjectName(u"labelADC6Max")
        self.labelADC6Max.setGeometry(QRect(750, 65, 51, 17))
        self.labelADC6Min = QLabel(self.groupBox_14)
        self.labelADC6Min.setObjectName(u"labelADC6Min")
        self.labelADC6Min.setGeometry(QRect(850, 65, 51, 17))
        self.label_95 = QLabel(self.groupBox_14)
        self.label_95.setObjectName(u"label_95")
        self.label_95.setGeometry(QRect(580, 65, 67, 17))
        self.label_96 = QLabel(self.groupBox_14)
        self.label_96.setObjectName(u"label_96")
        self.label_96.setGeometry(QRect(810, 65, 31, 17))
        self.label_97 = QLabel(self.groupBox_14)
        self.label_97.setObjectName(u"label_97")
        self.label_97.setGeometry(QRect(710, 65, 31, 17))
        self.labelADC7Avg = QLabel(self.groupBox_14)
        self.labelADC7Avg.setObjectName(u"labelADC7Avg")
        self.labelADC7Avg.setGeometry(QRect(650, 80, 51, 17))
        self.labelADC7Max = QLabel(self.groupBox_14)
        self.labelADC7Max.setObjectName(u"labelADC7Max")
        self.labelADC7Max.setGeometry(QRect(750, 80, 51, 17))
        self.labelADC7Min = QLabel(self.groupBox_14)
        self.labelADC7Min.setObjectName(u"labelADC7Min")
        self.labelADC7Min.setGeometry(QRect(850, 80, 51, 17))
        self.label_98 = QLabel(self.groupBox_14)
        self.label_98.setObjectName(u"label_98")
        self.label_98.setGeometry(QRect(580, 80, 51, 17))
        self.label_100 = QLabel(self.groupBox_14)
        self.label_100.setObjectName(u"label_100")
        self.label_100.setGeometry(QRect(810, 80, 31, 17))
        self.label_101 = QLabel(self.groupBox_14)
        self.label_101.setObjectName(u"label_101")
        self.label_101.setGeometry(QRect(710, 80, 31, 17))
        self.labelADC4Min = QLabel(self.groupBox_14)
        self.labelADC4Min.setObjectName(u"labelADC4Min")
        self.labelADC4Min.setGeometry(QRect(850, 35, 50, 17))
        self.labelADC4Avg = QLabel(self.groupBox_14)
        self.labelADC4Avg.setObjectName(u"labelADC4Avg")
        self.labelADC4Avg.setGeometry(QRect(650, 35, 50, 17))
        self.labelADC4Max = QLabel(self.groupBox_14)
        self.labelADC4Max.setObjectName(u"labelADC4Max")
        self.labelADC4Max.setGeometry(QRect(750, 35, 50, 17))
        self.label_89 = QLabel(self.groupBox_14)
        self.label_89.setObjectName(u"label_89")
        self.label_89.setGeometry(QRect(810, 35, 31, 17))
        self.label_90 = QLabel(self.groupBox_14)
        self.label_90.setObjectName(u"label_90")
        self.label_90.setGeometry(QRect(710, 35, 31, 17))
        self.label_88 = QLabel(self.groupBox_14)
        self.label_88.setObjectName(u"label_88")
        self.label_88.setGeometry(QRect(580, 35, 67, 17))
        self.pushButtonTestAverages = QPushButton(self.groupBox_14)
        self.pushButtonTestAverages.setObjectName(u"pushButtonTestAverages")
        self.pushButtonTestAverages.setGeometry(QRect(1040, 40, 101, 25))
        self.label_102 = QLabel(self.groupBox_14)
        self.label_102.setObjectName(u"label_102")
        self.label_102.setGeometry(QRect(400, 35, 31, 17))
        self.labelADC0Diff = QLabel(self.groupBox_14)
        self.labelADC0Diff.setObjectName(u"labelADC0Diff")
        self.labelADC0Diff.setGeometry(QRect(440, 35, 51, 17))
        self.labelADC1Diff = QLabel(self.groupBox_14)
        self.labelADC1Diff.setObjectName(u"labelADC1Diff")
        self.labelADC1Diff.setGeometry(QRect(440, 50, 51, 17))
        self.label_103 = QLabel(self.groupBox_14)
        self.label_103.setObjectName(u"label_103")
        self.label_103.setGeometry(QRect(400, 50, 31, 17))
        self.labelADC2Diff = QLabel(self.groupBox_14)
        self.labelADC2Diff.setObjectName(u"labelADC2Diff")
        self.labelADC2Diff.setGeometry(QRect(440, 65, 51, 17))
        self.label_104 = QLabel(self.groupBox_14)
        self.label_104.setObjectName(u"label_104")
        self.label_104.setGeometry(QRect(400, 65, 31, 17))
        self.labelADC3Diff = QLabel(self.groupBox_14)
        self.labelADC3Diff.setObjectName(u"labelADC3Diff")
        self.labelADC3Diff.setGeometry(QRect(440, 80, 51, 17))
        self.label_105 = QLabel(self.groupBox_14)
        self.label_105.setObjectName(u"label_105")
        self.label_105.setGeometry(QRect(400, 80, 31, 17))
        self.label_107 = QLabel(self.groupBox_14)
        self.label_107.setObjectName(u"label_107")
        self.label_107.setGeometry(QRect(910, 65, 31, 17))
        self.labelADC4Diff = QLabel(self.groupBox_14)
        self.labelADC4Diff.setObjectName(u"labelADC4Diff")
        self.labelADC4Diff.setGeometry(QRect(950, 35, 51, 17))
        self.labelADC5Diff = QLabel(self.groupBox_14)
        self.labelADC5Diff.setObjectName(u"labelADC5Diff")
        self.labelADC5Diff.setGeometry(QRect(950, 50, 51, 17))
        self.label_108 = QLabel(self.groupBox_14)
        self.label_108.setObjectName(u"label_108")
        self.label_108.setGeometry(QRect(910, 35, 31, 17))
        self.labelADC7Diff = QLabel(self.groupBox_14)
        self.labelADC7Diff.setObjectName(u"labelADC7Diff")
        self.labelADC7Diff.setGeometry(QRect(950, 80, 51, 17))
        self.label_109 = QLabel(self.groupBox_14)
        self.label_109.setObjectName(u"label_109")
        self.label_109.setGeometry(QRect(910, 80, 31, 17))
        self.label_110 = QLabel(self.groupBox_14)
        self.label_110.setObjectName(u"label_110")
        self.label_110.setGeometry(QRect(910, 50, 31, 17))
        self.labelADC6Diff = QLabel(self.groupBox_14)
        self.labelADC6Diff.setObjectName(u"labelADC6Diff")
        self.labelADC6Diff.setGeometry(QRect(950, 65, 51, 17))

        self.verticalLayout_32.addWidget(self.groupBox_14)

        self.tabWidgetMain.addTab(self.tab_debugging, "")
        self.tab_software = QWidget()
        self.tab_software.setObjectName(u"tab_software")
        self.groupBox_11 = QGroupBox(self.tab_software)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setGeometry(QRect(20, 0, 231, 141))
        self.listWidgetTuningscheme = QListWidget(self.groupBox_11)
        self.listWidgetTuningscheme.setObjectName(u"listWidgetTuningscheme")
        self.listWidgetTuningscheme.setGeometry(QRect(0, 40, 231, 91))
        self.tabWidgetMain.addTab(self.tab_software, "")
        self.tab_temporary = QWidget()
        self.tab_temporary.setObjectName(u"tab_temporary")
        self.groupBox_16 = QGroupBox(self.tab_temporary)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.groupBox_16.setGeometry(QRect(10, 0, 1161, 361))
        self.groupBox_16.setStyleSheet(u"")
        self.progressBar_bch = QProgressBar(self.groupBox_16)
        self.progressBar_bch.setObjectName(u"progressBar_bch")
        self.progressBar_bch.setGeometry(QRect(120, 60, 61, 51))
        self.progressBar_bch.setStyleSheet(u"QProgressBar {\n"
"	color: black;\n"
"	font-weight: bold;\n"
"	text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: lightblue;\n"
"}")
        self.progressBar_bch.setMinimum(-48)
        self.progressBar_bch.setMaximum(48)
        self.progressBar_bch.setValue(6)
        self.progressBar_bch.setOrientation(Qt.Vertical)
        self.label_2 = QLabel(self.groupBox_16)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(120, 40, 61, 17))
        self.label_2.setStyleSheet(u"")
        self.label_4 = QLabel(self.groupBox_16)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 120, 61, 17))
        self.label_4.setStyleSheet(u"")
        self.progressBar_bchb = QProgressBar(self.groupBox_16)
        self.progressBar_bchb.setObjectName(u"progressBar_bchb")
        self.progressBar_bchb.setGeometry(QRect(10, 140, 61, 51))
        self.progressBar_bchb.setStyleSheet(u"QProgressBar {\n"
"	color: black;\n"
"	font-weight: bold;\n"
"	text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: lightblue;\n"
"}")
        self.progressBar_bchb.setMaximum(127)
        self.progressBar_bchb.setValue(48)
        self.progressBar_bchb.setOrientation(Qt.Vertical)
        self.label_5 = QLabel(self.groupBox_16)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 200, 61, 17))
        self.label_5.setStyleSheet(u"")
        self.progressBar_bchbn = QProgressBar(self.groupBox_16)
        self.progressBar_bchbn.setObjectName(u"progressBar_bchbn")
        self.progressBar_bchbn.setGeometry(QRect(10, 220, 61, 51))
        self.progressBar_bchbn.setStyleSheet(u"QProgressBar {\n"
"	color: black;\n"
"	font-weight: bold;\n"
"	text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: lightblue;\n"
"}")
        self.progressBar_bchbn.setMaximum(127)
        self.progressBar_bchbn.setValue(48)
        self.progressBar_bchbn.setOrientation(Qt.Vertical)
        self.label_6 = QLabel(self.groupBox_16)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(120, 160, 71, 17))
        self.label_6.setStyleSheet(u"")
        self.progressBar_ar1 = QProgressBar(self.groupBox_16)
        self.progressBar_ar1.setObjectName(u"progressBar_ar1")
        self.progressBar_ar1.setGeometry(QRect(120, 180, 61, 51))
        self.progressBar_ar1.setStyleSheet(u"QProgressBar {\n"
"	color: black;\n"
"	font-weight: bold;\n"
"	text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: lightblue;\n"
"}")
        self.progressBar_ar1.setMinimum(-48)
        self.progressBar_ar1.setMaximum(48)
        self.progressBar_ar1.setValue(0)
        self.progressBar_ar1.setOrientation(Qt.Vertical)
        self.progressBar_bchsh = QProgressBar(self.groupBox_16)
        self.progressBar_bchsh.setObjectName(u"progressBar_bchsh")
        self.progressBar_bchsh.setGeometry(QRect(340, 220, 61, 51))
        self.progressBar_bchsh.setStyleSheet(u"QProgressBar {\n"
"	color: black;\n"
"	font-weight: bold;\n"
"	text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: lightblue;\n"
"}")
        self.progressBar_bchsh.setMinimum(-32737)
        self.progressBar_bchsh.setMaximum(32767)
        self.progressBar_bchsh.setValue(6)
        self.progressBar_bchsh.setOrientation(Qt.Vertical)
        self.label_9 = QLabel(self.groupBox_16)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(340, 200, 61, 17))
        self.label_9.setStyleSheet(u"")
        self.progressBar_bchshr = QProgressBar(self.groupBox_16)
        self.progressBar_bchshr.setObjectName(u"progressBar_bchshr")
        self.progressBar_bchshr.setGeometry(QRect(340, 140, 61, 51))
        self.progressBar_bchshr.setStyleSheet(u"QProgressBar {\n"
"	color: black;\n"
"	font-weight: bold;\n"
"	text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: lightblue;\n"
"}")
        self.progressBar_bchshr.setMaximum(24)
        self.progressBar_bchshr.setValue(6)
        self.progressBar_bchshr.setOrientation(Qt.Vertical)
        self.label_12 = QLabel(self.groupBox_16)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(340, 120, 61, 17))
        self.label_12.setStyleSheet(u"")
        self.progressBar_bchs5 = QProgressBar(self.groupBox_16)
        self.progressBar_bchs5.setObjectName(u"progressBar_bchs5")
        self.progressBar_bchs5.setGeometry(QRect(450, 220, 61, 51))
        self.progressBar_bchs5.setStyleSheet(u"QProgressBar {\n"
"	color: black;\n"
"	font-weight: bold;\n"
"	text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: lightblue;\n"
"}")
        self.progressBar_bchs5.setMinimum(-32767)
        self.progressBar_bchs5.setMaximum(32767)
        self.progressBar_bchs5.setValue(6)
        self.progressBar_bchs5.setOrientation(Qt.Vertical)
        self.label_14 = QLabel(self.groupBox_16)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(450, 200, 61, 17))
        self.label_14.setStyleSheet(u"")
        self.label_24 = QLabel(self.groupBox_16)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(230, 160, 71, 17))
        self.label_24.setStyleSheet(u"")
        self.progressBar_bcha = QProgressBar(self.groupBox_16)
        self.progressBar_bcha.setObjectName(u"progressBar_bcha")
        self.progressBar_bcha.setGeometry(QRect(230, 180, 61, 51))
        self.progressBar_bcha.setStyleSheet(u"QProgressBar {\n"
"	color: black;\n"
"	font-weight: bold;\n"
"	text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: lightblue;\n"
"}")
        self.progressBar_bcha.setMinimum(-48)
        self.progressBar_bcha.setMaximum(48)
        self.progressBar_bcha.setValue(0)
        self.progressBar_bcha.setOrientation(Qt.Vertical)
        self.progressBar_ar2 = QProgressBar(self.groupBox_16)
        self.progressBar_ar2.setObjectName(u"progressBar_ar2")
        self.progressBar_ar2.setGeometry(QRect(230, 60, 61, 51))
        self.progressBar_ar2.setStyleSheet(u"QProgressBar {\n"
"	color: black;\n"
"	font-weight: bold;\n"
"	text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: lightblue;\n"
"}")
        self.progressBar_ar2.setMinimum(-48)
        self.progressBar_ar2.setMaximum(48)
        self.progressBar_ar2.setValue(0)
        self.progressBar_ar2.setOrientation(Qt.Vertical)
        self.label_31 = QLabel(self.groupBox_16)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setGeometry(QRect(230, 40, 71, 17))
        self.label_31.setStyleSheet(u"")
        self.progressBar_ar3 = QProgressBar(self.groupBox_16)
        self.progressBar_ar3.setObjectName(u"progressBar_ar3")
        self.progressBar_ar3.setGeometry(QRect(450, 60, 61, 51))
        self.progressBar_ar3.setStyleSheet(u"QProgressBar {\n"
"	color: black;\n"
"	font-weight: bold;\n"
"	text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: lightblue;\n"
"}")
        self.progressBar_ar3.setMaximum(700)
        self.progressBar_ar3.setValue(48)
        self.progressBar_ar3.setOrientation(Qt.Vertical)
        self.label_48 = QLabel(self.groupBox_16)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setGeometry(QRect(450, 40, 71, 17))
        self.label_48.setStyleSheet(u"")
        self.tabWidgetMain.addTab(self.tab_temporary, "")
        self.tab_nodeeditor = QWidget()
        self.tab_nodeeditor.setObjectName(u"tab_nodeeditor")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.tab_nodeeditor.sizePolicy().hasHeightForWidth())
        self.tab_nodeeditor.setSizePolicy(sizePolicy9)
        self.verticalLayout_5 = QVBoxLayout(self.tab_nodeeditor)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.nodeHeader = QHBoxLayout()
        self.nodeHeader.setSpacing(0)
        self.nodeHeader.setObjectName(u"nodeHeader")
        self.nodeHeader.setContentsMargins(0, 0, 0, 0)
        self.label_38 = QLabel(self.tab_nodeeditor)
        self.label_38.setObjectName(u"label_38")

        self.nodeHeader.addWidget(self.label_38)

        self.comboBox = QComboBox(self.tab_nodeeditor)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.nodeHeader.addWidget(self.comboBox)

        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.nodeHeader.addItem(self.horizontalSpacer_4)

        self.label_66 = QLabel(self.tab_nodeeditor)
        self.label_66.setObjectName(u"label_66")

        self.nodeHeader.addWidget(self.label_66)

        self.comboBox_2 = QComboBox(self.tab_nodeeditor)
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.nodeHeader.addWidget(self.comboBox_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.nodeHeader.addItem(self.horizontalSpacer_3)

        self.pushButtonOrganize = QPushButton(self.tab_nodeeditor)
        self.pushButtonOrganize.setObjectName(u"pushButtonOrganize")
        self.pushButtonOrganize.setMinimumSize(QSize(70, 0))
        self.pushButtonOrganize.setMaximumSize(QSize(100, 16777215))

        self.nodeHeader.addWidget(self.pushButtonOrganize)


        self.verticalLayout_5.addLayout(self.nodeHeader)

        self.nodeDetails = QVBoxLayout()
        self.nodeDetails.setSpacing(0)
        self.nodeDetails.setObjectName(u"nodeDetails")

        self.verticalLayout_5.addLayout(self.nodeDetails)

        self.nodeContainer = QVBoxLayout()
        self.nodeContainer.setSpacing(0)
        self.nodeContainer.setObjectName(u"nodeContainer")
        self.nodeContainer.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_5.addLayout(self.nodeContainer)

        self.tabWidgetMain.addTab(self.tab_nodeeditor, "")
        self.tab_plugins = QWidget()
        self.tab_plugins.setObjectName(u"tab_plugins")
        self.verticalLayout_31 = QVBoxLayout(self.tab_plugins)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.horizontalLayout_54 = QHBoxLayout()
        self.horizontalLayout_54.setObjectName(u"horizontalLayout_54")
        self.label_67 = QLabel(self.tab_plugins)
        self.label_67.setObjectName(u"label_67")
        self.label_67.setMaximumSize(QSize(130, 16777215))

        self.horizontalLayout_54.addWidget(self.label_67)

        self.comboBoxPlugins = QComboBox(self.tab_plugins)
        self.comboBoxPlugins.setObjectName(u"comboBoxPlugins")

        self.horizontalLayout_54.addWidget(self.comboBoxPlugins)

        self.pushButtonPluginsAdd = QPushButton(self.tab_plugins)
        self.pushButtonPluginsAdd.setObjectName(u"pushButtonPluginsAdd")
        self.pushButtonPluginsAdd.setMinimumSize(QSize(0, 0))
        self.pushButtonPluginsAdd.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_54.addWidget(self.pushButtonPluginsAdd)

        self.pushButtonPluginsRemove = QPushButton(self.tab_plugins)
        self.pushButtonPluginsRemove.setObjectName(u"pushButtonPluginsRemove")
        self.pushButtonPluginsRemove.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_54.addWidget(self.pushButtonPluginsRemove)

        self.pushButtonPluginsName = QPushButton(self.tab_plugins)
        self.pushButtonPluginsName.setObjectName(u"pushButtonPluginsName")
        self.pushButtonPluginsName.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_54.addWidget(self.pushButtonPluginsName)


        self.verticalLayout_31.addLayout(self.horizontalLayout_54)

        self.line_21 = QFrame(self.tab_plugins)
        self.line_21.setObjectName(u"line_21")
        self.line_21.setFrameShape(QFrame.Shape.HLine)
        self.line_21.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_31.addWidget(self.line_21)

        self.scrollPlugins = QScrollArea(self.tab_plugins)
        self.scrollPlugins.setObjectName(u"scrollPlugins")
        self.scrollPlugins.setFrameShape(QFrame.NoFrame)
        self.scrollPlugins.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollPlugins.setWidgetResizable(True)
        self.scrollPlugins.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollAreaContentsPlugins = QWidget()
        self.scrollAreaContentsPlugins.setObjectName(u"scrollAreaContentsPlugins")
        self.scrollAreaContentsPlugins.setGeometry(QRect(0, 0, 1146, 30))
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.scrollAreaContentsPlugins.sizePolicy().hasHeightForWidth())
        self.scrollAreaContentsPlugins.setSizePolicy(sizePolicy10)
        self.scrollAreaContentsPlugins.setMinimumSize(QSize(1146, 0))
        self.verticalLayoutPlugins = QVBoxLayout(self.scrollAreaContentsPlugins)
        self.verticalLayoutPlugins.setObjectName(u"verticalLayoutPlugins")
        self.verticalLayoutPlugins.setContentsMargins(0, 0, 0, 0)
        self.scrollPlugins.setWidget(self.scrollAreaContentsPlugins)

        self.verticalLayout_31.addWidget(self.scrollPlugins)

        self.tabWidgetMain.addTab(self.tab_plugins, "")

        self.baseMainLayout.addWidget(self.tabWidgetMain)


        self.verticalLayout.addLayout(self.baseMainLayout)


        self.retranslateUi(Widget)

        self.tabWidgetMain.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Ekdahl FAR Configuration utility", None))
        self.pushButtonConnectDisconnect.setText(QCoreApplication.translate("Widget", u"Connect", None))
        self.pushButtonSaveToModule.setText(QCoreApplication.translate("Widget", u"Save settings", None))
        self.checkBoxContinuousSMData.setText(QCoreApplication.translate("Widget", u"Live update", None))
        self.pushButtonLoadFromModule.setText(QCoreApplication.translate("Widget", u"Refresh", None))
        self.pushButtonShowConsole.setText(QCoreApplication.translate("Widget", u"Show console", None))
        self.pushButtonShowReference.setText(QCoreApplication.translate("Widget", u"Show reference", None))
        self.pushButtonPreferences.setText(QCoreApplication.translate("Widget", u"Preferences", None))
        self.pushButtonToggleSidebar.setText(QCoreApplication.translate("Widget", u"Show/hide sidebar", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Widget", u"Pickup analysis", None))
        self.labelAnalyzeNote.setText(QCoreApplication.translate("Widget", u"A2", None))
        self.labelAnalyzeCents.setText(QCoreApplication.translate("Widget", u"50", None))
        self.labelAnalyzeFreq.setText(QCoreApplication.translate("Widget", u"666.66", None))
        self.label_35.setText(QCoreApplication.translate("Widget", u"Hz", None))
        self.label_15.setText(QCoreApplication.translate("Widget", u"Cents", None))
        self.pushButtonPickupAnalyse.setText(QCoreApplication.translate("Widget", u"Analyse", None))
        self.groupBoxBasicTuningParameters.setTitle(QCoreApplication.translate("Widget", u"Pitch settings", None))
        self.label_7.setText(QCoreApplication.translate("Widget", u"Fundamental Frequency", None))
        self.label_8.setText(QCoreApplication.translate("Widget", u"Map to key", None))
        self.comboBoxFundamentalFrequency.setItemText(0, QCoreApplication.translate("Widget", u"A - 440.00Hz", None))

        self.pushButtonDetectFundamental.setText(QCoreApplication.translate("Widget", u"Detect", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("Widget", u"Auto calibrations", None))
        self.pushButtonCalibrateAll.setText(QCoreApplication.translate("Widget", u"Calibrate all", None))
        self.pushButtonCalibratePressure.setText(QCoreApplication.translate("Widget", u"Cal. Pressure", None))
        self.pushButtonCalibrateMute.setText(QCoreApplication.translate("Widget", u"Cal. Mute", None))
        self.pushButtonCalibrateHammer.setText(QCoreApplication.translate("Widget", u"Cal. Hammer", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Widget", u"Harmonic series", None))
        self.label_16.setText(QCoreApplication.translate("Widget", u"Saved series'", None))
        self.pushButtonAddHarmonicList.setText(QCoreApplication.translate("Widget", u"Add", None))
        self.pushButtonRemoveHarmonicList.setText(QCoreApplication.translate("Widget", u"Remove", None))
        self.pushButtonRenameHarmonicList.setText(QCoreApplication.translate("Widget", u"Rename", None))
        self.pushButtonAddHarmonicListFile.setText(QCoreApplication.translate("Widget", u"Add file", None))
        self.pushButtonAddHarmonic.setText(QCoreApplication.translate("Widget", u"Add", None))
        self.pushButtonRemoveHarmonic.setText(QCoreApplication.translate("Widget", u"Remove", None))
        self.label_23.setText(QCoreApplication.translate("Widget", u"Preset", None))
        self.pushButtonLoadHarmonicPreset.setText(QCoreApplication.translate("Widget", u"Load preset", None))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tab_basic), QCoreApplication.translate("Widget", u"Basics", None))
        self.label_29.setText(QCoreApplication.translate("Widget", u"Configuration", None))
        self.pushButtonConfigurationAdd.setText(QCoreApplication.translate("Widget", u"add", None))
        self.pushButtonConfigurationRemove.setText(QCoreApplication.translate("Widget", u"remove", None))
        self.pushButtonConfigurationName.setText(QCoreApplication.translate("Widget", u"Rename", None))
        self.label_36.setText(QCoreApplication.translate("Widget", u"MIDI Channel", None))
        self.comboBoxMidiChannel.setItemText(0, QCoreApplication.translate("Widget", u"Omni", None))
        self.comboBoxMidiChannel.setItemText(1, QCoreApplication.translate("Widget", u"1", None))
        self.comboBoxMidiChannel.setItemText(2, QCoreApplication.translate("Widget", u"2", None))
        self.comboBoxMidiChannel.setItemText(3, QCoreApplication.translate("Widget", u"3", None))
        self.comboBoxMidiChannel.setItemText(4, QCoreApplication.translate("Widget", u"4", None))
        self.comboBoxMidiChannel.setItemText(5, QCoreApplication.translate("Widget", u"5", None))
        self.comboBoxMidiChannel.setItemText(6, QCoreApplication.translate("Widget", u"6", None))
        self.comboBoxMidiChannel.setItemText(7, QCoreApplication.translate("Widget", u"7", None))
        self.comboBoxMidiChannel.setItemText(8, QCoreApplication.translate("Widget", u"8", None))
        self.comboBoxMidiChannel.setItemText(9, QCoreApplication.translate("Widget", u"9", None))
        self.comboBoxMidiChannel.setItemText(10, QCoreApplication.translate("Widget", u"10", None))
        self.comboBoxMidiChannel.setItemText(11, QCoreApplication.translate("Widget", u"11", None))
        self.comboBoxMidiChannel.setItemText(12, QCoreApplication.translate("Widget", u"12", None))
        self.comboBoxMidiChannel.setItemText(13, QCoreApplication.translate("Widget", u"13", None))
        self.comboBoxMidiChannel.setItemText(14, QCoreApplication.translate("Widget", u"14", None))
        self.comboBoxMidiChannel.setItemText(15, QCoreApplication.translate("Widget", u"15", None))
        self.comboBoxMidiChannel.setItemText(16, QCoreApplication.translate("Widget", u"16", None))

        self.pushButtonMidiRestoreDefaults.setText(QCoreApplication.translate("Widget", u"Restore default midi commands", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Widget", u"Note on", None))
        self.label_44.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>Vel to hammer</p></body></html>", None))
        self.midiNoteOnSendMuteRest.setText(QCoreApplication.translate("Widget", u"Send mute rest", None))
        self.midiNoteOnHammerStaccato.setText(QCoreApplication.translate("Widget", u"Send hammer only when all new notes", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Widget", u"Note off", None))
        self.midiNoteOffSendFullMute.setText(QCoreApplication.translate("Widget", u"Send mute full mute", None))
        self.midiNoteOffMotorOff.setText(QCoreApplication.translate("Widget", u"Turn off motor", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("Widget", u"Sustain pedal", None))
        self.midiSustainSend.setItemText(0, QCoreApplication.translate("Widget", u"Nothing", None))
        self.midiSustainSend.setItemText(1, QCoreApplication.translate("Widget", u"MIDI & Mute sustain", None))
        self.midiSustainSend.setItemText(2, QCoreApplication.translate("Widget", u"MIDI sustain", None))
        self.midiSustainSend.setItemText(3, QCoreApplication.translate("Widget", u"Mute sustain", None))

        self.label_54.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>Send to</p></body></html>", None))
        self.midiSustainInvert.setText(QCoreApplication.translate("Widget", u"Invert", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Widget", u"Pitch bend", None))
        self.label_49.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>Scale</p></body></html>", None))
        self.midiPitchbendSend.setItemText(0, QCoreApplication.translate("Widget", u"Nothing", None))
        self.midiPitchbendSend.setItemText(1, QCoreApplication.translate("Widget", u"Harmonic shift", None))
        self.midiPitchbendSend.setItemText(2, QCoreApplication.translate("Widget", u"Pressure modifier", None))
        self.midiPitchbendSend.setItemText(3, QCoreApplication.translate("Widget", u"Pressure baseline", None))
        self.midiPitchbendSend.setItemText(4, QCoreApplication.translate("Widget", u"Mute position", None))
        self.midiPitchbendSend.setItemText(5, QCoreApplication.translate("Widget", u"Solenoid force multiplier", None))

        self.label_50.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>Send to</p></body></html>", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("Widget", u"Channel aftertouch", None))
        self.label_51.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>Scale</p></body></html>", None))
        self.midiChannelATSend.setItemText(0, QCoreApplication.translate("Widget", u"Nothing", None))
        self.midiChannelATSend.setItemText(1, QCoreApplication.translate("Widget", u"Pressure modifier", None))
        self.midiChannelATSend.setItemText(2, QCoreApplication.translate("Widget", u"Pressure baseline", None))
        self.midiChannelATSend.setItemText(3, QCoreApplication.translate("Widget", u"Mute position", None))
        self.midiChannelATSend.setItemText(4, QCoreApplication.translate("Widget", u"Solenoid force multiplier", None))
        self.midiChannelATSend.setItemText(5, QCoreApplication.translate("Widget", u"Harmonic shift", None))

        self.label_52.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>Send to</p></body></html>", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Widget", u"Poly aftertouch", None))
        self.label_45.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>Scale</p></body></html>", None))
        self.midiPolyATSend.setItemText(0, QCoreApplication.translate("Widget", u"Nothing", None))
        self.midiPolyATSend.setItemText(1, QCoreApplication.translate("Widget", u"Pressure modifier", None))
        self.midiPolyATSend.setItemText(2, QCoreApplication.translate("Widget", u"Pressure baseline", None))
        self.midiPolyATSend.setItemText(3, QCoreApplication.translate("Widget", u"Mute position", None))
        self.midiPolyATSend.setItemText(4, QCoreApplication.translate("Widget", u"Solenoid force multiplier", None))
        self.midiPolyATSend.setItemText(5, QCoreApplication.translate("Widget", u"Harmonic shift", None))

        self.label_46.setText(QCoreApplication.translate("Widget", u"<html><head/><body><p>Send to</p></body></html>", None))
        self.groupBox.setTitle(QCoreApplication.translate("Widget", u"Advanced configuration", None))
        self.label.setText(QCoreApplication.translate("Widget", u"MIDI Events", None))
        self.pushButtonCCAddLearn.setText(QCoreApplication.translate("Widget", u"+ Learn", None))
        self.pushButtonCCAdd.setText(QCoreApplication.translate("Widget", u"+", None))
        self.pushButtonCCRemove.setText(QCoreApplication.translate("Widget", u"-", None))
        self.label_11.setText(QCoreApplication.translate("Widget", u"Event Description", None))
        self.label_28.setText(QCoreApplication.translate("Widget", u"Event commands", None))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tab_midiSettings), QCoreApplication.translate("Widget", u"MIDI settings", None))
        self.groupBoxCV1.setTitle(QCoreApplication.translate("Widget", u"Harmonic (0)", None))
        self.labelCV1_2.setText(QCoreApplication.translate("Widget", u"Read value", None))
        self.labelCVHarmonic.setText(QCoreApplication.translate("Widget", u"0", None))
        self.labelCV1_4.setText(QCoreApplication.translate("Widget", u"CV Scale", None))
        self.labelCV1_5.setText(QCoreApplication.translate("Widget", u"Note offset", None))
        self.labelCV1_7.setText(QCoreApplication.translate("Widget", u"Zero point", None))
        self.label_53.setText(QCoreApplication.translate("Widget", u"Commands", None))
        self.groupBoxCV1_2.setTitle(QCoreApplication.translate("Widget", u"Harmonic shift (1)", None))
        self.labelCV1_8.setText(QCoreApplication.translate("Widget", u"Read value", None))
        self.labelCVHarmonicShift.setText(QCoreApplication.translate("Widget", u"0", None))
        self.labelCV1_10.setText(QCoreApplication.translate("Widget", u"CV Scale", None))
        self.labelCV1_11.setText(QCoreApplication.translate("Widget", u"Zero point", None))
        self.pushButtonCVHarmonicShiftZeroCalibrate.setText(QCoreApplication.translate("Widget", u"Calibrate", None))
        self.label_55.setText(QCoreApplication.translate("Widget", u"Commands", None))
        self.groupBoxCV1_7.setTitle(QCoreApplication.translate("Widget", u"Fine tune (2)", None))
        self.labelCV1_15.setText(QCoreApplication.translate("Widget", u"Read value", None))
        self.labelCVFineTune.setText(QCoreApplication.translate("Widget", u"0", None))
        self.labelCV1_13.setText(QCoreApplication.translate("Widget", u"Center", None))
        self.pushButtonCVFinetuneCalibrate.setText(QCoreApplication.translate("Widget", u"Calibrate", None))
        self.label_60.setText(QCoreApplication.translate("Widget", u"Commands", None))
        self.groupBoxCV1_4.setTitle(QCoreApplication.translate("Widget", u"Pressure (3)", None))
        self.labelCV1_20.setText(QCoreApplication.translate("Widget", u"Read value", None))
        self.labelCVPressure.setText(QCoreApplication.translate("Widget", u"0", None))
        self.label_57.setText(QCoreApplication.translate("Widget", u"Commands", None))
        self.groupBoxCV1_3.setTitle(QCoreApplication.translate("Widget", u"Mute (7)", None))
        self.labelCV1_14.setText(QCoreApplication.translate("Widget", u"Read value", None))
        self.labelCVMute.setText(QCoreApplication.translate("Widget", u"0", None))
        self.label_56.setText(QCoreApplication.translate("Widget", u"Commands", None))
        self.groupBoxCV1_8.setTitle(QCoreApplication.translate("Widget", u"Hammer scale (6)", None))
        self.labelCV1_16.setText(QCoreApplication.translate("Widget", u"Read value", None))
        self.labelCVHammerScale.setText(QCoreApplication.translate("Widget", u"0", None))
        self.label_61.setText(QCoreApplication.translate("Widget", u"Commands", None))
        self.groupBoxCV1_6.setTitle(QCoreApplication.translate("Widget", u"Gate (5)", None))
        self.labelCV1_32.setText(QCoreApplication.translate("Widget", u"Read value", None))
        self.labelCVGate.setText(QCoreApplication.translate("Widget", u"0", None))
        self.label_111.setText(QCoreApplication.translate("Widget", u"Threshold", None))
        self.checkBoxCVGateEngage.setText(QCoreApplication.translate("Widget", u"Engage / Disengage", None))
        self.checkBoxCVGatePowerMotor.setText(QCoreApplication.translate("Widget", u"Power motor", None))
        self.checkBoxCVGateHold.setText(QCoreApplication.translate("Widget", u"Hold", None))
        self.label_59.setText(QCoreApplication.translate("Widget", u"Commands", None))
        self.groupBoxCV1_5.setTitle(QCoreApplication.translate("Widget", u"Hammer trigger (4)", None))
        self.labelCV1_26.setText(QCoreApplication.translate("Widget", u"Read value", None))
        self.labelCVHammerTrigger.setText(QCoreApplication.translate("Widget", u"0", None))
        self.label_58.setText(QCoreApplication.translate("Widget", u"Commands", None))
        self.pushButtonResetADCSettings.setText(QCoreApplication.translate("Widget", u"Reset all CV commands", None))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tab_cvmapping), QCoreApplication.translate("Widget", u"CV Mapping", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("Widget", u"Bowing motor parameters", None))
        self.label_64.setText(QCoreApplication.translate("Widget", u"Int. err allowed", None))
        self.label_65.setText(QCoreApplication.translate("Widget", u"Max correct.", None))
        self.label_13.setText(QCoreApplication.translate("Widget", u"Motor max speed (Hz)", None))
        self.label_18.setText(QCoreApplication.translate("Widget", u"Motor voltage", None))
        self.label_40.setText(QCoreApplication.translate("Widget", u"PID Kp", None))
        self.pushButtonCalibrateMotorSpeed.setText(QCoreApplication.translate("Widget", u"Cal. Motor", None))
        self.label_17.setText(QCoreApplication.translate("Widget", u"Motor min speed (Hz)", None))
        self.label_37.setText(QCoreApplication.translate("Widget", u"Motor timeout", None))
        self.label_63.setText(QCoreApplication.translate("Widget", u"PID Kd", None))
        self.label_41.setText(QCoreApplication.translate("Widget", u"PID Ki", None))
        self.groupBoxBowParameters.setTitle(QCoreApplication.translate("Widget", u"Basic bow parameters", None))
        self.label_21.setText(QCoreApplication.translate("Widget", u"Bow rest position", None))
        self.pushButtonBowRestPressureTest.setText(QCoreApplication.translate("Widget", u"T", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Preset", None))
        self.pushButtonActuatorLoad.setText(QCoreApplication.translate("Widget", u"Load", None))
        self.pushButtonActuatorAdd.setText(QCoreApplication.translate("Widget", u"Add", None))
        self.pushButtonActuatorRemove.setText(QCoreApplication.translate("Widget", u"Remove", None))
        self.pushButtonActuatorRename.setText(QCoreApplication.translate("Widget", u"Rename", None))
        self.pushButtonRestBow.setText(QCoreApplication.translate("Widget", u"Reset pressure rest \n"
" and go to rest position", None))
        self.label_20.setText(QCoreApplication.translate("Widget", u"Bow engage position", None))
        self.pushButtonBowEngagePressureTest.setText(QCoreApplication.translate("Widget", u"T", None))
        self.label_19.setText(QCoreApplication.translate("Widget", u"Bow max position", None))
        self.pushButtonBowMaxPressureTest.setText(QCoreApplication.translate("Widget", u"T", None))
        self.groupBoxMuteParameters.setTitle(QCoreApplication.translate("Widget", u"Mute parameters", None))
        self.label_25.setText(QCoreApplication.translate("Widget", u"Rest position", None))
        self.pushButtonMuteRestTest.setText(QCoreApplication.translate("Widget", u"T", None))
        self.label_26.setText(QCoreApplication.translate("Widget", u"Full mute position", None))
        self.pushButtonMuteFullTest.setText(QCoreApplication.translate("Widget", u"T", None))
        self.label_27.setText(QCoreApplication.translate("Widget", u"Half mute position", None))
        self.pushButtonMuteHalfTest.setText(QCoreApplication.translate("Widget", u"T", None))
        self.label_42.setText(QCoreApplication.translate("Widget", u"Back off", None))
        self.label_43.setText(QCoreApplication.translate("Widget", u"mS", None))
        self.pushButtonRestMute.setText(QCoreApplication.translate("Widget", u"Reset rest position and go to rest position", None))
        self.groupBoxSolenoidParameters.setTitle(QCoreApplication.translate("Widget", u"Hammer parameters", None))
        self.label_32.setText(QCoreApplication.translate("Widget", u"Minimum force", None))
        self.pushButtonSolenoidMinForceTest.setText(QCoreApplication.translate("Widget", u"T", None))
        self.label_33.setText(QCoreApplication.translate("Widget", u"Maximum force", None))
        self.pushButtonSolenoidMaxForceTest.setText(QCoreApplication.translate("Widget", u"T", None))
        self.label_39.setText(QCoreApplication.translate("Widget", u"Engage duration", None))
        self.label_62.setText(QCoreApplication.translate("Widget", u"uS", None))
        self.pushButtonHammerDurationTest.setText(QCoreApplication.translate("Widget", u"T", None))
        self.pushButtonEngageHammer.setText(QCoreApplication.translate("Widget", u"Engage hammer", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Widget", u"Misc parameters", None))
        self.label_47.setText(QCoreApplication.translate("Widget", u"Harmonic shift range", None))
        self.label_22.setText(QCoreApplication.translate("Widget", u"Selected Module", None))
        self.pushButtonHomeBow.setText(QCoreApplication.translate("Widget", u"Home bow", None))
        self.pushButtonHomeMute.setText(QCoreApplication.translate("Widget", u"Home mute", None))
        self.pushButtonResetAllSettings.setText(QCoreApplication.translate("Widget", u"Reset all settings", None))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tab_advanced), QCoreApplication.translate("Widget", u"Advanced", None))
        self.label_34.setText(QCoreApplication.translate("Widget", u"Set frequency", None))
        self.labelSetFrequency.setText(QCoreApplication.translate("Widget", u"???.?? Hz", None))
        self.label_10.setText(QCoreApplication.translate("Widget", u"Motor frequency", None))
        self.labelBowFrequency.setText(QCoreApplication.translate("Widget", u"110Hz / A2 - 0", None))
        self.label_30.setText(QCoreApplication.translate("Widget", u"Bow motor current", None))
        self.labelBowCurrent.setText(QCoreApplication.translate("Widget", u"1A", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("Widget", u"Averages", None))
        self.pushButtonClearAverages.setText(QCoreApplication.translate("Widget", u"Clear", None))
        self.label_71.setText(QCoreApplication.translate("Widget", u"ADC 0", None))
        self.label_72.setText(QCoreApplication.translate("Widget", u"Average", None))
        self.label_73.setText(QCoreApplication.translate("Widget", u"ADC 1", None))
        self.label_74.setText(QCoreApplication.translate("Widget", u"ADC 2", None))
        self.label_75.setText(QCoreApplication.translate("Widget", u"ADC 3", None))
        self.labelADC0Avg.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC0Max.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_78.setText(QCoreApplication.translate("Widget", u"Max", None))
        self.labelADC0Min.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_80.setText(QCoreApplication.translate("Widget", u"Min", None))
        self.label_85.setText(QCoreApplication.translate("Widget", u"ADC 4", None))
        self.label_92.setText(QCoreApplication.translate("Widget", u"ADC 5", None))
        self.label_99.setText(QCoreApplication.translate("Widget", u"ADC 6", None))
        self.label_106.setText(QCoreApplication.translate("Widget", u"ADC 7", None))
        self.labelADC1Avg.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC1Max.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC1Min.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_76.setText(QCoreApplication.translate("Widget", u"Average", None))
        self.label_81.setText(QCoreApplication.translate("Widget", u"Min", None))
        self.label_79.setText(QCoreApplication.translate("Widget", u"Max", None))
        self.labelADC2Avg.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC2Max.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC2Min.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_77.setText(QCoreApplication.translate("Widget", u"Average", None))
        self.label_82.setText(QCoreApplication.translate("Widget", u"Min", None))
        self.label_83.setText(QCoreApplication.translate("Widget", u"Max", None))
        self.labelADC3Avg.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC3Max.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC3Min.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_84.setText(QCoreApplication.translate("Widget", u"Average", None))
        self.label_86.setText(QCoreApplication.translate("Widget", u"Min", None))
        self.label_87.setText(QCoreApplication.translate("Widget", u"Max", None))
        self.labelADC5Avg.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC5Max.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC5Min.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_91.setText(QCoreApplication.translate("Widget", u"Average", None))
        self.label_93.setText(QCoreApplication.translate("Widget", u"Min", None))
        self.label_94.setText(QCoreApplication.translate("Widget", u"Max", None))
        self.labelADC6Avg.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC6Max.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC6Min.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_95.setText(QCoreApplication.translate("Widget", u"Average", None))
        self.label_96.setText(QCoreApplication.translate("Widget", u"Min", None))
        self.label_97.setText(QCoreApplication.translate("Widget", u"Max", None))
        self.labelADC7Avg.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC7Max.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC7Min.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_98.setText(QCoreApplication.translate("Widget", u"Average", None))
        self.label_100.setText(QCoreApplication.translate("Widget", u"Min", None))
        self.label_101.setText(QCoreApplication.translate("Widget", u"Max", None))
        self.labelADC4Min.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC4Avg.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC4Max.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_89.setText(QCoreApplication.translate("Widget", u"Min", None))
        self.label_90.setText(QCoreApplication.translate("Widget", u"Max", None))
        self.label_88.setText(QCoreApplication.translate("Widget", u"Average", None))
        self.pushButtonTestAverages.setText(QCoreApplication.translate("Widget", u"Initiate Test", None))
        self.label_102.setText(QCoreApplication.translate("Widget", u"Diff", None))
        self.labelADC0Diff.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC1Diff.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_103.setText(QCoreApplication.translate("Widget", u"Diff", None))
        self.labelADC2Diff.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_104.setText(QCoreApplication.translate("Widget", u"Diff", None))
        self.labelADC3Diff.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_105.setText(QCoreApplication.translate("Widget", u"Diff", None))
        self.label_107.setText(QCoreApplication.translate("Widget", u"Diff", None))
        self.labelADC4Diff.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.labelADC5Diff.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_108.setText(QCoreApplication.translate("Widget", u"Diff", None))
        self.labelADC7Diff.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.label_109.setText(QCoreApplication.translate("Widget", u"Diff", None))
        self.label_110.setText(QCoreApplication.translate("Widget", u"Diff", None))
        self.labelADC6Diff.setText(QCoreApplication.translate("Widget", u"65535", None))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tab_debugging), QCoreApplication.translate("Widget", u"Debugging", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("Widget", u"Tuning scheme", None))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tab_software), QCoreApplication.translate("Widget", u"Software settings", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("Widget", u"Bow frequency", None))
        self.progressBar_bch.setFormat(QCoreApplication.translate("Widget", u"%v", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"bch", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"bchb", None))
        self.progressBar_bchb.setFormat(QCoreApplication.translate("Widget", u"%v", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"bchbn", None))
        self.progressBar_bchbn.setFormat(QCoreApplication.translate("Widget", u"%v", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"Subtract", None))
        self.progressBar_ar1.setFormat(QCoreApplication.translate("Widget", u"%v", None))
        self.progressBar_bchsh.setFormat(QCoreApplication.translate("Widget", u"%v", None))
        self.label_9.setText(QCoreApplication.translate("Widget", u"bchsh", None))
        self.progressBar_bchshr.setFormat(QCoreApplication.translate("Widget", u"%v", None))
        self.label_12.setText(QCoreApplication.translate("Widget", u"bchshr", None))
        self.progressBar_bchs5.setFormat(QCoreApplication.translate("Widget", u"%v", None))
        self.label_14.setText(QCoreApplication.translate("Widget", u"bchs5", None))
        self.label_24.setText(QCoreApplication.translate("Widget", u"bcha", None))
        self.progressBar_bcha.setFormat(QCoreApplication.translate("Widget", u"%v", None))
        self.progressBar_ar2.setFormat(QCoreApplication.translate("Widget", u"%v", None))
        self.label_31.setText(QCoreApplication.translate("Widget", u"Harmonic", None))
        self.progressBar_ar3.setFormat(QCoreApplication.translate("Widget", u"%v", None))
        self.label_48.setText(QCoreApplication.translate("Widget", u"T. Freq", None))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tab_temporary), QCoreApplication.translate("Widget", u"Temporary", None))
        self.label_38.setText(QCoreApplication.translate("Widget", u"Filter by ", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Widget", u"None", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Widget", u"Source", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Widget", u"Destination", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Widget", u"Plugins", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Widget", u"Module", None))

        self.label_66.setText(QCoreApplication.translate("Widget", u"Show ", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("Widget", u"All", None))

        self.pushButtonOrganize.setText(QCoreApplication.translate("Widget", u"Organize", None))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tab_nodeeditor), QCoreApplication.translate("Widget", u"Nodes", None))
        self.label_67.setText(QCoreApplication.translate("Widget", u"Avaliable plugins", None))
        self.pushButtonPluginsAdd.setText(QCoreApplication.translate("Widget", u"Add", None))
        self.pushButtonPluginsRemove.setText(QCoreApplication.translate("Widget", u"Remove", None))
        self.pushButtonPluginsName.setText(QCoreApplication.translate("Widget", u"Name", None))
        self.tabWidgetMain.setTabText(self.tabWidgetMain.indexOf(self.tab_plugins), QCoreApplication.translate("Widget", u"Pluugins", None))
    # retranslateUi

