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

class CommandItem:
    def startOfQuote(self, inCommandString, index, quote):
                                                #        print("Start of quote " + inCommandString[index:])
        while index < len(inCommandString):
            if inCommandString[index] == quote:
                return index
            index += 1
        print("Couldn't find end of quote")
        exit()
        return -1

    def __init__(self, inCommandString):
        self.argument = []
        self.command = ""

        inCommandString = inCommandString.strip(' ')
        foundIndex = inCommandString.find(":")
        if foundIndex == -1:
            self.command = inCommandString
#            print("adding command " + inCommandString)
            return
        else:
            self.command = inCommandString[:foundIndex]
#            print("adding command " + self.command)

        foundIndex += 1
        startIndex = foundIndex
        while foundIndex < len(inCommandString):
            if (inCommandString[foundIndex] == ":") and (startIndex != foundIndex):
#                print("adding argument " + inCommandString[startIndex:foundIndex])
                self.argument.append(str(inCommandString[startIndex:foundIndex]))
                startIndex = foundIndex + 1
            elif inCommandString[foundIndex] == "\"" or inCommandString[foundIndex] == "'":
                startIndex = foundIndex
                foundIndex = self.startOfQuote(inCommandString, foundIndex + 1, inCommandString[foundIndex])
                self.argument.append(inCommandString[startIndex + 1:foundIndex])
#                print("adding quoted string argument " + inCommandString[startIndex + 1:foundIndex])
                startIndex = foundIndex + 1
            foundIndex += 1

        if startIndex < foundIndex:
#            print("adding restoring as argument " + inCommandString[startIndex:foundIndex])
            self.argument.append(str(inCommandString[startIndex:foundIndex]))

    def print(self):
        print("command " + self.command)
        for i in self.argument:
            print("argument " + i)

class CommandList:
#    commands = []

    def startOfQuote(self, inCommandString, index, quote):
#        print("Start of quote")
        while index < len(inCommandString):
            if inCommandString[index] == quote:
                return index
            index += 1
#        print("Couldn't find end of quote")
        return -1

    def waitIfProcessing(self):
        while self.processingCommands:
            pass

    def clear(self):
        self.commands.clear()

    def getCommandAttribute(self, command, attribute):
        for i in self.commands:
            if i.command == command:
                if len(i.argument) > attribute:
                    return i.argument[attribute] #[0]
                else:
                    return ""
        return ""

    def addCommands(self, commandItems):
        startIndex = 0
        foundIndex = 0
        while foundIndex < len(commandItems):

            if commandItems[foundIndex] == "\"" or commandItems[foundIndex] == "'":
#                print("Found quote in command string at " + str(foundIndex))
                foundIndex = self.startOfQuote(commandItems, foundIndex + 1, commandItems[foundIndex])
                if (foundIndex == -1):
                    print("Error parsing string " + commandItems)
                    return False

#                print("Skipped forward to " + str(foundIndex))
            elif commandItems[foundIndex] == ",":
#                print("Found command at " + str(startIndex) + ":" + str(foundIndex) + " " + commandItems[startIndex:foundIndex].strip(' '))
                self.commands.append(CommandItem(commandItems[startIndex:foundIndex]))
                startIndex = foundIndex + 1
            foundIndex += 1

        if startIndex < foundIndex:
#            print("restoring data " + commandItems[startIndex:foundIndex])
            self.commands.append(CommandItem(commandItems[startIndex:foundIndex]))

        return True

    def print(self):
        for i in self.commands:
            i.print()

    # buildCommandString will strip all commands in ignoreCommands from the command list
    def buildCommandString(self, ignoreCommands):
        commandString = ""
        for i in self.commands:
            found = False
            for a in ignoreCommands:
                if i.command == a:
                    found = True
            if not found:
                commandString += i.command
                for a in i.argument:
                    commandString += ":" + a
                commandString += ","
        return commandString[0:len(commandString) - 1]


    def __init__(self, commands = ""):
        self.commands = []
        self.processingCommands = False
        if not commands == "":
            self.addCommands(commands)
        pass
