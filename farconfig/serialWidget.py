import dataclasses

from PySide6.QtWidgets import QApplication, QWidget, QDoubleSpinBox, QListWidgetItem, QInputDialog, QMessageBox, QLineEdit, QComboBox, QSlider, QCheckBox
from PySide6.QtCore import QThread, Signal, QTimer, QModelIndex, Qt, QObject, QDir, Slot
from PySide6.QtGui import QTextBlock, QTextCursor, QTextBlockFormat, QColor, QKeyEvent, QTextCharFormat

from ui_prompt import Ui_Form
from enum import Enum, auto, IntEnum

from preferences import SettingsClass

import re

class ReportTypeEnum(Enum):
    command = auto()
    debug = auto()
    error = auto()
    expressionParser = auto()
    hardware = auto()
    infoRequest = auto()
    priority = auto()
    usb = auto()
    undefined = auto()
    output = auto()
    internal = auto()

class SerialWidget(QWidget):
    reportTypeData = { 'command' : SettingsClass(True, 'command'),
                       'debug' : SettingsClass(True, 'debug'),
                       'error' : SettingsClass(True, 'error'),
                       'expressionparser' : SettingsClass(True, 'expressionparser'),
                       'hardware' : SettingsClass(True, 'hardware'),
                       'inforequest' : SettingsClass(True, 'inforequest'),
                       'priority' : SettingsClass(True, 'priority'),
                       'usb' : SettingsClass(True, 'usb'),
                       'undefined' : SettingsClass(True, 'undefined'),
                       'output' : SettingsClass(True, 'output'),
                       'internal' : SettingsClass(True, 'internal')}

    backgroundColor = QColor(63,63,63)

    def __init__(self, inSerialHandler, inTimeStamper, inLogging, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.filterHideOutput = False
        self.filterHideInfoRequest = False
        self.serialHandler = inSerialHandler
        self.timeStamper = inTimeStamper
        self.debugCursorFollow = True
        self.logging = inLogging

        self.ui.pushButtonSend.pressed.connect(self.lineEditSend)
        self.originalLineEditKeyPressEvent = self.ui.lineEditSend.keyPressEvent
        self.ui.lineEditSend.keyPressEvent = self.lineEditKeypressEvent

        self.ui.pushButtonClear.pressed.connect(self.debugClear)

        self.ui.plainTextEditSerialOutput.setStyleSheet("QPlainTextEdit { background-color: " + self.backgroundColor.name() + "; }")

        self.lineLimit = 2500
        self.lineLimitOn = True
        self.cursorFollow = True

    def lineEditKeypressEvent(self, event:QKeyEvent):
        qline = self.ui.lineEditSend
        match(event.key()):
            case 16777220:
                qline.addItem(self.ui.lineEditSend.currentText())
                self.lineEditSend()
            case 16777235: #up
                if (qline.currentIndex() + 1 < qline.count()):
                    qline.setCurrentIndex(qline.currentIndex() + 1)
                else:
                    if (qline.currentText() != ""):
                        qline.clearEditText()
                    else:
                        if (qline.count() != 0): qline.setCurrentIndex(0)
            case 16777237:
                if (qline.currentIndex() - 1 > - 1):
                    qline.setCurrentIndex(qline.currentIndex() - 1)
                else:
                    if (qline.currentText() != ""):
                        qline.clearEditText()
                    else:
                        if (qline.count() != 0): qline.setCurrentIndex(qline.count() - 1)
            case _:
                self.originalLineEditKeyPressEvent(event)

    def addToDebugWindow(self, text):
        dpdir = text[1:3]
        ignoreMessage = False
        dptype = ""
        qcolor = QColor(255, 255, 255)
        if dpdir == "si":
            dptype = text[6:9]
            color = "white"
            match (dptype):
                case "cmd":
                    color = "rgb(180,255,120)"
                    qcolor = QColor(180,255,120)
                case "dbg":
                    color = "rgb(255,255,115)"
                    qcolor = QColor(255,255,115)
                case "err":
                    color = "rgb(255,0,0)"
                    qcolor = QColor(255,80,80)
                case "pri":
                    color = "rgb(255,100,100)"
                    qcolor = QColor(255,100,100)
                case "hlp":
                    color = "rgb(115,200,255)"
                    qcolor = QColor(115,200,255)
                case "irq":
                    color = "rgb(215,200,255)"
                    qcolor = QColor(215,200,255)
                    if self.filterHideInfoRequest:
                        ignoreMessage = True
                case "txi":
                    color = "rgb(100,100,255)"
                    qcolor = QColor(100, 100, 255)
        elif dpdir == "mi":
                qcolor = QColor(00,200,200)
        elif dpdir == "so":
                qcolor = QColor(127,127,127)
                if self.filterHideOutput:
                    ignoreMessage = True
        else:
            color = "rgb(230,200,160)"

        text = str(round(self.timeStamper.getCurrent(), 1)) + " : " + text

        far = text
        far = re.sub('[\u003c]', '&lt;', far)
        far = re.sub('[\u003e]', '&gt;', far)

        tc = QTextCursor(self.ui.plainTextEditSerialOutput.document())
        tc.movePosition(QTextCursor.MoveOperation.End)

        #tbf = QTextBlockFormat()
        #tbf.setBackground(qcolor)
        #tc.setBlockFormat(tbf)

        tcf = QTextCharFormat()
        tcf.setForeground(qcolor)
        tc.setCharFormat(tcf)

        if not ignoreMessage:
            tc.insertText(text)
#        tb = QTextBlock()
#        self.ui.plainTextEditSerialOutput.appendHtml("<div class='" + dptype + "' dir='" + dpdir + "' style='background-color: " + color + ";'>" + far + "</div>")
            if self.debugCursorFollow:
                scrollBar = self.ui.plainTextEditSerialOutput.verticalScrollBar()
                scrollBar.setValue(scrollBar.maximum())

        self.logging.error(text.rstrip("\n"))

    def debugClear(self):
        self.ui.plainTextEditSerialOutput.clear()

    def setSerialVisibility(self, data):
        match(data.identifier):
            case "inforequest":
                self.filterHideInfoRequest = not data.value
            case "output":
                self.filterHideOutput = not data.value
            case _:
                out = str(int(data.value))
                self.serialHandler.write("debugprint:" + data.identifier + ":" + out)
        pass

    def checkBoxDebugCursorFollowToggled(self):
        value = self.sender().checkState()
        if (value == Qt.CheckState.Checked):
            self.debugCursorFollow = True
        else:
            self.debugCursorFollow = False

    def updateLineLimit(self):
        if (self.lineLimitOn):
            self.ui.plainTextEditSerialOutput.setMaximumBlockCount(self.lineLimit)
        else:
            self.ui.plainTextEditSerialOutput.setMaximumBlockCount(0)

    def checkBoxLimitLinesStateChanged(self):
        value = self.sender().checkState()
        if (value == Qt.CheckState.Checked):
            self.lineLimitOn = True
        else:
            self.lineLimitOn = False
        self.updateLineLimit()

    def spinBoxLimitLinesValueChanged(self):
        value = self.sender().value()
        self.lineLimit = value
        self.updateLineLimit()

    def lineEditSend(self):
        tempText = self.ui.lineEditSend.currentText()
        self.serialHandler.write(tempText)
        print("sending " + str(tempText.encode()))
        self.ui.lineEditSend.setCurrentText("")
