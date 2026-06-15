from enum import Enum, auto, IntEnum

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
    help = auto()

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
    bowPressureTMCInfo = auto()

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
    midiConfigurationNoteOn = auto()
    midiConfigurationNoteOff = auto()
    midiConfigurationPolyAT = auto()
    midiConfigurationChannelAT = auto()
    midiConfigurationPitchbend = auto()
    midiConfigurationProgramChange = auto()
    midiConfigurationContinuousController = auto()
    midiConfigurationCCControl = auto()
    midiConfigurationCCCommands = auto()

    controlBoxControlData = auto()
    controlBoxControlDefaults = auto()
    controlBoxDataReturn = auto()
    controlBoxADCSettings = auto()
    controlBoxHarmonic = auto()
    controlBoxHarmonicShift = auto()
    controlBoxFinetune = auto()
    controlBoxPressure = auto()
    controlBoxHammerTrig = auto()
    controlBoxGate = auto()
    controlBoxHammerScale = auto()
    controlBoxMute = auto()

    testADCLatency = auto()
    testADCLatencyReturn = auto()
    testADCMinMax = auto()

    pluginHandlerAdd = auto()
    pluginHandlerRemove = auto()
    pluginHandlerCount = auto()

    pluginMultName = auto()
    pluginMultTarget = auto()
    pluginMultData = auto()
    pluginMultRemove = auto()

    pluginLFOName = auto()
    pluginLFOEnable = auto()
    pluginLFOTarget = auto()
    pluginLFOUpdateRate = auto()
    pluginLFOWaveform = auto()
    pluginLFOFrequency = auto()
    pluginLFOAmpltiude = auto()
    pluginLFODelay = auto()
    pluginLFOResetDelay = auto()
    pluginLFOResetWave = auto()
    pluginLFOBipolar = auto()

    pluginAHDSRName = auto()
    pluginAHDSREnable = auto()
    pluginAHDSRTarget = auto()
    pluginAHDSRUpdateRate = auto()
    pluginAHDSRGate = auto()
    pluginAHDSRAttack = auto()
    pluginAHDSRHold = auto()
    pluginAHDSRDecay = auto()
    pluginAHDSRSustain = auto()
    pluginAHDSRRelease = auto()
    pluginAHDSRReleaseTarget = auto()
    pluginAHDSRAmpltiude = auto()
    pluginAHDSRInvert = auto()

    pluginMapName = auto()
    pluginMapTarget = auto()
    pluginMapData = auto()
    pluginMapRemove = auto()
    pluginMapScale = auto()
    pluginMapTrigger = auto()

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
    CommandID.harmonicSeriesSelect : CommandType.index,

    CommandID.pluginLFOName : CommandType.simple,
    CommandID.pluginLFOTarget : CommandType.simple,
    CommandID.pluginLFODelay : CommandType.simple,
    CommandID.pluginLFOWaveform : CommandType.simple,
    CommandID.pluginLFOFrequency : CommandType.simple,
    CommandID.pluginLFOEnable : CommandType.simple,
    CommandID.pluginLFOAmpltiude : CommandType.simple,

    CommandID.pluginAHDSRName : CommandType.simple,
    CommandID.pluginAHDSRAmpltiude : CommandType.simple,
    CommandID.pluginAHDSRAttack : CommandType.simple,
    CommandID.pluginAHDSRHold: CommandType.simple,
    CommandID.pluginAHDSRDecay: CommandType.simple,
    CommandID.pluginAHDSRSustain: CommandType.simple,
    CommandID.pluginAHDSRRelease: CommandType.simple,
    CommandID.pluginAHDSREnable: CommandType.simple,
    CommandID.pluginAHDSRInvert: CommandType.simple,
    CommandID.pluginAHDSRTarget: CommandType.simple,
    CommandID.pluginAHDSRReleaseTarget: CommandType.simple,

    CommandID.pluginMapData : CommandType.advanced,
    CommandID.pluginMapScale : CommandType.simple,
    CommandID.pluginMapName : CommandType.simple,
    CommandID.pluginMapTarget : CommandType.simple,

    CommandID.pluginMultName : CommandType.simple,
    CommandID.pluginMultTarget : CommandType.simple,
    CommandID.pluginMultData : CommandType.simple
}

