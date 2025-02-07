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
                               QComboBox, QSlider, QTabBar, QTabWidget, QVBoxLayout, QCheckBox, QDial, QPushButton)
from PySide6.QtCore import QThread, Signal, QTimer, QModelIndex, Qt, QObject, QDir, Slot, QSettings, QSize, QRect
from PySide6.QtGui import QTextBlock, QTextCursor, QTextBlockFormat, QColor, QIcon, QPainter, QTransform, QShortcut, QKeySequence

import re

import commandparser
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

#def except_hook(cls, exception, traceback):
#    sys.__excepthook__(cls, exception, traceback)

from time import process_time

import mido

from commandparser import CommandItem, CommandList

import timedChart

#import midihandler

from stringModule import stringModule, CC, InstrumentMaster

global serialStream
#serialStream = None

stringModules = []
instrumentMaster = InstrumentMaster()

currentSerialModule = 0
currentBow = 0
moduleCount = 0
currentHarmonicListSelected = 0

currentShowingModule = 0
#updatingFromModule = False

adcAverages = [averager.Averager() for i in range(8)]

def addModulesIfNeeded(needed):
    global stringModules
    while len(stringModules) <= needed:
        stringModules.append(stringModule())
    while (mainWidget.ui.comboBoxCurrentlySelectedModule.count() <= needed):
        mainWidget.ui.comboBoxCurrentlySelectedModule.addItem(str(mainWidget.ui.comboBoxCurrentlySelectedModule.count() + 1))

def processInformationForChart(inSerialHandler, command):
    inSerialHandler.chartCommandSignal.emit(command)
    return

# processInformationReturn updates both the stringModule attached and the GUI
def processInformationReturn(inSerialHandler, infoReturn):
    #print("processInformationReturn")
    commandList = CommandList()
    commandList.addCommands(infoReturn)

    global stringModules
    global currentSerialModule
    global currentBow
    mainWidget.updatingFromModule = True

    processed = True

    for i in commandList.commands:
        #processed = processInformationForChart(inSerialHandler, i)
        processInformationForChart(inSerialHandler, i)
        match i.command:
            case "m":
                currentSerialModule = int(i.argument[0])
                addModulesIfNeeded(currentSerialModule)
                print ("setting current serial module to " + i.argument[0])
            case "mc":
                global moduleCount
                try:
                    moduleCount = int(i.argument[0])
                    addModulesIfNeeded(moduleCount - 1)
                    print("setting module count to " + i.argument[0])
                except:
                    messageBox("Error", "Error retreiving module count!")
            case "b" | "bcu" | "bmv" | "bmt" | "bpkp" | "bpki" | "bpkd" | "bpie" | "mfmp" | "mhmp" | "mrp" | "mbo" | \
                 "bmsx" | "bmsi" | "bppx" | "bppe" | "bppr" | "bmf" | "psf" | "bmc" | "sxf" | "sif" | "sed" | "bcf" | \
                 "bpkp" | "bpki" | "bkpd" | "bpie" | "bpme" | "bhs" | "bch" | "bchb" | "bchshr" | "bchsh" | "bchs5" | \
                 "ba" | "bcha" | "bchsr":
                stringModules[currentSerialModule].setCommandValue(i.command, float(i.argument[0]))
                mainWidget.updateStringModuleData()
            case "bhsl":
                try:
                    hl = i.argument[0]
                    #print(hl)
                    print(len(stringModules[currentSerialModule].harmonicData))
    #                if (int(hl) != len(stringModules[currentSerialModule].harmonicData)):
    #                    print("Error, harmonic list is broken")
    #                    return
    #                hs = []
                    stringModules[currentSerialModule].harmonicData.clear()
    #                hsi = 1
                    hsi = 0
                    while (hsi < len(i.argument)):
                        print("Adding value " + str(i.argument[hsi]))
     #                   hs.append(i.argument[hsi])
                        stringModules[currentSerialModule].harmonicData.append(i.argument[hsi])
                        hsi += 1
    #                stringModules[currentSerialModule].harmonicData.append(hs)
                    mainWidget.updateHarmonicTable()
                    print("Added harmonic list " + str(stringModules[currentSerialModule].harmonicData))
                except  :
                    messageBox("Problem! Yes!", "Oh no")
            case "bhsd":
                try:
#                    hl = i.argument[0]
                    print(len(stringModules[currentSerialModule].harmonicData))
                    stringModules[currentSerialModule].harmonicData.clear()
                    hsi = 2
                    while (hsi < len(i.argument)):
                        print("Adding value " + str(i.argument[hsi]))
                        stringModules[currentSerialModule].harmonicData.append(i.argument[hsi])
                        hsi += 1
                    mainWidget.updateHarmonicTable()
                    print("Added harmonic list " + str(stringModules[currentSerialModule].harmonicData))
                except:
                    messageBox("Problem! Yes!", "Oh no")

            case "bhsc":
                mainWidget.ui.comboBoxHarmonicList.clear()
                hl = 0
                while (hl < int(i.argument[0])):
                    #mainWidget.ui.comboBoxHarmonicList.addItem(str(hl))
                    mainWidget.ui.comboBoxHarmonicList.addItem(str(i.argument[hl + 1]))
                    serialHandler.write("rqi:bhsd:" + str(hl))
                    hl += 1
                mainWidget.ui.comboBoxHarmonicList.setCurrentIndex(stringModules[currentSerialModule].getCommandValue("bhs"))
            case "mev":
                match i.argument[0]:
                    case "noteon":
                        mainWidget.remove_item(mainWidget.ui.listWidgetMidiEvents, "Note On")
                        instrumentMaster.evNoteOn = i.argument[1]
                        mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Note On"))

                        instrumentMaster.cmdNoteOn.clear()
                        instrumentMaster.cmdNoteOn.addCommands(i.argument[1])
                        offset, multiplier = equationParsingHelpers.getVariable(instrumentMaster.cmdNoteOn.getCommandAttribute("se", 0),"velocity")
                        mainWidget.ui.midiNoteOnVelToHammer.setValue(multiplier)

                        if equationParsingHelpers.isVariableInEquation(instrumentMaster.cmdNoteOn.getCommandAttribute("se", 0), "notecount"):
                            mainWidget.ui.midiNoteOnHammerStaccato.setChecked(True)
                        else:
                            mainWidget.ui.midiNoteOnHammerStaccato.setChecked(False)

                        if not instrumentMaster.cmdNoteOn.getCommandAttribute("mr", 0) == "":
                            mainWidget.ui.midiNoteOnSendMuteRest.setChecked(True)
                        else:
                            mainWidget.ui.midiNoteOnSendMuteRest.setChecked(False)

#                        mainWidget.ui.midiNoteOnOther.setText(instrumentMaster.evNoteOn)

                        print("Setting NoteOn to " + str(instrumentMaster.evNoteOn))
                    case "noteoff":
                        mainWidget.remove_item(mainWidget.ui.listWidgetMidiEvents, "Note Off")
                        instrumentMaster.evNoteOff = i.argument[1]
                        mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Note Off"))

                        instrumentMaster.cmdNoteOff.clear()
                        instrumentMaster.cmdNoteOff.addCommands(i.argument[1])

                        if not instrumentMaster.cmdNoteOff.getCommandAttribute("mfm", 0) == "":
                            mainWidget.ui.midiNoteOffSendFullMute.setChecked(True)
                        else:
                            mainWidget.ui.midiNoteOffSendFullMute.setChecked(False)

                        if not instrumentMaster.cmdNoteOff.getCommandAttribute("bmr", 0) == "":
                            mainWidget.ui.midiNoteOffMotorOff.setChecked(True)
                        else:
                            mainWidget.ui.midiNoteOffMotorOff.setChecked(False)

