from enum import Enum, auto

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
