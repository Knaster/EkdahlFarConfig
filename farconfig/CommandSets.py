from ModuleSystem import ModuleCommand, Module, ModuleHandler, ModuleGroup, ModuleTypes, HelpModule, HelpCommand

from commanddefinitions import CommandID, CommandType, defaultCommandType, ModuleCommand, getModuleCommandTypeDesc
#from farconfig import serialHandler

#from general_helpers import stripLeadingQuotes, messageBox

from PySide6.QtWidgets import QCompleter
from PySide6.QtCore import Qt, QTimer
from commandparser import Derivedcommandlist, Derivedcommanditem

from CommandSet import CommandSet
from CommandSetOG import CommandSetOG

class CommandSetModular(CommandSet):
    '''
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
            CommandID.pluginLFOBipolar : "bp",
            CommandID.pluginLFOOutputValue : "ov"
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
            CommandID.pluginLFOBipolar: "bipolar",
            CommandID.pluginLFOOutputValue: "outputvalue"
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
    '''

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
    '''
    def getCommandType(self, commandItem):
        command, module, index = self.getCommandModuleAndCommand(commandItem)
        id = self.getCommandID(command, module)
        if (id in defaultCommandType):
            return defaultCommandType[id]
        return CommandType.undefined
    '''
    '''
    def getCommandDataS(self, commandString: str):
        return self.baseModule.getCommandDataS(commandString)

    def getCommandData(self, commandItem: Derivedcommanditem):
        return self.baseModule.getCommandData(commandItem)

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
    '''
    def getCommandAndModule(self, commandContainer:Derivedcommanditem, firstIteration = True) -> (ModuleCommand, Module | ModuleHandler):
        return self.baseModule.getCommandAndModule(commandContainer)

    '''
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
                id, trash = moduleP.getCommandID(moduleP, command)
                return id, moduleP

            if (module == ""):
                for commandP in moduleP.longCommands:
                    if (commandP == command):
                        id, trash = moduleP.getCommandID(moduleP, command)
                        return id, moduleP
                for commandP in moduleP.shortCommands:
                    if (commandP == command):
                        id, trash = moduleP.getCommandID(moduleP, command)
                        return id, moduleP

            #if (module in group.longName) or (module in group.shortName):
        return None
    '''
    '''
    def initialRequest(self) -> list:
        return ["ls:m:r:i", "nop", "help", "nop"]
    '''
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

    def splitStringIntoModuleCommandIndex(self, commandString:str):
        newCommandItem = Derivedcommanditem(commandString)
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


    def getModuleHierarchy(self, inModule:ModuleHandler | Module):
        hierarchy = []
        if (inModule.longName != ""):
            hierarchy.insert(0, [inModule.longName, inModule.getIndex()])
        if (inModule.parent is not None) and not isinstance(inModule.parent, CommandSetModular):
            newHierarchy = self.getModuleHierarchy(inModule.parent)
            hierarchy = newHierarchy + hierarchy
        return hierarchy
    '''
    def commandHasStorableDataCI(self, command:Derivedcommanditem):
        commandData = self.baseModule.getCommandData(command)
        if (not isinstance(commandData, ModuleCommand)): return False
        return self.commandHasStorableDataHlp(commandData.helpCommand)

    def commandHasStorableDataCmd(self, command:ModuleCommand):
        return self.commandHasStorableDataHlp(command.helpCommand)

    def commandHasStorableDataHlp(self, helpCommand:HelpCommand):
        if (helpCommand.commandTypeAccess != HelpCommand.CommandType_access.ectInvokeOnly and
                (helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectParameter or
                 helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectCountModules or
                 helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectName or
                 helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectIndex or
                 helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectAssignment) and
                (not helpCommand.commandTypeLogic)):

            if (helpCommand.shortCommand != "nop" and helpCommand.shortCommand != "rqi" and helpCommand.shortCommand != "ver" and
                    helpCommand.longCommand != "" and (not helpCommand.hidden)):

                return True
        return False
    '''
    def requestAllData(self, module:Module, serialHandler):
        commands:list[ModuleCommand] = []
        module.requestAllData(commands)
        for command in commands:
            serialHandler.write("rqi:" + command.getFullCommand())

        #if hasattr(module, "children"):
        #    for child in module.children:
        #        name = child.fullCommand[:child.fullCommand.rfind("[") + 1] + "]"
        #        serialHandler.write("rqi:" + name)
        #        self.requestAllData(child, serialHandler)

    def processMessages(self, commandItem, commandSets, mainWidget, serialHandler):
        command, module, index = self.splitStringIntoModuleCommandIndex(commandItem)

        #id, trash = self.getCommandID(command, module)
        found = True
        if (not self.ready):
            match(command):
                case "ver" | "version": #CommandID.version:
                    if self.loadingStage == 0:
                        serialHandler.write("help,nop")
                        self.hasHierarchy = False
                        self.loadingStage = 1
                        pass

                # Loading stage 1; build the help system
                case "help":
                    newItem = Derivedcommanditem(commandItem.argument[0])
                    newItem.argument = commandItem.argument[1:]
                    self.helpModule.addEntry(newItem)
                    pass

                case "list" | "ls":
                    # Loading stage 2: Build module hierarchy adding each module and its associated commands as derived from the help
                    if (self.loadingStage == 2):
                        self.buildHierarchy(commandItem, mainWidget)
                    # Loading stage 3: Build command lists used for preferences and auto-completer
                    elif (self.loadingStage == 3):
                        #mainWidget.preferences.addCommandToCommandsComboBox(commandItem)
                        if (mainWidget is not None):
                            mainWidget.completerList.append(commandItem.argument[0].strip())
                            mainWidget.completerList.append(commandItem.argument[1].strip())
                        pass

                case "nop" | "nooperation": #CommandID.nop:
                    match(self.loadingStage):
                        # End of loading stage 1, beginning of loading stage 2:
                        # Build module hierarchy adding each module and its associated commands as derived from the help
                        case 1:
                            self.baseModule.addHelp()
                            #self.hasHelp = True
                            serialHandler.write("ls:m:r:i,nop")
                            self.loadingStage = 2
                        # End of loading stage 2, beginning of loading stage 3:
                        # Build command lists used for preferences and auto-completer
                        case 2:
                            #self.hasHierarchy = True
                            #self.hasCommandList = False
                            serialHandler.write("ls:c:r:i,nop")
                            self.loadingStage = 3
                        # End of loading stage 3, beginning of loading stage 4:
                        # Build the plugin list and request ALL data from the module that is pertinent; this being judged on the commands types
                        case 3:
                            #elif (not self.hasCommandList):
                            #self.hasCommandList = True
                            if (mainWidget is not None):
                                mainWidget.completer = QCompleter(mainWidget.completerList, completionMode=QCompleter.CompletionMode.InlineCompletion,
                                                              filterMode=Qt.MatchFlag.MatchContains, caseSensitivity=Qt.CaseSensitivity.CaseInsensitive)
                                mainWidget.serialWidget.ui.lineEditSend.setCompleter(mainWidget.completer)

                            #self.requestAllData(self.baseModule, serialHandler)
                            commands:list[ModuleCommand]=[]
                            self.baseModule.requestAllData(commands)
                            for command in commands:
                                out = "rqi:" + command.getFullCommand()
                                if (command.isIndex): out += "[]"
                                serialHandler.write(out)

                            serialHandler.write("nop")
                            self.loadingStage = 4
                        # End of loading stage 4: device ready for regular i/o
                        case 4:
                            #self.hasPluginList = True
                            self.ready = True
                            serialHandler.write("nop")

                case _:
                    # Loading stage 4: Add all incoming data into the module structure and build the base data
                    if self.loadingStage == 4:
                        self.baseModule.setCommandData(commandItem)
        else:
            #if (self.commandHasStorableDataCI(commandItem)):
            commandX, moduleX = self.getCommandAndModule(commandItem)
            if (commandX is not None):
                match(commandX.helpCommand.commandTypeFunction):
                    case HelpCommand.CommandType_function.ectAddModule:
                        newCommandItem = Derivedcommanditem(commandItem.argument[0] + "[" + str(commandItem.argument[1] + "]"))
                        newModule = moduleX.addModule(newCommandItem)
                        self.requestAllData(moduleX, serialHandler)
                        pass
                    case HelpCommand.CommandType_function.ectRemoveModule:
                        if (len(commandItem.argument) >= 2):
                            moduleX.removeModule(commandItem.argument[0], commandItem.argument[1])
                            self.requestAllData(moduleX, serialHandler)
                        else:
                            pass

            self.baseModule.setCommandData(commandItem)

        return True

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
        self.hasPluginList = False
        self.helpModule = HelpModule(self)
        self.baseModule = ModuleHandler(self, self, None, None)
        #self.baseModule.helpModule = self.helpModule
        self.CommandItem = Derivedcommanditem
        self.CommandList = Derivedcommandlist

        self.fromVer = 20260111184310
        self.toVer = 99999999999999
        '''
        self.commands = [self.Base, self.Mute, self.Solenoid, self.BowingWheel, self.DCMotor, self.PID, self.BowPressure, self.BowActuatorHandler,
                         self.Actuator, self.HarmonicSeriesHandler, self.HarmonicSeries, self.MidiConfigurationHandler, self.MidiConfiguration, self.MidiCC,
                         self.ControlBox, self.PluginHandler, self.PluginMultiple, self.PluginLFO, self.PluginMap, self.PluginAHDSR]
        '''
        self.updateStage = 0

        self.ready = False

