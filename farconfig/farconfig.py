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

import platform, sys, time, os # random, datetime,
import serial.tools.list_ports
from PySide6.QtWidgets import (QApplication, QWidget, QDoubleSpinBox, QListWidgetItem, QInputDialog, QMessageBox, QLineEdit, QSpinBox,
                               QComboBox, QSlider, QTabBar, QTabWidget, QCheckBox, QDial, QPushButton, QListWidget, QDockWidget, QSizePolicy,
                               QVBoxLayout, QMainWindow, QHBoxLayout, QLabel, QGraphicsScene, QGraphicsView, QFrame)
# QTextEdit, QAbstractButton, QStackedWidget,
from PySide6.QtCore import QThread, Signal, QTimer, Qt, Slot, QSettings, QSize
from PySide6.QtGui import QIcon, QPainter
import logging
from logging.handlers import RotatingFileHandler

import enum
import math

#import equationParsingHelpers
import waitdialog
#import tableTest

from commandparser import CommandItem, Derivedcommanditem
from general_helpers import messageBox, inputBox, find_item #, remove_item
from ui_form import Ui_Widget

from serialWidget import SerialWidget as SerialWidget #, ReportTypeEnum
from commandReference import commandReference as CommandReference
from preferences import preferences as preferences
import timedChart

from CommandSets import CommandSets, Derivedcommanditem, Derivedcommandlist, CommandSetModular  # CommandID, CommandType,
from ModuleSystem import Module, ModuleCommand, HelpCommand, HelpModule
from GUICallbackSystem import GUICallbackSystem, GUICallback

from pluginhandler import PluginHandler
import nodehandler

from tabbasic import TabBasic
from tabadvanced import TabAdvanced
from tabmidi import TabMIDI
from tabcv import TabCV

global serialStream
commandSets = CommandSets()
app = None

