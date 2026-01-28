#
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
import platform
import random
# This Python file uses the following encoding: utf-8
import sys
import time
import os
import serial.tools.list_ports

from PySide6.QtWidgets import (QApplication, QWidget, QDoubleSpinBox, QListWidgetItem, QInputDialog, QMessageBox, QLineEdit,
                               QComboBox, QSlider, QTabBar, QTabWidget, QVBoxLayout, QCheckBox, QDial, QPushButton, QListWidget)
from PySide6.QtCore import QThread, Signal, QTimer, QModelIndex, Qt, QObject, QDir, Slot, QSettings, QSize, QRect
from PySide6.QtGui import QTextBlock, QTextCursor, QTextBlockFormat, QColor, QIcon, QPainter, QTransform, QShortcut, QKeySequence

import re

#import commandparser
import equationParsingHelpers
import averager
import waitdialog

import logging
from logging.handlers import RotatingFileHandler

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
import tableTest

from ui_form import Ui_Widget
from serialWidget import SerialWidget as SerialWidget
from commandReference import commandReference as CommandReference

from time import process_time

import mido

import timedChart

from stringModule import stringModule, CC, InstrumentMaster, SimpleFARHandler

simpleFARHandler = SimpleFARHandler

global serialStream

from CommandSets import CommandSets, CommandID, CommandType
commandSets = CommandSets()

app = None

import nodehandler

adcAverages = [averager.Averager() for i in range(8)]

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

    #processed = True

    for i in commandList.commands:
        commandType = commandSets.getCommandType(i)
        processInformationForChart(inSerialHandler, i)

#match commandType:
    #case CommandType.simple:
        id = commandSets.getCommandID(i)
        if (commandType == CommandType.simple):
            try:
                value = float(i.argument[0])
            except:
                print("Internal error")
                value = 0
            simpleFARHandler.stringModules[0].setCommandValue(id, value)
            mainWidget.updateStringModuleData()

    #case _:
        #processed = processed | False

        if (i.command == "ver"):
            commandSets.chooseCommandSet(i.argument[0])
            mainWidget.debugTimedChart.commandSet = commandSets.currentCommandSet
            simpleFARHandler.connected = True

        if (commandSets.processMessages(i, commandSets, simpleFARHandler, mainWidget, serialHandler)):
            pass
        else:
            match id:
                case mainWidget.modalEvent:
                    mainWidget.modalDialog.stop()
                    mainWidget.updateUIData()

        if (localNodehandler):
            localNodehandler.parseCommand(i)
            localNodehandler.postBuildUpdate()

    mainWidget.updatingFromModule = False
#    return processed

def messageBox(title, message):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(message)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(QMessageBox.Ok) # | QMessageBox.Cancel)

    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        pass

def inputBox(title, message):
    text, ok = QInputDialog().getText(mainWidget, title, message, QLineEdit.Normal)
    if ok and text:
        return text
    else:
        return None

