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

from commandparser import derivedCommandList as CommandList
from commandparser import derivedCommandItem as CommandItem

class stringModule:
    def __init__(self):
        self.moduleIndex = -1
        self.retrieveFromHW = True
        self.updateHW = True

        self.commandValues = {}
        self.harmonicData = []

        self.adcValue = [0,0,0,0,0,0,0,0]
        self.adcCommand = ["","","","","","","",""]
        self.adcCommandLists = [CommandList(),CommandList(),CommandList(),CommandList(),CommandList(),CommandList(),CommandList(),CommandList()]
        pass

    def updateRequest(self):
        request = "rqi:bowcontrolfundamental"
        return request

    def setCVValue(self, ch, value):
        self.adcValue[int(ch)] = int(value);
        return

    def getCVValue(self, ch):
        return self.adcValue[int(ch)]

    # This function will add any single value instrument data to the commandValues dictionary
    # where the key is the associated command
    def setCommandValue(self, command, value, index = 0):
        if (command in self.commandValues):
            try:
                if len(self.commandValues[command]) <= index:
                    self.commandValues[command].insert(index, value)
                else:
                    self.commandValues[command][index] = value
            except:
                pass
        else:
            if (index == 0):
                self.commandValues[command] = [value]
            else:
                pass


    def getCommandValue(self, command, index = 0):
        #if command in self.commandValues:
        try:
            return self.commandValues[command][index]
        #else:
        except:
            return -1

    def setCVCommand(self, channel, command):
        channel = int(channel)
        self.adcCommandLists[channel] = CommandList(command)
        self.adcCommand[channel] = command

    def getCVCommand(self, channel):
        channel = int(channel)
        return self.adcCommand[channel]

    def getCVCommandList(self, channel):
        channel = int(channel)
        return self.adcCommandLists[channel]

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

class SimpleFARHandler:
    stringModules = []
    instrumentMaster = InstrumentMaster()
    moduleCount = 0
#    currentHarmonicListSelected = 0
    currentShowingModule = 0
    connected = False
