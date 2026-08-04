import datetime
import time

from commanddefinitions import CommandID, CommandType, defaultCommandType, ModuleCommand, getModuleCommandTypeDesc

from general_helpers import stripLeadingQuotes, messageBox

from PySide6.QtWidgets import QCompleter
from PySide6.QtCore import Qt, QTimer
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

    def buildHierarchy(self, commandItem, widget):
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

            case CommandID.moduleSelect:
                mainWidget.addModulesIfNeeded(0)

            case CommandID.moduleCount:
                global moduleCount
                try:
                    moduleCount = int(commandItem.argument[0])
                    mainWidget.addModulesIfNeeded(moduleCount - 1)
                except:
                    messageBox("Error", "Error retreiving module count!")

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
        serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.harmonicSeriesData)[0] + ":" + str(harmonicSeries))

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
            CommandID.help: "help",

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
            CommandID.help: "help",

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

    def buildHierarchy(self, commandItem, widget):
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

    def clearData(self):
        pass

    def processHelpReturn(self, infoReturn, commandReference):
        commandList = self.CommandList()
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
                    scope = "Global"
                case "[str]":
                    scopeText = "This command is dependent on the currently selected module, bow and/or solenoid"
                    scope = "Local"
                case _:
                    scopeText = ""
                    scope = "Unknown"

            if not skip:
                x = command.find("|")
                help = scopeText + "\n\n"
                help += "command: \n" + command + "\n\n"
                help += "parameters: \n"
                for j in range(1,len(i.argument) - 1):
                    help += i.argument[j]
                    if (j < (len(i.argument)-2)):
                        help += ":"
                help += "\n\nDescription: \n" + i.argument[len(i.argument) - 1]

                if x != -1:
                    short = command[x+1:]
                    command = command[:x]
                else:
                    short = ""

                commandReference.addCommand(command, help)

