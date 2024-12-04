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

from PySide6.QtWidgets import QApplication, QWidget, QDoubleSpinBox, QListWidgetItem, QInputDialog, QMessageBox, QLineEdit, QComboBox, QSlider
from PySide6.QtCore import QThread, Signal, QTimer, QModelIndex, Qt, QObject, QDir, Slot
from PySide6.QtGui import QTextBlock, QTextCursor, QTextBlockFormat, QColor

import re

import commandparser
import equationParsingHelpers
import averager

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

        #try:
        match i.command:
            case "m":
                currentSerialModule = int(i.argument[0])
                addModulesIfNeeded(currentSerialModule)
                print ("setting current serial module to " + i.argument[0])
            case "mc":
                global moduleCount
                moduleCount = int(i.argument[0])
                addModulesIfNeeded(moduleCount - 1)
                print ("setting module count to " + i.argument[0])
            case "b" | "bcu" | "bmv" | "bmt" | "bpkp" | "bpki" | "bpkd" | "bpie" | "mfmp" | "mhmp" | "mrp" | "mbo" | \
                 "bmsx" | "bmsi" | "bppx" | "bppe" | "bppr" | "bmf" | "psf" | "bmc" | "sxf" | "sif" | "sed" | "bcf" | \
                 "bpkp" | "bpki" | "bkpd" | "bpie" | "bpme" | "bhs":
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
                except:
                    messageBox("Problem! Yes!", "Oh no")

            case "bhsc":
                mainWidget.ui.comboBoxHarmonicList.clear()
                hl = 0
                while (hl < int(i.argument[0])):
                    #mainWidget.ui.comboBoxHarmonicList.addItem(str(hl))
                    mainWidget.ui.comboBoxHarmonicList.addItem(str(i.argument[hl + 1]))
                    hl += 1
                mainWidget.ui.comboBoxHarmonicList.setCurrentIndex(stringModules[currentSerialModule].getCommandValue("bhs"))
            case "mev":
                match i.argument[0]:
                    case "noteon":
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

                        mainWidget.ui.midiNoteOnOther.setText(instrumentMaster.evNoteOn)

                        print("Setting NoteOn to " + str(instrumentMaster.evNoteOn))
                    case "noteoff":
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

                        mainWidget.ui.midiNoteOffOther.setText(instrumentMaster.evNoteOff)

                        print("Setting NoteOff to " + str(instrumentMaster.evNoteOff))
                    case "cc":
                        instrumentMaster.addCC(int(i.argument[1]), str(i.argument[2]))
                        mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("CC " + str(i.argument[1])))
                        print("Setting CC " + i.argument[1] + " to " + str(i.argument[2]))
                    case "pat":
                        instrumentMaster.evPolyAftertouch = i.argument[1]
                        mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Poly Aftertouch"))

                        instrumentMaster.cmdPolyAftertouch.clear()
                        instrumentMaster.cmdPolyAftertouch.addCommands(i.argument[1])

                        selectSendDestinationAndRatio(mainWidget.ui.midiPolyATSend, instrumentMaster.cmdPolyAftertouch,
                                                      mainWidget.ui.midiPolyATRatio, "pressure")

                        print("Setting polyphonic aftertouch to " + str(instrumentMaster.evPolyAftertouch))
                    case "pb":
                        instrumentMaster.evPitchbend = i.argument[1]
                        mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Pitchbend"))

                        instrumentMaster.cmdPitchbend.clear()
                        instrumentMaster.cmdPitchbend.addCommands(i.argument[1])

                        selectSendDestinationAndRatio(mainWidget.ui.midiPitchbendSend, instrumentMaster.cmdPitchbend,
                                                      mainWidget.ui.midiPitchbendRatio, "pitch")

                        print("Setting polyphonic aftertouch to " + str(instrumentMaster.evPitchbend))
                    case "cat":
                        instrumentMaster.evChannelAftertouch = i.argument[1]
                        mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Channel Aftertouch"))

                        instrumentMaster.cmdChannelAftertouch.clear()
                        instrumentMaster.cmdChannelAftertouch.addCommands(i.argument[1])

                        selectSendDestinationAndRatio(mainWidget.ui.midiChannelATSend, instrumentMaster.cmdChannelAftertouch,
                                                      mainWidget.ui.midiChannelATRatio, "pitch")

                        print("Setting polyphonic aftertouch to " + str(instrumentMaster.evChannelAftertouch))
                    case "pc":
                        instrumentMaster.evProgramChange = i.argument[1]
                        mainWidget.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Program change"))

                        print("Setting polyphonic aftertouch to " + str(instrumentMaster.evProgramChange))

            case "bchbn":
                for a in range(1, mainWidget.ui.comboBoxBaseNote.count()):
                    if int(mainWidget.ui.comboBoxBaseNote.itemData(a)) == int(i.argument[0]):
                        mainWidget.ui.comboBoxBaseNote.setCurrentIndex(a)
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

                widget.setPlainText(i.argument[1])
                stringModules[currentSerialModule].setCVCommand(i.argument[0], i.argument[1])
                mainWidget.updateCVData()

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
#    serialHandler.write("rqi:bowcontrolharmoniclist")
#    serialHandler.write("rqi:bowcontrolharmoniccount")

    serialHandler.write("rqi:bowharmonicseriescount")
    serialHandler.write("rqi:bowharmonicserieslist")
    serialHandler.write("rqi:bowharmonicseries")

    serialHandler.write("rqi:midieventhandler")
    serialHandler.write("rqi:bowcontrolharmonicbasenote")
    serialHandler.write("rqi:solenoidmaxforce")
    serialHandler.write("rqi:solenoidminforce")
    serialHandler.write("rqi:solenoidengageduration")
    serialHandler.write("rqi:bowactuatorcount")
    serialHandler.write("rqi:midiconfigurationcount")
    serialHandler.write("rqi:mrc")
    serialHandler.write("help")
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

