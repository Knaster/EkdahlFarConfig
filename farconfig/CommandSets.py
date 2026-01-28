from enum import Enum, auto
import random
from watchdog.watchmedo import command_parsers

from commandparser import CommandList as _commandList
from commandparser import CommandItem as _commandItem

from stringModule import SimpleFARHandler

def stripLeadingQuotes(inp:str):
    if (len(inp) < 2): return inp
    if ((inp[0] == "'") or (inp[0] == "\"")) and ((inp[len(inp) - 1] == "'") or (inp[len(inp) - 1] == "\"")):
        inp = inp[1:len(inp)-1]
    return inp

class CommandID(Enum):
    nop = auto()
    requestInfo = auto()
    debugPrint = auto()
    saveAllParameters = auto()
    loadAllParameters = auto()
    resetAllParameters = auto()
    userVariable = auto()
    expressionparserEvaluate = auto()
    ifEqual = auto()
    ifGreater = auto()
    ifLess = auto()
    reset = auto()
    nickName = auto()
    dir = auto()
    dumpSaveData = auto()
    freeMemory = auto()
    version = auto()

    moduleSelect = auto()
    moduleCount = auto()
    calibrateAll = auto()
    calibrateBowSpeed = auto()
    calibrateBowPressure = auto()
    calibrateMute = auto()
    pickupStringFrequency = auto()
    pickupAudioPeak = auto()
    pickupAudioRMS = auto()

    bowSelect = auto()
    bowStatus = auto()
    bowSpeedMode = auto()
    bowMotorTimeout = auto()
    bowHome = auto()
    bowPIDEnable = auto()

    bowFundamental = auto()
    bowHarmonic = auto()
    bowHarmonicAdd = auto()
    bowHarmonicBase = auto()
    bowHarmonicBaseNote = auto()
    bowHarmonicShift = auto()
    bowHarmonicShiftRange = auto()
    bowHarmonicShift5 = auto()
    bowMeasureTimeToTarget = auto()

    harmonicSeriesSelect = auto()
    harmonicSeriesData = auto()
    harmonicSeriesRatio = auto()
    harmonicSeriesRemoveRatio = auto()
    harmonicSeriesCount = auto()
    harmonicSeriesSave = auto()
    harmonicSeriesRemove = auto()
    harmonicSeriesAdd = auto()
    harmonicSeriesName = auto()

    actuatorSelect = auto()
    actuatorAdd = auto()
    actuatorRemove = auto()
    actuatorSave = auto()
    actuatorData = auto()
    actuatorCount = auto()
    actuatorName = auto()

    motorRun = auto()
    motorDirectPWM = auto()
    motorVoltage = auto()
    motorCurrent = auto()
    motorCurrentLimit = auto()
    motorPowerLimit = auto()
    motorEmergencyStop = auto()
    motorPWMMin = auto()
    motorPWMMax = auto()
    motorFrequency = auto()
    motorFaultCommands = auto()
    motorOverPowerCommands = auto()

    pidTargetFreq = auto()
    pidKi = auto()
    pidKp = auto()
    pidKd = auto()
    pidIntegratorError = auto()
    pidReset = auto()
    pidMaxError = auto()
    pidPeakError = auto()
    pidSpeedMax = auto()
    pidSpeedMin = auto()

    bowPressureBaseline = auto()
    bowPressureModifier = auto()
    bowPressureRest = auto()
    bowPressureEngage = auto()
    bowPressurePositionMax = auto()
    bowPressurePositionEngage = auto()
    bowPressurePositionRest = auto()
    bowPressureEngageSpeed = auto()
    bowPressureModulationSpeed = auto()
    bowPressureHold = auto()

    solenoidSelect = auto()
    solenoidEngage = auto()
    solenoidDisengage = auto()
    solenoidMaxForce = auto()
    solenoidMinForce = auto()
    solenoidForceMultiplier = auto()
    solenoidEngageDuration = auto()

    muteSelect = auto()
    muteSetPosition = auto()
    muteFullMute = auto()
    muteHalfMute = auto()
    muteRest = auto()
    muteSaveFull = auto()
    muteSaveHalf = auto()
    muteSaveRest = auto()
    muteFullMutePosition = auto()
    muteHalfMutePosition = auto()
    muteRestPosition = auto()
    muteSustain = auto()
    muteBackoff = auto()
    muteHome = auto()

    muteSetHardwarePosition = auto()
    muteCompleteTask = auto()
    muteAutoCorrect = auto()
    muteHomingSensed = auto()
    muteMoveDirection = auto()
    muteCurrentStep = auto()
    muteHomingPoint = auto()
    muteHomingStage = auto()
    muteTMCInfo = auto()

    midiConfigurationSelect = auto()
    midiConfigurationAdd = auto()
    midiConfigurationRemove = auto()
    midiConfigurationCount = auto()
    midiConfigurationName = auto()
    midiConfigurationData = auto()
    midiConfigurationRemoveCC = auto()
    midiConfigurationAddCC = auto()
    midiConfigurationDefaults = auto()
    midiReceiveChannel = auto()
    midiAllNotesOff = auto()

    controlBoxControlData = auto()
    controlBoxControlDefaults = auto()
    controlBoxDataReturn = auto()
    controlBoxADCSettings = auto()

    testADCLatency = auto()
    testADCLatencyReturn = auto()
    testADCMinMax = auto()


class CommandType(Enum):
    undefined = 0
    simple = auto()
    advanced = auto()
    modal = auto()
    index = auto()

defaultCommandType = {
    CommandID.calibrateAll: CommandType.modal,
    CommandID.calibrateBowSpeed: CommandType.modal,
    CommandID.calibrateBowPressure: CommandType.modal,
    CommandID.calibrateMute: CommandType.modal,

    #CommandID.bowSelect: CommandType.simple,
    CommandID.bowFundamental: CommandType.simple,
    CommandID.motorVoltage: CommandType.simple,
    CommandID.bowMotorTimeout: CommandType.simple,
    CommandID.pidKp: CommandType.simple,
    CommandID.pidKi: CommandType.simple,
    CommandID.pidKd: CommandType.simple,
    CommandID.pidIntegratorError: CommandType.simple,
    CommandID.muteFullMutePosition: CommandType.simple,
    CommandID.muteHalfMutePosition: CommandType.simple,
    CommandID.muteRestPosition: CommandType.simple,
    CommandID.muteBackoff: CommandType.simple,
    CommandID.motorPWMMax: CommandType.simple,
    CommandID.motorPWMMin: CommandType.simple,
    CommandID.bowPressurePositionMax: CommandType.simple,
    CommandID.bowPressurePositionRest: CommandType.simple,
    CommandID.bowPressurePositionEngage: CommandType.simple,
    CommandID.motorFrequency: CommandType.simple,
    CommandID.pickupStringFrequency: CommandType.simple,
    CommandID.motorCurrent: CommandType.simple,
    CommandID.solenoidMaxForce: CommandType.simple,
    CommandID.solenoidMinForce: CommandType.simple,
    CommandID.solenoidEngageDuration: CommandType.simple,
    CommandID.pidTargetFreq: CommandType.simple,
    CommandID.pidMaxError: CommandType.simple,
    CommandID.bowHarmonicShift: CommandType.simple,
    CommandID.bowHarmonic: CommandType.simple,
    CommandID.bowHarmonicBase: CommandType.simple,
    CommandID.bowHarmonicShiftRange: CommandType.simple,
    CommandID.bowHarmonicShift5: CommandType.simple,
    CommandID.bowHarmonicAdd: CommandType.simple,

    CommandID.midiConfigurationSelect : CommandType.index,
    CommandID.actuatorSelect : CommandType.index,
    CommandID.harmonicSeriesSelect : CommandType.index
}

from commandparser import derivedCommandList, derivedCommandItem

