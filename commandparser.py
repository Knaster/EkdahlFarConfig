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
            if inCommandString[foundIndex] == ":":
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

    def addCommands(self, commandItems):
        startIndex = 0
        foundIndex = 0
        while foundIndex < len(commandItems):

            if commandItems[foundIndex] == "\"" or commandItems[foundIndex] == "'":
#                print("Found quote in command string at " + str(foundIndex))
                foundIndex = self.startOfQuote(commandItems, foundIndex + 1, commandItems[foundIndex])
#                print("Skipped forward to " + str(foundIndex))
            elif commandItems[foundIndex] == ",":
#                print("Found command at " + str(startIndex) + ":" + str(foundIndex) + " " + commandItems[startIndex:foundIndex].strip(' '))
                self.commands.append(CommandItem(commandItems[startIndex:foundIndex]))
                startIndex = foundIndex + 1
            foundIndex += 1

        if startIndex < foundIndex:
#            print("restoring data " + commandItems[startIndex:foundIndex])
            self.commands.append(CommandItem(commandItems[startIndex:foundIndex]))

    def print(self):
        for i in self.commands:
            i.print()

    def __init__(self):
        self.commands = []
        self.processingCommands = False
        pass