# Finds the first destination command in commandList and selects it in the Combo Box given in comboBox
# Sets the slider given in ratio to the multiplier value used in combination with the string literal variable given in variable
def selectSendDestinationAndRatio(comboBox, commandList, ratio, variable):
    comboBox.blockSignals(True)
    ratio.blockSignals(True)

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
    ratio.blockSignals(False)

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
        self.serialThread.chartCommandSignal.connect(self.chartCommand)

        self.midiHandlerC = midihandler.MidiHandler(self.midiDataAvaliableSignal) #self.addToDebugWindow)
        self.midiHandlerC.updateMIDIInDevices(self.ui.comboBoxMIDILearnDevice)
        self.midiDataAvaliableSignal.connect(self.midiDataAvaliable)

        self.updatingFromModule = False

        self.timeStamper = self.debugTimedChart.timeStamper #timedChart.timeStamp()

    def addData(self, seriesID, value, inSeriesType): # min, max):
        self.debugTimedChart.addData(seriesID, value, inSeriesType) # min, max)
                #str(i.command + i.argument[0]) i.argument[1]
#        self.addData("adcr0", 5)

    def chartCommand(self, command):
        self.debugTimedChart.processCommand(command)

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
            serialHandler.write(tempText)
            print("sending " + str(tempText.encode()))
            mainWidget.ui.lineEditSend.clear()

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

        self.updateContinuousStringModuleData()

    def updateContinuousStringModuleData(self): 
        #freq = float(stringModules[currentShowingModule].stringFrequency)
        freq = stringModules[currentShowingModule].getCommandValue("psf")
        if not freq is None:
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

    def updateCVData(self):
        #offset, multiplier = equationParsingHelpers.getVariable(instrumentMaster.cmdNoteOn.getCommandAttribute("se", 0), "velocity")
        cl = stringModules[currentSerialModule].getCVCommandList(0)
        attr = cl.getCommandAttribute("bch",0)
        offset, multiplier = equationParsingHelpers.getVariable(attr, "value")
        pass

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
            serialHandler.write("debugprint:" + sender.reportType + ":" + out)

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

    def assignValueChanged(self, qtObject, command):
        qtObject.command = command
        qtObject.valueChanged.connect(self.basicChangedSignal)

    def basicChangedSignal(self, value):
        sender = self.sender()
        out = "m:" + str(currentShowingModule) + "," + sender.command + ":" + str(value)
        stringModules[currentShowingModule].setCommandValue(sender.command, float(value))
        serialHandler.write(out)

    def assignButtonPressCommandIssue(self, qtObject, command):
        qtObject.command = command
        qtObject.pressed.connect(self.buttonPressIssueCommand)
    def buttonPressIssueCommand(self):
        sender = self.sender()
        serialHandler.write(sender.command)

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
            serialHandler.write(send + "rqi:bhsl,rqi:bhs")