class CommandSet:
    commandID = None
    indexingChild = None

    def __init__(self):
        self.CommandItem = derivedCommandItem
        self.CommandList = derivedCommandList

        self.fromVer = 0
        self.toVer = 99999999999999

        self.commandTypes = defaultCommandType

        self.shortCommands: dict = {}
        self.longCommands: dict = {}

        self.shortID: dict = {}
        self.longID: dict = {}

    def postInit(self):
        self.shortID = {v: k for k, v in self.shortCommands.items()}
        self.longID = {v: k for k, v in self.longCommands.items()}

    def initialRequest(self) -> list:
        return []

    def requestData(self, serialHandler) -> list:
        return []

    def requestContinuousData(self, serialHandler):
        pass

    def buildHierarchy(self, commandItem):
        pass

    def getCommandType(self, commandItem):
        pass

    def getQualifiedShortCommand(self, commandID, selectionIndex=None, stripIndex = False):
        pass

    def getCommandID(self, inCommand, module = None):
        revCID = dict(zip(self.longCommands.values(), self.longCommands.keys()))
        if (inCommand in revCID): return revCID[inCommand]

        revCID = dict(zip(self.shortCommands.values(), self.shortCommands.keys()))
        if (inCommand in revCID): return revCID[inCommand]

        return None

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        cId = self.getCommandID(commandItem)

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
                mainWidget.handleMIDIConfigurationName(commandItem.argument[0])

            case CommandID.controlBoxDataReturn:
                mainWidget.handleControlBoxReturnData(commandItem.argument[0], commandItem.argument[1])

            case CommandID.actuatorCount:
                mainWidget.ui.comboBoxActuatorPreset.clear()
                for a in range(0, int(commandItem.argument[0])):
                    serialHandler.write("rqi:bad:" + str(a))

            case CommandID.actuatorData:
                if (len(commandItem.argument) < 5):
                    # break
                    raise ("Something is wrong in BAD command")
                mainWidget.handleActuatorData(commandItem.argument[4], commandItem.argument[0], commandItem.argument[3], commandItem.argument[1], commandItem.argument[2])

            case CommandID.moduleSelect:
                mainWidget.addModulesIfNeeded(0)

            case CommandID.moduleCount:
                global moduleCount
                try:
                    moduleCount = int(commandItem.argument[0])
                    mainWidget.addModulesIfNeeded(moduleCount - 1)
                except:
                    mainWidget.messageBox("Error", "Error retreiving module count!")

            case CommandID.midiConfigurationSelect:
                simpleFARHandler.stringModules[0].setCommandValue(CommandID.midiConfigurationSelect, commandItem.argument[0])
                mainWidget.handleMIDIConfigurationSelect(commandItem.argument[0])
                serialHandler.write("rqi:mev")

            case CommandID.midiConfigurationCount:
                simpleFARHandler.stringModules[0].setCommandValue(CommandID.midiConfigurationCount, commandItem.argument[0])
                mainWidget.handleMIDIConfigurationCount(commandItem.argument[0])
                for a in range(0, int(commandItem.argument[0])):
                    serialHandler.write("rqi:mcfn:" + str(a))

            case CommandID.midiConfigurationData:
                match commandItem.argument[0]:
                    case "noteon":
                        mainWidget.setMIDINoteOnCommands(commandItem.argument[1])
                    case "noteoff":
                        mainWidget.setMIDINoteOffCommands(commandItem.argument[1])
                    case "cc":
                        mainWidget.setMIDICCCommands(commandItem.argument[1],commandItem.argument[2])
                    case "pat":
                        mainWidget.setMIDIPATCommands(commandItem.argument[1])
                    case "pb":
                        mainWidget.setMIDIPBCommands(commandItem.argument[1])
                    case "cat":
                        mainWidget.setMIDICATCommands(commandItem.argument[1])
                    case "pc":
                        mainWidget.setMIDIPBCommands(commandItem.argument[1])

            case CommandID.midiConfigurationName:
                mainWidget.handleMIDIConfigurationName(commandItem.argument[0], str(commandItem.argument[1]), True)

            case CommandID.midiReceiveChannel:
                mainWidget.handleMIDIReceiveChannel(commandItem.argument[0])

            case CommandID.controlBoxControlData:
                mainWidget.handleControlBoxControlData(commandItem.argument[0], commandItem.argument[1])

            case CommandID.bowHarmonic | CommandID.bowHarmonicShift | CommandID.bowHarmonicShift5 | CommandID.bowHarmonicBase | CommandID.bowHarmonicAdd:
                rqTg = self.getQualifiedShortCommand(CommandID.pidTargetFreq)[0]
                serialHandler.write("rqi:" + rqTg)

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

    def setHarmonicSeriesRatio(self, sender, serialHandler, simpleFARHandler, harmonicSeries, ratioIndex, ratio):
        qualifiedShort = self.getQualifiedShortCommand(CommandID.harmonicSeriesRatio, [harmonicSeries])[0]
        serialHandler.write(qualifiedShort + ":"+ str(ratioIndex) + ":" + str(ratio))

    def addHarmonicSeriesRatio(self, sender, serialHandler, simpleFARHandler, harmonicSeries):
        ratioIndex = len(simpleFARHandler.stringModules[0].harmonicData)
        self.setHarmonicSeriesRatio(sender, serialHandler, simpleFARHandler, harmonicSeries, ratioIndex, 1)
        serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.harmonicSeriesData)[0] + ":" + str(harmonicSeries))

    def removeHarmonicSeriesRatio(self, sender, serialHandler, simpleFARHandler, harmonicSeries, ratioIndex):
        qualifiedShort = self.getQualifiedShortCommand(CommandID.harmonicSeriesRemoveRatio, [harmonicSeries])[0]
        serialHandler.write(qualifiedShort + ":"+ str(ratioIndex))

    def setHarmonicSeriesSelect(self, sender, serialHandler, simpleFARHandler, index):
        if (index == -1): index = 0
        simpleFARHandler.stringModules[0].setCommandValue(CommandID.harmonicSeriesSelect, index)
        if (not sender.updatingFromModule):
            qualifiedShort = self.getQualifiedShortCommand(CommandID.harmonicSeriesSelect, [index])[0]
            serialHandler.write(qualifiedShort + ":"+ str(index))
    '''
    def saveHarmonicSeries(self, sender, serialHandler, simpleFARHandler, harmonicSeries, name, setToList):
        qualifiedShort = self.getQualifiedShortCommand(CommandID.harmonicSeriesSave, [harmonicSeries])[0]
        serialHandler.write(qualifiedShort + ":"+ str(harmonicSeries) + ":'" + name + "'")
        serialHandler.write(self.getQualifiedShortCommand(CommandID.harmonicSeriesCount)[0] + ":" + str(harmonicSeries))
        if (setToList): serialHandler.write(self.getQualifiedShortCommand(CommandID.harmonicSeriesSelect)[0] + ":" + str(harmonicSeries))
    '''

    def addHarmonicSeries(self, sender, serialHandler, simpleFARHandler, harmonicSeries, name, setToList):
        qualifiedShort = self.getQualifiedShortCommand(CommandID.harmonicSeriesAdd)[0]
        serialHandler.write(qualifiedShort + ":'" + name + "'")
        #serialHandler.write(self.getQualifiedShortCommand(CommandID.harmonicSeriesCount)[0] + ":" + str(harmonicSeries))
        if (setToList): serialHandler.write(self.getQualifiedShortCommand(CommandID.harmonicSeriesSelect)[0] + ":" + str(harmonicSeries))

    def removeHarmonicSeries(self, sender, serialHandler, simpleFARHandler, harmonicSeries):
        qualifiedShort = self.getQualifiedShortCommand(CommandID.harmonicSeriesRemove)[0]
        serialHandler.write(qualifiedShort + ":"+ str(harmonicSeries))
        #harmonicSeries = harmonicSeries - 1
        #if (harmonicSeries < 0): harmonicSeries = 0
        #serialHandler.write(self.getQualifiedShortCommand(CommandID.harmonicSeriesCount)[0])
        #serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.harmonicSeriesSelect)[0] + ":" + str(harmonicSeries))

    def renameHarmonicSeries(self, sender, serialHandler, simpleFARHandler, harmonicSeries, name):
        setHSData = self.getQualifiedShortCommand(CommandID.harmonicSeriesName, [harmonicSeries])[0]
        serialHandler.write(setHSData + ":'" + name + "'")

    def setHarmonicSeriesData(self, sender, serialHandler, simpleFARHandler, harmonicSeries, name, data):
        setHSData = self.getQualifiedShortCommand(CommandID.harmonicSeriesData, [harmonicSeries])[0]
        comm = setHSData + ":'" + name + "'"
        for d in data: comm += ":" + str(d)
        serialHandler.write(comm)
    '''
    def saveActuator(self, sender, serialHandler, simpleFARHandler, newIndex, name, rest = 0, engage = 2000, stall = 60000):
        bowActuatorSave = self.getQualifiedShortCommand(CommandID.actuatorSave)[0]
        serialHandler.write(bowActuatorSave + ":" + str(newIndex) + ":'" + name + "',ba:" + str(newIndex) + ",bac")
    '''
    def loadActuator(self, sender, serialHandler, simpleFARHandler, index):
        actuatorLoad = self.getQualifiedShortCommand(CommandID.actuatorSelect)[0]
        bowPressureMax = self.getQualifiedShortCommand(CommandID.bowPressurePositionMax)[0]
        bowPressureEngage = self.getQualifiedShortCommand(CommandID.bowPressurePositionEngage)[0]
        bowPressureRest = self.getQualifiedShortCommand(CommandID.bowPressurePositionRest)[0]
        serialHandler.write(actuatorLoad + ":" + str(index) + ",rqi:" + bowPressureMax + ",rqi:" + bowPressureEngage + ",rqi:" + bowPressureRest)

    def addActuator(self, sender, serialHandler, simpleFARHandler, newIndex, name):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.actuatorAdd)[0]
        serialHandler.write(qualifiedCommand + ":" + name)

    def removeActuator(self, sender, serialHandler, simpleFARHandler, index):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.actuatorRemove)[0]
        serialHandler.write(qualifiedCommand + ":" + str(index))

    def renameActuator(self, sender, serialHandler, simpleFARHandler, index, name):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.actuatorName, [index])[0]
        serialHandler.write(qualifiedCommand + ":" + name)