class CommandSetModular(CommandSet):
    class Base(CommandSet):
        longName = ""
        shortName = ""
        index = False

        def __init__(self):
            super().__init__()
            self.postInit()

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
            CommandID.dir : "ls",
            CommandID.help: "help",
            CommandID.freeMemory: "free",
            CommandID.dumpSaveData : "dump",
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
            CommandID.nop: "nooperation",
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
            CommandID.dir: "list",
            CommandID.help: "help",
            CommandID.freeMemory: "freeram",
            CommandID.dumpSaveData: "dump",

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
            CommandID.actuatorName : "na",
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
            CommandID.bowHome: "hm",
            CommandID.bowPressureTMCInfo: "tmi"
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
            CommandID.bowPressureTMCInfo: "tmcinfo"
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
            CommandID.solenoidDisengage: "rest",
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
            #CommandID.midiConfigurationData : "da",
            CommandID.midiConfigurationAddCC : "ac",
            CommandID.midiConfigurationRemoveCC : "rmc",
            CommandID.midiConfigurationDefaults : "d",
            CommandID.midiReceiveChannel : "rc",
            CommandID.midiConfigurationNoteOn : "non",
            CommandID.midiConfigurationNoteOff: "nof",
            CommandID.midiConfigurationPolyAT: "pat",
            CommandID.midiConfigurationChannelAT: "cat",
            CommandID.midiConfigurationProgramChange: "pc",
            CommandID.midiConfigurationPitchbend: "pb",
            CommandID.midiConfigurationContinuousController: "ccd"
        }

        longCommands = {
            CommandID.midiConfigurationName : "name",
            #CommandID.midiConfigurationData : "data",
            CommandID.midiConfigurationAddCC : "addcc",
            CommandID.midiConfigurationRemoveCC : "removecc",
            CommandID.midiConfigurationDefaults : "defaults",
            CommandID.midiReceiveChannel : "receivechannel",
            CommandID.midiConfigurationNoteOn: "noteon",
            CommandID.midiConfigurationNoteOff: "noteoff",
            CommandID.midiConfigurationPolyAT: "polyaftertouch",
            CommandID.midiConfigurationChannelAT: "channelaftertouch",
            CommandID.midiConfigurationProgramChange: "programchange",
            CommandID.midiConfigurationPitchbend: "pitchbend",
            CommandID.midiConfigurationContinuousController: "continuouscontrollerdata"
        }

        requestData = [
            #CommandID.midiConfigurationName, CommandID.midiConfigurationData, CommandID.midiReceiveChannel
        ]

        requestContinuousData = []

    class MidiCC(CommandSet):
        longName = "continuouscontroller"
        shortName = "cc"
        index = False

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.midiConfigurationCCControl : "cl",
            CommandID.midiConfigurationCCCommands : "cm",
        }

        longCommands = {
            CommandID.midiConfigurationCCControl : "control",
            CommandID.midiConfigurationCCCommands : "command",
        }

        requestData = [ CommandID.midiConfigurationCCCommands, CommandID.midiConfigurationCCControl ]

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

            CommandID.controlBoxHarmonic : "har",
            CommandID.controlBoxHarmonicShift : "has",
            CommandID.controlBoxFinetune : "fin",
            CommandID.controlBoxPressure : "pre",
            CommandID.controlBoxMute : "mut",
            CommandID.controlBoxHammerScale: "hms",
            CommandID.controlBoxGate: "gt",
            CommandID.controlBoxHammerTrig: "hmt",

            CommandID.testADCLatency : "tal",
            CommandID.testADCLatencyReturn : "talr",
            CommandID.testADCMinMax : "tix"
        }

        longCommands = {
            CommandID.controlBoxControlData : "controldata",
            CommandID.controlBoxControlDefaults : "controldefaults",
            CommandID.controlBoxDataReturn : "datareturn",
            CommandID.controlBoxADCSettings : "adcsettings",

            CommandID.controlBoxHarmonic: "harmonic",
            CommandID.controlBoxHarmonicShift: "harmonicshift",
            CommandID.controlBoxFinetune: "finetune",
            CommandID.controlBoxPressure: "pressure",
            CommandID.controlBoxMute: "mute",
            CommandID.controlBoxHammerScale: "hammerscale",
            CommandID.controlBoxGate: "gate",
            CommandID.controlBoxHammerTrig: "hammertrig",

            CommandID.testADCLatency : "testadclatency",
            CommandID.testADCLatencyReturn : "testadclatencyreturn",
            CommandID.testADCMinMax : "testadcminmax"
        }

        requestData = [ CommandID.controlBoxHarmonic, CommandID.controlBoxHarmonicShift, CommandID.controlBoxFinetune, CommandID.controlBoxPressure,
                        CommandID.controlBoxMute, CommandID.controlBoxHammerScale, CommandID.controlBoxGate, CommandID.controlBoxHammerTrig]
        requestContinuousData = []

    class PluginHandler(CommandSet):
        longName = "pluginhandler"
        shortName = "ph"
        index = False

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.pluginHandlerAdd : "a",
            CommandID.pluginHandlerRemove: "rm",
            CommandID.pluginHandlerCount: "c",
        }

        longCommands = {
            CommandID.pluginHandlerAdd : "add",
            CommandID.pluginHandlerRemove: "remove",
            CommandID.pluginHandlerCount: "count",
        }

        requestData = []
        requestContinuousData = []

    class PluginMultiple(CommandSet):
        longName = "multiple"
        shortName = "mlt"
        index = True

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.pluginMultName : "na",
            CommandID.pluginMultTarget : "tg",
            CommandID.pluginMultData : "da",
            CommandID.pluginMultRemove : "rm"
        }

        longCommands = {
            CommandID.pluginMultName: "name",
            CommandID.pluginMultTarget: "target",
            CommandID.pluginMultData: "data",
            CommandID.pluginMultRemove: "rempve"
        }

        requestData = [ CommandID.pluginMultName ]
        requestContinuousData = []

    class PluginLFO(CommandSet):
        longName = "lfo"
        shortName = "lfo"
        index = True

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.pluginLFOName : "na",
            CommandID.pluginLFOEnable : "en",
            CommandID.pluginLFOTarget : "tg",
            CommandID.pluginLFOUpdateRate : "ur",
            CommandID.pluginLFOWaveform : "wf",
            CommandID.pluginLFOFrequency : "fq",
            CommandID.pluginLFOAmpltiude : "amp",
            CommandID.pluginLFODelay : "dl",
            CommandID.pluginLFOResetDelay : "rd",
            CommandID.pluginLFOResetWave : "rw",
            CommandID.pluginLFOBipolar : "bp"
        }

        longCommands = {
            CommandID.pluginLFOName : "name",
            CommandID.pluginLFOEnable: "enable",
            CommandID.pluginLFOTarget: "target",
            CommandID.pluginLFOUpdateRate: "updaterate",
            CommandID.pluginLFOWaveform: "waveform",
            CommandID.pluginLFOFrequency: "frequency",
            CommandID.pluginLFOAmpltiude: "amplitude",
            CommandID.pluginLFODelay: "delay",
            CommandID.pluginLFOResetDelay: "resetdelay",
            CommandID.pluginLFOResetWave: "resetwave",
            CommandID.pluginLFOBipolar: "bipolar"
        }

        requestData = [ CommandID.pluginLFOName ]
        requestContinuousData = []

    class PluginAHDSR(CommandSet):
        longName = "ahdsr"
        shortName = "ahdsr"
        index = True

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.pluginAHDSRName : "na",
            CommandID.pluginAHDSREnable : "en",
            CommandID.pluginAHDSRTarget : "tg",
            CommandID.pluginAHDSRUpdateRate : "ur",
            CommandID.pluginAHDSRGate : "gt",
            CommandID.pluginAHDSRAttack : "at",
            CommandID.pluginAHDSRHold : "hd",
            CommandID.pluginAHDSRDecay : "dc",
            CommandID.pluginAHDSRSustain : "su",
            CommandID.pluginAHDSRRelease : "re",
            CommandID.pluginAHDSRReleaseTarget : "rt",
            CommandID.pluginAHDSRAmpltiude : "amp",
            CommandID.pluginAHDSRInvert : "inv"
        }

        longCommands = {
            CommandID.pluginAHDSRName : "name",
            CommandID.pluginAHDSREnable: "enable",
            CommandID.pluginAHDSRTarget: "target",
            CommandID.pluginAHDSRUpdateRate: "updaterate",
            CommandID.pluginAHDSRGate: "gate",
            CommandID.pluginAHDSRAttack: "attack",
            CommandID.pluginAHDSRHold: "hold",
            CommandID.pluginAHDSRDecay: "decay",
            CommandID.pluginAHDSRSustain: "sustain",
            CommandID.pluginAHDSRRelease: "release",
            CommandID.pluginAHDSRReleaseTarget: "releasetarget",
            CommandID.pluginAHDSRAmpltiude: "amplitude",
            CommandID.pluginAHDSRInvert: "invert"
        }

        requestData = [ CommandID.pluginAHDSRName ]
        requestContinuousData = []

    class PluginMap(CommandSet):
        longName = "numbermap"
        shortName = "nm"
        index = True

        def __init__(self):
            super().__init__()
            self.postInit()

        shortCommands = {
            CommandID.pluginMapName : "na",
            CommandID.pluginMapTarget : "tg",
            CommandID.pluginMapData : "da",
            CommandID.pluginMapRemove : "rm",
            CommandID.pluginMapScale : "sc",
            CommandID.pluginMapTrigger : "tr"
        }

        longCommands = {
            CommandID.pluginMapName: "name",
            CommandID.pluginMapTarget: "target",
            CommandID.pluginMapData: "data",
            CommandID.pluginMapRemove: "remove",
            CommandID.pluginMapScale : "scale",
            CommandID.pluginMapTrigger: "trigger"
        }

        requestData = [ CommandID.pluginMapName, CommandID.pluginMapTarget ]
        requestContinuousData = []

    class Module:
        def __init__(self, baseCommandSet, commandItem = None, itemCommandSet = None):
            self.longName = ""
            self.shortName = ""
            self.moduleType = ""
            self.indexingChild = None
            self.commandSet = None
            self.index = 0
            self.parent = None
            self.commands = {}

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
            self.empty = False

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
            self.instances = 0
            self.isEmpty = False

        def remove(self, item):
            if (isinstance(item, int)):
                index = item
                item = self.children[index]
            else:
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

        def getGroupParsed(self, newItem, rootGroup = None, addGroups = False, isEmpty = False):
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
                            return group.getGroupParsed(newItem, group.children, addGroups, isEmpty)
            if (addGroups):
                self.addGroupFromHierarchy(newItem, isEmpty)
                if (len(rootGroup) != 0):
                    group = rootGroup[-1]
                    if (newItem.hierarchyIndex < (len(newItem.hierarchy))):
                        group.getGroupParsed(newItem, group.children, True)
                else:
                    pass

        def getGroup(self, commandItem):
            return self.getGroupParsed(commandItem, self.children)

        def getGroupAndAddIfNone(self, commandItem, isEmpty = False):
            return self.getGroupParsed(commandItem, self.children, True, isEmpty)

        def addGroup(self, commandItem, commandGroup, isEmpty = False):
            child = self.commandSet.GroupHandler(self.commandSet, commandItem, commandGroup)
            child.parent = self
            child.isEmpty = isEmpty
            self.children.append(child)
            return  self.children[-1]

        def addGroupFromHierarchy(self, commandItem, isEmpty = False):
            commandGroup = None
            for item in self.commandSet.commands:
                if (item.longName == commandItem.hierarchy[commandItem.hierarchyIndex].name or
                        item.shortName == commandItem.hierarchy[commandItem.hierarchyIndex].name):
                    commandGroup = item
                    break
            if (commandGroup == None):
                pass
            else:
                self.addGroup(commandItem, commandGroup, isEmpty)
                commandItem.hierarchyIndex += 1
            if (len(self.children) == 0):
                return None
            return  self.children[-1]

        def addModule(self, commandItem, isEmpty = False):
            self.getGroupAndAddIfNone(commandItem, isEmpty)

        def addModuleFromDirReturn(self, commandItem):
            newCommandItem = derivedCommandItem(commandItem.argument[0])
            emptyGroup = False
            if (len(commandItem.argument) == 4):
                if (int(commandItem.argument[2]) == 0):
                    emptyGroup = True
            self.addModule(newCommandItem, emptyGroup)

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
        command, module, index = self.getCommandModuleAndCommand(commandItem)
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

            if (module == ""):
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
        return ["ls:m:r:i", "nop", "help", "nop"]

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
        #cbd = self.getQualifiedShortCommand(CommandID.controlBoxControlData)[0]
        '''
        serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.controlBoxHarmonic)[0])
        serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.controlBoxHarmonicShift)[0])
        serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.controlBoxFinetune)[0])
        serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.controlBoxPressure)[0])
        serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.controlBoxMute)[0])
        serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.controlBoxGate)[0])
        serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.controlBoxHammerScale)[0])
        serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.controlBoxHammerTrig)[0])
        '''
        cba = self.getQualifiedShortCommand(CommandID.controlBoxADCSettings)[0]
        for i in range(0,8):
            serialHandler.write("rqi:" + cba + ":" + str(i))

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

    def buildHierarchy(self, commandItem, widget):
        self.baseModule.addModuleFromDirReturn(commandItem)
        pass

    def getCommandModuleAndCommand(self, commandItem):
        newCommandItem = derivedCommandItem(commandItem)
        newCommandItem.buildHierarchy()
        if (len(newCommandItem.hierarchy) <= 1):
            module = ""
            command = newCommandItem.hierarchy[0].name
            index = 0
        else:
            module = newCommandItem.hierarchy[len(newCommandItem.hierarchy) - 2].name
            command = newCommandItem.hierarchy[len(newCommandItem.hierarchy) - 1].name
            if len(newCommandItem.hierarchy[len(newCommandItem.hierarchy) - 2].selection) > 0:
                index = newCommandItem.hierarchy[len(newCommandItem.hierarchy) - 2].selection[0]
            else:
                index = 0
        return command, module, index

    def getModuleHierarchy(self, inModule):
        hierarchy = []
        if (inModule.longName != ""):
            hierarchy.insert(0, [inModule.longName, inModule.index])
        if (inModule.parent is not None):
            newHierarchy = self.getModuleHierarchy(inModule.parent)
            hierarchy = newHierarchy + hierarchy
        return hierarchy

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        command, module, index = self.getCommandModuleAndCommand(commandItem)
        if (command == "na"):
            pass
        id = self.getCommandID(command, module)

        if (id == None and command != "bpr" and command != "bmes" and command != "msi" and command != "msx" and command != "ver" and command != "ls" and
                command != "dp" and command != "fmp" and command != "hmp"):
            pass

        found = True

        match(id):
            case CommandID.version:
                mainWidget.completerList.clear()
                serialHandler.write("ls:m:r:i,nop")
                self.hasHierarchy = False
                pass

            case CommandID.dir:
                if (not self.hasHierarchy):
                    self.buildHierarchy(commandItem, mainWidget)
                elif (not self.hasCommandList):
                    mainWidget.completerList.append(commandItem.argument[0].strip())
                    mainWidget.completerList.append(commandItem.argument[1].strip())

            case CommandID.nop:
                if (not self.hasHierarchy):
                    self.hasHierarchy = True
                    self.hasCommandList = False
                    serialHandler.write("ls:c:r:i,nop")
                elif (not self.hasCommandList):
                    self.hasCommandList = True
                    mainWidget.completer = QCompleter(mainWidget.completerList, completionMode=QCompleter.CompletionMode.InlineCompletion,
                                                      filterMode=Qt.MatchFlag.MatchContains, caseSensitivity=Qt.CaseSensitivity.CaseInsensitive)
                    mainWidget.serialWidget.ui.lineEditSend.setCompleter(mainWidget.completer)
                    serialHandler.write("help, nop")
                elif (not self.hasHelp):
                    self.buildHelp(mainWidget.commandReference)
                    self.hasHelp = True
                    mainWidget.pluginHandler.commandSet = self
                    mainWidget.pluginHandler.buildPluginList()
                    self.requestData(serialHandler)
                    mainWidget.localNodeHandler.commandSet = self
                    mainWidget.localNodeHandler.addDynamicNodeSet(self.baseModule)
                    serialHandler.write("nop")

            case CommandID.midiConfigurationSelect:
                index = commandItem.hierarchy[len(commandItem.hierarchy) - 1].selection[0]
                mainWidget.midiEventHandler.handleMIDIConfigurationSelect(index)
                #qualifiedShort = self.getQualifiedShortCommand(CommandID.midiConfigurationData, [index])[0]
                #serialHandler.write("rqi:" + qualifiedShort)
                qualifiedShorts = self.getQualifiedShortCommand(CommandID.midiConfigurationName, [index])
                for qualifiedShort in qualifiedShorts:
                    serialHandler.write("rqi:" + qualifiedShort)
                qualifiedShort = self.getQualifiedShortCommand(CommandID.midiReceiveChannel, [index])[0]
                serialHandler.write("rqi:" + qualifiedShort)


            case CommandID.midiConfigurationNoteOn:
                mainWidget.midiEventHandler.setMIDINoteOnCommands(stripLeadingQuotes(commandItem.argument[0]))
            case CommandID.midiConfigurationNoteOff:
                mainWidget.midiEventHandler.setMIDINoteOffCommands(stripLeadingQuotes(commandItem.argument[0]))
            case CommandID.midiConfigurationPolyAT:
                mainWidget.midiEventHandler.setMIDIPATCommands(stripLeadingQuotes(commandItem.argument[0]))
            case CommandID.midiConfigurationChannelAT:
                mainWidget.midiEventHandler.setMIDICATCommands(stripLeadingQuotes(commandItem.argument[0]))
            case CommandID.midiConfigurationPitchbend:
                mainWidget.midiEventHandler.setMIDIPBCommands(stripLeadingQuotes(commandItem.argument[0]))
            case CommandID.midiConfigurationProgramChange:
                mainWidget.midiEventHandler.setMIDIPCCommands(stripLeadingQuotes(commandItem.argument[0]))
            case CommandID.midiConfigurationContinuousController:
                # Second argument may not exist if the CC hasn't been mapped yet
                if (len(commandItem.argument) == 2):
                    ccCommands = stripLeadingQuotes(commandItem.argument[1])
                else:
                    ccCommands = ""
                mainWidget.midiEventHandler.setMIDICCCommands(stripLeadingQuotes(commandItem.argument[0]), ccCommands)

            case CommandID.midiConfigurationCount:
                simpleFARHandler.stringModules[0].setCommandValue(CommandID.midiConfigurationCount, commandItem.argument[0])
                mainWidget.midiEventHandler.handleMIDIConfigurationCount(commandItem.argument[0])
                serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.midiConfigurationNoteOn)[0])
                serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.midiConfigurationNoteOff)[0])
                serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.midiConfigurationPolyAT)[0])
                serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.midiConfigurationChannelAT)[0])
                serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.midiConfigurationPitchbend)[0])
                serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.midiConfigurationProgramChange)[0])
                serialHandler.write("rqi:" + self.getQualifiedShortCommand(CommandID.midiConfigurationContinuousController)[0])
                qualifiedShorts = self.getQualifiedShortCommand(CommandID.midiConfigurationName)
                for qualifiedShort in qualifiedShorts:
                    serialHandler.write("rqi:" + qualifiedShort)

            case CommandID.midiConfigurationName:
                try:
                    index = commandItem.hierarchy[len(commandItem.hierarchy) - 2].selection[0]
                except:
                    index = 0
                mainWidget.midiEventHandler.handleMIDIConfigurationName(index, str(commandItem.argument[0]), False)

            case CommandID.midiReceiveChannel:
                mainWidget.midiEventHandler.handleMIDIReceiveChannel(commandItem.argument[0])

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
                mainWidget.cvEventHandler.handleControlBoxReturnData(commandItem.argument[0], commandItem.argument[1])

            case CommandID.controlBoxControlData:
                mainWidget.cvEventHandler.handleControlBoxControlData(commandItem.argument[0], commandItem.argument[1])

            case CommandID.controlBoxHarmonic:
                mainWidget.cvEventHandler.handleControlBoxControlData(0, commandItem.argument[0])

            case CommandID.controlBoxHarmonicShift:
                mainWidget.cvEventHandler.handleControlBoxControlData(1, commandItem.argument[0])

            case CommandID.controlBoxFinetune:
                mainWidget.cvEventHandler.handleControlBoxControlData(2, commandItem.argument[0])

            case CommandID.controlBoxPressure:
                mainWidget.cvEventHandler.handleControlBoxControlData(3, commandItem.argument[0])

            case CommandID.controlBoxHammerTrig:
                mainWidget.cvEventHandler.handleControlBoxControlData(4, commandItem.argument[0])

            case CommandID.controlBoxGate:
                mainWidget.cvEventHandler.handleControlBoxControlData(5, commandItem.argument[0])

            case CommandID.controlBoxHammerScale:
                mainWidget.cvEventHandler.handleControlBoxControlData(6, commandItem.argument[0])

            case CommandID.controlBoxMute:
                mainWidget.cvEventHandler.handleControlBoxControlData(7, commandItem.argument[0])

            case CommandID.help:
                #self.processHelpReturn(commandItem, mainWidget.ref)
                pass

            case CommandID.pluginAHDSRTarget:
                pass

            case _:
                #if (not super().processMessages(commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler)):
                #    return False
                found = super().processMessages(commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler)

        if (self.hasHelp) and (mainWidget.localNodeHandler is not None):
            found = found & mainWidget.localNodeHandler.parseCommand(commandItem)
            if (not self.hasNodes):
                self.mainWidget = mainWidget
                if (not self.updateTimer):
                    self.updateTimer = QTimer(mainWidget)
                    self.updateTimer.timeout.connect(self.nodeAutoUpdater)
                    self.updateTimer.start(1000)
                    print("Starting timer")
