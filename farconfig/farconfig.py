#  This file is part of The Ekdahl FAR firmware.
#
#  The Ekdahl FAR firmware is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  The Ekdahl FAR firmware is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with The Ekdahl FAR firmware. If not, see <https://www.gnu.org/licenses/>.
#
# Copyright (C) 2024 Karl Ekdahl
#

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py

## @package farconfig
# \mainpage The Ekdahl FAR Configuration software
#
# This is the configuration software for the Knas Ekdahl FAR.\n\n
# The software communicates with the instrument(s) via RS-232 over USB, all communications is based on the concept of \a commands as outlined in the general
# FAR documentation. The information here within will only cover the communications with the latest version of the Ekdahl FAR firmware as any updates or changes
# should not be done to any legacy compatibility code for older versions. \n
# \n
# The basic concept of communication is that the configuration software will issue various \a information \a request \a commands ('rqi') and populate its
# various controls and status bars per the responses received. The rule of thumb is that each \a command issued generates a response, this can vary from a
# simple aknowledgement to returning a full set of data. The software is not to populate the GUI information whilst issuing commands but rather relies soley
# on responses in this regard. \n
# \n
# In the initial phase of communication some information has to be fully received before requesting additional information.
# Certain \a commands will return an unknown number of responses thus those requests are generally followed by a \a 'nop'-command.
# When a \a 'nop' aknowledgement is received the software knows that the previous data has been exhausted.
#
# The basic workflow for this software works as follows:
# * Issue a version request command to the FAR in order to know which \ref "CommandSets" "command set" to use
# * Issue a \a 'list'-command in order to receive the number of \a modules and \a commands contained within the instrument
# * Build a internal hierarchy from the responses of the \a 'list'-command using \ref CommandSets.CommandSetModular.buildHierarchy
# * Issue a \a 'help'-command in order to build the help reference
# * Build the help using \ref CommandSets.CommandSetModular.buildHelp
# * Build a plugin list from the internal \a module hierarchy using \ref "pluginhandler.PluginHandler.buildPluginList" "PluginHandler.buildPluginList"
# * Request data for each \a module depending on their \a request \a data
# * Build a node map from the \a modules and \a command \a responses received. See the \ref "nodehandler.NodeHandler" "NodeHandler" for more information

import platform, random, sys, time, datetime, os
import serial.tools.list_ports
from PySide6.QtWidgets import (QApplication, QWidget, QDoubleSpinBox, QListWidgetItem, QInputDialog, QMessageBox, QLineEdit,
                               QComboBox, QSlider, QTabBar, QTabWidget, QCheckBox, QDial, QPushButton, QListWidget)
from PySide6.QtCore import QThread, Signal, QTimer, Qt, Slot, QSettings, QSize
from PySide6.QtGui import QIcon, QPainter
import logging
from logging.handlers import RotatingFileHandler

import enum

import equationParsingHelpers
import waitdialog
import tableTest
#from farconfig.commandparser import CommandItem
from commandparser import CommandItem
from general_helpers import messageBox, inputBox, find_item, remove_item
from ui_form import Ui_Widget
import midieventhandling
from cveventhandling import CVEventHandler

from midieventhandling import midiEventHandler as midiEventHandler
from serialWidget import SerialWidget as SerialWidget
from commandReference import commandReference as CommandReference
import timedChart
from stringModule import stringModule, SimpleFARHandler

simpleFARHandler = SimpleFARHandler

global serialStream
from CommandSets import CommandSets, CommandID, CommandType

commandSets = CommandSets()
app = None

import pluginhandler

import nodehandler

def addModulesIfNeeded(needed):
    global simpleFARHandler
    while len(simpleFARHandler.stringModules) <= needed:
        simpleFARHandler.stringModules.append(stringModule())
    while (mainWidget.ui.comboBoxCurrentlySelectedModule.count() <= needed):
        mainWidget.ui.comboBoxCurrentlySelectedModule.addItem(str(mainWidget.ui.comboBoxCurrentlySelectedModule.count() + 1))

def processInformationForChart(inSerialHandler, command):
    inSerialHandler.chartCommandSignal.emit(command)
    return

def processInformationReturn(inSerialHandler, infoReturn):
    global simpleFARHandler
    global commandSets
    commandList = commandSets.currentCommandSet.CommandList()
    commandList.addCommands(infoReturn)

    mainWidget.updatingFromModule = True

    for i in commandList.commands:
        commandType = commandSets.getCommandType(i)
        processInformationForChart(inSerialHandler, i)

        id = commandSets.getCommandID(i)
        if (commandType == CommandType.simple):
            if ((len(i.argument)) > 0):
                try:
                    value = float(i.argument[0])
                except:
                    value = i.argument[0]
            else:
                value = ""
            try:
                index = i.hierarchy[len(i.hierarchy) - 2].selection[0]
            except:
                index = 0
            simpleFARHandler.stringModules[0].setCommandValue(id, value, index)
        mainWidget.updateStringModuleData()

        if (i.command == "ver"):
            if (len(i.argument) == 4):
                commandSets.chooseCommandSet(i.argument[3])
            else:
                commandSets.chooseCommandSet(i.argument[0])
            mainWidget.debugTimedChart.commandSet = commandSets.currentCommandSet
            simpleFARHandler.connected = True

        if (id == CommandID.help):
            commandSets.currentCommandSet.processHelpReturn(i, commandReference)

        if (commandSets.processMessages(i, commandSets, simpleFARHandler, mainWidget, serialHandler)):
            pass
        else:
            mainWidget.pluginHandler.processMessages(i, commandSets, simpleFARHandler, mainWidget, serialHandler)
            match id:
                case mainWidget.modalEvent:
                    mainWidget.modalDialog.stop()
                    mainWidget.updateUIData()

    mainWidget.updatingFromModule = False

def requestStringModuleData():
    if (not simpleFARHandler.connected): return
    commandSets.requestData(serialHandler)

def requestHelp():
    commandReference.ui.listWidgetCommands.clear()
    serialHandler.write("help")

class serialHandler(QThread):
    dataAvaliable = Signal(object, str)
    disconnectSignal = Signal()
    chartDataSignal = Signal(str, float, timedChart.seriesType) # float, float)
    chartCommandSignal = Signal(commandSets.currentCommandSet.CommandItem)

    def run(self) -> None:
        while self.isRunning:
            processed = False
            global serialStream
            try:
                if serialStream is not None:
                    if serialStream.inWaiting() != 0:
                        receivedText = serialStream.readline().decode('ascii').strip()
                        self.dataAvaliable.emit(self, receivedText)

            except Exception as e:
                serialStream = None
                self.disconnectSignal.emit()
                print("Error in serialStream")
                print(e)
            self.sleep(0.1)

    def stop(self):
        self.isRunning = False

    def write(str):
        serialWidget.addToDebugWindow(">so> " + str + "\n")
        str = str  + "\n\r"
        if serialStream == None:
            return
        serialStream.write(str.encode('ascii'))

    def writeI(self, str):
        str = str  + "\n\r"
        serialStream.write(str.encode('ascii'))

class VerticalIconTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDrawBase(False)

    def tabSizeHint(self, index):
        # Set a fixed size for each tab to accommodate the icon
        return QSize(100, 100)

    def paintEvent(self, event):
        painter = QPainter(self)
        for index in range(self.count()):
            rect = self.tabRect(index)
            icon = self.tabIcon(index)

            # Draw the icon centered within the tab rectangle
            painter.save()
            icon_size = 100
            pixmap = icon.pixmap(icon_size, icon_size)
            center_x = rect.x() + (rect.width() - icon_size) // 2
            center_y = rect.y() + (rect.height() - icon_size) // 2
            painter.drawPixmap(center_x, center_y, pixmap)
            painter.restore()

