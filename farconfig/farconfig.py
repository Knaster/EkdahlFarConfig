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
                               QVBoxLayout, QMainWindow, QHBoxLayout, QLabel, QGraphicsScene, QGraphicsView, QFrame, QProgressDialog)
# QTextEdit, QAbstractButton, QStackedWidget,
from PySide6.QtCore import QThread, Signal, QTimer, Qt, Slot, QSettings, QSize, QIODevice, QByteArray, QObject, QCoreApplication
import PySide6.QtSerialPort as QSerialPort
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

#global serialStream
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
            if (moduleCommand is not None) and (moduleCommand.helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectAssignment or \
                    moduleCommand.helpCommand.commandTypeData == HelpCommand.CommandType_data.ectOutputAssignment):
                mainWidget.localNodeHandler.parseCommand(i)

        if (not commandSets.currentCommandSet.ready):
            mainWidget.progressDialog.setValue(commandSets.currentCommandSet.loadingStage)

        if (commandSets.currentCommandSet.ready) and (not mainWidget.callBacksAdded):
            mainWidget.progressDialog.setValue(5)

            commandReference.buildReferenceFromHelpSystem(commandSets.currentCommandSet.baseModule)
            preferences.updateCommandset(commandSets.currentCommandSet)
            mainWidget.pluginHandler.buildPluginList()
            mainWidget.timedChart.updateCommandSetAndCallbacks(commandSets.currentCommandSet, mainWidget.guiCallbackSystem,
                                                               mainWidget.serialWidget, mainWidget.preferences)

            mainWidget.addMainGUICallbacks()
            mainWidget.callBacksAdded = True
            mainWidget.guiCallbackSystem.refreshAllGUIElements()
            serialWidget.commandSet = commandSets.currentCommandSet
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["cmd"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["ep"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["dbg"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["hw"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["pri"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["un"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["usb"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["out"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["irq"])
            serialWidget.setSerialVisibility(serialWidget.reportTypeData["int"])

            mainWidget.nodeTimer.start(1000)
            print("Starting timer")

        if (commandSets.currentCommandSet.ready):
            commandX, moduleX = commandSets.currentCommandSet.getCommandAndModule(i)
            if (commandX is not None):
                match(commandX.helpCommand.commandTypeFunction):
                    case HelpCommand.CommandType_function.ectAddModule:
                        preferences.updateCommandsComboBox()
                    case HelpCommand.CommandType_function.ectRemoveModule:
                        preferences.updateCommandsComboBox()

    mainWidget.updatingFromModule = False
'''
class serialHandler(QThread):
    dataAvaliable = Signal(object, str)
    disconnectSignal = Signal()
    
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
        serialWidget.addToDebugWindow("[out]" + str + "\n")
        str = str  + "\n\r"
        if serialStream == None:
            return
        serialStream.write(str.encode('ascii'))
'''

class SerialHandler(QObject):
    def __init__(self, mainWidget) -> None:
        super().__init__()
        self.mainWidget = mainWidget

    def write(self, str):
        mainWidget.write(str)

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
        log_app = logging.getLogger('farconfig')
        log_app.setLevel(logging.DEBUG)
        log_app.addHandler(log_handler)
        log_app.propagate = False

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
        self.ui.tabWidgetMain.setTabText(7, "")
        self.ui.tabWidgetMain.setTabIcon(7, QIcon(icondir + "nodes.png"))
        self.ui.tabWidgetMain.setTabText(8, "")
        self.ui.tabWidgetMain.setTabIcon(8, QIcon(icondir + "plugins.png"))

        self.ui.closeEvent = self.closeEvent

        #self.serialThread = serialHandler(parent=self) # self is parent for Qthread so Qthread will be destroyed when it's parent no longer exist
        #self.serialThread.dataAvaliable.connect(self.dataAvaliable)
        #self.serialThread.disconnectSignal.connect(self.serialDisconnect)
        #self.serialThread.start()

        self.updateTimer = QTimer(self)
        self.updateTimer.timeout.connect(self.timerUpdateControl)

        self.nodeTimer = QTimer(self)
        self.nodeTimer.timeout.connect(self.nodeAutoUpdater)

        self.timedChart = timedChart.timedChart(None, self)
        '''
        self.ui.layoutChart.addWidget(self.timedChart._chart_view)
        self.legendScene = QGraphicsScene()
        self.legendScene.addItem(self.timedChart.legend)
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
        self.timedChart.legend.adjustSize()        
        self.ui.layoutChart.addWidget(self.legendView)
        self.ui.layoutChart.setContentsMargins(0,0,0,0)
        '''
        self.updatingFromModule = False
        self.updatingFromGUI = False

        self.timeStamper = self.timedChart.timeStamper #timedChart.timeStamp()
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

        self.serialPort = QSerialPort.QSerialPort(self)
        self.lastUnterminatedSerialData = ""

    def closeEvent(self, event):
        #self.serialThread.stop()
        #self.serialThread.quit()
        #self.serialThread.wait()
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
                self.progressDialog.setValue(6)
            case 1:
                if (self.hasNodes):
                    self.nodeTimer.stop()
                    self.localNodeHandler.redraw()
                    self.localNodeHandler.ga.graph.select_all()
                    self.localNodeHandler.ga.graph.fit_to_selection()
                    self.localNodeHandler.ga.graph.clear_selection()
                    self.updateStage = 2
                    self.progressDialog.close()

    def timerUpdateControl(self):
        self.readSMData()
        pass

    #@Slot(str)
    def midiDataAvaliable(self, device, msg):
        serialWidget.addToDebugWindow("[mid]" + str(msg) + "\n")

    @Slot()
#    def dataAvaliable(self, inSerialHandler = None, v = None):
    def dataAvaliable(self):
        v = self.serialPort.readAll()
        receivedText = bytes(v).decode('ascii', errors='ignore')
        if mainWidget.lastUnterminatedSerialData != "":
            receivedText = mainWidget.lastUnterminatedSerialData + receivedText
            mainWidget.lastUnterminatedSerialData = ""

        if (receivedText.find("\r\n") != -1) and (receivedText[len(receivedText)-2:] != "\r\n"):
            mainWidget.lastUnterminatedSerialData = receivedText[receivedText.rfind("\r\n"):len(receivedText)].strip("\r\n")
            receivedText = receivedText[:receivedText.rfind("\r\n")]
        receivedText = receivedText.rstrip("\r\n")
        if receivedText.find("\n") or receivedText.find("\r"):
            pass
        textItems = receivedText.split("\r\n")
        for receivedText in textItems:
            if len(receivedText) > 5:
                if (receivedText[:5] == "[irq]"):
                    #processInformationReturn(inSerialHandler, receivedText[5:])
                    processInformationReturn(serialHandler, receivedText[5:])

                #this should be deprecated
                elif (receivedText[:5] == "[hlp]"):
                    commandSets.processHelpReturn(receivedText[5:], commandReference)
            serialWidget.addToDebugWindow(receivedText + "\n")
            self.lastSerialEvent = time.time()

    def serialError(self, err):
        print("Serial port error " + self.serialPort.errorString())
        pass

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
                    #global serialStream
                    #serialStream = serial.Serial(selectedPort.split(' ')[0], 115200)
                    #if serialStream is None:
                    #    print("serialStream is none!")
                    #    return
                    self.serialPort.setPortName(selectedPort.split(' ')[0])
                    self.serialPort.setBaudRate(115200)
                    self.serialPort.setDataBits(QSerialPort.QSerialPort.DataBits.Data8)
                    self.serialPort.setParity(QSerialPort.QSerialPort.Parity.NoParity)
                    self.serialPort.setStopBits(QSerialPort.QSerialPort.StopBits.OneStop)
                    self.serialPort.setFlowControl(QSerialPort.QSerialPort.FlowControl.SoftwareControl)
                    self.serialPort.close()
                    if not self.serialPort.open(QIODevice.OpenModeFlag.ReadWrite):
                        print("Failed at opening serial port")
                        return
                    else:
                        print("Open:", self.serialPort.isOpen())
                        print("Baud:", self.serialPort.baudRate())
                        print("Is open:", self.serialPort.isOpen())
                        print("Bytes available:", self.serialPort.bytesAvailable())
                        self.serialPort.setDataTerminalReady(True)
                        self.serialPort.setRequestToSend(True)
                        time.sleep(0.1)
                        self.serialPort.readyRead.connect(self.dataAvaliable)
                        self.serialPort.errorOccurred.connect(self.serialError)

                    #serialWidget.addToDebugWindow("Connected to " + serialStream.portstr + "\n")
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

                    self.progressDialog = QProgressDialog("Loading from instrument..", "Cancel", 0, 6)
                    self.progressDialog.setWindowModality(Qt.WindowModal)
                    self.progressDialog.show()
                    self.progressDialog.setValue(0)

                    self.setUIEnabled(True)
                    self.updateUIData()
                    #serialHandler.write("dp:expressionparser:0, dp:internal:0, dp:debug:0, dp:inforequest:1")
                    serialHandler.write("dp:expressionparser:0, dp:internal:0, dp:debug:0, dp:inforequest:1")
                    serialHandler.write("rqi:ver")

                except (OSError, serial.SerialException):
                    print("Connection issue")
                    pass
        else:
            #if serialStream.isOpen:
            #    serialStream.close()
            #    serialStream = None
            self.serialPort.close()
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

        for portInfo in QSerialPort.QSerialPortInfo.availablePorts():
            mainWidget.ui.comboBoxSerialPorts.addItem(portInfo.portName() + " - " + portInfo.description(), portInfo)

        #serialPorts = serial.tools.list_ports.comports()
        #for port, desc, hwid in sorted(serialPorts):
        #        mainWidget.ui.comboBoxSerialPorts.addItem(port + " - " + desc)
        mainWidget.ui.comboBoxSerialPorts.setCurrentIndex(itemSelected)

    def write(self, string:str):
        if not self.serialPort.isOpen():
            print("Serial port not open")
            return 0

        serialWidget.addToDebugWindow("[out]" + string + "\n")

        if not string.endswith('\r\n'):
            string += '\r\n'

        data = string.encode("ascii", "ignore")
        bytes_written = self.serialPort.write(data)
        #self.serialPort.flush()

        #print(f"Sent {bytes_written} bytes: {repr(string[:50])}")

        #if self.serialPort.waitForBytesWritten(1):
        #    print("Data confirmed sent")
        #else:
        #    print("Timeout - data may not have been sent")
        #self.serialPort.setDataTerminalReady(True)
        #self.serialPort.setRequestToSend(True)
        #QCoreApplication.processEvents()

    def pushButtonLoadFromModulePressed(self):
        self.updateUIData()

    def pushButtonSaveToModulePressed(self):
        serialHandler.write("sap")

    def setContinuousSMReadings(self, state):
        if state == True:
            self.updateTimer.start(self.timedChart.updateRate)
        else:
            self.updateTimer.stop()

    def readSMData(self):
        #commandSets.requestContinuousData(serialHandler)
        for chart in self.timedChart.commandCharts:
            if chart.isRequest and chart.visible:
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
    width = enum.auto()

def settingsDeclaration():
    #su = serialWidget
    #mu = mainWidget.ui
    pu = preferences.ui
    return  [["mainGeometry", mainWindow, settingsType.Geometry],['mainState', mainWindow, settingsType.windowState],
             ["mainMaximized", mainWindow, settingsType.maximized],

             ["consoleLineLimit", pu.checkBoxLimitLines, settingsType.checkState],
             ["consoleCursorFollow", pu.checkBoxDebugCursorFollow, settingsType.checkState],
             ["consoleLineLimitLines", pu.spinBoxLimitLines, settingsType.value],

             ["filterHardware", serialWidget.reportTypeData['hw'], settingsType.settingsClass],
             ["filterDebug", serialWidget.reportTypeData['dbg'], settingsType.settingsClass],
             ["filterError", serialWidget.reportTypeData['err'], settingsType.settingsClass],
             ["filterOutput", serialWidget.reportTypeData['out'], settingsType.settingsClass],
             ["filterUSB", serialWidget.reportTypeData['usb'], settingsType.settingsClass],
             ["filterPriority", serialWidget.reportTypeData['pri'], settingsType.settingsClass],
             ["filterUndefined", serialWidget.reportTypeData['un'], settingsType.settingsClass],
             ["filterCommAck", serialWidget.reportTypeData['cmd'], settingsType.settingsClass],
             ["filterExpressionParser", serialWidget.reportTypeData['ep'], settingsType.settingsClass],
             ["filterInfoRequest", serialWidget.reportTypeData['irq'], settingsType.settingsClass],
             ["filterInternal", serialWidget.reportTypeData['int'], settingsType.settingsClass],

             ["tuningScheme", pu.listWidgetTuningscheme, settingsType.index],

             ["serialMonitorWidth", mainWindow.dockWidgetSerial, settingsType.width]
             #["referenceGeometry", commandReference, settingsType.Geometry], ["referenceWindowVisible", commandReference, settingsType.Visibility],
             #["serialMonitorGeometry", serialWidget, settingsType.Geometry], ["serialMonitorVisible", serialWidget, settingsType.Visibility]
             ]

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
                value = set[1].show
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
            case settingsType.width:
                settings.setValue(set[0], set[1].width())

    if mainWidget.timedChart is not None:
        timedChart.timedChart.saveCharts(mainWidget.timedChart, settings)

def loadCheckState(settings, name, checkBox):
    state = settings.value(name)
    if state == Qt.CheckState.Checked or state == 'Checked':
        checkBox.setCheckState(Qt.CheckState.Checked)
    else:
        checkBox.setCheckState(Qt.CheckState.Unchecked)

def convertSettingsBool(settingsBool) -> bool:
    if not isinstance(settingsBool, str): return False
    if settingsBool == "true":
        return True
    if settingsBool == "false":
        return False


#dockResizeData = None

def load_settings():
    # Load window geometry using QSettings
    isMaximized = False
#    global dockResizeData
    dockResizeData = None
    settings = QSettings("Knas", "Ekdahl FAR Config")
    for set in settingsDeclaration():
        if settings.contains(set[0]):
            match(set[2]):
                case settingsType.checkState:
                    loadCheckState(settings, set[0], set[1])
                    #preferences.ui.checkBoxDebugCursorFollow.setCheckState()
                    #set[1].stateChanged.emit(set[1])
                    #s = QCheckBox()
                    #set[1].setChecked(set[1].isChecked())
                case settingsType.Visibility:
                    set[1].setVisible(convertSettingsBool(settings.value(set[0])))
                case settingsType.Geometry:
                    geometry = settings.value(set[0])
                    if geometry: set[1].restoreGeometry(geometry)
                    prefix = str(set[0])[:len(set[0]) - 8]
                    value = settings.value(prefix + "Maximized", type=bool)
                    if value:
                        mainWidget.showMaximized()
                        mainWidget.setGeometry(mainWidget.screen().availableGeometry())
                    pass
                case settingsType.windowState:
                    state = settings.value(set[0])
                    if state: set[1].restoreState(state)
                case settingsType.value:
                    set[1].setValue(int(settings.value(set[0])))
                    #set[1].valueChanged.emit(set[1])
                case settingsType.index:
                    set[1].setCurrentRow(int(settings.value(set[0])))
                case settingsType.settingsClass:
                    set[1].setShowData(int(settings.value(set[0])))
                case settingsType.maximized:
                    if convertSettingsBool(settings.value(set[0])):
                        # Fucking stupid Qt asynchronicity bug hack
                        QTimer.singleShot(100, mainWindow.showMaximized)
                case settingsType.width:
                    # Fucking stupid Qt asynchronicity bug hack
                    QTimer.singleShot(200, lambda:mainWindow.resizeDocks([mainWindow.dockWidgetSerial], [int(settings.value(set[0]))], Qt.Horizontal))
        else:
            pass

    #mainWindow.updateGeometry()

    if (mainWidget.timedChart is not None):
        timedChart.timedChart.loadCharts(mainWidget.timedChart, settings)

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

        self.progressDialog = None

    def closeEvent(self, event, /):
        mainWidget.closeEvent(event)
        super().closeEvent(event)
        pass

    def toggleSidebar(self):
        self.dockWidgetReference.toggleViewAction().trigger()
        self.dockWidgetSerial.toggleViewAction().trigger()
        #self.dockWidgetSerial.hide()
        #self.dockWidgetReference.hide()

def clear_layout(layout):
    """Recursively remove all widgets and layouts from the given layout."""
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                # Schedule widget for deletion
                widget.deleteLater()
            else:
                # If it's a nested layout, recurse into it
                nested_layout = item.layout()
                if nested_layout is not None:
                    clear_layout(nested_layout)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    mainWidget = FarConfig()
    serialHandler = SerialHandler(mainWidget)
    serialWidget = SerialWidget(serialHandler, mainWidget.timeStamper, logging)
    commandReference = CommandReference()
    preferences = preferences(mainWidget, serialWidget, mainWidget.timedChart, commandSets)


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

    preferences.ui.label_7.setVisible(False)
    preferences.ui.lineEditChartParameters.setVisible(False)
    preferences.ui.checkBoxChartRequireArgument.setVisible(False)
    preferences.ui.spinBoxChartRequiredArgument.setVisible(False)
    preferences.ui.label_10.setVisible(False)
    preferences.ui.lineEditChartRequiredEquals.setVisible(False)

    mainWidget.ui.tabWidgetMain.setTabVisible(5, False)
    mainWidget.ui.tabWidgetMain.setTabVisible(6, False)

    clear_layout(mainWidget.ui.horizontalLayout_55)
    mainWidget.ui.groupBox_14.deleteLater()
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
    mainWidget.serialPort.close()

