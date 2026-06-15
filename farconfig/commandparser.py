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
        #print("Start of quote " + inCommandString[index:])
        while index < len(inCommandString):
            if inCommandString[index] == quote:
                return index
            index += 1
        print("Couldn't find end of quote")
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
                cmd = str(inCommandString[startIndex:foundIndex])
                if (cmd == ":"):
                    self.argument.append("")
                else:
                    self.argument.append(cmd)
                startIndex = foundIndex + 1
            elif (inCommandString[foundIndex] == ":") and (startIndex == foundIndex):
                self.argument.append("")
            elif (inCommandString[foundIndex] == "\"" or inCommandString[foundIndex] == "'") and ((foundIndex + 1) < len(inCommandString)):
                startIndex = foundIndex
                foundIndex = self.startOfQuote(inCommandString, foundIndex + 1, inCommandString[foundIndex])
                if (foundIndex != -1):
                    self.argument.append(inCommandString[startIndex + 1:foundIndex])
#                print("adding quoted string argument " + inCommandString[startIndex + 1:foundIndex])
                    foundIndex += 1
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
    commandItem = CommandItem

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
                self.commands.append(self.commandItem(commandItems[startIndex:foundIndex]))
                startIndex = foundIndex + 1
            foundIndex += 1

        if startIndex < foundIndex:
#            print("restoring data " + commandItems[startIndex:foundIndex])
            if (commandItems[startIndex:foundIndex] != ""):
                self.commands.append(self.commandItem(commandItems[startIndex:foundIndex]))
            else:
                pass

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

class derivedCommandItem(CommandItem):
    class commandItemPart:
        def __init__(self, inName, inSelection):
            self.name: str = inName
            self.selection: list = inSelection

    def __init__(self, inCommandString):
        if (isinstance(inCommandString, str)):
            super().__init__(inCommandString)
        if (isinstance(inCommandString, CommandItem)):
            self.command = inCommandString.command
            self.argument = inCommandString.argument

        self.hierarchy: list = []
        self.hierarchyIndex = 0
        self.selection: list = []
        self.buildHierarchy()

    def buildHierarchy(self):
        self.hierarchyIndex = 0
        self.hierarchy.clear()

        start = 0
        end = 0
        self.command: str = self.command
        while (end < len(self.command)):
            end = self.command.find('.', start)
            if (end == -1): end = len(self.command)
            portion = self.command[start:end]
            thisSel: list = []

            i = portion.find('[')
            j = portion.find(']')
            if ((i != -1) and (j != -1)):
                i += 1
                k = 0
                while (k < j):
                    k = portion.find(',', i + 1)
                    if (k == -1): k = j
                    sel = portion[i:k]
                    l = sel.find('-')
                    if (l == -1):
                        try:
                            thisSel.append(int(sel))
                        except:
                            pass
                    else:
                        m = int(sel[0:l])
                        n = int(sel[l + 1: len(sel)])
                        if ((n < m) or (m < 0) or (n < 0) or (m > 255) or (n > 255)):
                            raise ("Invalid selection range!")
                        for m in range(m, n):
                            thisSel.append(m)
                    i = k + 1
                portion = portion[0:portion.find('[')]
            self.hierarchy.append(self.commandItemPart(portion, thisSel))
            start = end + 1


class derivedCommandList(CommandList):
    def __init__(self, commands=""):
        self.commandItem = derivedCommandItem
        super().__init__(commands)

def getCommandIndex(inCommandItem:derivedCommandItem):
    if (len(inCommandItem.hierarchy) < 2): return 0
    if (len(inCommandItem.hierarchy[len(inCommandItem.hierarchy) - 2].selection) < 1): return 0
    return int(inCommandItem.hierarchy[len(inCommandItem.hierarchy) - 2].selection[0])
