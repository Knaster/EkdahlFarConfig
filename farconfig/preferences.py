from PySide6.QtWidgets import QWidget, QListWidgetItem, QTableView, QHeaderView, QTreeWidget, QTreeWidgetItem, QComboBox
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from watchdog.watchmedo import command

#from farconfig import commandSets
from ui_preferences import Ui_Form as preferencesWidget
import timedChart as TimedChart
import CommandSets

class preferences(QWidget):
    def __init__(self, farConfig, serialHandler,
                 timedChart:TimedChart.timedChart, commandSets:CommandSets.CommandSets, parent=None):
        super().__init__(parent)
        self.ui = preferencesWidget()
        self.ui.setupUi(self)

        self.farConfig = farConfig
        self.timedChart = timedChart
        self.commandSets = commandSets

        serialHandler.assignFeedbackReportItem(self.ui.checkBoxFilterCommAck, "command")
        serialHandler.assignFeedbackReportItem(self.ui.checkBoxFilterDebug, "debug")
        serialHandler.assignFeedbackReportItem(self.ui.checkBoxFilterError, "error")
        serialHandler.assignFeedbackReportItem(self.ui.checkBoxFilterExpressionParser, "expressionparser")
        serialHandler.assignFeedbackReportItem(self.ui.checkBoxFilterHardware, "hardware")
        serialHandler.assignFeedbackReportItem(self.ui.checkBoxFilterInfoRequest, "inforequest")
        serialHandler.assignFeedbackReportItem(self.ui.checkBoxFilterPriority, "priority")
        serialHandler.assignFeedbackReportItem(self.ui.checkBoxFilterUSB, "usb")
        serialHandler.assignFeedbackReportItem(self.ui.checkBoxFilterUndefined, "undefined")
        serialHandler.assignFeedbackReportItem(self.ui.checkBoxFilterOutput, "output")
        serialHandler.assignFeedbackReportItem(self.ui.checkBoxFilterInternal, "internal")

        self.ui.checkBoxDebugCursorFollow.stateChanged.connect(serialHandler.checkBoxDebugCursorFollowToggled)
        self.ui.checkBoxLimitLines.stateChanged.connect(serialHandler.checkBoxLimitLinesStateChanged)
        self.ui.spinBoxLimitLines.valueChanged.connect(serialHandler.spinBoxLimitLinesValueChanged)

        self.ui.pushButtonOk.pressed.connect(self.close)

        self.ui.listWidgetCharts.pressed.connect(self.chartItemSelected)
        #self.ui.comboBoxChartCommand.showPopup = self.custom_showPopup
        self.comboBoxChartCommandMinWidth = 0

    def getChartItem(self, name) -> TimedChart.CommandChart:
        for chart in self.timedChart.commandCharts:
            if (chart.name == name): return chart
        return None

    def chartItemSelected(self):
        chart = self.getChartItem(self.ui.listWidgetCharts.currentItem().text())
        if (chart is None): return
        self.ui.lineEditChartName.setText(chart.name)
        if (self.ui.comboBoxChartCommand.count() > 0):
            #self.ui.comboBoxChartCommand.addItem(chart.command)
            #self.ui.comboBoxChartCommand.setCurrentIndex(0)
            #commandItem = self.commandSets.currentCommandSet.CommandItem(chart.command)
            #commandID = self.commandSets.getCommandID(commandItem)

            for i in range(0, self.ui.comboBoxChartCommand.count() + 1):
                item = self.ui.comboBoxChartCommand.itemData(i)
                if item == chart.command:
                    self.ui.comboBoxChartCommand.setCurrentIndex(i)
                    break
            pass
        else:
            pass
        if (chart.isRequest):
            self.ui.lineEditChartParameters.setText(chart.parameters)
        else:
            self.ui.lineEditChartParameters.setText("")
        self.ui.checkBoxChartRequest.setChecked(chart.isRequest)
        self.ui.lineEditChartParameters.setEnabled(chart.isRequest)

        if (chart.requireArgument):
            self.ui.spinBoxChartRequiredArgument.setValue(chart.requiredArgumentIndex)
            self.ui.lineEditChartRequiredEquals.setText(chart.requiredArgumentContents)
        else:
            self.ui.spinBoxChartRequiredArgument.setValue(0)
            self.ui.lineEditChartRequiredEquals.setText("")
        self.ui.checkBoxChartRequireArgument.setChecked(chart.requireArgument)
        self.ui.spinBoxChartRequiredArgument.setEnabled(chart.requireArgument)
        self.ui.lineEditChartRequiredEquals.setEnabled(chart.requireArgument)

        self.ui.spinBoxChartValueArgument.setValue(chart.argument)
        self.ui.doubleSpinBoxChartRangeMax.setValue(chart.rangeMax)
        self.ui.doubleSpinBoxChartRangeMin.setValue(chart.rangeMin)
        self.ui.checkBoxChartLogarithmic.setChecked(True) if (chart.logarithmic) else self.ui.checkBoxChartLogarithmic.setChecked(False)
        self.ui.lineEditChartSuffix.setText(chart.suffix) if (not chart.suffix == "") else self.ui.lineEditChartSuffix.setText("")
        self.ui.checkBoxChartVisible.setChecked(True) if (chart.visible) else self.ui.checkBoxChartVisible.setChecked(False)
        self.ui.checkBoxChartSuppressFromSerial.setChecked(True) if (chart.supressSerial) else self.ui.checkBoxChartSuppressFromSerial.setChecked(False)
        pass

    def custom_showPopup(self):
        # Calculate the maximum width needed for all items
        fm = self.ui.comboBoxChartCommand.fontMetrics()
        max_width = max(fm.width(self.ui.comboBoxChartCommand.itemText(i)) for i in range(self.ui.comboBoxChartCommand.count()))

        # Get the internal view (QListView) and set its minimum width
        view = self.ui.comboBoxChartCommand.view()
        view.setMinimumWidth(max_width + 20)  # Add padding for aesthetics

        # Call the original showPopup
        super(QComboBox, self.ui.comboBoxChartCommand).showPopup()

    def clearCommandsComboBox(self):
        self.ui.comboBoxChartCommand.clear()

    def addCommandToCommandsComboBox(self, longName, shortName, commandID):
        text = shortName + " - " + longName

        fm = self.ui.comboBoxChartCommand.fontMetrics()
        wide = fm.width(text)
        if (wide > self.comboBoxChartCommandMinWidth):
            self.comboBoxChartCommandMinWidth = wide
            self.ui.comboBoxChartCommand.view().setMinimumWidth(self.comboBoxChartCommandMinWidth + 20)

        self.ui.comboBoxChartCommand.addItem(text, commandID)

    def show(self, /) -> None:
        self.ui.listWidgetCharts.clear()
        if hasattr(self.timedChart, "commandCharts"):
            for chart in self.timedChart.commandCharts:
                self.ui.listWidgetCharts.addItem(chart.name)
        super().show()

    def closeMe(self):
        self.close()