#
#  This file is part of The Ekdahl FAR firmware.
#
#  The Ekdahl FAR firmware is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  The Ekdahl FAR firmware is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with The Ekdahl FAR firmware. If not, see <https://www.gnu.org/licenses/>.
#
# Copyright (C) 2024 Karl Ekdahl
#

# This Python file uses the following encoding: utf-8

from commandparser import CommandItem, CommandList

class stringModule:
    def __init__(self):
        self.moduleIndex = -1
        self.retrieveFromHW = True
        self.updateHW = True

        self.commandValues = {}

#        self.fundamentalFrequency = float(-1)
#        self.bowMotorVoltage = float(-1)
        self.pidKp = float(-1)
        self.pidKi = float(-1)
        self.pidKd = float(-1)
        self.integratorError = float(-1)
#        self.bowTimeOut = float(-1)
        self.muteFullMutePosition = float(-1)
        self.muteHalfMutePosition = float(-1)
        self.muteRestPosition = float(-1)
        self.muteBackoff = float(-1)
        self.bowMotorMaxSpeed = float(-1)
        self.bowMotorMinSpeed = float(-1)
        self.bowMaxPressure = float(-1)
        self.bowMinPressure = float(-1)
        self.bowRestPosition = float(-1)
        self.harmonicData = []

        self.stringFrequency = float(-1)
        self.bowFrequency = float(-1)
        self.bowCurrent = float(-1)
        self.setFrequency = float(-1)

        self.solenoidMinForce = float(-1)
        self.solenoidMaxForce = float(-1)
        self.solenoidEngageDuration = float(-1)

        self.cv0 = float(-1)
        self.cv1 = float(-1)
        self.cv2 = float(-1)
        self.cv3 = float(-1)
        self.cv4 = float(-1)
        self.cv5 = float(-1)
        self.cv6 = float(-1)
        self.cv7 = float(-1)
        pass

    def updateRequest(self):
        request = "m:" + str(self.moduleIndex)
        request = "rqi:bowcontrolfundamental"
        return request

    def retrieveUsingFormat(formatString):
        pass

    def getBowRestPosition(self):
        return self.bowRestPosition

    def setBowRestPosition(self, position):
        self.bowRestPosition = position;

    def getBowMinPressure(self):
        return self.bowMinPressure

    def setBowMinPressure(self, pressure):
        self.bowMinPressure = pressure;

    def getBowMaxPressure(self):
        return self.bowMaxPressure

    def setBowMaxPressure(self, pressure):
        self.bowMaxPressure = pressure;

    def getBowMotorMinSpeed(self):
        return self.bowMotorMinSpeed

    def setBowMotorMinSpeed(self, speed):
        self.bowMotorMinSpeed = speed;

    def getBowMotorMaxSpeed(self):
        return self.bowMotorMaxSpeed

    def setBowMotorMaxSpeed(self, speed):
        self.bowMotorMaxSpeed = speed;

    def getMuteRestPosition(self):
        return self.muteRestPosition

    def setMuteRestPosition(self, position):
        self.muteRestPosition = position;

    def getMuteHalfMutePosition(self):
        return self.muteHalfMutePosition

    def setMuteHalfMutePosition(self, position):
        self.muteHalfMutePosition = position;

    def getMuteFullMutePosition(self):
        return self.muteFullMutePosition

    def setMuteFullMutePosition(self, position):
        self.muteFullMutePosition = position;

    def getMuteBackoff(self):
        return self.muteBackoff

    def setMuteBackoff(self, backoff):
        self.muteBackoff = backoff

#    def getBowTimeOut(self):
#        return self.bowTimeOut

#    def setBowTimeOut(self, timeOut):
#        self.bowTimeOut = timeOut;

    def getIntegratorError(self):
        return self.integratorError

    def setIntegratorError(self, ie):
        self.integratorError = ie;

    def getPIDKp(self):
        return self.pidKp

    def setPIDKp(self, Kp):
        self.pidKp = Kp

    def getPIDKi(self):
        return self.pidKi

    def setPIDKi(self, Ki):
        self.pidKi = Ki

    def getPIDKd(self):
        return self.pidKd

    def setPIDKd(self, Kd):
        self.pidKd = Kd

#    def getMotorVoltage(self):
#        return self.bowMotorVoltage

#    def setMotorVoltage(self, inVoltage):
#        self.bowMotorVoltage = inVoltage

#    def getFundamentalFrequency(self):
#        return self.fundamentalFrequency

#    def setFundamentalFrequency(self, inFundamentalFrequency):
#        self.fundamentalFrequency = float(inFundamentalFrequency)

    def setSolenoidMaxForce(self, maxForce):
        self.solenoidMaxForce = maxForce

    def setSolenoidMinForce(self, minForce):
        self.solenoidMinForce = minForce

    def getSolenoidMaxForce(self):
        return self.solenoidMaxForce

    def getSolenoidMinForce(self):
        return self.solenoidMinForce

    def setSetFrequency(self, freq):
        self.setFrequency = freq

    def getSolenoidEngageDuration(self):
        return self.solenoidEngageDuration

    def setSolenoidEngageDuration(self, duration):
        self.solenoidEngageDuration = duration

    def getSetFrequency(self):
        return self.setFrequency

    def setCV(self, ch, value):
        match ch:
            case 0:
                self.cv0 = value
            case 1:
                self.cv1 = value
            case 2:
                self.cv2 = value
            case 3:
                self.cv3 = value
            case 4:
                self.cv4 = value
            case 5:
                self.cv5 = value
            case 6:
                self.cv6 = value
            case 7:
                self.cv7 = value

    def getCV(self, ch):
        match ch:
            case 0:
                return self.cv0
            case 1:
                return self.cv1
            case 2:
                return self.cv2
            case 3:
                return self.cv3
            case 4:
                return self.cv4
            case 5:
                return self.cv5
            case 6:
                return self.cv6
            case 7:
                return self.cv7
    def setCommandValue(self, command, value):
        #if command in self.commandValues:
#        if command == "psf":
#            if value != -1:
#                oop = 3
        self.commandValues[command] = value

    def getCommandValue(self, command):
        if command in self.commandValues:
            return self.commandValues[command]
        else:
            return None

class CC:
    def __init__(self):
        self.control = 0
        self.command = ""

class InstrumentMaster:
    def __init__(self):
        self.evNoteOn = ""
        self.evNoteOff = ""
        self.evPolyAftertouch = ""
        self.evProgramChange = ""
        self.evChannelAftertouch = ""
        self.evPitchbend = ""
        self.evCC = []

        self.cmdNoteOn = CommandList()
        self.cmdNoteOff = CommandList()
        self.cmdPolyAftertouch = CommandList()
        self.cmdPitchbend = CommandList()
        self.cmdSustain = CommandList()
        self.cmdChannelAftertouch = CommandList()

    def getCC(self, control):
        for i in self.evCC:
            if i.control == control:
                return i
        return

    def addCC(self, control, command):
        for i in self.evCC:
            if i.control == control:
                print("replacing cc")
                i.command = command
                return
        a = CC()
        a.command = command
        a.control = control
        self.evCC.append(a)
        print("adding new cc")
