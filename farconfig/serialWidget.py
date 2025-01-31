from PySide6.QtWidgets import QApplication, QWidget, QDoubleSpinBox, QListWidgetItem, QInputDialog, QMessageBox, QLineEdit, QComboBox, QSlider
from PySide6.QtCore import QThread, Signal, QTimer, QModelIndex, Qt, QObject, QDir, Slot
from PySide6.QtGui import QTextBlock, QTextCursor, QTextBlockFormat, QColor

from ui_prompt import Ui_Form

import re

class SerialWidget(QWidget):
    def __init__(self, inSerialHandler, inTimeStamper, inLogging, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.filterHideOutput = False
        self.serialHandler = inSerialHandler
        self.timeStamper = inTimeStamper
        self.debugCursorFollow = False
        self.logging = inLogging

        self.ui.pushButtonSend.pressed.connect(self.lineEditSend)
        self.ui.lineEditSend.returnPressed.connect(self.lineEditSend)
        self.assignFeedbackReportItem(self.ui.checkBoxFilterCommAck, "command")
        self.assignFeedbackReportItem(self.ui.checkBoxFilterDebug, "debug")
        self.assignFeedbackReportItem(self.ui.checkBoxFilterError, "error")
        self.assignFeedbackReportItem(self.ui.checkBoxFilterExpressionParser, "expressionparser")
        self.assignFeedbackReportItem(self.ui.checkBoxFilterHardware, "hardware")
        self.assignFeedbackReportItem(self.ui.checkBoxFilterInfoRequest, "inforequest")
        self.assignFeedbackReportItem(self.ui.checkBoxFilterPriority, "priority")
        self.assignFeedbackReportItem(self.ui.checkBoxFilterUSB, "usb")
        self.assignFeedbackReportItem(self.ui.checkBoxFilterUndefined, "undefined")
        self.assignFeedbackReportItem(self.ui.checkBoxFilterOutput, "output")

        self.ui.checkBoxDebugCursorFollow.toggled.connect(self.checkBoxDebugCursorFollowToggled)
        self.ui.pushButtonClear.pressed.connect(self.debugClear)
        self.ui.checkBoxLimitLines.stateChanged.connect(self.checkBoxLimitLinesStateChanged)
        self.ui.spinBoxLimitLines.valueChanged.connect(self.spinBoxLimitLinesValueChanged)

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
                    qcolor = QColor(255,0,0)
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

        tbf = QTextBlockFormat()
        tbf.setBackground(qcolor)

        tc.setBlockFormat(tbf)
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

    def assignFeedbackReportItem(self, qtObject, reportType):
        qtObject.reportType = reportType
        qtObject.toggled.connect(self.feedbackReportToggled)

    def feedbackReportToggled(self):
        sender = self.sender()
        if (sender.reportType == "inforequest"):
            if (sender.isChecked()):
                self.filterHideInfoRequest = False
            else:
                self.filterHideInfoRequest = True
        elif (sender.reportType == "output"):
            if (sender.isChecked()):
                self.filterHideOutput = False
            else:
                self.filterHideOutput = True
        else:
            if (sender.isChecked()):
                out = "1"
            else:
                out = "0"
            self.serialHandler.write("debugprint:" + sender.reportType + ":" + out)

    def setReportFeedback(self, reportType, state):
        if (state):
            out = "1"
        else:
            out = "0"
        self.serialHandler.write("debugprint:" + reportType + ":" + out)

    def checkBoxFilterCommAckToggled(self):
        self.setReportFeedback("command", self.ui.checkBoxFilterCommAck.isChecked())

    def checkBoxFilterDebugToggled(self):
        self.setReportFeedback("debug", self.ui.checkBoxFilterDebug.isChecked())

    def checkBoxFilterErrorToggled(self):
        self.setReportFeedback("error", self.ui.checkBoxFilterError.isChecked())

    def checkBoxFilterExpressionParserToggled(self):
        self.setReportFeedback("expressionparser", self.ui.checkBoxFilterExpressionParser.isChecked())

    def checkBoxFilterHardwareToggled(self):
        self.setReportFeedback("hardware", self.ui.checkBoxFilterHardware.isChecked())

    def checkBoxFilterInfoRequestToggled(self):
        #setReportFeedback("inforequest", self.ui.checkBoxFilterInfoRequest.isChecked())
        if (self.ui.checkBoxFilterInfoRequest.isChecked()):
            self.filterHideInfoRequest = False
        else:
            self.filterHideInfoRequest = True

    def checkBoxFilterPriorityToggled(self):
        self.setReportFeedback("priority", self.ui.checkBoxFilterPriority.isChecked())

    def checkBoxFilterUSBToggled(self):
        self.setReportFeedback("usb", self.ui.checkBoxFilterUSB.isChecked())

    def checkBoxFilterUndefinedToggled(self):
        self.setReportFeedback("undefined", self.ui.checkBoxFilterUndefined.isChecked())

    def checkBoxFilterOutputToggled(self):
        if (self.ui.checkBoxFilterOutput.isChecked()):
            self.filterHideOutput = False
        else:
            self.filterHideOutput = True

    def checkBoxDebugCursorFollowToggled(self):
        if (self.ui.checkBoxDebugCursorFollow.isChecked()):
            self.debugCursorFollow = True
        else:
            self.debugCursorFollow = False

    def setReportFeedback(self, reportType, state):
        if (state):
            out = "1"
        else:
            out = "0"
        self.serialHandler.write("debugprint:" + reportType + ":" + out)

    def updateLineLimit(self):
        if (self.ui.checkBoxLimitLines.checkState() == Qt.CheckState.Checked):
            self.ui.plainTextEditSerialOutput.setMaximumBlockCount(self.ui.spinBoxLimitLines.value())
        else:
            self.ui.plainTextEditSerialOutput.setMaximumBlockCount(0)

    def checkBoxLimitLinesStateChanged(self):
        self.updateLineLimit()

    def spinBoxLimitLinesValueChanged(self, value):
        self.updateLineLimit()


    def lineEditSend(self):
#        if self.serialStream is not None:
        try:
            tempText = self.ui.lineEditSend.text()
            self.serialHandler.write(tempText)
            print("sending " + str(tempText.encode()))
            self.ui.lineEditSend.clear()
        except:
            print("ERROR SENDING DATA!")