class FarConfig(QWidget):
    midiDataAvaliableSignal = Signal(str, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.focusing = False
        self.midiEventHandler = midiEventHandler(self, serialHandler, commandSets, simpleFARHandler)
        self.cvEventHandler = CVEventHandler(self, serialHandler, commandSets, simpleFARHandler)

        scriptdir = os.path.dirname(os.path.realpath(__file__))

        log_formatter = logging.Formatter('%(asctime)s - %(message)s')
        log_file = scriptdir + "/farconfig.log"
        log_handler = RotatingFileHandler(log_file, mode='w', maxBytes=1024 * 1024, backupCount=1, encoding=None, delay=0)
        log_handler.setFormatter(log_formatter)
        log_handler.setLevel(logging.DEBUG)
        log_app = logging.getLogger('root')
        log_app.setLevel(logging.DEBUG)
        log_app.addHandler(log_handler)

        icondir = ""
        match(platform.system()):
            case 'Darwin':
                icondir = scriptdir + "/resources/"
                pass
            case 'Linux':
                icondir = scriptdir + "/resources/"
                pass
            case 'Windows':
                icondir = scriptdir + "\\resources\\"
                pass

        self.ui.tabWidgetMain.setTabIcon(0, QIcon(icondir + "tuning_fork.png"))
        self.ui.tabWidgetMain.setTabText(0, "")
        self.ui.tabWidgetMain.setTabIcon(1, QIcon(icondir + "midi.png"))
        self.ui.tabWidgetMain.setTabText(1, "")
        self.ui.tabWidgetMain.setTabIcon(2, QIcon(icondir + "cv.png"))
        self.ui.tabWidgetMain.setTabText(2, "")
        self.ui.tabWidgetMain.setTabIcon(3, QIcon(icondir + "advanced.png"))
        self.ui.tabWidgetMain.setTabText(3, "")
        self.ui.tabWidgetMain.setTabIcon(4, QIcon(icondir + "stats.png"))
        self.ui.tabWidgetMain.setTabText(4, "")
        self.ui.tabWidgetMain.setTabIcon(5, QIcon(icondir + "software.png"))
        self.ui.tabWidgetMain.setTabText(5, "")

        self.ui.tab_temporary.setVisible(False)
        self.ui.tabWidgetMain.setTabText(6, "")

        self.ui.closeEvent = self.closeEvent

        self.serialThread = serialHandler(parent=self) # self is parent for Qthread so Qthread will be destroyed when it's parent no longer exist
        self.serialThread.dataAvaliable.connect(self.dataAvaliable)
        self.serialThread.disconnectSignal.connect(self.serialDisconnect)
        self.serialThread.start()

        self.updateTimer = QTimer(self)
        self.updateTimer.timeout.connect(self.timerUpdateControl)

        self.populateComboBoxBaseNote()
        self.populateHarmonicPresets()

        self.debugTimedChart = timedChart.timedChart()
        self.ui.gridLayoutChart.addWidget(self.debugTimedChart._chart_view)
        self.serialThread.chartDataSignal.connect(self.addData)
        self.serialThread.chartCommandSignal.connect(self.chartCommand)

        self.updatingFromModule = False

        self.timeStamper = self.debugTimedChart.timeStamper #timedChart.timeStamp()
        self.modalEvent = ""

        self.messageBox = messageBox
        self.addModulesIfNeeded = addModulesIfNeeded

        self.lastSerialEvent = 0

    def resizeEvent(self, event, /):
        self.ui.tabWidgetMain.setFixedWidth(event.size().width() - 19)
        self.ui.tabWidgetMain.setFixedHeight(event.size().height() - 59)
        self.ui.tab_nodeeditor.setFixedWidth(event.size().width() - 100)
        self.ui.tab_nodeeditor.setFixedHeight(event.size().height() - 59)
        pass

    def drawTabBar(self):
        self.ui.tabWidgetMain.setTabIcon(0, QIcon("resources/tuning_fork.png"))

        tabs = []
        for i in range(self.ui.tabWidgetMain.count()):
            widget = self.ui.tabWidgetMain.widget(i)
            text = self.ui.tabWidgetMain.tabText(i)
            icon = QIcon("resources/tuning_fork.png")  # Replace with actual icons
            tabs.append((widget, text, icon))

        # Set custom tab bar
        self.ui.tabWidgetMain.setTabPosition(QTabWidget.TabPosition.West)
        self.ui.tabWidgetMain.setTabBar(VerticalIconTabBar(self))

        # Clear and re-add tabs
        self.ui.tabWidgetMain.clear()
        for widget, text, icon in tabs:
            new_widget = QWidget()  # Optionally replace with existing widgets
            self.ui.tabWidgetMain.addTab(new_widget, icon, text)

        self.ui.tabWidgetMain.setCurrentIndex(0)

    def closeEvent(self, event):
        self.serialThread.stop()
        self.serialThread.quit()
        self.serialThread.wait()
        save_settings()
        print("close")
        app.quit()

    def handleHarmonicBaseNote(self, note):
        for a in range(1, mainWidget.ui.comboBoxBaseNote.count()):
            if int(mainWidget.ui.comboBoxBaseNote.itemData(a)) == int(note):
                mainWidget.ui.comboBoxBaseNote.setCurrentIndex(a)
        simpleFARHandler.stringModules[0].setCommandValue(CommandID.bowHarmonicBaseNote, float(note))

    def handleActuatorData(self, index, name, rest, engage, stall):
        if (name) == "":
            name = "noname" + str(random.randrange(0, 9999))
        while (self.ui.comboBoxActuatorPreset.count() <= int(index)):
            mainWidget.ui.comboBoxActuatorPreset.insertItem(self.ui.comboBoxActuatorPreset.count() + 1, "placeholder")

        simpleFARHandler.stringModules[0].setCommandValue(CommandID.bowPressureRest, rest)
        simpleFARHandler.stringModules[0].setCommandValue(CommandID.bowPressureEngage, engage)
        simpleFARHandler.stringModules[0].setCommandValue(CommandID.bowPressurePositionMax, stall)

        mainWidget.ui.comboBoxActuatorPreset.setItemText(int(index), name)
        mainWidget.ui.doubleSpinBoxBowRestPosition.setValue(float(rest))
        mainWidget.ui.doubleSpinBoxBowMinPressure.setValue(float(engage))
        mainWidget.ui.doubleSpinBoxBowMaxPressure.setValue(float(stall))

    def handleHarmonicSeriesData(self, index, name, ratios):
        if name != "":
            mainWidget.ui.comboBoxHarmonicList.setItemText(int(index), name)
        try:
            simpleFARHandler.stringModules[0].harmonicData.clear()
            hsi = 0 #2
            while (hsi < len(ratios)):
                simpleFARHandler.stringModules[0].harmonicData.append(ratios[hsi])
                hsi += 1
            mainWidget.updateHarmonicTable()
        except:
            mainWidget.messageBox("Problem! Yes!", "Oh no")

    def addData(self, seriesID, value, inSeriesType): # min, max):
        self.debugTimedChart.addData(seriesID, value, inSeriesType) # min, max)

    def chartCommand(self, command):
        self.debugTimedChart.processCommand(command)

    def timerUpdateControl(self):
        self.readSMData()

    @Slot(str)
    def midiDataAvaliable(self, device, msg):
        serialWidget.addToDebugWindow("<mi<" + str(msg) + "\n")

    def dataAvaliable(self, inSerialHandler, v):
        receivedText = v
        if (receivedText[:5] == "[irq]"):
            processInformationReturn(inSerialHandler, receivedText[5:])
        elif (receivedText[:5] == "[hlp]"):
            commandSets.processHelpReturn(receivedText[5:], commandReference)
        serialWidget.addToDebugWindow("<si< " + receivedText + "\n")
        self.lastSerialEvent = time.time()

    def setUIEnabled(self, state):
        serialWidget.ui.checkBoxFilterCommAck.setEnabled(state)
        serialWidget.ui.checkBoxFilterUSB.setEnabled(state)
        serialWidget.ui.checkBoxFilterHardware.setEnabled(state)
        serialWidget.ui.checkBoxFilterUndefined.setEnabled(state)
        serialWidget.ui.checkBoxFilterPriority.setEnabled(state)
        serialWidget.ui.checkBoxFilterError.setEnabled(state)
        serialWidget.ui.checkBoxFilterInfoRequest.setEnabled(state)
        serialWidget.ui.checkBoxFilterExpressionParser.setEnabled(state)
        serialWidget.ui.checkBoxFilterDebug.setEnabled(state)
        serialWidget.ui.checkBoxFilterOutput.setEnabled(state)
        self.ui.tabWidgetMain.setEnabled(state)

    def updateUIData(self):
        self.ui.listWidgetMidiEvents.clear()
        #self.ui.listWidgetCommands.clear()
        self.ui.comboBoxActuatorPreset.clear()
        self.ui.comboBoxHarmonicList.clear()
        requestStringModuleData()

    def connectDisconnect(self):
        if mainWidget.ui.pushButtonConnectDisconnect.text() == "Connect":
            selectedPort = mainWidget.ui.comboBoxSerialPorts.currentText()
            if selectedPort != "":
#                print(selectedPort.split(' ')[0])
                try:
                    global serialStream
                    serialStream = serial.Serial(selectedPort.split(' ')[0], 115200)
                    if serialStream is None:
                        print("serialStream is none!")
                        return
                    serialWidget.addToDebugWindow("Connected to " + serialStream.portstr + "\n")
                    mainWidget.ui.pushButtonConnectDisconnect.setText("Disconnect")

                    mainWidget.ui.listWidgetMidiEvents.clear()
                    mainWidget.ui.comboBoxHarmonicList.clear()
                    mainWidget.ui.comboBoxConfiguration.clear()
                    mainWidget.ui.comboBoxActuatorPreset.clear()
                    mainWidget.pluginHandler.clearAllPlugins()
                    mainWidget.localNodeHandler.clearNodes()
                    commandSets.currentCommandSet.clearData()
                    commandReference.clear()

                    self.setUIEnabled(True)
                    self.updateUIData()
                    serialHandler.write("rqi:ver")

                    serialWidget.checkBoxFilterErrorToggled()
                    serialWidget.checkBoxFilterExpressionParserToggled()
                    serialWidget.checkBoxFilterDebugToggled()
                    serialWidget.checkBoxFilterHardwareToggled()
                    serialWidget.checkBoxFilterPriorityToggled()
                    serialWidget.checkBoxFilterUndefinedToggled()
                    serialWidget.checkBoxFilterUSBToggled()
                    serialWidget.checkBoxFilterCommAckToggled()
#                    serialHandler.write("debugprint:inforequest:1")

                except (OSError, serial.SerialException):
                    print("Connection issue")
                    pass
        else:
            if serialStream.isOpen:
                serialStream.close()
                serialStream = None
            serialWidget.addToDebugWindow("Disconnected\n")
            mainWidget.ui.pushButtonConnectDisconnect.setText("Connect")

            simpleFARHandler.connected = False

    def serialDisconnect(self):
        self.ui.checkBoxContinuousSMData.setChecked(False)
        self.updateTimer.stop()
        self.ui.pushButtonConnectDisconnect.setText("Connect")
        #self.setUIEnabled(False)

    def populateSerialPorts(self):
        itemSelected = mainWidget.ui.comboBoxSerialPorts.currentIndex()
        mainWidget.ui.comboBoxSerialPorts.clear()
        serialPorts = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(serialPorts):
                mainWidget.ui.comboBoxSerialPorts.addItem(port + " - " + desc)
        mainWidget.ui.comboBoxSerialPorts.setCurrentIndex(itemSelected)

    def updateStringModuleData(self):
        global stringModules

        u = self.ui
        simpleUpdates = [u.doubleSpinBoxBowMotorPIDKp, u.doubleSpinBoxBowMotorPIDKi, u.doubleSpinBoxBowMotorPIDKd, u.doubleSpinBoxBowMotorPIDie,
                         u.doubleSpinBoxBowMotorMaxError, u.doubleSpinBoxBowMotorVoltage, u.doubleSpinBoxBowMotorTimeout, u.doubleSpinBoxMuteFullMutePosition,
                         u.doubleSpinBoxMuteHalfMutePosition, u.doubleSpinBoxMuteRestPosition, u.doubleSpinBoxMuteBackoff, u.doubleSpinBoxBowMotorMaxSpeed,
                         u.doubleSpinBoxBowMotorMinSpeed, u.doubleSpinBoxBowMaxPressure, u.doubleSpinBoxBowMinPressure, u.doubleSpinBoxBowRestPosition,
                         u.doubleSpinBoxSolenoidMaxForce, u.doubleSpinBoxSolenoidMaxForce, u.doubleSpinBoxSolenoidMinForce,
                         u.doubleSpinBoxSolenoidEngageDuration, u.spinBoxHarmonicShiftRange]

        progressBars = [[u.progressBar_bch, CommandID.bowHarmonic], [u.progressBar_bchb, CommandID.bowHarmonicBase],
                        [u.progressBar_bchbn, CommandID.bowHarmonicBaseNote], [u.progressBar_bchshr, CommandID.bowHarmonicShiftRange],
                        [u.progressBar_bchsh, CommandID.bowHarmonicShift], [u.progressBar_bchs5, CommandID.bowHarmonicShift5],
                        [u.progressBar_bcha, CommandID.bowHarmonicAdd], [u.progressBar_ar3, CommandID.pidTargetFreq]]

        for up in simpleUpdates:
            value = simpleFARHandler.stringModules[0].getCommandValue(up.command)
            if (value is not None):
                up.setValue(float(value))
            else:
                pass

        for pb in progressBars:
            value = simpleFARHandler.stringModules[0].getCommandValue(pb[1])
            if (value is not None):
                pb[0].setValue(int(value))
            else:
                pass

        self.ui.progressBar_ar1.setValue(self.ui.progressBar_bchb.value() - self.ui.progressBar_bchbn.value())
        self.ui.progressBar_ar2.setValue(self.ui.progressBar_bch.value() + self.ui.progressBar_bcha.value())

        self.updateContinuousStringModuleData()

        mainWidget.pluginHandler.updateWidgets(simpleFARHandler)

    def updateContinuousStringModuleData(self):
        freq = simpleFARHandler.stringModules[0].getCommandValue(CommandID.pickupStringFrequency)
        if not freq is None:
            #self.ui.horizontalSliderStringFrequency.setValue(int(freq))
            if (freq > 0):
                if (self.ui.listWidgetTuningscheme.currentItem() != None):
                    if ((self.ui.listWidgetTuningscheme.currentItem().text()) == "Equal temperament"):
                        ret = getBaseNoteFromFrequency(freq, scaleDataEqual)
                    else:
                        ret = getBaseNoteFromFrequency(freq, scaleDataJust)
                else:
                    ret = getBaseNoteFromFrequency(freq, scaleDataJust)

                self.ui.labelAnalyzeNote.setText(ret[3] + str(ret[0]))
                self.ui.labelAnalyzeCents.setText(str(round(ret[2])))
                self.ui.horizontalSliderStringFrequency.setValue(round(ret[2]))
                self.ui.labelAnalyzeFreq.setText(str(round(freq,1)))

        freq = simpleFARHandler.stringModules[0].getCommandValue(CommandID.motorFrequency)
        if not freq is None:
            mainWidget.ui.horizontalSliderBowFrequency.setValue(int(freq))
            if (freq > 0):
                if (self.ui.listWidgetTuningscheme.currentItem() != None):
                    if ((self.ui.listWidgetTuningscheme.currentItem().text()) == "Equal temperament"):
                        ret = getBaseNoteFromFrequency(freq, scaleDataEqual)
                    else:
                        ret = getBaseNoteFromFrequency(freq, scaleDataJust)
                else:
                    ret = getBaseNoteFromFrequency(freq, scaleDataJust)

                mainWidget.ui.labelBowFrequency.setText(ret[3] + str(ret[0]) + ":" + str(round(ret[2])) + " / " + str(round(freq,1)) + "Hz")

        current = simpleFARHandler.stringModules[0].getCommandValue(CommandID.motorCurrent)
        if not current is None:
            mainWidget.ui.horizontalSliderBowCurrent.setValue(int(current * 10))
            mainWidget.ui.labelBowCurrent.setText(str(current) + " A")

        freq = simpleFARHandler.stringModules[0].getCommandValue(CommandID.pidTargetFreq)
        if not freq is None:
            mainWidget.ui.labelSetFrequency.setText(str(freq) + " Hz")

        u = self.ui
        cvMaps = [[u.dialCVHarmonic, u.labelCVHarmonic], [u.dialCVHarmonicShift ,u.labelCVHarmonicShift], [u.dialCVFineTune ,u.labelCVFineTune],
                  [u.dialCVPressure ,u.labelCVPressure], [u.dialCVHammerTrigger ,u.labelCVHammerTrigger], [u.dialCVGate ,u.labelCVGate],
                  [u.dialCVHammerScale ,u.labelCVHammerScale], [u.dialCVMute ,u.labelCVMute]]

        for cv in range(0,8):
            cvMaps[cv][0].setValue(int(simpleFARHandler.stringModules[0].getCVValue(cv)) )
            cvMaps[cv][1].setText(str(simpleFARHandler.stringModules[0].getCVValue(cv)) )

    def comboBoxCurrentSelectedModuleIndexChanged(self, index):
        pass

    def expGUIToModule(self, value, max):
        divisor = 65535 / math.log10(max)
        out = math.pow(10, (value / divisor)) - 0.999
        return out

    def logModuleToGUI(self, value, max):
        value = float(value)
        if (value < 0): return 0
        divisor = 65535 / math.log10(max)
        return math.log10(value + 0.999) * divisor

    def assignValueChanged(self, qtObject, command, selectionIndex = None, log = False, max = 65535):
        qtObject.command = command
        qtObject.selectionIndex = selectionIndex
        qtObject.log = log
        qtObject.logMax = max
        if (isinstance(qtObject, QLineEdit)):
            qtObject.editingFinished.connect(self.textChangedSignal)
        elif (isinstance(qtObject, QCheckBox)):
            qtObject.checkStateChanged.connect(self.checkChangedSignal)
        else:
            qtObject.valueChanged.connect(self.basicChangedSignal)

    def checkChangedSignal(self):
        self.basicChangedSignal(self.sender().isChecked())

    def textChangedSignal(self):
        self.basicChangedSignal(self.sender().text())

    def basicChangedSignal(self, value):
        if (mainWidget.updatingFromModule or (not simpleFARHandler.connected)):
            return
        sender = self.sender()
        commandID = sender.command
        selection = None
        stripIndex = False
        try:
            selection = sender.selectionIndex
        except Exception as e:
            stripIndex = True
            pass
        if (selection is None):
            stripIndex = True
            selection = [0]
        qualifiedShorts = commandSets.getQualifiedShortCommand(commandID, selection, stripIndex)
        out = ""
        if isinstance(value, bool):
            if (value == True):
                value = 1
            else:
                value = 0
        else:
            try:
                if (sender.log):
                    value = self.expGUIToModule(float(value), sender.logMax)
                else:
                    value = float(value)
            except:
                value = "'" + value + "'"
        for qualifiedShort in qualifiedShorts:
            if (out != ""): out += ","
            out = qualifiedShort + ":" + str(value)
#            out = sender.command + ":" + str(value)
        for index in selection:
            simpleFARHandler.stringModules[0].setCommandValue(sender.command, value, index)
        serialHandler.write(out)

    def assignButtonPressCommandIssue(self, qtObject, command, refresh = False):
        qtObject.command = command
        qtObject.refresh = refresh
        qtObject.pressed.connect(self.buttonPressIssueCommand)

    def convertWidgetCommandToString(self, sender):
        command = ""
        if (isinstance(sender.command, list)):
            i = 0
            while(i < len(sender.command)):
                qualifiedShorts = commandSets.getQualifiedShortCommand(sender.command[i])
                for qualified in qualifiedShorts:
                    if (command != ""): command += ","
                    command += qualified + ":" + sender.command[i + 1]
                i += 2
        elif (isinstance(sender.command, CommandID)):
            qualifiedShorts = commandSets.getQualifiedShortCommand(sender.command)
            for qualified in qualifiedShorts:
                if (command != ""): command += ","
                command += qualified
        else:
            command = sender.command
        return command

    def buttonPressIssueCommand(self):
        sender = self.sender()
        command = self.convertWidgetCommandToString(sender)
        serialHandler.write(command)
        if sender.refresh:
            self.updateUIData()

    def checkBoxChartToggled(self):
        checkbox = self.sender()
        if (checkbox.isChecked()):
            visible = True
        else:
            visible = False
        mainWidget.debugTimedChart.setSeriesVisibleCommand(checkbox.seriesCommand, checkbox.seriesIndex, visible)

    def checkBoxChartAssign(self, qtobject, seriesCommand, index, seriesType):
        qtobject.toggled.connect(mainWidget.checkBoxChartToggled)
        qtobject.seriesCommand = seriesCommand
        qtobject.seriesIndex = index
        qtobject.seriesType = seriesType

    def tableViewScaleDataChanged(self, topLeft, bottomRight, role):
        commandSets.setHarmonicSeriesRatio(self, serialHandler, simpleFARHandler,
                                           int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.harmonicSeriesSelect)), topLeft.column(), topLeft.data())

    def comboBoxHarmonicListCurrentIndexChanged(self, index):
        if (index == -1): index = simpleFARHandler.stringModules[0].getCommandValue(CommandID.harmonicSeriesSelect)
        commandSets.setHarmonicSeriesSelect(self, serialHandler, simpleFARHandler, index)
        self.updateHarmonicTable()

    def pushButtonAddHarmonicPressed(self):
        commandSets.addHarmonicSeriesRatio(self, serialHandler, simpleFARHandler, int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.harmonicSeriesSelect)))
        #self.pushButtonSaveCurrentHarmonicListPressed()

    def pushButtonRemoveHarmonicPressed(self):
        selected = int(mainWidget.ui.tableViewScale.currentIndex().column())
        if (selected < 0):
            messageBox("Error", "Incorrect selection");
        commandSets.removeHarmonicSeriesRatio(self, serialHandler, simpleFARHandler, int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.harmonicSeriesSelect)), selected)

    '''
    def pushButtonSaveCurrentHarmonicListPressed(self):
        try:
            harmonicList = mainWidget.ui.comboBoxHarmonicList.currentIndex()
            listID = mainWidget.ui.comboBoxHarmonicList.currentText()
            commandSets.saveHarmonicSeries(self, serialHandler, simpleFARHandler, harmonicList, listID, False)
        except:
            messageBox("Error", "Error saving list")
    
    def pushButtonSaveNewHarmonicListPressed(self):
        listID = inputBox("List name", "List name")
        if listID is None:
            return
        if (self.find_item(mainWidget.ui.comboBoxHarmonicList, listID) != -1):
            messageBox("Error", "Harmonic series already exists!")
            return
        newIndex = mainWidget.ui.comboBoxHarmonicList.count()
        commandSets.saveHarmonicSeries(self, serialHandler, simpleFARHandler, newIndex, listID, True)
    '''
    def pushButtonAddHarmonicListPressed(self):
        listID = inputBox("List name", "List name")
        if listID is None:
            return
        newIndex = mainWidget.ui.comboBoxHarmonicList.count()
        commandSets.addHarmonicSeries(self, serialHandler, simpleFARHandler, newIndex, listID, True)
        self.ui.comboBoxHarmonicList.addItem(listID)

    def pushButtonRenameHarmonicListPressed(self):
        harmonicList = mainWidget.ui.comboBoxHarmonicList.currentIndex()
        listName = inputBox("List name", "List name")
        if listName is None:
            return
        commandSets.renameHarmonicSeries(self, serialHandler, simpleFARHandler, harmonicList, listName)
        mainWidget.ui.comboBoxHarmonicList.setItemText(harmonicList, listName)

    def pushButtonRemoveHarmonicListPressed(self):
        harmonicList = mainWidget.ui.comboBoxHarmonicList.currentIndex()
        commandSets.removeHarmonicSeries(self, serialHandler, simpleFARHandler, harmonicList)
        self.ui.comboBoxHarmonicList.removeItem(harmonicList)

    def pushButtonAddHarmonicListFilePressed(self):
        pass

    def updateHarmonicTable(self):
        mainWidget.ui.tableViewScale.setModel(tableTest.CustomTableModel(simpleFARHandler.stringModules[0].harmonicData))
        mainWidget.ui.tableViewScale.model().dataChanged.connect(mainWidget.tableViewScaleDataChanged)

    def pushButtonLoadFromModulePressed(self):
        self.updateUIData()

    def pushButtonSaveToModulePressed(self):
        serialHandler.write(commandSets.getQualifiedShortCommand(CommandID.saveAllParameters)[0])

    def setContinuousSMReadings(self, state):
        if state == True:
            self.updateTimer.start(100)
        else:
            self.updateTimer.stop()

    def readSMData(self):
        commandSets.requestContinuousData(serialHandler)
        self.updateContinuousStringModuleData()