#                        mainWidget.ui.midiNoteOffOther.setText(instrumentMaster.evNoteOff)

                        print("Setting NoteOff to " + str(instrumentMaster.evNoteOff))
                    case "cc":
                        mainWidget.remove_item(mainWidget.ui.listWidgetMidiEvents, "CC " + str(i.argument[1]))

                        instrumentMaster.addCC(int(i.argument[1]), str(i.argument[2]))
                        mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("CC " + str(i.argument[1])))
                        print("Setting CC " + i.argument[1] + " to " + str(i.argument[2]))
                    case "pat":
                        mainWidget.remove_item(mainWidget.ui.listWidgetMidiEvents, "Poly Aftertouch")
                        instrumentMaster.evPolyAftertouch = i.argument[1]
                        mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Poly Aftertouch"))

                        instrumentMaster.cmdPolyAftertouch.clear()
                        instrumentMaster.cmdPolyAftertouch.addCommands(i.argument[1])

                        mainWidget.selectSendDestinationAndRatio(mainWidget.ui.midiPolyATSend, instrumentMaster.cmdPolyAftertouch,
                                                      mainWidget.ui.midiPolyATRatio, "pressure")

                        print("Setting polyphonic aftertouch to " + str(instrumentMaster.evPolyAftertouch))
                    case "pb":
                        mainWidget.remove_item(mainWidget.ui.listWidgetMidiEvents, "Pitchbend")
                        instrumentMaster.evPitchbend = i.argument[1]
                        mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Pitchbend"))

                        instrumentMaster.cmdPitchbend.clear()
                        instrumentMaster.cmdPitchbend.addCommands(i.argument[1])

                        mainWidget.selectSendDestinationAndRatio(mainWidget.ui.midiPitchbendSend, instrumentMaster.cmdPitchbend,
                                                      mainWidget.ui.midiPitchbendRatio, "pitch", 127)

                        print("Setting polyphonic aftertouch to " + str(instrumentMaster.evPitchbend))
                    case "cat":
                        mainWidget.remove_item(mainWidget.ui.listWidgetMidiEvents, "Channel Aftertouch")
                        instrumentMaster.evChannelAftertouch = i.argument[1]
                        mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Channel Aftertouch"))

                        instrumentMaster.cmdChannelAftertouch.clear()
                        instrumentMaster.cmdChannelAftertouch.addCommands(i.argument[1])

                        mainWidget.selectSendDestinationAndRatio(mainWidget.ui.midiChannelATSend, instrumentMaster.cmdChannelAftertouch,
                                                      mainWidget.ui.midiChannelATRatio, "pressure")

                        print("Setting polyphonic aftertouch to " + str(instrumentMaster.evChannelAftertouch))
                    case "pc":
                        mainWidget.remove_item(mainWidget.ui.listWidgetMidiEvents, "Program change")
                        instrumentMaster.evProgramChange = i.argument[1]
                        mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Program change"))

                        print("Setting polyphonic aftertouch to " + str(instrumentMaster.evProgramChange))

            case "bchbn":
                for a in range(1, mainWidget.ui.comboBoxBaseNote.count()):
                    if int(mainWidget.ui.comboBoxBaseNote.itemData(a)) == int(i.argument[0]):
                        mainWidget.ui.comboBoxBaseNote.setCurrentIndex(a)
                #mainWidget.ui.progressBar_bchbn.setValue(int(i.argument[0]))
                stringModules[currentSerialModule].setCommandValue(i.command, float(i.argument[0]))
                print("setting base note to " + str(i.argument[0]))

            case "adcr":
                #print("adcr " + str(i.argument[0]) + ":" + str(i.argument[1]))
                stringModules[currentSerialModule].setCVValue(int(i.argument[0]), int(i.argument[1]))
                #print("module data " + str(stringModules[currentSerialModule].getCVValue(0)))
                mainWidget.updateContinuousStringModuleData()
                adcAverages[int(i.argument[0])].addValue(i.argument[1])
                mainWidget.updateAverages()

            case "bac":
                print("bac " + str(i.argument[0]))
                mainWidget.ui.comboBoxActuatorPreset.clear()
                for a in range(0, int(i.argument[0])):
                    serialHandler.write("rqi:bad:" + str(a))

            case "bad":
                print("bad")
                if (len(i.argument) < 5):
                    break
                if (i.argument[4]) == "":
                    i.argument[4] = "noname" + str(random.randrange(0,9999))
                    #break

                mainWidget.ui.comboBoxActuatorPreset.addItem(i.argument[4], i.argument[0])
                mainWidget.ui.comboBoxActuatorPreset.setCurrentIndex(stringModules[currentSerialModule].getCommandValue("ba"))

            case  "mcf":
                stringModules[currentSerialModule].setCommandValue(i.command, float(i.argument[0]))
                mainWidget.updateStringModuleData()
                mainWidget.ui.listWidgetMidiEvents.clear()
                mainWidget.ui.comboBoxConfiguration.setCurrentIndex(int(stringModules[currentSerialModule].getCommandValue("mcf")))
                serialHandler.write("rqi:mev")

            case "mcfc":
                mainWidget.ui.comboBoxConfiguration.clear()
                for a in range(0, int(i.argument[0])):
                    serialHandler.write("rqi:mcfn:" + str(a))

            case "mcfn":
#                mainWidget.remove_item(mainWidget.ui.comboBoxConfiguration, str(i.argument[1]))
                index = mainWidget.find_item(mainWidget.ui.comboBoxConfiguration, str(i.argument[1]))
                if (index != -1):
                    mainWidget.ui.comboBoxConfiguration.removeItem(index)
                mainWidget.ui.comboBoxConfiguration.insertItem(int(i.argument[0]), str(i.argument[1]))
                mainWidget.ui.comboBoxConfiguration.setCurrentIndex(stringModules[currentSerialModule].getCommandValue("mcf"))

#            case "bcp":
#                if mainWidget.modalEvent == "bcp":
#                    mainWidget.modalDialog.stop()
#                mainWidget.updateUIData()

            case "mrc":
                mainWidget.ui.comboBoxMidiChannel.blockSignals(True)
                ch = int (i.argument[0])
                if ((ch < 1) or (ch >16)):
                    find = "Omni"
                else:
                    find = str(ch)

                for a in range(0, mainWidget.ui.comboBoxMidiChannel.count()):
                    if find == mainWidget.ui.comboBoxMidiChannel.itemText(a):
                        mainWidget.ui.comboBoxMidiChannel.setCurrentIndex(a)
                        break
                mainWidget.ui.comboBoxMidiChannel.blockSignals(False)

            case "acm":
                match int(i.argument[0]):
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
                        messageBox("ADC Command error", "ADC Command error")
                        return

                widget.setText(i.argument[1])
                stringModules[currentSerialModule].setCVCommand(i.argument[0], i.argument[1])
                mainWidget.updateCVData()

            case mainWidget.modalEvent:
                mainWidget.modalDialog.stop()
                mainWidget.updateUIData()

            case _:
                processed = processed | False
                    #processed = False
        #except Exception as e:
        #    pass

    mainWidget.updatingFromModule = False
    return processed

def messageBox(title, message):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(message)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(QMessageBox.Ok) # | QMessageBox.Cancel)
    #msgBox.buttonClicked.connect(msgButtonClick)

    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        print('OK clicked')

def inputBox(title, message):
    text, ok = QInputDialog().getText(mainWidget, title, message, QLineEdit.Normal)
    if ok and text:
        return text
    else:
        return None

def processHelpReturn(infoReturn):
    commandList = CommandList()
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
                skip = True
                print("Unknown " + i.command)

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

            #commandReference.add_row([command, short, scope, i.argument[1], i.argument[2]])

            commandReference.addCommand(command, help)

            #commandItemHelp = QListWidgetItem()
            #commandItemHelp.setText(command)
            #commandItemHelp.setData(Qt.UserRole, help)
            #mainWidget.ui.listWidgetCommands.addItem(commandItemHelp)
            print(help)

def requestStringModuleData():
    serialHandler.write("rqi:bowcontrolfundamental")
    serialHandler.write("rqi:bmv")
    serialHandler.write("rqi:bowpidki")
    serialHandler.write("rqi:bowpidkp")
    serialHandler.write("rqi:bowpidkd")
    serialHandler.write("rqi:bowpidintegratorerror")
    serialHandler.write("rqi:bowmotortimeout")
    serialHandler.write("rqi:mutefullmuteposition")
    serialHandler.write("rqi:mutehalfmuteposition")
    serialHandler.write("rqi:muterestposition")
    serialHandler.write("rqi:mutebackoff")
    serialHandler.write("rqi:bowmotorspeedmax")
    serialHandler.write("rqi:bowmotorspeedmin")
    serialHandler.write("rqi:bowpressurepositionmax")
    serialHandler.write("rqi:bowpressurepositionengage")
    serialHandler.write("rqi:bowpressurepositionrest")
#    serialHandler.write("rqi:bowcontrolharmoniclist")
#    serialHandler.write("rqi:bowcontrolharmoniccount")

    serialHandler.write("rqi:bowcontrolharmonic")
    serialHandler.write("rqi:bowcontrolharmonicbase")
    serialHandler.write("rqi:bowcontrolharmonicbasenote")
    serialHandler.write("rqi:bowcontrolharmonicadd")
    serialHandler.write("rqi:bowcontrolharmonicshift")
    serialHandler.write("rqi:bowcontrolharmonicshiftrange")
    serialHandler.write("rqi:bowcontrolharmonicshift5")
    serialHandler.write("rqi:bowcontrolfrequency")

    serialHandler.write("rqi:bowharmonicseriescount")
    #serialHandler.write("rqi:bowharmonicseriesdata")
    serialHandler.write("rqi:bowharmonicseries")

    serialHandler.write("rqi:midiconfigurationcount")
    serialHandler.write("rqi:midiconfiguration")
#    serialHandler.write("rqi:midieventhandler")

    serialHandler.write("rqi:bowcontrolharmonicbasenote")
    serialHandler.write("rqi:solenoidmaxforce")
    serialHandler.write("rqi:solenoidminforce")
    serialHandler.write("rqi:solenoidengageduration")

    serialHandler.write("rqi:bowactuator")
    serialHandler.write("rqi:bowactuatorcount")

    serialHandler.write("rqi:mrc")
    serialHandler.write("rqi:acm:0")
    serialHandler.write("rqi:acm:1")
    serialHandler.write("rqi:acm:2")
    serialHandler.write("rqi:acm:3")
    serialHandler.write("rqi:acm:4")
    serialHandler.write("rqi:acm:5")
    serialHandler.write("rqi:acm:6")
    serialHandler.write("rqi:acm:7")

    serialHandler.write("rqi:bpkp")
    serialHandler.write("rqi:bpki")
    serialHandler.write("rqi:bpkd")
    serialHandler.write("rqi:bpie")
    serialHandler.write("rqi:bpme")

def requestHelp():
    commandReference.ui.listWidgetCommands.clear()
    serialHandler.write("help")

