from typing import Any

from PySide6.QtWidgets import QWidget, QListWidgetItem, QTableView, QHeaderView, QTreeWidget, QTreeWidgetItem, QComboBox
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from watchdog.watchmedo import command

from ModuleSystem import HelpModule, HelpCommand, ModuleHandler, Module, ModuleCommand
from ui_preferences import Ui_Form as preferencesWidget
import timedChart as TimedChart
from CommandSets import CommandSetModular

class SettingsClass():
    value = None
    uiReportFunction = Any
    dataReportFunction = Any
    identifier = None
    uiObject = None

    def __init__(self, inValue, inIdentifier, inUIReportFunction = None, inDataReportFunction = None, inUIObject = None):
        self.value = inValue
        self.identifier = inIdentifier
        if (self.uiReportFunction is not None): self.uiReportFunction = inUIReportFunction
        if (self.dataReportFunction is not None): self.dataReportFunction = inDataReportFunction
        if (self.uiObject is not None): self.uiObject = inUIObject

    def setValueUI(self, inValue):
        self.value = inValue
        if (self.dataReportFunction is not None): self.dataReportFunction(self)

    def setValueData(self, inValue):
        self.value = inValue
        if (self.uiReportFunction is not None): self.uiReportFunction(self)

class preferences(QWidget):
    def __init__(self, farConfig, serialWidget,
                 timedChart:TimedChart.timedChart, commandSet:CommandSetModular, parent=None):
        super().__init__(parent)
        self.ui = preferencesWidget()
        self.ui.setupUi(self)

        self.farConfig = farConfig
        self.timedChart = timedChart
        self.commandSet = commandSet
        self.serialWidget = serialWidget

        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterCommAck, 'command')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterDebug, 'debug')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterError, 'error')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterExpressionParser, 'expressionparser')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterHardware, 'hardware')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterInfoRequest, 'inforequest')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterPriority, 'priority')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterUSB, 'usb')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterUndefined, 'undefined')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterOutput, 'output')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterInternal, 'internal')

        self.ui.checkBoxDebugCursorFollow.stateChanged.connect(serialWidget.checkBoxDebugCursorFollowToggled)
        self.ui.checkBoxLimitLines.stateChanged.connect(serialWidget.checkBoxLimitLinesStateChanged)
        self.ui.spinBoxLimitLines.editingFinished.connect(serialWidget.spinBoxLimitLinesValueChanged)

        self.ui.pushButtonOk.pressed.connect(self.close)

        self.ui.listWidgetCharts.pressed.connect(self.chartItemSelected)
        self.comboBoxChartCommandMinWidth = 0

        self.ui.checkBoxChartVisible.stateChanged.connect(self.chartVisibleChanged)
        self.ui.lineEditChartName.editingFinished.connect(self.chartNameChanged)
        self.ui.comboBoxChartCommand.currentIndexChanged.connect(self.chartCommandChanged)
        self.ui.checkBoxChartRequest.stateChanged.connect(self.chartRequestChanged)
        self.ui.checkBoxZeroIsUnavailable.stateChanged.connect(self.chartZeroIsUnavailableChanged)
        #self.ui.comboBoxChartCommand.currentTextChanged.connect(self.chartCommandChanged)

    def chartZeroIsUnavailableChanged(self):
        name = self.ui.listWidgetCharts.currentItem().text()
        self.timedChart.setChartZeroIsUnavailable(name, self.ui.checkBoxZeroIsUnavailable.isChecked())

    def chartRequestChanged(self):
        name = self.ui.listWidgetCharts.currentItem().text()
        self.timedChart.setChartRequest(name, self.ui.checkBoxChartRequest.isChecked())

    def chartCommandChanged(self):
        if (self.ui.listWidgetCharts.currentItem() is None): return
        name = self.ui.listWidgetCharts.currentItem().text()
        commandID = self.ui.comboBoxChartCommand.currentData()
        if (commandID is None) or (str(commandID) == ""):
            commandID = self.ui.comboBoxChartCommand.currentText()
        self.timedChart.setChartCommand(name, commandID)

    def chartNameChanged(self):
        newName = self.ui.lineEditChartName.text()
        oldName = self.ui.listWidgetCharts.currentItem().text()
        #chart = self.getChartItem(oldName)
        #chart.setChartName(oldName, newName)
        self.timedChart.setChartName(oldName, newName)
        self.ui.listWidgetCharts.currentItem().setText(newName)

    def chartVisibleChanged(self):
        chart = self.getChartItem(self.ui.listWidgetCharts.currentItem().text())
        if (chart is None): return
        chart.visible = self.ui.checkBoxChartVisible.isChecked()
        self.timedChart.setChartVisible(chart.name, chart.visible)

    def assignCheckBoxToSettingsClass(self, objectName, setting):
        self.serialWidget.reportTypeData[setting].uiReportFunction = self.serialWidgetUIReportFunction
        self.serialWidget.reportTypeData[setting].uiObject = objectName
        self.serialWidget.reportTypeData[setting].dataReportFunction = self.serialWidget.setSerialVisibility
        objectName.reportObject = self.serialWidget.reportTypeData[setting]
        objectName.stateChanged.connect(self.checkBoxStateChanged)
        objectName.guiUpdate = False

    def checkBoxStateChanged(self):
        sender = self.sender()
        if sender.guiUpdate: return
        sender.reportObject.setValueUI(sender.isChecked())
        pass

    def serialWidgetUIReportFunction(self, setting):
        setting.uiObject.guiUpdate = True
        value = setting.value
        if (isinstance(value, str)):
            if value == "true": value = True
            else: value = False
        setting.uiObject.setChecked(value)
        setting.uiObject.guiUpdate = False

        pass

    def getChartItem(self, name) -> TimedChart.CommandChart:
        for chart in self.timedChart.commandCharts:
            if (chart.name == name): return chart
        return None

    def chartItemSelected(self):
        chart = self.getChartItem(self.ui.listWidgetCharts.currentItem().text())
        if (chart is None): return
        self.ui.lineEditChartName.setText(chart.name)
        #if (self.ui.comboBoxChartCommand.count() > 0):
        #    for i in range(0, self.ui.comboBoxChartCommand.count() + 1):
        #        item = self.ui.comboBoxChartCommand.itemData(i)
        #        if item is not None:
        #            if item.commandID == chart.commandID:
        #                self.ui.comboBoxChartCommand.setCurrentIndex(i)
        #                break
        #    pass
        #else:
        #    pass

        if chart.commandData is None:
            self.ui.comboBoxChartCommand.setCurrentText("")
        else:
            self.ui.comboBoxChartCommand.setCurrentText(chart.commandData.getFullCommand())
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
        self.ui.checkBoxZeroIsUnavailable.setChecked(True) if (chart.zeroIsUnavailable) else self.ui.checkBoxZeroIsUnavailable.setChecked(False)
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

    def addCommandsToCommandComboBoxFromModule(self, module:ModuleHandler):
        for command in module.commands.values():
            helpCommand = command.helpCommand
            if (helpCommand.commandTypeData != HelpCommand.CommandType_data.ectSimpleString and
                helpCommand.commandTypeData != HelpCommand.CommandType_data.ectCommands and
                helpCommand.commandTypeData != HelpCommand.CommandType_data.ectData and
                helpCommand.commandTypeData != HelpCommand.CommandType_data.ectOutputAssignment and
                helpCommand.commandTypeDataOptions != HelpCommand.CommandType_dataOptions.ectExpression and
                helpCommand.commandTypeAccess != HelpCommand.CommandType_access.ectInvokeOnly and
                helpCommand.commandTypeFunction != helpCommand.commandTypeFunction.ectRemoveModule and
                helpCommand.commandTypeFunction != helpCommand.commandTypeFunction.ectAddModule and
                helpCommand.commandTypeFunction != helpCommand.commandTypeFunction.ectName and
                helpCommand.commandTypeFunction != helpCommand.commandTypeFunction.ectAssignment and
                (not helpCommand.commandTypeLogic) and (not helpCommand.commandTypeSystem)):

                if (helpCommand.shortCommand != "nop" and helpCommand.shortCommand != "rqi" and helpCommand.shortCommand != "ver" and
                        helpCommand.longCommand != "" and (not helpCommand.hidden)):

                    self.addCommandToCommandsComboBox(command)

        for group in module.groups:
            for child in group.children:
                self.addCommandsToCommandComboBoxFromModule(child)

    def updateCommandset(self, commandSet:CommandSetModular):
        self.commandSet = commandSet
        self.updateCommandsComboBox()

    def updateCommandsComboBox(self):
        self.addCommandsToCommandComboBoxFromModule(self.commandSet.baseModule)

    def addCommandToCommandsComboBox(self, command:ModuleCommand):
        text = command.getFullCommand()
        #ci = self.commandSet.currentCommandSet.CommandItem(commandItem.argument[0])
        #commandID, module = self.commandSet.currentCommandSet.getCommandID(ci)
        #if (commandID is not None):
            #ci.commandID = commandID
        ci = command
        fm = self.ui.comboBoxChartCommand.fontMetrics()
        wide = fm.width(text)
        if (wide > self.comboBoxChartCommandMinWidth):
            self.comboBoxChartCommandMinWidth = wide
            self.ui.comboBoxChartCommand.view().setMinimumWidth(self.comboBoxChartCommandMinWidth + 20)
        self.ui.comboBoxChartCommand.addItem(text, ci)

    def show(self, /) -> None:
        self.ui.listWidgetCharts.clear()
        if hasattr(self.timedChart, "commandCharts"):
            for chart in self.timedChart.commandCharts:
                self.ui.listWidgetCharts.addItem(chart.name)
        super().show()

    def closeMe(self):
        self.close()