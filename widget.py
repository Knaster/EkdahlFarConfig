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

# This Python file uses the following encoding: utf-8
import sys

import serial.tools.list_ports

from PySide6.QtWidgets import QApplication, QWidget, QDoubleSpinBox, QListWidgetItem, QInputDialog, QMessageBox, QLineEdit
from PySide6.QtCore import QThread, Signal, QTimer, QModelIndex, Qt, QObject, QDir, Slot
from PySide6.QtGui import QTextBlock, QTextCursor, QTextBlockFormat, QColor

import re
import equationParsingHelpers

import logging
from logging.handlers import RotatingFileHandler
#logging.basicConfig(filename="farconfig.log", filemode="a", format='%(asctime)s - %(message)s',level=logging.DEBUG)
log_formatter = logging.Formatter('%(asctime)s - %(message)s')
log_file = "farconfig.log"
log_handler = RotatingFileHandler(log_file, mode='w', maxBytes=1024*1024, backupCount=1, encoding=None, delay=0)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.DEBUG)
log_app = logging.getLogger('root')
log_app.setLevel(logging.DEBUG)
log_app.addHandler(log_handler)

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

#def except_hook(cls, exception, traceback):
#    sys.__excepthook__(cls, exception, traceback)

from time import process_time

import mido

import tableTest
from commandparser import CommandItem, CommandList

import timedChart

import midihandler

from stringModule import stringModule, CC, InstrumentMaster

serialPorts = serial.tools.list_ports.comports()
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

def addModulesIfNeeded(needed):
    global stringModules
    print("has " + str(len(stringModules)) + " modules, looking for module " + str(needed))
    while len(stringModules) <= needed:
        print("Adding a module")
        stringModules.append(stringModule())
    while (mainWidget.ui.comboBoxCurrentlySelectedModule.count() <= needed):
        mainWidget.ui.comboBoxCurrentlySelectedModule.addItem(str(mainWidget.ui.comboBoxCurrentlySelectedModule.count() + 1))

def processInformationForChart(inSerialHandler, command):
    match command.command:
        case "adcr":
            inSerialHandler.chartDataSignal.emit("Adc#" + str(command.argument[0]), float(command.argument[1]), timedChart.seriesType.integer) #0, 65535)
        case "bcf":
            inSerialHandler.chartDataSignal.emit("Targ.Freq", float(command.argument[0]), timedChart.seriesType.frequency) # 0, 65535)
        case "bmf":
            inSerialHandler.chartDataSignal.emit("Mot.Freq", float(command.argument[0]), timedChart.seriesType.frequency) #0, 65535)
        case "psf":
            if (float(command.argument[0]) > 0):
                inSerialHandler.chartDataSignal.emit("FFT Freq", float(command.argument[0]), timedChart.seriesType.frequency) #0, 65535)
        case "pap":
            inSerialHandler.chartDataSignal.emit("Aud.peak", float(command.argument[0])*65535, timedChart.seriesType.integer)  # 0, 65535)
        case "par":
            inSerialHandler.chartDataSignal.emit("Aud.RMS", float(command.argument[0])*65535, timedChart.seriesType.integer)  # 0, 65535)
        case "bpperr":
            inSerialHandler.chartDataSignal.emit("PIDPeakErr", float(command.argument[0]), timedChart.seriesType.frequency) #0, 65535)
        case _:
            return False
    return True

def processInformationReturn(inSerialHandler, infoReturn):
    print("processInformationReturn")
    commandList = CommandList()
    commandList.addCommands(infoReturn)

    global stringModules
    global currentSerialModule
    global currentBow