def processHelpReturn(infoReturn):
    commandList = commandSets.currentCommandSet.CommandList()
    if not commandList.addCommands(infoReturn):
        messageBox("ERROR", "Error parsing help return string")
        return

    for i in commandList.commands:
        prefix = i.command
        command = i.argument[0]
        skip = False
        match prefix:
            case "[glo]":
                scopeText = "This is a global command"
                scope = "Global"
            case "[str]":
                scopeText = "This command is dependent on the currently selected module, bow and/or solenoid"
                scope = "Local"
            case _:
                scopeText = ""
                scope = "Unknown"

        if not skip:
            x = command.find("|")
            help = scopeText + "\n\n"
            help += "command: \n" + command + "\n\n"
            help += "parameters: \n"
            for j in range(1,len(i.argument) - 1):
                help += i.argument[j]
                if (j < (len(i.argument)-2)):
                    help += ":"
            help += "\n\nDescription: \n" + i.argument[len(i.argument) - 1]

            if x != -1:
                short = command[x+1:]
                command = command[:x]
            else:
                short = ""

            commandReference.addCommand(command, help)

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

    # Finds the first destination command in commandList and selects it in the Combo Box given in comboBox
    # Sets the slider given in ratio to the multiplier value used in combination with the string literal variable given in variable
    def selectSendDestinationAndRatio(self, comboBox, commandList, ratio, variable, inMultiplier = 1):
        comboBox.blockSignals(True)
        ratio.blockSignals(True)

        found = False
        for a in commandList.commands:
            for b in range(0, comboBox.count()):
                cId = commandSets.getCommandID(a)
                if comboBox.itemData(b)[1] == cId:
                    comboBox.setCurrentIndex(b)
                    found = True
                    break

        #if find != "Nothing":
        if found:
            try:
                offset, multiplier = equationParsingHelpers.getVariable(a.argument[0], variable)
                multiplier = multiplier * inMultiplier
                ratio.setValue(multiplier)
            except:
                pass
        else:
            comboBox.setCurrentIndex(0)
            ratio.setValue(0)

        comboBox.blockSignals(False)
        ratio.blockSignals(False)

    MIDIVariableSenders = [["Nothing", "", 0, 0],
                           ["Harmonic shift", CommandID.bowHarmonicShift, -32767, 1],
                           ["Pressure (modifier)", CommandID.bowPressureModifier, 0, 1],
                           ["Pressure (baseline)", CommandID.bowPressureBaseline, 0, 1],
                           ["Mute position", CommandID.muteSetPosition, 0, 1],
                           ["Solenoid force multiplier", CommandID.solenoidForceMultiplier, 0, "1 / 65535"]]

    #    MIDIBinarySenders = [["MIDI & Mute sustain", ""]]
    def populateComboBoxSendByte(self, comboBox):
        comboBox.clear()
        for sendData in self.MIDIVariableSenders:
            comboBox.addItem(sendData[0], sendData)

    def widgetMIDIEventUpdateSignal(self):
        self.widgetMIDIEventUpdate(self.sender())

    def widgetMIDIEventUpdate(self, widget):
        #widget = self.sender()
        if widget is None:
            return
        match widget.midiEvent:
            case "pb":
                value = self.ui.midiPitchbendRatio.value() / 128
                itemData = self.ui.midiPitchbendSend.itemData(self.ui.midiPitchbendSend.currentIndex())
                variableName = "pitch"
                pass
            case "pat":
                value = self.ui.midiPolyATRatio.value()
                itemData = self.ui.midiPolyATSend.itemData(self.ui.midiPolyATSend.currentIndex())
                variableName = "pressure"
                pass
            case "cat":
                value = self.ui.midiChannelATRatio.value()
                itemData = self.ui.midiChannelATSend.itemData(self.ui.midiChannelATSend.currentIndex())
                variableName = "pressure"
                pass

        qualifiedMidiAssigns = commandSets.getQualifiedShortCommand(CommandID.midiConfigurationData,
                                                                    [simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect)])
        if itemData[1] == "":
            for qualifiedAssign in qualifiedMidiAssigns:
                command = qualifiedAssign + ":" + widget.midiEvent + ":''"
                serialHandler.write(command)
        else:
            for qualifiedAssign in qualifiedMidiAssigns:
                qualifiedCommand = commandSets.getQualifiedShortCommand(itemData[1])[0]
                command = (qualifiedAssign + ":" + widget.midiEvent + ":'" + qualifiedCommand + ":(" + variableName + " * " +
                           str(value) + " * " + str(itemData[3]) + ")'")
                serialHandler.write(command)

    def connectWidgetsToMIDIEvent(self, midiEventName, widgets):
        for widget in widgets:
            widget.midiEvent = midiEventName
            widget.widgets = widgets
            if isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(self.widgetMIDIEventUpdateSignal)
            elif isinstance(widget, QSlider):
                self.assignMouseReleaseEvent(widget, self.widgetMIDIEventUpdate)
            elif isinstance(widget, QCheckBox):
                widget.stateChanged.connect(self.widgetMIDIEventUpdateSignal)

    def setMIDINoteOnCommands(self, commands):
        #mainWidget.remove_item(mainWidget.ui.listWidgetMidiEvents, "Note On")
        simpleFARHandler.instrumentMaster.evNoteOn = commands
        if (self.find_item(self.ui.listWidgetMidiEvents, "Note On") == -1):
            self.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Note On"))

        simpleFARHandler.instrumentMaster.cmdNoteOn.clear()
        simpleFARHandler.instrumentMaster.cmdNoteOn.addCommands(commands)
        seCmd = commandSets.getQualifiedShortCommand(CommandID.solenoidEngage, None, True)[0]
        offset, multiplier = equationParsingHelpers.getVariable(simpleFARHandler.instrumentMaster.cmdNoteOn.getCommandAttribute(seCmd, 0), "velocity")
        mainWidget.ui.midiNoteOnVelToHammer.setValue(multiplier)

        if equationParsingHelpers.isVariableInEquation(simpleFARHandler.instrumentMaster.cmdNoteOn.getCommandAttribute(seCmd, 0), "notecount"):
            mainWidget.ui.midiNoteOnHammerStaccato.setChecked(True)
        else:
            mainWidget.ui.midiNoteOnHammerStaccato.setChecked(False)

        mrCmd = commandSets.getQualifiedShortCommand(CommandID.muteRest, None, True)[0]
        if not simpleFARHandler.instrumentMaster.cmdNoteOn.getCommandAttribute(mrCmd, 0) == "":
            mainWidget.ui.midiNoteOnSendMuteRest.setChecked(True)
        else:
            mainWidget.ui.midiNoteOnSendMuteRest.setChecked(False)

    def setMIDINoteOffCommands(self, commands):
        #mainWidget.remove_item(mainWidget.ui.listWidgetMidiEvents, "Note Off")
        simpleFARHandler.instrumentMaster.evNoteOff = commands
        if (self.find_item(self.ui.listWidgetMidiEvents, "Note Off") == -1):
            mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Note Off"))

        simpleFARHandler.instrumentMaster.cmdNoteOff.clear()
        simpleFARHandler.instrumentMaster.cmdNoteOff.addCommands(commands)

        mfmCmd = commandSets.getQualifiedShortCommand(CommandID.muteFullMute, None, True)[0]
        if not simpleFARHandler.instrumentMaster.cmdNoteOff.getCommandAttribute(mfmCmd, 0) == "":
            mainWidget.ui.midiNoteOffSendFullMute.setChecked(True)
        else:
            mainWidget.ui.midiNoteOffSendFullMute.setChecked(False)

        bmrCmd = commandSets.getQualifiedShortCommand(CommandID.motorRun, None, True)[0]
        if not simpleFARHandler.instrumentMaster.cmdNoteOff.getCommandAttribute(bmrCmd, 0) == "":
            mainWidget.ui.midiNoteOffMotorOff.setChecked(True)
        else:
            mainWidget.ui.midiNoteOffMotorOff.setChecked(False)

    def setMIDICCCommands(self, cc, commands):
        #mainWidget.remove_item(mainWidget.ui.listWidgetMidiEvents, "CC " + str(cc))
        simpleFARHandler.instrumentMaster.addCC(int(cc), commands)
        if (self.find_item(self.ui.listWidgetMidiEvents, "CC " + str(cc)) == -1):
            mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("CC " + str(cc)))
        self.setMIDISustainDestination()

    def setMIDISustainDestination(self):
        commands = simpleFARHandler.instrumentMaster.getCC(64).command
        commandList = commandSets.currentCommandSet.CommandList(commands)

        if ("ibool" in commands):
            self.ui.midiSustainInvert.setChecked(True)
        else:
            self.ui.midiSustainInvert.setChecked(False)

        for b in range(0, self.ui.midiSustainSend.count()):
            if (len(self.ui.midiSustainSend.itemData(b)[1]) == len(commandList.commands)):
                found = True
                for a in commandList.commands:
                    cId = commandSets.getCommandID(a)
                    if cId not in self.ui.midiSustainSend.itemData(b)[1]:
                        found = False
                        break
                if (len(commandList.commands) > 0) and (found):
                    self.ui.midiSustainSend.setCurrentIndex(b)
                    return
        self.ui.midiSustainSend.setCurrentIndex(0)

    def setMIDIPATCommands(self, commands):
        simpleFARHandler.instrumentMaster.evPolyAftertouch = commands
        if (self.find_item(self.ui.listWidgetMidiEvents, "Poly Aftertouch") == -1):
            mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Poly Aftertouch"))

        simpleFARHandler.instrumentMaster.cmdPolyAftertouch.clear()
        simpleFARHandler.instrumentMaster.cmdPolyAftertouch.addCommands(commands)

        mainWidget.selectSendDestinationAndRatio(mainWidget.ui.midiPolyATSend, simpleFARHandler.instrumentMaster.cmdPolyAftertouch,
                                                 mainWidget.ui.midiPolyATRatio, "pressure")

    def setMIDIPBCommands(self, commands):
        simpleFARHandler.instrumentMaster.evPitchbend = commands
        if (self.find_item(self.ui.listWidgetMidiEvents, "Pitchbend") == -1):
            mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Pitchbend"))

        simpleFARHandler.instrumentMaster.cmdPitchbend.clear()
        simpleFARHandler.instrumentMaster.cmdPitchbend.addCommands(commands)

        mainWidget.selectSendDestinationAndRatio(mainWidget.ui.midiPitchbendSend, simpleFARHandler.instrumentMaster.cmdPitchbend,
                                                 mainWidget.ui.midiPitchbendRatio, "pitch", 127)

    def setMIDICATCommands(self, commands):
        simpleFARHandler.instrumentMaster.evChannelAftertouch = commands
        if (self.find_item(self.ui.listWidgetMidiEvents, "Channel Aftertouch") == -1):
            mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Channel Aftertouch"))

        simpleFARHandler.instrumentMaster.cmdChannelAftertouch.clear()
        simpleFARHandler.instrumentMaster.cmdChannelAftertouch.addCommands(commands)

        mainWidget.selectSendDestinationAndRatio(mainWidget.ui.midiChannelATSend, simpleFARHandler.instrumentMaster.cmdChannelAftertouch,
                                                 mainWidget.ui.midiChannelATRatio, "pressure")

    def setMIDIPCCommands(self, commands):
        simpleFARHandler.instrumentMaster.evProgramChange = commands
        if (self.find_item(self.ui.listWidgetMidiEvents, "Program change") == -1):
            mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Program change"))

    def handleMIDIConfigurationCount(self, count):
        mainWidget.ui.comboBoxConfiguration.clear()
        while (self.ui.comboBoxConfiguration.count() < int(count)):
            mainWidget.ui.comboBoxConfiguration.insertItem(self.ui.comboBoxConfiguration.count() + 1, "placeholder")

    def handleMIDIConfigurationName(self, index, name, setIndex):
        mainWidget.ui.comboBoxConfiguration.setItemText(index, name)
        if (setIndex):
            mainWidget.ui.comboBoxConfiguration.setCurrentIndex(simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect))

    def handleMIDIConfigurationSelect(self, config):
        simpleFARHandler.stringModules[0].setCommandValue(CommandID.midiConfigurationSelect, float(config))
        mainWidget.updateStringModuleData()
        mainWidget.ui.listWidgetMidiEvents.clear()
        mainWidget.ui.comboBoxConfiguration.setCurrentIndex(int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect)))

    def handleMIDIReceiveChannel(self, channel):
        mainWidget.ui.comboBoxMidiChannel.blockSignals(True)
        ch = int(channel)
        if ((ch < 1) or (ch > 16)):
            find = "Omni"
        else:
            find = str(ch)

        for a in range(0, mainWidget.ui.comboBoxMidiChannel.count()):
            if find == mainWidget.ui.comboBoxMidiChannel.itemText(a):
                mainWidget.ui.comboBoxMidiChannel.setCurrentIndex(a)
                break
        mainWidget.ui.comboBoxMidiChannel.blockSignals(False)

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

        mainWidget.ui.comboBoxActuatorPreset.setItemText(index, name)
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

    def handleControlBoxReturnData(self, channel, value):
        simpleFARHandler.stringModules[0].setCVValue(int(channel), int(value))
        self.updateContinuousStringModuleData()
        adcAverages[int(channel)].addValue(value)
        self.updateAverages()

    def handleControlBoxControlData(self, channel, commands):
        match int(channel):
            case 0:
                widget = mainWidget.ui.plainTextEditCVHarmonicCommands
            case 1:
                widget = mainWidget.ui.plainTextEditCVHarmonicShiftCommands
            case 2:
                widget = mainWidget.ui.plainTextEditCVFineTuneCommands
            case 3:
                widget = mainWidget.ui.plainTextEditCVPressureCommands
            case 4:
                widget = mainWidget.ui.plainTextEditCVHammerTriggerCommands
            case 5:
                widget = mainWidget.ui.plainTextEditCVGateCommands
            case 6:
                widget = mainWidget.ui.plainTextEditCVHammerScaleCommands
            case 7:
                widget = mainWidget.ui.plainTextEditCVMuteCommands
            case _:
                mainWidget.messageBox("ADC Command error", "ADC Command error")
                return

        widget.setText(commands)
        simpleFARHandler.stringModules[0].setCVCommand(channel, commands)
        mainWidget.updateCVData()

    MIDIBinarySenders = [["None", []], ["Bow hold & Mute inhibit", [CommandID.bowPressureHold, CommandID.muteSustain]], ["Bow hold", [CommandID.bowPressureHold]],
                         ["Mute inhibit", [CommandID.muteSustain]]]

    def connectWidgetsToBinarySenders(self, midiEvent, widgets):
        for widget in widgets:
            widget.midiEvent = midiEvent
            widget.widgets = widgets
            if isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(self.widgetMIDIBinarySendersCallback)
            elif isinstance(widget, QSlider):
                self.assignMouseReleaseEvent(widget, self.widgetMIDIBinarySendersCallback)
            elif isinstance(widget, QCheckBox):
                widget.stateChanged.connect(self.widgetMIDIBinarySendersCallback)

    def populateComboBoxSendBinary(self, comboBox):
        comboBox.clear()
        for sendData in self.MIDIBinarySenders:
            comboBox.addItem(sendData[0], sendData)
        pass

    def widgetMIDIBinarySendersCallback(self):
        if (self.updatingFromModule): return
        widget = self.sender()
        cmd = ""
        itemData = self.ui.midiSustainSend.itemData(self.ui.midiSustainSend.currentIndex())
        booltype = "bool"
        if self.ui.midiSustainInvert.isChecked():
            booltype = "ibool"
        command = (commandSets.getQualifiedShortCommand(CommandID.midiConfigurationData,
                                                       [simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect)])[0] +
                                                                    ":cc:64:")
        if itemData[1] == "":
            command += "''"
        else:
            command += "'"
            for a in itemData[1]:
                cmm = commandSets.getQualifiedShortCommand(a)
                if len(cmm) == 0: break
                if (command[-1] != "'"):
                    command += ","
                #command += a + ":" + booltype + "(value)"
                command += cmm[0] + ":" + booltype + "(value)"
        command += "'"
        serialHandler.write(command)
        #self.updateUIData()

    def addData(self, seriesID, value, inSeriesType): # min, max):
        self.debugTimedChart.addData(seriesID, value, inSeriesType) # min, max)

    def chartCommand(self, command):
        self.debugTimedChart.processCommand(command)

    def timerUpdateControl(self):
        self.readSMData()

    @Slot(str)
    def midiDataAvaliable(self, device, msg):
        serialWidget.addToDebugWindow("<mi<" + str(msg) + "\n")
        # + str(device) + "<"
        pass

    def dataAvaliable(self, inSerialHandler, v):
