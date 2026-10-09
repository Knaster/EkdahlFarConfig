from CommandSet import CommandSet
from commandparser import Derivedcommanditem, Derivedcommandlist
from commanddefinitions import CommandID, CommandType

from general_helpers import messageBox

class CommandSetOG(CommandSet):
    CommandItem = Derivedcommanditem
    CommandList = Derivedcommandlist

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

    '''
    def initialRequest(self):
        return ["help"]
    '''
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
        return cId, None

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