def requestBaseData():
    serialHandler.write("rqi:modulecount")

class serialHandler(QThread):
    dataAvaliable = Signal(object, str)
    disconnectSignal = Signal()
    chartDataSignal = Signal(str, float, timedChart.seriesType) # float, float)
    chartCommandSignal = Signal(commandparser.CommandItem)

#    def __init__(self):
#        #QThread.__init__(self)
#        pass

    def run(self) -> None:
        while self.isRunning:
            processed = False
            global serialStream
            try:
                if serialStream is not None:                   
                    if serialStream.inWaiting() != 0:
                        receivedText = serialStream.readline().decode('ascii').strip()
                        #print("Received '" + receivedText + "'")
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
        if str == "rqi:mev":
            pass
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

        print(icondir)

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
        #self.drawTabBar()

        self.ui.closeEvent = self.closeEvent
        #app.aboutToQuit.connect(self.closeEvent)

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

#        self.midiHandlerC = midihandler.MidiHandler(self.midiDataAvaliableSignal) #self.addToDebugWindow)
#        self.midiHandlerC.updateMIDIInDevices(self.ui.comboBoxMIDILearnDevice)
#        self.midiDataAvaliableSignal.connect(self.midiDataAvaliable)

        self.updatingFromModule = False

        self.timeStamper = self.debugTimedChart.timeStamper #timedChart.timeStamp()
        self.modalEvent = ""

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

        find = ""
        for a in commandList.commands:
            for b in range(0, comboBox.count()):
                if comboBox.itemData(b)[1] == a.command:
                    comboBox.setCurrentIndex(b)
                    break

        if find != "Nothing":
            try:
                offset, multiplier = equationParsingHelpers.getVariable(a.argument[0], variable)
                multiplier = multiplier * inMultiplier
                ratio.setValue(multiplier)
            except:
                pass

        comboBox.blockSignals(False)
        ratio.blockSignals(False)

    MIDIVariableSenders = [["Nothing", "", 0, 0], ["Harmonic shift", "bchsh", -32767, 1], ["Pressure (modifier)", "bpm", 0, 1],
                           ["Pressure (baseline)", "bpb", 0, 1], ["Mute position", "msp", 0, 1],
                           ["Solenoid force multiplier", "sfm", 0, "1 / 65535"]]

    #    MIDIBinarySenders = [["MIDI & Mute sustain", ""]]
    def populateComboBoxSendByte(self, comboBox):
        comboBox.clear()
        for sendData in self.MIDIVariableSenders:
            comboBox.addItem(sendData[0], sendData)
        pass

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

        if itemData[1] == "":
            command = "mev:" + widget.midiEvent + ":''"
        else:
            command = ("mev:" + widget.midiEvent + ":'" + "m:" + str(currentShowingModule) + "," + itemData[1] + ":(" + variableName + " * " +
                       str(value) + " * " + str(itemData[3]) + ")'")
        print(command)
        serialHandler.write(command)
        self.updateUIData()

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
        pass

    MIDIBinarySenders = [["Bow hold & Mute inhibit", ["bowpressurehold", "mutesustain"]], ["Bow hold", ["bowpressurehold"]],
                         ["Mute inhibit", ["mutesusain"]]]

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
        widget = self.sender()
        cmd = ""
 #       match widget.midiEvent:
#            case "Sustain":
        itemData = self.ui.midiSustainSend.itemData(self.ui.midiSustainSend.currentIndex())
        booltype = "bool"
        if self.ui.midiSustainInvert.isChecked():
            booltype = "ibool"
        if itemData[1] == "":
            command = "mev:cc:64:''"
        else:
            command = "mev:cc:64:'" + "m:" + str(currentShowingModule)
            for a in itemData[1]:
                command += "," + a + ":" + booltype + "(value)"
        command += "'"
        print(command)
        serialHandler.write(command)
        self.updateUIData()

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
            processed = processInformationReturn(inSerialHandler, receivedText[5:])
        elif (receivedText[:5] == "[hlp]"):
            processed = processHelpReturn(receivedText[5:])
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
        requestBaseData()
        requestStringModuleData()

    def connectDisconnect(self):
        if mainWidget.ui.pushButtonConnectDisconnect.text() == "Connect":
            selectedPort = mainWidget.ui.comboBoxSerialPorts.currentText()
            if selectedPort != "":
                print(selectedPort.split(' ')[0])
                try:
                    global serialStream
                    serialStream = serial.Serial(selectedPort.split(' ')[0], 115200)
                    if serialStream is None:
                        print("serialStream is none!")
                        return
                    serialWidget.addToDebugWindow("Connected to " + serialStream.portstr + "\n")
                    mainWidget.ui.pushButtonConnectDisconnect.setText("Disconnect")

                    self.setUIEnabled(True)
                    self.updateUIData()
                    requestHelp()

                    #serialHandler.write("nop")
                    self.showModalWait("nop", "nop", 15000, "Connecting")


                    serialWidget.checkBoxFilterErrorToggled()
                    serialWidget.checkBoxFilterExpressionParserToggled()
                    serialWidget.checkBoxFilterDebugToggled()
                    serialWidget.checkBoxFilterHardwareToggled()
                    serialWidget.checkBoxFilterPriorityToggled()
                    serialWidget.checkBoxFilterUndefinedToggled()
                    serialWidget.checkBoxFilterUSBToggled()
                    serialWidget.checkBoxFilterCommAckToggled()
                    serialHandler.write("debugprint:inforequest:1")

                except (OSError, serial.SerialException):
                    print("Connection issue")
                    pass
        else:
            if serialStream.isOpen:
                serialStream.close()
                serialStream = None
                self.setUIEnabled(False)
            serialWidget.addToDebugWindow("Disconnected\n")
            mainWidget.ui.pushButtonConnectDisconnect.setText("Connect")

    def serialDisconnect(self):
        self.ui.checkBoxContinuousSMData.setChecked(False)
        self.updateTimer.stop()
        self.ui.pushButtonConnectDisconnect.setText("Connect")
        self.setUIEnabled(False)

    def populateSerialPorts(self):
        itemSelected = mainWidget.ui.comboBoxSerialPorts.currentIndex()
        mainWidget.ui.comboBoxSerialPorts.clear()
        serialPorts = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(serialPorts):
                print("{}: {}".format(port, desc))
                mainWidget.ui.comboBoxSerialPorts.addItem(port + " - " + desc)
        mainWidget.ui.comboBoxSerialPorts.setCurrentIndex(itemSelected)

    def updateStringModuleData(self):
        global stringModules
        global currentShowingModule
        self.ui.doubleSpinBoxFundamentalFrequency.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxFundamentalFrequency.command)))

        self.ui.doubleSpinBoxBowMotorPIDKp.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxBowMotorPIDKp.command)))
        self.ui.doubleSpinBoxBowMotorPIDKi.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxBowMotorPIDKi.command)))
        self.ui.doubleSpinBoxBowMotorPIDKd.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxBowMotorPIDKd.command)))
        self.ui.doubleSpinBoxBowMotorPIDie.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxBowMotorPIDie.command)))
        self.ui.doubleSpinBoxBowMotorMaxError.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxBowMotorMaxError.command)))

        self.ui.doubleSpinBoxBowMotorVoltage.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxBowMotorVoltage.command)))
        self.ui.doubleSpinBoxBowMotorTimeout.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxBowMotorTimeout.command)))
        self.ui.doubleSpinBoxMuteFullMutePosition.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxMuteFullMutePosition.command)))
        self.ui.doubleSpinBoxMuteHalfMutePosition.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxMuteHalfMutePosition.command)))
        self.ui.doubleSpinBoxMuteRestPosition.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxMuteRestPosition.command)))
        self.ui.doubleSpinBoxMuteBackoff.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxMuteBackoff.command)))
        self.ui.doubleSpinBoxBowMotorMaxSpeed.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxBowMotorMaxSpeed.command)))
        self.ui.doubleSpinBoxBowMotorMinSpeed.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxBowMotorMinSpeed.command)))
        self.ui.doubleSpinBoxBowMaxPressure.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxBowMaxPressure.command)))
        self.ui.doubleSpinBoxBowMinPressure.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxBowMinPressure.command)))
        self.ui.doubleSpinBoxBowRestPosition.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxBowRestPosition.command)))
        self.ui.doubleSpinBoxSolenoidMaxForce.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxSolenoidMaxForce.command)))
        self.ui.doubleSpinBoxSolenoidMinForce.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxSolenoidMinForce.command)))
        self.ui.doubleSpinBoxSolenoidEngageDuration.setValue(float(stringModules[currentShowingModule].getCommandValue(self.ui.doubleSpinBoxSolenoidEngageDuration.command)))
        self.ui.spinBoxHarmonicShiftRange.setValue(int(stringModules[currentShowingModule].getCommandValue(self.ui.spinBoxHarmonicShiftRange.command)))

        self.ui.progressBar_bch.setValue(int(stringModules[currentShowingModule].getCommandValue("bch")))
        self.ui.progressBar_bchb.setValue(int(stringModules[currentShowingModule].getCommandValue("bchb")))
        self.ui.progressBar_bchbn.setValue(int(stringModules[currentShowingModule].getCommandValue("bchbn")))
        self.ui.progressBar_bchshr.setValue(int(stringModules[currentShowingModule].getCommandValue("bchshr")))
        self.ui.progressBar_bchsh.setValue(int(stringModules[currentShowingModule].getCommandValue("bchsh")))
        self.ui.progressBar_bchs5.setValue(int(stringModules[currentShowingModule].getCommandValue("bchs5")))
        self.ui.progressBar_bcha.setValue(int(stringModules[currentShowingModule].getCommandValue("bcha")))
        self.ui.progressBar_ar1.setValue(self.ui.progressBar_bchb.value() - self.ui.progressBar_bchbn.value())
        self.ui.progressBar_ar2.setValue(self.ui.progressBar_bch.value() + self.ui.progressBar_bcha.value())
        self.ui.progressBar_ar3.setValue(int(stringModules[currentShowingModule].getCommandValue("bcf")))

        self.updateContinuousStringModuleData()

    def updateContinuousStringModuleData(self): 
        #freq = float(stringModules[currentShowingModule].stringFrequency)
        freq = stringModules[currentShowingModule].getCommandValue("psf")
        if not freq is None:
            #self.ui.horizontalSliderStringFrequency.setValue(int(freq))
            if (freq > 0):
                if (self.ui.listWidgetTuningscheme.currentItem() != None):
                    print(self.ui.listWidgetTuningscheme.currentItem().text())
                    if ((self.ui.listWidgetTuningscheme.currentItem().text()) == "Equal temperament"):
                        ret = getBaseNoteFromFrequency(freq, scaleDataEqual)
                    else:
                        ret = getBaseNoteFromFrequency(freq, scaleDataJust)
                else:
                    ret = getBaseNoteFromFrequency(freq, scaleDataJust)

                self.ui.labelAnalyzeNote.setText(ret[3] + str(ret[0]))
                self.ui.labelAnalyzeCents.setText(str(round(ret[2])))