#        if (currentHarmonicListSelected < len(stringModules[currentSerialModule].harmonicData)):
#        mainWidget.ui.tableViewScale.setModel(tableTest.CustomTableModel(stringModules[currentSerialModule].harmonicData[currentHarmonicListSelected]))
#        mainWidget.ui.tableViewScale.model().dataChanged.connect(mainWidget.tableViewScaleDataChanged)
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
            serialHandler.write("bhss:'" + listID + "':" + str(harmonicList))
        except:
            messageBox("Error", "Error saving list")

    def pushButtonSaveNewHarmonicListPressed(self):
        listID = inputBox("List name", "List name")
        if listID is None:
            return
        newIndex = mainWidget.ui.comboBoxHarmonicList.count()
        serialHandler.write("bhss:'" + listID + "':" + str(newIndex))
        mainWidget.updateUIData()
    def pushButtonAddHarmonicListPressed(self):
        listID = inputBox("List name", "List name")
        if listID is None:
            return
        newIndex = mainWidget.ui.comboBoxHarmonicList.count()
        serialHandler.write("bhsl:" + str(newIndex) + ":'" + listID + "':1")
        mainWidget.updateUIData()
    def pushButtonAddHarmonicListFilePressed(self):
        pass
    def pushButtonRemoveHarmonicListPressed(self):
        try:
            harmonicList = stringModules[currentSerialModule].getCommandValue("bhs")
            serialHandler.write("bhsrm:" + str(harmonicList))
        except:
            messageBox("Error", "Error saving list")
        mainWidget.updateUIData()
    def updateHarmonicTable(self):
        mainWidget.ui.tableViewScale.setModel(tableTest.CustomTableModel(stringModules[currentSerialModule].harmonicData))
        mainWidget.ui.tableViewScale.model().dataChanged.connect(mainWidget.tableViewScaleDataChanged)


    def updateLineLimit(self):
        if (self.ui.checkBoxLimitLines.checkState() == Qt.CheckState.Checked):
            self.ui.plainTextEditSerialOutput.setMaximumBlockCount(self.ui.spinBoxLimitLines.value())
        else:
            self.ui.plainTextEditSerialOutput.setMaximumBlockCount(0)

    def checkBoxLimitLinesStateChanged(self):
        self.updateLineLimit()

    def spinBoxLimitLinesValueChanged(self, value):
        self.updateLineLimit()

#    def pushButtonSaveToModulePressed(self):
#        serialHandler.write("globalsaveallparameters")
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

    def selectMIDIDevice(self, Index):
        if mainWidget.ui.comboBoxMIDILearnDevice.currentIndex() == -1:
            return
        # midiIn = mido.open_input(mainWidget.ui.comboBoxMIDILearnDevice.currentText())
        self.midiHandlerC.connecToMIDIIn(mainWidget.ui.comboBoxMIDILearnDevice.currentText())

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
        widget.mouseReleaseFunction()
        #if widget is QSlider:
        if type(widget) == QSlider:
            QSlider.mouseReleaseEvent(widget, event)
        #super(MainWidget, self).mouseReleaseEvent(event)

    def assignMouseReleaseEvent(self, qtObject, function):
        qtObject.mouseReleaseEvent = lambda event: self.mouseReleaseEventIntermediate(event, qtObject)
        qtObject.mouseReleaseFunction = function

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
## Hiding until implemented
    mainWidget.ui.pushButtonAddHarmonicListFile.setVisible(False)