class CommandSetOG(CommandSet):
    CommandItem = derivedCommandItem
    CommandList = derivedCommandList

    def __init__(self):
        super().__init__()

        self.fromVer = 0
        self.toVer = 20260111184309

        # self.commandTypes[CommandID.fundamentalFrequency] = CommandSets.CommandType.advanced

        self.shortCommands = {
            CommandID.calibrateAll: "bca",
            CommandID.calibrateBowSpeed: "bcs",
            CommandID.calibrateBowPressure: "bcp",
            CommandID.calibrateMute: "mca",
            CommandID.nop: "nop",
            CommandID.requestInfo: "rqi",
            CommandID.debugPrint: "dp",
            CommandID.saveAllParameters: "gsap",
            CommandID.loadAllParameters: "glap",
            CommandID.resetAllParameters: "grap",
            CommandID.userVariable: "guv",
            CommandID.expressionparserEvaluate: "epev",
            CommandID.reset: "rst",
            CommandID.nickName: "nick",
            CommandID.version: "ver",

            CommandID.moduleSelect: "m",
            CommandID.moduleCount: "mc",
            CommandID.pickupStringFrequency: "psf",
            CommandID.pickupAudioPeak: "pap",
            CommandID.pickupAudioRMS: "par",

            CommandID.bowSelect: "bow",
            CommandID.bowStatus: "bs",
            CommandID.bowSpeedMode: "bcsm",
            CommandID.bowMotorTimeout: "bmt",
            CommandID.bowHome: "bh",
            CommandID.bowPIDEnable: "bpid",

            CommandID.pidTargetFreq: "bcf",
            CommandID.bowFundamental: "bcu",
            CommandID.bowHarmonic: "bch",
            CommandID.bowHarmonicAdd: "bcha",
            CommandID.bowHarmonicBase: "bchb",
            CommandID.bowHarmonicBaseNote: "bchbn",
            CommandID.bowHarmonicShift: "bchsh",
            CommandID.bowHarmonicShiftRange: "bchsr",
            CommandID.bowHarmonicShift5: "bchs5",
            CommandID.bowMeasureTimeToTarget: "bdmtt",

            CommandID.harmonicSeriesSelect: "bhs",
            CommandID.harmonicSeriesData: "bhsd",
            CommandID.harmonicSeriesRatio: "bhsr",
            CommandID.harmonicSeriesRemoveRatio: "bhsrr",
            CommandID.harmonicSeriesCount: "bhsc",
            CommandID.harmonicSeriesSave: "bhss",
            CommandID.harmonicSeriesRemove: "bhsrm",

            CommandID.actuatorSelect: "ba",
            CommandID.actuatorRemove: "bar",
            CommandID.actuatorSave: "bas",
            CommandID.actuatorData: "bad",
            CommandID.actuatorCount: "bac",

            CommandID.motorRun: "bmr",
            CommandID.motorDirectPWM: "bmdp",
            CommandID.motorVoltage: "bmv",
            CommandID.motorCurrent: "bmc",
            CommandID.motorCurrentLimit: "bmcl",
            CommandID.motorPowerLimit: "bmpl",
            CommandID.motorFrequency: "bmf",
            CommandID.motorEmergencyStop: "bmes",
            CommandID.motorPWMMax: "bmsx",
            CommandID.motorPWMMin: "bmsi",
            CommandID.motorFaultCommands: "bmfc",
            CommandID.motorOverPowerCommands: "bmopc",

            CommandID.pidKi: "bpki",
            CommandID.pidKp: "bpkp",
            CommandID.pidKd: "bpkd",
            CommandID.pidIntegratorError: "bpie",
            CommandID.pidReset: "bpir",
            CommandID.pidMaxError: "bpme",
            CommandID.pidPeakError: "bpperr",

            CommandID.bowPressureBaseline: "bpb",
            CommandID.bowPressureModifier: "bpm",
            CommandID.bowPressureRest: "bpr",
            CommandID.bowPressureEngage: "bpe",
            CommandID.bowPressurePositionMax: "bppx",
            CommandID.bowPressurePositionEngage: "bppe",
            CommandID.bowPressurePositionRest: "bppr",
            CommandID.bowPressureEngageSpeed: "bpes",
            CommandID.bowPressureModulationSpeed: "bpms",
            CommandID.bowPressureHold: "bph",

            CommandID.solenoidSelect: "so",
            CommandID.solenoidEngage: "se",
            CommandID.solenoidDisengage: "sd",
            CommandID.solenoidMaxForce: "sxf",
            CommandID.solenoidMinForce: "sif",
            CommandID.solenoidForceMultiplier: "sfm",
            CommandID.solenoidEngageDuration: "sed",

            CommandID.muteSetPosition: "msp",
            CommandID.muteFullMute: "mfm",
            CommandID.muteHalfMute: "mhm",
            CommandID.muteRest: "mr",
            CommandID.muteSaveFull: "msf",
            CommandID.muteSaveHalf: "msh",
            CommandID.muteSaveRest: "msr",
            CommandID.muteFullMutePosition: "mfmp",
            CommandID.muteHalfMutePosition: "mhmp",
            CommandID.muteRestPosition: "mrp",
            CommandID.muteSustain: "ms",
            CommandID.muteBackoff: "mbo",
            CommandID.muteHome: "mh",

            CommandID.midiConfigurationSelect: "mcf",
            CommandID.midiConfigurationAdd: "mcfa",
            CommandID.midiConfigurationRemove: "mcfr",
            CommandID.midiConfigurationCount: "mcfc",
            CommandID.midiConfigurationName: "mcfn",
            CommandID.midiConfigurationData: "mev",
            CommandID.midiConfigurationRemoveCC: "mevcr",
            CommandID.midiConfigurationDefaults: "mcfd",
            CommandID.midiReceiveChannel: "mrc",
            CommandID.midiAllNotesOff: "mano",

            CommandID.controlBoxControlData: "acm",
            CommandID.controlBoxControlDefaults: "acd",
            CommandID.controlBoxDataReturn: "adcr",
            CommandID.controlBoxADCSettings: "adcs",

            CommandID.testADCLatency: "tal",
            CommandID.testADCLatencyReturn: "talr",
            CommandID.testADCMinMax: "tamm"

        }

        self.longCommands = {
            CommandID.nop: "nop",
            CommandID.requestInfo: "requestinfo",
            CommandID.debugPrint: "debugprint",
            CommandID.saveAllParameters: "globalsaveallparameters",
            CommandID.loadAllParameters: "globalloadallparameters",
            CommandID.resetAllParameters: "globalresetallparameters",
            CommandID.userVariable: "globaluservariable",
            CommandID.expressionparserEvaluate: "expressionparserevaluate",
            CommandID.reset: "reset",
            CommandID.nickName: "nick",
            CommandID.version: "ver",

            CommandID.moduleSelect: "module",
            CommandID.moduleCount: "modulecount",
            CommandID.calibrateAll: "bowcalibrateall",
            CommandID.calibrateBowSpeed: "bowcalibratespeed",
            CommandID.calibrateBowPressure: "bowcalibratepressure",
            CommandID.calibrateMute: "mutecalibrate",
            CommandID.pickupStringFrequency: "pickupstringfrequency",
            CommandID.pickupAudioPeak: "pickupaudiopeak",
            CommandID.pickupAudioRMS: "pickupaudiorms",

            CommandID.bowSelect: "bow",
            CommandID.bowStatus: "bowstatus",
            CommandID.bowSpeedMode: "bowcontrolspeedmode",
            CommandID.bowMotorTimeout: "bowmotortimeout",
            CommandID.bowHome: "bowhome",
            CommandID.bowPIDEnable: "bowpid",

            CommandID.pidTargetFreq: "bowcontrolfrequency",
            CommandID.bowFundamental: "bowcontrolfundamental",
            CommandID.bowHarmonic: "bowcontrolharmonic",
            CommandID.bowHarmonicAdd: "bowcontrolharmonicadd",
            CommandID.bowHarmonicBase: "bowcontrolharmonicbase",
            CommandID.bowHarmonicBaseNote: "bowcontrlharmonicbasenote",
            CommandID.bowHarmonicShift: "bowcontrolharmonicshift",
            CommandID.bowHarmonicShiftRange: "bowcontrolharmonicshiftrange",
            CommandID.bowHarmonicShift5: "bowcontrolharmonicshift5",
            CommandID.bowMeasureTimeToTarget: "bowdebugmeasuretimetotarget",

            CommandID.harmonicSeriesSelect: "bowharmonicseries",
            CommandID.harmonicSeriesData: "bowharmonicseriesdata",
            CommandID.harmonicSeriesRatio: "bowharmonicseriesratio",
            CommandID.harmonicSeriesRemoveRatio: "bowharmonicseriesratioremove",
            CommandID.harmonicSeriesCount: "bowharmonicseriescount",
            CommandID.harmonicSeriesSave: "bowharmonicseriessave",
            CommandID.harmonicSeriesRemove: "bowharmonicseriesremove",

            CommandID.actuatorSelect: "bowactuator",
            CommandID.actuatorRemove: "bowactuatorremove",
            CommandID.actuatorSave: "bowactuatorsave",
            CommandID.actuatorData: "bowactuatordata",
            CommandID.actuatorCount: "bowactuatorcount",

            CommandID.motorRun: "bowmotorrun",
            CommandID.motorDirectPWM: "bowmotordirectpwm",
            CommandID.motorVoltage: "bowmotorvoltage",
            CommandID.motorCurrent: "bowmotorcurrent",
            CommandID.motorCurrentLimit: "bowmotorcurrentlimit",
            CommandID.motorPowerLimit: "bowmotorpowerlimit",
            CommandID.motorFrequency: "bowmotorfrequency",
            CommandID.motorEmergencyStop: "bowmotoremergencystop",
            CommandID.motorPWMMax: "bowmotorspeedmax",
            CommandID.motorPWMMin: "bowmotorspeedmin",
            CommandID.motorFaultCommands: "bowmotorfaultcommands",
            CommandID.motorOverPowerCommands: "bowmotoroverpowercommands",

            CommandID.pidKi: "bowpidki",
            CommandID.pidKp: "bowpidkp",
            CommandID.pidKd: "bowpidkd",
            CommandID.pidIntegratorError: "bowpidintegratorerror",
            CommandID.pidReset: "bowpidr",
            CommandID.pidMaxError: "bowpidmaxerror",
            CommandID.pidPeakError: "bowpidpeakerror",

            CommandID.bowPressureBaseline: "bowpressurebaseline",
            CommandID.bowPressureModifier: "bowpressuremodifier",
            CommandID.bowPressureRest: "bowpressurerest",
            CommandID.bowPressureEngage: "bowpressureengage",
            CommandID.bowPressurePositionMax: "bowpressurepositionmax",
            CommandID.bowPressurePositionEngage: "bowpressurepositionengage",
            CommandID.bowPressurePositionRest: "bowpressurepositionrest",
            CommandID.bowPressureEngageSpeed: "bowpressureengagespeed",
            CommandID.bowPressureModulationSpeed: "bowpressuremodulationspeed",
            CommandID.bowPressureHold: "bowpressurehold",

            CommandID.solenoidSelect: "solenoid",
            CommandID.solenoidEngage: "solenoidengage",
            CommandID.solenoidDisengage: "solenoiddisengage",
            CommandID.solenoidMaxForce: "solenoidmaxforce",
            CommandID.solenoidMinForce: "solenoidminforce",
            CommandID.solenoidForceMultiplier: "solenoidforcemultiplier",
            CommandID.solenoidEngageDuration: "solenoidengageduration",

            CommandID.muteSetPosition: "mutesetposition",
            CommandID.muteFullMute: "mutefullmute",
            CommandID.muteHalfMute: "mutehalfmute",
            CommandID.muteRest: "muterest",
            CommandID.muteSaveFull: "mutesavefull",
            CommandID.muteSaveHalf: "mutesavehalf",
            CommandID.muteSaveRest: "mutesaverest",
            CommandID.muteFullMutePosition: "mutefullmuteposition",
            CommandID.muteHalfMutePosition: "mutehalfmuteposition",
            CommandID.muteRestPosition: "muterestposition",
            CommandID.muteSustain: "mutesustain",
            CommandID.muteBackoff: "mutebackoff",
            CommandID.muteHome: "mutehome",

            CommandID.midiConfigurationSelect: "midiconfiguration",
            CommandID.midiConfigurationAdd: "midiconfigurationadd",
            CommandID.midiConfigurationRemove: "midiconfigurationremove",
            CommandID.midiConfigurationCount: "midiconfigurationcount",
            CommandID.midiConfigurationName: "midiconfigurationname",
            CommandID.midiConfigurationData: "midieventhandler",
            CommandID.midiConfigurationRemoveCC: "midieventhandlerccremove",
            CommandID.midiConfigurationDefaults: "midiconfigurationdefaults",
            CommandID.midiReceiveChannel: "midireceivechannel",
            CommandID.midiAllNotesOff: "midiallnotesoff",

            CommandID.controlBoxControlData: "adccommandmap",
            CommandID.controlBoxControlDefaults: "adcdefaults",
            CommandID.controlBoxDataReturn: "adcread",
            CommandID.controlBoxADCSettings: "adcsettings",

            CommandID.testADCLatency: "testadclatency",
            CommandID.testADCLatencyReturn: "testadclatencyreturn",
            CommandID.testADCMinMax: "testadcminmax"
        }

        super().postInit()

    def initialRequest(self):
        return ["help"]

    def requestData(self, serialHandler):
        serialHandler.write("rqi:bcu")
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

        serialHandler.write("rqi:bowcontrolharmonic")
        serialHandler.write("rqi:bowcontrolharmonicbase")
        serialHandler.write("rqi:bowcontrolharmonicbasenote")
        serialHandler.write("rqi:bowcontrolharmonicadd")
        serialHandler.write("rqi:bowcontrolharmonicshift")
        serialHandler.write("rqi:bowcontrolharmonicshiftrange")
        serialHandler.write("rqi:bowcontrolharmonicshift5")
        serialHandler.write("rqi:bowcontrolfrequency")

        serialHandler.write("rqi:bowharmonicseriescount")
        serialHandler.write("rqi:bowharmonicseries")

        serialHandler.write("rqi:midiconfigurationcount")
        serialHandler.write("rqi:midiconfiguration")

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
        pass

    def requestContinuousData(self, serialHandler):
        serialHandler.write("rqi:pickupstringfrequency")
        serialHandler.write("rqi:pickupaudiopeak")
        serialHandler.write("rqi:pickupaudiorms")
        serialHandler.write("rqi:bowmotorfrequency")
        serialHandler.write("rqi:bowmotorcurrent")
        serialHandler.write("rqi:bowcontrolfrequency")
        serialHandler.write("rqi:bowpidpeakerror")

    def buildHierarchy(self, commandItem):
        return

    def getCommandType(self, ci):
        if (ci.command in self.shortID):
            cId = self.shortID[ci.command]
        elif (ci.command in self.longID):
            cId = self.longID[ci.command]
        else:
            return CommandType.undefined
        if (cId in self.commandTypes):
            return self.commandTypes[cId]
        else:
            return CommandType.undefined

    def getQualifiedShortCommand(self, commandID, selectionIndex = None, stripIndex = False):
        if (commandID in self.shortCommands):
            comm = self.shortCommands[commandID]
        elif (commandID in self.longCommands):
            comm = self.longCommands[commandID]
        if (selectionIndex is not None):
            pass
        return [comm]

    def getCommandID(self, ci, module = None):
        if (ci.command in self.shortID):
            cId = self.shortID[ci.command]
        elif (ci.command in self.longID):
            cId = self.longID[ci.command]
        else:
            cId = None;
            #raise("Command not found!")
        return cId

