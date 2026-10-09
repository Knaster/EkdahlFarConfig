from commandparser import Derivedcommanditem, Derivedcommandlist
from commanddefinitions import defaultCommandType, CommandID

class CommandSet:
    commandID = None
    indexingChild = None

    def __init__(self):
        self.CommandItem = Derivedcommanditem
        self.CommandList = Derivedcommandlist

        self.fromVer = 0
        self.toVer = 99999999999999

        self.commandTypes = defaultCommandType

        self.shortCommands: dict = {}
        self.longCommands: dict = {}

        self.shortID: dict = {}
        self.longID: dict = {}

        self.commands = []

        self.loadingStage = 0
        self.ready = False

    def postInit(self):
        self.shortID = {v: k for k, v in self.shortCommands.items()}
        self.longID = {v: k for k, v in self.longCommands.items()}

    '''
    def initialRequest(self) -> list:
        return []
    '''
    '''
    def requestData(self, serialHandler) -> list:
        return []
    
    def requestContinuousData(self, serialHandler):
        pass
    '''
    def buildHierarchy(self, commandItem, widget):
        pass

    '''
    def getCommandType(self, commandItem):
        pass
    
    def getQualifiedShortCommand(self, commandID, selectionIndex=None, stripIndex = False):
        pass

    def getCommandID(self, inCommand, module = None):
        revCID = dict(zip(self.longCommands.values(), self.longCommands.keys()))
        if (inCommand in revCID): return revCID[inCommand], None

        revCID = dict(zip(self.shortCommands.values(), self.shortCommands.keys()))
        if (inCommand in revCID): return revCID[inCommand], None

        return None, None
    '''
    def getCommandAndModule(self, inCommand, module = None):
        revCID = dict(zip(self.longCommands.values(), self.longCommands.keys()))
        if (inCommand in revCID): return revCID[inCommand], None

        revCID = dict(zip(self.shortCommands.values(), self.shortCommands.keys()))
        if (inCommand in revCID): return revCID[inCommand], None

        return None, None

    def processMessages(self, commandItem, commandSets, mainWidget, serialHandler):
        return

    '''        
        cId, module = self.getCommandID(commandItem)

        match(cId):
            case CommandID.version:
                serialHandler.write("help,nop")
                global connected
                connected = True
                self.requestData(serialHandler)

            case CommandID.harmonicSeriesData:
                ratios = []
                for i in range(2, len(commandItem.argument)):
                    ratios.append(commandItem.argument[i])

                mainWidget.handleHarmonicSeriesData(commandItem.argument[0], commandItem.argument[1], ratios)

            case CommandID.harmonicSeriesCount:
                simpleFARHandler.stringModules[0].setCommandValue(CommandID.harmonicSeriesCount, commandItem.argument[0])
                currentHarmonicSeries = simpleFARHandler.stringModules[0].getCommandValue(CommandID.harmonicSeriesSelect)
                mainWidget.ui.comboBoxHarmonicList.clear()
                hl = 0
                while (hl < int(commandItem.argument[0])):
                    mainWidget.ui.comboBoxHarmonicList.addItem(str(commandItem.argument[hl + 1]))
                    serialHandler.write("rqi:bhsd:" + str(hl))
                    hl += 1
                simpleFARHandler.stringModules[0].setCommandValue(CommandID.harmonicSeriesSelect, currentHarmonicSeries)
                mainWidget.ui.comboBoxHarmonicList.setCurrentIndex(int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.harmonicSeriesSelect)))

            case CommandID.harmonicSeriesSelect:
                simpleFARHandler.stringModules[0].setCommandValue(CommandID.harmonicSeriesSelect, commandItem.argument[0])
                #simpleFARHandler.currentHarmonicListSelected = int(commandItem.argument[0])
                mainWidget.ui.comboBoxHarmonicList.setCurrentIndex(int(commandItem.argument[0]))

            case CommandID.bowHarmonicBaseNote:
                mainWidget.handleHarmonicBaseNote(int(commandItem.argument[0]))

            case CommandID.midiConfigurationName:
                mainWidget.midiEventHandler.handleMIDIConfigurationName(commandItem.argument[0], str(commandItem.argument[1]), True)

            case CommandID.controlBoxDataReturn:
                mainWidget.cvEventHandler.handleControlBoxReturnData(commandItem.argument[0], commandItem.argument[1])

            case CommandID.actuatorCount:
                mainWidget.ui.comboBoxActuatorPreset.clear()
                for a in range(0, int(commandItem.argument[0])):
                    serialHandler.write("rqi:bad:" + str(a))

            case CommandID.actuatorData:
                if (len(commandItem.argument) < 5):
                    # break
                    raise ("Something is wrong in BAD command")
                mainWidget.handleActuatorData(commandItem.argument[0], commandItem.argument[4], commandItem.argument[3], commandItem.argument[1], commandItem.argument[2])

            case CommandID.midiConfigurationSelect:
                simpleFARHandler.stringModules[0].setCommandValue(CommandID.midiConfigurationSelect, commandItem.argument[0])
                mainWidget.midiEventHandler.handleMIDIConfigurationSelect(commandItem.argument[0])
                serialHandler.write("rqi:mev")

            case CommandID.midiConfigurationCount:
                simpleFARHandler.stringModules[0].setCommandValue(CommandID.midiConfigurationCount, commandItem.argument[0])
                mainWidget.midiEventHandler.handleMIDIConfigurationCount(commandItem.argument[0])
                for a in range(0, int(commandItem.argument[0])):
                    serialHandler.write("rqi:mcfn:" + str(a))

            case CommandID.midiConfigurationData:
                match commandItem.argument[0]:
                    case "noteon":
                        mainWidget.midiEventHandler.setMIDINoteOnCommands(commandItem.argument[1])
                    case "noteoff":
                        mainWidget.midiEventHandler.setMIDINoteOffCommands(commandItem.argument[1])
                    case "cc":
                        mainWidget.midiEventHandler.setMIDICCCommands(commandItem.argument[1],commandItem.argument[2])
                    case "pat":
                        mainWidget.midiEventHandler.setMIDIPATCommands(commandItem.argument[1])
                    case "pb":
                        mainWidget.midiEventHandler.setMIDIPBCommands(commandItem.argument[1])
                    case "cat":
                        mainWidget.midiEventHandler.setMIDICATCommands(commandItem.argument[1])
                    case "pc":
                        mainWidget.midiEventHandler.setMIDIPCCommands(commandItem.argument[1])

            case CommandID.midiConfigurationName:
                mainWidget.midiEventHandler.handleMIDIConfigurationName(commandItem.argument[0], str(commandItem.argument[1]), True)

            case CommandID.midiReceiveChannel:
                mainWidget.midiEventHandler.handleMIDIReceiveChannel(commandItem.argument[0])

            case CommandID.controlBoxControlData:
                mainWidget.cvEventHandler.handleControlBoxControlData(commandItem.argument[0], commandItem.argument[1])

            case CommandID.bowHarmonic | CommandID.bowHarmonicShift | CommandID.bowHarmonicShift5 | CommandID.bowHarmonicBase | CommandID.bowHarmonicAdd:
                rqTg = self.getQualifiedShortCommand(CommandID.pidTargetFreq)
                if len(rqTg) > 0:
                    serialHandler.write("rqi:" + rqTg[0])

            case _:
                return False
        return True

    def setMidiConfigurationSelect(self, sender, serialHandler, simpleFARHandler, index):
        simpleFARHandler.stringModules[0].setCommandValue(CommandID.midiConfigurationSelect, index)
        if (not sender.updatingFromModule):
            qualifiedShort = self.getQualifiedShortCommand(CommandID.midiConfigurationSelect)[0]
            serialHandler.write(qualifiedShort + ":"+ str(index))

    def setMidiConfigurationName(self, sender, serialHandler, simpleFARHandler, index, name):
        setConfig = self.getQualifiedShortCommand(CommandID.midiConfigurationSelect)[0]
        serialHandler.write(setConfig + ":" + str(index))
        setName = self.getQualifiedShortCommand(CommandID.midiConfigurationName)[0]
        serialHandler.write(setName + ":" + str(name))

    def addMidiConfiguration(self, sender, serialHandler, simpleFARHandler, name):
        addConf = self.getQualifiedShortCommand(CommandID.midiConfigurationAdd)[0]
        #selConf = self.getQualifiedShortCommand(CommandID.midiConfigurationSelect)[0]
        newIndex = simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationCount)
        serialHandler.write(addConf + ":" + name) # + "," + selConf + ":" + str(newIndex))
        #serialHandler.write("midiconfigurationadd:" + str(text))
        #serialHandler.write("midiconfiguration:" + str(mainWidget.ui.comboBoxConfiguration.count() - 1))

    def removeMidiConfiguration(self, sender, serialHandler, simpleFARHandler, index):
        rmConf = self.getQualifiedShortCommand(CommandID.midiConfigurationRemove)[0]
        confCount = self.getQualifiedShortCommand(CommandID.midiConfigurationCount)[0]
        confIndex = self.getQualifiedShortCommand(CommandID.midiConfigurationSelect)[0]
        serialHandler.write(rmConf + ":" + str(index) + ",rqi:" + confCount + ",rqi:" + confIndex)

    def addMidiConfigurationCC(self, sender, serialHandler, simpleFARHandler, cc):
        setCC = self.getQualifiedShortCommand(CommandID.midiConfigurationData)[0]
        serialHandler.write(setCC + ":cc:" + str(cc) + ":''")

    def removeMidiConfigurationCC(self, sender, serialHandler, simpleFARHandler, cc):
        rmCC = self.getQualifiedShortCommand(CommandID.midiConfigurationRemoveCC)[0]
        serialHandler.write(rmCC + ":" + str(cc))

    def setMidiConfigurationNoteOnCommands(self, sender, serialHandler, simpleFAR, index, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationData, [index])[0]
        serialHandler.write(qualifiedCommand + ":noteon:'" + commands + "'")

    def setMidiConfigurationNoteOffCommands(self, sender, serialHandler, simpleFAR, index, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationData, [index])[0]
        serialHandler.write(qualifiedCommand + ":noteoff:'" + commands + "'")

    def setMidiConfigurationPolyAftertouchCommands(self, sender, serialHandler, simpleFAR, index, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationData, [index])[0]
        serialHandler.write(qualifiedCommand + ":pat:'" + commands + "'")

    def setMidiConfigurationChannelAftertouchCommands(self, sender, serialHandler, simpleFAR, index, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationData, [index])[0]
        serialHandler.write(qualifiedCommand + ":cat:'" + commands + "'")

    def setMidiConfigurationProgramChangeCommands(self, sender, serialHandler, simpleFAR, index, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationData, [index])[0]
        serialHandler.write(qualifiedCommand + ":pc:'" + commands + "'")

    def setMidiConfigurationPitchBendCommands(self, sender, serialHandler, simpleFAR, index, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationData, [index])[0]
        serialHandler.write(qualifiedCommand + ":pb:'" + commands + "'")

    def setMidiConfigurationContinuousControllerCommands(self, sender, serialHandler, simpleFAR, index, cc, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationData, [index])[0]
        serialHandler.write(qualifiedCommand + ":cc:" + str(cc) + ":'" + commands + "'")
    '''
