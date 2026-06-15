from commanddefinitions import CommandID
from PySide6.QtWidgets import QWidget, QDial, QDoubleSpinBox, QCheckBox
from PySide6.QtCore import QTimer, Qt
from general_helpers import messageBox
import equationParsingHelpers
import math
import averager

class CVEventHandler(QWidget):
    def __init__(self, mainClass, serialHandler, commandSet, simpleFARHandler):
        super().__init__()
        self.mainClass = mainClass
        self.serialHandler = serialHandler
        self.commandSet = commandSet
        self.simpleFARHandler = simpleFARHandler
        self.adcAverages = [averager.Averager() for i in range(8)]

    def handleControlBoxReturnData(self, channel, value):
        self.simpleFARHandler.stringModules[0].setCVValue(int(channel), int(value))
        self.mainClass.updateContinuousStringModuleData()
        self.adcAverages[int(channel)].addValue(value)
        self.updateAverages()

    def updateAverages(self):
        self.mainClass.ui.labelADC0Avg.setText(str(self.adcAverages[0].average))
        self.mainClass.ui.labelADC0Max.setText(str(self.adcAverages[0].max))
        self.mainClass.ui.labelADC0Min.setText(str(self.adcAverages[0].min))
        self.mainClass.ui.labelADC0Diff.setText(str(self.adcAverages[0].max - self.adcAverages[0].min))
        self.mainClass.ui.labelADC1Avg.setText(str(self.adcAverages[1].average))
        self.mainClass.ui.labelADC1Max.setText(str(self.adcAverages[1].max))
        self.mainClass.ui.labelADC1Min.setText(str(self.adcAverages[1].min))
        self.mainClass.ui.labelADC1Diff.setText(str(self.adcAverages[1].max - self.adcAverages[1].min))
        self.mainClass.ui.labelADC2Avg.setText(str(self.adcAverages[2].average))
        self.mainClass.ui.labelADC2Max.setText(str(self.adcAverages[2].max))
        self.mainClass.ui.labelADC2Min.setText(str(self.adcAverages[2].min))
        self.mainClass.ui.labelADC2Diff.setText(str(self.adcAverages[2].max - self.adcAverages[2].min))
        self.mainClass.ui.labelADC3Avg.setText(str(self.adcAverages[3].average))
        self.mainClass.ui.labelADC3Max.setText(str(self.adcAverages[3].max))
        self.mainClass.ui.labelADC3Min.setText(str(self.adcAverages[3].min))
        self.mainClass.ui.labelADC3Diff.setText(str(self.adcAverages[3].max - self.adcAverages[3].min))
        self.mainClass.ui.labelADC4Avg.setText(str(self.adcAverages[4].average))
        self.mainClass.ui.labelADC4Max.setText(str(self.adcAverages[4].max))
        self.mainClass.ui.labelADC4Min.setText(str(self.adcAverages[4].min))
        self.mainClass.ui.labelADC4Diff.setText(str(self.adcAverages[4].max - self.adcAverages[4].min))
        self.mainClass.ui.labelADC5Avg.setText(str(self.adcAverages[5].average))
        self.mainClass.ui.labelADC5Max.setText(str(self.adcAverages[5].max))
        self.mainClass.ui.labelADC5Min.setText(str(self.adcAverages[5].min))
        self.mainClass.ui.labelADC5Diff.setText(str(self.adcAverages[5].max - self.adcAverages[5].min))
        self.mainClass.ui.labelADC6Avg.setText(str(self.adcAverages[6].average))
        self.mainClass.ui.labelADC6Max.setText(str(self.adcAverages[6].max))
        self.mainClass.ui.labelADC6Min.setText(str(self.adcAverages[6].min))
        self.mainClass.ui.labelADC6Diff.setText(str(self.adcAverages[6].max - self.adcAverages[6].min))
        self.mainClass.ui.labelADC7Avg.setText(str(self.adcAverages[7].average))
        self.mainClass.ui.labelADC7Max.setText(str(self.adcAverages[7].max))
        self.mainClass.ui.labelADC7Min.setText(str(self.adcAverages[7].min))
        self.mainClass.ui.labelADC7Diff.setText(str(self.adcAverages[7].max - self.adcAverages[7].min))

    def averagesClear(self):
        for a in self.adcAverages:
            a.clear()
        self.updateAverages()

    def averagesTest(self):
        for i in range(8):
            self.serialHandler.write(self.commandSet.getQualifiedShortCommand(CommandID.controlBoxADCSettings) + ":" + str(i) + ":1:1:2:10")


    def handleControlBoxControlData(self, channel, commands):
        match int(channel):
            case 0:
                widget = self.mainClass.ui.plainTextEditCVHarmonicCommands
            case 1:
                widget = self.mainClass.ui.plainTextEditCVHarmonicShiftCommands
            case 2:
                widget = self.mainClass.ui.plainTextEditCVFineTuneCommands
            case 3:
                widget = self.mainClass.ui.plainTextEditCVPressureCommands
            case 4:
                widget = self.mainClass.ui.plainTextEditCVHammerTriggerCommands
            case 5:
                widget = self.mainClass.ui.plainTextEditCVGateCommands
            case 6:
                widget = self.mainClass.ui.plainTextEditCVHammerScaleCommands
            case 7:
                widget = self.mainClass.ui.plainTextEditCVMuteCommands
            case _:
                self.mainClass.messageBox("ADC Command error", "ADC Command error")
                return

        widget.setText(commands)
        self.simpleFARHandler.stringModules[0].setCVCommand(channel, commands)
        self.updateCVData()

    def updateCVData(self):
        for a in range(0, 7):
            cl = self.commandSet.currentCommandSet.CommandList(self.simpleFARHandler.stringModules[0].getCVCommand(a))
            if len(cl.commands) > 0:
                match a:
                    case 0:
                        cmd = cl.getCommandAttribute(self.commandSet.getQualifiedShortCommand(CommandID.bowHarmonicAdd)[0], 0)
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

                        self.mainClass.ui.dialCVHarmonicScale.setValue(cvScale)   # * 1000
                        self.mainClass.ui.widgetCVHarmonicNoteOffset.setValue(cvOffset)
                        self.mainClass.ui.widgetCVHarmonicZero.setValue(cvZero)
                    case 1:
                        cmd = cl.getCommandAttribute(self.commandSet.getQualifiedShortCommand(CommandID.bowHarmonicShift5)[0], 0)
                        if cmd == "":
                            break
                        try:
                            result = equationParsingHelpers.extractZeroCoefficientOffset(cmd)
                        except:
                            messageBox("Error", "Error in equation parser with string " + cmd)
                            break
                        cvScale = 2.425 / (1 / result["coefficient"])
                        cvZero = (32767) + result["zeroPosition"]
                        self.mainClass.ui.dialCVHarmonicShiftScale.setValue(cvScale)  # * 1000
                        self.mainClass.ui.dialCVHarmonicShiftZero.setValue(cvZero)
                    case 2:
                        cmd = cl.getCommandAttribute(self.commandSet.getQualifiedShortCommand(CommandID.bowHarmonicShift)[0], 0)
                        if cmd == "":
                            break
                        try:
                            cmd = equationParsingHelpers.removeFunction(cmd, "deadband")
                            offset, multiplier = equationParsingHelpers.extractValueOffsetAndMultiplier(cmd)
                            result = equationParsingHelpers.extractZeroCoefficientOffset(cmd)
                        except:
                            messageBox("Error", "Error in equation parser with string " + cmd)
                            break
                        self.mainClass.ui.dialCVFineTuneCenter.setValue(32767 + result["zeroPosition"])
                        pass
                    case 5:
                        # bmr:1,bpid:1,bcsm:0,bpe:bool(value-2000),bpr:ibool(value-2000),bph:ibool(value-2000)
                        cmd = cl.getCommandAttribute(self.commandSet.getQualifiedShortCommand(CommandID.motorRun)[0],0)
                        if cmd == "1":
                            self.mainClass.ui.checkBoxCVGatePowerMotor.setCheckState(Qt.CheckState.Checked)
                        else:
                            self.mainClass.ui.checkBoxCVGatePowerMotor.setCheckState(Qt.CheckState.Unchecked)

                        threshold = 2000

                        cmd = cl.getCommandAttribute(self.commandSet.getQualifiedShortCommand(CommandID.bowPressureHold)[0], 0)
                        if cmd != "":
                            self.mainClass.ui.checkBoxCVGateHold.setCheckState(Qt.CheckState.Checked)
                            threshold = abs(int(equationParsingHelpers.stripBoolIBool(cmd)))
                        else:
                            self.mainClass.ui.checkBoxCVGateHold.setCheckState(Qt.CheckState.Unchecked)

                        cmd = cl.getCommandAttribute(self.commandSet.getQualifiedShortCommand(CommandID.bowPressureEngage)[0], 0)
                        if cmd != "":
                            self.mainClass.ui.checkBoxCVGateEngage.setCheckState(Qt.CheckState.Checked)
                            threshold = abs(int(equationParsingHelpers.stripBoolIBool(cmd)))
                        else:
                            self.mainClass.ui.checkBoxCVGateEngage.setCheckState(Qt.CheckState.Unchecked)

                        self.mainClass.ui.widgetCVGateThreshold.setValue(threshold)
                pass
            else:
                pass
        pass

    def widgetCVMappingCallback(self, widget = None):
        if self.mainClass.updatingFromModule:
            return
        if not isinstance(widget, QWidget):
            widget = self.sender()
        cl = self.commandSet.currentCommandSet.CommandList(self.simpleFARHandler.stringModules[0].getCVCommand(int(widget.CVcontrol)))
        match widget.CVcontrol:
            case 0:
                cmd = cl.buildCommandString({self.commandSet.getQualifiedShortCommand(CommandID.bowHarmonicAdd)[0]})
                cvScale = str(1327.716667 / (self.mainClass.ui.dialCVHarmonicScale.value()))  #  / 1000
                cvOffset = str(self.mainClass.ui.widgetCVHarmonicNoteOffset.value()) # + self.mainClass.dialCVHarmonicNoteOffset.value() * 1327.716667)
                cvZero = self.mainClass.ui.widgetCVHarmonicZero.value()
                cmd += self.commandSet.getQualifiedShortCommand(CommandID.bowHarmonicAdd)[0] + ":(value"
                if int(cvZero) >= 0:
                    cmd += "+"
                cmd += str(cvZero) + ")/" + str(cvScale) + "+(" + str(cvOffset) + ")"
            case 1:
                cmd = cl.buildCommandString({self.commandSet.getQualifiedShortCommand(CommandID.bowHarmonicShift5)[0]})
                cvScale = str(2.425 / (self.mainClass.ui.dialCVHarmonicShiftScale.value()))    #  / 1000
                cvOffset = -(32767 - self.mainClass.ui.dialCVHarmonicShiftZero.value())
                cmd += self.commandSet.getQualifiedShortCommand(CommandID.bowHarmonicShift5)[0] + ":\"deadband(value" + str(cvOffset) + ", 30)/" + str(cvScale) + "\""
            case 2:
                cmd = cl.buildCommandString({self.commandSet.getQualifiedShortCommand(CommandID.bowHarmonicShift)[0]})
                cmd += (self.commandSet.getQualifiedShortCommand(CommandID.bowHarmonicShift)[0]+
                        ":\"deadband(value-" + str(32767 - self.mainClass.ui.dialCVFineTuneCenter.value()) + ", 400)*0.49064\"")
            case 5:

                cmd = cl.buildCommandString({ self.commandSet.getQualifiedShortCommand(CommandID.motorRun)[0],
                                              self.commandSet.getQualifiedShortCommand(CommandID.bowPIDEnable)[0],
                                              self.commandSet.getQualifiedShortCommand(CommandID.bowSpeedMode)[0],
                                              self.commandSet.getQualifiedShortCommand(CommandID.bowPressureEngage)[0],
                                              self.commandSet.getQualifiedShortCommand(CommandID.bowPressureRest)[0],
                                              self.commandSet.getQualifiedShortCommand(CommandID.bowPressureHold)[0] })

                #"bmr","bpid","bcsm","bpe","bpr","bph"
                if cmd != "":
                    cmd += ","
                if self.mainClass.ui.checkBoxCVGatePowerMotor.isChecked():
                    cmd += self.commandSet.getQualifiedShortCommand(CommandID.motorRun)[0] + ":1," + \
                           self.commandSet.getQualifiedShortCommand(CommandID.bowPIDEnable)[0] + ":1," + \
                           self.commandSet.getQualifiedShortCommand(CommandID.bowSpeedMode)[0] + ":0,"
                    #cmd += "bmr:1,bpid:1,bcsm:0,"
                if self.mainClass.ui.checkBoxCVGateEngage.isChecked():
                    cmd += self.commandSet.getQualifiedShortCommand(CommandID.bowPressureEngage)[0] + ":bool(value-" + \
                           str(self.mainClass.ui.widgetCVGateThreshold.value()) + "),bpr:ibool(value-" + \
                           str(self.mainClass.ui.widgetCVGateThreshold.value()) + "),"
