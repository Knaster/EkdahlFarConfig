# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plugin_numbermap.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form_NumberMap(object):
    def setupUi(self, Form_NumberMap):
        if not Form_NumberMap.objectName():
            Form_NumberMap.setObjectName(u"Form_NumberMap")
        Form_NumberMap.resize(1139, 268)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form_NumberMap.sizePolicy().hasHeightForWidth())
        Form_NumberMap.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Form_NumberMap)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainGroupBox = QGroupBox(Form_NumberMap)
        self.mainGroupBox.setObjectName(u"mainGroupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mainGroupBox.sizePolicy().hasHeightForWidth())
        self.mainGroupBox.setSizePolicy(sizePolicy1)
        self.mainGroupBox.setMinimumSize(QSize(1121, 250))
        self.mainLayout = QVBoxLayout(self.mainGroupBox)
        self.mainLayout.setObjectName(u"mainLayout")
        self.layoutSliders = QHBoxLayout()
        self.layoutSliders.setObjectName(u"layoutSliders")
        self.layoutRange = QVBoxLayout()
        self.layoutRange.setObjectName(u"layoutRange")
        self.label_4 = QLabel(self.mainGroupBox)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setMinimumSize(QSize(71, 0))
        self.label_4.setMaximumSize(QSize(71, 16777215))
        self.label_4.setAlignment(Qt.AlignCenter)

        self.layoutRange.addWidget(self.label_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.mainGroupBox)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(32, 0))
        self.label_3.setMaximumSize(QSize(50, 16777215))

        self.verticalLayout_3.addWidget(self.label_3)

        self.label_2 = QLabel(self.mainGroupBox)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        self.label_2.setMaximumSize(QSize(50, 16777215))

        self.verticalLayout_3.addWidget(self.label_2)

        self.label = QLabel(self.mainGroupBox)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(0, 17))
        self.label.setMaximumSize(QSize(50, 17))

        self.verticalLayout_3.addWidget(self.label)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.sliderRange = QSlider(self.mainGroupBox)
        self.sliderRange.setObjectName(u"sliderRange")
        self.sliderRange.setMinimumSize(QSize(15, 0))
        self.sliderRange.setMaximumSize(QSize(15, 16777215))
        self.sliderRange.setMaximum(2)
        self.sliderRange.setPageStep(1)
        self.sliderRange.setSliderPosition(2)
        self.sliderRange.setOrientation(Qt.Vertical)

        self.horizontalLayout_3.addWidget(self.sliderRange)


        self.layoutRange.addLayout(self.horizontalLayout_3)


        self.layoutSliders.addLayout(self.layoutRange)

        self.layoutScale = QVBoxLayout()
        self.layoutScale.setObjectName(u"layoutScale")
        self.label_5 = QLabel(self.mainGroupBox)
        self.label_5.setObjectName(u"label_5")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy3)
        self.label_5.setMinimumSize(QSize(71, 0))
        self.label_5.setMaximumSize(QSize(71, 16777215))
        self.label_5.setAlignment(Qt.AlignCenter)

        self.layoutScale.addWidget(self.label_5)

        self.sliderScale = QSlider(self.mainGroupBox)
        self.sliderScale.setObjectName(u"sliderScale")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.sliderScale.sizePolicy().hasHeightForWidth())
        self.sliderScale.setSizePolicy(sizePolicy4)
        self.sliderScale.setMinimumSize(QSize(71, 0))
        self.sliderScale.setMaximumSize(QSize(71, 16777215))
        self.sliderScale.setMaximum(65535)
        self.sliderScale.setOrientation(Qt.Vertical)

        self.layoutScale.addWidget(self.sliderScale)


        self.layoutSliders.addLayout(self.layoutScale)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutSliders.addItem(self.horizontalSpacer_2)


        self.mainLayout.addLayout(self.layoutSliders)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelTarget = QLabel(self.mainGroupBox)
        self.labelTarget.setObjectName(u"labelTarget")

        self.horizontalLayout.addWidget(self.labelTarget)

        self.textEditTarget = QLineEdit(self.mainGroupBox)
        self.textEditTarget.setObjectName(u"textEditTarget")
        self.textEditTarget.setMinimumSize(QSize(600, 0))

        self.horizontalLayout.addWidget(self.textEditTarget)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.labelNumberTitle = QLabel(self.mainGroupBox)
        self.labelNumberTitle.setObjectName(u"labelNumberTitle")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.labelNumberTitle.sizePolicy().hasHeightForWidth())
        self.labelNumberTitle.setSizePolicy(sizePolicy5)

        self.horizontalLayout.addWidget(self.labelNumberTitle)

        self.pushButtonAdd = QPushButton(self.mainGroupBox)
        self.pushButtonAdd.setObjectName(u"pushButtonAdd")
        sizePolicy1.setHeightForWidth(self.pushButtonAdd.sizePolicy().hasHeightForWidth())
        self.pushButtonAdd.setSizePolicy(sizePolicy1)
        self.pushButtonAdd.setMinimumSize(QSize(80, 0))

        self.horizontalLayout.addWidget(self.pushButtonAdd)

        self.pushButtonRemove = QPushButton(self.mainGroupBox)
        self.pushButtonRemove.setObjectName(u"pushButtonRemove")
        sizePolicy1.setHeightForWidth(self.pushButtonRemove.sizePolicy().hasHeightForWidth())
        self.pushButtonRemove.setSizePolicy(sizePolicy1)
        self.pushButtonRemove.setMinimumSize(QSize(80, 0))

        self.horizontalLayout.addWidget(self.pushButtonRemove)


        self.mainLayout.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.mainGroupBox)


        self.retranslateUi(Form_NumberMap)

        QMetaObject.connectSlotsByName(Form_NumberMap)
    # setupUi

    def retranslateUi(self, Form_NumberMap):
        Form_NumberMap.setWindowTitle(QCoreApplication.translate("Form_NumberMap", u"Form", None))
        self.mainGroupBox.setTitle(QCoreApplication.translate("Form_NumberMap", u"Number map", None))
        self.label_4.setText(QCoreApplication.translate("Form_NumberMap", u"Range", None))
        self.label_3.setText(QCoreApplication.translate("Form_NumberMap", u"Full", None))
        self.label_2.setText(QCoreApplication.translate("Form_NumberMap", u"MIDI", None))
        self.label.setText(QCoreApplication.translate("Form_NumberMap", u"Octave", None))
        self.label_5.setText(QCoreApplication.translate("Form_NumberMap", u"Scale", None))
        self.labelTarget.setText(QCoreApplication.translate("Form_NumberMap", u"Target(use nmout)", None))
        self.labelNumberTitle.setText(QCoreApplication.translate("Form_NumberMap", u"Number", None))
        self.pushButtonAdd.setText(QCoreApplication.translate("Form_NumberMap", u"Add", None))
        self.pushButtonRemove.setText(QCoreApplication.translate("Form_NumberMap", u"Remove", None))
    # retranslateUi

