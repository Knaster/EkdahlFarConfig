import dataclasses

from PySide6.QtWidgets import QApplication, QWidget, QDoubleSpinBox, QListWidgetItem, QInputDialog, QMessageBox, QLineEdit, QComboBox, QSlider, QCheckBox
from PySide6.QtCore import QThread, Signal, QTimer, QModelIndex, Qt, QObject, QDir, Slot
from PySide6.QtGui import QTextBlock, QTextCursor, QTextBlockFormat, QColor, QKeyEvent, QTextCharFormat
from ui_prompt import Ui_Form
from enum import Enum, auto, IntEnum

from general_helpers import dataVisibilitySettings
from CommandSets import CommandSetModular

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
    reportTypeData = { 'cmd' : dataVisibilitySettings(True, 'command', color=QColor(180,255,120)),
                       'dbg' : dataVisibilitySettings(True, 'debug', color=QColor(255,255,115)),
                       'err' : dataVisibilitySettings(True, 'error', color=QColor(255,80,80)),
                       'ep' : dataVisibilitySettings(True, 'expressionparser'),
                       'hw' : dataVisibilitySettings(True, 'hardware'),
                       'irq' : dataVisibilitySettings(True, 'inforequest', color=QColor(215,200,255)),
                       'pri' : dataVisibilitySettings(True, 'priority', color=QColor(255,100,100)),
                       'usb' : dataVisibilitySettings(True, 'usb'),
                       'un' : dataVisibilitySettings(True, 'undefined'),
                       'out' : dataVisibilitySettings(True, '', color=QColor(127,127,127)),
                       'int' : dataVisibilitySettings(True, 'internal', color=QColor(128,128,128)),
                       'hlp': dataVisibilitySettings(True,'help', color=QColor(115, 200, 255)),
                       'txi' : dataVisibilitySettings(True, 'text')}

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
        self.commandSet:CommandSetModular = None

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

    def addToDebugWindow(self, text:str):
        ignoreMessage = False

        ignoreMessage = False
        qcolor = QColor(255, 255, 255)
        prefixName = ""
        if text[0:1] == "[":
            prefixName = text[1:text.find("]")]
            if prefixName in self.reportTypeData:
                qcolor = self.reportTypeData[prefixName].color
                if self.reportTypeData[prefixName].show <= 0:
                    ignoreMessage = True
            #text = text[len(prefixName) + 2:]

        '''
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
                    if self.reportTypeData['irq'].show == 0:
                    #if self.filterHideInfoRequest:
                        ignoreMessage = True
                case "txi":
                    color = "rgb(100,100,255)"
                    qcolor = QColor(100, 100, 255)
        elif dpdir == "mi":
                qcolor = QColor(00,200,200)
        elif dpdir == "so":
                qcolor = QColor(127,127,127)
                if self.reportTypeData['out'].show == 0:
                    #if self.filterHideOutput:
                    ignoreMessage = True
        else:
            color = "rgb(230,200,160)"
        '''

        if not ignoreMessage:
            if (prefixName == "irq" or prefixName == "cmd" or prefixName == "out") and self.commandSet is not None:
                find = text[5:]
                if prefixName == "out" and find[:4] == "rqi:": find = find[4:]
                find = find.strip("\n\r")
                if (find == ""): return
                moduleCommand, data = self.commandSet.getCommandAndModule(find)
                if moduleCommand is not None and moduleCommand in self.reportTypeData:
                    if self.reportTypeData[moduleCommand].show <= 0:
                        ignoreMessage = True

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

        self.logging.debug(text.rstrip("\n"))

    def debugClear(self):
        self.ui.plainTextEditSerialOutput.clear()

    def setSerialVisibility(self, data:dataVisibilitySettings):
        '''
        match(data.prefixType):
            case "irq":
                self.filterHideInfoRequest = not data.show
            case "out":
                self.filterHideOutput = not data.show
            case _:
                out = str(int(data.show))
                self.serialHandler.write("debugprint:" + data.prefixType[0] + ":" + out)
        pass
        '''
        if data.identifier != "":
            out = str(int(data.show))
            self.serialHandler.write("debugprint:" + data.identifier + ":" + out)

    def guiChangedDebugCursorFollowToggled(self):
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

    def guiChangedLimitLinesEnabled(self):
        value = self.sender().checkState()
        if (value == Qt.CheckState.Checked):
            self.lineLimitOn = True
        else:
            self.lineLimitOn = False
        self.updateLineLimit()

    def guiChangedLimitLinesValue(self):
        value = self.sender().value()
        self.lineLimit = value
        self.updateLineLimit()

    def lineEditSend(self):
        tempText = self.ui.lineEditSend.currentText()
        self.serialHandler.write(tempText)
        print("sending " + str(tempText.encode()))
        self.ui.lineEditSend.setCurrentText("")