#        print("update!")

    def checkBoxContinuousSMDataToggled(self):
        self.setContinuousSMReadings(self.ui.checkBoxContinuousSMData.isChecked())

    midiKeys = ["C-", "C#", "D-", "D#", "E-", "F-", "F#", "G-", "G#", "A-", "A#", "B-"]

    def populateComboBoxBaseNote(self):
        for octave in range(0,3):
            for key in range(0,12):
                self.ui.comboBoxBaseNote.addItem(self.midiKeys[key] + str(octave + 4), (octave + 4) * 12 + key)

    def comboBoxBaseNotePressed(self, index):
        qualifiedCommands = commandSets.getQualifiedShortCommand(CommandID.bowHarmonicBaseNote)
        for qualified in qualifiedCommands:
            serialHandler.write(qualified + ":" + str(self.ui.comboBoxBaseNote.itemData(index)))

    harmonicPresets = [["Just", 1, 1.06667, 1.125, 1.2, 1.25, 1.3333, 1.40625, 1.5, 1.6, 1.66667, 1.8, 1.875],
        ["Equal", 1, 1.059463094, 1.122462048, 1.189207115, 1.25992105, 1.334839854, 1.414213562, 1.498307077, 1.587401052, 1.681792831, 1.781797436, 1.887748625]]

    def populateHarmonicPresets(self):
        for a in self.harmonicPresets:
            self.ui.comboBoxHarmonicPresets.addItem(a[0])

    def pushButtonLoadHarmonicPresetPressed(self):
        b = self.ui.comboBoxHarmonicPresets.currentIndex()
        if (b < 0) or (b > len(self.harmonicPresets)):
            print("Error!")
            return

        commandSets.setHarmonicSeriesData(self, serialHandler, simpleFARHandler, simpleFARHandler.stringModules[0].getCommandValue(CommandID.harmonicSeriesSelect),
                                          self.ui.comboBoxHarmonicList.currentText(), self.harmonicPresets[b][1:len(self.harmonicPresets[b])])