#                self.ui.dialAnalyzeCents.setValue(round(ret[2]))
                self.ui.horizontalSliderStringFrequency.setValue(round(ret[2]))
                self.ui.labelAnalyzeFreq.setText(str(round(freq,1)))
#                self.ui.dialAnalyzeFreq.setValue(round(freq,1))
#                self.ui.labelStringFrequency.setText(ret[3] + str(ret[0]) + ":" + str(round(ret[2])) + " / " + str(round(freq,1)) + "Hz")

        #freq = float(stringModules[currentShowingModule].bowFrequency)
        freq = stringModules[currentShowingModule].getCommandValue("bmf")
        if not freq is None:
            mainWidget.ui.horizontalSliderBowFrequency.setValue(int(freq))
            if (freq > 0):
                #ret = getBaseNoteFromFrequency(freq, scaleDataJust)
                if (self.ui.listWidgetTuningscheme.currentItem() != None):
                    print(self.ui.listWidgetTuningscheme.currentItem().text())
                    if ((self.ui.listWidgetTuningscheme.currentItem().text()) == "Equal temperament"):
                        ret = getBaseNoteFromFrequency(freq, scaleDataEqual)
                    else:
                        ret = getBaseNoteFromFrequency(freq, scaleDataJust)
                else:
                    ret = getBaseNoteFromFrequency(freq, scaleDataJust)

                mainWidget.ui.labelBowFrequency.setText(ret[3] + str(ret[0]) + ":" + str(round(ret[2])) + " / " + str(round(freq,1)) + "Hz")

        #current = float(stringModules[currentShowingModule].bowCurrent)
        current = stringModules[currentShowingModule].getCommandValue("bmc")
        if not current is None:
            mainWidget.ui.horizontalSliderBowCurrent.setValue(int(current * 10))
            mainWidget.ui.labelBowCurrent.setText(str(current) + " A")

        #freq = float(stringModules[currentShowingModule].setFrequency)
        freq = stringModules[currentShowingModule].getCommandValue("bcf")
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

            dial.setValue(int(stringModules[currentShowingModule].getCVValue(cv)) )
            label.setText(str(stringModules[currentShowingModule].getCVValue(cv)) )

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
            serialHandler.write("adcs:" + str(i) + ":1:1:2:10")

    def comboBoxCurrentSelectedModuleIndexChanged(self, index):
        global currentShowingModule
        currentShowingModule = index
        print("Setting currently showing module to " + str(currentShowingModule))

    def assignValueChanged(self, qtObject, command):
        qtObject.command = command
        qtObject.valueChanged.connect(self.basicChangedSignal)

    def basicChangedSignal(self, value):
        if (mainWidget.updatingFromModule):
            return
        sender = self.sender()
        out = "m:" + str(currentShowingModule) + "," + sender.command + ":" + str(value)
        stringModules[currentShowingModule].setCommandValue(sender.command, float(value))
        serialHandler.write(out)

    def assignButtonPressCommandIssue(self, qtObject, command, refresh = False):
        qtObject.command = command
        qtObject.refresh = refresh
        qtObject.pressed.connect(self.buttonPressIssueCommand)

    def buttonPressIssueCommand(self):
        sender = self.sender()
        serialHandler.write(sender.command)
        if sender.refresh:
            self.updateUIData()

    def checkBoxChartToggled(self):
        checkbox = self.sender()
        if (checkbox.isChecked()):
            visible = True
        else:
            visible = False
        #mainWidget.debugTimedChart.setSeriesVisible(checkbox.seriesName, checkbox.seriesType, visible)
        mainWidget.debugTimedChart.setSeriesVisibleCommand(checkbox.seriesCommand, visible)

    def checkBoxChartAssign(self, qtobject, seriesCommand, seriesType):
        qtobject.toggled.connect(mainWidget.checkBoxChartToggled)
        qtobject.seriesCommand = seriesCommand
        qtobject.seriesType = seriesType


#    def pushButtonCalibrateMutePressed(self):
#        serialHandler.write("mutecalibrate")

    def tableViewScaleDataChanged(self, topLeft, bottomRight, role):
        print("edited " + str(topLeft.column()) + ":" + str(topLeft.data()))
#        serialHandler.write("m:" + str(currentSerialModule) + ",bowcontrolharmonicratio:" + str(topLeft.column()) + ":" + str(topLeft.data()))
        serialHandler.write("m:" + str(currentSerialModule) + ",bowharmonicseriesratio:" + str(topLeft.column()) + ":" + str(topLeft.data()))

    def comboBoxHarmonicListCurrentIndexChanged(self, index):
        currentHarmonicListSelected = int(index)
        if (currentHarmonicListSelected != -1):
            send = "bhs:" + str(currentHarmonicListSelected) + ","
        else:
            send = ""
        if not self.updatingFromModule:
#            serialHandler.write(send + "rqi:bhsl,rqi:bhs")
            serialHandler.write(send + "rqi:bhsd:" + str(currentHarmonicListSelected)) # + ",rqi:bhs")
        self.updateHarmonicTable()

    def pushButtonAddHarmonicPressed(self):
        serialHandler.write("bhsr:" + str(len(stringModules[currentSerialModule].harmonicData)) + ":1")
        self.updateUIData()
        pass

    def pushButtonRemoveHarmonicPressed(self):
        selected = int(mainWidget.ui.tableViewScale.currentIndex().column())
        if (selected < 0):
            messageBox("Error", "Incorrect selection");
        serialHandler.write("bhsrr:" + str(selected))
        self.updateUIData()
        pass

    def pushButtonSaveCurrentHarmonicListPressed(self):
        try:
            harmonicList = stringModules[currentSerialModule].getCommandValue("bhs")
            listID = mainWidget.ui.comboBoxHarmonicList.currentText()
            #serialHandler.write("bhss:'" + listID + "':" + str(harmonicList))
            serialHandler.write("bhss:" + str(harmonicList) + ":'" + listID + "'")
        except:
            messageBox("Error", "Error saving list")

    def pushButtonSaveNewHarmonicListPressed(self):
        listID = inputBox("List name", "List name")
        if listID is None:
            return
        if (mainWidget.find_item(mainWidget.ui.comboBoxHarmonicList, listID) != -1):
            messageBox("Error", "Harmonic series already exists!")
            return
        newIndex = mainWidget.ui.comboBoxHarmonicList.count()
#        serialHandler.write("bhss:'" + listID + "':" + str(newIndex))
        serialHandler.write("bhss:" + str(newIndex) + ":'" + listID + "',bhs:" + str(newIndex))
        #mainWidget.ui.comboBoxHarmonicList.setCurrentIndex(newIndex)
        mainWidget.updateUIData()

    def pushButtonAddHarmonicListPressed(self):
        listID = inputBox("List name", "List name")
        if listID is None:
            return
        newIndex = mainWidget.ui.comboBoxHarmonicList.count()
        #serialHandler.write("bhsl:" + str(newIndex) + ":'" + listID + "':1")
        serialHandler.write("bhsd:" + str(newIndex) + ":'" + listID + "':1")
        mainWidget.updateUIData()

    def pushButtonAddHarmonicListFilePressed(self):
        pass

    def pushButtonRemoveHarmonicListPressed(self):
        try:
            harmonicList = stringModules[currentSerialModule].getCommandValue("bhs")
            serialHandler.write("bhsrm:" + str(harmonicList) + ",rqi:bhs")
        except:
            messageBox("Error", "Error saving list")
        mainWidget.updateUIData()

    def updateHarmonicTable(self):
        mainWidget.ui.tableViewScale.setModel(tableTest.CustomTableModel(stringModules[currentSerialModule].harmonicData))
        mainWidget.ui.tableViewScale.model().dataChanged.connect(mainWidget.tableViewScaleDataChanged)