#    def setMidiConfigurationSelect(self, sender, serialHandler, index):
#        serialHandler.write("midiconfiguration:" + str(index))

    def setHarmonicSeriesSelect(self, sender, serialHandler, simpleFARHandler, index):
        super().setHarmonicSeriesSelect(sender, serialHandler, simpleFARHandler, index)
        if (not sender.updatingFromModule):
            serialHandler.write("rqi:bhsd:" + str(index))

    def addHarmonicSeries(self, sender, serialHandler, simpleFARHandler, harmonicSeries, name, setToList):
        self.saveHarmonicSeries(sender, serialHandler, simpleFARHandler, simpleFARHandler.stringModules[0].getCommandValue(CommandID.harmonicSeriesCount),
                                name, setToList)


class CommandSetModular(CommandSet):
    class Base(CommandSet):
        longName = ""
        shortName = ""
        index = False

        def __init__(self):
            super().__init__()
            self.postInit()
            pass

        shortCommands = {
            CommandID.nop : "nop",
            CommandID.requestInfo : "rqi",
            CommandID.debugPrint : "dp",
            CommandID.saveAllParameters : "sap",
            CommandID.loadAllParameters : "lap",
            CommandID.resetAllParameters : "rap",
            CommandID.userVariable : "uv",
            CommandID.expressionparserEvaluate : "evep",
            CommandID.ifEqual : "ife",
            CommandID.ifGreater : "ifg",
            CommandID.ifLess : "ifl",
            CommandID.reset : "rst",
            CommandID.nickName : "nick",
            CommandID.dir : "dir",
            #dir, dump, freeram

            CommandID.moduleSelect: "[na]",
            CommandID.moduleCount: "[na]",
            CommandID.calibrateAll : "ca",
            CommandID.calibrateBowSpeed : "cbs",
            CommandID.calibrateBowPressure: "cbp",
            CommandID.calibrateMute: "cmu",
            CommandID.pickupStringFrequency: "psf",
            CommandID.pickupAudioPeak: "pap",
            CommandID.pickupAudioRMS: "par",
            CommandID.version: "ver"
        }

        longCommands = {
            CommandID.nop: "nop",
            CommandID.requestInfo: "requestinfo",
            CommandID.debugPrint: "debugprint",
            CommandID.saveAllParameters: "saveallparameters",
            CommandID.loadAllParameters: "loadallparameters",
            CommandID.resetAllParameters: "resetallparameters",
            CommandID.userVariable: "uservariable",
            CommandID.expressionparserEvaluate: "expressionparserevaluate",
            CommandID.ifEqual: "ifequal",
            CommandID.ifGreater: "ifgreater",
            CommandID.ifLess: "ifless",
            CommandID.reset: "reset",
            CommandID.nickName: "nick",
            CommandID.dir: "dir",

            CommandID.moduleSelect: "[na]",
            CommandID.moduleCount: "[na]",
            CommandID.calibrateAll: "calibrateall",
            CommandID.calibrateBowSpeed: "calibratebowspeed",
            CommandID.calibrateBowPressure: "calibratebowpressure",
            CommandID.calibrateMute: "calibratemute",
            CommandID.pickupStringFrequency: "pickupstringfrequency",
            CommandID.pickupAudioPeak: "pickupaudiopeak",
            CommandID.pickupAudioRMS: "pickupaudiorms",
            CommandID.version: "version"
        }

        requestData = [ CommandID.nickName, CommandID.debugPrint ]

        requestContinuousData = [ CommandID.pickupStringFrequency, CommandID.pickupAudioPeak, CommandID.pickupAudioRMS ]

    class BowingWheel(CommandSet):
        longName = "bowingwheel"
        shortName = "bw"
        index = True
        commandID = CommandID.bowSelect

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.bowStatus: "[na]",
            CommandID.bowSpeedMode: "sm",
            CommandID.bowMotorTimeout: "mt",
            CommandID.bowPIDEnable: "pe",
            CommandID.motorFaultCommands: "mfc",
            CommandID.motorOverPowerCommands: "moc"
        }

        longCommands = {
            CommandID.bowStatus: "[na]",
            CommandID.bowSpeedMode: "speedmode",
            CommandID.bowMotorTimeout: "motortimeout",
            CommandID.bowPIDEnable: "pidenable",
            CommandID.motorFaultCommands: "motorfaultcommands",
            CommandID.motorOverPowerCommands: "motoroverpowercommands",
        }

        requestData = [
            CommandID.bowMotorTimeout, CommandID.motorFaultCommands, CommandID.motorOverPowerCommands
        ]

        requestContinuousData = []

    class HarmonicSeriesHandler(CommandSet):
        longName = "harmonicserieshandler"
        shortName = "hsh"
        index = False
        indexingChild = "harmonicseries"

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.bowFundamental: "fu",
            CommandID.bowHarmonic : "h",
            CommandID.bowHarmonicAdd : "ha",
            CommandID.bowHarmonicBase : "hb",
            CommandID.bowHarmonicBaseNote : "bn",
            CommandID.bowHarmonicShift : "sh",
            CommandID.bowHarmonicShiftRange : "sr",
            CommandID.bowHarmonicShift5 : "sh5",
            CommandID.harmonicSeriesAdd : "a",
            CommandID.harmonicSeriesRemove : "rm",
            CommandID.harmonicSeriesCount : "c",
            CommandID.harmonicSeriesSelect : "hs"
        }

        longCommands = {
            CommandID.bowFundamental: "fundamental",
            CommandID.bowHarmonic : "harmonic",
            CommandID.bowHarmonicAdd : "harmonicadd",
            CommandID.bowHarmonicBase : "harmonicbase",
            CommandID.bowHarmonicBaseNote : "basenote",
            CommandID.bowHarmonicShift : "shift",
            CommandID.bowHarmonicShiftRange : "shiftrange",
            CommandID.bowHarmonicShift5 : "shift5",

            CommandID.harmonicSeriesAdd : "add",
            CommandID.harmonicSeriesRemove : "remove",
            CommandID.harmonicSeriesCount : "count",
            CommandID.harmonicSeriesSelect : "harmonicseries"
        }

        requestData = [
            CommandID.bowFundamental, CommandID.bowHarmonicShiftRange, CommandID.harmonicSeriesCount, CommandID.harmonicSeriesSelect,
            CommandID.bowHarmonicBaseNote
        ]

        requestContinuousData = []

    class HarmonicSeries(CommandSet):
        longName = "harmonicseries"
        shortName = "hs"
        index = True
        #commandID = CommandID.harmonicSeriesSelect

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.harmonicSeriesSave : "[na]",
            CommandID.harmonicSeriesName : "na",
            CommandID.harmonicSeriesData : "da",
            CommandID.harmonicSeriesRatio : "r",
            CommandID.harmonicSeriesRemoveRatio : "rm"
        }

        longCommands = {
            CommandID.harmonicSeriesSave : "[na]",
            CommandID.harmonicSeriesName : "name",
            CommandID.harmonicSeriesData : "data",
            CommandID.harmonicSeriesRatio : "ratio",
            CommandID.harmonicSeriesRemoveRatio : "remove",
        }

        requestData = [
            #CommandID.harmonicSeriesName, CommandID.harmonicSeriesData
        ]

        requestContinuousData = []

    class BowActuatorHandler(CommandSet):
        longName = "actuatorhandler"
        shortName = "ah"
        index = False
        indexingChild = "actuator"

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.actuatorAdd : "a",
            CommandID.actuatorRemove : "rm",
            CommandID.actuatorCount : "c",
            CommandID.actuatorSelect : "ac"
        }

        longCommands = {
            CommandID.actuatorAdd : "add",
            CommandID.actuatorRemove : "remove",
            CommandID.actuatorCount : "count",
            CommandID.actuatorSelect : "actuator"
        }

        requestData = [ CommandID.actuatorCount, CommandID.actuatorSelect ]
        requestContinuousData = []

    class Actuator(CommandSet):
        longName = "actuator"
        shortName = "ac"
        index = True
        commandID = CommandID.actuatorSelect

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.actuatorSave : "[na]",
            CommandID.actuatorData : "da",
            CommandID.actuatorName : "na"
        }

        longCommands = {
            CommandID.actuatorSave : "[na]",
            CommandID.actuatorData: "data",
            CommandID.actuatorName: "name",
        }

        requestData = [
            #CommandID.actuatorName, CommandID.actuatorData
        ]

        requestContinuousData = []

    class DCMotor(CommandSet):
        longName = "dcmotor"
        shortName = "dcm"
        index = True

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.motorRun : "ru",
            CommandID.motorDirectPWM : "pwm",
            CommandID.motorVoltage : "vo",
            CommandID.motorCurrent : "cu",
            CommandID.motorCurrentLimit : "cl",
            CommandID.motorPowerLimit : "pl",
            CommandID.motorFrequency : "fq",
            CommandID.motorEmergencyStop : "es",
            CommandID.motorPWMMax : "xp",
            CommandID.motorPWMMin : "ip",
        }

        longCommands = {
            CommandID.motorRun : "run",
            CommandID.motorDirectPWM : "pwm",
            CommandID.motorVoltage : "voltage",
            CommandID.motorCurrent : "current",
            CommandID.motorCurrentLimit : "currentlimit",
            CommandID.motorPowerLimit : "powerlimit",
            CommandID.motorFrequency : "frequency",
            CommandID.motorEmergencyStop : "emergencystop",
            CommandID.motorPWMMax : "maxpwm",
            CommandID.motorPWMMin : "minpwm",
        }

        requestData = [
            CommandID.motorVoltage, CommandID.motorCurrentLimit, CommandID.motorPowerLimit, CommandID.motorPWMMax, CommandID.motorPWMMin
        ]

        requestContinuousData = [
            CommandID.motorCurrent, CommandID.motorFrequency
        ]

    class PID(CommandSet):
        longName = "pid"
        shortName = "pid"
        index = True

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.pidTargetFreq : "tf",
            CommandID.pidKi: "ki",
            CommandID.pidKp: "kp",
            CommandID.pidKd: "kd",
            CommandID.pidIntegratorError: "ie",
            CommandID.pidReset: "re",
            CommandID.pidMaxError: "xe",
            CommandID.pidPeakError: "pe",
            CommandID.pidSpeedMax : "msx",
            CommandID.pidSpeedMin : "msi",
            CommandID.bowMeasureTimeToTarget: "mtt"
        }

        longCommands = {
            CommandID.pidTargetFreq : "targetfrequency",
            CommandID.pidKi: "ki",
            CommandID.pidKp: "kp",
            CommandID.pidKd: "kd",
            CommandID.pidIntegratorError: "integratorerror",
            CommandID.pidReset: "reset",
            CommandID.pidMaxError: "maxerror",
            CommandID.pidPeakError: "peakerror",
            CommandID.pidSpeedMax : "motorspeedmax",
            CommandID.pidSpeedMin : "motorspeedmin",
            CommandID.bowMeasureTimeToTarget: "measuretimetotarget",
        }

        requestData = [
            CommandID.pidKi, CommandID.pidKp, CommandID.pidKd, CommandID.pidIntegratorError, CommandID.pidMaxError, CommandID.pidSpeedMax,
            CommandID.pidSpeedMin
        ]

        requestContinuousData = []

    class BowPressure(CommandSet):
        longName = "bowpressure"
        shortName = "bp"
        index = False

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.bowPressureBaseline: "ba",
            CommandID.bowPressureModifier: "mo",
            CommandID.bowPressureRest: "rs",
            CommandID.bowPressureEngage: "en",
            CommandID.bowPressurePositionMax: "sp",
            CommandID.bowPressurePositionEngage: "ep",
            CommandID.bowPressurePositionRest: "rp",
            CommandID.bowPressureEngageSpeed: "es",
            CommandID.bowPressureModulationSpeed: "ms",
            CommandID.bowPressureHold: "hd",
            CommandID.bowHome: "hm"
        }

        longCommands = {
            CommandID.bowPressureBaseline: "baseline",
            CommandID.bowPressureModifier: "modifier",
            CommandID.bowPressureRest: "rest",
            CommandID.bowPressureEngage: "engage",
            CommandID.bowPressurePositionMax: "stallpressure",
            CommandID.bowPressurePositionEngage: "engagepressure",
            CommandID.bowPressurePositionRest: "restpressure",
            CommandID.bowPressureEngageSpeed: "engagespeed",
            CommandID.bowPressureModulationSpeed: "modulationspeed",
            CommandID.bowPressureHold: "hold",
            CommandID.bowHome: "home",
        }

        requestData = [
            CommandID.bowPressurePositionRest, CommandID.bowPressurePositionEngage, CommandID.bowPressurePositionMax, CommandID.bowPressureEngageSpeed,
            CommandID.bowPressureModulationSpeed
        ]

        requestContinuousData = []

    class Solenoid(CommandSet):
        longName = "solenoid"
        shortName = "so"
        index = True
        commandID = CommandID.solenoidSelect

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.solenoidEngage: "en",
            CommandID.solenoidDisengage: "rs",
            CommandID.solenoidMaxForce: "xf",
            CommandID.solenoidMinForce: "if",
            CommandID.solenoidForceMultiplier: "fm",
            CommandID.solenoidEngageDuration: "ed"
        }

        longCommands = {
            CommandID.solenoidEngage: "engage",
            CommandID.solenoidDisengage: "disengage",
            CommandID.solenoidMaxForce: "maxforce",
            CommandID.solenoidMinForce: "minforce",
            CommandID.solenoidForceMultiplier: "forcemultiplier",
            CommandID.solenoidEngageDuration: "engageduration"
        }

        requestData = [
            CommandID.solenoidMinForce, CommandID.solenoidMaxForce, CommandID.solenoidEngageDuration
        ]

        requestContinuousData = []

    class Mute(CommandSet):
        longName = "mute"
        shortName = "mu"
        index = True
        commandID = CommandID.muteSelect

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.muteSetPosition : "sp",
            CommandID.muteFullMute : "fm",
            CommandID.muteHalfMute : "hm",
            CommandID.muteRest : "rs",
            CommandID.muteSaveFull : "sf",
            CommandID.muteSaveHalf : "sh",
            CommandID.muteSaveRest : "sr",
            CommandID.muteFullMutePosition : "fmp",
            CommandID.muteHalfMutePosition : "hmp",
            CommandID.muteRestPosition : "rp",
            CommandID.muteSustain : "su",
            CommandID.muteBackoff : "bo",
            CommandID.muteHome : "hm",

            CommandID.muteSetHardwarePosition : "hwp",
            CommandID.muteCompleteTask : "cpt",
            CommandID.muteAutoCorrect : "ac",
            CommandID.muteHomingSensed : "hms",
            CommandID.muteMoveDirection : "md",
            CommandID.muteCurrentStep : "cs",
            CommandID.muteHomingPoint : "hmp",
            CommandID.muteHomingStage : "hms",
            CommandID.muteTMCInfo : "tmi"
        }

        longCommands = {
            CommandID.muteSetPosition : "setposition",
            CommandID.muteFullMute : "fullmute",
            CommandID.muteHalfMute : "halfmute",
            CommandID.muteRest : "rest",
            CommandID.muteSaveFull : "savefull",
            CommandID.muteSaveHalf : "savehalf",
            CommandID.muteSaveRest : "saverest",
            CommandID.muteFullMutePosition : "fullmuteposition",
            CommandID.muteHalfMutePosition : "halfmuteposition",
            CommandID.muteRestPosition : "restposition",
            CommandID.muteSustain : "sustain",
            CommandID.muteBackoff : "backoff",
            CommandID.muteHome : "home",

            CommandID.muteSetHardwarePosition : "hardwareposition",
            CommandID.muteCompleteTask : "completetask",
            CommandID.muteAutoCorrect : "autocorrect",
            CommandID.muteHomingSensed : "homingsensed",
            CommandID.muteMoveDirection : "movedirection",
            CommandID.muteCurrentStep : "currentstep",
            CommandID.muteHomingPoint : "homingpoint",
            CommandID.muteHomingStage : "homingstage",
            CommandID.muteTMCInfo : "tmcinfo",
        }

        requestData = [
            CommandID.muteFullMutePosition, CommandID.muteHalfMutePosition, CommandID.muteRestPosition, CommandID.muteBackoff
        ]

        requestContinuousData = []

    class MidiConfigurationHandler(CommandSet):
        longName = "midiconfigurationhandler"
        shortName = "mcf"
        index = False
        indexingChild = "midiconfiguration"

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.midiAllNotesOff : "ano",
            CommandID.midiConfigurationAdd : "a",
            CommandID.midiConfigurationRemove : "rm",
            CommandID.midiConfigurationCount : "c",
            CommandID.midiConfigurationSelect : "mc"
        }

        longCommands = {
            CommandID.midiAllNotesOff : "allnotesoff",
            CommandID.midiConfigurationAdd : "add",
            CommandID.midiConfigurationRemove : "remove",
            CommandID.midiConfigurationCount : "count",
            CommandID.midiConfigurationSelect: "midiconfiguration"
        }

        requestData = [ CommandID.midiConfigurationCount, CommandID.midiConfigurationSelect ]
        requestContinuousData = []

    class MidiConfiguration(CommandSet):
        longName = "midiconfiguration"
        shortName = "mc"
        index = True
        commandID = CommandID.midiConfigurationSelect

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.midiConfigurationName : "na",
            CommandID.midiConfigurationData : "da",
            CommandID.midiConfigurationAddCC : "ac",
            CommandID.midiConfigurationRemoveCC : "rmc",
            CommandID.midiConfigurationDefaults : "d",
            CommandID.midiReceiveChannel : "rc"
        }

        longCommands = {
            CommandID.midiConfigurationName : "name",
            CommandID.midiConfigurationData : "data",
            CommandID.midiConfigurationAddCC : "addcc",
            CommandID.midiConfigurationRemoveCC : "removecc",
            CommandID.midiConfigurationDefaults : "defaults",
            CommandID.midiReceiveChannel : "receivechannel",
        }

        requestData = [
            #CommandID.midiConfigurationName, CommandID.midiConfigurationData, CommandID.midiReceiveChannel
        ]

        requestContinuousData = []

    class ControlBox(CommandSet):
        longName = "controlbox"
        shortName = "cb"
        index = True

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.controlBoxControlData : "cda",
            CommandID.controlBoxControlDefaults : "cde",
            CommandID.controlBoxDataReturn : "dr",
            CommandID.controlBoxADCSettings : "ads",

            CommandID.testADCLatency : "tal",
            CommandID.testADCLatencyReturn : "talr",
            CommandID.testADCMinMax : "tix"
        }

        longCommands = {
            CommandID.controlBoxControlData : "controldata",
            CommandID.controlBoxControlDefaults : "controldefaults",
            CommandID.controlBoxDataReturn : "datareturn",
            CommandID.controlBoxADCSettings : "adcsettings",

            CommandID.testADCLatency : "testadclatency",
            CommandID.testADCLatencyReturn : "testadclatencyreturn",
            CommandID.testADCMinMax : "testadcminmax"
        }

        requestData = []

        requestContinuousData = []

    class Module:
        longName = ""
        shortName = ""
        moduleType = ""
        indexingChild = None
        commandSet = None
        index = 0
        parent = None

        def __init__(self, baseCommandSet, commandItem = None, itemCommandSet = None):
            self.commandSet = baseCommandSet
            self.index = 0
            if (commandItem is not None):
                if (len(commandItem.hierarchy[commandItem.hierarchyIndex].selection) > 0):
                    self.index = int(commandItem.hierarchy[commandItem.hierarchyIndex].selection[0])
            if (itemCommandSet is not None):
                #commandItem: CommandSet = commandItem
                self.longName = itemCommandSet.longName
                self.shortName = itemCommandSet.shortName
                if (itemCommandSet.indexingChild is not None):
                    self.indexingChild = itemCommandSet.indexingChild
            elif (commandItem is not None):
                self.longName = commandItem.argument[0].strip()
                self.shortName = commandItem.argument[1].strip()
                if hasattr(self, "moduleType"):
                    self.moduleType = commandItem.argument[3].strip()

    class Group(Module):
        def __init__(self, inCommandSet, commandItem = None):
            self.children = []
            super().__init__(inCommandSet, commandItem)
            pass

        def addModule(self, commandItem):
            child = CommandSetModular.Group(self.commandSet, commandItem)
            child.parent = self
            self.children.append(child)
            return self.children[-1]

        def remove(self, index):
            pass

    class GroupHandler(Module):
        def __init__(self, baseCommandSet, commandItem, itemCommandSet):
            super().__init__(baseCommandSet, commandItem, itemCommandSet)
            self.children = []

        def remove(self, item):
            index = self.children.index(item)
            self.children.remove(item)
            for i in range(index, len(self.children)):
                self.children[i].index -= 1
            pass

        def getGroups(self, name):
            toReturn = []
            for child in self.children:
                if ((child.longName == name) or (child.shortName == name)):
                    toReturn.append(child)
                else:
                    subChildren = child.getGroups(name)
                    for subChild in subChildren: toReturn.append(subChild)
            return toReturn

        def getGroupParsed(self, newItem, rootGroup = None, addGroups = False):
            try:
                groupName = newItem.hierarchy[newItem.hierarchyIndex].name
            except:
                raise("Group not found")
            thisItem = 0
            for group in rootGroup:
                if ((str(group.longName) == str(groupName)) or (str(group.shortName) == str(groupName))):
                    if (len(newItem.hierarchy) == 0 or (newItem.hierarchyIndex >= (len(newItem.hierarchy) - 1))):
                        if (len(newItem.hierarchy[newItem.hierarchyIndex].selection) == 0):
                            break
                        else:
                            if (int(newItem.hierarchy[newItem.hierarchyIndex].selection[0]) == group.index):
                                return group
                    else:
                        newItem.hierarchyIndex += 1
                        if (newItem.hierarchyIndex >= len(newItem.hierarchy)):
                            break
                        else:
                            return group.getGroupParsed(newItem, group.children, addGroups)
            if (addGroups):
                self.addGroupFromHierarchy(newItem)
                if (len(rootGroup) != 0):
                    group = rootGroup[-1]
                    if (newItem.hierarchyIndex < (len(newItem.hierarchy))):
                        group.getGroupParsed(newItem, group.children, True)
                else:
                    pass

        def getGroup(self, commandItem):
            return self.getGroupParsed(commandItem, self.children)

        def getGroupAndAddIfNone(self, commandItem):
            return self.getGroupParsed(commandItem, self.children, True)

        def addGroup(self, commandItem, commandGroup):
            child = self.commandSet.GroupHandler(self.commandSet, commandItem, commandGroup)
            child.parent = self
            self.children.append(child)
            return  self.children[-1]

        def addGroupFromHierarchy(self, commandItem):
            #if (commandItem.hierarchyIndex >= (len(commandItem.hierarchy) - 1)):
            #group = self.commandSet.GroupHandler(self.commandSet, commandItem)
            commandGroup = None
            for item in self.commandSet.commands:
                if (item.longName == commandItem.hierarchy[commandItem.hierarchyIndex].name or
                        item.shortName == commandItem.hierarchy[commandItem.hierarchyIndex].name):
                    commandGroup = item
                    break
            if (commandGroup == None):
                #raise("Unknown module!")
                pass
            else:
                #child = self.commandSet.GroupHandler(self.commandSet, commandItem, commandGroup)
                #chil
                #self.children.append()
                self.addGroup(commandItem, commandGroup)
                commandItem.hierarchyIndex += 1
            if (len(self.children) == 0):
                return None
            return  self.children[-1]

        def addModule(self, commandItem):
            self.getGroupAndAddIfNone(commandItem)

        def addModuleFromDirReturn(self, commandItem):
            newCommandItem = derivedCommandItem(commandItem.argument[0])
            self.addModule(newCommandItem)

    def getModuleTypeFromCommandID(self, commandID):
        moduleType = []
        for module in self.commands:
            if (commandID in module.longCommands) or (commandID == module.commandID):
                moduleType.append(module)
        return moduleType

    def getModulesByName(self, name):
        retModules = []
        for module in self.commands:
            if ((name == module.longName) or (name == module.shortName)):
                retModules.append(module)
        return retModules

    def getCommand(self, commandID, short = False):
        for module in self.commands:
            if (short):
                if commandID in module.shortCommands:
                    return module.shortCommands[commandID]
            else:
                if commandID in module.longCommands:
                    return module.longCommands[commandID]
        return None

    def getCommandType(self, commandItem):
        if ("rp" in commandItem.command):
            pass
        command, module = self._getCommandModuleAndCommand(commandItem)
        id = self.getCommandID(command, module)
        if (id in defaultCommandType):
            return defaultCommandType[id]
        return CommandType.undefined

    def getQualifiedShortCommand(self, commandID, selectionIndex = None, stripIndex = False):
        indexing = False
        qualifiedIDList = []
        moduleTypes = self.getModuleTypeFromCommandID(commandID)
        if (commandID in self.commandTypes):
            if (self.commandTypes[commandID] == CommandType.index):
                moduleTypes = self.getModulesByName(moduleTypes[0].indexingChild)
                indexing = True
        for moduleType in moduleTypes:
            if (moduleType.shortName == ""):
                base = self.commands[0]
                qualifiedIDList.append(base.shortCommands[commandID])
            else:
                allGroups = self.baseModule.getGroups(moduleType.shortName)
                if (allGroups is None):
                    raise("Problem")

                groups = []
                for group in allGroups:
                    if selectionIndex is None:
                        groups.append(group)
                    elif group.index in selectionIndex:
                        groups.append(group)
                if (len(groups) == 0):
                    #raise("another problem")
                    pass
                for group in groups:
                    qualifiedID = ""
                    if (qualifiedID != ""): qualifiedID = "." + qualifiedID
                    qualifiedID = group.shortName + qualifiedID
                    parent = group.parent
                    index = group.index
                    while(parent is not None):
                        parent = group.parent
                        if (parent.shortName != ""):
                            qualifiedID = parent.shortName + "." + qualifiedID
                        else:
                            break
                        if (parent is not None): group = parent
                    comm = self.getCommand(commandID, True)
                    if (comm is None):
                        comm = ""
                    else:
                        comm = "." + comm

                    if (not stripIndex): qualifiedID += "[" + str(index) + "]"
                    if (not indexing): qualifiedID += comm
                    qualifiedIDList.append(qualifiedID)
                    #if (stripIndex):
                    #    qualifiedIDList.append(qualifiedID + comm)
                    #elif (indexing):
                    #    qualifiedIDList.append(qualifiedID + "[" + str(index) + "]")
                    #else:
                    #    qualifiedIDList.append(qualifiedID + "[" + str(index) + "]" + comm)
        return qualifiedIDList

    def getCommandID(self, commandContainer, module = None):
        if (isinstance(commandContainer, self.CommandItem)):
            if (len(commandContainer.hierarchy) <= 1):
                module = ""
                command = commandContainer.hierarchy[0].name
            else:
                module = commandContainer.hierarchy[len(commandContainer.hierarchy) - 2].name
                command = commandContainer.hierarchy[len(commandContainer.hierarchy) - 1].name
        else:
            if (module is None):
                module = ""
            command = commandContainer

        for moduleP in self.commands:
            if (moduleP.longName == module) or (moduleP.shortName == module):
                id = moduleP.getCommandID(moduleP, command)
                return id

            for commandP in moduleP.longCommands:
                if (commandP == command):
                    id = moduleP.getCommandID(moduleP, command)
                    return id
            for commandP in moduleP.shortCommands:
                if (commandP == command):
                    id = moduleP.getCommandID(moduleP, command)
                    return id

            #if (module in group.longName) or (module in group.shortName):
        return None

    def initialRequest(self) -> list:
        return ["dir:m:r:i", "nop", "help", "nop"]

    def requestData(self, serialHandler):
        if (not self.hasHierarchy): return None
        for requestGroups in self.commands:
            for request in requestGroups.requestData:
                isIndex = False
                if (request in self.commandTypes):
                    if (self.commandTypes[request] == CommandType.index): isIndex = True
                if (isIndex):
                    qualifiedShort = self.getQualifiedShortCommand(request, [0], True)[0]
                    if (qualifiedShort is not None):
                        qualifiedShort += "[]"
                        serialHandler.write("rqi:" + qualifiedShort)
                else:
                    qualifiedShorts = self.getQualifiedShortCommand(request)
                    for qualifiedShort in qualifiedShorts:
                        if (isIndex): qualifiedShort += "[]"
                        serialHandler.write("rqi:" + qualifiedShort)

        #CommandID.controlBoxControlData, CommandID.controlBoxADCSettings
        cbd = self.getQualifiedShortCommand(CommandID.controlBoxControlData)[0]
        cba = self.getQualifiedShortCommand(CommandID.controlBoxADCSettings)[0]
        for i in range(0,8):
            serialHandler.write("rqi:" + cbd + ":" + str(i) + ",rqi:" + cba + ":" + str(i))

    def requestContinuousData(self, serialHandler):
        if (not self.hasHierarchy): return None
        for requestGroups in self.commands:
            for request in requestGroups.requestContinuousData:
                isIndex = False
                if (request in self.commandTypes):
                    if (self.commandTypes[request] == CommandType.index): isIndex = True
                if (isIndex):
                    qualifiedShort = self.getQualifiedShortCommand(request, [0], True)[0]
                    if (qualifiedShort is not None):
                        qualifiedShort += "[]"
                        serialHandler.write("rqi:" + qualifiedShort)
                else:
                    qualifiedShorts = self.getQualifiedShortCommand(request)
                    for qualifiedShort in qualifiedShorts:
                        if (isIndex): qualifiedShort += "[]"
                        serialHandler.write("rqi:" + qualifiedShort)

        cbd = self.getQualifiedShortCommand(CommandID.controlBoxControlData)[0]
        cba = self.getQualifiedShortCommand(CommandID.controlBoxADCSettings)[0]
        for i in range(0,7):
            serialHandler.write("rqi:" + cbd + ":" + str(i) + ",rqi:" + cba + ":" + str(i))

    def buildHierarchy(self, commandItem):
        #if ((len(commandItem.argument) != 4) or (commandItem.hierarchy[0].name != "dir")):
        #    return
        self.baseModule.addModuleFromDirReturn(commandItem)
        pass

    def _getCommandModuleAndCommand(self, commandItem):
        newCommandItem = derivedCommandItem(commandItem)
        newCommandItem.buildHierarchy()
        if (len(newCommandItem.hierarchy) <= 1):
            module = ""
            command = newCommandItem.hierarchy[0].name
        else:
            module = newCommandItem.hierarchy[len(newCommandItem.hierarchy) - 2].name
            command = newCommandItem.hierarchy[len(newCommandItem.hierarchy) - 1].name
        return command, module

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        command, module = self._getCommandModuleAndCommand(commandItem)
        if (command == "na"):
            pass
        id = self.getCommandID(command, module)

        if (id == None and command != "bpr" and command != "bmes" and command != "msi" and command != "msx" and command != "ver" and command != "dir" and
                command != "dp" and command != "fmp" and command != "hmp"):
            pass

        match(id):
            case CommandID.version:
                serialHandler.write("dir:m:r:i,nop")
                self.hasHierarchy = False
                pass

            case CommandID.dir:
                if (not self.hasHierarchy):
                    self.buildHierarchy(commandItem)

            case CommandID.nop:
                if (not self.hasHierarchy):
                    self.hasHierarchy = True
                    self.requestData(serialHandler)
                else:
                    pass

            case CommandID.midiConfigurationSelect:
                index = commandItem.hierarchy[len(commandItem.hierarchy) - 1].selection[0]
                mainWidget.handleMIDIConfigurationSelect(index)
                qualifiedShort = self.getQualifiedShortCommand(CommandID.midiConfigurationData, [index])[0]
                serialHandler.write("rqi:" + qualifiedShort)
                qualifiedShorts = self.getQualifiedShortCommand(CommandID.midiConfigurationName, [index])
                for qualifiedShort in qualifiedShorts:
                    serialHandler.write("rqi:" + qualifiedShort)
                qualifiedShort = self.getQualifiedShortCommand(CommandID.midiReceiveChannel, [index])[0]
                serialHandler.write("rqi:" + qualifiedShort)

            case CommandID.midiConfigurationData:
                if len(commandItem.selection) == 0:
                    selection = 0
                else:
                    pass

                i = 0
                while(i < (len(commandItem.argument))):
                    if (i >= (len(commandItem.argument) - 1)): arg = ""
                    else: arg = stripLeadingQuotes(commandItem.argument[i + 1])
                    match(commandItem.argument[i]):
                        case "noteon":
                            mainWidget.setMIDINoteOnCommands(arg)
                        case "noteoff":
                            mainWidget.setMIDINoteOffCommands(arg)
                        case "cc":
                            if ((i + 2) >= (len(commandItem.argument))):
                                return
                            mainWidget.setMIDICCCommands(commandItem.argument[i + 1], stripLeadingQuotes(commandItem.argument[i + 2]))
                            i += 1
                        case "pat":
                            mainWidget.setMIDIPATCommands(arg)
                        case "pb":
                            mainWidget.setMIDIPBCommands(arg)
                        case "cat":
                            mainWidget.setMIDICATCommands(arg)
                        case "pc":
                            mainWidget.setMIDIPBCommands(arg)
                    i += 2
                mainWidget.updateTextForSelectedListItem()

            case CommandID.midiConfigurationCount:
                simpleFARHandler.stringModules[0].setCommandValue(CommandID.midiConfigurationCount, commandItem.argument[0])
                mainWidget.handleMIDIConfigurationCount(commandItem.argument[0])
                qualifiedShorts = self.getQualifiedShortCommand(CommandID.midiConfigurationData)
                for qualifiedShort in qualifiedShorts:
                    serialHandler.write("rqi:" + qualifiedShort)
                qualifiedShorts = self.getQualifiedShortCommand(CommandID.midiConfigurationName)
                for qualifiedShort in qualifiedShorts:
                    serialHandler.write("rqi:" + qualifiedShort)

            case CommandID.midiConfigurationName:
                try:
                    index = commandItem.hierarchy[len(commandItem.hierarchy) - 2].selection[0]
                except:
                    index = 0
                mainWidget.handleMIDIConfigurationName(index, str(commandItem.argument[0]), False)

            case CommandID.midiReceiveChannel:
                mainWidget.handleMIDIReceiveChannel(commandItem.argument[0])

            case CommandID.actuatorSelect:
                index = commandItem.hierarchy[len(commandItem.hierarchy) - 1].selection[0]
                simpleFARHandler.stringModules[0].setCommandValue(CommandID.actuatorSelect, index)
                rqData = self.getQualifiedShortCommand(CommandID.actuatorData, [index])[0]
                serialHandler.write("rqi:" + rqData)

            case CommandID.actuatorCount:
                mainWidget.ui.comboBoxActuatorPreset.clear()
                simpleFARHandler.stringModules[0].setCommandValue(CommandID.actuatorCount, commandItem.argument[0])
                qualifiedShorts = self.getQualifiedShortCommand(CommandID.actuatorData)
                for qualifiedShort in qualifiedShorts:
                    serialHandler.write("rqi:" + qualifiedShort)

            case CommandID.actuatorData:
                try:
                    index = commandItem.hierarchy[len(commandItem.hierarchy) - 2].selection[0]
                except:
                    index = 0
                mainWidget.handleActuatorData(index, commandItem.argument[0],commandItem.argument[1], commandItem.argument[2], commandItem.argument[3])

            case CommandID.harmonicSeriesSelect:
                index = commandItem.hierarchy[len(commandItem.hierarchy) - 1].selection[0]
                simpleFARHandler.stringModules[0].setCommandValue(CommandID.harmonicSeriesSelect, index)
                rqData = self.getQualifiedShortCommand(CommandID.harmonicSeriesData, [index])[0]
                serialHandler.write("rqi:" + rqData)

            case CommandID.harmonicSeriesCount:
                mainWidget.ui.comboBoxHarmonicList.clear()
                hl = 0
                while (hl < int(commandItem.argument[0])):
                    mainWidget.ui.comboBoxHarmonicList.addItem("--_--" + str(hl))
                    #serialHandler.write("rqi:bhsd:" + str(hl))
                    hl += 1
                index = simpleFARHandler.stringModules[0].getCommandValue(CommandID.harmonicSeriesSelect)
                if (index is None) or (index == -1): index = 0
                mainWidget.ui.comboBoxHarmonicList.setCurrentIndex(index)
                cmds = self.getQualifiedShortCommand(CommandID.harmonicSeriesData)
                for cmd in cmds:
                    serialHandler.write("rqi:" + cmd)

            case CommandID.harmonicSeriesData:
                ratios = []
                for i in range(1, len(commandItem.argument)):
                    ratios.append(commandItem.argument[i])

                currentItem = -1
                if (len(commandItem.hierarchy) > 1):
                    selection = commandItem.hierarchy[len(commandItem.hierarchy) - 2].selection
                    if (len(selection) > 0):
                        currentItem = int(selection[0])

                if (currentItem == -1):
                    for i in range(0, mainWidget.ui.comboBoxHarmonicList.count()):
                        data = mainWidget.ui.comboBoxHarmonicList.itemText(i)
                        if "--_--" in data:
                            currentItem = i
                            break

                if (currentItem == -1):
                    raise("Error in harmonic series data handler / command set modular")

                mainWidget.handleHarmonicSeriesData(currentItem, commandItem.argument[0], ratios)

            case CommandID.controlBoxDataReturn:
                mainWidget.handleControlBoxReturnData(commandItem.argument[0], commandItem.argument[1])

            case CommandID.controlBoxControlData:
                mainWidget.handleControlBoxControlData(commandItem.argument[0], commandItem.argument[1])

            case _:
                return super().processMessages(commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler)
        return True

    def addHarmonicSeries(self, sender, serialHandler, simpleFARHandler,  harmonicSeries, name, setToList):
        super().addHarmonicSeries(sender, serialHandler, simpleFARHandler, harmonicSeries, name, setToList)
        hh: CommandSetModular.GroupHandler = self.baseModule.getGroups("hsh")[0]
        newItem = derivedCommandItem("harmonicseries[" + str(harmonicSeries) + "]")
        hh.addModule(newItem)
        hsRq = self.getQualifiedShortCommand(CommandID.harmonicSeriesCount)[0]
        serialHandler.write("rqi:" + hsRq);

    def removeHarmonicSeries(self, sender, serialHandler, simpleFARHandler, harmonicSeries):
        super().removeHarmonicSeries(sender, serialHandler, simpleFARHandler, harmonicSeries)
        hh: CommandSetModular.GroupHandler = self.baseModule.getGroups("hsh")[0]
        newItem = derivedCommandItem("harmonicseries[" + str(harmonicSeries) + "]")
        module:CommandSetModular.Module =  hh.getGroup(newItem)
        par:CommandSetModular.GroupHandler =  module.parent
        par.remove(module)
        hsRq = self.getQualifiedShortCommand(CommandID.harmonicSeriesCount)[0]
        serialHandler.write("rqi:" + hsRq);

    '''
    def saveActuator(self, sender, serialHandler, simpleFARHandler, newIndex, name, rest = 0, engage = 2000, stall = 60000):
        count = int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.actuatorCount))
        if (newIndex >= count):
            addAc = self.getQualifiedShortCommand(CommandID.actuatorAdd)[0]
            serialHandler.write(addAc + ":" + name + ":" + rest + ":" + engage + ":" + stall)
            mh:CommandSetModular.GroupHandler = self.baseModule.getGroups("ah")[0]
            newItem = derivedCommandItem("actuatorhandler.actuator[" + str(newIndex) + "]")
            self.baseModule.addModule(newItem)
            rqAC = self.getQualifiedShortCommand(CommandID.actuatorCount)[0]
            serialHandler.write("rqi:" + rqAC)
        else:
            bowActuatorData = self.getQualifiedShortCommand(CommandID.actuatorData, [newIndex])[0]
            serialHandler.write(bowActuatorData + ":" + name + ":" + rest + ":" + engage + ":" + stall)
    '''
    def loadActuator(self, sender, serialHandler, simpleFARHandler, index):
        actuatorLoad = self.getQualifiedShortCommand(CommandID.actuatorSelect, [index])[0]
        serialHandler.write(actuatorLoad + ":" + str(index))  # + ",rqi:" + bowPressureMax + ",rqi:" + bowPressureEngage + ",rqi:" + bowPressureRest)

    def addActuator(self, sender, serialHandler, simpleFARHandler, index, name):
        super().addActuator(sender, serialHandler, simpleFARHandler, index, name)
        hh: CommandSetModular.GroupHandler = self.baseModule.getGroups("actuatorhandler")[0]
        newItem = derivedCommandItem("actuator[" + str(index) + "]")
        hh.addModule(newItem)
        acRq = self.getQualifiedShortCommand(CommandID.actuatorCount)[0]
        serialHandler.write("rqi:" + acRq);

    def removeActuator(self, sender, serialHandler, simpleFARHandler, index):
        super().removeActuator(sender, serialHandler, simpleFARHandler, index)
        hh: CommandSetModular.GroupHandler = self.baseModule.getGroups("actuatorhandler")[0]
        newItem = derivedCommandItem("actuator[" + str(index) + "]")
        module:CommandSetModular.Module =  hh.getGroup(newItem)
        par:CommandSetModular.GroupHandler =  module.parent
        par.remove(module)
        rqAC = self.getQualifiedShortCommand(CommandID.actuatorCount)[0]
        serialHandler.write("rqi:" + rqAC)
        acRq = self.getQualifiedShortCommand(CommandID.actuatorCount)[0]
        serialHandler.write("rqi:" + acRq);

    def setMidiConfigurationSelect(self, sender, serialHandler, simpleFARHandler, index):
        simpleFARHandler.stringModules[0].setCommandValue(CommandID.midiConfigurationSelect, index)
        if (not sender.updatingFromModule):
            qualifiedShort = self.getQualifiedShortCommand(CommandID.midiConfigurationSelect, [index])[0]
            serialHandler.write(qualifiedShort)

    def addMidiConfiguration(self, sender, serialHandler, simpleFARHandler, name):
        super().addMidiConfiguration(sender, serialHandler, simpleFARHandler, name)
        index = int(simpleFARHandler.stringModules[0].getCommandValue(CommandID.midiConfigurationCount))
        mc: CommandSetModular.GroupHandler = self.baseModule.getGroups("mc")[0]
        newItem = derivedCommandItem("midiconfigurationhandler.midiconfiguration[" + str(index) + "]")
        self.baseModule.addModule(newItem)
        rqAC = self.getQualifiedShortCommand(CommandID.midiConfigurationCount)[0]
        serialHandler.write("rqi:" + rqAC)
        self.setMidiConfigurationSelect(sender, serialHandler, simpleFARHandler, index)
        mcRq = self.getQualifiedShortCommand(CommandID.midiConfigurationCount)[0]
        serialHandler.write("rqi:" + mcRq);

    def removeMidiConfiguration(self, sender, serialHandler, simpleFARHandler, index):
        super().removeMidiConfiguration(sender, serialHandler, simpleFARHandler, index)
        newItem = derivedCommandItem("midiconfigurationhandler.midiconfiguration[" + str(index) + "]")
        module:CommandSetModular.Module =  self.baseModule.getGroup(newItem)
        par:CommandSetModular.GroupHandler =  module.parent
        par.remove(module)
        rqAC = self.getQualifiedShortCommand(CommandID.midiConfigurationCount)[0]
        serialHandler.write("rqi:" + rqAC)
        mcRq = self.getQualifiedShortCommand(CommandID.midiConfigurationCount)[0]
        serialHandler.write("rqi:" + mcRq);

    def __init__(self):
        super().__init__()
        self.hasHierarchy = False
        self.baseModule = self.GroupHandler(self, None, None)
        self.CommandItem = derivedCommandItem
        self.CommandList = derivedCommandList

        self.fromVer = 20260111184310
        self.toVer = 99999999999999

        self.commands = [self.Base, self.Mute, self.Solenoid, self.BowingWheel, self.DCMotor, self.PID, self.BowPressure, self.BowActuatorHandler,
                         self.Actuator, self.HarmonicSeriesHandler, self.HarmonicSeries, self.MidiConfigurationHandler, self.MidiConfiguration, self.ControlBox]

