from typing import Any

from PySide6.QtWidgets import QWidget, QListWidgetItem, QTableView, QHeaderView, QTreeWidget, QTreeWidgetItem, QComboBox
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor
from PySide6.QtCore import Qt
from watchdog.watchmedo import command

from ModuleSystem import HelpModule, HelpCommand, ModuleHandler, Module, ModuleCommand
from ui_preferences import Ui_Form as preferencesWidget
import timedChart as TimedChart
from CommandSets import CommandSetModular
from general_helpers import dataVisibilitySettings, inputBox

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

        self.updatingGUI = False

        #### Global stuff
        self.ui.pushButtonOk.pressed.connect(self.close)

        #### Serial reporting
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterCommAck, 'cmd')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterDebug, 'dbg')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterError, 'err')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterExpressionParser, 'ep')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterHardware, 'hw')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterInfoRequest, 'irq')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterPriority, 'pri')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterUSB, 'usb')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterUndefined, 'un')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterOutput, 'out')
        self.assignCheckBoxToSettingsClass(self.ui.checkBoxFilterInternal, 'int')

        self.ui.checkBoxDebugCursorFollow.stateChanged.connect(serialWidget.guiChangedDebugCursorFollowToggled)
        self.ui.checkBoxLimitLines.stateChanged.connect(serialWidget.guiChangedLimitLinesEnabled)
        self.ui.spinBoxLimitLines.valueChanged.connect(serialWidget.guiChangedLimitLinesValue)

        #### Oscilloscope settings
        self.ui.listWidgetCharts.pressed.connect(self.guiChangedChartListItem)
        self.comboBoxChartCommandMinWidth = 0

        self.ui.lineEditChartName.editingFinished.connect(self.guiChangedChartName)
        self.ui.comboBoxChartCommand.currentIndexChanged.connect(self.guiChangedChartCommand)
        self.ui.checkBoxChartRequest.stateChanged.connect(self.guiChangedChartCommandRequest)
        #self.ui.lineEditChartParameters.editingFinished.connect(self.chartParametersChanged)
        self.ui.checkBoxChartRequireArgument.stateChanged.connect(self.guiChangedChartRequireArgument)
        #self.ui.lineEditChartRequiredEquals.editingFinished.connect(self.chartRequiredEqualsChanged)
        #self.ui.spinBoxChartValueArgument.editingFinished.connect(self.chartValueChanged)
        self.ui.spinBoxChartValueArgument.valueChanged.connect(self.guiChangedChartValueArgument)
        self.ui.doubleSpinBoxChartRangeMin.valueChanged.connect(self.guiChangedChartRangeMin)
        self.ui.doubleSpinBoxChartRangeMax.valueChanged.connect(self.guiChangedChartRangeMax)
        self.ui.checkBoxChartLogarithmic.stateChanged.connect(self.guiChangedChartLogarithmic)
        self.ui.lineEditChartSuffix.editingFinished.connect(self.guiChangedChartSuffix)
        self.ui.checkBoxZeroIsUnavailable.stateChanged.connect(self.guiChangedChartZeroIsUnavaliable)
        self.ui.checkBoxChartVisible.stateChanged.connect(self.guiChangedChartVisible)
        self.ui.checkBoxChartSuppressFromSerial.stateChanged.connect(self.guiChangedChartSuppressFromSerial)

        self.ui.pushButtonHideAll.pressed.connect(self.guiChangedChartHideAll)
        self.ui.pushButtonShowAll.pressed.connect(self.guiChangedChartShowAll)
        self.ui.pushButtonAddChart.pressed.connect(self.guiChangedChartAdd)
        self.ui.pushButtonRemoveChart.pressed.connect(self.guiChangedChartRemove)

    def guiChangedChartHideAll(self):
        for chart in self.timedChart.commandCharts:
            self.timedChart.setChartVisible(chart.name, False)

    def guiChangedChartShowAll(self):
        for chart in self.timedChart.commandCharts:
            self.timedChart.setChartVisible(chart.name, True)

    def guiChangedChartAdd(self):
        name = inputBox("Add chart", "Chart Name:")
        if name is None: return
        #self.timedChart.commandCharts.append(TimedChart.CommandChart(self.timedChart, name=name))
        self.timedChart.addChart(name)
        self.show()

    def guiChangedChartRemove(self):
        item = self.ui.listWidgetCharts.currentItem()
        if item is None or item == -1: return
        self.timedChart.removeChart(item.text())
        self.show()

        self.ui.doubleSpinBoxChartRangeMin.editingFinshed.connect(self.guiChangedChartRangeMin)
        self.ui.doubleSpinBoxChartRangeMax.editingFinshed.connect(self.guiChangedChartRangeMax)
        self.ui.checkBoxChartLogarithmic.stateChanged.connect(self.guiChangedChartLogarithmic)
        self.ui.lineEditChartSuffix.editingFinished.connect(self.guiChangedChartSuffix)

    def guiChangedChartName(self):
        newName = self.ui.lineEditChartName.text()
        oldName = self.ui.listWidgetCharts.currentItem().text()
        self.timedChart.setChartName(oldName, newName)
        self.ui.listWidgetCharts.currentItem().setText(newName)

    def guiChangedChartCommand(self):
        if (self.ui.listWidgetCharts.currentItem() is None): return
        name = self.ui.listWidgetCharts.currentItem().text()
        moduleCommand = self.ui.comboBoxChartCommand.currentData()
        if (moduleCommand is None) or (str(moduleCommand) == ""):
            moduleCommand = self.ui.comboBoxChartCommand.currentText()
        self.timedChart.setChartCommand(name, moduleCommand)

    def guiChangedChartRequireArgument(self):
        name = self.ui.listWidgetCharts.currentItem().text()
        self.timedChart.setChartRequireArgument(name, self.ui.checkBoxChartRequireArgument.isChecked())

    def guiChangedChartValueArgument(self):
        name = self.ui.listWidgetCharts.currentItem().text()
        self.timedChart.setValueArguments(name, self.ui.spinBoxChartValueArgument.value())

    def guiChangedChartCommandRequest(self):
        name = self.ui.listWidgetCharts.currentItem().text()
        self.timedChart.setChartRequest(name, self.ui.checkBoxChartRequest.isChecked())

    def guiChangedChartRangeMin(self):
        name = self.ui.listWidgetCharts.currentItem().text()
        self.timedChart.setRangeMin (name, self.ui.doubleSpinBoxChartRangeMin.value())

    def guiChangedChartRangeMax(self):
        name = self.ui.listWidgetCharts.currentItem().text()
        self.timedChart.setRangeMax (name, self.ui.doubleSpinBoxChartRangeMax.value())

    def guiChangedChartLogarithmic(self):
        name = self.ui.listWidgetCharts.currentItem().text()
        self.timedChart.setLogarithmic (name, self.ui.checkBoxChartLogarithmic.isChecked())

    def guiChangedChartSuffix(self):
        name = self.ui.listWidgetCharts.currentItem().text()
        self.timedChart.setSuffix (name, self.ui.lineEditChartSuffix.text())

    def guiChangedChartZeroIsUnavaliable(self):
        name = self.ui.listWidgetCharts.currentItem().text()
        self.timedChart.setChartZeroIsUnavailable(name, self.ui.checkBoxZeroIsUnavailable.isChecked())

    def guiChangedChartVisible(self):
        chart = self.getChartItem(self.ui.listWidgetCharts.currentItem().text())
        if (chart is None): return
        chart.visible = self.ui.checkBoxChartVisible.isChecked()
        self.timedChart.setChartVisible(chart.name, chart.visible)

    def guiChangedChartSuppressFromSerial(self):
        if self.updatingGUI: return
        chart = self.getChartItem(self.ui.listWidgetCharts.currentItem().text())
        chart.supressSerial = self.ui.checkBoxChartSuppressFromSerial.isChecked()
        if chart.commandData is not None:
            if chart.commandData not in self.serialWidget.reportTypeData:
                self.serialWidget.reportTypeData[chart.commandData] = dataVisibilitySettings(0, chart.commandData.getFullCommand(),
                                                                                   moduleCommand=chart.commandData)
            self.serialWidget.reportTypeData[chart.commandData].show = int(not self.ui.checkBoxChartSuppressFromSerial.isChecked())

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
        sender.reportObject.setShowUI(sender.isChecked())
        pass

    def serialWidgetUIReportFunction(self, setting):
        setting.uiObject.guiUpdate = True
        value = setting.show
        if (isinstance(value, str)):
            if value == "true": value = True
            else: value = False
        setting.uiObject.setChecked(value)
        setting.uiObject.guiUpdate = False

    def getChartItem(self, name) -> TimedChart.CommandChart:
        for chart in self.timedChart.commandCharts:
            if (chart.name == name): return chart
        return None

    def guiChangedChartListItem(self):
        self.updatingGUI = True

        chart = self.getChartItem(self.ui.listWidgetCharts.currentItem().text())
        if (chart is None): return
        self.ui.lineEditChartName.setText(chart.name)

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

        self.updatingGUI = False

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
                helpCommand.commandTypeFunction != helpCommand.commandTypeFunction.ectCountModules and
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

        for chart in self.timedChart.commandCharts:
            if chart.commandData is not None:
                if chart.commandData not in self.serialWidget.reportTypeData:
                    self.serialWidget.reportTypeData[chart.commandData] = dataVisibilitySettings(int(not chart.supressSerial),
                                                                                                 chart.commandData.getFullCommand(),
                                                                                                 moduleCommand=chart.commandData)

    def updateCommandsComboBox(self):
        self.ui.comboBoxChartCommand.clear()
        self.addCommandsToCommandComboBoxFromModule(self.commandSet.baseModule)

    def addCommandToCommandsComboBox(self, command:ModuleCommand):
        text = command.getFullCommand()
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