#        self.addToDebugWindow(v + "\n")
        receivedText = v
        if (receivedText[:5] == "[irq]"):
            processInformationReturn(inSerialHandler, receivedText[5:])
        elif (receivedText[:5] == "[hlp]"):
            processHelpReturn(receivedText[5:])
            #pass

        #if (not processed):
        serialWidget.addToDebugWindow("<si< " + receivedText + "\n")

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
                    commandReference.clear()

                    self.setUIEnabled(True)
                    self.updateUIData()
                    serialHandler.write("rqi:ver")

#                    self.showModalWait("nop", "nop", 15000, "Connecting")

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
                #self.setUIEnabled(False)
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
#                print("{}: {}".format(port, desc))
                mainWidget.ui.comboBoxSerialPorts.addItem(port + " - " + desc)
        mainWidget.ui.comboBoxSerialPorts.setCurrentIndex(itemSelected)

    def updateStringModuleData(self):
        global stringModules

        self.ui.doubleSpinBoxFundamentalFrequency.setValue(
            float(simpleFARHandler.stringModules[0].getCommandValue(CommandID.bowFundamental)))
        #self.ui.doubleSpinBoxFundamentalFrequency.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxFundamentalFrequency.command)))

        self.ui.doubleSpinBoxBowMotorPIDKp.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxBowMotorPIDKp.command)))
        self.ui.doubleSpinBoxBowMotorPIDKi.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxBowMotorPIDKi.command)))
        self.ui.doubleSpinBoxBowMotorPIDKd.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxBowMotorPIDKd.command)))
        self.ui.doubleSpinBoxBowMotorPIDie.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxBowMotorPIDie.command)))
        self.ui.doubleSpinBoxBowMotorMaxError.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxBowMotorMaxError.command)))

        self.ui.doubleSpinBoxBowMotorVoltage.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxBowMotorVoltage.command)))
        self.ui.doubleSpinBoxBowMotorTimeout.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxBowMotorTimeout.command)))
        self.ui.doubleSpinBoxMuteFullMutePosition.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxMuteFullMutePosition.command)))
        self.ui.doubleSpinBoxMuteHalfMutePosition.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxMuteHalfMutePosition.command)))
        self.ui.doubleSpinBoxMuteRestPosition.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxMuteRestPosition.command)))
        self.ui.doubleSpinBoxMuteBackoff.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxMuteBackoff.command)))
        self.ui.doubleSpinBoxBowMotorMaxSpeed.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxBowMotorMaxSpeed.command)))
        self.ui.doubleSpinBoxBowMotorMinSpeed.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxBowMotorMinSpeed.command)))
        self.ui.doubleSpinBoxBowMaxPressure.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxBowMaxPressure.command)))
        self.ui.doubleSpinBoxBowMinPressure.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxBowMinPressure.command)))
        self.ui.doubleSpinBoxBowRestPosition.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxBowRestPosition.command)))
        self.ui.doubleSpinBoxSolenoidMaxForce.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxSolenoidMaxForce.command)))
        self.ui.doubleSpinBoxSolenoidMinForce.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxSolenoidMinForce.command)))
        self.ui.doubleSpinBoxSolenoidEngageDuration.setValue(float(simpleFARHandler.stringModules[0].getCommandValue(self.ui.doubleSpinBoxSolenoidEngageDuration.command)))
        self.ui.spinBoxHarmonicShiftRange.setValue(int(simpleFARHandler.stringModules[0].getCommandValue(self.ui.spinBoxHarmonicShiftRange.command)))

        self.ui.progressBar_bch.setValue(int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.bowHarmonic)))
        self.ui.progressBar_bchb.setValue(int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.bowHarmonicBase)))
        self.ui.progressBar_bchbn.setValue(int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.bowHarmonicBaseNote)))
        self.ui.progressBar_bchshr.setValue(int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.bowHarmonicShiftRange)))
        self.ui.progressBar_bchsh.setValue(int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.bowHarmonicShift)))
        self.ui.progressBar_bchs5.setValue(int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.bowHarmonicShift5)))
        self.ui.progressBar_bcha.setValue(int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.bowHarmonicAdd)))
        self.ui.progressBar_ar1.setValue(self.ui.progressBar_bchb.value() - self.ui.progressBar_bchbn.value())
        self.ui.progressBar_ar2.setValue(self.ui.progressBar_bch.value() + self.ui.progressBar_bcha.value())
        self.ui.progressBar_ar3.setValue(int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.pidTargetFreq)))

        self.updateContinuousStringModuleData()

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

        for cv in range(0,8):
            match cv:
                case 0:
                    dial = mainWidget.ui.dialCVHarmonic
                    label = mainWidget.ui.labelCVHarmonic
                case 1:
                    dial = mainWidget.ui.dialCVHarmonicShift
                    label = mainWidget.ui.labelCVHarmonicShift
                case 2:
                    dial = mainWidget.ui.dialCVFineTune
                    label = mainWidget.ui.labelCVFineTune
                case 3:
                    dial = mainWidget.ui.dialCVPressure
                    label = mainWidget.ui.labelCVPressure
                case 4:
                    dial = mainWidget.ui.dialCVHammerTrigger
                    label = mainWidget.ui.labelCVHammerTrigger
                case 5:
                    dial = mainWidget.ui.dialCVGate
                    label = mainWidget.ui.labelCVGate
                case 6:
                    dial = mainWidget.ui.dialCVHammerScale
                    label = mainWidget.ui.labelCVHammerScale
                case 7:
                    dial = mainWidget.ui.dialCVMute
                    label = mainWidget.ui.labelCVMute

            dial.setValue(int(simpleFARHandler.stringModules[0].getCVValue(cv)) )
            label.setText(str(simpleFARHandler.stringModules[0].getCVValue(cv)) )

    def updateAverages(self):
        self.ui.labelADC0Avg.setText(str(adcAverages[0].average))
        self.ui.labelADC0Max.setText(str(adcAverages[0].max))
        self.ui.labelADC0Min.setText(str(adcAverages[0].min))
        self.ui.labelADC0Diff.setText(str(adcAverages[0].max - adcAverages[0].min))
        self.ui.labelADC1Avg.setText(str(adcAverages[1].average))
        self.ui.labelADC1Max.setText(str(adcAverages[1].max))
        self.ui.labelADC1Min.setText(str(adcAverages[1].min))
        self.ui.labelADC1Diff.setText(str(adcAverages[1].max - adcAverages[1].min))
        self.ui.labelADC2Avg.setText(str(adcAverages[2].average))
        self.ui.labelADC2Max.setText(str(adcAverages[2].max))
        self.ui.labelADC2Min.setText(str(adcAverages[2].min))
        self.ui.labelADC2Diff.setText(str(adcAverages[2].max - adcAverages[2].min))
        self.ui.labelADC3Avg.setText(str(adcAverages[3].average))
        self.ui.labelADC3Max.setText(str(adcAverages[3].max))
        self.ui.labelADC3Min.setText(str(adcAverages[3].min))
        self.ui.labelADC3Diff.setText(str(adcAverages[3].max - adcAverages[3].min))
        self.ui.labelADC4Avg.setText(str(adcAverages[4].average))
        self.ui.labelADC4Max.setText(str(adcAverages[4].max))
        self.ui.labelADC4Min.setText(str(adcAverages[4].min))
        self.ui.labelADC4Diff.setText(str(adcAverages[4].max - adcAverages[4].min))
        self.ui.labelADC5Avg.setText(str(adcAverages[5].average))
        self.ui.labelADC5Max.setText(str(adcAverages[5].max))
        self.ui.labelADC5Min.setText(str(adcAverages[5].min))
        self.ui.labelADC5Diff.setText(str(adcAverages[5].max - adcAverages[5].min))
        self.ui.labelADC6Avg.setText(str(adcAverages[6].average))
        self.ui.labelADC6Max.setText(str(adcAverages[6].max))
        self.ui.labelADC6Min.setText(str(adcAverages[6].min))
        self.ui.labelADC6Diff.setText(str(adcAverages[6].max - adcAverages[6].min))
        self.ui.labelADC7Avg.setText(str(adcAverages[7].average))
        self.ui.labelADC7Max.setText(str(adcAverages[7].max))
        self.ui.labelADC7Min.setText(str(adcAverages[7].min))
        self.ui.labelADC7Diff.setText(str(adcAverages[7].max - adcAverages[7].min))

    def averagesClear(self):
        for a in adcAverages:
            a.clear()
        self.updateAverages()

    def averagesTest(self):
        for i in range(8):
            serialHandler.write(commandSets.getQualifiedShortCommand(CommandID.controlBoxADCSettings) + ":" + str(i) + ":1:1:2:10")

    def comboBoxCurrentSelectedModuleIndexChanged(self, index):
        pass

    def assignValueChanged(self, qtObject, command, selectionIndex = None):
        qtObject.command = command
        qtObject.selectionIndex = selectionIndex
        qtObject.valueChanged.connect(self.basicChangedSignal)

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
        if (selection == None): stripIndex = True
        qualifiedShorts = commandSets.getQualifiedShortCommand(commandID, selection, stripIndex)
        out = ""
        for qualifiedShort in qualifiedShorts:
            if (out != ""): out += ","
            out = qualifiedShort + ":" + str(value)