class CommandSets:
    currentCommandSet:CommandSet = CommandSetOG

    '''
    def getCommandType(self, commandItem):
        return self.currentCommandSet.getCommandType(commandItem)

    def getCommandID(self, commandItem, module = None):
        return self.currentCommandSet.getCommandID(commandItem, module)
    '''
    '''
    def initialRequest(self):
        return self.currentCommandSet.initialRequest()
    '''
    '''
    def requestData(self, serialHandler):
        return self.currentCommandSet.requestData(serialHandler)

    def requestContinuousData(self, serialHandler):
        self.currentCommandSet.requestContinuousData(serialHandler)
    '''
    def __init__(self):
        self.currentCommandSet = CommandSetOG()
        self.commandSets = { CommandSetOG(), CommandSetModular() }
        #self.currentCommandSet = None
        #self.commandSets = { CommandSetModular()}

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
    '''
    def getQualifiedShortCommand(self, commandID, selectionIndex = None, stripIndex = False):
        return self.currentCommandSet.getQualifiedShortCommand(commandID, selectionIndex, stripIndex)
    '''
    def processMessages(self, commandItem, commandSets, mainWidget, serialHandler):
            return self.currentCommandSet.processMessages(commandItem, commandSets, mainWidget, serialHandler)
    '''
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
    
    def saveActuator(self, sender, serialHandler, simpleFARHandler, newIndex, name, rest = 0, engage = 2000, stall = 60000):
        return self.currentCommandSet.saveActuator(sender, serialHandler, simpleFARHandler, newIndex, name, rest, engage, stall)
    
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

    def getCommandAndModule(self, inCommand, module = None):
        return self.currentCommandSet.getCommandAndModule((inCommand, module))
    
    def getCommandDataS(self, commandString: str):
        return self.currentCommandSet.baseModule.getCommandDataS(commandString)

    def getCommandData(self, commandItem: Derivedcommanditem):
        return self.currentCommandSet.baseModule.getCommandData(commandItem)
    '''