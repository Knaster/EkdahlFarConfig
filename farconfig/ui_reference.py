# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reference.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QSizePolicy, QTextEdit,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(583, 588)
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
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.plainTextEditCMVDescription = QTextEdit(Form)
        self.plainTextEditCMVDescription.setObjectName(u"plainTextEditCMVDescription")

        self.gridLayout.addWidget(self.plainTextEditCMVDescription, 1, 1, 1, 1)

        self.label_31 = QLabel(Form)
        self.label_31.setObjectName(u"label_31")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_31, 0, 1, 1, 1)

        self.listWidgetCommands = QTreeWidget(Form)
        self.listWidgetCommands.setObjectName(u"listWidgetCommands")
        self.listWidgetCommands.setColumnCount(2)
        self.listWidgetCommands.header().setVisible(True)
        self.listWidgetCommands.header().setDefaultSectionSize(300)

        self.gridLayout.addWidget(self.listWidgetCommands, 1, 0, 1, 1)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.lineEditReferenceSearch = QLineEdit(Form)
        self.lineEditReferenceSearch.setObjectName(u"lineEditReferenceSearch")

        self.gridLayout.addWidget(self.lineEditReferenceSearch, 2, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Command reference", None))
        self.label.setText(QCoreApplication.translate("Form", u"Search", None))
        self.label_31.setText(QCoreApplication.translate("Form", u"Description", None))
        ___qtreewidgetitem = self.listWidgetCommands.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"Short command", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Long command", None));
        self.label_6.setText(QCoreApplication.translate("Form", u"FAR Commands", None))
    # retranslateUi