#    def pushButtonSaveToModulePressed(self):
#        serialHandler.write("globalsaveallparameters")
    def pushButtonLoadFromModulePressed(self):
        self.updateUIData()

    def pushButtonSaveToModulePressed(self):
        mainWidget.pushButtonActuatorSavePressed()
        serialHandler.write("globalsaveallparameters")

    eventDescription = [[ "Note On", "Note on message, sent when a key has been depressed. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n note - note number (0-127) \n velocity - key velocity (0-127)" ],
        [ "Note Off", "Note off message, sent when a key has been released. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n note - note number (0-127) \n velocity - key velocity (0-127)" ],
        [ "CC [xx]", "Continous Controller, sent by various control surfaces. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n control - control number (0-127) \n value - controller value (0-127)" ],
        [ "Poly Aftertouch", "Polyphonic Aftertouch, key pressure per key. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n note - note number (0-127) \n pressure - key pressure (0-127)" ],
        [ "Channel Aftertouch", "Channel Aftertouch, key pressure per channel. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n pressure - key pressure (0-127)"],
        [ "Pitchbend", "Pitchbend, frequency change from the current key. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n pitch - bend (-8192 - 8192)"],
        [ "Program change", "Program change message, mostly used to change sound on various devices. \n\nAdded variables: \n channel - MIDI Channel (0-127) \n program - program number (0-127)"]
        ]

    def listWidgetMidiEventscurrentItemChanged(self, current, previous):
        self.ui.plainTextEditEventDescription.clear()
        if current is None:
            return
        match (current.text()):
            case "Note On":
                mainWidget.ui.lineEditMidiEventCommand.setText(str(instrumentMaster.evNoteOn))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[0][1])
            case "Note Off":
                mainWidget.ui.lineEditMidiEventCommand.setText(str(instrumentMaster.evNoteOff))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[1][1])
            case "Poly Aftertouch":
                mainWidget.ui.lineEditMidiEventCommand.setText(str(instrumentMaster.evPolyAftertouch))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[3][1])
            case "Channel Aftertouch":
                mainWidget.ui.lineEditMidiEventCommand.setText(str(instrumentMaster.evChannelAftertouch))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[4][1])
            case "Pitchbend":
                mainWidget.ui.lineEditMidiEventCommand.setText(str(instrumentMaster.evPitchbend))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[5][1])
            case "Program change":
                mainWidget.ui.lineEditMidiEventCommand.setText(str(instrumentMaster.evProgramChange))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[6][1])
            case _:
                if current.text()[:2] == "CC":
                    print("cc")
                    print(current.text()[3:])
#                    mainWidget.ui.lineEditMidiEventCommand.clear()
                    mainWidget.ui.lineEditMidiEventCommand.setText(str(instrumentMaster.getCC(int(current.text()[3:])).command))
                self.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[2][1])

    def setContinuousSMReadings(self, state):
        if state == True:
            self.updateTimer.start(100)
        else:
            self.updateTimer.stop()

    def readSMData(self):
        serialHandler.write("rqi:pickupstringfrequency")
        serialHandler.write("rqi:pickupaudiopeak")
        serialHandler.write("rqi:pickupaudiorms")
        serialHandler.write("rqi:bowmotorfrequency")
        serialHandler.write("rqi:bowmotorcurrent")
        serialHandler.write("rqi:bowcontrolfrequency")
        serialHandler.write("rqi:bowpidpeakerror")
        print("update!")

    def checkBoxContinuousSMDataToggled(self):
        self.setContinuousSMReadings(self.ui.checkBoxContinuousSMData.isChecked())

    midiKeys = ["C-", "C#", "D-", "D#", "E-", "F-", "F#", "G-", "G#", "A-", "A#", "B-"]

    def populateComboBoxBaseNote(self):
        for octave in range(0,3):
            for key in range(0,12):
                self.ui.comboBoxBaseNote.addItem(self.midiKeys[key] + str(octave + 4), (octave + 4) * 12 + key)

    def comboBoxBaseNotePressed(self, index):
        serialHandler.write("bowcontrolharmonicbasenote:" + str(self.ui.comboBoxBaseNote.itemData(index)))

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

        for c in range(1,len(self.harmonicPresets[b])):
#            mainWidget.ui.tableViewScale.model().setDataNR((c - 1), float(self.harmonicPresets[b][c]))
            serialHandler.write("bhsr:" + str(c - 1) + ":" + str(self.harmonicPresets[b][c]))

        self.updateUIData()

    def lineEditMidiEventCommandFinished(self):
        if mainWidget.ui.listWidgetMidiEvents.currentItem() == None:
            return
        commandSelected = mainWidget.ui.listWidgetMidiEvents.currentItem().text()
        commandSequence = mainWidget.ui.lineEditMidiEventCommand.text()

        match (commandSelected):
            case "Note On":
                setStr = "noteon"
                instrumentMaster.evNoteOn = commandSequence
            case "Note Off":
                setStr = "noteoff"
                instrumentMaster.evNoteOff = commandSequence
            case "Poly Aftertouch":
                setStr = "pat"
                instrumentMaster.evPolyAftertouch = commandSequence
            case "Channel Aftertouch":
                setStr = "cat"
                instrumentMaster.evChannelAftertouch = commandSequence
            case "Program change":
                setStr = "pc"
                instrumentMaster.evProgramChange = commandSequence
            case "Pitchbend":
                setStr = "pb"
                instrumentMaster.evPitchbend = commandSequence
            case _:
                if commandSelected[:2] == "CC":
                    setStr = "cc:" + commandSelected[3:]
                    cc = int(commandSelected[3:])
                    item = instrumentMaster.getCC(cc)
                    item.command = commandSequence

                else:
                    print(commandSelected + " not found")
                    return

        serialString = "mev:" + setStr + ":\"" + commandSequence + "\""
        serialHandler.write(serialString)

#    def listWidgetCommandsCurrentItemChanged(self, current, previous):
#        mainWidget.ui.plainTextEditCMVDescription.clear()
#        if current is not None:
#            mainWidget.ui.plainTextEditCMVDescription.insertPlainText(current.data(Qt.UserRole))

    def find_item(self, combo_box, item_text):
        for index in range(combo_box.count()):
            if combo_box.itemText(index) == item_text:
                return index
        return -1

    def remove_item(self, widget, item_text):
        index = widget.findItems(item_text, Qt.MatchFlag.MatchExactly)
        if (len(index) != 0):
            widget.takeItem(widget.row(index[0]))

    def pushButonActuatorSaveNewPressed(self):
        listID = inputBox("New actuator name", "Actuator name")
        if listID is None:
            return
        if (mainWidget.find_item(mainWidget.ui.comboBoxActuatorPreset, listID) != -1):
            messageBox("Error", "Actuator already exists!")
            return
        newIndex = mainWidget.ui.comboBoxActuatorPreset.count()
        #serialHandler.write("baa,bas:" + str(newIndex) + ",bav,bai:'" + listID + "',bac,bas:" + str(newIndex) + ",bal")
        serialHandler.write("bas:" + str(newIndex) + ":'" + listID + "',ba:" + str(newIndex) + ",bac")
        self.updatingFromModule = True
        mainWidget.ui.comboBoxActuatorPreset.setCurrentIndex(newIndex)
        self.updatingFromModule = False

    def pushButtonActuatorSavePressed(self):
        comboIndex = self.find_item(mainWidget.ui.comboBoxActuatorPreset, mainWidget.ui.comboBoxActuatorPreset.currentText())
        if comboIndex == -1:
            return
            #comboIndex = mainWidget.ui.comboBoxActuatorPreset.count()
            #serialHandler.write("baa")