class CommandSets:
    currentCommandSet:CommandSet = CommandSetOG

    def getCommandType(self, commandItem):
        return self.currentCommandSet.getCommandType(commandItem)

    def getCommandID(self, commandItem, module = None):
        return self.currentCommandSet.getCommandID(commandItem, module)

    def initialRequest(self):
        return self.currentCommandSet.initialRequest()

    def requestData(self, serialHandler):
        return self.currentCommandSet.requestData(serialHandler)

    def requestContinuousData(self, serialHandler):
        return self.currentCommandSet.requestContinuousData(serialHandler)

    def __init__(self):
        self.currentCommandSet = CommandSetOG()
        self.commandSets = { CommandSetOG(), CommandSetModular() }

    def chooseCommandSet(self, versionNumber):
        versionNumber = int(versionNumber[4:])
        self.currentCommandSet = None
        for commandSet in self.commandSets:
            if ((versionNumber >= commandSet.fromVer) and (versionNumber <= commandSet.toVer)):
                self.currentCommandSet = commandSet
                break
        if (self.currentCommandSet == None):
            raise("No command set found!")
        pass

    def buildHierarchy(self, commandItem:currentCommandSet.CommandItem):
        self.currentCommandSet.buildHierarchy(commandItem)
        pass

    def getQualifiedShortCommand(self, commandID, selectionIndex = None, stripIndex = False):
        return self.currentCommandSet.getQualifiedShortCommand(commandID, selectionIndex, stripIndex)

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        return self.currentCommandSet.processMessages(commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler)

    def setMidiConfigurationSelect(self, sender, serialHandler, simpleFARHandler, index):
        return self.currentCommandSet.setMidiConfigurationSelect(sender, serialHandler, simpleFARHandler, index)

    def setHarmonicSeriesSelect(self, sender, serialHandler, simpleFARHandler, index):
        return self.currentCommandSet.setHarmonicSeriesSelect(sender, serialHandler, simpleFARHandler, index)

    def setHarmonicSeriesRatio(self, sender, serialHandler, simpleFARHandler,  harmonicSeries, ratioIndex, ratio):
        return self.currentCommandSet.setHarmonicSeriesRatio(sender, serialHandler, simpleFARHandler, harmonicSeries, ratioIndex, ratio)

    def addHarmonicSeriesRatio(self, sender, serialHandler, simpleFARHandler,  harmonicSeries):
        return self.currentCommandSet.addHarmonicSeriesRatio(sender, serialHandler, simpleFARHandler, harmonicSeries)

    def removeHarmonicSeriesRatio(self, sender, serialHandler, simpleFARHandler,  harmonicSeries, ratioIndex):
        return self.currentCommandSet.removeHarmonicSeriesRatio(sender, serialHandler, simpleFARHandler, harmonicSeries, ratioIndex)

    def saveHarmonicSeries(self, sender, serialHandler, simpleFARHandler,  harmonicSeries, name, setToList):
        ind = simpleFARHandler.stringModules[0].getCommandValue(CommandID.harmonicSeriesCount)
        self.addHarmonicSeries(sender, serialHandler, simpleFARHandler, ind, "default", False)

        #return self.currentCommandSet.saveHarmonicSeries(sender, serialHandler, simpleFARHandler, harmonicSeries, name, setToList)

    def addHarmonicSeries(self, sender, serialHandler, simpleFARHandler,  harmonicSeries, name, setToList):
        return self.currentCommandSet.addHarmonicSeries(sender, serialHandler, simpleFARHandler, harmonicSeries, name, setToList)

    def removeHarmonicSeries(self, sender, serialHandler, simpleFARHandler, harmonicSeries):
        return self.currentCommandSet.removeHarmonicSeries(sender, serialHandler, simpleFARHandler, harmonicSeries)

    def renameHarmonicSeries(self, sender, serialHandler, simpleFARHandler, harmonicSeries, name):
        return self.currentCommandSet.renameHarmonicSeries(sender, serialHandler, simpleFARHandler, harmonicSeries, name)

    def setHarmonicSeriesData(self, sender, serialHandler, simpleFARHandler, harmonicSeries, name, data):
        return self.currentCommandSet.setHarmonicSeriesData(sender, serialHandler, simpleFARHandler, harmonicSeries, name, data)
    '''
    def saveActuator(self, sender, serialHandler, simpleFARHandler, newIndex, name, rest = 0, engage = 2000, stall = 60000):
        return self.currentCommandSet.saveActuator(sender, serialHandler, simpleFARHandler, newIndex, name, rest, engage, stall)
    '''
    def loadActuator(self, sender, serialHandler, simpleFARHandler, index):
        return self.currentCommandSet.loadActuator(sender, serialHandler, simpleFARHandler, index)
    
    def addActuator(self, sender, serialHandler, simpleFARHandler, index, name):
        return self.currentCommandSet.addActuator(sender, serialHandler, simpleFARHandler, index, name)

    def renameActuator(self, sender, serialHandler, simpleFARHandler, index, name):
        return self.currentCommandSet.renameActuator(sender, serialHandler, simpleFARHandler, index, name)

    def removeActuator(self, sender, serialHandler, simpleFARHandler, index):
        return self.currentCommandSet.removeActuator(sender, serialHandler, simpleFARHandler, index)

    def setMidiConfigurationName(self, sender, serialHandler, simpleFARHandler, index, name):
        return self.currentCommandSet.setMidiConfigurationName(sender, serialHandler, simpleFARHandler, index, name)

    def addMidiConfiguration(self, sender, serialHandler, simpleFARHandler, name):
        return self.currentCommandSet.addMidiConfiguration(sender, serialHandler, simpleFARHandler, name)

    def removeMidiConfiguration(self, sender, serialHandler, simpleFARHandler, index):
        self.currentCommandSet.removeMidiConfiguration(sender, serialHandler, simpleFARHandler, index)

    def addMidiConfigurationCC(self, sender, serialHandler, simpleFARHandler, cc):
        self.currentCommandSet.addMidiConfigurationCC(sender, serialHandler, simpleFARHandler, cc)

    def removeMidiConfigurationCC(self, sender, serialHandler, simpleFARHandler, cc):
        self.currentCommandSet.removeMidiConfigurationCC(sender, serialHandler, simpleFARHandler, cc)