class ModuleCommandType_data(IntEnum):
    SimpleString = 0
    SimpleBool = 1
    SimpleFloat = 2
    SimpleUInt8 = 3
    SimpleInt16 = 4
    SimpleUInt16 = 5
    Commands = 6
    Data = 7
    Conditional = 8
    Immediate = 9
    Milliseconds = 10
    Microseconds = 11
    Hertz = 12
    OutputAssignment = 13
    SimpleInt8 = 14

ModuleCommandType_data_desc = {
    ModuleCommandType_data.SimpleString : "Text",
    ModuleCommandType_data.SimpleBool : "1|0 / true|false",
    ModuleCommandType_data.SimpleFloat : "Decimal number",
    ModuleCommandType_data.SimpleUInt8 : "Value 0-255",
    ModuleCommandType_data.SimpleInt16 : "Value -322767 - 32767",
    ModuleCommandType_data.SimpleUInt16 : "Value 0-65535",
    ModuleCommandType_data.Commands : "One or more commands",
    ModuleCommandType_data.Data : "Data, defined per command",
    ModuleCommandType_data.Conditional : "Conditional, where '1' means execute",
    ModuleCommandType_data.Immediate : "Immediate; executes without arguments",
    ModuleCommandType_data.Milliseconds : "Argument is in milliseconds",
    ModuleCommandType_data.Microseconds : "Argument is in microseconds",
    ModuleCommandType_data.Hertz : "Argument in Hertz",
    ModuleCommandType_data.OutputAssignment : "One or more commands to execute when a specific event happens",
    ModuleCommandType_data.SimpleInt8: "Value -127 - 127"
}

eCT_do_sh = 5

class ModuleCommandType_dataOptions(IntEnum):
    Static = 0b0 << eCT_do_sh
    Expression = 0b1 << eCT_do_sh

ModuleCommandType_dataOptions_desc = {
    ModuleCommandType_dataOptions.Static : "Static; argument is taken exactly as written",
    ModuleCommandType_dataOptions.Expression : "Expression; argument(s) can be or contain mathematical expressions and/or variables"
}

eCT_ac = (eCT_do_sh + 1)

class ModuleCommandType_access(IntEnum):
    Normal = 0b00 << eCT_ac
    Request = 0b01 << eCT_ac
    SelfInvoked = 0b10 << eCT_ac
    InvokeOnly = 0b11 << eCT_ac

ModuleCommandType_access_desc = {
    ModuleCommandType_access.Normal : "Normal; Command can be used to set or request a value",
    ModuleCommandType_access.Request : "Request-only; Command cannot be set",
    ModuleCommandType_access.SelfInvoked : "Self-invoked; Command will automatically be triggered under certain circumstances",
    ModuleCommandType_access.InvokeOnly : "Invoke only; Command does not return any value if requested and may execute if so"
}

eCT_fu = (eCT_ac + 3)

class ModuleCommandType_function(IntEnum):
    Parameter = (0 << eCT_fu)
    Setting = (1 << eCT_fu)
    Add = (2 << eCT_fu)
    Remove = (3 << eCT_fu)
    Count = (4 << eCT_fu)
    Name = (5 << eCT_fu)
    Index = (6 << eCT_fu)
    System = (7 << eCT_fu)
    Undefined = (8 << eCT_fu)
    VolatileSetting = (9 << eCT_fu)
    Assignment = (10 << eCT_fu)
    Logic = (11 << eCT_fu)

