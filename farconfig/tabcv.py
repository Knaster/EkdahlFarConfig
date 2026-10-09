from PySide6.QtCore import QObject, Qt, QTimer
from PySide6.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QListWidgetItem
import math

from GUICallbackSystem import GUICallbackSystem, GUICallback
from ModuleSystem import ModuleCommand
from CommandSets import CommandSetModular
from commandparser import Derivedcommandlist
from general_helpers import messageBox
import equationParsingHelpers

#from cveventhandling import CVEventHandler

class TabCV(QObject):
    def __init__(self, mainWidget, serialHandler, commandSet:CommandSetModular, guiCallbackSystem:GUICallbackSystem):
        super().__init__()
        self.mainWidget = mainWidget
        self.serialHandler = serialHandler
        self.commandSet:CommandSetModular = commandSet
        self.guiCallbackSystem = guiCallbackSystem
        self.ui = mainWidget.ui
        #self.cvEventHandler = CVEventHandler(self, serialHandler, commandSet, simpleFARHandler)

        self.guiCallbacks = [GUICallback(self.ui.plainTextEditCVHarmonicCommands, "cb.cbc[0].cm",
                                         guiCallbackFunction = self.guiChangedCVHarmonicTextEdit),
                             GUICallback(self.ui.dialCVHarmonic, "cb.cbc[0].va"),
                             GUICallback(None, "cb.cbc[0].cm", dataCallbackFunction = self.dataChangedCVHarmonic),
                             GUICallback(self.ui.dialCVHarmonicScale, "", guiCallbackFunction = self.guiChangedCVHarmonic),
                             GUICallback(self.ui.widgetCVHarmonicNoteOffset, "", guiCallbackFunction = self.guiChangedCVHarmonic),
                             GUICallback(self.ui.widgetCVHarmonicZero, "", guiCallbackFunction = self.guiChangedCVHarmonic),

                             GUICallback(self.ui.plainTextEditCVHarmonicShiftCommands, "cb.cbc[1].cm",
                                         guiCallbackFunction = self.guiChangedCVHarmonicShiftTextEdit),
                             GUICallback(self.ui.dialCVHarmonicShift, "cb.cbc[1].va"),
                             GUICallback(None, "cb.cbc[1].cm", dataCallbackFunction = self.dataChangedCVHarmonicShift),
                             GUICallback(self.ui.dialCVHarmonicShiftScale, "", guiCallbackFunction = self.guiChangedCVHarmonicShift),
                             GUICallback(self.ui.dialCVHarmonicShiftZero, "", guiCallbackFunction = self.guiChangedCVHarmonicShift),
                             GUICallback(self.ui.pushButtonCVHarmonicShiftZeroCalibrate, "",
                                         guiCallbackFunction = self.guiChangedCVHarmonicShiftZeroCalibrate),

                            GUICallback(self.ui.plainTextEditCVFineTuneCommands, "cb.cbc[2].cm",
                                        guiCallbackFunction = self.guiChangedCVFineTuneTextEdit),
                            GUICallback(None, "cb.cbc[2].cm", dataCallbackFunction = self.dataChangedCVFineTune),
                            GUICallback(self.ui.dialCVFineTuneCenter, "", guiCallbackFunction = self.guiChangedCVFineTune),
                            GUICallback(self.ui.pushButtonCVFinetuneCalibrate, "", guiCallbackFunction = self.guiChangedCVFineTuneCalibrate),

                            GUICallback(self.ui.plainTextEditCVPressureCommands, "cb.cbc[3].cm",
                                        guiCallbackFunction = self.guiChangedCVPressure),
                            GUICallback(self.ui.dialCVPressure, "cb.cbc[3].va"),

                            GUICallback(self.ui.plainTextEditCVMuteCommands, "cb.cbc[7].cm",
                                        guiCallbackFunction=self.guiChangedCVMute),
                            GUICallback(self.ui.dialCVMute, "cb.cbc[7].va"),

                            GUICallback(self.ui.plainTextEditCVHammerScaleCommands, "cb.cbc[6].cm",
                                        guiCallbackFunction=self.guiChangedCVHammerScale),
                            GUICallback(self.ui.dialCVHammerScale, "cb.cbc[6].va"),

                            GUICallback(self.ui.plainTextEditCVGateCommands, "cb.cbc[5].cm",
                                        guiCallbackFunction=self.guiChangedCVGateTextEdit),
                            GUICallback(self.ui.dialCVGate, "cb.cbc[5].va"),
                            GUICallback(None, "cb.cbc[5].cm", dataCallbackFunction = self.dataChangedCVGate),
                            GUICallback(self.ui.widgetCVGateThreshold, "", guiCallbackFunction = self.guiChangedCVGate),
                            GUICallback(self.ui.checkBoxCVGateEngage, "", guiCallbackFunction=self.guiChangedCVGate),
                            GUICallback(self.ui.checkBoxCVGatePowerMotor, "", guiCallbackFunction=self.guiChangedCVGate),
                            GUICallback(self.ui.checkBoxCVGateHold, "", guiCallbackFunction=self.guiChangedCVGate),

                            GUICallback(self.ui.plainTextEditCVHammerTriggerCommands, "cb.cbc[4].cm",
                                       guiCallbackFunction=self.guiChangedCVHammerTrigger),
                            GUICallback(self.ui.dialCVHammerTrigger, "cb.cbc[4].va")]

    def addGUICallbacks(self):
        self.guiCallbackSystem.addGUICallbacks(self.guiCallbacks)

    def updateWidget(self):
        #self.guiCallbackSystem.updatingFromGUI += 1
        self.guiCallbackSystem.setGUIObjectValueFromCallbacks(self.guiCallbacks)

