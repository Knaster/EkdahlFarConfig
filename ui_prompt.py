# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'prompt.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpinBox, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(821, 336)
        Form.setMinimumSize(QSize(529, 336))
        Form.setStyleSheet(u"QWidget {\n"
"	background-color: white;\n"
"	font-family: cantarell;\n"
"	font-size: 13px;\n"
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
"    subcontrol-position: top left; /* Moves the title to the top-l"
                        "eft corner */\n"
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
"")
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.plainTextEditSerialOutput = QPlainTextEdit(Form)
        self.plainTextEditSerialOutput.setObjectName(u"plainTextEditSerialOutput")
        self.plainTextEditSerialOutput.setMinimumSize(QSize(0, 100))
        self.plainTextEditSerialOutput.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.plainTextEditSerialOutput.setReadOnly(False)

        self.horizontalLayout.addWidget(self.plainTextEditSerialOutput)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.spinBoxLimitLines = QSpinBox(Form)
        self.spinBoxLimitLines.setObjectName(u"spinBoxLimitLines")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxLimitLines.sizePolicy().hasHeightForWidth())
        self.spinBoxLimitLines.setSizePolicy(sizePolicy)
        self.spinBoxLimitLines.setMaximum(10000)
        self.spinBoxLimitLines.setValue(5000)

        self.gridLayout.addWidget(self.spinBoxLimitLines, 1, 1, 1, 1)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_6, 1, 2, 1, 1)

        self.checkBoxDebugCursorFollow = QCheckBox(Form)
        self.checkBoxDebugCursorFollow.setObjectName(u"checkBoxDebugCursorFollow")
        self.checkBoxDebugCursorFollow.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.checkBoxDebugCursorFollow.sizePolicy().hasHeightForWidth())
        self.checkBoxDebugCursorFollow.setSizePolicy(sizePolicy1)
        self.checkBoxDebugCursorFollow.setChecked(True)

        self.gridLayout.addWidget(self.checkBoxDebugCursorFollow, 1, 3, 1, 1)

        self.pushButtonClear = QPushButton(Form)
        self.pushButtonClear.setObjectName(u"pushButtonClear")
        sizePolicy1.setHeightForWidth(self.pushButtonClear.sizePolicy().hasHeightForWidth())
        self.pushButtonClear.setSizePolicy(sizePolicy1)
        self.pushButtonClear.setMinimumSize(QSize(94, 0))

        self.gridLayout.addWidget(self.pushButtonClear, 1, 4, 1, 1)

        self.checkBoxLimitLines = QCheckBox(Form)
        self.checkBoxLimitLines.setObjectName(u"checkBoxLimitLines")
        sizePolicy1.setHeightForWidth(self.checkBoxLimitLines.sizePolicy().hasHeightForWidth())
        self.checkBoxLimitLines.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.checkBoxLimitLines, 0, 0, 2, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.groupBox_16 = QGroupBox(Form)
        self.groupBox_16.setObjectName(u"groupBox_16")
        sizePolicy.setHeightForWidth(self.groupBox_16.sizePolicy().hasHeightForWidth())
        self.groupBox_16.setSizePolicy(sizePolicy)
        self.groupBox_16.setMinimumSize(QSize(0, 140))
        self.groupBox_16.setMaximumSize(QSize(16777215, 140))
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_16)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.checkBoxFilterCommAck = QCheckBox(self.groupBox_16)
        self.checkBoxFilterCommAck.setObjectName(u"checkBoxFilterCommAck")
        self.checkBoxFilterCommAck.setEnabled(False)

        self.gridLayout_3.addWidget(self.checkBoxFilterCommAck, 0, 0, 1, 1)

        self.checkBoxFilterUndefined = QCheckBox(self.groupBox_16)
        self.checkBoxFilterUndefined.setObjectName(u"checkBoxFilterUndefined")
        self.checkBoxFilterUndefined.setEnabled(True)

        self.gridLayout_3.addWidget(self.checkBoxFilterUndefined, 0, 1, 1, 1)

        self.checkBoxFilterInfoRequest = QCheckBox(self.groupBox_16)
        self.checkBoxFilterInfoRequest.setObjectName(u"checkBoxFilterInfoRequest")
        self.checkBoxFilterInfoRequest.setEnabled(True)

        self.gridLayout_3.addWidget(self.checkBoxFilterInfoRequest, 0, 2, 1, 1)

        self.checkBoxFilterUSB = QCheckBox(self.groupBox_16)
        self.checkBoxFilterUSB.setObjectName(u"checkBoxFilterUSB")
        self.checkBoxFilterUSB.setEnabled(False)
        self.checkBoxFilterUSB.setCheckable(True)

        self.gridLayout_3.addWidget(self.checkBoxFilterUSB, 1, 0, 1, 1)

        self.checkBoxFilterPriority = QCheckBox(self.groupBox_16)
        self.checkBoxFilterPriority.setObjectName(u"checkBoxFilterPriority")
        self.checkBoxFilterPriority.setEnabled(True)

        self.gridLayout_3.addWidget(self.checkBoxFilterPriority, 1, 1, 1, 1)

        self.checkBoxFilterExpressionParser = QCheckBox(self.groupBox_16)
        self.checkBoxFilterExpressionParser.setObjectName(u"checkBoxFilterExpressionParser")
        self.checkBoxFilterExpressionParser.setEnabled(True)

        self.gridLayout_3.addWidget(self.checkBoxFilterExpressionParser, 1, 2, 1, 1)

        self.checkBoxFilterHardware = QCheckBox(self.groupBox_16)
        self.checkBoxFilterHardware.setObjectName(u"checkBoxFilterHardware")
        self.checkBoxFilterHardware.setEnabled(True)

        self.gridLayout_3.addWidget(self.checkBoxFilterHardware, 2, 0, 2, 1)

        self.checkBoxFilterError = QCheckBox(self.groupBox_16)
        self.checkBoxFilterError.setObjectName(u"checkBoxFilterError")
        self.checkBoxFilterError.setEnabled(True)

        self.gridLayout_3.addWidget(self.checkBoxFilterError, 2, 1, 1, 1)

        self.checkBoxFilterDebug = QCheckBox(self.groupBox_16)
        self.checkBoxFilterDebug.setObjectName(u"checkBoxFilterDebug")
        self.checkBoxFilterDebug.setEnabled(True)

        self.gridLayout_3.addWidget(self.checkBoxFilterDebug, 2, 2, 2, 1)

        self.checkBoxFilterOutput = QCheckBox(self.groupBox_16)
        self.checkBoxFilterOutput.setObjectName(u"checkBoxFilterOutput")
        self.checkBoxFilterOutput.setEnabled(False)

        self.gridLayout_3.addWidget(self.checkBoxFilterOutput, 3, 1, 1, 1)


        self.horizontalLayout_3.addLayout(self.gridLayout_3)


        self.gridLayout_4.addWidget(self.groupBox_16, 2, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lineEditSend = QLineEdit(Form)
        self.lineEditSend.setObjectName(u"lineEditSend")

        self.gridLayout_2.addWidget(self.lineEditSend, 0, 0, 1, 1)

        self.pushButtonSend = QPushButton(Form)
        self.pushButtonSend.setObjectName(u"pushButtonSend")
        sizePolicy1.setHeightForWidth(self.pushButtonSend.sizePolicy().hasHeightForWidth())
        self.pushButtonSend.setSizePolicy(sizePolicy1)
        self.pushButtonSend.setMinimumSize(QSize(94, 0))

        self.gridLayout_2.addWidget(self.pushButtonSend, 0, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 3, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Console", None))
        self.plainTextEditSerialOutput.setPlaceholderText("")
        self.label_6.setText(QCoreApplication.translate("Form", u"Lines", None))
        self.checkBoxDebugCursorFollow.setText(QCoreApplication.translate("Form", u"Cursor follow", None))
        self.pushButtonClear.setText(QCoreApplication.translate("Form", u"Clear", None))
        self.checkBoxLimitLines.setText(QCoreApplication.translate("Form", u"Keep maximum of", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("Form", u"Filter messages", None))
        self.checkBoxFilterCommAck.setText(QCoreApplication.translate("Form", u"Command aknowledge", None))
        self.checkBoxFilterUndefined.setText(QCoreApplication.translate("Form", u"Undefined messages", None))
        self.checkBoxFilterInfoRequest.setText(QCoreApplication.translate("Form", u"Info Requests", None))
        self.checkBoxFilterUSB.setText(QCoreApplication.translate("Form", u"USB Commands", None))
        self.checkBoxFilterPriority.setText(QCoreApplication.translate("Form", u"Priority messages", None))
        self.checkBoxFilterExpressionParser.setText(QCoreApplication.translate("Form", u"Expression parser", None))
        self.checkBoxFilterHardware.setText(QCoreApplication.translate("Form", u"Hardware messages", None))
        self.checkBoxFilterError.setText(QCoreApplication.translate("Form", u"Error messages", None))
        self.checkBoxFilterDebug.setText(QCoreApplication.translate("Form", u"Debug messages", None))
        self.checkBoxFilterOutput.setText(QCoreApplication.translate("Form", u"Output messages", None))
        self.pushButtonSend.setText(QCoreApplication.translate("Form", u"Send", None))
    # retranslateUi

