from PySide6.QtWidgets import *
from commanddefinitions import CommandID
from general_helpers import find_item, remove_item
import equationParsingHelpers

class midiEventHandler:
    def __init__(self, mainClass, serialHandler, commandSet, simpleFARHandler):
        self.mainClass = mainClass
        self.serialHandler = serialHandler
        self.commandSet = commandSet
        self.simpleFARHandler = simpleFARHandler

    MIDIBinarySenders = [["None", []], ["Bow hold & Mute inhibit", [CommandID.bowPressureHold, CommandID.muteSustain]], ["Bow hold", [CommandID.bowPressureHold]],
                         ["Mute inhibit", [CommandID.muteSustain]]]

    def connectWidgetsToBinarySenders(self, midiEvent, widgets):
        for widget in widgets:
            widget.midiEvent = midiEvent
            widget.widgets = widgets
            if isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(self.widgetMIDIBinarySendersCallback)
            elif isinstance(widget, QSlider):
                self.mainClass.assignMouseReleaseEvent(widget, self.widgetMIDIBinarySendersCallback)
            elif isinstance(widget, QCheckBox):
                widget.stateChanged.connect(self.widgetMIDIBinarySendersCallback)

    def populateComboBoxSendBinary(self, comboBox):
        comboBox.clear()
        for sendData in self.MIDIBinarySenders:
            comboBox.addItem(sendData[0], sendData)
        pass

    def widgetMIDIBinarySendersCallback(self):
        if (self.mainClass.updatingFromModule): return
        widget = self.sender()
        cmd = ""
        itemData = self.mainClass.ui.midiSustainSend.itemData(self.ui.midiSustainSend.currentIndex())
        booltype = "bool"
        if self.mainClass.ui.midiSustainInvert.isChecked():
            booltype = "ibool"
        command = (self.commandSets.getQualifiedShortCommand(CommandID.midiConfigurationData,
                                                       [self.simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect)])[0] +
                                                                    ":cc:64:")
        if itemData[1] == "":
            command += "''"
        else:
            command += "'"
            for a in itemData[1]:
                cmm = self.commandSets.getQualifiedShortCommand(a)
                if len(cmm) == 0: break
                if (command[-1] != "'"):
                    command += ","
                #command += a + ":" + booltype + "(value)"
                command += cmm[0] + ":" + booltype + "(value)"
        command += "'"
        self.serialHandler.write(command)
        #self.updateUIData()

    def widgetMIDIEventUpdateSignal(self):
        self.widgetMIDIEventUpdate(self.sender())

    def widgetMIDIEventUpdate(self, widget):
        # widget = self.sender()
        if widget is None:
            return
        match widget.midiEvent:
            case "pb":
                value = self.mainClass.ui.midiPitchbendRatio.value() / 128
                itemData = self.mainClass.ui.midiPitchbendSend.itemData(self.mainClass.ui.midiPitchbendSend.currentIndex())
                variableName = "pitch"
                pass
            case "pat":
                value = self.mainClass.ui.midiPolyATRatio.value()
                itemData = self.mainClass.ui.midiPolyATSend.itemData(self.mainClass.ui.midiPolyATSend.currentIndex())
                variableName = "pressure"
                pass
            case "cat":
                value = self.mainClass.ui.midiChannelATRatio.value()
                itemData = self.mainClass.ui.midiChannelATSend.itemData(self.mainClass.ui.midiChannelATSend.currentIndex())
                variableName = "pressure"
                pass

        qualifiedMidiAssigns = self.commandSet.getQualifiedShortCommand(CommandID.midiConfigurationData,
                                                                    [self.simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect)])
        if itemData[1] == "":
            for qualifiedAssign in qualifiedMidiAssigns:
                command = qualifiedAssign + ":" + widget.midiEvent + ":''"
                self.serialHandler.write(command)
        else:
            for qualifiedAssign in qualifiedMidiAssigns:
                qualifiedCommand = self.commandSet.getQualifiedShortCommand(itemData[1])[0]
                command = (qualifiedAssign + ":" + widget.midiEvent + ":'" + qualifiedCommand + ":(" + variableName + " * " +
                           str(value) + " * " + str(itemData[3]) + ")'")
                self.serialHandler.write(command)


    def connectWidgetsToMIDIEvent(self, midiEventName, widgets):
        for widget in widgets:
            widget.midiEvent = midiEventName
            widget.widgets = widgets
            if isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(self.widgetMIDIEventUpdateSignal)
            elif isinstance(widget, QSlider):
                self.mainClass.assignMouseReleaseEvent(widget, self.widgetMIDIEventUpdate)
            elif isinstance(widget, QCheckBox):
                widget.stateChanged.connect(self.widgetMIDIEventUpdateSignal)


    def setMIDINoteOnCommands(self, commands):
        self.simpleFARHandler.instrumentMaster.evNoteOn = commands
        if (find_item(self.mainClass.ui.listWidgetMidiEvents, "Note On") == -1):
            self.mainClass.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Note On"))

        self.simpleFARHandler.instrumentMaster.cmdNoteOn.clear()
        self.simpleFARHandler.instrumentMaster.cmdNoteOn.addCommands(commands)
        seCmd = self.commandSet.getQualifiedShortCommand(CommandID.solenoidEngage, None, True)[0]
        offset, multiplier = equationParsingHelpers.getVariable(self.simpleFARHandler.instrumentMaster.cmdNoteOn.getCommandAttribute(seCmd, 0), "velocity")
        self.mainClass.ui.midiNoteOnVelToHammer.setValue(multiplier)

        if equationParsingHelpers.isVariableInEquation(self.simpleFARHandler.instrumentMaster.cmdNoteOn.getCommandAttribute(seCmd, 0), "notecount"):
            self.mainClass.ui.midiNoteOnHammerStaccato.setChecked(True)
        else:
            self.mainClass.ui.midiNoteOnHammerStaccato.setChecked(False)

        mrCmd = self.commandSet.getQualifiedShortCommand(CommandID.muteRest, None, True)[0]
        if not self.simpleFARHandler.instrumentMaster.cmdNoteOn.getCommandAttribute(mrCmd, 0) == "":
            self.mainClass.ui.midiNoteOnSendMuteRest.setChecked(True)
        else:
            self.mainClass.ui.midiNoteOnSendMuteRest.setChecked(False)


    def setMIDINoteOffCommands(self, commands):
        self.simpleFARHandler.instrumentMaster.evNoteOff = commands
        if (find_item(self.mainClass.ui.listWidgetMidiEvents, "Note Off") == -1):
            self.mainClass.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Note Off"))

        self.simpleFARHandler.instrumentMaster.cmdNoteOff.clear()
        self.simpleFARHandler.instrumentMaster.cmdNoteOff.addCommands(commands)

        mfmCmd = self.commandSet.getQualifiedShortCommand(CommandID.muteFullMute, None, True)[0]
        if not self.simpleFARHandler.instrumentMaster.cmdNoteOff.getCommandAttribute(mfmCmd, 0) == "":
            self.mainClass.ui.midiNoteOffSendFullMute.setChecked(True)
        else:
            self.mainClass.ui.midiNoteOffSendFullMute.setChecked(False)

        bmrCmd = self.commandSet.getQualifiedShortCommand(CommandID.motorRun, None, True)[0]
        if not self.simpleFARHandler.instrumentMaster.cmdNoteOff.getCommandAttribute(bmrCmd, 0) == "":
            self.mainClass.ui.midiNoteOffMotorOff.setChecked(True)
        else:
            self.mainClass.ui.midiNoteOffMotorOff.setChecked(False)


    def setMIDICCCommands(self, cc, commands):
        self.simpleFARHandler.instrumentMaster.addCC(int(cc), commands)
        if (find_item(self.mainClass.ui.listWidgetMidiEvents, "CC " + str(cc)) == -1):
            self.mainClass.ui.listWidgetMidiEvents.addItem(QListWidgetItem("CC " + str(cc)))
        self.setMIDISustainDestination()


    def setMIDISustainDestination(self):
        commands = self.simpleFARHandler.instrumentMaster.getCC(64).command
        commandList = self.commandSet.currentCommandSet.CommandList(commands)

        if ("ibool" in commands):
            self.mainClass.ui.midiSustainInvert.setChecked(True)
        else:
            self.mainClass.ui.midiSustainInvert.setChecked(False)

        for b in range(0, self.mainClass.ui.midiSustainSend.count()):
            if (len(self.mainClass.ui.midiSustainSend.itemData(b)[1]) == len(commandList.commands)):
                found = True
                for a in commandList.commands:
                    cId = self.commandSet.getCommandID(a)
                    if cId not in self.mainClass.ui.midiSustainSend.itemData(b)[1]:
                        found = False
                        break
                if (len(commandList.commands) > 0) and (found):
                    self.mainClass.ui.midiSustainSend.setCurrentIndex(b)
                    return
        self.mainClass.ui.midiSustainSend.setCurrentIndex(0)


    def setMIDIPATCommands(self, commands):
        self.simpleFARHandler.instrumentMaster.evPolyAftertouch = commands
        if (find_item(self.mainClass.ui.listWidgetMidiEvents, "Poly Aftertouch") == -1):
            self.mainClass.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Poly Aftertouch"))

        self.simpleFARHandler.instrumentMaster.cmdPolyAftertouch.clear()
        self.simpleFARHandler.instrumentMaster.cmdPolyAftertouch.addCommands(commands)

        self.selectSendDestinationAndRatio(self.mainClass.ui.midiPolyATSend, self.simpleFARHandler.instrumentMaster.cmdPolyAftertouch,
                                                 self.mainClass.ui.midiPolyATRatio, "pressure")


    def setMIDIPBCommands(self, commands):
        self.simpleFARHandler.instrumentMaster.evPitchbend = commands
        if (find_item(self.mainClass.ui.listWidgetMidiEvents, "Pitchbend") == -1):
            self.mainClass.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Pitchbend"))

        self.simpleFARHandler.instrumentMaster.cmdPitchbend.clear()
        self.simpleFARHandler.instrumentMaster.cmdPitchbend.addCommands(commands)

        self.selectSendDestinationAndRatio(self.mainClass.ui.midiPitchbendSend, self.simpleFARHandler.instrumentMaster.cmdPitchbend,
                                                 self.mainClass.ui.midiPitchbendRatio, "pitch", 127)


    def setMIDICATCommands(self, commands):
        self.simpleFARHandler.instrumentMaster.evChannelAftertouch = commands
        if (find_item(self.mainClass.ui.listWidgetMidiEvents, "Channel Aftertouch") == -1):
            self.mainClass.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Channel Aftertouch"))

        self.simpleFARHandler.instrumentMaster.cmdChannelAftertouch.clear()
        self.simpleFARHandler.instrumentMaster.cmdChannelAftertouch.addCommands(commands)

        self.selectSendDestinationAndRatio(self.mainClass.ui.midiChannelATSend, self.simpleFARHandler.instrumentMaster.cmdChannelAftertouch,
                                                 self.mainClass.ui.midiChannelATRatio, "pressure")


    def setMIDIPCCommands(self, commands):
        self.simpleFARHandler.instrumentMaster.evProgramChange = commands
        if (find_item(self.mainClass.ui.listWidgetMidiEvents, "Program change") == -1):
            self.mainClass.ui.listWidgetMidiEvents.addItem(QListWidgetItem("Program change"))


    def handleMIDIConfigurationCount(self, count):
        self.mainClass.ui.comboBoxConfiguration.clear()
        while (self.mainClass.ui.comboBoxConfiguration.count() < int(count)):
            self.mainClass.ui.comboBoxConfiguration.insertItem(self.mainClass.ui.comboBoxConfiguration.count() + 1, "placeholder")


    def handleMIDIConfigurationName(self, index, name, setIndex):
        self.mainClass.ui.comboBoxConfiguration.setItemText(index, name)
        if (setIndex):
            self.mainClass.ui.comboBoxConfiguration.setCurrentIndex(self.simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect))


    def handleMIDIConfigurationSelect(self, config):
        self.simpleFARHandler.stringModules[0].setCommandValue(CommandID.midiConfigurationSelect, float(config))
        self.mainClass.updateStringModuleData()
        self.mainClass.ui.listWidgetMidiEvents.clear()
        self.mainClass.ui.comboBoxConfiguration.setCurrentIndex(int(self.simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationSelect)))


    def handleMIDIReceiveChannel(self, channel):
        self.mainClass.ui.comboBoxMidiChannel.blockSignals(True)
        ch = int(channel)
        if ((ch < 1) or (ch > 16)):
            find = "Omni"
        else:
            find = str(ch)

        for a in range(0, self.mainClass.ui.comboBoxMidiChannel.count()):
            if find == self.mainClass.ui.comboBoxMidiChannel.itemText(a):
                self.mainClass.ui.comboBoxMidiChannel.setCurrentIndex(a)
                break
        self.mainClass.ui.comboBoxMidiChannel.blockSignals(False)

    # Finds the first destination command in commandList and selects it in the Combo Box given in comboBox
    # Sets the slider given in ratio to the multiplier value used in combination with the string literal variable given in variable
    def selectSendDestinationAndRatio(self, comboBox, commandList, ratio, variable, inMultiplier = 1):
        comboBox.blockSignals(True)
        ratio.blockSignals(True)

        found = False
        for a in commandList.commands:
            for b in range(0, comboBox.count()):
                cId = self.commandSet.getCommandID(a)
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

    eventDescription = [[ "Note On", "Note on message, sent when a key has been depressed. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n note - note number (0-127) \n velocity - key velocity (0-127)" ],
        [ "Note Off", "Note off message, sent when a key has been released. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n note - note number (0-127) \n velocity - key velocity (0-127)" ],
        [ "CC [xx]", "Continous Controller, sent by various control surfaces. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n control - control number (0-127) \n value - controller value (0-127)" ],
        [ "Poly Aftertouch", "Polyphonic Aftertouch, key pressure per key. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n note - note number (0-127) \n pressure - key pressure (0-127)" ],
        [ "Channel Aftertouch", "Channel Aftertouch, key pressure per channel. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n pressure - key pressure (0-127)"],
        [ "Pitchbend", "Pitchbend, frequency change from the current key. \n\nAdded variables: \n channel - MIDI Channel (0-15)\n pitch - bend (-8192 - 8192)"],
        [ "Program change", "Program change message, mostly used to change sound on various devices. \n\nAdded variables: \n channel - MIDI Channel (0-127) \n program - program number (0-127)"]
        ]

    def updateTextForSelectedListItem(self):
        current = self.mainClass.ui.listWidgetMidiEvents.currentItem()
        self.listWidgetMidiEventscurrentItemChanged(current, current)

    def listWidgetMidiEventscurrentItemChanged(self, current, previous):
        self.mainClass.ui.plainTextEditEventDescription.clear()
        if current is None:
            return
        match (current.text()):
            case "Note On":
                self.mainClass.ui.lineEditMidiEventCommand.setText(str(self.simpleFARHandler.instrumentMaster.evNoteOn))
                self.mainClass.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[0][1])
            case "Note Off":
                self.mainClass.ui.lineEditMidiEventCommand.setText(str(self.simpleFARHandler.instrumentMaster.evNoteOff))
                self.mainClass.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[1][1])
            case "Poly Aftertouch":
                self.mainClass.ui.lineEditMidiEventCommand.setText(str(self.simpleFARHandler.instrumentMaster.evPolyAftertouch))
                self.mainClass.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[3][1])
            case "Channel Aftertouch":
                self.mainClass.ui.lineEditMidiEventCommand.setText(str(self.simpleFARHandler.instrumentMaster.evChannelAftertouch))
                self.mainClass.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[4][1])
            case "Pitchbend":
                self.mainClass.ui.lineEditMidiEventCommand.setText(str(self.simpleFARHandler.instrumentMaster.evPitchbend))
                self.mainClass.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[5][1])
            case "Program change":
                self.mainClass.ui.lineEditMidiEventCommand.setText(str(self.simpleFARHandler.instrumentMaster.evProgramChange))
                self.mainClass.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[6][1])
            case _:
                if current.text()[:2] == "CC":
                    self.mainClass.ui.lineEditMidiEventCommand.setText(str(self.simpleFARHandler.instrumentMaster.getCC(int(current.text()[3:])).command))
                self.mainClass.ui.plainTextEditEventDescription.insertPlainText(self.eventDescription[2][1])