#                    cmd += ("bpe:bool(value-" + str(self.mainClass.ui.widgetCVGateThreshold.value()) + "),bpr:ibool(value-" +
#                            str(self.mainClass.ui.widgetCVGateThreshold.value()) + "),")
                if self.mainClass.ui.checkBoxCVGateHold.isChecked():
                    cmd += self.commandSet.getQualifiedShortCommand(CommandID.bowPressureHold)[0] + ":ibool(value-" + \
                           str(self.mainClass.ui.widgetCVGateThreshold.value()) + ")"
                    #cmd += "bph:ibool(value-" + str(self.mainClass.ui.widgetCVGateThreshold.value()) + ")"
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
        setCommands = self.commandSet.getQualifiedShortCommand(CommandID.controlBoxControlData)[0]
        cmd = setCommands + ":" + str(widget.CVcontrol) + ":'" + cmd + "'"
        self.serialHandler.write(cmd)

    def connectCVMappingModifiers(self, CVcontrol, widgets):
        for widget in widgets:
            widget.CVcontrol = CVcontrol
            #widget.valueChanged.connect(self.widgetCVMappingCallback)
            if isinstance(widget, QDial):
                #self.mainClass.assignMouseReleaseEvent(widget, self.widgetCVMappingCallback)
                widget.sliderReleased.connect(self.widgetCVMappingCallback)
            if isinstance(widget, QDoubleSpinBox):
                widget.valueChanged.connect(self.widgetCVMappingCallback)
            if isinstance(widget, QCheckBox):
                widget.stateChanged.connect(self.widgetCVMappingCallback)

    def widgetCVTextCallback(self):
        widget = self.sender()
        cmd = widget.text()
        setCommands = self.commandSet.getQualifiedShortCommand(CommandID.controlBoxControlData)[0]
        cmd = setCommands + ":" + str (widget.CVcontrol) + ":'" + cmd + "'"
        self.serialHandler.write(cmd)

    def connectCVTextWidgets(self, CVcontrol, widget):
        widget.CVcontrol = CVcontrol
        widget.returnPressed.connect(self.widgetCVTextCallback)

    def CVFinetuneCalibrate(self):
        messageBox("CV fine tuning center calibration",
                   "Turn the 'Harmonic shift'-knob all the way to the left, then turn it to the center.\nPress OK when you are done")
        setADC = self.commandSet.getQualifiedShortCommand(CommandID.controlBoxDataReturn)[0]
        self.serialHandler.write("rqi:" + setADC + ":2")
        QTimer.singleShot(1000, self.CVFinetuneCalibrateContinue)

    def CVFinetuneCalibrateContinue(self):
        self.firstCv = self.simpleFARHandler.stringModules[0].getCVValue(2)
        messageBox("CV fine tuning center calibration",
                   "Now turn the 'Harmonic shift'-knob all the way to the right, then turn it to the center.\nPress OK when you are done")
        setADC = self.commandSet.getQualifiedShortCommand(CommandID.controlBoxDataReturn)[0]
        self.serialHandler.write("rqi:" + setADC + ":2")
        QTimer.singleShot(1000, self.CVFinetuneCalibrateFinish)

    def CVFinetuneCalibrateFinish(self):
        offset = (self.simpleFARHandler.stringModules[0].getCVValue(2) - self.firstCv) / 2
        self.mainClass.ui.dialCVFineTuneCenter.setValue(offset)
        harmonicShift = self.commandSet.getQualifiedShortCommand(CommandID.bowHarmonicShift)[0]
        self.serialHandler.write(harmonicShift + ":0")

    def CVHarmonicShiftZeroCalibrate(self):
        messageBox("Harmonic shift zero calibation", "Turn the 'Harmonic shift modulation'-knob all the way to the right, then turn it all the way to the left.\nPress OK when you are done")
        setADC = self.commandSet.getQualifiedShortCommand(CommandID.controlBoxDataReturn)[0]
        self.serialHandler.write("rqi:" + setADC + ":1")
        QTimer.singleShot(1000, self.CVHarmonicShiftZeroCalibrateContinue)

    def CVHarmonicShiftZeroCalibrateContinue(self):
        cv = self.simpleFARHandler.stringModules[0].getCVValue(1)
        self.mainClass.ui.dialCVHarmonicShiftZero.setValue(32767 - cv)
        harmonicShift5 = self.commandSet.getQualifiedShortCommand(CommandID.bowHarmonicShift5)[0]
        self.serialHandler.write(harmonicShift5 + ":0")