##### Harmonic functions #####

    def guiChangedCVHarmonicTextEdit(self, anything):
        self.serialHandler.write("cb.cbc[0].cm:'" + self.ui.plainTextEditCVHarmonicCommands.text() + "'")

    def dataChangedCVHarmonic(self, moduleCommand:ModuleCommand):
        cl = Derivedcommandlist(moduleCommand.arguments[0])

        cmd = cl.getCommandAttribute("bw.hsh.ha", 0)
        if cmd == "": return
        result = equationParsingHelpers.extractZeroCoefficientOffset(cmd)

        cvScale = 1327.716667 * result["coefficient"]  # * multiplier
        offsetDiv = result["offset"] / 1327.716667
        noteOffset = round(offsetDiv)
        if (result["offset"] < 0):
            cvOffset = result["offset"] - (noteOffset * 1327.716667)
        else:
            cvOffset = result["offset"] - (noteOffset * 1327.716667)
        noteOffset = math.trunc(offsetDiv)

        cvZero = result["zeroPosition"]

        self.mainWidget.ui.dialCVHarmonicScale.setValue(cvScale)  # * 1000
        self.mainWidget.ui.widgetCVHarmonicNoteOffset.setValue(cvOffset)
        self.mainWidget.ui.widgetCVHarmonicZero.setValue(cvZero)

    def guiChangedCVHarmonic(self, anything):
        moduleCommand, module = self.commandSet.getCommandAndModule("cb.cbc[0].cm")
        cl = Derivedcommandlist(moduleCommand.arguments[0])

        cmd = cl.buildCommandString({"bw.hsh.ha"})
        if (cmd == "''") or (cmd == "\"\""): cmd = ""
        cvScale = str(1327.716667 / (self.ui.dialCVHarmonicScale.value()))  # / 1000
        cvOffset = str(self.ui.widgetCVHarmonicNoteOffset.value())  # + self.mainClass.dialCVHarmonicNoteOffset.value() * 1327.716667)
        cvZero = self.ui.widgetCVHarmonicZero.value()
        cmd += "bw.hsh.ha" + ":\"(value"
        if int(cvZero) >= 0:
            cmd += "+"
        cmd += str(cvZero) + ")/" + str(cvScale)
        if (cvOffset != 0): cmd += "+(" + str(cvOffset) + ")"
        cmd += "\""

        if cmd == "": return
        cmd = "cb.cbc[0].cm" + ":'" + cmd + "'"
        self.serialHandler.write(cmd)

