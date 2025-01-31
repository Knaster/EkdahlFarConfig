# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reference.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPlainTextEdit,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1000, 602)
        Form.setStyleSheet(u"QWidget {\n"
"	background-color: white;\n"
"	font-family: cantarell;\n"
"	font-size: 13px;\n"
"	color: black;\n"
"}")
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 2, 1)

        self.label_31 = QLabel(Form)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout.addWidget(self.label_31, 0, 1, 1, 1)

        self.listWidgetCommands = QListWidget(Form)
        self.listWidgetCommands.setObjectName(u"listWidgetCommands")
        self.listWidgetCommands.setDragEnabled(True)
        self.listWidgetCommands.setDragDropMode(QAbstractItemView.DragOnly)

        self.gridLayout.addWidget(self.listWidgetCommands, 2, 0, 1, 1)

        self.plainTextEditCMVDescription = QPlainTextEdit(Form)
        self.plainTextEditCMVDescription.setObjectName(u"plainTextEditCMVDescription")
        self.plainTextEditCMVDescription.setEnabled(True)

        self.gridLayout.addWidget(self.plainTextEditCMVDescription, 2, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Command reference", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"FAR Commands", None))
        self.label_31.setText(QCoreApplication.translate("Form", u"Description", None))
    # retranslateUi