ModuleCommandType_function_desc = {
    ModuleCommandType_function.Parameter : "Parameter, generally usable during performance",
    ModuleCommandType_function.Setting : "Setting, generally only used during setup",
    ModuleCommandType_function.Add : "Add, adds a new item",
    ModuleCommandType_function.Remove : "Remove, removes an item",
    ModuleCommandType_function.Count : "Count, lists the number of items",
    ModuleCommandType_function.Name : "Name, sets the name of an item",
    ModuleCommandType_function.Index : "Index, selects an item",
    ModuleCommandType_function.System : "System, command is generally not very useful to a direct user/player",
    ModuleCommandType_function.Undefined : "Undefined, command doesn't fit in the other categories",
    ModuleCommandType_function.VolatileSetting : "Setting is volatile, meaning it might be able to break the instrument if set wrong",
    ModuleCommandType_function.Assignment : "Assignment, command assigns commands to execute during an event",
    ModuleCommandType_function.Logic : "Logic, command performs a logical function and doesn't change anything in itself"
}

def parseModuleCommandType(inMCT:int):
    data = inMCT & 0b11111
    options = inMCT & (0b1 <<  eCT_do_sh)
    access = inMCT &  (0b111 << eCT_ac)
    func = inMCT & (0b1111 << eCT_fu)
    return data, options, access, func

def getModuleCommandTypeDesc(inMCT):
    try:
        data, options, access, func = parseModuleCommandType(int(inMCT))

        out = "Command value type: " + ModuleCommandType_data_desc[data] + "\n\nArgument style: " + \
              ModuleCommandType_dataOptions_desc[options] + "\n\nAccess type: " + \
              ModuleCommandType_access_desc[access] + "\n\nCommand function style: " + \
              ModuleCommandType_function_desc[func]
    except:
        out = ""
        pass
    return out

'''
class ModuleCommandType(Enum):
    SimpleString = 0,
    SimpleBool = 1,
    SimpleFloat = 2,
    SimpleUInt8 = 3,
    SimpleInt16 = 4,
    SimpleUInt16 = 5,
    Commands = 6,
    Data = 7,
    Conditional = 8,
    ReturnOnly = 9,
    Immediate = 10,
    Expression = 11,
    Add = 12,
    Remove = 13,
    Count = 14,
    Name = 15,
    Index = 16,
    Milliseconds = 17,
    Microseconds = 18,
    Hertz = 19,
    RequestOnly = 20,
    ReturnRequest = 21,
    OutputAssignment = 22

ModuleCommandTypeDescription = {
    "string" : ModuleCommandType.SimpleString,
    "bool" : ModuleCommandType.SimpleBool,
    "float" : ModuleCommandType.SimpleFloat,
    "uint8" : ModuleCommandType.SimpleUInt8,
    "int16" : ModuleCommandType.SimpleInt16,
    "uint16" : ModuleCommandType.SimpleUInt16,
    "commands" : ModuleCommandType.Commands,
    "data" : ModuleCommandType.Data,
    "conditional" : ModuleCommandType.Conditional,
    "returnonly" : ModuleCommandType.ReturnOnly,
    "immediate" : ModuleCommandType.Immediate,
    "expression" : ModuleCommandType.Expression,
    "add" : ModuleCommandType.Add,
    "remove" : ModuleCommandType.Remove,
    "count" : ModuleCommandType.Count,
    "name" : ModuleCommandType.Name,
    "index" : ModuleCommandType.Index,
    "milliseconds" : ModuleCommandType.Milliseconds,
    "microseconds" : ModuleCommandType.Microseconds,
    "hertz" : ModuleCommandType.Hertz,
    "requestonly" : ModuleCommandType.RequestOnly,
    "returnrequest" : ModuleCommandType.ReturnRequest,
    "outputassignment" : ModuleCommandType.OutputAssignment
}
'''

class ModuleCommand:
    def __init__(self, inLongCommand, inShortCommand, inArguments = "[select]", inDescription = "", inHidden = False, inCommandType = 0, inVariables = None):
        self.longCommand = inLongCommand
        self.shortCommand = inShortCommand
        self.arguments = inArguments
        self.description = inDescription
        self.hidden = inHidden
        self.commandType = inCommandType #ModuleCommandTypeDescription[inCommandType]
        self.variables = inVariables