#        qualifiedCommand = commandSets.getQualifiedShortCommand(CommandID.harmonicSeriesRatio,
#                                                                 [simpleFARHandler.stringModules[0].getCommandValue(CommandID.harmonicSeriesSelect)])[0]
#        for c in range(1,len(self.harmonicPresets[b])):
#            serialHandler.write(qualifiedCommand + ":" + str(c - 1) + ":" + str(self.harmonicPresets[b][c]))

        #self.updateUIData()

    def lineEditMidiEventCommandFinished(self):
        if mainWidget.ui.listWidgetMidiEvents.currentItem() == None:
            return
        commandSelected = mainWidget.ui.listWidgetMidiEvents.currentItem().text()
        commandSequence = mainWidget.ui.lineEditMidiEventCommand.text()
        index = int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect))
        match (commandSelected):
            case "Note On":
                #setStr = "noteon"
                #simpleFARHandler.instrumentMaster.evNoteOn = commandSequence
                commandSets.setMidiConfigurationNoteOnCommands(mainWidget, serialHandler, simpleFARHandler, index, commandSequence)
            case "Note Off":
                #setStr = "noteoff"
                #simpleFARHandler.instrumentMaster.evNoteOff = commandSequence
                commandSets.setMidiConfigurationNoteOffCommands(mainWidget, serialHandler, simpleFARHandler, index, commandSequence)
            case "Poly Aftertouch":
                #setStr = "pat"
                #simpleFARHandler.instrumentMaster.evPolyAftertouch = commandSequence
                commandSets.setMidiConfigurationPolyAftertouchCommands(mainWidget, serialHandler, simpleFARHandler, index, commandSequence)
            case "Channel Aftertouch":
                #setStr = "cat"
                #simpleFARHandler.instrumentMaster.evChannelAftertouch = commandSequence
                commandSets.setMidiConfigurationChannelAftertouchCommands(mainWidget, serialHandler, simpleFARHandler, index, commandSequence)
            case "Program change":
                #setStr = "pc"
                #simpleFARHandler.instrumentMaster.evProgramChange = commandSequence
                commandSets.setMidiConfigurationProgramChangeCommands(mainWidget, serialHandler, simpleFARHandler, index, commandSequence)
            case "Pitchbend":
                #setStr = "pb"
                #simpleFARHandler.instrumentMaster.evPitchbend = commandSequence
                commandSets.setMidiConfigurationPitchBendCommands(mainWidget, serialHandler, simpleFARHandler, index, commandSequence)
            case _:
                if commandSelected[:2] == "CC":
                    #setStr = "cc:" + commandSelected[3:]
                    cc = int(commandSelected[3:])
                    #item = simpleFARHandler.instrumentMaster.getCC(cc)
                    #item.command = commandSequence
                    commandSets.setMidiConfigurationContinuousControllerCommands(mainWidget, serialHandler, simpleFARHandler, index, cc, commandSequence)
                else:
                    print(commandSelected + " not found")
                    return

        #qualifiedCommand = commandSets.getQualifiedShortCommand(CommandID.midiConfigurationData,
        #                                                        [simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect)])[0]
        #serialString = qualifiedCommand + ":" + setStr + ":\"" + commandSequence + "\""
        #serialHandler.write(serialString)

    def pushButtonActuatorRenamePressed(self):
        index = mainWidget.ui.comboBoxActuatorPreset.currentIndex()
        if (index == -1): return
        listID = inputBox("New actuator name", "Actuator name")
        if listID is None:
            return
        if (find_item(mainWidget.ui.comboBoxActuatorPreset, listID) != -1):
            messageBox("Error", "Actuator already exists!")
            return
        mainWidget.ui.comboBoxActuatorPreset.setItemText(index, listID)
        commandSets.renameActuator(self, serialHandler, simpleFARHandler, index, listID)

        #newIndex = mainWidget.ui.comboBoxActuatorPreset.count()
        #commandSets.saveActuator(self, serialHandler, simpleFARHandler, newIndex, listID, str(self.ui.doubleSpinBoxBowRestPosition.value()),
        #                         str(self.ui.doubleSpinBoxBowMinPressure.value()), str(self.ui.doubleSpinBoxBowMaxPressure.value()))
        #self.updatingFromModule = True
        #mainWidget.ui.comboBoxActuatorPreset.setCurrentIndex(newIndex)
        #self.updatingFromModule = False


    def pushButtonActuatorAddPressed(self):
        #comboIndex = self.find_item(mainWidget.ui.comboBoxActuatorPreset, mainWidget.ui.comboBoxActuatorPreset.currentText())
        #if comboIndex == -1:
        #    return
        #commandSets.saveActuator(self, serialHandler, simpleFARHandler, comboIndex, mainWidget.ui.comboBoxActuatorPreset.currentText(),
        #                         str(self.ui.doubleSpinBoxBowRestPosition.value()), str(self.ui.doubleSpinBoxBowMinPressure.value()),
        #                         str(self.ui.doubleSpinBoxBowMaxPressure.value()))
        listID = inputBox("New actuator name", "Actuator name")
        if listID is None:
            return
        newIndex = simpleFARHandler.stringModules[0].getCommandValue(CommandID.actuatorCount)
        commandSets.addActuator(self, serialHandler, simpleFARHandler, newIndex, listID)
        mainWidget.ui.comboBoxActuatorPreset.addItem(listID)
        #mainWidget.ui.comboBoxActuatorPreset.setCurrentIndex(mainWidget.ui.comboBoxActuatorPreset.count() - 1)

    def comboBoxActuatorIndexChanged(self):
        if (self.updatingFromModule):
            return
        comboIndex = mainWidget.ui.comboBoxActuatorPreset.currentIndex()
        if comboIndex == -1:
            if (mainWidget.ui.comboBoxActuatorPreset.count() == 0):
                return
            mainWidget.ui.comboBoxActuatorPreset.setCurrentIndex(0)
            ba = 0
        commandSets.loadActuator(self, serialHandler, simpleFARHandler, comboIndex)
        #self.ui.doubleSpinBoxBowRestPosition.selectionIndex = [comboIndex]
        #self.ui.doubleSpinBoxBowMinPressure.selectionIndex = [comboIndex]
        #self.ui.doubleSpinBoxBowMaxPressure.selectionIndex = [comboIndex]

    def pushButtonAcutatorRemovePressed(self):
        comboIndex = mainWidget.ui.comboBoxActuatorPreset.currentIndex() # self.find_item(mainWidget.ui.comboBoxActuatorPreset, mainWidget.ui.comboBoxActuatorPreset.currentText())
        if comboIndex == -1:
            return
        mainWidget.ui.comboBoxActuatorPreset.removeItem(comboIndex)
        commandSets.removeActuator(self, serialHandler, simpleFARHandler, comboIndex)

    def assignButtonTest(self, qtObject, command, valuePointer, commandPost):
        qtObject.command = command
        qtObject.valuePointer = valuePointer
        qtObject.commandPost = commandPost
        qtObject.pressed.connect(self.testSignal)

    def testSignal(self):
        sender = self.sender()
        out = sender.commandPost
        serialHandler.write(out)

    def configurationSetName(self):
        defText = mainWidget.ui.comboBoxConfiguration.currentText()
        text, ok = QInputDialog().getText(self, "Configuration name",
                                          "Configuration name:", QLineEdit.Normal, defText)
        conf = mainWidget.ui.comboBoxConfiguration.currentIndex()
        if ok and text and (conf > -1):
            commandSets.setMidiConfigurationName(self, serialHandler, simpleFARHandler, conf, text)
            #serialHandler.write("midiconfiguration:" + str(conf) + ",midiconfigurationname:" + text)
            mainWidget.ui.comboBoxConfiguration.setItemText(conf, text)

    def configurationAdd(self):
        defText = mainWidget.ui.comboBoxConfiguration.currentText()
        text, ok = QInputDialog().getText(self, "Configuration name","Configuration name:", QLineEdit.Normal, defText)
        if ok and text:
            if (find_item(mainWidget.ui.comboBoxConfiguration, text) != -1):
                messageBox("Error", "Name already exists!")
                return
            commandSets.addMidiConfiguration(self, serialHandler, simpleFARHandler, text)
            mainWidget.ui.comboBoxConfiguration.addItem(text)

    def configurationRemove(self):
        config = int(self.ui.comboBoxConfiguration.currentIndex())
        if (config < 0) or (self.ui.comboBoxConfiguration.count() == 0):
            return
        commandSets.removeMidiConfiguration(self, serialHandler, simpleFARHandler, config)
        self.ui.comboBoxConfiguration.removeItem(config)
        #serialHandler.write("midiconfigurationremove:" + str(config) + ",rqi:mcfc,rqi:mcf")

    def configurationSet(self):
        if (self.updatingFromModule):
            return
        config = int(mainWidget.ui.comboBoxConfiguration.currentIndex())
        if (config < 0) or (mainWidget.ui.comboBoxConfiguration.count() == 0):
            return
        commandSets.setMidiConfigurationSelect(self, serialHandler, simpleFARHandler, config)