#            out = sender.command + ":" + str(value)

        simpleFARHandler.stringModules[0].setCommandValue(sender.command, float(value))
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
        self.pushButtonSaveCurrentHarmonicListPressed()

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
        mainWidget.pushButtonActuatorSavePressed()
        serialHandler.write(commandSets.getQualifiedShortCommand(CommandID.saveAllParameters)[0])

    eventDescription = [[ "Note On", "Note on message, sent when a key has been depressed. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n note - note number (0-127) \n velocity - key velocity (0-127)" ],
        [ "Note Off", "Note off message, sent when a key has been released. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n note - note number (0-127) \n velocity - key velocity (0-127)" ],
        [ "CC [xx]", "Continous Controller, sent by various control surfaces. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n control - control number (0-127) \n value - controller value (0-127)" ],
        [ "Poly Aftertouch", "Polyphonic Aftertouch, key pressure per key. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n note - note number (0-127) \n pressure - key pressure (0-127)" ],
        [ "Channel Aftertouch", "Channel Aftertouch, key pressure per channel. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n pressure - key pressure (0-127)"],
        [ "Pitchbend", "Pitchbend, frequency change from the current key. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n pitch - bend (-8192 - 8192)"],
        [ "Program change", "Program change message, mostly used to change sound on various devices. \n\nAdded variables: \n channel - MIDI Channel (0-127) \n program - program number (0-127)"]
        ]

    def updateTextForSelectedListItem(self):
        current = self.ui.listWidgetMidiEvents.currentItem()
        self.listWidgetMidiEventscurrentItemChanged(current, current)

    def listWidgetMidiEventscurrentItemChanged(self, current, previous):
        self.ui.plainTextEditEventDescription.clear()
        if current is None:
            return
        match (current.text()):
            case "Note On":
                mainWidget.ui.lineEditMidiEventCommand.setText(str(simpleFARHandler.instrumentMaster.evNoteOn))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[0][1])
            case "Note Off":
                mainWidget.ui.lineEditMidiEventCommand.setText(str(simpleFARHandler.instrumentMaster.evNoteOff))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[1][1])
            case "Poly Aftertouch":
                mainWidget.ui.lineEditMidiEventCommand.setText(str(simpleFARHandler.instrumentMaster.evPolyAftertouch))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[3][1])
            case "Channel Aftertouch":
                mainWidget.ui.lineEditMidiEventCommand.setText(str(simpleFARHandler.instrumentMaster.evChannelAftertouch))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[4][1])
            case "Pitchbend":
                mainWidget.ui.lineEditMidiEventCommand.setText(str(simpleFARHandler.instrumentMaster.evPitchbend))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[5][1])
            case "Program change":
                mainWidget.ui.lineEditMidiEventCommand.setText(str(simpleFARHandler.instrumentMaster.evProgramChange))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[6][1])
            case _:
                if current.text()[:2] == "CC":
                    mainWidget.ui.lineEditMidiEventCommand.setText(str(simpleFARHandler.instrumentMaster.getCC(int(current.text()[3:])).command))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[2][1])

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

        match (commandSelected):
            case "Note On":
                setStr = "noteon"
                simpleFARHandler.instrumentMaster.evNoteOn = commandSequence
            case "Note Off":
                setStr = "noteoff"
                simpleFARHandler.instrumentMaster.evNoteOff = commandSequence
            case "Poly Aftertouch":
                setStr = "pat"
                simpleFARHandler.instrumentMaster.evPolyAftertouch = commandSequence
            case "Channel Aftertouch":
                setStr = "cat"
                simpleFARHandler.instrumentMaster.evChannelAftertouch = commandSequence
            case "Program change":
                setStr = "pc"
                simpleFARHandler.instrumentMaster.evProgramChange = commandSequence
            case "Pitchbend":
                setStr = "pb"
                simpleFARHandler.instrumentMaster.evPitchbend = commandSequence
            case _:
                if commandSelected[:2] == "CC":
                    setStr = "cc:" + commandSelected[3:]
                    cc = int(commandSelected[3:])
                    item = simpleFARHandler.instrumentMaster.getCC(cc)
                    item.command = commandSequence

                else:
                    print(commandSelected + " not found")
                    return

        qualifiedCommand = commandSets.getQualifiedShortCommand(CommandID.midiConfigurationData,
                                                                [simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect)])[0]
        serialString = qualifiedCommand + ":" + setStr + ":\"" + commandSequence + "\""
        serialHandler.write(serialString)

    def find_item(self, widget, item_text):
        if (isinstance(widget, QComboBox)):
            for index in range(widget.count()):
                if widget.itemText(index) == item_text:
                    return index
        elif (isinstance(widget, QListWidget)):
            index = widget.findItems(item_text, Qt.MatchFlag.MatchExactly)
            if (len(index) == 0): return -1
            else:
                return index[0]
        return -1

    def remove_item(self, widget, item_text):
        index = widget.findItems(item_text, Qt.MatchFlag.MatchExactly)
        if (len(index) != 0):
            widget.takeItem(widget.row(index[0]))

    def pushButtonActuatorRenamePressed(self):
        index = mainWidget.ui.comboBoxActuatorPreset.currentIndex()
        if (index == -1): return
        listID = inputBox("New actuator name", "Actuator name")
        if listID is None:
            return
        if (self.find_item(mainWidget.ui.comboBoxActuatorPreset, listID) != -1):
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
            if (self.find_item(mainWidget.ui.comboBoxConfiguration, text) != -1):
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
            if (self.find_item(self.ui.listWidgetMidiEvents, "CC " + str(cc)) == -1):
                mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("CC " + str(cc)))
            #self.updateUIData()

    def ccRemove(self):
        if (mainWidget.ui.listWidgetMidiEvents.currentIndex() == -1):
            return
        if (mainWidget.ui.listWidgetMidiEvents.currentItem().text()[0:2] != "CC"):
            return
        text = mainWidget.ui.listWidgetMidiEvents.currentItem().text()
        commandSets.removeMidiConfigurationCC(self, serialHandler, simpleFARHandler, text[3:len(text)])
        if (self.find_item(self.ui.listWidgetMidiEvents, "CC " + str(cc)) != -1):
            self.remove_item(self.ui.listWidgetMidiEvents, "CC " + str(cc))
        #self.updateUIData()

    def updateCVData(self):
        for a in range(0, 7):
            cl = commandSets.currentCommandSet.CommandList(simpleFARHandler.stringModules[0].getCVCommand(a))
            if len(cl.commands) > 0:
                match a:
                    case 0:
                        cmd = cl.getCommandAttribute(commandSets.getQualifiedShortCommand(CommandID.bowHarmonicAdd)[0], 0)
                        if cmd == "":
                            break
                        try:
                            result = equationParsingHelpers.extractZeroCoefficientOffset(cmd)
                        except:
                            messageBox("Error", "Error in equation parser with string " + cmd)
                            break

                        cvScale = 1327.716667 * result["coefficient"] # * multiplier
                        offsetDiv = result["offset"] / 1327.716667
                        noteOffset = round(offsetDiv)
                        if (result["offset"] < 0):
                            cvOffset = result["offset"] - (noteOffset * 1327.716667)
                        else:
                            cvOffset = result["offset"] - (noteOffset * 1327.716667)
                        noteOffset = math.trunc(offsetDiv)

                        cvZero = result["zeroPosition"]

                        self.ui.dialCVHarmonicScale.setValue(cvScale)   # * 1000
                        self.ui.widgetCVHarmonicNoteOffset.setValue(cvOffset)
                        self.ui.widgetCVHarmonicZero.setValue(cvZero)
                    case 1:
                        cmd = cl.getCommandAttribute(commandSets.getQualifiedShortCommand(CommandID.bowHarmonicShift5)[0], 0)
                        if cmd == "":
                            break
                        try:
                            result = equationParsingHelpers.extractZeroCoefficientOffset(cmd)
                        except:
                            messageBox("Error", "Error in equation parser with string " + cmd)
                            break
                        cvScale = 2.425 / (1 / result["coefficient"])
                        cvZero = (32767) + result["zeroPosition"]
                        self.ui.dialCVHarmonicShiftScale.setValue(cvScale)  # * 1000
                        self.ui.dialCVHarmonicShiftZero.setValue(cvZero)
                    case 2:
                        cmd = cl.getCommandAttribute(commandSets.getQualifiedShortCommand(CommandID.bowHarmonicShift)[0], 0)
                        if cmd == "":
                            break
                        try:
                            cmd = equationParsingHelpers.removeFunction(cmd, "deadband")
                            offset, multiplier = equationParsingHelpers.extractValueOffsetAndMultiplier(cmd)
                            result = equationParsingHelpers.extractZeroCoefficientOffset(cmd)
                        except:
                            messageBox("Error", "Error in equation parser with string " + cmd)
                            break
                        self.ui.dialCVFineTuneCenter.setValue(32767 + result["zeroPosition"])
                        pass
                    case 5:
                        # bmr:1,bpid:1,bcsm:0,bpe:bool(value-2000),bpr:ibool(value-2000),bph:ibool(value-2000)
                        cmd = cl.getCommandAttribute(commandSets.getQualifiedShortCommand(CommandID.motorRun)[0],0)
                        if cmd == "1":
                            mainWidget.ui.checkBoxCVGatePowerMotor.setCheckState(Qt.CheckState.Checked)
                        else:
                            mainWidget.ui.checkBoxCVGatePowerMotor.setCheckState(Qt.CheckState.Unchecked)

                        threshold = 2000

                        cmd = cl.getCommandAttribute(commandSets.getQualifiedShortCommand(CommandID.bowPressureHold)[0], 0)
                        if cmd != "":
                            mainWidget.ui.checkBoxCVGateHold.setCheckState(Qt.CheckState.Checked)
                            threshold = abs(int(equationParsingHelpers.stripBoolIBool(cmd)))
                        else:
                            mainWidget.ui.checkBoxCVGateHold.setCheckState(Qt.CheckState.Unchecked)

                        cmd = cl.getCommandAttribute(commandSets.getQualifiedShortCommand(CommandID.bowPressureEngage)[0], 0)
                        if cmd != "":
                            mainWidget.ui.checkBoxCVGateEngage.setCheckState(Qt.CheckState.Checked)
                            threshold = abs(int(equationParsingHelpers.stripBoolIBool(cmd)))
                        else:
                            mainWidget.ui.checkBoxCVGateEngage.setCheckState(Qt.CheckState.Unchecked)

                        mainWidget.ui.widgetCVGateThreshold.setValue(threshold)
                pass
            else:
                pass
        pass

    def widgetCVMappingCallback(self, widget = None):
        if self.updatingFromModule:
            return
        if not isinstance(widget, QWidget):
            widget = self.sender()
        cl = commandSets.currentCommandSet.CommandList(simpleFARHandler.stringModules[0].getCVCommand(int(widget.CVcontrol)))
        match widget.CVcontrol:
            case 0:
                cmd = cl.buildCommandString({commandSets.getQualifiedShortCommand(CommandID.bowHarmonicAdd)[0]})
                cvScale = str(1327.716667 / (self.ui.dialCVHarmonicScale.value()))  #  / 1000
                cvOffset = str(self.ui.widgetCVHarmonicNoteOffset.value()) # + self.ui.dialCVHarmonicNoteOffset.value() * 1327.716667)
                cvZero = self.ui.widgetCVHarmonicZero.value()
                cmd += commandSets.getQualifiedShortCommand(CommandID.bowHarmonicAdd)[0] + ":(value"
                if int(cvZero) >= 0:
                    cmd += "+"
                cmd += str(cvZero) + ")/" + str(cvScale) + "+(" + str(cvOffset) + ")"
            case 1:
                cmd = cl.buildCommandString({commandSets.getQualifiedShortCommand(CommandID.bowHarmonicShift5)[0]})
                cvScale = str(2.425 / (self.ui.dialCVHarmonicShiftScale.value()))    #  / 1000
                cvOffset = -(32767 - self.ui.dialCVHarmonicShiftZero.value())
                cmd += commandSets.getQualifiedShortCommand(CommandID.bowHarmonicShift5)[0] + ":\"deadband(value" + str(cvOffset) + ", 30)/" + str(cvScale) + "\""
            case 2:
                cmd = cl.buildCommandString({commandSets.getQualifiedShortCommand(CommandID.bowHarmonicShift)[0]})
                cmd += (commandSets.getQualifiedShortCommand(CommandID.bowHarmonicShift)[0]+
                        ":\"deadband(value-" + str(32767 - self.ui.dialCVFineTuneCenter.value()) + ", 400)*0.49064\"")
            case 5:

                cmd = cl.buildCommandString({ commandSets.getQualifiedShortCommand(CommandID.motorRun)[0],
                                              commandSets.getQualifiedShortCommand(CommandID.bowPIDEnable)[0],
                                              commandSets.getQualifiedShortCommand(CommandID.bowSpeedMode)[0],
                                              commandSets.getQualifiedShortCommand(CommandID.bowPressureEngage)[0],
                                              commandSets.getQualifiedShortCommand(CommandID.bowPressureRest)[0],
                                              commandSets.getQualifiedShortCommand(CommandID.bowPressureHold)[0] })

                #"bmr","bpid","bcsm","bpe","bpr","bph"
                if cmd != "":
                    cmd += ","
                if mainWidget.ui.checkBoxCVGatePowerMotor.isChecked():
                    cmd += commandSets.getQualifiedShortCommand(CommandID.motorRun)[0] + ":1," + \
                           commandSets.getQualifiedShortCommand(CommandID.bowPIDEnable)[0] + ":1," + \
                           commandSets.getQualifiedShortCommand(CommandID.bowSpeedMode)[0] + ":0,"
                    #cmd += "bmr:1,bpid:1,bcsm:0,"
                if mainWidget.ui.checkBoxCVGateEngage.isChecked():
                    cmd += commandSets.getQualifiedShortCommand(CommandID.bowPressureEngage)[0] + ":bool(value-" + \
                           str(mainWidget.ui.widgetCVGateThreshold.value()) + "),bpr:ibool(value-" + \
                           str(mainWidget.ui.widgetCVGateThreshold.value()) + "),"