def processInformationReturn(inSerialHandler, infoReturn):
    global commandSets
    commandList = Derivedcommandlist(infoReturn)

    mainWidget.updatingFromModule = True

    for i in commandList.commands:
        if (i.command == "ver"):
            if (commandSets.currentCommandSet is None) or (commandSets.currentCommandSet.loadingStage == 0):
                if (len(i.argument) == 4):
                    commandSets.chooseCommandSet(i.argument[3])
                else:
                    commandSets.chooseCommandSet(i.argument[0])

                mainWidget.guiCallbackSystem = GUICallbackSystem(mainWidget, commandSets.currentCommandSet, serialHandler)
                mainWidget.pluginHandler = PluginHandler(mainWidget, serialHandler, commandSets.currentCommandSet, mainWidget.guiCallbackSystem)
                mainWidget.tabBasic = TabBasic(mainWidget, serialHandler, commandSets.currentCommandSet, mainWidget.guiCallbackSystem)
                mainWidget.tabAdvanced = TabAdvanced(mainWidget, serialHandler, commandSets.currentCommandSet, mainWidget.guiCallbackSystem)
                mainWidget.tabMIDI = TabMIDI(mainWidget, serialHandler, commandSets.currentCommandSet, mainWidget.guiCallbackSystem)
                mainWidget.tabCV = TabCV(mainWidget, serialHandler, commandSets.currentCommandSet, mainWidget.guiCallbackSystem)
                mainWidget.completerList.clear()

        if (commandSets.processMessages(i, commandSets, mainWidget, serialHandler)):
            pass

        if (i.command == "nop") and (commandSets.currentCommandSet.loadingStage == 3):
            mainWidget.localNodeHandler.commandSet = commandSets.currentCommandSet
            mainWidget.localNodeHandler.addDynamicNodeSet(commandSets.currentCommandSet.baseModule)

        if (commandSets.currentCommandSet.loadingStage == 4) and (mainWidget.updateStage < 2):
            moduleCommand, module = commandSets.currentCommandSet.getCommandAndModule(i)
            if (moduleCommand.helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectAssignment) or \
                (moduleCommand.helpCommand.commandTypeData == HelpCommand.CommandType_data.ectOutputAssignment):
                mainWidget.localNodeHandler.parseCommand(i)

        if (commandSets.currentCommandSet.ready) and (not mainWidget.callBacksAdded):
            mainWidget.nodeTimer.start(1000)
            print("Starting timer")

            preferences.updateCommandset(commandSets.currentCommandSet)
            mainWidget.pluginHandler.buildPluginList()
            mainWidget.debugTimedChart.updateCommandSetAndCallbacks(commandSets.currentCommandSet, mainWidget.guiCallbackSystem)

            mainWidget.addMainGUICallbacks()
            mainWidget.callBacksAdded = True
            mainWidget.guiCallbackSystem.refreshAllGUIElements()

            serialWidget.setSerialVisibility(serialWidget.reportTypeData["command"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["expressionparser"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["debug"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["hardware"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["priority"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["undefined"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["usb"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["output"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["inforequest"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["internal"])

    mainWidget.updatingFromModule = False

class serialHandler(QThread):
    dataAvaliable = Signal(object, str)
    disconnectSignal = Signal()
    #if (commandSets.currentCommandSet is not None):
    #    chartCommandSignal = Signal(commandSets.currentCommandSet.CommandItem)
    #else:
    #    chartCommandSignal = None

    def run(self) -> None:
        while self.isRunning:
            #processed = False
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
    '''
    def writeI(self, str):
        str = str  + "\n\r"
        serialStream.write(str.encode('ascii'))
    '''
class FarConfig(QWidget):
    #midiDataAvaliableSignal = Signal(str, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        #self.focusing = False

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
        self.ui.tabWidgetMain.setTabText(6, "")

        self.ui.closeEvent = self.closeEvent

        self.serialThread = serialHandler(parent=self) # self is parent for Qthread so Qthread will be destroyed when it's parent no longer exist
        self.serialThread.dataAvaliable.connect(self.dataAvaliable)
        self.serialThread.disconnectSignal.connect(self.serialDisconnect)
        self.serialThread.start()

        self.updateTimer = QTimer(self)
        self.updateTimer.timeout.connect(self.timerUpdateControl)

        self.nodeTimer = QTimer(self)
        self.nodeTimer.timeout.connect(self.nodeAutoUpdater)

        self.debugTimedChart = timedChart.timedChart(None)
        self.ui.layoutChart.addWidget(self.debugTimedChart._chart_view)
        self.legendScene = QGraphicsScene()
        self.legendScene.addItem(self.debugTimedChart.legend)
        #rect = self.debugTimedChart.legend.boundingRect()
        #self.legendScene.setSceneRect(rect.adjusted(2,0,-2,0))
        #self.debugTimedChart.legend.rect().setRect(0,0,150,400)

        self.legendView = QGraphicsView(self.legendScene)
        #self.legendView.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.legendView.setMinimumWidth(200)
        self.legendView.setMaximumWidth(200)
        self.legendView.setViewportMargins(0,0,0,0)
        self.legendView.setContentsMargins(0,0,0,0)
        #self.legendView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.legendView.setFrameShape(QFrame.Shape.NoFrame)

        self.debugTimedChart.legend.adjustSize()
        self.ui.layoutChart.addWidget(self.legendView)
        self.ui.layoutChart.setContentsMargins(0,0,0,0)

        self.updatingFromModule = False
        self.updatingFromGUI = False

        self.timeStamper = self.debugTimedChart.timeStamper #timedChart.timeStamp()
        self.modalEvent = ""

        self.messageBox = messageBox

        self.lastSerialEvent = 0

        self.pluginHandler:PluginHandler = None
        self.guiCallBackSystem:GUICallbackSystem = None
        self.callBacksAdded = False
        self.tabBasic:TabBasic = None
        self.tabAdvanced:TabAdvanced = None
        self.tabMIDI:TabMIDI = None
        self.tabCV:TabCV = None

        self.updateStage = 0
        self.hasNodes = False

    def closeEvent(self, event):
        self.serialThread.stop()
        self.serialThread.quit()
        self.serialThread.wait()
        save_settings()
        print("close")
        app.quit()

    def addMainGUICallbacks(self):
        self.tabBasic.addGUICallbacks()
        self.tabBasic.updateWidget()
        self.tabAdvanced.addGUICallbacks()
        self.tabAdvanced.updateWidget()
        self.tabMIDI.addGUICallbacks()
        self.tabMIDI.updateWidget()
        self.tabCV.addGUICallbacks()
        self.tabCV.updateWidget()
        if (self.pluginHandler is not None):
            self.pluginHandler.addGUICallbacks()

    def nodeAutoUpdater(self):
        match (self.updateStage):
            case 0:
                a = time.time()
                #if (a > (self.mainWidget.lastSerialEvent + 1)):  # and (not self.hasNodes):
                self.localNodeHandler.postBuildUpdate()
                self.hasNodes = True
                self.updateStage = 1
            case 1:
                if (self.hasNodes):
                    self.nodeTimer.stop()
                    self.localNodeHandler.redraw()
                    self.localNodeHandler.ga.graph.select_all()
                    self.localNodeHandler.ga.graph.fit_to_selection()
                    self.localNodeHandler.ga.graph.clear_selection()

                    self.updateStage = 2

    def timerUpdateControl(self):
        self.readSMData()
        pass

    @Slot(str)
    def midiDataAvaliable(self, device, msg):
        serialWidget.addToDebugWindow("<mi<" + str(msg) + "\n")

    def dataAvaliable(self, inSerialHandler, v):
        receivedText = v
        if len(receivedText) > 5:
            if (receivedText[:5] == "[irq]"):
                processInformationReturn(inSerialHandler, receivedText[5:])

            #this should be deprecated
            elif (receivedText[:5] == "[hlp]"):
                commandSets.processHelpReturn(receivedText[5:], commandReference)
        serialWidget.addToDebugWindow("<si< " + receivedText + "\n")
        self.lastSerialEvent = time.time()

    def setUIEnabled(self, state):
        preferences.ui.checkBoxFilterCommAck.setEnabled(state)
        preferences.ui.checkBoxFilterUSB.setEnabled(state)
        preferences.ui.checkBoxFilterHardware.setEnabled(state)
        preferences.ui.checkBoxFilterUndefined.setEnabled(state)
        preferences.ui.checkBoxFilterPriority.setEnabled(state)
        preferences.ui.checkBoxFilterError.setEnabled(state)
        preferences.ui.checkBoxFilterInfoRequest.setEnabled(state)
        preferences.ui.checkBoxFilterExpressionParser.setEnabled(state)
        preferences.ui.checkBoxFilterDebug.setEnabled(state)
        preferences.ui.checkBoxFilterOutput.setEnabled(state)
        self.ui.tabWidgetMain.setEnabled(state)

    def updateUIData(self):
        self.ui.listWidgetMidiEvents.clear()
        self.ui.comboBoxActuatorPreset.clear()
        self.ui.comboBoxHarmonicList.clear()

    def connectDisconnect(self):
        if mainWidget.ui.pushButtonConnectDisconnect.text() == "Connect":
            selectedPort = mainWidget.ui.comboBoxSerialPorts.currentText()
            if selectedPort != "":
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
                    if (mainWidget.pluginHandler is not None):
                        mainWidget.pluginHandler.clearAllPlugins()
                    if (mainWidget.localNodeHandler is not None):
                        mainWidget.localNodeHandler.clearNodes()
                    if (commandSets.currentCommandSet is not None):
                        commandSets.currentCommandSet.clearData()
                    commandReference.clear()
                    mainWidget.callBacksAdded = False

                    self.setUIEnabled(True)
                    self.updateUIData()
                    serialHandler.write("dp:expressionparser:0, dp:internal:0, dp:debug:0, dp:inforequest:1")
                    serialHandler.write("rqi:ver")

                except (OSError, serial.SerialException):
                    print("Connection issue")
                    pass
        else:
            if serialStream.isOpen:
                serialStream.close()
                serialStream = None
            serialWidget.addToDebugWindow("Disconnected\n")
            mainWidget.ui.pushButtonConnectDisconnect.setText("Connect")

            #simpleFARHandler.connected = False

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

    def pushButtonLoadFromModulePressed(self):
        self.updateUIData()

    def pushButtonSaveToModulePressed(self):
        serialHandler.write("sap")

    def setContinuousSMReadings(self, state):
        if state == True:
            self.updateTimer.start(100)
        else:
            self.updateTimer.stop()

    def readSMData(self):
        #commandSets.requestContinuousData(serialHandler)
        for chart in self.debugTimedChart.commandCharts:
            if chart.isRequest:
                serialHandler.write("rqi:" + chart.commandString)

        #self.updateContinuousStringModuleData()

    def checkBoxContinuousSMDataToggled(self):
        self.setContinuousSMReadings(self.ui.checkBoxContinuousSMData.isChecked())

    def addTuningSchemes(self):
        preferences.ui.listWidgetTuningscheme.addItem("Just intonation")
        preferences.ui.listWidgetTuningscheme.addItem("Equal temperament")

    def tuningSchemeChanged(self, current, previous):
        mainWidget.populateFundamentalComboBox()
        pass

    # Base note at octave 5
    scaleDataJust = [440, [1, 1.06667, 1.125, 1.2, 1.25, 1.3333, 1.40625, 1.5, 1.6, 1.66667, 1.8, 1.875],
                     ["A-", "A#", "B-", "C-", "C#", "D-", "D#", "E-", "F-", "F#", "G-", "G#"]]
    scaleDataEqual = [440, [1, 1.059463094, 1.122462048, 1.189207115, 1.259921050, 1.334839854, 1.414213562, 1.498307077, 1.587401052, 1.681792831, 1.781797436,
                            1.887748625],
                      ["A-", "A#", "B-", "C-", "C#", "D-", "D#", "E-", "F-", "F#", "G-", "G#"]]

    def populateFundamentalComboBox(self):
        mainWidget.ui.comboBoxFundamentalFrequency.clear()

        try:
            if ((preferences.ui.listWidgetTuningscheme.currentItem().text()) == "Equal temperament"):
                noteDataArray = self.scaleDataEqual
            else:
                noteDataArray = self.scaleDataJust
        except:
            noteDataArray = self.scaleDataJust

        base = 55 / 2   #110 / 4
        for octave in range(0, 2):  #3
            for note in range (0, 11):
                mainWidget.ui.comboBoxFundamentalFrequency.addItem(noteDataArray[2][note] + " " + str(round((pow(2, octave)*base) * noteDataArray[1][note], 2)))
    '''
    def mouseReleaseEventIntermediate(self, event, widget):
        widget.mouseReleaseFunction(widget)
        if type(widget) == QSlider:
            QSlider.mouseReleaseEvent(widget, event)
    '''

    def showModalWait(self, issueCommand, resultCommand, progressTime, title, timeOut = False):
        if not isinstance(issueCommand. str):
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
    '''
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
    '''

class settingsType(enum.Enum):
    Geometry = enum.auto()
    Visibility = enum.auto()
    checkState = enum.auto()
    windowState = enum.auto()
    value = enum.auto()
    index = enum.auto()
    settingsClass = enum.auto()
    maximized = enum.auto()

def settingsDeclaration():
    #su = serialWidget.ui
    #mu = mainWidget.ui
    pu = preferences.ui
    return  [["mainGeometry", mainWindow, settingsType.Geometry],['mainState', mainWindow, settingsType.windowState],
             ["mainMaximized", mainWindow, settingsType.maximized],

             ["consoleLineLimit", pu.checkBoxLimitLines, settingsType.checkState], ["consoleCursorFollow", pu.checkBoxDebugCursorFollow, settingsType.checkState],
             ["consoleLineLimitLines", pu.spinBoxLimitLines, settingsType.value],

             ["filterHardware", serialWidget.reportTypeData['hardware'], settingsType.settingsClass],
             ["filterDebug", serialWidget.reportTypeData['debug'], settingsType.settingsClass],
             ["filterError", serialWidget.reportTypeData['error'], settingsType.settingsClass],
             ["filterOutput", serialWidget.reportTypeData['output'], settingsType.settingsClass],
             ["filterUSB", serialWidget.reportTypeData['usb'], settingsType.settingsClass],
             ["filterPriority", serialWidget.reportTypeData['priority'], settingsType.settingsClass],
             ["filterUndefined", serialWidget.reportTypeData['undefined'], settingsType.settingsClass],
             ["filterCommAck", serialWidget.reportTypeData['command'], settingsType.settingsClass],
             ["filterExpressionParser", serialWidget.reportTypeData['expressionparser'], settingsType.settingsClass],
             ["filterInfoRequest", serialWidget.reportTypeData['inforequest'], settingsType.settingsClass],
             ["filterInternal", serialWidget.reportTypeData['internal'], settingsType.settingsClass],

             ["tuningScheme", pu.listWidgetTuningscheme, settingsType.index],

             ["referenceGeometry", commandReference, settingsType.Geometry], ["referenceWindowVisible", commandReference, settingsType.Visibility]]

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
            case settingsType.windowState:
                settings.setValue(set[0], set[1].saveState())
            case settingsType.value:
                settings.setValue(set[0], set[1].value())
            case settingsType.index:
                settings.setValue(set[0], set[1].currentRow())
            case settingsType.settingsClass:
                value = set[1].value
                if (isinstance(value, str)):
                    if (value == "true"):
                        value = 1
                    else:
                        value = 0
                if (isinstance(value, bool)):
                    if value == True:
                        value = 1
                    else:
                        value = 0
                settings.setValue(set[0], value)
            case settingsType.maximized:
                settings.setValue(set[0], set[1].isMaximized())

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
                    #preferences.ui.checkBoxDebugCursorFollow.setCheckState()
                    #set[1].stateChanged.emit(set[1])
                    #s = QCheckBox()
                    #set[1].setChecked(set[1].isChecked())
                case settingsType.Visibility:
                    set[1].setVisible(bool(settings.value(set[0])))
                case settingsType.Geometry:
                    geometry = settings.value(set[0])
                    if geometry: set[1].restoreGeometry(geometry)
                    prefix = str(set[0])[:len(set[0]) - 8]
                    value = settings.value(prefix + "Maximized", type=bool)
                    if value:
                        mainWidget.showMaximized()
                        mainWidget.setGeometry(QApplication.desktop().availableGeometry(mainWidget))
                case settingsType.windowState:
                    state = settings.value(set[0])
                    if state: set[1].restoreState(state)
                case settingsType.value:
                    set[1].setValue(int(settings.value(set[0])))
                    #set[1].valueChanged.emit(set[1])
                case settingsType.index:
                    set[1].setCurrentRow(int(settings.value(set[0])))
                case settingsType.settingsClass:
                    set[1].setValueData(int(settings.value(set[0])))
        except Exception as e:
            pass
    mainWindow.updateGeometry()

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
    if (localNodehandler is not None):
        localNodehandler.postBuildUpdate()

def setMainEventHandlers():
    ## Global commands
    mainWidget.ui.pushButtonConnectDisconnect.pressed.connect(mainWidget.connectDisconnect)
    mainWidget.ui.pushButtonSaveToModule.pressed.connect(mainWidget.pushButtonSaveToModulePressed)
    mainWidget.ui.pushButtonLoadFromModule.pressed.connect(mainWidget.pushButtonLoadFromModulePressed)
    mainWidget.ui.checkBoxContinuousSMData.toggled.connect(mainWidget.checkBoxContinuousSMDataToggled)
    mainWidget.ui.pushButtonShowConsole.pressed.connect(showConsole)
    mainWidget.ui.pushButtonShowReference.pressed.connect(showReference)

    preferences.ui.listWidgetTuningscheme.currentItemChanged.connect(mainWidget.tuningSchemeChanged)

    mainWidget.ui.pushButtonPreferences.pressed.connect(showPreferences)

def showPreferences():
    #preferences.setWindowModality(Qt.WindowModality.WindowModal)
    preferences.show()

class DockTitleBar(QWidget):
    def __init__(self, title, parent_dock):
        super().__init__(parent_dock)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        # Add Title
        label = QLabel(title)
        label.setStyleSheet("font-weight: bold; color: white;")
        layout.addWidget(label)

        layout.addStretch()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(mainWidget)
        self.setDockNestingEnabled(False)

        #Dock widget is our docking area
        self.dockWidgetSerial = QDockWidget("Serial console", self)
        self.dockWidgetSerial.setObjectName("SerialDock")
        self.dockWidgetSerial.setWidget(serialWidget)
        #self.dockWidgetSerial.setFeatures(self.dockWidgetSerial.features() & ~QDockWidget.DockWidgetClosable)
        #dockWidgetSerial.setFloating(False)
        #for btn in self.dockWidgetSerial.findChildren(QAbstractButton):
        #    if "close" in btn.objectName().lower(): btn.hide()
        self.dockWidgetSerial.setTitleBarWidget(DockTitleBar("Serial", self.dockWidgetSerial))
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidgetSerial)
        self.dockWidgetSerial.setStyleSheet("QDockWidget::close-button { image: none; width: 0px; height: 0px; border: none; }")

        self.dockWidgetReference = QDockWidget("Language reference")
        self.dockWidgetReference.setObjectName("ReferenceDock")
        self.dockWidgetReference.setWidget(commandReference)
        #dockWidgetReference.setFloating(False)
        #self.dockWidgetReference.setFeatures(self.dockWidgetReference.features() & ~QDockWidget.DockWidgetClosable)
        #for btn in self.dockWidgetReference.findChildren(QAbstractButton):
        #    if "close" in btn.objectName().lower(): btn.hide()
        self.dockWidgetReference.setTitleBarWidget(DockTitleBar("Reference", self.dockWidgetReference))
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidgetReference)
        self.dockWidgetReference.setStyleSheet("QDockWidget::close-button { image: none; width: 0px; height: 0px; border: none; }")

        self.tabifyDockWidget(self.dockWidgetSerial, self.dockWidgetReference)
        self.tabBar = QTabBar(self.findChild(QTabBar))
        self.tabBar.setAutoHide(True)
        self.setTabPosition(Qt.DockWidgetArea.RightDockWidgetArea, QTabWidget.TabPosition.North)
        self.tabBar.setContentsMargins(0,10,0,0)
        #self.destroyed.connect(self.closeEvent)

    def closeEvent(self, event, /):
        mainWidget.closeEvent(event)
        super().closeEvent(event)
        pass

    def toggleSidebar(self):
        self.dockWidgetReference.toggleViewAction().trigger()
        self.dockWidgetSerial.toggleViewAction().trigger()
        #self.dockWidgetSerial.hide()
        #self.dockWidgetReference.hide()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    mainWidget = FarConfig()
    serialWidget = SerialWidget(serialHandler, mainWidget.timeStamper, logging)
    commandReference = CommandReference()
    preferences = preferences(mainWidget, serialWidget, mainWidget.debugTimedChart, commandSets)

    mainWidget.setObjectName("main")
    serialWidget.setObjectName("console")
    serialWidget.setObjectName("reference")

    #mainWindow is nothing but a container for mainWidget using QMainWindow so i can use more docking features
    mainWindow = MainWindow()
    mainWindow.show()
    mainWidget.ui.pushButtonToggleSidebar.pressed.connect(mainWindow.toggleSidebar)

    ## Hiding old
    mainWidget.ui.pushButtonActuatorLoad.setVisible(False)
    mainWidget.ui.pushButtonShowReference.setVisible(False)
    mainWidget.ui.pushButtonShowConsole.setVisible(False)
    mainWidget.ui.label_22.setVisible(False)
    mainWidget.ui.comboBoxCurrentlySelectedModule.setVisible(False)
## Hiding until implemented
    mainWidget.ui.pushButtonAddHarmonicListFile.setVisible(False)
    mainWidget.ui.pushButtonCCAddLearn.setVisible(False)
    mainWidget.ui.pushButtonDetectFundamental.setVisible(False)
    mainWidget.ui.pushButtonCalibrateHammer.setVisible(False)

    setMainEventHandlers()

    mainWidget.completerList = []
    # mainWidget.completer = QCompleter(mainWidget.completerList)
    mainWidget.serialWidget = serialWidget
    # serialWidget.ui.lineEditSend.setCompleter(mainWidget.completer)

## Default settings
    mainWidget.addTuningSchemes()
    mainWidget.setUIEnabled(True)
    mainWidget.ui.tabWidgetMain.setCurrentIndex(0)
    serialWidget.ui.plainTextEditSerialOutput.setUndoRedoEnabled(False)

#stringModule inits
    #strm = stringModule()
    #simpleFARHandler.stringModules.append(strm)

# pre-start inits
    load_settings()

    localNodehandler = None
    localNodehandler = nodehandler.NodeHandler(mainWidget.ui.nodeContainer)
    mainWidget.localNodeHandler = localNodehandler
    mainWidget.ui.pushButtonOrganize.pressed.connect(organize)

    mainWidget.commandReference = commandReference
    mainWidget.preferences = preferences

    mainWidget.destroyed.connect(mainWidget.closeEvent)
    mainWidget.populateFundamentalComboBox()
    mainWidget.USBRefreshTimer = QTimer()
    mainWidget.USBRefreshTimer.timeout.connect(mainWidget.populateSerialPorts)
    mainWidget.USBRefreshTimer.start(1000)

    serialWidget.addToDebugWindow("Initialized\n")
    sys.exit(app.exec())
    mainWidget.thread1.terminate()
    mainWindow.close()