#    def selectMIDIDevice(self, Index):
#        if mainWidget.ui.comboBoxMIDILearnDevice.currentIndex() == -1:
#            return

    def ccAdd(self):
        cc, ok = QInputDialog.getInt(self, "CC Number", "CC Number")
        if ok and (cc > -1 and cc < 128):
            index = mainWidget.ui.listWidgetMidiEvents.findItems("CC " + str(cc), Qt.MatchFlag.MatchExactly)
            if (len(index) != 0):
                messageBox("Error", "Event already exists!")
                return
            commandSets.addMidiConfigurationCC(self, serialHandler, simpleFARHandler, cc)
            if (find_item(self.ui.listWidgetMidiEvents, "CC " + str(cc)) == -1):
                mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("CC " + str(cc)))
            #self.updateUIData()

    def ccRemove(self):
        if (mainWidget.ui.listWidgetMidiEvents.currentIndex() == -1):
            return
        if (mainWidget.ui.listWidgetMidiEvents.currentItem().text()[0:2] != "CC"):
            return
        text = mainWidget.ui.listWidgetMidiEvents.currentItem().text()
        commandSets.removeMidiConfigurationCC(self, serialHandler, simpleFARHandler, text[3:len(text)])
        if (find_item(self.ui.listWidgetMidiEvents, "CC " + str(cc)) != -1):
            remove_item(self.ui.listWidgetMidiEvents, "CC " + str(cc))
        #self.updateUIData()

    def cmdNoteOnUpdate(self, widget = None):
        if self.updatingFromModule:
            return

        solenoidEngage = commandSets.getQualifiedShortCommand(CommandID.solenoidEngage, None, True)[0]
        muteRest = commandSets.getQualifiedShortCommand(CommandID.muteRest, None, True)[0]

        currentConfig = simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect)
        mapCmd = commandSets.getQualifiedShortCommand(CommandID.midiConfigurationData, [currentConfig])[0]

        cl = commandSets.currentCommandSet.CommandList(simpleFARHandler.instrumentMaster.evNoteOn)
        cmd = cl.buildCommandString({solenoidEngage, muteRest})

        if self.ui.midiNoteOnVelToHammer.value() > 0:
            cmd += "," + solenoidEngage + ":(velocity*" + str(self.ui.midiNoteOnVelToHammer.value()) + ")"
            if self.ui.midiNoteOnHammerStaccato.checkState() == Qt.CheckState.Checked:
                cmd += "*(1-notecount)"
        if self.ui.midiNoteOnSendMuteRest.checkState() == Qt.CheckState.Checked:
            cmd += "," + muteRest + ":1"
        serialString = mapCmd + ":noteon:\"" + cmd + "\""
        serialHandler.write(serialString)
        #self.updateUIData()

    def cmdNoteOffUpdate(self):
        if self.updatingFromModule:
            return

        muteFull = commandSets.getQualifiedShortCommand(CommandID.muteFullMute, None, True)[0]
        motorRun = commandSets.getQualifiedShortCommand(CommandID.motorRun, None, True)[0]

        currentConfig = simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect)
        mapCmd = commandSets.getQualifiedShortCommand(CommandID.midiConfigurationData, [currentConfig])[0]

        cl = commandSets.currentCommandSet.CommandList(simpleFARHandler.instrumentMaster.evNoteOff)
        cmd = cl.buildCommandString({muteFull, motorRun})

        if self.ui.midiNoteOffSendFullMute.checkState() == Qt.CheckState.Checked:
            cmd += "," + muteFull + ":1"
        if self.ui.midiNoteOffMotorOff.checkState() == Qt.CheckState.Checked:
            cmd += "," + motorRun + ":0"
        serialString = cmd + ":noteoff:\"" + cmd + "\""
        serialHandler.write(serialString)
        #self.updateUIData()

    def addTuningSchemes(self):
        mainWidget.ui.listWidgetTuningscheme.addItem("Just intonation")
        mainWidget.ui.listWidgetTuningscheme.addItem("Equal temperament")

    def tuningSchemeChanged(self, current, previous):
        mainWidget.populateFundamentalComboBox()
        pass

    def comboBoxMidiChannelIndexChanged(self):
        if mainWidget.ui.comboBoxMidiChannel.currentText() == "Omni":
            ch = 0
        else:
            ch = int(mainWidget.ui.comboBoxMidiChannel.currentText())
        #serialHandler.write("mrc:" + str(ch))

        currentConfig = simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect)
        mrc = commandSets.getQualifiedShortCommand(CommandID.midiReceiveChannel, [currentConfig])
        for comm in mrc:
            serialHandler.write(comm + ":" + str(ch))

    def populateFundamentalComboBox(self):
        mainWidget.ui.comboBoxFundamentalFrequency.clear()

        try:
            if ((self.ui.listWidgetTuningscheme.currentItem().text()) == "Equal temperament"):
                noteDataArray = scaleDataEqual
            else:
                noteDataArray = scaleDataJust
        except:
            noteDataArray = scaleDataJust

        base = 55 / 2   #110 / 4
        for octave in range(0, 2):  #3
            for note in range (0, 11):
                mainWidget.ui.comboBoxFundamentalFrequency.addItem(noteDataArray[2][note] + " " + str(round((pow(2, octave)*base) * noteDataArray[1][note], 2)))

    def comboBoxFundamentalFrequencyIndexChanged(self):
        text = mainWidget.ui.comboBoxFundamentalFrequency.currentText()
        if text == "":
            return
        mainWidget.ui.doubleSpinBoxFundamentalFrequency.setValue(float(mainWidget.ui.comboBoxFundamentalFrequency.currentText()[3:len(text)]))

    def mouseReleaseEventIntermediate(self, event, widget):
        widget.mouseReleaseFunction(widget)
        if type(widget) == QSlider:
            QSlider.mouseReleaseEvent(widget, event)