## Global commands
    mainWidget.ui.pushButtonConnectDisconnect.pressed.connect(mainWidget.connectDisconnect)
    #mainWidget.ui.pushButtonSaveToModule.pressed.connect(mainWidget.pushButtonSaveToModulePressed)
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonSaveToModule, "globalsaveallparameters")
    mainWidget.ui.pushButtonLoadFromModule.pressed.connect(mainWidget.pushButtonLoadFromModulePressed)
    mainWidget.ui.pushButtonReadSMData.pressed.connect(mainWidget.readSMData)
    mainWidget.ui.checkBoxContinuousSMData.toggled.connect(mainWidget.checkBoxContinuousSMDataToggled)
## Debug console
    mainWidget.assignFeedbackReportItem(mainWidget.ui.checkBoxFilterCommAck, "command")
    mainWidget.assignFeedbackReportItem(mainWidget.ui.checkBoxFilterDebug, "debug")
    mainWidget.assignFeedbackReportItem(mainWidget.ui.checkBoxFilterError, "error")
    mainWidget.assignFeedbackReportItem(mainWidget.ui.checkBoxFilterExpressionParser, "expressionparser")
    mainWidget.assignFeedbackReportItem(mainWidget.ui.checkBoxFilterHardware, "hardware")
    mainWidget.assignFeedbackReportItem(mainWidget.ui.checkBoxFilterInfoRequest, "inforequest")
    mainWidget.assignFeedbackReportItem(mainWidget.ui.checkBoxFilterPriority, "priority")
    mainWidget.assignFeedbackReportItem(mainWidget.ui.checkBoxFilterUSB, "usb")
    mainWidget.assignFeedbackReportItem(mainWidget.ui.checkBoxFilterUndefined, "undefined")
    mainWidget.assignFeedbackReportItem(mainWidget.ui.checkBoxFilterOutput, "output")

    mainWidget.ui.lineEditSend.editingFinished.connect(mainWidget.lineEditSend)
    mainWidget.ui.checkBoxDebugCursorFollow.toggled.connect(mainWidget.checkBoxDebugCursorFollowToggled)
    mainWidget.ui.pushButtonClear.pressed.connect(mainWidget.debugClear)
    mainWidget.ui.checkBoxLimitLines.stateChanged.connect(mainWidget.checkBoxLimitLinesStateChanged)
    mainWidget.ui.spinBoxLimitLines.valueChanged.connect(mainWidget.spinBoxLimitLinesValueChanged)

