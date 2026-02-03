# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plugin_lfo.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDial, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QSizePolicy, QSlider, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form_LFO(object):
    def setupUi(self, Form_LFO):
        if not Form_LFO.objectName():
            Form_LFO.setObjectName(u"Form_LFO")
        Form_LFO.resize(1139, 178)
        self.verticalLayout = QVBoxLayout(Form_LFO)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainGroupBox = QGroupBox(Form_LFO)
        self.mainGroupBox.setObjectName(u"mainGroupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainGroupBox.sizePolicy().hasHeightForWidth())
        self.mainGroupBox.setSizePolicy(sizePolicy)
        self.mainGroupBox.setMinimumSize(QSize(1121, 160))
        self.verticalLayout_5 = QVBoxLayout(self.mainGroupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.mainLayout = QGridLayout()
        self.mainLayout.setObjectName(u"mainLayout")
        self.label_69 = QLabel(self.mainGroupBox)
        self.label_69.setObjectName(u"label_69")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_69.sizePolicy().hasHeightForWidth())
        self.label_69.setSizePolicy(sizePolicy1)
        self.label_69.setMinimumSize(QSize(140, 0))
        self.label_69.setMaximumSize(QSize(140, 16777215))
        self.label_69.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.label_69, 0, 1, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.checkBoxEnabled = QCheckBox(self.mainGroupBox)
        self.checkBoxEnabled.setObjectName(u"checkBoxEnabled")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.checkBoxEnabled.sizePolicy().hasHeightForWidth())
        self.checkBoxEnabled.setSizePolicy(sizePolicy2)

        self.verticalLayout_4.addWidget(self.checkBoxEnabled)

        self.checkBoxBipolar = QCheckBox(self.mainGroupBox)
        self.checkBoxBipolar.setObjectName(u"checkBoxBipolar")
        sizePolicy2.setHeightForWidth(self.checkBoxBipolar.sizePolicy().hasHeightForWidth())
        self.checkBoxBipolar.setSizePolicy(sizePolicy2)

        self.verticalLayout_4.addWidget(self.checkBoxBipolar)


        self.mainLayout.addLayout(self.verticalLayout_4, 1, 4, 1, 1)

        self.label_116 = QLabel(self.mainGroupBox)
        self.label_116.setObjectName(u"label_116")
        sizePolicy1.setHeightForWidth(self.label_116.sizePolicy().hasHeightForWidth())
        self.label_116.setSizePolicy(sizePolicy1)
        self.label_116.setMinimumSize(QSize(140, 0))
        self.label_116.setMaximumSize(QSize(140, 16777215))
        self.label_116.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.label_116, 0, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.label_70 = QLabel(self.mainGroupBox)
        self.label_70.setObjectName(u"label_70")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_70.sizePolicy().hasHeightForWidth())
        self.label_70.setSizePolicy(sizePolicy3)

        self.verticalLayout_3.addWidget(self.label_70)

        self.textEditTarget = QLineEdit(self.mainGroupBox)
        self.textEditTarget.setObjectName(u"textEditTarget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.textEditTarget.sizePolicy().hasHeightForWidth())
        self.textEditTarget.setSizePolicy(sizePolicy4)
        self.textEditTarget.setMinimumSize(QSize(250, 0))

        self.verticalLayout_3.addWidget(self.textEditTarget)


        self.mainLayout.addLayout(self.verticalLayout_3, 0, 5, 2, 1)

        self.label_112 = QLabel(self.mainGroupBox)
        self.label_112.setObjectName(u"label_112")
        sizePolicy1.setHeightForWidth(self.label_112.sizePolicy().hasHeightForWidth())
        self.label_112.setSizePolicy(sizePolicy1)
        self.label_112.setMinimumSize(QSize(140, 0))
        self.label_112.setMaximumSize(QSize(140, 16777215))
        self.label_112.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.label_112, 0, 2, 1, 1)

        self.dialDelay = QDial(self.mainGroupBox)
        self.dialDelay.setObjectName(u"dialDelay")
        sizePolicy2.setHeightForWidth(self.dialDelay.sizePolicy().hasHeightForWidth())
        self.dialDelay.setSizePolicy(sizePolicy2)
        self.dialDelay.setMinimumSize(QSize(140, 60))
        self.dialDelay.setMaximumSize(QSize(140, 16777215))
        self.dialDelay.setMaximum(65535)

        self.mainLayout.addWidget(self.dialDelay, 1, 3, 1, 1)

        self.dialFrequency = QDial(self.mainGroupBox)
        self.dialFrequency.setObjectName(u"dialFrequency")
        sizePolicy2.setHeightForWidth(self.dialFrequency.sizePolicy().hasHeightForWidth())
        self.dialFrequency.setSizePolicy(sizePolicy2)
        self.dialFrequency.setMinimumSize(QSize(140, 60))
        self.dialFrequency.setMaximumSize(QSize(140, 16777215))
        self.dialFrequency.setMaximum(65535)

        self.mainLayout.addWidget(self.dialFrequency, 1, 1, 1, 1)

        self.dialAmplitude = QDial(self.mainGroupBox)
        self.dialAmplitude.setObjectName(u"dialAmplitude")
        sizePolicy2.setHeightForWidth(self.dialAmplitude.sizePolicy().hasHeightForWidth())
        self.dialAmplitude.setSizePolicy(sizePolicy2)
        self.dialAmplitude.setMinimumSize(QSize(140, 60))
        self.dialAmplitude.setMaximumSize(QSize(140, 16777215))
        self.dialAmplitude.setMaximum(65535)

        self.mainLayout.addWidget(self.dialAmplitude, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSpacer = QSpacerItem(20, 1, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_5 = QLabel(self.mainGroupBox)
        self.label_5.setObjectName(u"label_5")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy5)
        self.label_5.setMaximumSize(QSize(60, 16777215))

        self.verticalLayout_2.addWidget(self.label_5)

        self.label_4 = QLabel(self.mainGroupBox)
        self.label_4.setObjectName(u"label_4")
        sizePolicy5.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy5)
        self.label_4.setMaximumSize(QSize(60, 16777215))

        self.verticalLayout_2.addWidget(self.label_4)

        self.label = QLabel(self.mainGroupBox)
        self.label.setObjectName(u"label")
        sizePolicy5.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy5)
        self.label.setMaximumSize(QSize(60, 16777215))

        self.verticalLayout_2.addWidget(self.label)

        self.label_3 = QLabel(self.mainGroupBox)
        self.label_3.setObjectName(u"label_3")
        sizePolicy5.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy5)
        self.label_3.setMaximumSize(QSize(60, 16777215))

        self.verticalLayout_2.addWidget(self.label_3)

        self.label_2 = QLabel(self.mainGroupBox)
        self.label_2.setObjectName(u"label_2")
        sizePolicy5.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy5)
        self.label_2.setMaximumSize(QSize(60, 16777215))

        self.verticalLayout_2.addWidget(self.label_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.sliderWaveform = QSlider(self.mainGroupBox)
        self.sliderWaveform.setObjectName(u"sliderWaveform")
        self.sliderWaveform.setMaximum(4)
        self.sliderWaveform.setPageStep(1)
        self.sliderWaveform.setValue(4)
        self.sliderWaveform.setTracking(False)
        self.sliderWaveform.setOrientation(Qt.Vertical)
        self.sliderWaveform.setInvertedAppearance(False)
        self.sliderWaveform.setInvertedControls(False)
        self.sliderWaveform.setTickPosition(QSlider.TicksAbove)

        self.horizontalLayout.addWidget(self.sliderWaveform)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.mainLayout.addLayout(self.horizontalLayout, 1, 2, 1, 1)

        self.label_114 = QLabel(self.mainGroupBox)
        self.label_114.setObjectName(u"label_114")
        sizePolicy1.setHeightForWidth(self.label_114.sizePolicy().hasHeightForWidth())
        self.label_114.setSizePolicy(sizePolicy1)
        self.label_114.setMinimumSize(QSize(140, 0))
        self.label_114.setMaximumSize(QSize(140, 16777215))
        self.label_114.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.label_114, 0, 3, 1, 1)

        self.labelFrequencyValue = QLabel(self.mainGroupBox)
        self.labelFrequencyValue.setObjectName(u"labelFrequencyValue")
        self.labelFrequencyValue.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.labelFrequencyValue, 2, 1, 1, 1)

        self.labelAmplitudeValue = QLabel(self.mainGroupBox)
        self.labelAmplitudeValue.setObjectName(u"labelAmplitudeValue")
        self.labelAmplitudeValue.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.labelAmplitudeValue, 2, 0, 1, 1)

        self.labelDelayValue = QLabel(self.mainGroupBox)
        self.labelDelayValue.setObjectName(u"labelDelayValue")
        self.labelDelayValue.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.labelDelayValue, 2, 3, 1, 1)


        self.verticalLayout_5.addLayout(self.mainLayout)


        self.verticalLayout.addWidget(self.mainGroupBox)


        self.retranslateUi(Form_LFO)

        QMetaObject.connectSlotsByName(Form_LFO)
    # setupUi

    def retranslateUi(self, Form_LFO):
        Form_LFO.setWindowTitle(QCoreApplication.translate("Form_LFO", u"Form", None))
        self.mainGroupBox.setTitle(QCoreApplication.translate("Form_LFO", u"LFO", None))
        self.label_69.setText(QCoreApplication.translate("Form_LFO", u"Frequency", None))
        self.checkBoxEnabled.setText(QCoreApplication.translate("Form_LFO", u"Enabled", None))
        self.checkBoxBipolar.setText(QCoreApplication.translate("Form_LFO", u"Bipolar", None))
        self.label_116.setText(QCoreApplication.translate("Form_LFO", u"Amplitude", None))
        self.label_70.setText(QCoreApplication.translate("Form_LFO", u"Target (use lfoout)", None))
        self.label_112.setText(QCoreApplication.translate("Form_LFO", u"Waveform", None))
        self.label_5.setText(QCoreApplication.translate("Form_LFO", u"Random", None))
        self.label_4.setText(QCoreApplication.translate("Form_LFO", u"Square", None))
        self.label.setText(QCoreApplication.translate("Form_LFO", u"Sine", None))
        self.label_3.setText(QCoreApplication.translate("Form_LFO", u"Triangle", None))
        self.label_2.setText(QCoreApplication.translate("Form_LFO", u"Saw", None))
        self.label_114.setText(QCoreApplication.translate("Form_LFO", u"Delay", None))
        self.labelFrequencyValue.setText(QCoreApplication.translate("Form_LFO", u"0", None))
        self.labelAmplitudeValue.setText(QCoreApplication.translate("Form_LFO", u"0", None))
        self.labelDelayValue.setText(QCoreApplication.translate("Form_LFO", u"0", None))
    # retranslateUi