#                    cmd += ("bpe:bool(value-" + str(mainWidget.ui.widgetCVGateThreshold.value()) + "),bpr:ibool(value-" +
#                            str(mainWidget.ui.widgetCVGateThreshold.value()) + "),")
                if mainWidget.ui.checkBoxCVGateHold.isChecked():
                    cmd += commandSets.getQualifiedShortCommand(CommandID.bowPressureHold)[0] + ":ibool(value-" + \
                           str(mainWidget.ui.widgetCVGateThreshold.value()) + ")"
                    #cmd += "bph:ibool(value-" + str(mainWidget.ui.widgetCVGateThreshold.value()) + ")"
                pass
        #cmd = "bchs:"
        #0 - bcha:value/1327.716667-20
        #  - multiplier = 1/1327
        #  - offset = -20
        #  - cvScale = multiplier * 1327
        #       range = 0.5 - 1 - 2 (500 to 2000)
        #       multiplierCalculated = (range / 1000) * 1327.716667
        #  - cvOffset = abs(offset % 1327), flip sign of offset if offset < 0
        #       range = -1 - 0 - 1 (-1327 to 1327)
        #       offsetCalculated = cvOffset
        #  - noteOffset = -20
        #       range = -24 - 24
        #       offsetCalculated += (range * multiplierCalculated)
        #1 - bchs5:"deadband(value-32236, 20)/2.425"
        #  - multiplier = 2.425
        #  - offset = -32236
        #  - cvScale = multiplier * 100
        #  -    range = 0.5 - 1 - 2 (500 to 2000)
        #  -    multiplierCalculated = (range / 1000) * 2.425
        #  - cvOffset = offset + 32767
        #  -    range = -1 - 0 - 1 (-1327 to 1327)
        #  -    offsetCalculated = range
        #2 - bchsh:"deadband((value-32600)*0.49064, 250)"
        #5 - bmr:1,bpid:1,bcsm:0,bpe:bool(value-1000),bpr:ibool(value-1000),bph:ibool(value-1000)
        #6 - sfm:"deadband(1/65535*value,0.002)"
        if cmd == "":
            return
        setCommands = commandSets.getQualifiedShortCommand(CommandID.controlBoxControlData)[0]
        cmd = setCommands + ":" + str(widget.CVcontrol) + ":'" + cmd + "'"
        serialHandler.write(cmd)

    def connectCVMappingModifiers(self, CVcontrol, widgets):
        for widget in widgets:
            widget.CVcontrol = CVcontrol
            #widget.valueChanged.connect(self.widgetCVMappingCallback)
            if isinstance(widget, QDial):
                mainWidget.assignMouseReleaseEvent(widget, self.widgetCVMappingCallback)
            if isinstance(widget, QDoubleSpinBox):
                widget.valueChanged.connect(self.widgetCVMappingCallback)
            if isinstance(widget, QCheckBox):
                widget.stateChanged.connect(self.widgetCVMappingCallback)

    def widgetCVTextCallback(self):
        widget = self.sender()
        cmd = widget.text()
        setCommands = commandSets.getQualifiedShortCommand(CommandID.controlBoxControlData)[0]
        cmd = setCommands + ":" + str (widget.CVcontrol) + ":'" + cmd + "'"
        serialHandler.write(cmd)

    def connectCVTextWidgets(self, CVcontrol, widget):
        widget.CVcontrol = CVcontrol
        widget.returnPressed.connect(self.widgetCVTextCallback)

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

    def assignMouseReleaseEvent(self, qtObject, function):
        qtObject.mouseReleaseEvent = lambda event: self.mouseReleaseEventIntermediate(event, qtObject)
        qtObject.mouseReleaseFunction = function

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

    def CVFinetuneCalibrate(self):
        messageBox("CV fine tuning center calibration",
                   "Turn the 'Harmonic shift'-knob all the way to the left, then turn it to the center.\nPress OK when you are done")
        setADC = commandSets.getQualifiedShortCommand(CommandID.controlBoxDataReturn)[0]
        serialHandler.write("rqi:" + setADC + ":2")
        QTimer.singleShot(1000, self.CVFinetuneCalibrateContinue)

    def CVFinetuneCalibrateContinue(self):
        self.firstCv = simpleFARHandler.stringModules[0].getCVValue(2)
        messageBox("CV fine tuning center calibration",
                   "Now turn the 'Harmonic shift'-knob all the way to the right, then turn it to the center.\nPress OK when you are done")
        setADC = commandSets.getQualifiedShortCommand(CommandID.controlBoxDataReturn)[0]
        serialHandler.write("rqi:" + setADC + ":2")
        QTimer.singleShot(1000, self.CVFinetuneCalibrateFinish)

    def CVFinetuneCalibrateFinish(self):
        offset = (simpleFARHandler.stringModules[0].getCVValue(2) - self.firstCv) / 2
        mainWidget.ui.dialCVFineTuneCenter.setValue(offset)
        harmonicShift = commandSets.getQualifiedShortCommand(CommandID.bowHarmonicShift)[0]
        serialHandler.write(harmonicShift + ":0")

    def CVHarmonicShiftZeroCalibrate(self):
        messageBox("Harmonic shift zero calibation", "Turn the 'Harmonic shift modulation'-knob all the way to the right, then turn it all the way to the left.\nPress OK when you are done")
        setADC = commandSets.getQualifiedShortCommand(CommandID.controlBoxDataReturn)[0]
        serialHandler.write("rqi:" + setADC + ":1")
        QTimer.singleShot(1000, self.CVHarmonicShiftZeroCalibrateContinue)

    def CVHarmonicShiftZeroCalibrateContinue(self):
        cv = simpleFARHandler.stringModules[0].getCVValue(1)
        mainWidget.ui.dialCVHarmonicShiftZero.setValue(32767 - cv)
        harmonicShift5 = commandSets.getQualifiedShortCommand(CommandID.bowHarmonicShift5)[0]
        serialHandler.write(harmonicShift5 + ":0")

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

