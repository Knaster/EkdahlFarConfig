from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QListWidgetItem

from ModuleSystem import ModuleCommand
from CommandSets import CommandSetModular
from commandparser import Derivedcommandlist

from general_helpers import messageBox, inputBox, find_item, remove_item, find_item_with_data
from GUICallbackSystem import GUICallbackSystem, GUICallback

from midieventhandling import midiEventHandler as midiEventHandler, MIDIEvents, e_midiEvents

import equationParsingHelpers

class TabMIDI(QObject):
    def __init__(self, mainWidget, serialHandler, commandSet:CommandSetModular, guiCallbackSystem:GUICallbackSystem):
        super().__init__()
        self.mainWidget = mainWidget
        self.serialHandler = serialHandler
        self.commandSet:CommandSetModular = commandSet
        self.guiCallbackSystem = guiCallbackSystem
        self.ui = mainWidget.ui
        self.midiEventHandler = midiEventHandler(self, serialHandler, commandSet, guiCallbackSystem)

        self.guiCallbacksConfig = [GUICallback(self.ui.pushButtonConfigurationName, "mcf.mc.na",
                                               guiCallbackFunction=self.guiChangedConfigurationName),
                                   GUICallback(self.ui.pushButtonMidiRestoreDefaults, "mcf.mc.d",
                                               guiCallbackFunction=self.guiChangedMidiRestoreDefaults, dataCallbackFunction=self.dataChangedMIDIRestoreDefaults),
                                   GUICallback(self.ui.comboBoxMidiChannel, "mcf.mc.rc", dataCallbackFunction = self.dataChangedMIDIChannel,
                                               guiCallbackFunction = self.guiChangedMIDIChannel),
                                   GUICallback(self.ui.midiPolyATSend, "mcf.mc.pat",
                                               guiCallbackFunction=self.midiEventHandler.guiChangedRatioDestination,
                                               dataCallbackFunction=self.dataChangedPATCommands),
                                   GUICallback(self.ui.midiPolyATRatio, "mcf.mc.pat",
                                               guiCallbackFunction=self.midiEventHandler.guiChangedRatioDestination,
                                               dataCallbackFunction = GUICallback.SKIP_CALLBACK),
                                   GUICallback(self.ui.midiChannelATSend, "mcf.mc.cat",
                                               guiCallbackFunction=self.midiEventHandler.guiChangedRatioDestination,
                                               dataCallbackFunction=self.dataChangedCATCommands),
                                   GUICallback(self.ui.midiChannelATRatio, "mcf.mc.cat",
                                               guiCallbackFunction=self.midiEventHandler.guiChangedRatioDestination,
                                               dataCallbackFunction = GUICallback.SKIP_CALLBACK),
                                   GUICallback(self.ui.midiPitchbendSend, "mcf.mc.pb",
                                               guiCallbackFunction = self.midiEventHandler.guiChangedRatioDestination,
                                               dataCallbackFunction = GUICallback.SKIP_CALLBACK),
                                   GUICallback(self.ui.midiPitchbendRatio, "mcf.mc.pb",
                                               guiCallbackFunction=self.midiEventHandler.guiChangedRatioDestination,
                                               dataCallbackFunction = GUICallback.SKIP_CALLBACK),
                                   GUICallback(None, "mcf.mc.non",
                                               dataCallbackFunction = self.dataChangedNoteOnCommands),
                                   GUICallback(None, "mcf.mc.nof",
                                               dataCallbackFunction=self.dataChangedNoteOffCommands),
                                   GUICallback(None, "mcf.mc.pb",
                                               dataCallbackFunction=self.dataChangedPBCommands),
                                   GUICallback(None, "mcf.mc.ccc",
                                               dataCallbackFunction=self.dataChangedCCCommands),
                                   GUICallback(self.ui.midiNoteOnVelToHammer, "mcf.mc.non",
                                               guiCallbackFunction = self.guiChangedNoteOn,
                                               dataCallbackFunction = GUICallback.SKIP_CALLBACK),
                                   GUICallback(self.ui.midiNoteOnHammerStaccato, "mcf.mc.non",
                                               guiCallbackFunction = self.guiChangedNoteOn,
                                               dataCallbackFunction = GUICallback.SKIP_CALLBACK),
                                   GUICallback(self.ui.midiNoteOnSendMuteRest, "mcf.mc.non",
                                               guiCallbackFunction = self.guiChangedNoteOn,
                                               dataCallbackFunction = GUICallback.SKIP_CALLBACK),
                                   GUICallback(self.ui.midiNoteOffSendFullMute, "mcf.mc.nof",
                                               guiCallbackFunction = self.guiChangedNoteOff,
                                               dataCallbackFunction = GUICallback.SKIP_CALLBACK),
                                   GUICallback(self.ui.midiNoteOffMotorOff, "mcf.mc.nof",
                                               guiCallbackFunction = self.guiChangedNoteOff,
                                               dataCallbackFunction = GUICallback.SKIP_CALLBACK),
                                   GUICallback(self.ui.listWidgetMidiEvents, "",
                                               guiCallbackFunction=self.midiEventHandler.updateTextForSelectedListItem),
                                   GUICallback(self.ui.lineEditMidiEventCommand, "", guiCallbackFunction=self.guiChangedMidiEventCommand,),
                                   GUICallback(self.ui.pushButtonCCAdd, "", guiCallbackFunction=self.guiChangedAddCC),
                                   GUICallback(None, "mcf.mc.ac", dataCallbackFunction=self.dataChangedAddCC),
                                   GUICallback(self.ui.pushButtonCCRemove, "", guiCallbackFunction=self.guiChangedRemoveCC),
                                   GUICallback(None, "mcf.mc.rmc", dataCallbackFunction=self.dataChangedRemoveCC),
                                   GUICallback(self.ui.midiSustainSend, "", guiCallbackFunction = self.guiChangedSustainDestination),
                                   GUICallback(self.ui.midiSustainInvert, "", guiCallbackFunction = self.guiChangedSustainDestination)]

        self.guiCallbacksSustain = [GUICallback(self.ui.midiSustainInvert, "mcf.mc.cc",
                                                guiCallbackFunction=self.midiEventHandler.guiChangedRatioDestination),
                                    GUICallback(self.ui.midiSustainSend, "mcf.mc.cat",
                                                guiCallbackFunction=self.midiEventHandler.guiChangedRatioDestination)]

        self.guiCallbacksMidiConfigurationNames: list[GUICallback] = list()
        self.guiCallbacksCCNumber : list[GUICallback] = list()

    def addGUICallbacks(self):
        self.guiCallbacks = [GUICallback(self.ui.comboBoxConfiguration, "mcf.mc", dataCallbackFunction = self.dataChangedMIDIConfiguration,
                                         guiCallbackFunction = self.guiChangedMIDIConfiguration),
                             GUICallback(None, "mcf.c", dataCallbackFunction = self.dataChangedMIDIConfigurationCount),
                             GUICallback(self.ui.pushButtonConfigurationAdd, "mcf.a", guiCallbackFunction = self.guiChangedAddConfiguration,
                                         dataCallbackFunction = self.dataChangedAddConfiguration),
                             GUICallback(self.ui.pushButtonConfigurationRemove, "mcf.rm", guiCallbackFunction = self.guiChangedRemoveConfiguration,
                                         dataCallbackFunction = self.dataChangedRemoveConfiguration)]

        self.guiCallbackSystem.addGUICallbacks(self.guiCallbacks)

        self.midiEventHandler.populateComboBoxSendByte(self.ui.midiPitchbendSend)
        self.midiEventHandler.populateComboBoxSendByte(self.ui.midiPolyATSend)
        self.midiEventHandler.populateComboBoxSendByte(self.ui.midiChannelATSend)
        self.midiEventHandler.populateComboBoxSendBinary(self.ui.midiSustainSend)

    def updateWidget(self):
        self.guiCallbackSystem.updatingFromGUI += 1
        self.ui.listWidgetMidiEvents.clear()
        for event in MIDIEvents.values():
            item = QListWidgetItem(event.name)
            self.ui.listWidgetMidiEvents.addItem(item)

        self.guiCallbackSystem.setGUIObjectValueFromCallbacks(self.guiCallbacks)
        self.setEventHandlersToCurrentConfiguration()
        self.guiCallbackSystem.updatingFromGUI -= 1
        pass

    # Global callbacks
    def setEventHandlersToCurrentConfiguration(self):
        #self.guiCallbackSystem.removeGUICallbacks()
        self.guiCallbackSystem.addGUICallbacks(self.guiCallbacksConfig, regenerateModuleCommand = True)
        self.guiCallbackSystem.setGUIObjectValueFromCallbacks(self.guiCallbacksConfig)

    def dataChangedMIDIConfigurationCount(self, moduleCommand:ModuleCommand):
        if (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) > 0):
            self.ui.comboBoxConfiguration.clear()
            for i in range(0, int(moduleCommand.arguments[0])):
                self.guiCallbackSystem.findCallbackWithIndexAndAdd(i, "mcf.mc", "na", self.dataChangedConfigurationName,
                                                                   self.guiCallbacksMidiConfigurationNames, force = True)

                command, module = self.commandSet.getCommandAndModule("mcf.mc[" + str(i) + "].na")
                if (command is not None) and (command.arguments is not None):
                    self.ui.comboBoxConfiguration.addItem(command.arguments[0])
                else:
                    self.ui.comboBoxConfiguration.addItem("--_--")
                    self.serialHandler.write("rqi:mcf.mc[" + str(i) + "].na")
            command, module = self.commandSet.getCommandAndModule("mcf.mc")
            self.ui.comboBoxConfiguration.setCurrentIndex(int(command.arguments[0]))

    def dataChangedMIDIConfiguration(self, moduleCommand:ModuleCommand):
        if (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) > 0):
            newIndex = int(moduleCommand.arguments[0])
            self.ui.comboBoxConfiguration.setCurrentIndex(newIndex)
            self.ui.listWidgetMidiEvents.clear()
            for event in MIDIEvents.values():
                item = QListWidgetItem(event.name)
                self.ui.listWidgetMidiEvents.addItem(item)
            self.setEventHandlersToCurrentConfiguration()

    def guiChangedMIDIConfiguration(self, index):
        if self.guiCallbackSystem.updatingFromModule > 0: return
        self.serialHandler.write("mcf.mc[" + str(self.ui.comboBoxConfiguration.currentIndex()) + "]")

    def guiChangedAddConfiguration(self, data):
        defText = self.ui.comboBoxConfiguration.currentText()
        text, ok = QInputDialog().getText(self.mainWidget, "Configuration name","Configuration name:", QLineEdit.Normal, defText)
        if ok and text:
            if (find_item(self.ui.comboBoxConfiguration, text) != -1):
                messageBox("Error", "Name already exists!")
                return
            #commandSets.addMidiConfiguration(self, self.serialHandler, simpleFARHandler, text)
            self.serialHandler.write("mcf.a:" + text)

    def dataChangedAddConfiguration(self, moduleCommand:ModuleCommand):
        if (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) > 1):
            index = int(moduleCommand.arguments[1])
            if (index == -1): return
            self.guiCallbackSystem.findCallbackWithIndexAndAdd(index, "mcf.mc", "na", self.dataChangedConfigurationName,
                                                           self.guiCallbacksMidiConfigurationNames)

    def guiChangedRemoveConfiguration(self, data):
        config = int(self.ui.comboBoxConfiguration.currentIndex())
        if (config < 0) or (self.ui.comboBoxConfiguration.count() == 0):
            return
        #commandSets.removeMidiConfiguration(self, serialHandler, simpleFARHandler, config)
        self.serialHandler.write("mcf.rm:" + str(config))

    def dataChangedRemoveConfiguration(self, moduleCommand:ModuleCommand):
        if moduleCommand.arguments is not None and len(moduleCommand.arguments) > 1:
            index = int(moduleCommand.arguments[1])
            if (index == -1): return
            self.guiCallbackSystem.findCallbackWithIndexAndRemove(index, self.guiCallbacksMidiConfigurationNames)

    def dataChangedConfigurationName(self, moduleCommand:ModuleCommand):
        if moduleCommand.arguments is not None and len(moduleCommand.arguments) > 0:
            index = moduleCommand.parent.getIndex()
            if index == -1: return
            self.ui.comboBoxConfiguration.setItemText(int(index), moduleCommand.arguments[0])
            command, module = self.commandSet.getCommandAndModule("mcf.mc")
            if (command is not None) and (command.arguments is not None) and (len(command.arguments) > 0):
                self.ui.comboBoxConfiguration.setCurrentIndex(int(command.arguments[0]))

    def guiChangedConfigurationName(self, anything):
        defText = self.ui.comboBoxConfiguration.currentText()
        text, ok = QInputDialog().getText(self.mainWidget, "Configuration name",
                                          "Configuration name:", QLineEdit.Normal, defText)
        conf = self.ui.comboBoxConfiguration.currentIndex()
        if ok and text and (conf > -1):
            self.serialHandler.write("mcf.mc.na:" + str(text))
            self.ui.comboBoxConfiguration.setItemText(conf, text)

    def guiChangedMidiRestoreDefaults(self, anything):
        msgBox = QMessageBox.warning(self.mainWidget, "RESET MIDICONFIGURATION",
                                     "This will reset ALL MIDI SETTINGS in the current configuration, you sure?",
                                     buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     defaultButton=QMessageBox.StandardButton.No)
        if msgBox == QMessageBox.StandardButton.Yes:
            self.serialHandler.write("mcf.mc.d:1")
        pass

    def dataChangedMIDIRestoreDefaults(self, moduleCommand:ModuleCommand):
        if moduleCommand.arguments is not None and len(moduleCommand.arguments) > 0:
            if moduleCommand.arguments[1] == "1":
                self.updateWidget()

    def guiChangedMidiEventCommand(self, moduleCommand:ModuleCommand):
        if self.ui.listWidgetMidiEvents.currentItem() == None:
            return
        commandSelected = self.ui.listWidgetMidiEvents.currentItem().text()
        commandSequence = self.ui.lineEditMidiEventCommand.text()

        command = ""
        if commandSelected[:2] == "CC":
            #cc = int(commandSelected[3:])
            ccIndex = self.ui.listWidgetMidiEvents.currentItem().data(Qt.ItemDataRole.UserRole)
            if ccIndex is not None:
                command += "mcf.mc.cc[" + str(ccIndex) + "].cm"
        else:
            for event in MIDIEvents.values():
                if event.name == commandSelected:
                    command = event.command
                    break
        if command == "":
            return

        serialString = command + ":\"" + commandSequence + "\""
        self.serialHandler.write(serialString)

    def addCCNumberChangedCallback(self, index:str):
        commandString = "mcf.mc.cc[" + index + "].cl"
        for guiCallback in self.guiCallbacksCCNumber:
            if (guiCallback.commandString == commandString):
                return

        guiCallback = GUICallback(None, commandString, dataCallbackFunction=self.dataChangedCCNumber)
        self.guiCallbacksCCNumber.append(guiCallback)
        self.guiCallbackSystem.addGUICallback(guiCallback)

    def removeCCNumberChangedCallback(self, index:str):
        commandString = "mcf.mc.cc[" + index + "].cl"
        for guiCallback in self.guiCallbacksCCNumber:
            if (guiCallback.commandString == commandString):
                self.guiCallbackSystem.removeGUICallback(guiCallback)
                self.guiCallbacksCCNumber.remove(guiCallback)

    def dataChangedCCCommands(self, moduleCommand:ModuleCommand):
        for i in range(0, int(moduleCommand.arguments[0])):
            command, module = self.commandSet.getCommandAndModule("mcf.mc.cc[" + str(i) + "].cl")

            listItem = QListWidgetItem()
            listItem.setData(Qt.ItemDataRole.UserRole, str(i))

            itemIndex = find_item_with_data(self.ui.listWidgetMidiEvents, str(i))

            if (command.arguments is None or len(command.arguments) == 0):
                if (itemIndex == -1):
                    listItem.setText("CC [UNKNOWN]")
                    self.ui.listWidgetMidiEvents.addItem(listItem)
                    self.addCCNumberChangedCallback(str(i))
            else:
                cc = command.arguments[0]
                if (itemIndex == -1):
                    listItem.setText("CC " + str(cc))
                    self.ui.listWidgetMidiEvents.addItem(listItem)
                else:
                    self.ui.listWidgetMidiEvents.item(itemIndex).setText("CC " + str(cc))
                if int(cc) == 64:
                    self.dataChangedSustainDestination()

    def dataChangedCCNumber(self, moduleCommand:ModuleCommand):
        if (moduleCommand.arguments is not None and len(moduleCommand.arguments) > 0):
            i = moduleCommand.parent.getIndex()
            if (i < 0): return
            itemIndex = find_item_with_data(self.ui.listWidgetMidiEvents, str(i))
            if (itemIndex == -1): return
            self.ui.listWidgetMidiEvents.item(itemIndex).setText("CC " + str(moduleCommand.arguments[0]))
        pass

    def guiChangedAddCC(self, anything):
        cc, ok = QInputDialog.getInt(self.mainWidget, "CC Number", "CC Number")
        if ok and (cc > -1 and cc < 128):
            index = self.ui.listWidgetMidiEvents.findItems("CC " + str(cc), Qt.MatchFlag.MatchExactly)
            if (len(index) != 0):
                messageBox("Error", "Event already exists!")
                return
            self.serialHandler.write("mcf.mc.ac:" + str(cc) + ":''")

    def dataChangedAddCC(self, moduleCommand:ModuleCommand):
        if (moduleCommand.arguments is not None and len(moduleCommand.arguments) > 0):
            index = moduleCommand.arguments[1]
            moduleCommand, module = self.commandSet.getCommandAndModule("mcf.mc.cc[" + index + "].cl")
            if (moduleCommand is not None) and (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) > 0):
                cc = moduleCommand.arguments[0]
            else:
                cc = "CC [UNKNOWN]"

            if find_item_with_data(self.ui.listWidgetMidiEvents, str(index)) != -1:
                return

            self.addCCNumberChangedCallback(index)

            listItem = QListWidgetItem("CC " + str(cc))
            listItem.setData(Qt.ItemDataRole.UserRole, index)
            self.ui.listWidgetMidiEvents.addItem(listItem)

    def guiChangedRemoveCC(self, anything):
        if (self.ui.listWidgetMidiEvents.currentIndex() == -1):
            return
        if (self.ui.listWidgetMidiEvents.currentItem().text()[0:2] != "CC"):
            return
        text = self.ui.listWidgetMidiEvents.currentItem().text()
        text = text[3:len(text)]
        self.serialHandler.write("mcf.mc.rmc:" + text)

    def dataChangedRemoveCC(self, moduleCommand:ModuleCommand):
        if (moduleCommand.arguments is not None and len(moduleCommand.arguments) > 1):
            index = moduleCommand.arguments[1]
            for i in range(0, self.ui.listWidgetMidiEvents.count()):
                item = self.ui.listWidgetMidiEvents.item(i)
                if (item.data(Qt.ItemDataRole.UserRole) == index):
                    self.removeCCNumberChangedCallback(index)
                    self.ui.listWidgetMidiEvents.takeItem(i)
                    return
            pass

    def dataChangedMIDIChannel(self, moduleCommand:ModuleCommand):
        if moduleCommand.arguments is not None and len(moduleCommand.arguments) > 0:
            value = int(moduleCommand.arguments[0])
            if value > 16:
                value = 0
            self.ui.comboBoxMidiChannel.setCurrentIndex(value)

    def guiChangedMIDIChannel(self, index):
        if (index == 0):
            index = 16
        else:
            index -= 1
        self.serialHandler.write("mcf.mc.rc:" + str(index))
        pass

    def guiChangedNoteOn(self, widget=None):
        #solenoidEngage = commandSets.getQualifiedShortCommand(CommandID.solenoidEngage, None, True)[0]
        #muteRest = commandSets.getQualifiedShortCommand(CommandID.muteRest, None, True)[0]
        #
        #currentConfig = simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect)
        #mapCmd = commandSets.getQualifiedShortCommand(CommandID.midiConfigurationData, [currentConfig])[0]
        #
        #cl = commandSets.currentCommandSet.CommandList(simpleFARHandler.instrumentMaster.evNoteOn)

        solenoidEngage = "so.en"
        muteRest = "mu.rs"

        moduleCommand, module = self.commandSet.getCommandAndModule("mcf.mc.non")
        if (moduleCommand is None):
            return
        cl = Derivedcommandlist(moduleCommand.arguments[0])
        cmd = cl.buildCommandString({solenoidEngage, muteRest})

        if self.ui.midiNoteOnVelToHammer.value() > 0:
            cmd += "," + solenoidEngage + ":(velocity*" + str(self.ui.midiNoteOnVelToHammer.value()) + ")"
            if self.ui.midiNoteOnHammerStaccato.checkState() == Qt.CheckState.Checked:
                cmd += "*(1-notecount)"
        if self.ui.midiNoteOnSendMuteRest.checkState() == Qt.CheckState.Checked:
            cmd += "," + muteRest + ":1"
        self.serialHandler.write("mcf.mc.non:\"" + cmd + "\"")

    def guiChangedNoteOff(self, anything):
        #muteFull = commandSets.getQualifiedShortCommand(CommandID.muteFullMute, None, True)[0]
        #motorRun = commandSets.getQualifiedShortCommand(CommandID.motorRun, None, True)[0]

        #currentConfig = simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect)
        #mapCmd = commandSets.getQualifiedShortCommand(CommandID.midiConfigurationData, [currentConfig])[0]

        #cl = commandSets.currentCommandSet.CommandList(simpleFARHandler.instrumentMaster.evNoteOff)
        muteFull = "mu.fm"
        motorRun = "bw.dcm.ru"
        moduleCommand, module = self.commandSet.getCommandAndModule("mcf.mc.nof")
        if (moduleCommand is None):
            return
        cl = Derivedcommandlist(moduleCommand.arguments[0])
        cmd = cl.buildCommandString({muteFull, motorRun})

        if self.ui.midiNoteOffSendFullMute.checkState() == Qt.CheckState.Checked:
            cmd += "," + muteFull + ":1"
        if self.ui.midiNoteOffMotorOff.checkState() == Qt.CheckState.Checked:
            cmd += "," + motorRun + ":0"
        #serialString = cmd + ":noteoff:\"" + cmd + "\""
        #serialHandler.write(serialString)
        #self.updateUIData()
        self.serialHandler.write("mcf.mc.nof:\"" + cmd + "\"")

    def dataChangedNoteOnCommands(self, moduleCommand:ModuleCommand):
        if (find_item(self.ui.listWidgetMidiEvents, MIDIEvents[e_midiEvents.NoteOn].name) == -1):
            self.ui.listWidgetMidiEvents.addItem(QListWidgetItem(MIDIEvents[e_midiEvents.NoteOn].name))

        commandList = Derivedcommandlist(moduleCommand.arguments[0])
        seCmd = "so.en"

        offset, multiplier = equationParsingHelpers.getVariable(commandList.getCommandAttribute(seCmd, 0), "velocity")
        self.ui.midiNoteOnVelToHammer.setValue(multiplier)

        if equationParsingHelpers.isVariableInEquation(commandList.getCommandAttribute(seCmd, 0), "notecount"):
            self.ui.midiNoteOnHammerStaccato.setChecked(True)
        else:
            self.ui.midiNoteOnHammerStaccato.setChecked(False)

        if commandList.getCommandAttribute("mu.rs", 0) != "":
            self.ui.midiNoteOnSendMuteRest.setChecked(True)
        else:
            self.ui.midiNoteOnSendMuteRest.setChecked(False)

    def dataChangedNoteOffCommands(self, moduleCommand:ModuleCommand):
        if (find_item(self.ui.listWidgetMidiEvents, MIDIEvents[e_midiEvents.NoteOff].name) == -1):
            self.ui.listWidgetMidiEvents.addItem(QListWidgetItem(MIDIEvents[e_midiEvents.NoteOff].name))

        commandList = Derivedcommandlist(moduleCommand.arguments[0])

        mfmCmd = commandList.getCommandAttribute("mu.fm", 0)
        if (mfmCmd != ""):
            self.ui.midiNoteOffSendFullMute.setChecked(True)
        else:
            self.ui.midiNoteOffSendFullMute.setChecked(False)

        bmrCmd = commandList.getCommandAttribute("bw.dcm.ru", 0)
        if (bmrCmd != ""):
            self.ui.midiNoteOffMotorOff.setChecked(True)
        else:
            self.ui.midiNoteOffMotorOff.setChecked(False)

    def dataChangedPATCommands(self, moduleCommand:ModuleCommand):
        if (find_item(self.ui.listWidgetMidiEvents, MIDIEvents[e_midiEvents.PolyAT].name) == -1):
            self.ui.listWidgetMidiEvents.addItem(QListWidgetItem(MIDIEvents[e_midiEvents.PolyAT].name))
        commands = Derivedcommandlist(moduleCommand.arguments[0])
        self.selectSendDestinationAndRatio(self.ui.midiPolyATSend, commands, self.ui.midiPolyATRatio, "pressure")

    def dataChangedPBCommands(self, moduleCommand:ModuleCommand):
        if (find_item(self.ui.listWidgetMidiEvents, MIDIEvents[e_midiEvents.PB].name) == -1):
            self.ui.listWidgetMidiEvents.addItem(QListWidgetItem(MIDIEvents[e_midiEvents.PB].name))
        commands = Derivedcommandlist(moduleCommand.arguments[0])
        self.selectSendDestinationAndRatio(self.ui.midiPitchbendSend, commands, self.ui.midiPitchbendRatio, "pitch", 127)

    def dataChangedCATCommands(self, moduleCommand:ModuleCommand):
        if (find_item(self.ui.listWidgetMidiEvents, MIDIEvents[e_midiEvents.ChannelAT].name) == -1):
            self.ui.listWidgetMidiEvents.addItem(QListWidgetItem(MIDIEvents[e_midiEvents.ChannelAT].name))
        commands = Derivedcommandlist(moduleCommand.arguments[0])
        self.selectSendDestinationAndRatio(self.ui.midiChannelATSend, commands, self.ui.midiChannelATRatio, "pressure")

    def dataChangedPCCommands(self, moduleCommand:ModuleCommand):
        if (find_item(self.ui.listWidgetMidiEvents, MIDIEvents[e_midiEvents.PC].name) == -1):
            self.ui.listWidgetMidiEvents.addItem(QListWidgetItem(MIDIEvents[e_midiEvents.PC].name))
        commands = Derivedcommandlist(moduleCommand.arguments[0])

    def selectSendDestinationAndRatio(self, comboBox, commandList, ratio, variable, inMultiplier = 1):
        comboBox.blockSignals(True)
        ratio.blockSignals(True)

        found = False
        for a in commandList.commands:
            for b in range(0, comboBox.count()):

                if (a.command == comboBox.itemData(b)[1]):
                    comboBox.setCurrentIndex(b)
                    senderMultiplier = comboBox.itemData(b)[2]
                    found = True
                    break

        #if find != "Nothing":
        if found:
            offset, multiplier = equationParsingHelpers.getVariable(a.argument[0], variable)
            multiplier = multiplier * inMultiplier / senderMultiplier
            ratio.setValue(multiplier)
        else:
            comboBox.setCurrentIndex(0)
            ratio.setValue(0)

        comboBox.blockSignals(False)
        ratio.blockSignals(False)


    def guiChangedSustainDestination(self, anything):
        if (self.guiCallbackSystem.updatingFromModule > 0): return
        itemData = self.ui.midiSustainSend.itemData(self.ui.midiSustainSend.currentIndex())
        booltype = "bool"
        if self.ui.midiSustainInvert.isChecked():
            booltype = "ibool"

        command = "mcf.mc.ac:64:"
        if (itemData is None) or len(itemData) < 2:
            return
        if itemData[1] == "":
            command += "''"
        else:
            command += "'"
            for commandString in itemData[1]:
                #cmm = ""
                #if len(cmm) == 0: break
                if (command[-1] != "'"):
                    command += ","
                #command += cmm[0] + ":" + booltype + "(value)"
                command += commandString + ":" + booltype + "(value)"
        command += "'"
        self.serialHandler.write(command)

    def dataChangedSustainDestination(self):
        found = False
        moduleCommand, module = self.commandSet.getCommandAndModule("mcf.mc.ccc")
        count = int(moduleCommand.arguments[0])
        for  i in range(0, count):
            moduleCommand, module = self.commandSet.getCommandAndModule("mcf.mc.cc[" + str(i) + "].cl")
            if (moduleCommand.arguments[0] == '64'):
                found = True
                break
        if not found: return

        moduleCommand, module = self.commandSet.getCommandAndModule("mcf.mc.cc[" + str(i) + "].cm")
        if (moduleCommand.arguments is None) or (len(moduleCommand.arguments) < 1):
            return
        commandList = Derivedcommandlist(moduleCommand.arguments[0])

        foundFinal = False
        for b in range(0, self.ui.midiSustainSend.count()):
            if (len(self.ui.midiSustainSend.itemData(b)[1]) == len(commandList.commands)):
                found = True
                for a in commandList.commands:
                    #cId, module = self.commandSet.getCommandID(a)
                    if a.command not in self.ui.midiSustainSend.itemData(b)[1]:
                        found = False
                        break
                if (len(commandList.commands) > 0) and (found):
                    self.ui.midiSustainSend.setCurrentIndex(b)
                    foundFinal = True
                    break
        if not foundFinal:
            self.ui.midiSustainSend.setCurrentIndex(0)
        if ("ibool" in a.argument[0]):
            self.ui.midiSustainInvert.setChecked(True)
        else:
            self.ui.midiSustainInvert.setChecked(False)