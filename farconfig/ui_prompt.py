# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'prompt.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(220, 336)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(0, 336))
        Form.setStyleSheet(u"QWidget {\n"
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
"")
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButtonClear = QPushButton(Form)
        self.pushButtonClear.setObjectName(u"pushButtonClear")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButtonClear.sizePolicy().hasHeightForWidth())
        self.pushButtonClear.setSizePolicy(sizePolicy1)
        self.pushButtonClear.setMinimumSize(QSize(94, 0))

        self.gridLayout.addWidget(self.pushButtonClear, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.plainTextEditSerialOutput = QPlainTextEdit(Form)
        self.plainTextEditSerialOutput.setObjectName(u"plainTextEditSerialOutput")
        self.plainTextEditSerialOutput.setMinimumSize(QSize(0, 100))
        self.plainTextEditSerialOutput.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.plainTextEditSerialOutput.setReadOnly(False)

        self.horizontalLayout.addWidget(self.plainTextEditSerialOutput)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButtonSend = QPushButton(Form)
        self.pushButtonSend.setObjectName(u"pushButtonSend")
        sizePolicy1.setHeightForWidth(self.pushButtonSend.sizePolicy().hasHeightForWidth())
        self.pushButtonSend.setSizePolicy(sizePolicy1)
        self.pushButtonSend.setMinimumSize(QSize(94, 0))

        self.gridLayout_2.addWidget(self.pushButtonSend, 0, 2, 1, 1)

        self.lineEditSend = QComboBox(Form)
        self.lineEditSend.setObjectName(u"lineEditSend")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEditSend.sizePolicy().hasHeightForWidth())
        self.lineEditSend.setSizePolicy(sizePolicy2)
        self.lineEditSend.setMinimumSize(QSize(100, 0))
        self.lineEditSend.setEditable(True)
        self.lineEditSend.setInsertPolicy(QComboBox.InsertAtTop)

        self.gridLayout_2.addWidget(self.lineEditSend, 0, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 2, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Console", None))
        self.pushButtonClear.setText(QCoreApplication.translate("Form", u"Clear", None))
        self.plainTextEditSerialOutput.setPlaceholderText("")
        self.pushButtonSend.setText(QCoreApplication.translate("Form", u"Send", None))
    # retranslateUi