def save_settings():
    # Save window geometry using QSettings
    settings = QSettings("Knas", "Ekdahl FAR Config")
    settings.setValue("mainGeometry", mainWidget.saveGeometry())
    settings.setValue("consoleGeometry", serialWidget.saveGeometry())
    settings.setValue("consoleWindowVisible", serialWidget.isVisible())
    settings.setValue("filterHardware", serialWidget.ui.checkBoxFilterHardware.checkState())
    settings.setValue("filterUSB", serialWidget.ui.checkBoxFilterUSB.checkState())
    settings.setValue("filterDebug", serialWidget.ui.checkBoxFilterDebug.checkState())
    settings.setValue("filterError", serialWidget.ui.checkBoxFilterError.checkState())
    settings.setValue("filterOutput", serialWidget.ui.checkBoxFilterOutput.checkState())
    settings.setValue("filterPriority", serialWidget.ui.checkBoxFilterPriority.checkState())
    settings.setValue("filterUndefined", serialWidget.ui.checkBoxFilterUndefined.checkState())
    settings.setValue("filterCommAck", serialWidget.ui.checkBoxFilterCommAck.checkState())
    settings.setValue("filterExpressionParser", serialWidget.ui.checkBoxFilterExpressionParser.checkState())
    settings.setValue("filterInfoRequest", serialWidget.ui.checkBoxFilterInfoRequest.checkState())
    settings.setValue("consoleLineCount", serialWidget.ui.spinBoxLimitLines.value())
    settings.setValue("consoleLineLimit", serialWidget.ui.checkBoxLimitLines.checkState())
    settings.setValue("consoleCursorFollow", serialWidget.ui.checkBoxDebugCursorFollow.checkState())

    settings.setValue("chartA0", mainWidget.ui.checkBoxChartA0.checkState())
    settings.setValue("chartA1", mainWidget.ui.checkBoxChartA1.checkState())
    settings.setValue("chartA2", mainWidget.ui.checkBoxChartA2.checkState())
    settings.setValue("chartA3", mainWidget.ui.checkBoxChartA3.checkState())
    settings.setValue("chartA4", mainWidget.ui.checkBoxChartA4.checkState())
    settings.setValue("chartA5", mainWidget.ui.checkBoxChartA5.checkState())
    settings.setValue("chartA6", mainWidget.ui.checkBoxChartA6.checkState())
    settings.setValue("chartA7", mainWidget.ui.checkBoxChartA7.checkState())
    settings.setValue("chartAudPk", mainWidget.ui.checkBoxChartAudPk.checkState())
    settings.setValue("chartMotFreq", mainWidget.ui.checkBoxChartMotFreq.checkState())
    settings.setValue("chartPeakErr", mainWidget.ui.checkBoxChartPeakErr.checkState())
    settings.setValue("chartMotCurr", mainWidget.ui.checkBoxChartMotCurr.checkState())
    settings.setValue("chartReadFreq", mainWidget.ui.checkBoxChartReadFreq.checkState())
    settings.setValue("chartAudFFT", mainWidget.ui.checkBoxChartAudFFT.checkState())
    settings.setValue("chartAudRMS", mainWidget.ui.checkBoxChartAudRMS.checkState())

    settings.setValue("referenceGeometry", commandReference.saveGeometry())
    settings.setValue("referenceWindowVisible", commandReference.isVisible())