##### Harmonic Shift functions #####

    def guiChangedCVHarmonicShiftTextEdit(self, anything):
        self.serialHandler.write("cb.cbc[1].cm:'" + self.ui.plainTextEditCVHarmonicShiftCommands.text() + "'")

    def dataChangedCVHarmonicShift(self, moduleCommand:ModuleCommand):
        cl = Derivedcommandlist(moduleCommand.arguments[0])

        cmd = cl.getCommandAttribute("bw.hsh.sh5", 0)
        if cmd == "": return
        result = equationParsingHelpers.extractZeroCoefficientOffset(cmd)

        cvScale = 2.425 / (1 / result["coefficient"])
        cvZero = (32767) + result["zeroPosition"]
        self.mainWidget.ui.dialCVHarmonicShiftScale.setValue(cvScale)  # * 1000
        self.mainWidget.ui.dialCVHarmonicShiftZero.setValue(cvZero)

    def guiChangedCVHarmonicShift(self, anything):
        moduleCommand, module = self.commandSet.getCommandAndModule("cb.cbc[1].cm")
        cl = Derivedcommandlist(moduleCommand.arguments[0])

        cmd = cl.buildCommandString({"bw.hsh.sh5"})
        cvScale = str(2.425 / (self.ui.dialCVHarmonicShiftScale.value()))  # / 1000
        cvOffset = -(32767 - self.ui.dialCVHarmonicShiftZero.value())
        cmd += "bw.hsh.sh5:\"deadband(value" + str(cvOffset) + ", 30)/" + str(cvScale) + "\""

        cmd = "cb.cbc[1].cm" + ":'" + cmd + "'"
        self.serialHandler.write(cmd)

    def guiChangedCVHarmonicShiftZeroCalibrate(self, anything):
        messageBox("Harmonic shift zero calibation", "Turn the 'Harmonic shift modulation'-knob all the way to the right, then turn it all the way to the left.\nPress OK when you are done")
        #setADC = self.commandSet.getQualifiedShortCommand(CommandID.controlBoxDataReturn)[0]
        #self.serialHandler.write("rqi:" + setADC + ":1")
        self.serialHandler.write("rqi:cb.cbc[1].va")
        QTimer.singleShot(1000, self.CVHarmonicShiftZeroCalibrateContinue)

    def CVHarmonicShiftZeroCalibrateContinue(self):
        #cv = self.simpleFARHandler.stringModules[0].getCVValue(1)
        moduleCommand, module = self.commandSet.getCommandAndModule("cb.cbc[1].va")
        if (moduleCommand is not None) and (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) > 0):
            cv = int(moduleCommand.arguments[0])
            self.mainClass.ui.dialCVHarmonicShiftZero.setValue(32767 - cv)
            #harmonicShift5 = self.commandSet.getQualifiedShortCommand(CommandID.bowHarmonicShift5)[0]
            self.serialHandler.write("bw.hsh.sh5:0")

##### Fine tune functions #####

    def guiChangedCVFineTuneTextEdit(self, anything):
        self.serialHandler.write("cb.cbc[2].cm:'" + self.ui.plainTextEditCVHarmonicShiftCommands.text() + "'")

    def dataChangedCVFineTune(self, moduleCommand:ModuleCommand):
        cl = Derivedcommandlist(moduleCommand.arguments[0])

        cmd = cl.getCommandAttribute("bw.hsh.sh", 0)
        if cmd == "": return
        cmd = equationParsingHelpers.removeFunction(cmd, "deadband")
        offset, multiplier = equationParsingHelpers.extractValueOffsetAndMultiplier(cmd)
        result = equationParsingHelpers.extractZeroCoefficientOffset(cmd)
        self.ui.dialCVFineTuneCenter.setValue(32767 + result["zeroPosition"])

    def guiChangedCVFineTune(self, anything):
        moduleCommand, module = self.commandSet.getCommandAndModule("cb.cbc[2].cm")
        cl = Derivedcommandlist(moduleCommand.arguments[0])

        cmd = cl.buildCommandString({ "bw.hsh.sh" })
        cmd += "bw.hsh.sh:\"deadband((value-" + str(32767 - self.ui.dialCVFineTuneCenter.value()) + ")*0.49064, 250)\""

        cmd = "cb.cbc[2].cm" + ":'" + cmd + "'"
        self.serialHandler.write(cmd)

    def guiChangedCVFineTuneCalibrate(self, anything):
        messageBox("CV fine tuning center calibration",
                   "Turn the 'Harmonic shift'-knob all the way to the left, then turn it to the center.\nPress OK when you are done")
        self.serialHandler.write("rqi:cb.cbc[2].va")
        QTimer.singleShot(1000, self.CVFinetuneCalibrateContinue)

    def CVFinetuneCalibrateContinue(self):
        #self.firstCv = self.simpleFARHandler.stringModules[0].getCVValue(2)
        moduleCommand, module = self.commandSet.getCommandAndModule("cb.cbc[2].va")
        if (moduleCommand is not None) and (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) > 0):
            self.firstCv = int(moduleCommand.arguments[0])
            messageBox("CV fine tuning center calibration",
                       "Now turn the 'Harmonic shift'-knob all the way to the right, then turn it to the center.\nPress OK when you are done")
            self.serialHandler.write("rqi:cb.cbc[2].va")
            QTimer.singleShot(1000, self.CVFinetuneCalibrateFinish)

    def CVFinetuneCalibrateFinish(self):
        moduleCommand, module = self.commandSet.getCommandAndModule("cb.cbc[2].va")
        if (moduleCommand is not None) and (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) > 0):
            offset = (int(moduleCommand.arguments[0]) - self.firstCv) / 2
            self.ui.dialCVFineTuneCenter.setValue(offset)
            self.serialHandler.write("bw.hsh.sh:0")