#    def assignMouseReleaseEvent(self, qtObject, function):
#        qtObject.mouseReleaseEvent = lambda event: self.mouseReleaseEventIntermediate(event, qtObject)
#        qtObject.mouseReleaseFunction = function

    def showModalWait(self, issueCommand, resultCommand, progressTime, title, timeOut = False):
        isc = commandSets.getQualifiedShortCommand(issueCommand)[0]
        serialHandler.write(isc)
        self.modalEvent = resultCommand
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        self.modalDialog = waitdialog.ProgressDialog(progressTime, title) # Just sent to highest, was 16000
        self.modalDialog.start(timeOut)

        self.modalEvent = ""
        self.modalDialog = None

    def dialogSignaler(self):
        widget = self.sender()
        self.showModalWait(widget.issueCommand, widget.resultCommand, 20000, "Calibrating")

    def connectSignalToModalDialog(self, widget, issueCommand, resultCommand):
        widget.issueCommand = issueCommand
        widget.resultCommand = resultCommand
        if isinstance(widget, QPushButton):
            widget.pressed.connect(self.dialogSignaler)

    def pickupAnalyse(self):
        saveState = mainWidget.ui.checkBoxContinuousSMData.checkState()
        mainWidget.ui.checkBoxContinuousSMData.setChecked(True)
        forceMult = commandSets.getQualifiedShortCommand(CommandID.solenoidForceMultiplier)[0]
        en = commandSets.getQualifiedShortCommand(CommandID.solenoidEngage)[0]
        serialHandler.write(forceMult + ":1," + en + ":65535")
        mainWidget.showModalWait("", "", 2500, "Analysing", True)
        mainWidget.ui.checkBoxContinuousSMData.setCheckState(saveState)
        pass

    def resetAllSettings(self):
        msgBox = QMessageBox.warning(self, "WHOOPS COMPLETE RESET",
                                     "This will reset ALL SETTINGS in your Ekdahl FAR and then restart the instrument, you sure?",
                                     buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     defaultButton=QMessageBox.StandardButton.No)
        if msgBox == QMessageBox.StandardButton.Yes:
            saveAll = commandSets.getQualifiedShortCommand(CommandID.saveAllParameters)
            reset = commandSets.getQualifiedShortCommand(CommandID.reset)
            serialHandler.write(saveAll + "," + reset + ":1")
        pass

    def waitForSerialResponse(self, command, timeout = 5000):
        self.waitForCommand = command
        self.isWaitingForCommand = True
        startTime = time.monotonic()
        while(self.isWaitingForCommand):

            if time.monotonic() - starTime > (timeout / 1000):
                break
        if not self.isWaitingForCommand:
            self.isWaitingForCommand = True
            return False
        return True

import math

# Base note at octave 5
scaleDataJust = [440, [1, 1.06667, 1.125, 1.2, 1.25, 1.3333, 1.40625, 1.5, 1.6, 1.66667, 1.8, 1.875],
                 ["A-", "A#", "B-", "C-", "C#", "D-", "D#", "E-", "F-", "F#", "G-", "G#"]]
scaleDataEqual = [440, [1, 1.059463094, 1.122462048, 1.189207115, 1.259921050, 1.334839854, 1.414213562, 1.498307077, 1.587401052, 1.681792831, 1.781797436, 1.887748625],
                  ["A-", "A#", "B-", "C-", "C#", "D-", "D#", "E-", "F-", "F#", "G-", "G#"]]

def getBaseNoteFromFrequency(frequency, noteDataArray):
    oct0f = noteDataArray[0] / 32
    octave = 5
    while math.trunc(frequency / (oct0f * 2 ** octave)) < 2:
        octave -= 1
    octave += 1
    measBaseline = oct0f * 2 ** (octave)
    for note in range(0, len(noteDataArray[1])):
        if measBaseline * noteDataArray[1][note] > frequency: break

# if we're still under we're just at the break of the next octave
    if measBaseline * noteDataArray[1][note] <= frequency:
        note = 11

    note -= 1
    cents = math.log2(frequency / (measBaseline * noteDataArray[1][note])) * 1200
#  if we are over 60 we should convert to negative by recalculating towards the next note
    if (cents > 60):
        print ("too much, try again")
        note += 1
        cents = math.log2(frequency / (measBaseline * noteDataArray[1][note])) * 1200
#  if we're still over we're at the break of an octave
        if (cents > 60):
            octave += 1
            measBaseline = oct0f * 2 ** (octave)
            note = 0
            cents = math.log2(frequency / (measBaseline * noteDataArray[1][note])) * 1200

    noteName = noteDataArray[2][note]
    return octave, note, cents, noteName

class settingsType(enum.Enum):
    Geometry = enum.auto()
    Visibility = enum.auto()
    checkState = enum.auto()

def settingsDeclaration():
    su = serialWidget.ui
    mu = mainWidget.ui
    return  [["mainGeometry", mainWidget, settingsType.Geometry],["consoleGeometry", serialWidget, settingsType.Geometry],
           ["consoleWindowVisible", serialWidget, settingsType.Visibility],["filterHardware", su.checkBoxFilterHardware, settingsType.checkState],
           ["filterUSB", su.checkBoxFilterUSB, settingsType.checkState],["filterDebug", su.checkBoxFilterDebug, settingsType.checkState],
           ["filterDebug", su.checkBoxFilterDebug, settingsType.checkState],["filterError", su.checkBoxFilterError, settingsType.checkState],
           ["filterOutput", su.checkBoxFilterOutput, settingsType.checkState],["filterPriority", su.checkBoxFilterPriority, settingsType.checkState],
           ["filterUndefined", su.checkBoxFilterUndefined, settingsType.checkState],["filterCommAck", su.checkBoxFilterCommAck, settingsType.checkState],
           ["filterExpressionParser", su.checkBoxFilterExpressionParser, settingsType.checkState],["filterInfoRequest", su.checkBoxFilterInfoRequest, settingsType.checkState],
           ["filterInternal", su.checkBoxFilterInternal, settingsType.checkState],["consoleLineLimit", su.checkBoxLimitLines, settingsType.checkState],
           ["consoleCursorFollow", su.checkBoxDebugCursorFollow, settingsType.checkState],["chartA0", mu.checkBoxChartA0, settingsType.checkState],
           ["chartA1", mu.checkBoxChartA1, settingsType.checkState],["chartA2", mu.checkBoxChartA2, settingsType.checkState],
           ["chartA3", mu.checkBoxChartA3, settingsType.checkState],["chartA4", mu.checkBoxChartA4, settingsType.checkState],
           ["chartA5", mu.checkBoxChartA5, settingsType.checkState],["chartA6", mu.checkBoxChartA6, settingsType.checkState],
           ["chartA7", mu.checkBoxChartA7, settingsType.checkState],["chartAudPk", mu.checkBoxChartAudPk, settingsType.checkState],
           ["chartMotFreq", mu.checkBoxChartMotFreq, settingsType.checkState],["chartPeakErr", mu.checkBoxChartPeakErr, settingsType.checkState],
           ["chartMotCurr", mu.checkBoxChartMotCurr, settingsType.checkState],["chartReadFreq", mu.checkBoxChartReadFreq, settingsType.checkState],
           ["chartAudFFT", mu.checkBoxChartAudFFT, settingsType.checkState],["chartAudRMS", mu.checkBoxChartAudRMS, settingsType.checkState],
           ["referenceGeometry", commandReference, settingsType.Geometry],["referenceWindowVisible", commandReference, settingsType.Visibility]]

def save_settings():
    # Save window geometry using QSettings
    settings = QSettings("Knas", "Ekdahl FAR Config")
    for set in settingsDeclaration():
        match(set[2]):
            case settingsType.checkState:
                settings.setValue(set[0], set[1].checkState())
            case settingsType.Visibility:
                settings.setValue(set[0], set[1].isVisible())
            case settingsType.Geometry:
                settings.setValue(set[0], set[1].saveGeometry())

def loadCheckState(settings, name, checkBox):
    state = settings.value(name)
    if state == Qt.CheckState.Checked or state == 'Checked':
        checkBox.setCheckState(Qt.CheckState.Checked)
    else:
        checkBox.setCheckState(Qt.CheckState.Unchecked)

def load_settings():
    # Load window geometry using QSettings
    settings = QSettings("Knas", "Ekdahl FAR Config")
    for set in settingsDeclaration():
        try:
            match(set[2]):
                case settingsType.checkState:
                    loadCheckState(settings, set[0], set[1])
                case settingsType.Visibility:
                    set[1].setVisible(bool(settings.value(set[0])))
                case settingsType.Geometry:
                    geometry = settings.value(set[0])
                    if geometry: set[1].restoreGeometry(geometry)
        except:
            pass

def showConsole():
    serialWidget.show()
    serialWidget.raise_()
    serialWidget.activateWindow()
    serialWidget.ui.lineEditSend.setFocus()

def showReference():
    commandReference.show()
    commandReference.raise_()
    commandReference.activateWindow()
    commandReference.ui.listWidgetCommands.setFocus()

#post = False
def organize():
    #global post
    #if not post:
    #    localNodehandler.postBuildUpdate()
    #    post = True
    #else:

    #localNodehandler.redraw()

    localNodehandler.postBuildUpdate()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    mainWidget = FarConfig()

    serialWidget = SerialWidget(serialHandler, mainWidget.timeStamper, logging)

    commandReference = CommandReference()

    mainWidget.setObjectName("main")
    serialWidget.setObjectName("console")
    serialWidget.setObjectName("reference")

    mainWidget.show()

