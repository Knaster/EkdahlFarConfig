# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plugin_ahdsr.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDial, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form_AHDSR(object):
    def setupUi(self, Form_AHDSR):
        if not Form_AHDSR.objectName():
            Form_AHDSR.setObjectName(u"Form_AHDSR")
        Form_AHDSR.resize(1139, 230)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form_AHDSR.sizePolicy().hasHeightForWidth())
        Form_AHDSR.setSizePolicy(sizePolicy)
        Form_AHDSR.setMinimumSize(QSize(300, 200))
        Form_AHDSR.setMaximumSize(QSize(16777215, 250))
        self.verticalLayout = QVBoxLayout(Form_AHDSR)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainGroupBox = QGroupBox(Form_AHDSR)
        self.mainGroupBox.setObjectName(u"mainGroupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mainGroupBox.sizePolicy().hasHeightForWidth())
        self.mainGroupBox.setSizePolicy(sizePolicy1)
        self.mainGroupBox.setMinimumSize(QSize(1121, 200))
        self.mainGroupBox.setMaximumSize(QSize(1121, 16777215))
        self.mainLayout = QHBoxLayout(self.mainGroupBox)
        self.mainLayout.setObjectName(u"mainLayout")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_116 = QLabel(self.mainGroupBox)
        self.label_116.setObjectName(u"label_116")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_116.sizePolicy().hasHeightForWidth())
        self.label_116.setSizePolicy(sizePolicy2)
        self.label_116.setMinimumSize(QSize(100, 20))
        self.label_116.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_116)

        self.dialAmplitude = QDial(self.mainGroupBox)
        self.dialAmplitude.setObjectName(u"dialAmplitude")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.dialAmplitude.sizePolicy().hasHeightForWidth())
        self.dialAmplitude.setSizePolicy(sizePolicy3)
        self.dialAmplitude.setMinimumSize(QSize(100, 60))
        self.dialAmplitude.setStyleSheet(u"QDial {\n"
"    background-color: #ffffff;\n"
"    border: 0px;\n"
"}")
        self.dialAmplitude.setMaximum(65535)
        self.dialAmplitude.setInvertedAppearance(False)
        self.dialAmplitude.setInvertedControls(False)
        self.dialAmplitude.setWrapping(False)

        self.verticalLayout_9.addWidget(self.dialAmplitude)


        self.mainLayout.addLayout(self.verticalLayout_9)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_69 = QLabel(self.mainGroupBox)
        self.label_69.setObjectName(u"label_69")
        sizePolicy2.setHeightForWidth(self.label_69.sizePolicy().hasHeightForWidth())
        self.label_69.setSizePolicy(sizePolicy2)
        self.label_69.setMinimumSize(QSize(100, 0))
        self.label_69.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_69)

        self.dialAttack = QDial(self.mainGroupBox)
        self.dialAttack.setObjectName(u"dialAttack")
        sizePolicy3.setHeightForWidth(self.dialAttack.sizePolicy().hasHeightForWidth())
        self.dialAttack.setSizePolicy(sizePolicy3)
        self.dialAttack.setMinimumSize(QSize(60, 60))
        self.dialAttack.setMaximum(65535)

        self.verticalLayout_8.addWidget(self.dialAttack)


        self.mainLayout.addLayout(self.verticalLayout_8)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_112 = QLabel(self.mainGroupBox)
        self.label_112.setObjectName(u"label_112")
        sizePolicy2.setHeightForWidth(self.label_112.sizePolicy().hasHeightForWidth())
        self.label_112.setSizePolicy(sizePolicy2)
        self.label_112.setMinimumSize(QSize(100, 0))
        self.label_112.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_112)

        self.dialHold = QDial(self.mainGroupBox)
        self.dialHold.setObjectName(u"dialHold")
        sizePolicy3.setHeightForWidth(self.dialHold.sizePolicy().hasHeightForWidth())
        self.dialHold.setSizePolicy(sizePolicy3)
        self.dialHold.setMinimumSize(QSize(100, 60))
        self.dialHold.setMaximum(65535)

        self.verticalLayout_7.addWidget(self.dialHold)


        self.mainLayout.addLayout(self.verticalLayout_7)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_114 = QLabel(self.mainGroupBox)
        self.label_114.setObjectName(u"label_114")
        sizePolicy2.setHeightForWidth(self.label_114.sizePolicy().hasHeightForWidth())
        self.label_114.setSizePolicy(sizePolicy2)
        self.label_114.setMinimumSize(QSize(100, 0))
        self.label_114.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_114)

        self.dialDecay = QDial(self.mainGroupBox)
        self.dialDecay.setObjectName(u"dialDecay")
        sizePolicy3.setHeightForWidth(self.dialDecay.sizePolicy().hasHeightForWidth())
        self.dialDecay.setSizePolicy(sizePolicy3)
        self.dialDecay.setMinimumSize(QSize(100, 60))
        self.dialDecay.setMaximum(65535)

        self.verticalLayout_6.addWidget(self.dialDecay)


        self.mainLayout.addLayout(self.verticalLayout_6)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_113 = QLabel(self.mainGroupBox)
        self.label_113.setObjectName(u"label_113")
        sizePolicy2.setHeightForWidth(self.label_113.sizePolicy().hasHeightForWidth())
        self.label_113.setSizePolicy(sizePolicy2)
        self.label_113.setMinimumSize(QSize(100, 0))
        self.label_113.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_113)

        self.dialSustain = QDial(self.mainGroupBox)
        self.dialSustain.setObjectName(u"dialSustain")
        sizePolicy3.setHeightForWidth(self.dialSustain.sizePolicy().hasHeightForWidth())
        self.dialSustain.setSizePolicy(sizePolicy3)
        self.dialSustain.setMinimumSize(QSize(100, 60))
        self.dialSustain.setMaximum(65535)

        self.verticalLayout_5.addWidget(self.dialSustain)


        self.mainLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_115 = QLabel(self.mainGroupBox)
        self.label_115.setObjectName(u"label_115")
        sizePolicy2.setHeightForWidth(self.label_115.sizePolicy().hasHeightForWidth())
        self.label_115.setSizePolicy(sizePolicy2)
        self.label_115.setMinimumSize(QSize(100, 0))
        self.label_115.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_115)

        self.dialRelease = QDial(self.mainGroupBox)
        self.dialRelease.setObjectName(u"dialRelease")
        sizePolicy3.setHeightForWidth(self.dialRelease.sizePolicy().hasHeightForWidth())
        self.dialRelease.setSizePolicy(sizePolicy3)
        self.dialRelease.setMinimumSize(QSize(100, 60))
        self.dialRelease.setMaximum(65535)

        self.verticalLayout_4.addWidget(self.dialRelease)


        self.mainLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.checkBoxEnabled = QCheckBox(self.mainGroupBox)
        self.checkBoxEnabled.setObjectName(u"checkBoxEnabled")
        sizePolicy3.setHeightForWidth(self.checkBoxEnabled.sizePolicy().hasHeightForWidth())
        self.checkBoxEnabled.setSizePolicy(sizePolicy3)

        self.verticalLayout_3.addWidget(self.checkBoxEnabled)

        self.checkBoxInverted = QCheckBox(self.mainGroupBox)
        self.checkBoxInverted.setObjectName(u"checkBoxInverted")
        sizePolicy3.setHeightForWidth(self.checkBoxInverted.sizePolicy().hasHeightForWidth())
        self.checkBoxInverted.setSizePolicy(sizePolicy3)

        self.verticalLayout_3.addWidget(self.checkBoxInverted)

        self.verticalSpacer_3 = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)


        self.mainLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.label_70 = QLabel(self.mainGroupBox)
        self.label_70.setObjectName(u"label_70")
        sizePolicy2.setHeightForWidth(self.label_70.sizePolicy().hasHeightForWidth())
        self.label_70.setSizePolicy(sizePolicy2)

        self.verticalLayout_2.addWidget(self.label_70)

        self.textEditTarget = QLineEdit(self.mainGroupBox)
        self.textEditTarget.setObjectName(u"textEditTarget")
        sizePolicy1.setHeightForWidth(self.textEditTarget.sizePolicy().hasHeightForWidth())
        self.textEditTarget.setSizePolicy(sizePolicy1)
        self.textEditTarget.setMinimumSize(QSize(300, 0))

        self.verticalLayout_2.addWidget(self.textEditTarget)

        self.label_117 = QLabel(self.mainGroupBox)
        self.label_117.setObjectName(u"label_117")
        sizePolicy2.setHeightForWidth(self.label_117.sizePolicy().hasHeightForWidth())
        self.label_117.setSizePolicy(sizePolicy2)
        self.label_117.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_2.addWidget(self.label_117)

        self.textEditReleaseTarget = QLineEdit(self.mainGroupBox)
        self.textEditReleaseTarget.setObjectName(u"textEditReleaseTarget")
        sizePolicy1.setHeightForWidth(self.textEditReleaseTarget.sizePolicy().hasHeightForWidth())
        self.textEditReleaseTarget.setSizePolicy(sizePolicy1)
        self.textEditReleaseTarget.setMinimumSize(QSize(300, 0))

        self.verticalLayout_2.addWidget(self.textEditReleaseTarget)

        self.verticalSpacer_4 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)


        self.mainLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout.addWidget(self.mainGroupBox)


        self.retranslateUi(Form_AHDSR)

        QMetaObject.connectSlotsByName(Form_AHDSR)
    # setupUi

    def retranslateUi(self, Form_AHDSR):
        Form_AHDSR.setWindowTitle(QCoreApplication.translate("Form_AHDSR", u"Form", None))
        self.mainGroupBox.setTitle(QCoreApplication.translate("Form_AHDSR", u"AHDSR", None))
        self.label_116.setText(QCoreApplication.translate("Form_AHDSR", u"Amplitude", None))
        self.label_69.setText(QCoreApplication.translate("Form_AHDSR", u"Attack", None))
        self.label_112.setText(QCoreApplication.translate("Form_AHDSR", u"Hold", None))
        self.label_114.setText(QCoreApplication.translate("Form_AHDSR", u"Decay", None))
        self.label_113.setText(QCoreApplication.translate("Form_AHDSR", u"Sustain", None))
        self.label_115.setText(QCoreApplication.translate("Form_AHDSR", u"Release", None))
        self.checkBoxEnabled.setText(QCoreApplication.translate("Form_AHDSR", u"Enabled", None))
        self.checkBoxInverted.setText(QCoreApplication.translate("Form_AHDSR", u"Inverted", None))
        self.label_70.setText(QCoreApplication.translate("Form_AHDSR", u"Target (use ahdsrout)", None))
        self.label_117.setText(QCoreApplication.translate("Form_AHDSR", u"Release target", None))
    # retranslateUi

