from PySide6.QtWidgets import *

from GUICallbackSystem import GUICallback, GUICallbackSystem
from ModuleSystem import ModuleCommand

from enum import Enum, auto

class e_midiEvents(Enum):
    NoteOn = auto()
    NoteOff = auto()
    PolyAT = auto()
    ChannelAT = auto()
    PC = auto()
    CC = auto()
    PB = auto()

class MIDIEventDeclaration():
    def __init__(self, name, command):
        self.name = name
        self.command = command

MIDIEvents = { e_midiEvents.NoteOn : MIDIEventDeclaration("Note On", "mcf.mc.non"),
               e_midiEvents.NoteOff : MIDIEventDeclaration("Note Off", "mcf.mc.nof"),
               e_midiEvents.PB : MIDIEventDeclaration("Pitch bend", "mcf.mc.pb"),
               e_midiEvents.PC : MIDIEventDeclaration("Program change", "mcf.mc.pc"),
               e_midiEvents.PolyAT : MIDIEventDeclaration("Poly after touch", "mcf.mc.pat"),
               e_midiEvents.ChannelAT : MIDIEventDeclaration("Channel after touch", "mcf.mc.cat")}

class midiEventHandler(QWidget):
    def __init__(self, mainWidget, serialHandler, commandSet, guiCallbackSystem:GUICallbackSystem):
        super().__init__()
        self.ui = mainWidget.ui
        self.serialHandler = serialHandler
        self.commandSet = commandSet
        self.unknownCCCallbacks:list[GUICallback] = []
        self.guiCallbackSystem = guiCallbackSystem

        self.guiCallbackLineEditMidiEventCommand:GUICallback = None

        self.midiEventModuleDataPointer = {
            MIDIEvents[e_midiEvents.NoteOn].name :  ["mcf.mc.non", 0, "", None],
            MIDIEvents[e_midiEvents.NoteOff].name : ["mcf.mc.nof", 1, "", None],
            MIDIEvents[e_midiEvents.PolyAT].name: ["mcf.mc.pat", 3, "pressure", self.ui.midiPolyATRatio],
            MIDIEvents[e_midiEvents.ChannelAT].name: ["mcf.mc.cat", 4, "pressure", self.ui.midiChannelATRatio],
            MIDIEvents[e_midiEvents.PB].name: ["mcf.mc.pb", 5, "pitch", self.ui.midiPitchbendRatio],
            MIDIEvents[e_midiEvents.PC].name: ["mcf.mc.pc", 6, "program", None]
        }

    MIDIBinarySenders = [["None", []], ["Bow hold & Mute inhibit", ["bw.bp.hd", "mu.su"]], ["Bow hold", ["bw.bp.hd"]],
                         ["Mute inhibit", ["mu.su"]]]

    def populateComboBoxSendBinary(self, comboBox):
        comboBox.clear()
        for sendData in self.MIDIBinarySenders:
            comboBox.addItem(sendData[0], sendData)
        pass

    # defined as Text description, command, multiplier
    # Multiplier is to be used with a slider ranging 0-512 because a standard MIDI value is 0-127 and 128*512 = 65535
    # For PB this is different since it is 14-bit -8191 - 8191
    MIDIVariableSenders = [["Nothing", "", 0], # 0, 0
                           ["Harmonic shift", "bw.hsh.sh", 1], # -32767, 1
                           ["Harmonic shift 5", "bw.hsh.sh5", 0.2],
                           ["Pressure (modifier)", "bw.bp.mo", 1], # 0, 1
                           ["Pressure (baseline)", "bw.bp.ba", 1], # 0, 1
                           ["Mute position", "mu.sp", 1], # 0, 1
                           ["Solenoid force multiplier", "so.fm", 1]] # 0, 1

    #    MIDIBinarySenders = [["MIDI & Mute sustain", ""]]
    def populateComboBoxSendByte(self, comboBox):
        # Fake updating from module just so that GUI elements don't try and update as we clear and repopulate the list
        self.guiCallbackSystem.updatingFromModule += 1
        comboBox.clear()
        for sendData in self.MIDIVariableSenders:
            comboBox.addItem(sendData[0], sendData)
        self.guiCallbackSystem.updatingFromModule -= 1

    def guiChangedRatioDestination(self, moduleCommand:ModuleCommand):
        commandPart = moduleCommand.shortCommand
        match commandPart:
            case "pb":
                value = self.ui.midiPitchbendRatio.value() / 128 # 14-bit number, get it in the CC range
                itemData = self.ui.midiPitchbendSend.itemData(self.ui.midiPitchbendSend.currentIndex())
                variableName = "pitch"
                setFunc = "mcf.mc.pb"
                pass
            case "pat":
                value = self.ui.midiPolyATRatio.value()
                itemData = self.ui.midiPolyATSend.itemData(self.ui.midiPolyATSend.currentIndex())
                variableName = "pressure"
                setFunc = "mcf.mc.pat"
                pass
            case "cat":
                value = self.ui.midiChannelATRatio.value()
                itemData = self.ui.midiChannelATSend.itemData(self.ui.midiChannelATSend.currentIndex())
                variableName = "pressure"
                setFunc = "mcf.mc.cat"
                pass
            case _:
                return

        if itemData is None:
            return
        elif itemData[1] == "":
            commandString = "''"
        else:
            commandString = "'" + itemData[1] + ":(" + variableName + " * " + str(value * itemData[2]) + ")'"

        self.serialHandler.write(setFunc + ":" + commandString)

    def updateTextForSelectedListItem(self, possible = None):
        current = self.ui.listWidgetMidiEvents.currentItem()
        self.listWidgetMidiEventscurrentItemChanged(current)

    def listWidgetMidiEventscurrentItemChanged(self, current):
        self.ui.plainTextEditEventDescription.clear()
        if current is None:
            return

        found = False
        for midiEvent in MIDIEvents.values():
            if midiEvent.name == current.text():
                found = True
                break
        if found:
            commandString = midiEvent.command
            command, module = self.commandSet.getCommandAndModule(commandString)
            self.ui.lineEditMidiEventCommand.setText(command.arguments[0])
            command:ModuleCommand = command
        elif current.text()[:2] == "CC":
            ccnum = current.text()[3:]
            found = False
            command, modules = self.commandSet.getCommandAndModule("mcf.mc.ccc")
            count = int(command.arguments[0])
            commandString = ""
            for i in range(0, count):
                command, trashx = self.commandSet.getCommandAndModule("mcf.mc.cc[" + str(i) + "].cl")
                if (command.arguments[0] == ccnum):
                    found = True
                    commandString = "mcf.mc.cc[" + str(i) + "].cm"
                    break
            if not found: return

            command, trashx = self.commandSet.getCommandAndModule(commandString)

            commands = ""
            if (command.arguments is not None and len(command.arguments) > 0):
                commands = command.arguments[0]

            self.ui.lineEditMidiEventCommand.setText(commands)
        else:
            return

        if self.guiCallbackLineEditMidiEventCommand is not None:
            self.guiCallbackSystem.removeGUICallback(self.guiCallbackLineEditMidiEventCommand, False)
        self.guiCallbackLineEditMidiEventCommand = GUICallback(None, commandString,
                                                               dataCallbackFunction = self.dataChangedMidiEventCommand)
        self.guiCallbackSystem.addGUICallback(self.guiCallbackLineEditMidiEventCommand, False)

        outputText = command.helpCommand.description + "\n\n" + "Sets the following variables:\n"
        variables = ""
        for variable in command.helpCommand.variables:
            if (variables != ""): variables += ", "
            variables +=  variable
        self.ui.plainTextEditEventDescription.insertPlainText(outputText + variables)


    def dataChangedMidiEventCommand(self, moduleCommand:ModuleCommand):
        if (moduleCommand.arguments is not None and len(moduleCommand.arguments) > 0):
            self.ui.lineEditMidiEventCommand.setText(moduleCommand.arguments[0])