#        serialHandler.write("bas:" + str(comboIndex) + ",bav,bai:'" + mainWidget.ui.comboBoxActuatorPreset.currentText() + "',bac,bas:" + str(comboIndex) + ",bal")
        serialHandler.write("bas:" + str(comboIndex) + ":'" + mainWidget.ui.comboBoxActuatorPreset.currentText() + "',ba:" + str(comboIndex) + ",bac")

    def pushButtonActuatorLoadPressed(self):
        #comboIndex = self.find_item(mainWidget.ui.comboBoxActuatorPreset, mainWidget.ui.comboBoxActuatorPreset.currentText())
        #if comboIndex == -1:
        #    return
        if (self.updatingFromModule):
            return
        comboIndex = mainWidget.ui.comboBoxActuatorPreset.currentIndex()
        #serialHandler.write("bas:" + str(comboIndex) + ",bal,rqi:bppx,rqi:bppe,rqi:bppr")
        serialHandler.write("ba:" + str(comboIndex) + ",rqi:bppx,rqi:bppe,rqi:bppr")

    def pushButtonAcutatorDeletePreset(self):
        comboIndex = self.find_item(mainWidget.ui.comboBoxActuatorPreset, mainWidget.ui.comboBoxActuatorPreset.currentText())
        if comboIndex == -1:
            return
        mainWidget.ui.comboBoxActuatorPreset.removeItem(comboIndex)
        #serialHandler.write("bar:" + str(comboIndex) + ",bal,rqi:bppx,rqi:bppe,rqi:bppr")
        serialHandler.write("bar:" + str(comboIndex))

    def assignButtonTest(self, qtObject, command, valuePointer, commandPost):
        qtObject.command = command
        qtObject.valuePointer = valuePointer
        qtObject.commandPost = commandPost
        qtObject.pressed.connect(self.testSignal)

    def testSignal(self):
        sender = self.sender()
        #out = "m:" + str(currentShowingModule) + "," + sender.command + ":" + str(sender.valuePointer.value()) + "," + sender.commandPost
        out = "m:" + str(currentShowingModule) + "," + sender.commandPost
        serialHandler.write(out)

    def configurationSetName(self):
        defText = mainWidget.ui.comboBoxConfiguration.currentText()
        text, ok = QInputDialog().getText(self, "Configuration name",
                                          "Configuration name:", QLineEdit.Normal, defText)
        conf = mainWidget.ui.comboBoxConfiguration.currentIndex()
        if ok and text and (conf > -1):
            serialHandler.write("midiconfiguration:" + str(conf) + ",midiconfigurationname:" + text)
            mainWidget.ui.comboBoxConfiguration.setItemText(conf, text)

    def configurationAdd(self):
        defText = mainWidget.ui.comboBoxConfiguration.currentText()
        text, ok = QInputDialog().getText(self, "Configuration name","Configuration name:", QLineEdit.Normal, defText)
        if ok and text:
            if (mainWidget.find_item(mainWidget.ui.comboBoxConfiguration, text) != -1):
                messageBox("Error", "Name already exists!")
                return
            serialHandler.write("midiconfigurationadd:" + str(text))
            mainWidget.ui.comboBoxConfiguration.addItem(text)
            serialHandler.write("midiconfiguration:" + str(mainWidget.ui.comboBoxConfiguration.count() - 1))


    def configurationRemove(self):
        config = int(mainWidget.ui.comboBoxConfiguration.currentIndex())
        if (config < 0) or (mainWidget.ui.comboBoxConfiguration.count() == 0):
            return
        serialHandler.write("midiconfigurationremove:" + str(config) + ",rqi:mcfc,rqi:mcf")
        #self.updateStringModuleData()
        pass

    def configurationSet(self):
        if (self.updatingFromModule):
            return
        config = int(mainWidget.ui.comboBoxConfiguration.currentIndex())
        if (config < 0) or (mainWidget.ui.comboBoxConfiguration.count() == 0):
            return
        serialHandler.write("midiconfiguration:" + str(config))
        pass


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
            serialHandler.write("mev:cc:" + str(cc) + ":''")
            self.updateUIData()

    def ccRemove(self):
        if (mainWidget.ui.listWidgetMidiEvents.currentIndex() == -1):
            return
        if (mainWidget.ui.listWidgetMidiEvents.currentItem().text()[0:2] != "CC"):
            return
        text = mainWidget.ui.listWidgetMidiEvents.currentItem().text()
        serialHandler.write("mevcr:" + text[3:len(text)])
        self.updateUIData()

#    def updateCVData(self):
#        #offset, multiplier = equationParsingHelpers.getVariable(instrumentMaster.cmdNoteOn.getCommandAttribute("se", 0), "velocity")
#        cl = stringModules[currentSerialModule].getCVCommandList(0)
#        attr = cl.getCommandAttribute("bch",0)
#        offset, multiplier = equationParsingHelpers.getVariable(attr, "value")
#        pass

    def updateCVData(self):
        for a in range(0, 7):
            cl = commandparser.CommandList(stringModules[currentSerialModule].getCVCommand(a))
            if len(cl.commands) > 0:
                match a:
                    case 0:
                        cmd = cl.getCommandAttribute("bcha", 0)
                        if cmd == "":
                            break
                        try:
#                            offset, multiplier = equationParsingHelpers.getVariable(cmd, "value")
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
                        #if (offsetDiv - noteOffset) > 0.5:
                        #    cvOffset = 1327.716667 - (offset % 1327.716667)
                        #else:
                        #    cvOffset = abs(offset) % 1327.716667

                        #cvOffset = abs(offset % 1327.716667)
                        #if (offset < 0):
                        #    cvOffset = -1327.716667 + cvOffset

                        self.ui.dialCVHarmonicScale.setValue(cvScale)   # * 1000
                        self.ui.widgetCVHarmonicNoteOffset.setValue(cvOffset)
                        self.ui.widgetCVHarmonicZero.setValue(cvZero)
                    case 1:
                        cmd = cl.getCommandAttribute("bchs5", 0)
                        if cmd == "":
                            break
                        try:
#                            cmd = equationParsingHelpers.removeFunction(cmd, "deadband")
#                            offset, divisor = equationParsingHelpers.extractValueOffsetAndDivisor(cmd)
                            result = equationParsingHelpers.extractZeroCoefficientOffset(cmd)
                        except:
                            messageBox("Error", "Error in equation parser with string " + cmd)
                            break
                        #cvScale = 2.425 / divisor
                        cvScale = 2.425 / (1 / result["coefficient"])
                        #cvZero = (32767 - offset)
                        cvZero = (32767) + result["zeroPosition"]
                        self.ui.dialCVHarmonicShiftScale.setValue(cvScale)  # * 1000
                        self.ui.dialCVHarmonicShiftZero.setValue(cvZero)
                    case 2:
                        cmd = cl.getCommandAttribute("bchsh", 0)
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
                        cmd = cl.getCommandAttribute("bmr",0)
                        if cmd == "1":
                            mainWidget.ui.checkBoxCVGatePowerMotor.setCheckState(Qt.CheckState.Checked)
                        else:
                            mainWidget.ui.checkBoxCVGatePowerMotor.setCheckState(Qt.CheckState.Unchecked)

                        threshold = 2000

                        cmd = cl.getCommandAttribute("bph", 0)
                        if cmd != "":
                            mainWidget.ui.checkBoxCVGateHold.setCheckState(Qt.CheckState.Checked)
                            threshold = abs(int(equationParsingHelpers.stripBoolIBool(cmd)))
                        else:
                            mainWidget.ui.checkBoxCVGateHold.setCheckState(Qt.CheckState.Unchecked)

                        cmd = cl.getCommandAttribute("bpe", 0)
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
        #if widget is None:
        if not isinstance(widget, QWidget):
            widget = self.sender()
        cl = commandparser.CommandList(stringModules[currentSerialModule].getCVCommand(int(widget.CVcontrol)))
        match widget.CVcontrol:
            case 0:
                cmd = cl.buildCommandString({"bcha"})
                cvScale = str(1327.716667 / (self.ui.dialCVHarmonicScale.value()))  #  / 1000
                cvOffset = str(self.ui.widgetCVHarmonicNoteOffset.value()) # + self.ui.dialCVHarmonicNoteOffset.value() * 1327.716667)
                cvZero = self.ui.widgetCVHarmonicZero.value()
                cmd += "bcha:(value"
                if int(cvZero) >= 0:
                    cmd += "+"
                cmd += str(cvZero) + ")/" + str(cvScale) + "+(" + str(cvOffset) + ")"
            case 1:
                cmd = cl.buildCommandString({"bchs5"})
                cvScale = str(2.425 / (self.ui.dialCVHarmonicShiftScale.value()))    #  / 1000
                cvOffset = -(32767 - self.ui.dialCVHarmonicShiftZero.value())
                cmd += "bchs5:\"deadband(value" + str(cvOffset) + ", 30)/" + str(cvScale) + "\""
            case 2:
                cmd = cl.buildCommandString({"bchsh"})
                cmd += "bchsh:\"deadband(value-" + str(32767 - self.ui.dialCVFineTuneCenter.value()) + ", 400)*0.49064\""
            case 5:
                # 5 - bmr:1,bpid:1,bcsm:0,bpe:bool(value-1000),bpr:ibool(value-1000),bph:ibool(value-1000)
                cmd = cl.buildCommandString({"bmr","bpid","bcsm","bpe","bpr","bph"})
                if cmd != "":
                    cmd += ","
                if mainWidget.ui.checkBoxCVGatePowerMotor.isChecked():
                    cmd += "bmr:1,bpid:1,bcsm:0,"
                if mainWidget.ui.checkBoxCVGateEngage.isChecked():
                    cmd += ("bpe:bool(value-" + str(mainWidget.ui.widgetCVGateThreshold.value()) + "),bpr:ibool(value-" +
                            str(mainWidget.ui.widgetCVGateThreshold.value()) + "),")
                if mainWidget.ui.checkBoxCVGateHold.isChecked():
                    cmd += "bph:ibool(value-" + str(mainWidget.ui.widgetCVGateThreshold.value()) + ")"
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
        cmd = "acm:" + str(widget.CVcontrol) + ":'" + cmd + "'"
        print(cmd)
        serialHandler.write(cmd)
        #self.updatingFromModule = True
        #self.updateCVData()
        #self.updatingFromModule = False
        pass
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

        pass

    def widgetCVTextCallback(self):
        widget = self.sender()
        cmd = widget.text()
        cmd = "acm:" + str (widget.CVcontrol) + ":'" + cmd + "'"
        serialHandler.write(cmd)
        pass
    def connectCVTextWidgets(self, CVcontrol, widget):
        widget.CVcontrol = CVcontrol
        widget.returnPressed.connect(self.widgetCVTextCallback)

    def cmdNoteOnUpdate(self, widget = None):
        if self.updatingFromModule:
            return

        #cl = CommandList(self.ui.midiNoteOnOther.text())
        cl = CommandList(instrumentMaster.evNoteOn)
        cmd = cl.buildCommandString({"se", "mr"})

        if self.ui.midiNoteOnVelToHammer.value() > 0:
            cmd += ",se:(velocity*" + str(self.ui.midiNoteOnVelToHammer.value()) + ")"
            if self.ui.midiNoteOnHammerStaccato.checkState() == Qt.CheckState.Checked:
                cmd += "*(1-notecount)"
        if self.ui.midiNoteOnSendMuteRest.checkState() == Qt.CheckState.Checked:
            cmd += ",mr:1"
        serialString = "mev:noteon:\"" + cmd + "\""
        serialHandler.write(serialString)
        self.updateUIData()

    def cmdNoteOffUpdate(self):
        if self.updatingFromModule:
            return
        #cl = CommandList(self.ui.midiNoteOffOther.text())
        cl = CommandList(instrumentMaster.evNoteOff)
        cmd = cl.buildCommandString({"mfm", "bmr"})

        if self.ui.midiNoteOffSendFullMute.checkState() == Qt.CheckState.Checked:
            cmd += ",mfm:1"
        if self.ui.midiNoteOffMotorOff.checkState() == Qt.CheckState.Checked:
            cmd += ",bmr:0"
        serialString = "mev:noteoff:\"" + cmd + "\""
        serialHandler.write(serialString)
        self.updateUIData()

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
        serialHandler.write("mrc:" + str(ch))

    def populateFundamentalComboBox(self):
        mainWidget.ui.comboBoxFundamentalFrequency.clear()

        try:
            if ((self.ui.listWidgetTuningscheme.currentItem().text()) == "Equal temperament"):
                noteDataArray = scaleDataEqual
            else:
                noteDataArray = scaleDataJust
        except:
            noteDataArray = scaleDataJust

        base = 110 / 4
        for octave in range(0, 3):
            for note in range (0, 11):
                mainWidget.ui.comboBoxFundamentalFrequency.addItem(noteDataArray[2][note] + " " + str(round((pow(2, octave)*base) * noteDataArray[1][note], 2)))

    def comboBoxFundamentalFrequencyIndexChanged(self):
        text = mainWidget.ui.comboBoxFundamentalFrequency.currentText()
        if text == "":
            return
        mainWidget.ui.doubleSpinBoxFundamentalFrequency.setValue(float(mainWidget.ui.comboBoxFundamentalFrequency.currentText()[3:len(text)]))

    def mouseReleaseEventIntermediate(self, event, widget):
        widget.mouseReleaseFunction(widget)
        #if widget is QSlider:
        if type(widget) == QSlider:
            QSlider.mouseReleaseEvent(widget, event)
        #super(MainWidget, self).mouseReleaseEvent(event)

    def assignMouseReleaseEvent(self, qtObject, function):
        qtObject.mouseReleaseEvent = lambda event: self.mouseReleaseEventIntermediate(event, qtObject)
        qtObject.mouseReleaseFunction = function

    def showModalWait(self, issueCommand, resultCommand, progressTime, title, timeOut = False):
        serialHandler.write(issueCommand)
        self.modalEvent = resultCommand
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        self.modalDialog = waitdialog.ProgressDialog(progressTime, title) # Just sent to highest, was 16000
        #self.modalDialog = dialog
        self.modalDialog.start(timeOut)

        self.modalEvent = ""
        self.modalDialog = None

    def dialogSignaler(self):
        widget = self.sender()
        self.showModalWait(widget.issueCommand, widget.resultCommand, 20000, "Calibrating")