#    global updatingFromModule
    mainWidget.updatingFromModule = True

    processed = True

    for i in commandList.commands:
        #processed = processInformationForChart(inSerialHandler, i)
        processInformationForChart(inSerialHandler, i)

        try:
            match i.command:
                case "m":
                    currentSerialModule = int(i.argument[0])
                    addModulesIfNeeded(currentSerialModule)
                    print ("setting current serial module to " + i.argument[0])
                case "b":
                    currentBow = i.argument[0]
                    print ("setting current serial bow to " + i.argument[0])
                case "mc":
                    global moduleCount
                    moduleCount = int(i.argument[0])
                    addModulesIfNeeded(moduleCount - 1)
                    print ("setting module count to " + i.argument[0])
                case "bcu":
                    stringModules[currentSerialModule].setFundamentalFrequency(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting fundamental frequency to " + str(stringModules[currentSerialModule].getFundamentalFrequency()))
                case "bmv":
                    stringModules[currentSerialModule].setMotorVoltage(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting bow motor voltage to " + str(stringModules[currentSerialModule].getMotorVoltage()))
                case "bpkp":
                    stringModules[currentSerialModule].setPIDKp(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting bow PID Kp to " + str(stringModules[currentSerialModule].getPIDKp()))
                case "bpki":
                    stringModules[currentSerialModule].setPIDKi(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting bow PID Ki to " + str(stringModules[currentSerialModule].getPIDKi()))
                case "bpkd":
                    stringModules[currentSerialModule].setPIDKd(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting bow PID Kd to " + str(stringModules[currentSerialModule].getPIDKd()))
                case "bpie":
                    stringModules[currentSerialModule].setIntegratorError(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting bow PID integrator error to " + str(stringModules[currentSerialModule].getIntegratorError()))
                case "bmt":
                    stringModules[currentSerialModule].setBowTimeOut(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting bow timeout to " + str(stringModules[currentSerialModule].getBowTimeOut()))
                case "mfmp":
                    stringModules[currentSerialModule].setMuteFullMutePosition(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting mute full mute position to " + str(stringModules[currentSerialModule].getMuteFullMutePosition()))
                case "mhmp":
                    stringModules[currentSerialModule].setMuteHalfMutePosition(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting mute half mute position to " + str(stringModules[currentSerialModule].getMuteHalfMutePosition()))
                case "mrp":
                    stringModules[currentSerialModule].setMuteRestPosition(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting mute rest position to " + str(stringModules[currentSerialModule].getMuteRestPosition()))
                case "mbo":
                    stringModules[currentSerialModule].setMuteBackoff(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting mute backoff to " + str(stringModules[currentSerialModule].getMuteBackoff()))
                case "bmsx":
                    stringModules[currentSerialModule].setBowMotorMaxSpeed(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting bow motor max speed to " + str(stringModules[currentSerialModule].getBowMotorMaxSpeed()))
                case "bmsi":
                    stringModules[currentSerialModule].setBowMotorMinSpeed(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting bow motor min speed to " + str(stringModules[currentSerialModule].getBowMotorMinSpeed()))
                case "bppx":
                    stringModules[currentSerialModule].setBowMaxPressure(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting bow max pressure to " + str(stringModules[currentSerialModule].getBowMaxPressure()))
                case "bppe":
                    stringModules[currentSerialModule].setBowMinPressure(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting bow min pressure to " + str(stringModules[currentSerialModule].getBowMinPressure()))
                case "bppr":
                    stringModules[currentSerialModule].setBowRestPosition(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting bow rest position to " + str(stringModules[currentSerialModule].getBowRestPosition()))
                case "bchl":
                    hl = i.argument[0]
                    print(hl)
                    print(len(stringModules[currentSerialModule].harmonicData))
                    if (int(hl) != len(stringModules[currentSerialModule].harmonicData)):
                        print("Error, harmonic list is broken")
                        return
                    hs = []
                    hsi = 1
                    while (hsi < len(i.argument)):
                        print("Adding value " + str(i.argument[hsi]))
                        hs.append(i.argument[hsi])
                        hsi += 1
                    stringModules[currentSerialModule].harmonicData.append(hs)
                    print("Added harmonic list " + str(stringModules[currentSerialModule].harmonicData))

                case "bchc":
                    mainWidget.ui.comboBoxHarmonicList.clear()
                    hl = 0
                    while (hl < int(i.argument[0])):
                        mainWidget.ui.comboBoxHarmonicList.addItem(str(hl))
                        hl += 1
                    mainWidget.ui.comboBoxHarmonicList.setCurrentIndex(0)
                case "mev":
                    match i.argument[0]:
                        case "noteon":
                            instrumentMaster.evNoteOn = i.argument[1]
                            mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Note On"))

#                            mainWidget.ui.midiNoteOnVelToHammer.blockSignals(True)
#                            mainWidget.ui.midiNoteOnHammerStaccato.blockSignals(True)
#                            mainWidget.ui.midiNoteOnSendMuteRest.blockSignals(True)
#                            mainWidget.ui.midiNoteOnOther.blockSignals(True)

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

                            mainWidget.ui.midiNoteOnOther.setText(instrumentMaster.evNoteOn)

#                            mainWidget.ui.midiNoteOnVelToHammer.blockSignals(False)
#                            mainWidget.ui.midiNoteOnHammerStaccato.blockSignals(False)
#                            mainWidget.ui.midiNoteOnSendMuteRest.blockSignals(False)
#                            mainWidget.ui.midiNoteOnOther.blockSignals(False)

                            print("Setting NoteOn to " + str(instrumentMaster.evNoteOn))
                        case "noteoff":
                            instrumentMaster.evNoteOff = i.argument[1]
                            mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Note Off"))

#                            mainWidget.ui.midiNoteOffSendFullMute.blockSignals(True)
#                            mainWidget.ui.midiNoteOffMotorOff.blockSignals(True)
#                            mainWidget.ui.midiNoteOffOther.blockSignals(True)

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

                            mainWidget.ui.midiNoteOffOther.setText(instrumentMaster.evNoteOff)

 #                           mainWidget.ui.midiNoteOffSendFullMute.blockSignals(False)
 #                           mainWidget.ui.midiNoteOffMotorOff.blockSignals(False)
 #                           mainWidget.ui.midiNoteOffOther.blockSignals(False)

                            print("Setting NoteOff to " + str(instrumentMaster.evNoteOff))
                        case "cc":
                            instrumentMaster.addCC(int(i.argument[1]), str(i.argument[2]))
                            mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("CC " + str(i.argument[1])))
                            print("Setting CC " + i.argument[1] + " to " + str(i.argument[2]))
                        case "pat":
                            instrumentMaster.evPolyAftertouch = i.argument[1]
                            mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Poly Aftertouch"))

#                            mainWidget.ui.midiPolyATSend.blockSignals(True)
#                            mainWidget.ui.midiPolyATRatio.blockSignals(True)

                            instrumentMaster.cmdPolyAftertouch.clear()
                            instrumentMaster.cmdPolyAftertouch.addCommands(i.argument[1])

                            selectSendDestinationAndRatio(mainWidget.ui.midiPolyATSend, instrumentMaster.cmdPolyAftertouch, mainWidget.ui.midiPolyATRatio, "pressure")

#                            mainWidget.ui.midiPolyATSend.blockSignals(False)
#                            mainWidget.ui.midiPolyATRatio.blockSignals(False)

                            print("Setting polyphonic aftertouch to " + str(instrumentMaster.evPolyAftertouch))
                        case "pb":
                            instrumentMaster.evPitchbend = i.argument[1]
                            mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Pitchbend"))

                            mainWidget.ui.midiPitchbendSend.blockSignals(True)
                            mainWidget.ui.midiPitchbendRatio.blockSignals(True)

                            instrumentMaster.cmdPitchbend.clear()
                            instrumentMaster.cmdPitchbend.addCommands(i.argument[1])

                            selectSendDestinationAndRatio(mainWidget.ui.midiPitchbendSend, instrumentMaster.cmdPitchbend,
                                                          mainWidget.ui.midiPitchbendRatio, "pitch")

                            mainWidget.ui.midiPitchbendSend.blockSignals(False)
                            mainWidget.ui.midiPitchbendRatio.blockSignals(False)

                            print("Setting polyphonic aftertouch to " + str(instrumentMaster.evPitchbend))
                        case "cat":
                            instrumentMaster.evChannelAftertouch = i.argument[1]
                            mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Channel Aftertouch"))
                            print("Setting polyphonic aftertouch to " + str(instrumentMaster.evChannelAftertouch))
                        case "pc":
                            instrumentMaster.evProgramChange = i.argument[1]
                            mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Program change"))
                            print("Setting polyphonic aftertouch to " + str(instrumentMaster.evProgramChange))

                case "psf":
                    stringModules[currentSerialModule].stringFrequency = float(i.argument[0])
                    mainWidget.updateContinuousStringModuleData()
                    print("Setting string frequency to " + str(stringModules[currentSerialModule].stringFrequency))

                case "bmf":
                    stringModules[currentSerialModule].bowFrequency = float(i.argument[0])
                    mainWidget.updateContinuousStringModuleData()
                    print("Setting bow frequency to " + str(stringModules[currentSerialModule].stringFrequency))

                case "bchbn":
                    for a in range(1, mainWidget.ui.comboBoxBaseNote.count()):
                        if int(mainWidget.ui.comboBoxBaseNote.itemData(a)) == int(i.argument[0]):
                            mainWidget.ui.comboBoxBaseNote.setCurrentIndex(a)
                    print("setting base note to " + str(i.argument[0]))

                case "bmc":
                    stringModules[currentSerialModule].bowCurrent = float(i.argument[0])
                    mainWidget.updateContinuousStringModuleData()
                    print("Setting bow current to " + str(stringModules[currentSerialModule].bowCurrent))

                case "sxf":
                    stringModules[currentSerialModule].setSolenoidMaxForce(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting solenoid max force to " + str(stringModules[currentSerialModule].getSolenoidMaxForce()))

                case "sif":
                    stringModules[currentSerialModule].setSolenoidMinForce(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting solenoid min force to " + str(stringModules[currentSerialModule].getSolenoidMinForce()))

                case "sed":
                    stringModules[currentSerialModule].setSolenoidEngageDuration(i.argument[0])
                    mainWidget.updateStringModuleData()
                    print("Setting solenoid engage duration to " + str(stringModules[currentSerialModule].getSolenoidEngageDuration()))

                case "bcf":
                    stringModules[currentSerialModule].setSetFrequency(i.argument[0])
                    mainWidget.updateContinuousStringModuleData()
                    print("Setting set frequency to " + str(stringModules[currentSerialModule].setFrequency))

                case "adcr":
                    print("adcr " + str(i.argument[0]) + ":" + str(i.argument[1]))
                    stringModules[currentSerialModule].setCV(int(i.argument[0]), int(i.argument[1]))
                    print("module data " + str(stringModules[currentSerialModule].getCV(0)))
                    mainWidget.updateContinuousStringModuleData()

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
                        break
                    mainWidget.ui.comboBoxActuatorPreset.addItem(i.argument[4], i.argument[0])

                case "mcfc":
                    mainWidget.ui.comboBoxConfiguration.clear()
                    for a in range(0, int(i.argument[0])):
                        serialHandler.write("rqi:mcfn:" + str(a))

                case "mcfn":
                        mainWidget.ui.comboBoxConfiguration.insertItem(int(i.argument[0]), str(i.argument[1]))

                case "bcp":
                    mainWidget.updateUIData()

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

                case _:
                    processed = processed | False
                    #processed = False
        except:
            pass

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
            case "[str]":
                scopeText = "This command is dependent on the currently selected module, bow and/or solenoid"
            case _:
                skip = True
                print("Unknown " + i.command)

        if not skip:
            x = command.find("|")
            help = scopeText + "\n"
            help += "command: " + command + "\n"
            help += "data: "
            for j in range(1,len(i.argument) - 1):
                help += i.argument[j]
                if (j < (len(i.argument)-2)):
                    help += ":"
            help += "\nDescription: " + i.argument[len(i.argument) - 1]

            if x != -1:
                command = command[:x]

            commandItemHelp = QListWidgetItem()
            commandItemHelp.setText(command)
            commandItemHelp.setData(Qt.UserRole, help)
            mainWidget.ui.listWidgetCommands.addItem(commandItemHelp)
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
    serialHandler.write("rqi:bowcontrolharmoniclist")
    serialHandler.write("rqi:bowcontrolharmoniccount")
    serialHandler.write("rqi:midieventhandler")
    serialHandler.write("rqi:bowcontrolharmonicbasenote")
    serialHandler.write("rqi:solenoidmaxforce")
    serialHandler.write("rqi:solenoidminforce")
    serialHandler.write("rqi:solenoidengageduration")
    serialHandler.write("rqi:bowactuatorcount")
    serialHandler.write("rqi:midiconfigurationcount")
    serialHandler.write("rqi:mrc")
    serialHandler.write("help")

def requestBaseData():
    serialHandler.write("rqi:modulecount")

class serialHandler(QThread):
#    dataAvaliable = Signal(str)
    dataAvaliable = Signal(object, str)
    disconnectSignal = Signal()
    chartDataSignal = Signal(str, float, timedChart.seriesType) # float, float)

#    def __init__(self):
#        #QThread.__init__(self)
#        pass

    def run(self) -> None:
        #for index in range(20):
#        connectionTimeout = process_time()
#        alive = 0
        while self.isRunning:
            processed = False
            global serialStream
            try:
                if serialStream is not None:                   
                    if serialStream.inWaiting() != 0:
                        receivedText = serialStream.readline().decode('ascii').strip()
                        print("Received '" + receivedText + "'")
#                        if (receivedText[:5] == "[irq]"):
#                            processed = processInformationReturn(self, receivedText[5:])
#                        elif (receivedText[:5] == "[hlp]"):
#                            processed = processHelpReturn(receivedText[5:])
#
#                        if (not processed):
#                            self.dataAvaliable.emit("<si< " + receivedText)
                        self.dataAvaliable.emit(self, receivedText)

            except Exception as e:
                serialStream = None
#                mainWidget.serialDisconnect()
                self.disconnectSignal.emit()
                print("Error in serialStream")
                print(e)
            self.sleep(0.1)

    def stop(self):
        self.isRunning = False

    def write(str):
        mainWidget.addToDebugWindow(">so> " + str + "\n")
        str = str  + "\n\r"
        if serialStream == None:
            return
        serialStream.write(str.encode('ascii'))

    def writeI(self, str):
        str = str  + "\n\r"
        serialStream.write(str.encode('ascii'))

def setReportFeedback(reportType, state):
    if (state):
        out = "1"
    else:
        out = "0"
    serialHandler.write("debugprint:" + reportType + ":" + out)

def selectSendDestinationAndRatio(comboBox, commandList, ratio, variable):
    comboBox.blockSignals(True)

    find = ""
    for a in commandList.commands:
        match a.command:
            case "bpm":
                find = "Pressure modifier"
                break
            case "bpb":
                find = "Pressure baseline"
                break
            case "msp":
                find = "Mute position"
                break
            case "sfm":
                find = "Solenoid force multiplier"
                break
            case "bchsh":
                find = "Harmonic shift"
                break

    if find == "":
        find = "Nothing"

    for b in range(0, comboBox.count()):
        if find == comboBox.itemText(b):
            comboBox.setCurrentIndex(b)
            break

    if find != "Nothing":
        try:
            offset, multiplier = equationParsingHelpers.getVariable(a.argument[0], variable)
            ratio.setValue(multiplier)
        except:
            pass


    comboBox.blockSignals(False)

class MainWidget(QWidget):
    midiDataAvaliableSignal = Signal(str, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

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

        self.midiHandlerC = midihandler.MidiHandler(self.midiDataAvaliableSignal) #self.addToDebugWindow)
        self.midiHandlerC.updateMIDIInDevices(self.ui.comboBoxMIDILearnDevice)
        self.midiDataAvaliableSignal.connect(self.midiDataAvaliable)

        self.updatingFromModule = False

    def addData(self, seriesID, value, inSeriesType): # min, max):
        self.debugTimedChart.addData(seriesID, value, inSeriesType) # min, max)
                #str(i.command + i.argument[0]) i.argument[1]
#        self.addData("adcr0", 5)

    def timerUpdateControl(self):
        self.readSMData()

    def closeEvent(self, event):
        self.serialThread.stop()
        self.serialThread.quit()
        self.serialThread.wait()
        print("close")

    @Slot(str)
    def midiDataAvaliable(self, device, msg):
        self.addToDebugWindow("<mi<" + str(msg) + "\n")
        # + str(device) + "<"
        pass

    def dataAvaliable(self, inSerialHandler, v):
#        self.addToDebugWindow(v + "\n")
        receivedText = v
        if (receivedText[:5] == "[irq]"):
            processed = processInformationReturn(inSerialHandler, receivedText[5:])
        elif (receivedText[:5] == "[hlp]"):
            processed = processHelpReturn(receivedText[5:])

        #if (not processed):
        self.addToDebugWindow("<si< " + receivedText + "\n")

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

        logging.error(text.rstrip("\n"))

    def setUIEnabled(self, state):
        self.ui.checkBoxFilterCommAck.setEnabled(state)
        self.ui.checkBoxFilterUSB.setEnabled(state)
        self.ui.checkBoxFilterHardware.setEnabled(state)
        self.ui.checkBoxFilterUndefined.setEnabled(state)
        self.ui.checkBoxFilterPriority.setEnabled(state)
        self.ui.checkBoxFilterError.setEnabled(state)
        self.ui.checkBoxFilterInfoRequest.setEnabled(state)
        self.ui.checkBoxFilterExpressionParser.setEnabled(state)
        self.ui.checkBoxFilterDebug.setEnabled(state)
        self.ui.checkBoxFilterOutput.setEnabled(state)
        self.ui.tabWidgetMain.setEnabled(state)

    def updateUIData(self):
        self.ui.listWidgetMidiEvents.clear()
        self.ui.listWidgetCommands.clear()
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
                    self.addToDebugWindow("Connected to " + serialStream.portstr + "\n")
                    mainWidget.ui.pushButtonConnectDisconnect.setText("Disconnect")

                    self.setUIEnabled(True)
                    self.updateUIData()

                    self.checkBoxFilterErrorToggled()
                    self.checkBoxFilterExpressionParserToggled()
                    self.checkBoxFilterDebugToggled()
                    self.checkBoxFilterHardwareToggled()
                    self.checkBoxFilterPriorityToggled()
                    self.checkBoxFilterUndefinedToggled()
                    self.checkBoxFilterUSBToggled()
                    self.checkBoxFilterCommAckToggled()
                    serialHandler.write("debugprint:inforequest:1")

                    #self.ui.checkBoxFilterCommAck.setChecked(True)
                    #self.ui.checkBoxFilterDebug.setChecked(True)
                    #self.ui.checkBoxFilterError.setChecked(True)
                    #self.ui.checkBoxFilterExpressionParser.setChecked(True)
                    #self.ui.checkBoxFilterHardware.setChecked(True)
                    #self.ui.checkBoxFilterInfoRequest.setChecked(True)
                    #self.ui.checkBoxFilterPriority.setChecked(True)
                    #self.ui.checkBoxFilterUSB.setChecked(True)
                    #self.ui.checkBoxFilterUndefined.setChecked(True)

                except (OSError, serial.SerialException):
                    print("Connection issue")
                    pass
        else:
            if serialStream.isOpen:
                serialStream.close()
                serialStream = None
                self.setUIEnabled(False)
            self.addToDebugWindow("Disconnected\n")
            mainWidget.ui.pushButtonConnectDisconnect.setText("Connect")

    def serialDisconnect(self):
        self.ui.checkBoxContinuousSMData.setChecked(False)
        self.updateTimer.stop()
        self.ui.pushButtonConnectDisconnect.setText("Connect")
        self.setUIEnabled(False)

    def populateSerialPorts(self):
        for port, desc, hwid in sorted(serialPorts):
                print("{}: {}".format(port, desc))
                mainWidget.ui.comboBoxSerialPorts.addItem(port + " - " + desc)

    def lineEditSend(self):
        if serialStream is not None:
            tempText = mainWidget.ui.lineEditSend.text()
            #+ "\r\n"
    #        serialStream.write(tempText.encode('ascii'))
            serialHandler.write(tempText)
            print("sending " + str(tempText.encode()))
            mainWidget.ui.lineEditSend.clear()
        #print(widget.ui.lineEditSend.text())

    def updateStringModuleData(self):
        global stringModules
        global currentShowingModule
        self.ui.doubleSpinBoxFundamentalFrequency.setValue(float(stringModules[currentShowingModule].getFundamentalFrequency()))
        self.ui.doubleSpinBoxBowMotorVoltage.setValue(float(stringModules[currentShowingModule].getMotorVoltage()))
        self.ui.doubleSpinBoxBowMotorTimeout.setValue(float(stringModules[currentShowingModule].getBowTimeOut()))
        self.ui.doubleSpinBoxMuteFullMutePosition.setValue(float(stringModules[currentShowingModule].getMuteFullMutePosition()))
        self.ui.doubleSpinBoxMuteHalfMutePosition.setValue(float(stringModules[currentShowingModule].getMuteHalfMutePosition()))
        self.ui.doubleSpinBoxMuteRestPosition.setValue(float(stringModules[currentShowingModule].getMuteRestPosition()))
        self.ui.doubleSpinBoxMuteBackoff.setValue(float(stringModules[currentShowingModule].getMuteBackoff()))
        self.ui.doubleSpinBoxBowMotorMaxSpeed.setValue(float(stringModules[currentShowingModule].getBowMotorMaxSpeed()))
        self.ui.doubleSpinBoxBowMotorMinSpeed.setValue(float(stringModules[currentShowingModule].getBowMotorMinSpeed()))
        self.ui.doubleSpinBoxBowMaxPressure.setValue(float(stringModules[currentShowingModule].getBowMaxPressure()))
        self.ui.doubleSpinBoxBowMinPressure.setValue(float(stringModules[currentShowingModule].getBowMinPressure()))
        self.ui.doubleSpinBoxBowRestPosition.setValue(float(stringModules[currentShowingModule].getBowRestPosition()))

        self.ui.horizontalSliderBowFrequency.setMaximum(int(float(stringModules[currentShowingModule].getBowMotorMaxSpeed()) ))
        self.updateContinuousStringModuleData()

        self.ui.doubleSpinBoxSolenoidMaxForce.setValue(float(stringModules[currentShowingModule].getSolenoidMaxForce()))
        self.ui.doubleSpinBoxSolenoidMinForce.setValue(float(stringModules[currentShowingModule].getSolenoidMinForce()))
        self.ui.doubleSpinBoxSolenoidEngageDuration.setValue(float(stringModules[currentShowingModule].getSolenoidEngageDuration()))

    def updateContinuousStringModuleData(self): 
        freq = float(stringModules[currentShowingModule].stringFrequency)
        self.ui.horizontalSliderStringFrequency.setValue(int(freq))
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
            self.ui.dialAnalyzeCents.setValue(round(ret[2]))
            self.ui.labelAnalyzeFreq.setText(str(round(freq,1)))
            self.ui.dialAnalyzeFreq.setValue(round(freq,1))
            self.ui.labelStringFrequency.setText(ret[3] + str(ret[0]) + ":" + str(round(ret[2])) + " / " + str(round(freq,1)) + "Hz")

        freq = float(stringModules[currentShowingModule].bowFrequency)
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

        current = float(stringModules[currentShowingModule].bowCurrent)
        mainWidget.ui.horizontalSliderBowCurrent.setValue(int(current * 10))
        mainWidget.ui.labelBowCurrent.setText(str(current) + " A")

        freq = float(stringModules[currentShowingModule].setFrequency)
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

            dial.setValue( int(stringModules[currentShowingModule].getCV(cv)) )
            label.setText(str(stringModules[currentShowingModule].getCV(cv)) )

    def debugClear(self):
        self.ui.plainTextEditSerialOutput.clear()

    def checkBoxFilterCommAckToggled(self):
        setReportFeedback("command", self.ui.checkBoxFilterCommAck.isChecked())

    def checkBoxFilterDebugToggled(self):
        setReportFeedback("debug", self.ui.checkBoxFilterDebug.isChecked())

    def checkBoxFilterErrorToggled(self):
        setReportFeedback("error", self.ui.checkBoxFilterError.isChecked())

    def checkBoxFilterExpressionParserToggled(self):
        setReportFeedback("expressionparser", self.ui.checkBoxFilterExpressionParser.isChecked())

    def checkBoxFilterHardwareToggled(self):
        setReportFeedback("hardware", self.ui.checkBoxFilterHardware.isChecked())

    def checkBoxFilterInfoRequestToggled(self):
        #setReportFeedback("inforequest", self.ui.checkBoxFilterInfoRequest.isChecked())
        if (self.ui.checkBoxFilterInfoRequest.isChecked()):
            self.filterHideInfoRequest = False
        else:
            self.filterHideInfoRequest = True

    def checkBoxFilterPriorityToggled(self):
        setReportFeedback("priority", self.ui.checkBoxFilterPriority.isChecked())

    def checkBoxFilterUSBToggled(self):
        setReportFeedback("usb", self.ui.checkBoxFilterUSB.isChecked())

    def checkBoxFilterUndefinedToggled(self):
        setReportFeedback("undefined", self.ui.checkBoxFilterUndefined.isChecked())

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

    def comboBoxCurrentSelectedModuleIndexChanged(self, index):
        global currentShowingModule
        currentShowingModule = index
        print("Setting currently showing module to " + str(currentShowingModule))

    def doubleSpinBoxFundamentalFrequencyValueChanged(value):
        out = "m:" + str(currentShowingModule) + ",bowcontrolfundamental:" + str(mainWidget.ui.doubleSpinBoxFundamentalFrequency.value())
        serialHandler.write(out)
        print(out)

    def doubleSpinBoxBowMotorVoltageValueChanged(value):
        out = "m:" + str(currentShowingModule) + ",bowmotorvoltage:" + str(mainWidget.ui.doubleSpinBoxBowMotorVoltage.value())
        serialHandler.write(out)
        print(out)

    def doubleSpinBoxBowMotorTimeoutValueChanged(self):
        out = "m:" + str(currentShowingModule) + ",bowmotortimeout:" + str(
            mainWidget.ui.doubleSpinBoxBowMotorTimeout.value())
        serialHandler.write(out)
        print(out)

    def doubleSpinBoxBowMaxPressureValueChanged(value):
        out = "m:" + str(currentShowingModule) + ",bowpressurepositionmax:" + str(mainWidget.ui.doubleSpinBoxBowMaxPressure.value())
        serialHandler.write(out)
        print(out)

    def doubleSpinBoxBowMinPressureValueChanged(value):
        out = "m:" + str(currentShowingModule) + ",bowpressurepositionengage:" + str(mainWidget.ui.doubleSpinBoxBowMinPressure.value())
        serialHandler.write(out)
        print(out)

    def doubleSpinBoxBowRestPositionValueChanged(value):
        out = "m:" + str(currentShowingModule) + ",bowpressurepositionrest:" + str(mainWidget.ui.doubleSpinBoxBowRestPosition.value())
        serialHandler.write(out)
        print(out)

    def doubleSpinBoxMuteFullMutePositionValueChanged(value):
        out = "m:" + str(currentShowingModule) + ",mutefullmuteposition:" + str(mainWidget.ui.doubleSpinBoxMuteFullMutePosition.value())
        serialHandler.write(out)
        print(out)

    def doubleSpinBoxMuteHalfMutePositionValueChanged(value):
        out = "m:" + str(currentShowingModule) + ",mutehalfmuteposition:" + str(mainWidget.ui.doubleSpinBoxMuteHalfMutePosition.value())
        serialHandler.write(out)
        print(out)

    def doubleSpinBoxMuteRestPositionValueChanged(value):
        out = "m:" + str(currentShowingModule) + ",muterestposition:" + str(mainWidget.ui.doubleSpinBoxMuteRestPosition.value())
        serialHandler.write(out)
        print(out)

    def doubleSpinBoxMuteBackoffValueChanged(self):
        serialHandler.write("mutebackoff:" + str(mainWidget.ui.doubleSpinBoxMuteBackoff.value()))

    def pushButtonCalibrateMutePressed(self):
        serialHandler.write("mutecalibrate")

    def tableViewScaleDataChanged(self, topLeft, bottomRight, role):
        print("edited " + str(topLeft.column()) + ":" + str(topLeft.data()))
        serialHandler.write("m:" + str(currentSerialModule) + ",bowcontrolharmonicratio:" + str(topLeft.column()) + ":" + str(topLeft.data()))

    def comboBoxHarmonicListCurrentIndexChanged(self, index):
        currentHarmonicListSelected = int(index)
        mainWidget.ui.tableViewScale.setModel(tableTest.CustomTableModel(stringModules[currentSerialModule].harmonicData[currentHarmonicListSelected]))
        mainWidget.ui.tableViewScale.model().dataChanged.connect(mainWidget.tableViewScaleDataChanged)

    def doubleSpinBoxSolenoidMaxForceValueChanged(self, value):
        out = "m:" + str(currentShowingModule) + ",solenoidmaxforce:" + str(mainWidget.ui.doubleSpinBoxSolenoidMaxForce.value())
        serialHandler.write(out)
        print(out)

    def doubleSpinBoxSolenoidMinForceValueChanged(self, value):
        out = "m:" + str(currentShowingModule) + ",solenoidminforce:" + str(mainWidget.ui.doubleSpinBoxSolenoidMinForce.value())
        serialHandler.write(out)
        print(out)

    def doubleSpinBoxSolenoidEngageDurationValueChanged(self):
        out = "m:" + str(currentShowingModule) + ",solenoidengageduration:" + str(mainWidget.ui.doubleSpinBoxSolenoidEngageDuration.value())
        serialHandler.write(out)
        print(out)


    def updateLineLimit(self):
        if (self.ui.checkBoxLimitLines.checkState() == Qt.CheckState.Checked):
            self.ui.plainTextEditSerialOutput.setMaximumBlockCount(self.ui.spinBoxLimitLines.value())
        else:
            self.ui.plainTextEditSerialOutput.setMaximumBlockCount(0)

    def checkBoxLimitLinesStateChanged(self):
        self.updateLineLimit()

    def spinBoxLimitLinesValueChanged(self, value):
        self.updateLineLimit()

    def pushButtonSaveToModulePressed(self):
        serialHandler.write("globalsaveallparameters")
    def pushButtonLoadFromModulePressed(self):
        self.updateUIData()

    eventDescription = [[ "Note On", "Note on message, sent when a key has been depressed. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n note - note number (0-127) \n velocity - key velocity (0-127)" ],
        [ "Note Off", "Note off message, sent when a key has been released. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n note - note number (0-127) \n velocity - key velocity (0-127)" ],
        [ "CC [xx]", "Continous Controller, sent by various control surfaces. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n control - control number (0-127) \n value - controller value (0-127)" ],
        [ "Poly Aftertouch", "Polyphonic Aftertouch, key pressure per key. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n note - note number (0-127) \n pressure - key pressure (0-127)" ],
        [ "Channel Aftertouch", "Channel Aftertouch, key pressure per channel. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n pressure - key pressure (0-127)"],
        [ "Pitchbend", "Pitchbend, frequency change from the current key. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n pitch - bend (-32767 - 32767)"],
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
            #print(self.harmonicPresets[b][c])
            #d = tableTest.QAbstractTableModel.createIndex(tableTest.QAbstractTableModel, 0, c - 1)
            mainWidget.ui.tableViewScale.model().setDataNR((c - 1), float(self.harmonicPresets[b][c]))

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

    def listWidgetCommandsCurrentItemChanged(self, current, previous):
        mainWidget.ui.plainTextEditCMVDescription.clear()
        if current is not None:
            mainWidget.ui.plainTextEditCMVDescription.insertPlainText(current.data(Qt.UserRole))

    def find_item(self, combo_box, item_text):
        for index in range(combo_box.count()):
            if combo_box.itemText(index) == item_text:
                return index
        return -1

    def pushButtonActuatorSavePressed(self):
        comboIndex = self.find_item(mainWidget.ui.comboBoxActuatorPreset, mainWidget.ui.comboBoxActuatorPreset.currentText())
        if comboIndex == -1:
            comboIndex = mainWidget.ui.comboBoxActuatorPreset.count()
            serialHandler.write("baa")
        serialHandler.write("bas:" + str(comboIndex) + ",bav,bai:'" + mainWidget.ui.comboBoxActuatorPreset.currentText() + "',bac")

    def pushButtonActuatorLoadPressed(self):
        comboIndex = self.find_item(mainWidget.ui.comboBoxActuatorPreset, mainWidget.ui.comboBoxActuatorPreset.currentText())
        if comboIndex == -1:
            return
        serialHandler.write("bas:" + str(comboIndex) + ",bal,rqi:bxp,rqi:bip,rqi:brp")
    def pushButtonAcutatorDeletePreset(self):
        comboIndex = self.find_item(mainWidget.ui.comboBoxActuatorPreset, mainWidget.ui.comboBoxActuatorPreset.currentText())
        if comboIndex == -1:
            return
        mainWidget.ui.comboBoxActuatorPreset.removeItem(comboIndex)
        serialHandler.write("bar:" + str(comboIndex) + ",bal,rqi:bxp,rqi:bip,rqi:brp")

    def pushButtonCalibrateSpeedPressed(self):
        serialHandler.write("bowcalibratespeed")

    def pushButtonCalibratePressurePressed(self):
        serialHandler.write("bowcalibratepressure")

    def configurationSetName(self):
        defText = mainWidget.ui.comboBoxConfiguration.currentText()
        text, ok = QInputDialog().getText(self, "Configuration name",
                                          "Configuration name:", QLineEdit.Normal, defText)
        conf = mainWidget.ui.comboBoxConfiguration.currentIndex()
        if ok and text and (conf > -1):
            serialHandler.write("midiconfiguration:" + str(conf) + ",midiconfigurationname:" + text)
            mainWidget.ui.comboBoxConfiguration.setItemText(conf, text)

    def selectMIDIDevice(self, Index):
        if mainWidget.ui.comboBoxMIDILearnDevice.currentIndex() == -1:
            return
        # midiIn = mido.open_input(mainWidget.ui.comboBoxMIDILearnDevice.currentText())
        self.midiHandlerC.connecToMIDIIn(mainWidget.ui.comboBoxMIDILearnDevice.currentText())

    def pushButtonMidiRestoreDefaults(self):
        serialHandler.write("mcfd")

    def ccAdd(self):
        cc, ok = QInputDialog.getInt(self, "CC Number", "CC Number")
        if ok and (cc > -1 and cc < 128):
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

    def cmdNoteOnUpdate(self):
        if self.updatingFromModule:
            return

        cl = CommandList(self.ui.midiNoteOnOther.text())
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
        cl = CommandList(self.ui.midiNoteOffOther.text())
        cmd = cl.buildCommandString({"mfm", "bmr"})

        if self.ui.midiNoteOffSendFullMute.checkState() == Qt.CheckState.Checked:
            cmd += ",mfm:1"
        if self.ui.midiNoteOffMotorOff.checkState() == Qt.CheckState.Checked:
            cmd += ",bmr:1"
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

if __name__ == "__main__":
#    sys.excepthook = except_hook

    app = QApplication(sys.argv)
    mainWidget = MainWidget()
    mainWidget.show()

    mainWidget.ui.listWidgetCommands.setSortingEnabled(True)
    #mainWidget.ui.comboBoxFundamentalFrequency
## Hiding old
    mainWidget.ui.horizontalSliderStringFrequency.setVisible(False)
    mainWidget.ui.labelStringFrequency.setVisible(False)
    mainWidget.ui.horizontalSliderBowCurrent.setVisible(False)
    mainWidget.ui.horizontalSliderBowFrequency.setVisible(False)

## Global commands
    mainWidget.ui.pushButtonConnectDisconnect.pressed.connect(mainWidget.connectDisconnect)
    mainWidget.ui.pushButtonSaveToModule.pressed.connect(mainWidget.pushButtonSaveToModulePressed)
    mainWidget.ui.pushButtonLoadFromModule.pressed.connect(mainWidget.pushButtonLoadFromModulePressed)
    mainWidget.ui.pushButtonReadSMData.pressed.connect(mainWidget.readSMData)
    mainWidget.ui.checkBoxContinuousSMData.toggled.connect(mainWidget.checkBoxContinuousSMDataToggled)
## Debug console
    mainWidget.ui.checkBoxFilterCommAck.toggled.connect(mainWidget.checkBoxFilterCommAckToggled)
    mainWidget.ui.checkBoxFilterDebug.toggled.connect(mainWidget.checkBoxFilterDebugToggled)
    mainWidget.ui.checkBoxFilterError.toggled.connect(mainWidget.checkBoxFilterErrorToggled)
    mainWidget.ui.checkBoxFilterExpressionParser.toggled.connect(mainWidget.checkBoxFilterExpressionParserToggled)
    mainWidget.ui.checkBoxFilterHardware.toggled.connect(mainWidget.checkBoxFilterHardwareToggled)
    mainWidget.ui.checkBoxFilterInfoRequest.toggled.connect(mainWidget.checkBoxFilterInfoRequestToggled)
    mainWidget.ui.checkBoxFilterPriority.toggled.connect(mainWidget.checkBoxFilterPriorityToggled)
    mainWidget.ui.checkBoxFilterUSB.toggled.connect(mainWidget.checkBoxFilterUSBToggled)
    mainWidget.ui.checkBoxFilterUndefined.toggled.connect(mainWidget.checkBoxFilterUndefinedToggled)
    mainWidget.ui.checkBoxFilterOutput.toggled.connect(mainWidget.checkBoxFilterOutputToggled)
    mainWidget.ui.lineEditSend.editingFinished.connect(mainWidget.lineEditSend)
    mainWidget.ui.checkBoxDebugCursorFollow.toggled.connect(mainWidget.checkBoxDebugCursorFollowToggled)
    mainWidget.ui.pushButtonClear.pressed.connect(mainWidget.debugClear)
    mainWidget.ui.checkBoxLimitLines.stateChanged.connect(mainWidget.checkBoxLimitLinesStateChanged)
    mainWidget.ui.spinBoxLimitLines.valueChanged.connect(mainWidget.spinBoxLimitLinesValueChanged)

## Tab Module settings
    mainWidget.ui.comboBoxCurrentlySelectedModule.currentIndexChanged.connect(mainWidget.comboBoxCurrentSelectedModuleIndexChanged)

    mainWidget.ui.doubleSpinBoxFundamentalFrequency.valueChanged.connect(mainWidget.doubleSpinBoxFundamentalFrequencyValueChanged)
    mainWidget.ui.comboBoxBaseNote.currentIndexChanged.connect(mainWidget.comboBoxBaseNotePressed)
    mainWidget.ui.comboBoxFundamentalFrequency.currentIndexChanged.connect(mainWidget.comboBoxFundamentalFrequencyIndexChanged)
    mainWidget.ui.listWidgetTuningscheme.currentItemChanged.connect(mainWidget.tuningSchemeChanged)

    mainWidget.ui.doubleSpinBoxBowMotorVoltage.valueChanged.connect(mainWidget.doubleSpinBoxBowMotorVoltageValueChanged)
    mainWidget.ui.doubleSpinBoxBowMotorTimeout.valueChanged.connect(mainWidget.doubleSpinBoxBowMotorTimeoutValueChanged)
    mainWidget.ui.pushButtonCalibrateMotorSpeed.pressed.connect(mainWidget.pushButtonCalibrateSpeedPressed)

    mainWidget.ui.doubleSpinBoxBowMaxPressure.valueChanged.connect(mainWidget.doubleSpinBoxBowMaxPressureValueChanged)
    mainWidget.ui.doubleSpinBoxBowMinPressure.valueChanged.connect(mainWidget.doubleSpinBoxBowMinPressureValueChanged)
    mainWidget.ui.doubleSpinBoxBowRestPosition.valueChanged.connect(mainWidget.doubleSpinBoxBowRestPositionValueChanged)
    mainWidget.ui.pushButtonCalibratePressure.pressed.connect(mainWidget.pushButtonCalibratePressurePressed)

    mainWidget.ui.doubleSpinBoxMuteFullMutePosition.valueChanged.connect(mainWidget.doubleSpinBoxMuteFullMutePositionValueChanged)
    mainWidget.ui.doubleSpinBoxMuteHalfMutePosition.valueChanged.connect(mainWidget.doubleSpinBoxMuteHalfMutePositionValueChanged)
    mainWidget.ui.doubleSpinBoxMuteRestPosition.valueChanged.connect(mainWidget.doubleSpinBoxMuteRestPositionValueChanged)
    mainWidget.ui.doubleSpinBoxMuteBackoff.valueChanged.connect(mainWidget.doubleSpinBoxMuteBackoffValueChanged)
    mainWidget.ui.pushButtonCalibrateMute.pressed.connect(mainWidget.pushButtonCalibrateMutePressed)

    mainWidget.ui.comboBoxHarmonicList.currentIndexChanged.connect(mainWidget.comboBoxHarmonicListCurrentIndexChanged)
    mainWidget.ui.pushButtonLoadHarmonicPreset.pressed.connect(mainWidget.pushButtonLoadHarmonicPresetPressed)

    mainWidget.ui.doubleSpinBoxSolenoidMaxForce.valueChanged.connect(mainWidget.doubleSpinBoxSolenoidMaxForceValueChanged)
    mainWidget.ui.doubleSpinBoxSolenoidMinForce.valueChanged.connect(mainWidget.doubleSpinBoxSolenoidMinForceValueChanged)
    mainWidget.ui.doubleSpinBoxSolenoidEngageDuration.valueChanged.connect(mainWidget.doubleSpinBoxSolenoidEngageDurationValueChanged)

    mainWidget.ui.pushButtonActuatorSave.pressed.connect(mainWidget.pushButtonActuatorSavePressed)
    mainWidget.ui.pushButtonActuatorLoad.pressed.connect(mainWidget.pushButtonActuatorLoadPressed)
    mainWidget.ui.pushButtonActuatorDelete.pressed.connect(mainWidget.pushButtonAcutatorDeletePreset)

## Tab Midi settings
    mainWidget.ui.comboBoxMidiChannel.currentIndexChanged.connect(mainWidget.comboBoxMidiChannelIndexChanged)

    mainWidget.ui.pushButtonMidiRestoreDefaults.pressed.connect(mainWidget.pushButtonMidiRestoreDefaults)

    mainWidget.ui.midiNoteOnVelToHammer.valueChanged.connect(mainWidget.cmdNoteOnUpdate)
    mainWidget.ui.midiNoteOnHammerStaccato.stateChanged.connect(mainWidget.cmdNoteOnUpdate)
    mainWidget.ui.midiNoteOnSendMuteRest.stateChanged.connect(mainWidget.cmdNoteOnUpdate)
    mainWidget.ui.midiNoteOnOther.editingFinished.connect(mainWidget.cmdNoteOnUpdate)

    mainWidget.ui.midiNoteOffOther.editingFinished.connect(mainWidget.cmdNoteOffUpdate)
    mainWidget.ui.midiNoteOffSendFullMute.stateChanged.connect(mainWidget.cmdNoteOffUpdate)
    mainWidget.ui.midiNoteOffMotorOff.stateChanged.connect(mainWidget.cmdNoteOffUpdate)

    mainWidget.ui.pushButtonConfigurationName.pressed.connect(mainWidget.configurationSetName)
    mainWidget.ui.listWidgetMidiEvents.currentItemChanged.connect(mainWidget.listWidgetMidiEventscurrentItemChanged)
    mainWidget.ui.lineEditMidiEventCommand.editingFinished.connect(mainWidget.lineEditMidiEventCommandFinished)
    mainWidget.ui.listWidgetCommands.currentItemChanged.connect(mainWidget.listWidgetCommandsCurrentItemChanged)
    mainWidget.ui.comboBoxMIDILearnDevice.currentIndexChanged.connect(mainWidget.selectMIDIDevice)
    mainWidget.ui.pushButtonCCAdd.pressed.connect(mainWidget.ccAdd)
    mainWidget.ui.pushButtonCCRemove.pressed.connect(mainWidget.ccRemove)
## Tab Debugging
    mainWidget.ui.tableViewScale.setModel(tableTest.CustomTableModel())
    delegate = tableTest.SpinBoxDelegate()
    mainWidget.ui.tableViewScale.setItemDelegateForRow(0, delegate)
    mainWidget.ui.tableViewScale.model().dataChanged.connect(mainWidget.tableViewScaleDataChanged)

## Default settings
    mainWidget.addTuningSchemes()
    mainWidget.ui.spinBoxLimitLines.setValue(2500)
    mainWidget.setUIEnabled(True)
    mainWidget.ui.checkBoxLimitLines.setCheckState(Qt.CheckState.Checked)

    mainWidget.ui.checkBoxFilterInfoRequest.setCheckState(Qt.CheckState.Unchecked)
    mainWidget.ui.checkBoxFilterOutput.setCheckState(Qt.CheckState.Unchecked)
    mainWidget.checkBoxFilterInfoRequestToggled()
    mainWidget.checkBoxFilterOutputToggled()
    mainWidget.ui.checkBoxFilterUSB.setCheckState(Qt.CheckState.Checked)
    mainWidget.ui.checkBoxFilterHardware.setCheckState(Qt.CheckState.Unchecked)
    mainWidget.ui.checkBoxFilterExpressionParser.setCheckState(Qt.CheckState.Unchecked)
    mainWidget.ui.checkBoxFilterCommAck.setCheckState(Qt.CheckState.Checked)
    mainWidget.ui.checkBoxFilterDebug.setCheckState(Qt.CheckState.Unchecked)
    mainWidget.ui.checkBoxFilterPriority.setCheckState(Qt.CheckState.Checked)
    mainWidget.ui.checkBoxFilterError.setCheckState(Qt.CheckState.Checked)
    mainWidget.ui.checkBoxFilterUndefined.setCheckState(Qt.CheckState.Checked)
    mainWidget.checkBoxDebugCursorFollowToggled()

    mainWidget.ui.plainTextEditSerialOutput.setUndoRedoEnabled(False)

#    print(str(len(data)) + ":" + str(len(data[0])))
# various tests
#    mainWidget.ui.listWidgetCommands.addItem("m")

#stringModule inits
    strm = stringModule()
    stringModules.append(strm)
#    strm.setFundamentalFrequency(230)
#    print(stringModules[0].getFundamentalFrequency())
#    print(stringModules[0].updateRequest())

#midi

#various tests
#    commandItem = CommandItem("")
#    commandList = CommandList()
#    commandList.addCommands("ev:noteon:\"m:uv0,b:0,noteon,h:note-57,spm:0,run:1,pid:1,engage:1,muterest,ssm:0,/noteon\",ev:noteoff:\"m:uv0,b:0,noteoff,rest:ibool(notecount),mutefullmute,ssm:0,/noteoff\"")
#    commandList.print()
#    processInformationReturn("ev:noteoff:\"m:uv0,b:0,noteoff,rest:ibool(notecount),mutefullmute,ssm:0,/noteoff\",ev:noteon:\"m:uv0,b:0,noteon,h:note-48,spm:0,run:1,pid:1,engage:1,muterest,ssm:0,/noteon\",ev:channelAfterTouch:\"m:uv0,b:0,spm:(pressure*150)\",ev:cc:0:\"m:0,setpressurebaseline:value*512\",ev:cc:1:\"m:0,mutesetposition:value*512\",ev:cc:16:\"m:0,pid:1,run:1,frequency:value*2,ssm:1\",ev:cc:17:\"m:0,pid:0,run:1,setbowpower:value*512,ssm:1\",ev:cc:32:\"m:0,setbowhold:value\",ev:cc:48:\"m:0,solenoidengage:value*2\",ev:cc:64:\"uservariable:0:0\",ev:cc:2:\"m:1,setpressurebaseline:value*512\",ev:cc:3:\"m:1,mutesetposition:value*512\",ev:cc:18:\"m:1,pid:1,run:1,frequency:value*2,ssm:1\",ev:cc:19:\"m:1,pid:0,run:1,setbowpower:value*512,ssm:1\",ev:cc:34:\"m:1,setbowhold:value\",ev:cc:50:\"m:1,solenoidengage:value*2\",ev:cc:66:\"uservariable:0:1\",ev:cc:4:\"m:2,setpressurebaseline:value*512\",ev:cc:5:\"m:2,mutesetposition:value*512\",ev:cc:20:\"m:2,pid:1,run:1,frequency:value*2,ssm:1\",ev:cc:21:\"m:2,pid:0,run:1,setbowpower:value*512,ssm:1\",ev:cc:36:\"m:2,setbowhold:value\",ev:cc:52:\"m:2,solenoidengage:value*2\",ev:cc:68:\"uservariable:0:2\",ev:cc:55:\"ev:noteon:'m:mapkeys(note),b:0,h:note-48,spm:0,run:1,pid:1,engage:1,muterest,ssm:0,se:1',ev:noteoff:'m:mapkeys(note),b:0,rest:1,mutefullmute,ssm:0'\",ev:cc:71:\"ev:noteon:'m:uv0,b:0,h:note-48,spm:0,run:1,pid:1,engage:1,muterest,ssm:0,se:1',ev:noteoff:'m:uv0,b:0,rest:ibool(notecount),mutefullmute,ssm:0'\",m:0,bis:19.05,bxs:539.49,bip:0,bxp:55000,brp:12460,u:66.00,mfmp:0,mhmp:0,mrp:0,ki:12.00,kp:200.00,kd:200.00,ie:0.50,bv:6.60,hl:0:1.0000:1.0595:1.1225:1.1892:1.2599:1.3348:1.4142:1.4983:1.5874:1.6818:1.7818:1.8877,hl:1:1.0000:1.0667:1.1250:1.2000:1.2500:1.3333:1.4062:1.5000:1.6000:1.6667:1.8000:1.8750")
#    ret = getBaseNoteFromFrequency(450, scaleDataJust)
#    print("Octave " + str(ret[0]))
#    print("note " + str(ret[1]))
#    print("cents " + str(ret[2]))
#    print("noteName " + str(ret[3]))

# pre-start inits
    mainWidget.populateFundamentalComboBox()
    mainWidget.populateSerialPorts()
    mainWidget.addToDebugWindow("Initialized\n")
    sys.exit(app.exec())
    mainWidget.thread1.terminate()