## Hiding old
    mainWidget.ui.horizontalSliderBowCurrent.setVisible(False)
    mainWidget.ui.horizontalSliderBowFrequency.setVisible(False)
    mainWidget.ui.pushButtonActuatorLoad.setVisible(False)
## Hiding until implemented
    mainWidget.ui.pushButtonAddHarmonicListFile.setVisible(False)
    mainWidget.ui.pushButtonCCAddLearn.setVisible(False)
    mainWidget.ui.pushButtonDetectFundamental.setVisible(False)
    mainWidget.ui.pushButtonCalibrateHammer.setVisible(False)

## Global commands
    mainWidget.ui.pushButtonConnectDisconnect.pressed.connect(mainWidget.connectDisconnect)
    mainWidget.ui.pushButtonSaveToModule.pressed.connect(mainWidget.pushButtonSaveToModulePressed)
    mainWidget.ui.pushButtonLoadFromModule.pressed.connect(mainWidget.pushButtonLoadFromModulePressed)
    mainWidget.ui.checkBoxContinuousSMData.toggled.connect(mainWidget.checkBoxContinuousSMDataToggled)
    mainWidget.ui.pushButtonShowConsole.pressed.connect(showConsole)
    mainWidget.ui.pushButtonShowReference.pressed.connect(showReference)

## Tab Basic settings
    mainWidget.ui.pushButtonPickupAnalyse.pressed.connect(mainWidget.pickupAnalyse)

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxFundamentalFrequency, CommandID.bowFundamental)
    mainWidget.ui.comboBoxBaseNote.currentIndexChanged.connect(mainWidget.comboBoxBaseNotePressed)
    mainWidget.ui.comboBoxFundamentalFrequency.currentIndexChanged.connect(mainWidget.comboBoxFundamentalFrequencyIndexChanged)
    mainWidget.ui.listWidgetTuningscheme.currentItemChanged.connect(mainWidget.tuningSchemeChanged)

    mainWidget.connectSignalToModalDialog(mainWidget.ui.pushButtonCalibrateAll, CommandID.calibrateAll, CommandID.calibrateAll)

    mainWidget.ui.comboBoxHarmonicList.currentIndexChanged.connect(mainWidget.comboBoxHarmonicListCurrentIndexChanged)
    mainWidget.ui.pushButtonAddHarmonic.pressed.connect(mainWidget.pushButtonAddHarmonicPressed)
    mainWidget.ui.pushButtonRemoveHarmonic.pressed.connect(mainWidget.pushButtonRemoveHarmonicPressed)
    mainWidget.ui.pushButtonLoadHarmonicPreset.pressed.connect(mainWidget.pushButtonLoadHarmonicPresetPressed)
    #mainWidget.ui.pushButtonSaveCurrentHarmonicList.pressed.connect(mainWidget.pushButtonSaveCurrentHarmonicListPressed)
    #mainWidget.ui.pushButtonSaveNewHarmonicList.pressed.connect(mainWidget.pushButtonSaveNewHarmonicListPressed)
    mainWidget.ui.pushButtonRenameHarmonicList.pressed.connect(mainWidget.pushButtonRenameHarmonicListPressed)
    mainWidget.ui.pushButtonAddHarmonicList.pressed.connect(mainWidget.pushButtonAddHarmonicListPressed)
    mainWidget.ui.pushButtonAddHarmonicListFile.pressed.connect(mainWidget.pushButtonAddHarmonicListFilePressed)
    mainWidget.ui.pushButtonRemoveHarmonicList.pressed.connect(mainWidget.pushButtonRemoveHarmonicListPressed)
    '''
    mainWidget.ui.pushButtonSaveCurrentHarmonicList.setVisible(False)
    mainWidget.ui.pushButtonSaveNewHarmonicList.setText("Rename")
    mainWidget.ui.pushButtonActuatorSave.setText("Add")
    mainWidget.ui.pushButonActuatorSaveNew.setText("Rename")
    mainWidget.ui.pushButtonActuatorDelete.setText("Remove")
    '''
## Tab Midi settings
    mainWidget.ui.comboBoxMidiChannel.currentIndexChanged.connect(mainWidget.comboBoxMidiChannelIndexChanged)

    mainWidget.ui.comboBoxConfiguration.currentIndexChanged.connect(mainWidget.configurationSet)
    #mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonConfigurationAdd, "mcfa", True)
    mainWidget.ui.pushButtonConfigurationAdd.pressed.connect(mainWidget.configurationAdd)
    mainWidget.ui.pushButtonConfigurationRemove.pressed.connect(mainWidget.configurationRemove)
    mainWidget.ui.pushButtonConfigurationName.pressed.connect(mainWidget.configurationSetName)

    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonMidiRestoreDefaults, CommandID.midiConfigurationDefaults, True)

    #mainWidget.assignMouseReleaseEvent(mainWidget.ui.midiNoteOnVelToHammer, mainWidget.cmdNoteOnUpdate)
    mainWidget.ui.midiNoteOnVelToHammer.sliderReleased.connect(mainWidget.cmdNoteOnUpdate)

    mainWidget.ui.midiNoteOnHammerStaccato.stateChanged.connect(mainWidget.cmdNoteOnUpdate)
    mainWidget.ui.midiNoteOnSendMuteRest.stateChanged.connect(mainWidget.cmdNoteOnUpdate)

    mainWidget.ui.midiNoteOffSendFullMute.stateChanged.connect(mainWidget.cmdNoteOffUpdate)
    mainWidget.ui.midiNoteOffMotorOff.stateChanged.connect(mainWidget.cmdNoteOffUpdate)

    mainWidget.midiEventHandler.populateComboBoxSendByte(mainWidget.ui.midiPitchbendSend)
    mainWidget.midiEventHandler.connectWidgetsToMIDIEvent("pb", { mainWidget.ui.midiPitchbendSend, mainWidget.ui.midiPitchbendRatio })
    mainWidget.midiEventHandler.populateComboBoxSendByte(mainWidget.ui.midiPolyATSend)
    mainWidget.midiEventHandler.connectWidgetsToMIDIEvent("pat", { mainWidget.ui.midiPolyATSend, mainWidget.ui.midiPolyATRatio })
    mainWidget.midiEventHandler.populateComboBoxSendByte(mainWidget.ui.midiChannelATSend)
    mainWidget.midiEventHandler.connectWidgetsToMIDIEvent("cat", { mainWidget.ui.midiChannelATSend, mainWidget.ui.midiChannelATRatio })

    mainWidget.midiEventHandler.populateComboBoxSendBinary(mainWidget.ui.midiSustainSend)
    mainWidget.midiEventHandler.connectWidgetsToBinarySenders("sustain", { mainWidget.ui.midiSustainInvert, mainWidget.ui.midiSustainSend })

    mainWidget.ui.listWidgetMidiEvents.currentItemChanged.connect(mainWidget.midiEventHandler.listWidgetMidiEventscurrentItemChanged)
    mainWidget.ui.lineEditMidiEventCommand.editingFinished.connect(mainWidget.lineEditMidiEventCommandFinished)
    mainWidget.ui.pushButtonCCAdd.pressed.connect(mainWidget.ccAdd)
    mainWidget.ui.pushButtonCCRemove.pressed.connect(mainWidget.ccRemove)

## Tab CV Mapping
    mainWidget.cvEventHandler.connectCVMappingModifiers(0, { mainWidget.ui.dialCVHarmonicScale, mainWidget.ui.widgetCVHarmonicNoteOffset,
                                              mainWidget.ui.widgetCVHarmonicZero})
    mainWidget.cvEventHandler.connectCVTextWidgets(0, mainWidget.ui.plainTextEditCVHarmonicCommands)

    mainWidget.cvEventHandler.connectCVMappingModifiers(1, { mainWidget.ui.dialCVHarmonicShiftScale, mainWidget.ui.dialCVHarmonicShiftZero })
    mainWidget.cvEventHandler.connectCVTextWidgets(1, mainWidget.ui.plainTextEditCVHarmonicShiftCommands)
    mainWidget.ui.pushButtonCVHarmonicShiftZeroCalibrate.pressed.connect(mainWidget.cvEventHandler.CVHarmonicShiftZeroCalibrate)

    mainWidget.cvEventHandler.connectCVMappingModifiers(2, { mainWidget.ui.dialCVFineTuneCenter })
    mainWidget.cvEventHandler.connectCVTextWidgets(2, mainWidget.ui.plainTextEditCVFineTuneCommands)
    mainWidget.ui.pushButtonCVFinetuneCalibrate.pressed.connect(mainWidget.cvEventHandler.CVFinetuneCalibrate)

    mainWidget.cvEventHandler.connectCVTextWidgets(3, mainWidget.ui.plainTextEditCVPressureCommands)
    mainWidget.cvEventHandler.connectCVTextWidgets(4, mainWidget.ui.plainTextEditCVHammerTriggerCommands)

    mainWidget.cvEventHandler.connectCVMappingModifiers(5, { mainWidget.ui.checkBoxCVGateHold, mainWidget.ui.checkBoxCVGateEngage,
                                              mainWidget.ui.checkBoxCVGatePowerMotor, mainWidget.ui.widgetCVGateThreshold})
    mainWidget.cvEventHandler.connectCVTextWidgets(5, mainWidget.ui.plainTextEditCVGateCommands)

    mainWidget.cvEventHandler.connectCVTextWidgets(6, mainWidget.ui.plainTextEditCVHammerScaleCommands)
    mainWidget.cvEventHandler.connectCVTextWidgets(7, mainWidget.ui.plainTextEditCVMuteCommands)

    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonResetADCSettings, CommandID.controlBoxControlDefaults, True)