#        serialHandler.write(widget.issueCommand)
#        self.modalEvent = widget.resultCommand
#        app = QApplication.instance()
#        if app is None:
#            app = QApplication(sys.argv)

#        self.modalDialog = waitdialog.ProgressDialog(20000) # Just sent to highest, was 16000
#        self.modalDialog.start()
#
#        self.modalEvent = ""
#        self.modalDialog = None

    def connectSignalToModalDialog(self, widget, issueCommand, resultCommand):
        widget.issueCommand = issueCommand
        widget.resultCommand = resultCommand
        if isinstance(widget, QPushButton):
            widget.pressed.connect(self.dialogSignaler)

    def pickupAnalyse(self):
        saveState = mainWidget.ui.checkBoxContinuousSMData.checkState()
        mainWidget.ui.checkBoxContinuousSMData.setChecked(True)
        serialHandler.write("sfm:1,se:65535")
        mainWidget.showModalWait("", "", 2500, "Analysing", True)
        mainWidget.ui.checkBoxContinuousSMData.setCheckState(saveState)
        pass

    def resetAllSettings(self):
        msgBox = QMessageBox.warning(self, "WHOOPS COMPLETE RESET",
                                     "This will reset ALL SETTINGS in your Ekdahl FAR and then restart the instrument, you sure?",
                                     buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     defaultButton=QMessageBox.StandardButton.No)
        if msgBox == QMessageBox.StandardButton.Yes:
            serialHandler.write("grap,reset:1")
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
        serialHandler.write("rqi:adcr:2")
        QTimer.singleShot(1000, self.CVFinetuneCalibrateContinue)

    def CVFinetuneCalibrateContinue(self):
        self.firstCv = stringModules[currentSerialModule].getCVValue(2)
        messageBox("CV fine tuning center calibration",
                   "Now turn the 'Harmonic shift'-knob all the way to the right, then turn it to the center.\nPress OK when you are done")
        serialHandler.write("rqi:adcr:2")
        QTimer.singleShot(1000, self.CVFinetuneCalibrateFinish)

    def CVFinetuneCalibrateFinish(self):
        offset = (stringModules[currentSerialModule].getCVValue(2) - self.firstCv) / 2
        mainWidget.ui.dialCVFineTuneCenter.setValue(offset)
        serialHandler.write("bchsh:0")
        pass

    def CVHarmonicShiftZeroCalibrate(self):
        messageBox("Harmonic shift zero calibation", "Turn the 'Harmonic shift modulation'-knob all the way to the right, then turn it all the way to the left.\nPress OK when you are done")
        serialHandler.write("rqi:adcr:1")
        QTimer.singleShot(1000, self.CVHarmonicShiftZeroCalibrateContinue)

    def CVHarmonicShiftZeroCalibrateContinue(self):
        cv = stringModules[currentSerialModule].getCVValue(1)
        mainWidget.ui.dialCVHarmonicShiftZero.setValue(32767 - cv)
        serialHandler.write("bchs5:0")


#harmonicSeriesList = [,
#    [1, 1.059463094, 1.122462048, 1.189207115, 1.25992105, 1.334839854, 1.414213562, 1.498307077, 1.587401052, 1.681792831, 1.781797436, 1.887748625]]
#currentHarmonicSeries = 0

import math

# Base note at octave 5
scaleDataJust = [440, [1, 1.06667, 1.125, 1.2, 1.25, 1.3333, 1.40625, 1.5, 1.6, 1.66667, 1.8, 1.875],
                 ["A-", "A#", "B-", "C-", "C#", "D-", "D#", "E-", "F-", "F#", "G-", "G#"]]
scaleDataEqual = [440, [1, 1.059463094, 1.122462048, 1.189207115, 1.259921050, 1.334839854, 1.414213562, 1.498307077, 1.587401052, 1.681792831, 1.781797436, 1.887748625],
                  ["A-", "A#", "B-", "C-", "C#", "D-", "D#", "E-", "F-", "F#", "G-", "G#"]]

def getBaseNoteFromFrequency(frequency, noteDataArray):
    oct0f = noteDataArray[0] / 32
#    print ("frequency " + str(frequency))
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
#    print("note first try " + str(note))
#    print("cents first try " + str(cents))
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
#    sys.excepthook = except_hook

    app = QApplication(sys.argv)

    mainWidget = FarConfig()

    serialWidget = SerialWidget(serialHandler, mainWidget.timeStamper, logging)

    commandReference = CommandReference()

    mainWidget.show()

#    mainWidget.ui.listWidgetCommands.setSortingEnabled(True)
    #mainWidget.ui.comboBoxFundamentalFrequency
## Hiding old
    #mainWidget.ui.horizontalSliderStringFrequency.setVisible(False)
#    mainWidget.ui.labelStringFrequency.setVisible(False)
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
    #mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonSaveToModule, "globalsaveallparameters")
    mainWidget.ui.pushButtonLoadFromModule.pressed.connect(mainWidget.pushButtonLoadFromModulePressed)
#    mainWidget.ui.pushButtonReadSMData.pressed.connect(mainWidget.readSMData)
    mainWidget.ui.checkBoxContinuousSMData.toggled.connect(mainWidget.checkBoxContinuousSMDataToggled)
    mainWidget.ui.pushButtonShowConsole.pressed.connect(showConsole)
    mainWidget.ui.pushButtonShowReference.pressed.connect(showReference)