def loadCheckState(settings, name, checkBox):
    state = settings.value(name)
    if state == Qt.CheckState.Checked or state == 'Checked':
        checkBox.setCheckState(Qt.CheckState.Checked)
    else:
        checkBox.setCheckState(Qt.CheckState.Unchecked)

def load_settings():
    # Load window geometry using QSettings
    settings = QSettings("Knas", "Ekdahl FAR Config")
    mainGeometry = settings.value("mainGeometry")
    if mainGeometry:
        mainWidget.restoreGeometry(mainGeometry)
    consoleGeometry = settings.value("consoleGeometry")
    if consoleGeometry:
        serialWidget.restoreGeometry(consoleGeometry)
    consoleWindowVisible = settings.value("consoleWindowVisible")

    if consoleWindowVisible is True or consoleWindowVisible == 'true':
        serialWidget.show()
    else:
        serialWidget.hide()
    loadCheckState(settings, "filterHardware", serialWidget.ui.checkBoxFilterHardware)
    loadCheckState(settings, "filterUSB", serialWidget.ui.checkBoxFilterUSB)
    loadCheckState(settings, "filterDebug", serialWidget.ui.checkBoxFilterDebug)
    loadCheckState(settings, "filterUndefined", serialWidget.ui.checkBoxFilterUndefined)
    loadCheckState(settings, "filterError", serialWidget.ui.checkBoxFilterError)
    loadCheckState(settings, "filterOutput", serialWidget.ui.checkBoxFilterOutput)
    loadCheckState(settings, "filterPriority", serialWidget.ui.checkBoxFilterPriority)
    loadCheckState(settings, "filterCommAck", serialWidget.ui.checkBoxFilterCommAck)
    loadCheckState(settings, "filterInfoRequest", serialWidget.ui.checkBoxFilterInfoRequest)
    loadCheckState(settings, "filterExpressionParser", serialWidget.ui.checkBoxFilterExpressionParser)
    loadCheckState(settings, "consoleLineLimit", serialWidget.ui.checkBoxLimitLines)
    loadCheckState(settings, "consoleCursorFollow", serialWidget.ui.checkBoxDebugCursorFollow)
    #settings.setValue("consoleLineCount", serialWidget.ui.spinBoxLimitLines.value())
    try:
        serialWidget.ui.spinBoxLimitLines.setValue(int(settings.value("consoleLineCount")))
    except:
        pass

    loadCheckState(settings, "chartA0", mainWidget.ui.checkBoxChartA0)
    loadCheckState(settings, "chartA1", mainWidget.ui.checkBoxChartA1)
    loadCheckState(settings, "chartA2", mainWidget.ui.checkBoxChartA2)
    loadCheckState(settings, "chartA3", mainWidget.ui.checkBoxChartA3)
    loadCheckState(settings, "chartA4", mainWidget.ui.checkBoxChartA4)
    loadCheckState(settings, "chartA5", mainWidget.ui.checkBoxChartA5)
    loadCheckState(settings, "chartA6", mainWidget.ui.checkBoxChartA6)
    loadCheckState(settings, "chartA7", mainWidget.ui.checkBoxChartA7)
    loadCheckState(settings, "chartAudRMS", mainWidget.ui.checkBoxChartAudRMS)
    loadCheckState(settings, "chartAudPk", mainWidget.ui.checkBoxChartAudPk)
    loadCheckState(settings, "chartAudFFT", mainWidget.ui.checkBoxChartAudFFT)
    loadCheckState(settings, "chartReadFreq", mainWidget.ui.checkBoxChartReadFreq)
    loadCheckState(settings, "chartMotCurr", mainWidget.ui.checkBoxChartMotCurr)
    loadCheckState(settings, "chartPeakErr", mainWidget.ui.checkBoxChartPeakErr)
    loadCheckState(settings, "chartMotFreq", mainWidget.ui.checkBoxChartMotFreq)

    referenceGeometry = settings.value("referenceGeometry")
    if referenceGeometry:
        commandReference.restoreGeometry(referenceGeometry)
    referenceWindowVisible = settings.value("referenceWindowVisible")
    if referenceWindowVisible is True or referenceWindowVisible == 'true':
        commandReference.show()
    else:
        commandReference.hide()

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

    mainWidget.assignMouseReleaseEvent(mainWidget.ui.midiNoteOnVelToHammer, mainWidget.cmdNoteOnUpdate)

    mainWidget.ui.midiNoteOnHammerStaccato.stateChanged.connect(mainWidget.cmdNoteOnUpdate)
    mainWidget.ui.midiNoteOnSendMuteRest.stateChanged.connect(mainWidget.cmdNoteOnUpdate)

    mainWidget.ui.midiNoteOffSendFullMute.stateChanged.connect(mainWidget.cmdNoteOffUpdate)
    mainWidget.ui.midiNoteOffMotorOff.stateChanged.connect(mainWidget.cmdNoteOffUpdate)

    mainWidget.populateComboBoxSendByte(mainWidget.ui.midiPitchbendSend)
    mainWidget.connectWidgetsToMIDIEvent("pb", { mainWidget.ui.midiPitchbendSend, mainWidget.ui.midiPitchbendRatio })
    mainWidget.populateComboBoxSendByte(mainWidget.ui.midiPolyATSend)
    mainWidget.connectWidgetsToMIDIEvent("pat", {mainWidget.ui.midiPolyATSend, mainWidget.ui.midiPolyATRatio})
    mainWidget.populateComboBoxSendByte(mainWidget.ui.midiChannelATSend)
    mainWidget.connectWidgetsToMIDIEvent("cat", {mainWidget.ui.midiChannelATSend, mainWidget.ui.midiChannelATRatio})

    mainWidget.populateComboBoxSendBinary(mainWidget.ui.midiSustainSend)
    mainWidget.connectWidgetsToBinarySenders("sustain", { mainWidget.ui.midiSustainInvert, mainWidget.ui.midiSustainSend })

    mainWidget.ui.listWidgetMidiEvents.currentItemChanged.connect(mainWidget.listWidgetMidiEventscurrentItemChanged)
    mainWidget.ui.lineEditMidiEventCommand.editingFinished.connect(mainWidget.lineEditMidiEventCommandFinished)
    mainWidget.ui.pushButtonCCAdd.pressed.connect(mainWidget.ccAdd)
    mainWidget.ui.pushButtonCCRemove.pressed.connect(mainWidget.ccRemove)

