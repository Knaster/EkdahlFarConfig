# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plugin_mult.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form_Mult(object):
    def setupUi(self, Form_Mult):
        if not Form_Mult.objectName():
            Form_Mult.setObjectName(u"Form_Mult")
        Form_Mult.resize(1139, 203)
        self.verticalLayout = QVBoxLayout(Form_Mult)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainGroupBox = QGroupBox(Form_Mult)
        self.mainGroupBox.setObjectName(u"mainGroupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainGroupBox.sizePolicy().hasHeightForWidth())
        self.mainGroupBox.setSizePolicy(sizePolicy)
        self.mainGroupBox.setMinimumSize(QSize(1121, 0))
        self.mainLayout = QHBoxLayout(self.mainGroupBox)
        self.mainLayout.setObjectName(u"mainLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelAdder = QLabel(self.mainGroupBox)
        self.labelAdder.setObjectName(u"labelAdder")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelAdder.sizePolicy().hasHeightForWidth())
        self.labelAdder.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.labelAdder)

        self.pushButtonRemoveAdder = QPushButton(self.mainGroupBox)
        self.pushButtonRemoveAdder.setObjectName(u"pushButtonRemoveAdder")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButtonRemoveAdder.sizePolicy().hasHeightForWidth())
        self.pushButtonRemoveAdder.setSizePolicy(sizePolicy2)
        self.pushButtonRemoveAdder.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout.addWidget(self.pushButtonRemoveAdder)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.listAdders = QListWidget(self.mainGroupBox)
        self.listAdders.setObjectName(u"listAdders")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.listAdders.sizePolicy().hasHeightForWidth())
        self.listAdders.setSizePolicy(sizePolicy3)
        self.listAdders.setMinimumSize(QSize(0, 0))
        self.listAdders.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_4.addWidget(self.listAdders)


        self.mainLayout.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_2 = QSpacerItem(30, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.mainLayout.addItem(self.horizontalSpacer_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelRatios = QLabel(self.mainGroupBox)
        self.labelRatios.setObjectName(u"labelRatios")
        sizePolicy1.setHeightForWidth(self.labelRatios.sizePolicy().hasHeightForWidth())
        self.labelRatios.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.labelRatios)

        self.pushButtonRemoveRatio = QPushButton(self.mainGroupBox)
        self.pushButtonRemoveRatio.setObjectName(u"pushButtonRemoveRatio")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButtonRemoveRatio.sizePolicy().hasHeightForWidth())
        self.pushButtonRemoveRatio.setSizePolicy(sizePolicy4)
        self.pushButtonRemoveRatio.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_2.addWidget(self.pushButtonRemoveRatio)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.listRatios = QListWidget(self.mainGroupBox)
        self.listRatios.setObjectName(u"listRatios")
        sizePolicy3.setHeightForWidth(self.listRatios.sizePolicy().hasHeightForWidth())
        self.listRatios.setSizePolicy(sizePolicy3)
        self.listRatios.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_3.addWidget(self.listRatios)


        self.mainLayout.addLayout(self.verticalLayout_3)

        self.horizontalSpacer = QSpacerItem(30, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.mainLayout.addItem(self.horizontalSpacer)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.labelTarget = QLabel(self.mainGroupBox)
        self.labelTarget.setObjectName(u"labelTarget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.labelTarget.sizePolicy().hasHeightForWidth())
        self.labelTarget.setSizePolicy(sizePolicy5)

        self.verticalLayout_2.addWidget(self.labelTarget)

        self.textEditTarget = QLineEdit(self.mainGroupBox)
        self.textEditTarget.setObjectName(u"textEditTarget")
        sizePolicy4.setHeightForWidth(self.textEditTarget.sizePolicy().hasHeightForWidth())
        self.textEditTarget.setSizePolicy(sizePolicy4)
        self.textEditTarget.setMinimumSize(QSize(400, 0))

        self.verticalLayout_2.addWidget(self.textEditTarget)


        self.mainLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout.addWidget(self.mainGroupBox)


        self.retranslateUi(Form_Mult)

        QMetaObject.connectSlotsByName(Form_Mult)
    # setupUi

    def retranslateUi(self, Form_Mult):
        Form_Mult.setWindowTitle(QCoreApplication.translate("Form_Mult", u"Form", None))
        self.mainGroupBox.setTitle(QCoreApplication.translate("Form_Mult", u"Multiple input adder / multiplier", None))
        self.labelAdder.setText(QCoreApplication.translate("Form_Mult", u"Adders", None))
        self.pushButtonRemoveAdder.setText(QCoreApplication.translate("Form_Mult", u"Remove", None))
        self.labelRatios.setText(QCoreApplication.translate("Form_Mult", u"Ratios", None))
        self.pushButtonRemoveRatio.setText(QCoreApplication.translate("Form_Mult", u"Remove", None))
        self.labelTarget.setText(QCoreApplication.translate("Form_Mult", u"Target (use mltout)", None))
    # retranslateUi

