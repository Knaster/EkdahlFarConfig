from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox

from ModuleSystem import ModuleCommand
from CommandSets import CommandSetModular
from commandparser import Derivedcommanditem

from general_helpers import messageBox, inputBox, find_item, remove_item
from GUICallbackSystem import GUICallbackSystem, GUICallback

class TabAdvanced(QObject):
    def __init__(self, mainWidget, serialHandler, commandSet:CommandSetModular, guiCallbackSystem:GUICallbackSystem):
        super().__init__()
        self.mainWidget = mainWidget
        self.serialHandler = serialHandler
        self.commandSet:CommandSetModular = commandSet
        self.ui = mainWidget.ui

        self.guiCallbackSystem = guiCallbackSystem
        self.guiCallbacks: list[GUICallback] = list()
        self.guiCallbacksActuatorNames: list[GUICallback] = list()

    def addGUICallbacks(self):
        self.guiCallbacks = [GUICallback(self.ui.doubleSpinBoxBowMotorMaxSpeed, "bw.pid.msx"),
                             GUICallback(self.ui.doubleSpinBoxBowMotorMinSpeed, "bw.pid.msi"),
                             GUICallback(self.ui.doubleSpinBoxBowMotorVoltage, "bw.dcm.vo"),
                             GUICallback(self.ui.doubleSpinBoxBowMotorPIDKp, "bw.pid.kp"),
                             GUICallback(self.ui.doubleSpinBoxBowMotorPIDKi, "bw.pid.ki"),
                             GUICallback(self.ui.doubleSpinBoxBowMotorPIDKd, "bw.pid.kd"),
                             GUICallback(self.ui.doubleSpinBoxBowMotorPIDie, "bw.pid.ie"),
                             GUICallback(self.ui.doubleSpinBoxBowMotorMaxError, "bw.pid.xe"),
                             GUICallback(self.ui.doubleSpinBoxBowMotorTimeout, "bw.mt"),
                             GUICallback(self.ui.pushButtonCalibrateMotorSpeed, "cbs"),

                             GUICallback(self.ui.doubleSpinBoxBowMaxPressure, "bw.bp.sp"),
                             GUICallback(self.ui.doubleSpinBoxBowMinPressure, "bw.bp.ep"),
                             GUICallback(self.ui.doubleSpinBoxBowRestPosition, "bw.bp.rp"),
                             GUICallback(None, "bw.bp.ah.c", dataCallbackFunction = self.dataChangedActuatorCount),
                             GUICallback(self.ui.comboBoxActuatorPreset, "bw.bp.ah.ac", force=True,
                                         dataCallbackFunction = self.dataChangedActuatorPreset, guiCallbackFunction = self.guiChangedActuatorPreset),

                             GUICallback(self.ui.doubleSpinBoxMuteFullMutePosition, "mu.fmp"),
                             GUICallback(self.ui.doubleSpinBoxMuteHalfMutePosition, "mu.hmp"),
                             GUICallback(self.ui.doubleSpinBoxMuteRestPosition, "mu.rp"),
                             GUICallback(self.ui.doubleSpinBoxMuteBackoff, "mu.bo"),

                             GUICallback(self.ui.doubleSpinBoxSolenoidMaxForce, "so.xf"),
                             GUICallback(self.ui.doubleSpinBoxSolenoidMinForce, "so.if"),
                             GUICallback(self.ui.doubleSpinBoxSolenoidEngageDuration, "so.ed"),

                             GUICallback(self.ui.spinBoxHarmonicShiftRange, "bw.hsh.sr"),

                             GUICallback(self.ui.pushButtonHomeBow, "bw.bp.hm"),
                             GUICallback(self.ui.pushButtonHomeMute, "mu.hm"),

                             GUICallback(None, "bw.bp.ah.a", dataCallbackFunction=self.dataChangedActuatorAdded),
                             GUICallback(None, "bw.bp.ah.rm", dataCallbackFunction=self.dataChangedActuatorRemoved),

                             GUICallback(self.ui.pushButtonMuteFullTest, "mu.fm:1"),
                             GUICallback(self.ui.pushButtonMuteHalfTest, "mu.hfm:1"),
                             GUICallback(self.ui.pushButtonMuteRestTest, "mu.rs:1"),
                             GUICallback(self.ui.pushButtonBowMaxPressureTest, "bw.bp.mo:0,bw.bp.ba:65535"),
                             GUICallback(self.ui.pushButtonBowEngagePressureTest, "bw.bp.mo:0,bw.bp.ba:65535,bw.bp.en:1"),
                             GUICallback(self.ui.pushButtonBowRestPressureTest, "bw.bp.mo:0,bw.bp.ba:65535,bw.bp.rs:1"),
                             GUICallback(self.ui.pushButtonSolenoidMaxForceTest, "so.fm:65535,so.en:65535"),
                             GUICallback(self.ui.pushButtonSolenoidMinForceTest, "so.fm:65535,so.en:1"),
                             GUICallback(self.ui.pushButtonEngageHammer, "so.en:65535"),
                             GUICallback(self.ui.pushButtonHammerDurationTest, "so.fm:65535,so.en:65535"),
                             GUICallback(self.ui.pushButtonHomeBow, "bw.bp.hm:1"),
                             GUICallback(self.ui.pushButtonResetAllSettings, "", guiCallbackFunction=self.resetAllSettings)]

        self.guiCallbackSystem.addGUICallbacks(self.guiCallbacks)

        self.guiCallbacksActuator = [GUICallback(None, "bw.bp.ah.ac.na", dataCallbackFunction = self.dataChangedActuatorName)]

        self.ui.pushButtonRestBow.pressed.connect(self.guiChangedRestBow)
        #self.ui.comboBoxActuatorPreset.currentIndexChanged.connect(self.guiChangedActuatorPreset)
        self.ui.pushButtonActuatorAdd.pressed.connect(self.guiChangedActuatorAdd)
        self.ui.pushButtonActuatorRemove.pressed.connect(self.guiChangedActuatorRemove)
        self.ui.pushButtonActuatorRename.pressed.connect(self.guiChangedActuatorRename)
        self.ui.pushButtonRestMute.pressed.connect(self.guiChangedRestMute)
        self.ui.pushButtonEngageHammer.pressed.connect(self.guiChangedEngageHammer)

    def updateWidget(self):
        self.guiCallbackSystem.setGUIObjectValueFromCallbacks(self.guiCallbacks)

    def dataChangedActuatorPreset(self, moduleCommand : ModuleCommand):
        if (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) > 0):
            newIndex = int(moduleCommand.arguments[0])
            self.ui.comboBoxActuatorPreset.setCurrentIndex(newIndex)
            self.guiCallbackSystem.addGUICallbacks(self.guiCallbacksActuator, regenerateModuleCommand = True)
            self.serialHandler.write("rqi:bw.bp.rp,rqi:bw.bp.sp,rqi:bw.bp.ep")

    def guiChangedActuatorPreset(self, index):
        #if (index == -1): return
        self.serialHandler.write("bw.bp.ah.ac[" + str(self.ui.comboBoxActuatorPreset.currentIndex()) + "]")

    def dataChangedActuatorCount(self, moduleCommand : ModuleCommand):
        if (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) > 0):
            self.ui.comboBoxActuatorPreset.clear()
            for i in range(0, int(moduleCommand.arguments[0])):
                self.guiCallbackSystem.findCallbackWithIndexAndAdd(i, "bw.bp.ah.ac", "na", self.dataChangedActuatorName,
                                                                   self.guiCallbacksActuatorNames, force=True)

                command, module = self.commandSet.getCommandAndModule("bw.bp.ah.ac[" + str(i) + "].na")
                if (command is not None) and (command.arguments is not None) and (len(command.arguments) > 0):
                    self.ui.comboBoxActuatorPreset.addItem(command.arguments[0])
                else:
                    self.ui.comboBoxActuatorPreset.addItem("--_--")
                    self.serialHandler.write("rqi:bw.bp.ah.ac[" + str(i) + "].na")
            command, module = self.commandSet.getCommandAndModule("bw.bp.ah.ac")
            self.ui.comboBoxActuatorPreset.setCurrentIndex(int(command.arguments[0]))

    def dataChangedActuatorAdded(self, moduleCommand:ModuleCommand):
        if (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) >= 1):
            index = int(moduleCommand.arguments[1])
            if (index == -1): return
            self.guiCallbackSystem.findCallbackWithIndexAndAdd(index, "bw.bp.ah.ac", "na", self.dataChangedActuatorName,
                                                               self.guiCallbacksActuatorNames)

    def dataChangedActuatorRemoved(self, moduleCommand:ModuleCommand):
        if (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) >= 1):
            index = int(moduleCommand.arguments[1])
            if (index == -1): return
            self.guiCallbackSystem.findCallbackWithIndexAndRemove(index, self.guiCallbacksActuatorNames)

    def dataChangedActuatorName(self, moduleCommand:ModuleCommand):
        index = moduleCommand.parent.getIndex()
        if index == -1: return
        if (moduleCommand.arguments is not None) and len(moduleCommand.arguments) > 0:
            name = moduleCommand.arguments[0]
        else:
            name = "[none]"
        self.ui.comboBoxActuatorPreset.setItemText(int(index), name)
        command, module = self.commandSet.getCommandAndModule("bw.bp.ah.ac")
        self.ui.comboBoxActuatorPreset.setCurrentIndex(int(command.arguments[0]))

    def guiChangedRestBow(self):
        self.serialHandler.write("bw.bp.rp:0,bw.bp.rs:1")

    def guiChangedActuatorAdd(self):
        name =  inputBox("New actuator name", "Actuator name")
        if name is None: return
        self.serialHandler.write("bw.bp.ah.a:" + name)

    def guiChangedActuatorRemove(self):
        comboIndex = self.ui.comboBoxActuatorPreset.currentIndex()
        if comboIndex == -1: return
        self.serialHandler.write("bw.bp.ah.rm:" + str(comboIndex))

    def guiChangedActuatorRename(self):
        index = self.ui.comboBoxActuatorPreset.currentIndex()
        if (index == -1): return
        listID = inputBox("New actuator name", "Actuator name")
        if listID is None: return
        if (find_item(self.ui.comboBoxActuatorPreset, listID) != -1):
            messageBox("Error", "Actuator already exists!")
            return
        self.serialHandler.write("bw.bp.ah.ac[" + str(index) + "].name:" + listID)

    def guiChangedRestMute(self):
        self.serialHandler.write("mu.rp:0,mu.rs:1")
        pass

    def guiChangedEngageHammer(self):
        self.serialHandler.write("so.en:65535")
        pass

    def resetAllSettings(self, anything):
        msgBox = QMessageBox.warning(self.mainWidget, "WHOOPS COMPLETE RESET",
                                     "This will reset ALL SETTINGS in your Ekdahl FAR and then restart the instrument, you sure?",
                                     buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     defaultButton=QMessageBox.StandardButton.No)
        if msgBox == QMessageBox.StandardButton.Yes:
            #saveAll = commandSets.getQualifiedShortCommand(CommandID.saveAllParameters)
            #reset = commandSets.getQualifiedShortCommand(CommandID.reset)
            self.serialHandler.write("sap,rap:1")
        pass
