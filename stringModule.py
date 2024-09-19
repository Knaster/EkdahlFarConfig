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
        self.harmonicData = []

        self.adcValue = [0,0,0,0,0,0,0,0]
        self.adcCommand = ["","","","","","","",""]
        pass

    def updateRequest(self):
        request = "m:" + str(self.moduleIndex)
        request = "rqi:bowcontrolfundamental"
        return request

    def setCVValue(self, ch, value):
        self.adcValue[int(ch)] = int(value);
        return

    def getCVValue(self, ch):
        return self.adcValue[int(ch)]

    def setCommandValue(self, command, value):
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