##### Pressure functions #####

    def guiChangedCVPressure(self, anything):
        self.serialHandler.write("cb.cbc[3].cm:'" + self.ui.plainTextEditCVPressureCommands.text() + "'")

##### Mute functions #####

    def guiChangedCVMute(self, anything):
        self.serialHandler.write("cb.cbc[7].cm:'" + self.ui.plainTextEditCVMuteCommands.text() + "'")

##### Hammer scale functions #####

    def guiChangedCVHammerScale(self, anything):
        self.serialHandler.write("cb.cbc[6].cm:'" + self.ui.plainTextEditCVHammerScaleCommands.text() + "'")

##### Gate functions #####

    def guiChangedCVGateTextEdit(self, anything):
        self.serialHandler.write("cb.cbc[5].cm:'" + self.ui.plainTextEditCVGateCommands.text() + "'")

    def guiChangedCVGate(self, anything):
        moduleCommand, module = self.commandSet.getCommandAndModule("cb.cbc[5].cm")
        cl = Derivedcommandlist(moduleCommand.arguments[0])

        cmd = cl.buildCommandString({"bw.dcm.ru", "bw.pe", "bw.sm", "bw.bp.en", "bw.bp.rs", "bw.bp.hd"})

        if cmd != "":
            cmd += ","
        if self.ui.checkBoxCVGatePowerMotor.isChecked():
            cmd += "bw.dcm.ru:bool(value-" + str(int(self.ui.widgetCVGateThreshold.value())) + "),bw.pe:1,bw.sm:0,"
        if self.ui.checkBoxCVGateEngage.isChecked():
            cmd += "bw.bp.en:bool(value-" + \
                   str(int(self.ui.widgetCVGateThreshold.value())) + "),bw.bp.rs:ibool(value-" + \
                   str(int(self.ui.widgetCVGateThreshold.value())) + "),"
        if self.ui.checkBoxCVGateHold.isChecked():
            cmd += "bw.bp.hd:ibool(value-" + str(int(self.ui.widgetCVGateThreshold.value())) + ")"

        cmd = "cb.cbc[5].cm" + ":'" + cmd + "'"
        self.serialHandler.write(cmd)

    def dataChangedCVGate(self, moduleCommand:ModuleCommand):
        cl = Derivedcommandlist(moduleCommand.arguments[0])

        cmd = cl.getCommandAttribute("bw.dcm.ru", 0)
        if cmd != "":
            self.ui.checkBoxCVGatePowerMotor.setCheckState(Qt.CheckState.Checked)
        else:
            self.ui.checkBoxCVGatePowerMotor.setCheckState(Qt.CheckState.Unchecked)

        threshold = 2000

        cmd = cl.getCommandAttribute("bw.bp.hd", 0)
        if cmd != "":
            self.ui.checkBoxCVGateHold.setCheckState(Qt.CheckState.Checked)
            threshold = abs(int(equationParsingHelpers.stripBoolIBool(cmd)))
        else:
            self.ui.checkBoxCVGateHold.setCheckState(Qt.CheckState.Unchecked)

        cmd = cl.getCommandAttribute("bw.bp.en", 0)
        if cmd != "":
            self.ui.checkBoxCVGateEngage.setCheckState(Qt.CheckState.Checked)
            threshold = abs(int(equationParsingHelpers.stripBoolIBool(cmd)))
        else:
            self.ui.checkBoxCVGateEngage.setCheckState(Qt.CheckState.Unchecked)

        self.ui.widgetCVGateThreshold.setValue(threshold)

    ##### Hammer trigger functions #####

    def guiChangedCVHammerTrigger(self, anything):
        self.serialHandler.write("cb.cbc[4].cm:'" + self.ui.plainTextEditCVHammerTriggerCommands.text() + "'")