## Tab Adanced

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorMaxSpeed, CommandID.pidSpeedMax)
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorMinSpeed, CommandID.pidSpeedMin)

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorPIDKp, CommandID.pidKp)
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorPIDKi, CommandID.pidKi)
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorPIDKd, CommandID.pidKd)
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorPIDie, CommandID.pidIntegratorError)
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorMaxError, CommandID.pidMaxError)

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorVoltage, CommandID.motorVoltage)
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorTimeout, CommandID.bowMotorTimeout)
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonCalibrateMotorSpeed, CommandID.calibrateBowSpeed)

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMaxPressure, CommandID.bowPressurePositionMax)
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMinPressure, CommandID.bowPressurePositionEngage)
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowRestPosition, CommandID.bowPressurePositionRest)
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonRestBow, [CommandID.bowPressurePositionRest, "0", CommandID.bowPressureRest, "1"]) # "bppr:0,bpr:1"
    mainWidget.connectSignalToModalDialog(mainWidget.ui.pushButtonCalibratePressure, CommandID.calibrateBowPressure, CommandID.calibrateBowPressure)

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxMuteFullMutePosition, CommandID.muteFullMutePosition)
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxMuteHalfMutePosition, CommandID.muteHalfMutePosition)
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxMuteRestPosition, CommandID.muteRestPosition)
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxMuteBackoff, CommandID.muteBackoff)
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonRestMute, [CommandID.muteRestPosition, "0", CommandID.muteRest, "1"])
    mainWidget.connectSignalToModalDialog(mainWidget.ui.pushButtonCalibrateMute, CommandID.calibrateMute, CommandID.calibrateMute)

    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonMuteFullTest, [CommandID.muteFullMute, "1" ])
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonMuteHalfTest, [CommandID.muteHalfMute, "1" ])
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonMuteRestTest, [CommandID.muteRest, "1" ])

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxSolenoidMaxForce, CommandID.solenoidMaxForce)
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxSolenoidMinForce, CommandID.solenoidMinForce)
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxSolenoidEngageDuration, CommandID.solenoidEngageDuration)

#    mainWidget.ui.pushButtonActuatorSave.pressed.connect(mainWidget.pushButtonActuatorSavePressed)
    mainWidget.ui.comboBoxActuatorPreset.currentIndexChanged.connect(mainWidget.comboBoxActuatorIndexChanged)
#    mainWidget.ui.pushButonActuatorSaveNew.pressed.connect(mainWidget.pushButonActuatorSaveNewPressed)
   # mainWidget.ui.pushButtonActuatorLoad.pressed.connect(mainWidget.pushButtonActuatorLoadPressed)
    mainWidget.ui.pushButtonActuatorRemove.pressed.connect(mainWidget.pushButtonAcutatorRemovePressed)
    mainWidget.ui.pushButtonActuatorAdd.pressed.connect(mainWidget.pushButtonActuatorAddPressed)
    mainWidget.ui.pushButtonActuatorRename.pressed.connect(mainWidget.pushButtonActuatorRenamePressed)

    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonBowMaxPressureTest, [CommandID.bowPressureModifier, "0", CommandID.bowPressureBaseline, "65535"])
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonBowEngagePressureTest, [CommandID.bowPressureModifier, "0", CommandID.bowPressureBaseline, "65535", CommandID.bowPressureEngage, "1"])
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonBowRestPressureTest, [CommandID.bowPressureModifier, "0", CommandID.bowPressureBaseline, "65535", CommandID.bowPressureRest, "1"])
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonSolenoidMaxForceTest, [CommandID.solenoidForceMultiplier, "1", CommandID.solenoidEngage, "65535"])
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonSolenoidMinForceTest, [CommandID.solenoidForceMultiplier, "1", CommandID.solenoidEngage, "1"])
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonEngageHammer, [CommandID.solenoidEngage, "65535"])
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonHammerDurationTest, [CommandID.solenoidForceMultiplier, "1", CommandID.solenoidEngage, "65535"])

    mainWidget.assignValueChanged(mainWidget.ui.spinBoxHarmonicShiftRange, CommandID.bowHarmonicShiftRange)
    mainWidget.ui.comboBoxCurrentlySelectedModule.currentIndexChanged.connect(mainWidget.comboBoxCurrentSelectedModuleIndexChanged)
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonHomeBow, CommandID.bowHome, True)
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonHomeMute, CommandID.muteHome, True)
    mainWidget.ui.pushButtonResetAllSettings.pressed.connect(mainWidget.resetAllSettings)

## Tab Debugging
    mainWidget.ui.tableViewScale = tableTest.customTableView(mainWidget.ui.groupBox_3)
    mainWidget.ui.tableViewScale.horizontalHeader().setDefaultSectionSize(70)
    mainWidget.ui.tableViewScale.horizontalHeader().setMinimumSectionSize(18)
    mainWidget.ui.tableViewScale.verticalHeader().setDefaultSectionSize(30)
    mainWidget.ui.tableViewScale.verticalHeader().setMinimumSectionSize(22)
    mainWidget.ui.layoutHarmonicTable.replaceWidget(mainWidget.ui.xtableViewScale, mainWidget.ui.tableViewScale)
    mainWidget.ui.tableViewScale.setModel(tableTest.CustomTableModel())

    delegate = tableTest.noneDelegate()
    mainWidget.ui.tableViewScale.setItemDelegateForRow(0, delegate)
    mainWidget.ui.tableViewScale.model().dataChanged.connect(mainWidget.tableViewScaleDataChanged)

    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA0, CommandID.controlBoxDataReturn, 0, timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA1, CommandID.controlBoxDataReturn, 1, timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA2, CommandID.controlBoxDataReturn, 2, timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA3, CommandID.controlBoxDataReturn, 3, timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA4, CommandID.controlBoxDataReturn, 4, timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA5, CommandID.controlBoxDataReturn, 5, timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA6, CommandID.controlBoxDataReturn, 6, timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA7, CommandID.controlBoxDataReturn, 7, timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartAudPk, CommandID.pickupAudioPeak, -1, timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartAudRMS, CommandID.pickupAudioRMS, -1, timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartAudFFT, CommandID.pickupStringFrequency, -1, timedChart.seriesType.frequency)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartMotFreq, CommandID.motorFrequency, -1, timedChart.seriesType.frequency)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartReadFreq, CommandID.pidTargetFreq, -1, timedChart.seriesType.frequency)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartPeakErr, CommandID.pidPeakError, -1, timedChart.seriesType.frequency)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartMotCurr, CommandID.motorCurrent, -1, timedChart.seriesType.integer)

    mainWidget.ui.pushButtonClearAverages.pressed.connect(mainWidget.cvEventHandler.averagesClear)
    mainWidget.ui.pushButtonTestAverages.pressed.connect(mainWidget.cvEventHandler.averagesTest)

    #mainWidget.completerList = [ "banana", "apple", "orange" ]
    mainWidget.completerList = []
    #mainWidget.completer = QCompleter(mainWidget.completerList)
    mainWidget.serialWidget = serialWidget
    #serialWidget.ui.lineEditSend.setCompleter(mainWidget.completer)
## Plugin tab
    mainWidget.pluginHandler = pluginhandler.PluginHandler(mainWidget, serialHandler, simpleFARHandler)
    #self.ui = Ui_Widget()
    #self.ui.setupUi(self)
    #self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    #self.focusing = False

## Default settings
    mainWidget.addTuningSchemes()
    mainWidget.setUIEnabled(True)
    mainWidget.ui.tabWidgetMain.setCurrentIndex(0)

## Console widget
    serialWidget.ui.spinBoxLimitLines.setValue(2500)
    serialWidget.ui.checkBoxLimitLines.setCheckState(Qt.CheckState.Checked)
    serialWidget.ui.checkBoxFilterInfoRequest.setCheckState(Qt.CheckState.Unchecked)
    serialWidget.ui.checkBoxFilterOutput.setCheckState(Qt.CheckState.Unchecked)
    serialWidget.checkBoxFilterInfoRequestToggled()
    serialWidget.checkBoxFilterOutputToggled()
    serialWidget.ui.checkBoxFilterUSB.setCheckState(Qt.CheckState.Checked)
    serialWidget.ui.checkBoxFilterHardware.setCheckState(Qt.CheckState.Unchecked)
    serialWidget.ui.checkBoxFilterExpressionParser.setCheckState(Qt.CheckState.Unchecked)
    serialWidget.ui.checkBoxFilterCommAck.setCheckState(Qt.CheckState.Checked)
    serialWidget.ui.checkBoxFilterDebug.setCheckState(Qt.CheckState.Unchecked)
    serialWidget.ui.checkBoxFilterPriority.setCheckState(Qt.CheckState.Checked)
    serialWidget.ui.checkBoxFilterError.setCheckState(Qt.CheckState.Checked)
    serialWidget.ui.checkBoxFilterUndefined.setCheckState(Qt.CheckState.Checked)
    serialWidget.checkBoxDebugCursorFollowToggled()

    serialWidget.ui.plainTextEditSerialOutput.setUndoRedoEnabled(False)
# Command reference form

#stringModule inits
    strm = stringModule()
    simpleFARHandler.stringModules.append(strm)

# pre-start inits
    load_settings()

    localNodehandler = None
    localNodehandler = nodehandler.NodeHandler(mainWidget.ui.nodeContainer)
    mainWidget.localNodeHandler = localNodehandler
    mainWidget.ui.pushButtonOrganize.pressed.connect(organize)

    mainWidget.commandReference = commandReference

    mainWidget.destroyed.connect(mainWidget.closeEvent)
    mainWidget.populateFundamentalComboBox()
    mainWidget.USBRefreshTimer = QTimer()
    mainWidget.USBRefreshTimer.timeout.connect(mainWidget.populateSerialPorts)
    mainWidget.USBRefreshTimer.start(1000)

    serialWidget.addToDebugWindow("Initialized\n")
    sys.exit(app.exec())
    mainWidget.thread1.terminate()