## Tab CV Mapping
    mainWidget.connectCVMappingModifiers(0, { mainWidget.ui.dialCVHarmonicScale, mainWidget.ui.widgetCVHarmonicNoteOffset,
                                              mainWidget.ui.widgetCVHarmonicZero})
    mainWidget.connectCVTextWidgets(0, mainWidget.ui.plainTextEditCVHarmonicCommands)

    mainWidget.connectCVMappingModifiers(1, { mainWidget.ui.dialCVHarmonicShiftScale, mainWidget.ui.dialCVHarmonicShiftZero })
    mainWidget.connectCVTextWidgets(1, mainWidget.ui.plainTextEditCVHarmonicShiftCommands)
    mainWidget.ui.pushButtonCVHarmonicShiftZeroCalibrate.pressed.connect(mainWidget.CVHarmonicShiftZeroCalibrate)

    mainWidget.connectCVMappingModifiers(2, { mainWidget.ui.dialCVFineTuneCenter })
    mainWidget.connectCVTextWidgets(2, mainWidget.ui.plainTextEditCVFineTuneCommands)
    mainWidget.ui.pushButtonCVFinetuneCalibrate.pressed.connect(mainWidget.CVFinetuneCalibrate)

    mainWidget.connectCVTextWidgets(3, mainWidget.ui.plainTextEditCVPressureCommands)
    mainWidget.connectCVTextWidgets(4, mainWidget.ui.plainTextEditCVHammerTriggerCommands)

    mainWidget.connectCVMappingModifiers(5, { mainWidget.ui.checkBoxCVGateHold, mainWidget.ui.checkBoxCVGateEngage,
                                              mainWidget.ui.checkBoxCVGatePowerMotor, mainWidget.ui.widgetCVGateThreshold})
    mainWidget.connectCVTextWidgets(5, mainWidget.ui.plainTextEditCVGateCommands)

    mainWidget.connectCVTextWidgets(6, mainWidget.ui.plainTextEditCVHammerScaleCommands)
    mainWidget.connectCVTextWidgets(7, mainWidget.ui.plainTextEditCVMuteCommands)

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

    mainWidget.ui.pushButtonClearAverages.pressed.connect(mainWidget.averagesClear)
    mainWidget.ui.pushButtonTestAverages.pressed.connect(mainWidget.averagesTest)

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
#    localNodehandler = nodehandler.NodeHandler(mainWidget.ui.nodeContainer)

    '''
    commandList = ["mev:noteon:\"m:'map(0, note)',b:'map(0, note)',s:'map(0, note)',bchb:note,bmr:1,bpid:1,bpe:1,se:(velocity*512)*(1-notecount)\"", #,bcsm:0,
                   "mev:noteoff:\"m:'map(0, note)',b:'map(0, note)',s:'map(0, note)',bpr:ibool(notecount)\"",    #,bcsm:0,m:'map(0, note)',b:'map(0, note)',s:'map(0, note)',
                   "mev:cat:\"m:0:1:2:3,bpm:(pressure*512)\"",
                   "mev:pb:\"m:0:1:2:3,bchsh:pitch*4\"",
                   "acm:0:'s:0,bcha:value/1327.716667-20'",
                   "acm:1:'bchs5:\"deadband(value-32236, 20)/2.425\"'",
                   "acm:2:'bchsh:\"deadband((value-32600)*0.49064, 250)\"'",
                   "acm:3:'bpb:value'",
                   "acm:4:'se:value'",
                   "acm:5:'bmr:bool(value-10000),bpid:1,bcsm:0,bpe:bool(value-10000),bpr:ibool(value-10000),bph:ibool(value-10000)'",
                   "acm:6:'sfm:\"deadband(1/65535*value,0.002)\"'",
                   "acm:7:'msp:value'"]
    #commandList = ["mev:noteon:\"m:0,b:0,bchb:note,bmr:1,bpid:1,bpe:1,se:(velocity*512)*(1-notecount),bcsm:0\""]

    for command in commandList:
        item = commandparser.CommandItem(command)
        localNodehandler.parseCommand(item)
    localNodehandler.postBuildUpdate()
    localNodehandler.ga.update()
    #group = localNodehandler.ga.graph.create_node("nodes.group.CustomGroupNode")
    #group.migrate_objects()

    mainWidget.ui.tabWidgetMain.setCurrentIndex(7)
    serialWidget.hide()
    commandReference.hide()
    '''

    mainWidget.destroyed.connect(mainWidget.closeEvent)
    mainWidget.populateFundamentalComboBox()
    mainWidget.USBRefreshTimer = QTimer()
    mainWidget.USBRefreshTimer.timeout.connect(mainWidget.populateSerialPorts)
    mainWidget.USBRefreshTimer.start(1000)

    serialWidget.addToDebugWindow("Initialized\n")
    sys.exit(app.exec())
    mainWidget.thread1.terminate()