## Tab Module settings
    mainWidget.ui.comboBoxCurrentlySelectedModule.currentIndexChanged.connect(mainWidget.comboBoxCurrentSelectedModuleIndexChanged)

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxFundamentalFrequency, "bcu")
    mainWidget.ui.comboBoxBaseNote.currentIndexChanged.connect(mainWidget.comboBoxBaseNotePressed)
    mainWidget.ui.comboBoxFundamentalFrequency.currentIndexChanged.connect(mainWidget.comboBoxFundamentalFrequencyIndexChanged)
    mainWidget.ui.listWidgetTuningscheme.currentItemChanged.connect(mainWidget.tuningSchemeChanged)

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorMaxSpeed, "bmsx")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorMinSpeed, "bmsi")

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorPIDKp, "bpkp")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorPIDKi, "bpki")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorPIDKd, "bpkd")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorPIDie, "bpie")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorMaxError, "bpme")

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorVoltage, "bmv")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMotorTimeout, "bmt")
    #mainWidget.ui.pushButtonCalibrateMotorSpeed.pressed.connect(mainWidget.pushButtonCalibrateSpeedPressed)
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonCalibrateMotorSpeed, "bowcalibratespeed")

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMaxPressure, "bppx")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowMinPressure, "bppe")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxBowRestPosition, "bppr")
    #mainWidget.ui.pushButtonCalibratePressure.pressed.connect(mainWidget.pushButtonCalibratePressurePressed)
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonCalibratePressure, "bowcalibratepressure")

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxMuteFullMutePosition, "mfmp")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxMuteHalfMutePosition, "mhmp")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxMuteRestPosition, "mrp")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxMuteBackoff, "mbo")
    #mainWidget.ui.pushButtonCalibrateMute.pressed.connect(mainWidget.pushButtonCalibrateMutePressed)
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonCalibrateMute, "mutecalibrate")

    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonMuteFullTest, "mutefullmute:1")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonMuteHalfTest, "mutehalfmute:1")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonMuteRestTest, "muterest:1")

    mainWidget.ui.comboBoxHarmonicList.currentIndexChanged.connect(mainWidget.comboBoxHarmonicListCurrentIndexChanged)
    mainWidget.ui.pushButtonAddHarmonic.pressed.connect(mainWidget.pushButtonAddHarmonicPressed)
    mainWidget.ui.pushButtonRemoveHarmonic.pressed.connect(mainWidget.pushButtonRemoveHarmonicPressed)
    mainWidget.ui.pushButtonLoadHarmonicPreset.pressed.connect(mainWidget.pushButtonLoadHarmonicPresetPressed)
    mainWidget.ui.pushButtonSaveCurrentHarmonicList.pressed.connect(mainWidget.pushButtonSaveCurrentHarmonicListPressed)
    mainWidget.ui.pushButtonSaveNewHarmonicList.pressed.connect(mainWidget.pushButtonSaveNewHarmonicListPressed)
    mainWidget.ui.pushButtonAddHarmonicList.pressed.connect(mainWidget.pushButtonAddHarmonicListPressed)
    mainWidget.ui.pushButtonAddHarmonicListFile.pressed.connect(mainWidget.pushButtonAddHarmonicListFilePressed)
    mainWidget.ui.pushButtonRemoveHarmonicList.pressed.connect(mainWidget.pushButtonRemoveHarmonicListPressed)

    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxSolenoidMaxForce, "sxf")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxSolenoidMinForce, "sif")
    mainWidget.assignValueChanged(mainWidget.ui.doubleSpinBoxSolenoidEngageDuration, "sed")

    mainWidget.ui.pushButtonActuatorSave.pressed.connect(mainWidget.pushButtonActuatorSavePressed)
    mainWidget.ui.pushButtonActuatorLoad.pressed.connect(mainWidget.pushButtonActuatorLoadPressed)
    mainWidget.ui.pushButtonActuatorDelete.pressed.connect(mainWidget.pushButtonAcutatorDeletePreset)

    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonBowMaxPressureTest, "bowpressuremodifier:0,bowpressurebaseline:65535")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonBowEngagePressureTest, "bowpressuremodifier:0,bowpressurebaseline:0,bowpressureengage:1")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonBowRestPressureTest, "bowpressuremodifier:0,bowpressurebaseline:0,bowpressurerest:1")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonSolenoidMaxForceTest, "solenoidforcemultiplier:1,se:65535")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonSolenoidMinForceTest, "solenoidforcemultiplier:1,se:1")
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonEngageHammer, "se:65535")

## Tab Midi settings
    mainWidget.ui.comboBoxMidiChannel.currentIndexChanged.connect(mainWidget.comboBoxMidiChannelIndexChanged)

    #mainWidget.ui.pushButtonMidiRestoreDefaults.pressed.connect(mainWidget.pushButtonMidiRestoreDefaults)
    mainWidget.assignButtonPressCommandIssue(mainWidget.ui.pushButtonMidiRestoreDefaults, "mcfd")

    #mainWidget.ui.midiNoteOnVelToHammer.valueChanged.connect(mainWidget.cmdNoteOnUpdate)
#    mainWidget.ui.midiNoteOnVelToHammer.sliderReleased.connect(mainWidget.cmdNoteOnUpdate)
    mainWidget.assignMouseReleaseEvent(mainWidget.ui.midiNoteOnVelToHammer, mainWidget.cmdNoteOnUpdate)
# mainWidget.ui.midiNoteOnVelToHammer.mouseReleaseEvent = lambda event: mainWidget.mouseReleaseEventIntermediate(event, mainWidget.ui.midiNoteOnVelToHammer)

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