#            if self.hasNodes and (id == CommandID.nop):
#                    mainWidget.localNodeHandler.postBuildUpdate()
            return found
        return True

    def nodeAutoUpdater(self):
        match(self.updateStage):
            case 0:
                a = time.time()
                if (a > (self.mainWidget.lastSerialEvent + 1)): # and (not self.hasNodes):
                    self.mainWidget.localNodeHandler.postBuildUpdate()
                    self.hasNodes = True
                    self.updateStage = 1
            case 1:
                if (self.hasNodes):
                    self.updateTimer.stop()
                    self.mainWidget.localNodeHandler.redraw()
                    self.mainWidget.localNodeHandler.ga.graph.select_all()
                    self.mainWidget.localNodeHandler.ga.graph.fit_to_selection()
                    self.mainWidget.localNodeHandler.ga.graph.clear_selection()

                    self.updateStage = 2

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

    def addMidiConfigurationCC(self, sender, serialHandler, simpleFARHandler, cc):
        setCC = self.getQualifiedShortCommand(CommandID.midiConfigurationAddCC)[0]
        serialHandler.write(setCC + ":" + str(cc) + ":''")

    def setMidiConfigurationNoteOnCommands(self, sender, serialHandler, simpleFAR, index, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationNoteOn, [index])[0]
        serialHandler.write(qualifiedCommand + ":'" + commands + "'")

    def setMidiConfigurationNoteOffCommands(self, sender, serialHandler, simpleFAR, index, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationNoteOff, [index])[0]
        serialHandler.write(qualifiedCommand + ":'" + commands + "'")

    def setMidiConfigurationPolyAftertouchCommands(self, sender, serialHandler, simpleFAR, index, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationPolyAT, [index])[0]
        serialHandler.write(qualifiedCommand + ":'" + commands + "'")

    def setMidiConfigurationChannelAftertouchCommands(self, sender, serialHandler, simpleFAR, index, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationChannelAT, [index])[0]
        serialHandler.write(qualifiedCommand + ":'" + commands + "'")

    def setMidiConfigurationProgramChangeCommands(self, sender, serialHandler, simpleFAR, index, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationProgramChange, [index])[0]
        serialHandler.write(qualifiedCommand + ":'" + commands + "'")

    def setMidiConfigurationPitchBendCommands(self, sender, serialHandler, simpleFAR, index, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationPitchbend, [index])[0]
        serialHandler.write(qualifiedCommand + ":'" + commands + "'")

    def setMidiConfigurationContinuousControllerCommands(self, sender, serialHandler, simpleFAR, index, cc, commands):
        qualifiedCommand = self.getQualifiedShortCommand(CommandID.midiConfigurationContinuousController, [index])[0]
        serialHandler.write(qualifiedCommand + ":" + str(cc) + ":'" + commands + "'")

    def buildHelp(self, commandReference):
        self.processModuleForHelp(self.baseModule, commandReference)

    def processModuleForHelp(self, inModule, commandReference):
        yesno = ["no", "yes"]

        existingMods = {}
        for commandd in inModule.commands:
            command:ModuleCommand = inModule.commands[commandd]
            if (command is None): break
            lastCmd = str(command.shortCommand).rfind(".")
            if (lastCmd != -1):
                shortHand = command.shortCommand[lastCmd + 1:]
                comstr = command.longCommand[command.longCommand.rfind(".") + 1:]
            else:
                shortHand = command.shortCommand[:]
                comstr = command.longCommand
            if (command.longCommand == ""):
                comstr = "[select]"
                shortHand = "[select]"

            if (command.variables is None):
                variables = "none"
            else:
                variables = ""
                for var in command.variables:
                    variables += var + " "

            description = (command.description + "\n\nShorthand: " + shortHand + "\n\n" + getModuleCommandTypeDesc(command.commandType) + "\n\nArguments: " + \
                           command.arguments + "\n\nAssocated variables: " + variables + "\n\nHidden: " + yesno[int(command.hidden)])

            if (inModule.parent is not None):
                par = inModule.longName
            else:
                par = ""
            commandReference.addCommandB(comstr, par, shortHand, description)

        for child in inModule.children:
            if not child.longName in existingMods:
                existingMods[child.longName] = True
                child:CommandSetModular.Module = child
                if (child.longName in self.baseModule.commands):
                    description = self.baseModule.commands[child.longName].description + "\n\nShorthand: " + child.shortName + "\n\nSelectable" #(child.commands[child.longName])
                    commandReference.addCommandB(child.longName, "", child.shortName, description)
                    self.processModuleForHelp(child, commandReference)
                else:
                    pass

    def processHelpReturn(self, infoReturn, commandReference):
        if (len(infoReturn.argument) < 3):
            return

        if (infoReturn.argument[0][len(infoReturn.argument[0]) - 1:]) == ".":
            infoReturn.argument[0] = infoReturn.argument[0][:len(infoReturn.argument[0]) - 1]

        if (infoReturn.argument[1][len(infoReturn.argument[1]) - 1:]) == ".":
            infoReturn.argument[1] = infoReturn.argument[1][:len(infoReturn.argument[1]) - 1]

        longCommand = derivedCommandItem(infoReturn.argument[0])
        shortCommand = derivedCommandItem(infoReturn.argument[1])

        isModule = False
        if (len(infoReturn.argument) >= 6):
            if (len(infoReturn.argument) == 7):
                variables = stripLeadingQuotes(infoReturn.argument[6]).split(",")
                if (len(variables) == 1) and (variables[0] == ""): variables.remove(variables[0])
            else:
                variables = []
            mcd = ModuleCommand(infoReturn.argument[0], infoReturn.argument[1], infoReturn.argument[3], infoReturn.argument[5], infoReturn.argument[4],
                                infoReturn.argument[2], variables)
            id = self.getCommandID(longCommand)
            if id is None:
                pass
        else:
            mcd = ModuleCommand(infoReturn.argument[0], infoReturn.argument[1], inDescription = infoReturn.argument[2])
            id = longCommand.hierarchy[len(longCommand.hierarchy) - 1].name
            isModule = True

        if ((len(longCommand.hierarchy) > 1) and (not isModule)):
            parent = longCommand.hierarchy[len(longCommand.hierarchy) - 2].name
            command = longCommand.hierarchy[len(longCommand.hierarchy) - 1].name
            if mcd is not None:
                groups = self.baseModule.getGroups(parent)
                for group in groups:
                    group.commands[id] = mcd
            else:
                pass
        else:
            parent = "[base]"
            command = longCommand.command # hierarchy[0].name
            #self.baseModule.commands.append(mcd)
            if mcd is not None:
                self.baseModule.commands[id] = mcd

    def clearData(self):
        '''
            self.hasHierarchy = False
            self.hasHelp = False
            self.hasNodes = False
            self.hasCommandList = False
            self.updateStage = 0
            self.hasNodes = False
            self.updateTimer = None
        '''
        self.__init__()

    def __init__(self):
        super().__init__()
        self.hasHierarchy = False
        self.hasHelp = False
        self.hasNodes = False
        self.baseModule = self.GroupHandler(self, None, None)
        self.CommandItem = derivedCommandItem
        self.CommandList = derivedCommandList

        self.fromVer = 20260111184310
        self.toVer = 99999999999999

        self.commands = [self.Base, self.Mute, self.Solenoid, self.BowingWheel, self.DCMotor, self.PID, self.BowPressure, self.BowActuatorHandler,
                         self.Actuator, self.HarmonicSeriesHandler, self.HarmonicSeries, self.MidiConfigurationHandler, self.MidiConfiguration, self.MidiCC,
                         self.ControlBox, self.PluginHandler, self.PluginMultiple, self.PluginLFO, self.PluginMap, self.PluginAHDSR]

        self.updateTimer = None
        self.updateStage = 0

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

    def buildHierarchy(self, commandItem:currentCommandSet.CommandItem, widget):
        self.currentCommandSet.buildHierarchy(commandItem, widget)
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

    def setMidiConfigurationNoteOnCommands(self, sender, serialHandler, simpleFAR, index, commands):
        self.currentCommandSet.setMidiConfigurationNoteOnCommands(sender, serialHandler, simpleFAR, index, commands)

    def setMidiConfigurationNoteOffCommands(self, sender, serialHandler, simpleFAR, index, commands):
        self.currentCommandSet.setMidiConfigurationNoteOffCommands(sender, serialHandler, simpleFAR, index, commands)

    def setMidiConfigurationPolyAftertouchCommands(self, sender, serialHandler, simpleFAR, index, commands):
        self.currentCommandSet.setMidiConfigurationPolyAftertouchCommands(sender, serialHandler, simpleFAR, index, commands)

    def setMidiConfigurationChannelAftertouchCommands(self, sender, serialHandler, simpleFAR, index, commands):
        self.currentCommandSet.setMidiConfigurationChannelAftertouchCommands(sender, serialHandler, simpleFAR, index, commands)

    def setMidiConfigurationProgramChangeCommands(self, sender, serialHandler, simpleFAR, index, commands):
        self.currentCommandSet.setMidiConfigurationProgramChangeCommands(sender, serialHandler, simpleFAR, index, commands)

    def setMidiConfigurationPitchBendCommands(self, sender, serialHandler, simpleFAR, index, commands):
        self.currentCommandSet.setMidiConfigurationPitchBendCommands(sender, serialHandler, simpleFAR, index, commands)

    def setMidiConfigurationContinuousControllerCommands(self, sender, serialHandler, simpleFAR, index, cc, commands):
        self.currentCommandSet.setMidiConfigurationContinuousControllerCommands(sender, serialHandler, simpleFAR, index, cc, commands)

    def processHelpReturn(self, infoReturn, commandReference):
        self.currentCommandSet.processHelpReturn(infoReturn, commandReference)

    def clearData(self):
        self.currentCommandSet.clearData()