## Debug console
#    serialWidget.assignFeedbackReportItem(serialWidget.ui.checkBoxFilterCommAck, "command")
#    serialWidget.assignFeedbackReportItem(serialWidget.ui.checkBoxFilterDebug, "debug")
#    serialWidget.assignFeedbackReportItem(serialWidget.ui.checkBoxFilterError, "error")
#    serialWidget.assignFeedbackReportItem(serialWidget.ui.checkBoxFilterExpressionParser, "expressionparser")
#    serialWidget.assignFeedbackReportItem(serialWidget.ui.checkBoxFilterHardware, "hardware")
#    serialWidget.assignFeedbackReportItem(serialWidget.ui.checkBoxFilterInfoRequest, "inforequest")
#    serialWidget.assignFeedbackReportItem(serialWidget.ui.checkBoxFilterPriority, "priority")
#    serialWidget.assignFeedbackReportItem(serialWidget.ui.checkBoxFilterUSB, "usb")
#    serialWidget.assignFeedbackReportItem(serialWidget.ui.checkBoxFilterUndefined, "undefined")
#    serialWidget.assignFeedbackReportItem(serialWidget.ui.checkBoxFilterOutput, "output")

#    serialWidget.ui.checkBoxDebugCursorFollow.toggled.connect(serialWidget.checkBoxDebugCursorFollowToggled)
#    serialWidget.ui.pushButtonClear.pressed.connect(serialWidget.debugClear)
#    serialWidget.ui.checkBoxLimitLines.stateChanged.connect(serialWidget.checkBoxLimitLinesStateChanged)
#    serialWidget.ui.spinBoxLimitLines.valueChanged.connect(serialWidget.spinBoxLimitLinesValueChanged)

## Tab Module settings
    mainWidget.ui.pushButtonPickupAnalyse.pressed.connect(mainWidget.pickupAnalyse)

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxFundamentalFrequency, "bcu")
    mainWidget.ui.comboBoxBaseNote.currentIndexChanged.connect(mainWidget.comboBoxBaseNotePressed)
    mainWidget.ui.comboBoxFundamentalFrequency.currentIndexChanged.connect(mainWidget.comboBoxFundamentalFrequencyIndexChanged)
    mainWidget.ui.listWidgetTuningscheme.currentItemChanged.connect(mainWidget.tuningSchemeChanged)


    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonCalibrateAll, "bowcalibrateall", True)

    mainWidget.ui.comboBoxHarmonicList.currentIndexChanged.connect(mainWidget.comboBoxHarmonicListCurrentIndexChanged)
    mainWidget.ui.pushButtonAddHarmonic.pressed.connect(mainWidget.pushButtonAddHarmonicPressed)
    mainWidget.ui.pushButtonRemoveHarmonic.pressed.connect(mainWidget.pushButtonRemoveHarmonicPressed)
    mainWidget.ui.pushButtonLoadHarmonicPreset.pressed.connect(mainWidget.pushButtonLoadHarmonicPresetPressed)
    mainWidget.ui.pushButtonSaveCurrentHarmonicList.pressed.connect(mainWidget.pushButtonSaveCurrentHarmonicListPressed)
    mainWidget.ui.pushButtonSaveNewHarmonicList.pressed.connect(mainWidget.pushButtonSaveNewHarmonicListPressed)
    mainWidget.ui.pushButtonAddHarmonicList.pressed.connect(mainWidget.pushButtonAddHarmonicListPressed)
    mainWidget.ui.pushButtonAddHarmonicListFile.pressed.connect(mainWidget.pushButtonAddHarmonicListFilePressed)
    mainWidget.ui.pushButtonRemoveHarmonicList.pressed.connect(mainWidget.pushButtonRemoveHarmonicListPressed)

## Tab Midi settings
    mainWidget.ui.comboBoxMidiChannel.currentIndexChanged.connect(mainWidget.comboBoxMidiChannelIndexChanged)

    mainWidget.ui.comboBoxConfiguration.currentIndexChanged.connect(mainWidget.configurationSet)
    #mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonConfigurationAdd, "mcfa", True)
    mainWidget.ui.pushButtonConfigurationAdd.pressed.connect(mainWidget.configurationAdd)
    mainWidget.ui.pushButtonConfigurationRemove.pressed.connect(mainWidget.configurationRemove)
    mainWidget.ui.pushButtonConfigurationName.pressed.connect(mainWidget.configurationSetName)

    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonMidiRestoreDefaults, "mcfd", True)

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

    #mainWidget.ui.pushButtonConfigurationName.pressed.connect(mainWidget.configurationSetName)
    mainWidget.ui.listWidgetMidiEvents.currentItemChanged.connect(mainWidget.listWidgetMidiEventscurrentItemChanged)
    mainWidget.ui.lineEditMidiEventCommand.editingFinished.connect(mainWidget.lineEditMidiEventCommandFinished)
#    mainWidget.ui.listWidgetCommands.currentItemChanged.connect(mainWidget.listWidgetCommandsCurrentItemChanged)
#    mainWidget.ui.comboBoxMIDILearnDevice.currentIndexChanged.connect(mainWidget.selectMIDIDevice)
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

    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonResetADCSettings, "acd", True)
## Tab Adanced

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorMaxSpeed, "bmsx")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorMinSpeed, "bmsi")

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorPIDKp, "bpkp")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorPIDKi, "bpki")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorPIDKd, "bpkd")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorPIDie, "bpie")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorMaxError, "bpme")

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorVoltage, "bmv")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorTimeout, "bmt")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonCalibrateMotorSpeed, "bowcalibratespeed")

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMaxPressure, "bppx")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMinPressure, "bppe")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowRestPosition, "bppr")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonRestBow, "bppr:0,bpr:1")
    mainWidget.connectSignalToModalDialog(mainWidget.ui.pushButtonCalibratePressure, "bcp", "bcp")

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxMuteFullMutePosition, "mfmp")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxMuteHalfMutePosition, "mhmp")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxMuteRestPosition, "mrp")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxMuteBackoff, "mbo")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonRestMute, "mrp:0,mr:1")
    mainWidget.connectSignalToModalDialog(mainWidget.ui.pushButtonCalibrateMute, "mca", "mca")

    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonMuteFullTest, "mutefullmute:1")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonMuteHalfTest, "mutehalfmute:1")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonMuteRestTest, "muterest:1")

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxSolenoidMaxForce, "sxf")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxSolenoidMinForce, "sif")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxSolenoidEngageDuration, "sed")

    mainWidget.ui.pushButtonActuatorSave.pressed.connect(mainWidget.pushButtonActuatorSavePressed)
    mainWidget.ui.comboBoxActuatorPreset.currentIndexChanged.connect(mainWidget.pushButtonActuatorLoadPressed)
    mainWidget.ui.pushButonActuatorSaveNew.pressed.connect(mainWidget.pushButonActuatorSaveNewPressed)
   # mainWidget.ui.pushButtonActuatorLoad.pressed.connect(mainWidget.pushButtonActuatorLoadPressed)
    mainWidget.ui.pushButtonActuatorDelete.pressed.connect(mainWidget.pushButtonAcutatorDeletePreset)

    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonBowMaxPressureTest, "bowpressuremodifier:0,bowpressurebaseline:65535")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonBowEngagePressureTest, "bowpressuremodifier:0,bowpressurebaseline:0,bowpressureengage:1")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonBowRestPressureTest, "bowpressuremodifier:0,bowpressurebaseline:0,bowpressurerest:1")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonSolenoidMaxForceTest, "solenoidforcemultiplier:1,se:65535")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonSolenoidMinForceTest, "solenoidforcemultiplier:1,se:1")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonEngageHammer, "se:65535")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonHammerDurationTest, "sfm:1,se:65535")

    mainWidget.assignValueChanged(mainWidget.ui.spinBoxHarmonicShiftRange, "bchsr")
    mainWidget.ui.comboBoxCurrentlySelectedModule.currentIndexChanged.connect(mainWidget.comboBoxCurrentSelectedModuleIndexChanged)
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonHomeBow, "bowhome", True)
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonHomeMute, "mutehome", True)
    mainWidget.ui.pushButtonResetAllSettings.pressed.connect(mainWidget.resetAllSettings)

## Tab Debugging
#    mainWidget.msgSc = QShortcut(QKeySequence('Ctrl+M'), mainWidget.ui.tableViewScale)
#    mainWidget.msgSc.activated.connect(lambda: QMessageBox.information(mainWidget.ui.tableViewScale,'Message', 'Ctrl + M initiated'))
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

    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA0, "adcr0", timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA1, "adcr1", timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA2, "adcr2", timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA3, "adcr3", timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA4, "adcr4", timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA5, "adcr5", timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA6, "adcr6", timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartA7, "adcr7", timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartAudPk, "pap", timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartAudRMS, "par", timedChart.seriesType.integer)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartAudFFT, "psf", timedChart.seriesType.frequency)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartMotFreq, "bmf", timedChart.seriesType.frequency)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartReadFreq, "bcf", timedChart.seriesType.frequency)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartPeakErr, "bpperr", timedChart.seriesType.frequency)
    mainWidget.checkBoxChartAssign(mainWidget.ui.checkBoxChartMotCurr, "bmc", timedChart.seriesType.integer)

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
    stringModules.append(strm)

# pre-start inits
    load_settings()
    mainWidget.destroyed.connect(mainWidget.closeEvent)
    mainWidget.populateFundamentalComboBox()
    #mainWidget.populateSerialPorts()
    mainWidget.USBRefreshTimer = QTimer()
    mainWidget.USBRefreshTimer.timeout.connect(mainWidget.populateSerialPorts)
    mainWidget.USBRefreshTimer.start(1000)

    serialWidget.addToDebugWindow("Initialized\n")
#    app.lastWindowClosed.connect(app.quit)
    sys.exit(app.exec())
    mainWidget.thread1.terminate()
