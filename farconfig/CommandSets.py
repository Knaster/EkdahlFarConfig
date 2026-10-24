from ModuleSystem import ModuleCommand, Module, ModuleHandler, ModuleGroup, ModuleTypes, HelpModule, HelpCommand

#from commanddefinitions import CommandID, CommandType, defaultCommandType, ModuleCommand, getModuleCommandTypeDesc

from PySide6.QtWidgets import QCompleter
from PySide6.QtCore import Qt, QTimer
from commandparser import Derivedcommandlist, Derivedcommanditem

from CommandSet import CommandSet
from CommandSetOG import CommandSetOG

class CommandSetModular(CommandSet):
    def getCommandAndModule(self, commandContainer:Derivedcommanditem, firstIteration = True) -> (ModuleCommand, Module | ModuleHandler):
        return self.baseModule.getCommandAndModule(commandContainer)

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

    def requestAllData(self, module:Module, serialHandler):
        commands:list[ModuleCommand] = []
        module.requestAllData(commands)
        for command in commands:
            serialHandler.write("rqi:" + command.getFullCommand())

    def processMessages(self, commandItem, commandSets, mainWidget, serialHandler):
        command, module, index = self.splitStringIntoModuleCommandIndex(commandItem)

        if (not self.ready):
            match(command):
                case "ver" | "version": #CommandID.version:
                    if self.loadingStage == 0:
                        serialHandler.write("help,nop")
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
                        if (mainWidget is not None):
                            if (len(commandItem.argument) < 2):
                                pass
                            else:
                                mainWidget.completerList.append(commandItem.argument[0].strip())
                                mainWidget.completerList.append(commandItem.argument[1].strip())
                        pass

                case "nop" | "nooperation": #CommandID.nop:
                    match(self.loadingStage):
                        # End of loading stage 1, beginning of loading stage 2:
                        # Build module hierarchy adding each module and its associated commands as derived from the help
                        case 1:
                            self.baseModule.addHelp()
                            serialHandler.write("ls:m:r:i,nop")
                            self.loadingStage = 2
                        # End of loading stage 2, beginning of loading stage 3:
                        # Build command lists used for preferences and auto-completer
                        case 2:
                            serialHandler.write("ls:c:r:i,nop")
                            self.loadingStage = 3
                        # End of loading stage 3, beginning of loading stage 4:
                        # Build the plugin list and request ALL data from the module that is pertinent; this being judged on the commands types
                        case 3:
                            if (mainWidget is not None):
                                mainWidget.completer = QCompleter(mainWidget.completerList, completionMode=QCompleter.CompletionMode.InlineCompletion,
                                                              filterMode=Qt.MatchFlag.MatchContains, caseSensitivity=Qt.CaseSensitivity.CaseInsensitive)
                                mainWidget.serialWidget.ui.lineEditSend.setCompleter(mainWidget.completer)

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
                            self.ready = True
                            serialHandler.write("nop")

                case _:
                    # Loading stage 4: Add all incoming data into the module structure and build the base data
                    if self.loadingStage == 4:
                        self.baseModule.setCommandData(commandItem)
        else:
            commandX, moduleX = self.getCommandAndModule(commandItem)
            if (commandX is not None):
                match(commandX.helpCommand.commandTypeFunction):
                    case HelpCommand.CommandType_function.ectAddModule:
                        newCommandItem = Derivedcommanditem(commandItem.argument[0] + "[" + str(commandItem.argument[1] + "]"))
                        moduleX.addModule(newCommandItem)
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
        self.__init__()

    def __init__(self):
        super().__init__()
        self.helpModule = HelpModule(self)
        self.baseModule = ModuleHandler(self, self, None, None)
        self.CommandItem = Derivedcommanditem
        self.CommandList = Derivedcommandlist

        self.fromVer = 20260111184310
        self.toVer = 99999999999999
        self.updateStage = 0

        self.ready = False

class CommandSets:
    currentCommandSet:CommandSet = CommandSetOG

    def __init__(self):
        self.currentCommandSet = CommandSetOG()
        self.commandSets = { CommandSetOG(), CommandSetModular() }

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

    def processMessages(self, commandItem, commandSets, mainWidget, serialHandler):
            return self.currentCommandSet.processMessages(commandItem, commandSets, mainWidget, serialHandler)
