# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferences.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(640, 568)
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
        Form.setPalette(palette)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabSerial = QWidget()
        self.tabSerial.setObjectName(u"tabSerial")
        self.verticalLayout_5 = QVBoxLayout(self.tabSerial)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.checkBoxLimitLines = QCheckBox(self.tabSerial)
        self.checkBoxLimitLines.setObjectName(u"checkBoxLimitLines")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxLimitLines.sizePolicy().hasHeightForWidth())
        self.checkBoxLimitLines.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.checkBoxLimitLines)

        self.spinBoxLimitLines = QSpinBox(self.tabSerial)
        self.spinBoxLimitLines.setObjectName(u"spinBoxLimitLines")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.spinBoxLimitLines.sizePolicy().hasHeightForWidth())
        self.spinBoxLimitLines.setSizePolicy(sizePolicy1)
        self.spinBoxLimitLines.setMaximum(10000)
        self.spinBoxLimitLines.setValue(5000)

        self.horizontalLayout_3.addWidget(self.spinBoxLimitLines)

        self.label_6 = QLabel(self.tabSerial)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_6)

        self.checkBoxDebugCursorFollow = QCheckBox(self.tabSerial)
        self.checkBoxDebugCursorFollow.setObjectName(u"checkBoxDebugCursorFollow")
        self.checkBoxDebugCursorFollow.setEnabled(True)
        sizePolicy.setHeightForWidth(self.checkBoxDebugCursorFollow.sizePolicy().hasHeightForWidth())
        self.checkBoxDebugCursorFollow.setSizePolicy(sizePolicy)
        self.checkBoxDebugCursorFollow.setChecked(True)

        self.horizontalLayout_3.addWidget(self.checkBoxDebugCursorFollow)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.groupBox_16 = QGroupBox(self.tabSerial)
        self.groupBox_16.setObjectName(u"groupBox_16")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_16.sizePolicy().hasHeightForWidth())
        self.groupBox_16.setSizePolicy(sizePolicy2)
        self.groupBox_16.setMinimumSize(QSize(0, 140))
        self.groupBox_16.setMaximumSize(QSize(16777215, 140))
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_16)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.checkBoxFilterCommAck = QCheckBox(self.groupBox_16)
        self.checkBoxFilterCommAck.setObjectName(u"checkBoxFilterCommAck")
        self.checkBoxFilterCommAck.setEnabled(False)

        self.verticalLayout_2.addWidget(self.checkBoxFilterCommAck)

        self.checkBoxFilterUSB = QCheckBox(self.groupBox_16)
        self.checkBoxFilterUSB.setObjectName(u"checkBoxFilterUSB")
        self.checkBoxFilterUSB.setEnabled(False)
        self.checkBoxFilterUSB.setCheckable(True)

        self.verticalLayout_2.addWidget(self.checkBoxFilterUSB)

        self.checkBoxFilterHardware = QCheckBox(self.groupBox_16)
        self.checkBoxFilterHardware.setObjectName(u"checkBoxFilterHardware")
        self.checkBoxFilterHardware.setEnabled(True)

        self.verticalLayout_2.addWidget(self.checkBoxFilterHardware)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.checkBoxFilterUndefined = QCheckBox(self.groupBox_16)
        self.checkBoxFilterUndefined.setObjectName(u"checkBoxFilterUndefined")
        self.checkBoxFilterUndefined.setEnabled(True)

        self.verticalLayout_3.addWidget(self.checkBoxFilterUndefined)

        self.checkBoxFilterPriority = QCheckBox(self.groupBox_16)
        self.checkBoxFilterPriority.setObjectName(u"checkBoxFilterPriority")
        self.checkBoxFilterPriority.setEnabled(True)

        self.verticalLayout_3.addWidget(self.checkBoxFilterPriority)

        self.checkBoxFilterError = QCheckBox(self.groupBox_16)
        self.checkBoxFilterError.setObjectName(u"checkBoxFilterError")
        self.checkBoxFilterError.setEnabled(True)

        self.verticalLayout_3.addWidget(self.checkBoxFilterError)

        self.checkBoxFilterOutput = QCheckBox(self.groupBox_16)
        self.checkBoxFilterOutput.setObjectName(u"checkBoxFilterOutput")
        self.checkBoxFilterOutput.setEnabled(False)

        self.verticalLayout_3.addWidget(self.checkBoxFilterOutput)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.checkBoxFilterInfoRequest = QCheckBox(self.groupBox_16)
        self.checkBoxFilterInfoRequest.setObjectName(u"checkBoxFilterInfoRequest")
        self.checkBoxFilterInfoRequest.setEnabled(True)

        self.verticalLayout_4.addWidget(self.checkBoxFilterInfoRequest)

        self.checkBoxFilterExpressionParser = QCheckBox(self.groupBox_16)
        self.checkBoxFilterExpressionParser.setObjectName(u"checkBoxFilterExpressionParser")
        self.checkBoxFilterExpressionParser.setEnabled(True)

        self.verticalLayout_4.addWidget(self.checkBoxFilterExpressionParser)

        self.checkBoxFilterDebug = QCheckBox(self.groupBox_16)
        self.checkBoxFilterDebug.setObjectName(u"checkBoxFilterDebug")
        self.checkBoxFilterDebug.setEnabled(True)

        self.verticalLayout_4.addWidget(self.checkBoxFilterDebug)

        self.checkBoxFilterInternal = QCheckBox(self.groupBox_16)
        self.checkBoxFilterInternal.setObjectName(u"checkBoxFilterInternal")
        self.checkBoxFilterInternal.setEnabled(True)

        self.verticalLayout_4.addWidget(self.checkBoxFilterInternal)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.verticalLayout_5.addWidget(self.groupBox_16)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tabSerial, "")
        self.tabSoftware = QWidget()
        self.tabSoftware.setObjectName(u"tabSoftware")
        self.verticalLayout_6 = QVBoxLayout(self.tabSoftware)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_11 = QGroupBox(self.tabSoftware)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.listWidgetTuningscheme = QListWidget(self.groupBox_11)
        self.listWidgetTuningscheme.setObjectName(u"listWidgetTuningscheme")

        self.verticalLayout_7.addWidget(self.listWidgetTuningscheme)


        self.verticalLayout_6.addWidget(self.groupBox_11)

        self.tabWidget.addTab(self.tabSoftware, "")
        self.tabOscilloscope = QWidget()
        self.tabOscilloscope.setObjectName(u"tabOscilloscope")
        self.verticalLayout_9 = QVBoxLayout(self.tabOscilloscope)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label = QLabel(self.tabOscilloscope)
        self.label.setObjectName(u"label")

        self.verticalLayout_9.addWidget(self.label)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.tabOscilloscope)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEditChartName = QLineEdit(self.tabOscilloscope)
        self.lineEditChartName.setObjectName(u"lineEditChartName")

        self.horizontalLayout_4.addWidget(self.lineEditChartName)


        self.verticalLayout_8.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.tabOscilloscope)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_5.addWidget(self.label_5)

        self.comboBoxChartCommand = QComboBox(self.tabOscilloscope)
        self.comboBoxChartCommand.setObjectName(u"comboBoxChartCommand")
        self.comboBoxChartCommand.setEditable(True)

        self.horizontalLayout_5.addWidget(self.comboBoxChartCommand)


        self.verticalLayout_8.addLayout(self.horizontalLayout_5)

        self.checkBoxChartRequest = QCheckBox(self.tabOscilloscope)
        self.checkBoxChartRequest.setObjectName(u"checkBoxChartRequest")

        self.verticalLayout_8.addWidget(self.checkBoxChartRequest)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_7 = QLabel(self.tabOscilloscope)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(90, 16777215))

        self.horizontalLayout_6.addWidget(self.label_7)

        self.lineEditChartParameters = QLineEdit(self.tabOscilloscope)
        self.lineEditChartParameters.setObjectName(u"lineEditChartParameters")

        self.horizontalLayout_6.addWidget(self.lineEditChartParameters)


        self.verticalLayout_8.addLayout(self.horizontalLayout_6)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.checkBoxChartRequireArgument = QCheckBox(self.tabOscilloscope)
        self.checkBoxChartRequireArgument.setObjectName(u"checkBoxChartRequireArgument")

        self.horizontalLayout_10.addWidget(self.checkBoxChartRequireArgument)

        self.spinBoxChartRequiredArgument = QSpinBox(self.tabOscilloscope)
        self.spinBoxChartRequiredArgument.setObjectName(u"spinBoxChartRequiredArgument")

        self.horizontalLayout_10.addWidget(self.spinBoxChartRequiredArgument)


        self.verticalLayout_10.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_10 = QLabel(self.tabOscilloscope)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_12.addWidget(self.label_10)

        self.lineEditChartRequiredEquals = QLineEdit(self.tabOscilloscope)
        self.lineEditChartRequiredEquals.setObjectName(u"lineEditChartRequiredEquals")

        self.horizontalLayout_12.addWidget(self.lineEditChartRequiredEquals)


        self.verticalLayout_10.addLayout(self.horizontalLayout_12)


        self.verticalLayout_8.addLayout(self.verticalLayout_10)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_8 = QLabel(self.tabOscilloscope)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_9.addWidget(self.label_8)

        self.spinBoxChartValueArgument = QSpinBox(self.tabOscilloscope)
        self.spinBoxChartValueArgument.setObjectName(u"spinBoxChartValueArgument")

        self.horizontalLayout_9.addWidget(self.spinBoxChartValueArgument)


        self.verticalLayout_8.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_2 = QLabel(self.tabOscilloscope)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_7.addWidget(self.label_2)

        self.doubleSpinBoxChartRangeMin = QDoubleSpinBox(self.tabOscilloscope)
        self.doubleSpinBoxChartRangeMin.setObjectName(u"doubleSpinBoxChartRangeMin")
        self.doubleSpinBoxChartRangeMin.setMaximum(65535.000000000000000)

        self.horizontalLayout_7.addWidget(self.doubleSpinBoxChartRangeMin)

        self.label_3 = QLabel(self.tabOscilloscope)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(15, 16777215))

        self.horizontalLayout_7.addWidget(self.label_3)

        self.doubleSpinBoxChartRangeMax = QDoubleSpinBox(self.tabOscilloscope)
        self.doubleSpinBoxChartRangeMax.setObjectName(u"doubleSpinBoxChartRangeMax")
        self.doubleSpinBoxChartRangeMax.setDecimals(2)
        self.doubleSpinBoxChartRangeMax.setMaximum(65535.000000000000000)

        self.horizontalLayout_7.addWidget(self.doubleSpinBoxChartRangeMax)


        self.verticalLayout_8.addLayout(self.horizontalLayout_7)

        self.checkBoxChartLogarithmic = QCheckBox(self.tabOscilloscope)
        self.checkBoxChartLogarithmic.setObjectName(u"checkBoxChartLogarithmic")

        self.verticalLayout_8.addWidget(self.checkBoxChartLogarithmic)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_9 = QLabel(self.tabOscilloscope)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_11.addWidget(self.label_9)

        self.lineEditChartSuffix = QLineEdit(self.tabOscilloscope)
        self.lineEditChartSuffix.setObjectName(u"lineEditChartSuffix")

        self.horizontalLayout_11.addWidget(self.lineEditChartSuffix)


        self.verticalLayout_8.addLayout(self.horizontalLayout_11)

        self.pushButtonChartSetColor = QPushButton(self.tabOscilloscope)
        self.pushButtonChartSetColor.setObjectName(u"pushButtonChartSetColor")

        self.verticalLayout_8.addWidget(self.pushButtonChartSetColor)

        self.checkBoxChartVisible = QCheckBox(self.tabOscilloscope)
        self.checkBoxChartVisible.setObjectName(u"checkBoxChartVisible")

        self.verticalLayout_8.addWidget(self.checkBoxChartVisible)

        self.checkBoxChartSuppressFromSerial = QCheckBox(self.tabOscilloscope)
        self.checkBoxChartSuppressFromSerial.setObjectName(u"checkBoxChartSuppressFromSerial")

        self.verticalLayout_8.addWidget(self.checkBoxChartSuppressFromSerial)


        self.gridLayout.addLayout(self.verticalLayout_8, 0, 1, 1, 1)

        self.listWidgetCharts = QListWidget(self.tabOscilloscope)
        self.listWidgetCharts.setObjectName(u"listWidgetCharts")

        self.gridLayout.addWidget(self.listWidgetCharts, 0, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButtonHideAll = QPushButton(self.tabOscilloscope)
        self.pushButtonHideAll.setObjectName(u"pushButtonHideAll")

        self.horizontalLayout_8.addWidget(self.pushButtonHideAll)

        self.pushButtonShowAll = QPushButton(self.tabOscilloscope)
        self.pushButtonShowAll.setObjectName(u"pushButtonShowAll")

        self.horizontalLayout_8.addWidget(self.pushButtonShowAll)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)

        self.pushButtonAdd = QPushButton(self.tabOscilloscope)
        self.pushButtonAdd.setObjectName(u"pushButtonAdd")

        self.horizontalLayout_8.addWidget(self.pushButtonAdd)

        self.pushButtonRemove = QPushButton(self.tabOscilloscope)
        self.pushButtonRemove.setObjectName(u"pushButtonRemove")

        self.horizontalLayout_8.addWidget(self.pushButtonRemove)


        self.gridLayout.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)


        self.verticalLayout_9.addLayout(self.gridLayout)

        self.tabWidget.addTab(self.tabOscilloscope, "")
        self.tabNodes = QWidget()
        self.tabNodes.setObjectName(u"tabNodes")
        self.tabWidget.addTab(self.tabNodes, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonOk = QPushButton(Form)
        self.pushButtonOk.setObjectName(u"pushButtonOk")
        self.pushButtonOk.setMinimumSize(QSize(100, 0))
        self.pushButtonOk.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.pushButtonOk)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.checkBoxLimitLines.setText(QCoreApplication.translate("Form", u"Keep maximum of", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Lines", None))
        self.checkBoxDebugCursorFollow.setText(QCoreApplication.translate("Form", u"Cursor follow", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("Form", u"Filter messages", None))
        self.checkBoxFilterCommAck.setText(QCoreApplication.translate("Form", u"Command aknowledge", None))
        self.checkBoxFilterUSB.setText(QCoreApplication.translate("Form", u"USB Commands", None))
        self.checkBoxFilterHardware.setText(QCoreApplication.translate("Form", u"Hardware messages", None))
        self.checkBoxFilterUndefined.setText(QCoreApplication.translate("Form", u"Undefined messages", None))
        self.checkBoxFilterPriority.setText(QCoreApplication.translate("Form", u"Priority messages", None))
        self.checkBoxFilterError.setText(QCoreApplication.translate("Form", u"Error messages", None))
        self.checkBoxFilterOutput.setText(QCoreApplication.translate("Form", u"Output messages", None))
        self.checkBoxFilterInfoRequest.setText(QCoreApplication.translate("Form", u"Info Requests", None))
        self.checkBoxFilterExpressionParser.setText(QCoreApplication.translate("Form", u"Expression parser", None))
        self.checkBoxFilterDebug.setText(QCoreApplication.translate("Form", u"Debug messages", None))
        self.checkBoxFilterInternal.setText(QCoreApplication.translate("Form", u"Internal messages", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSerial), QCoreApplication.translate("Form", u"Serial monitor", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("Form", u"Tuning scheme for tuner", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSoftware), QCoreApplication.translate("Form", u"Software", None))
        self.label.setText(QCoreApplication.translate("Form", u"Signals", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Command", None))
        self.checkBoxChartRequest.setText(QCoreApplication.translate("Form", u"Request", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Parameters", None))
        self.checkBoxChartRequireArgument.setText(QCoreApplication.translate("Form", u"Require argument", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"To equal", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Value argument", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Range from", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"to", None))
        self.checkBoxChartLogarithmic.setText(QCoreApplication.translate("Form", u"Logarithmic", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Add suffix", None))
        self.pushButtonChartSetColor.setText(QCoreApplication.translate("Form", u"Set color", None))
        self.checkBoxChartVisible.setText(QCoreApplication.translate("Form", u"Visible", None))
        self.checkBoxChartSuppressFromSerial.setText(QCoreApplication.translate("Form", u"Suppress from serial monitor", None))
        self.pushButtonHideAll.setText(QCoreApplication.translate("Form", u"Hide all", None))
        self.pushButtonShowAll.setText(QCoreApplication.translate("Form", u"Show all", None))
        self.pushButtonAdd.setText(QCoreApplication.translate("Form", u"Add", None))
        self.pushButtonRemove.setText(QCoreApplication.translate("Form", u"Remove", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOscilloscope), QCoreApplication.translate("Form", u"Osciloscope", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNodes), QCoreApplication.translate("Form", u"Nodes", None))
        self.pushButtonOk.setText(QCoreApplication.translate("Form", u"Ok", None))
    # retranslateUi

