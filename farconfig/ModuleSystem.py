from __future__ import annotations
from typing import Callable, Any

#from commanddefinitions import ModuleCommand
from commandparser import Derivedcommanditem
from enum import Enum, auto, IntEnum

def commandHasStorableDataHlp(helpCommand: HelpCommand):
    if (helpCommand.commandTypeAccess != HelpCommand.CommandType_access.ectInvokeOnly and
            (helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectCalibration or
             helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectCountModules or
             helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectName or
             helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectIndex or
             helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectAssignment or
             helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectLiveParameter or
             helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectAdminSetting) and
            (not helpCommand.commandTypeLogic)):

        if (helpCommand.shortCommand != "nop" and helpCommand.shortCommand != "rqi" and helpCommand.shortCommand != "ver" and
                helpCommand.longCommand != "" and (not helpCommand.hidden)):
            return True
    return False

def commandHasStorableDataCmd(command: ModuleCommand):
    return commandHasStorableDataHlp(command.helpCommand)

class ModuleCommand:
    def __init__(self, helpCommand:HelpCommand, arguments:list[str], parent, isIndex = False):
        self.longCommand:str = helpCommand.longCommand
        self.shortCommand:str = helpCommand.shortCommand
        self.helpCommand:HelpCommand = helpCommand
        self.arguments:list[str] = arguments
        self.dataChanged:bool = True
        self.callbacks:list[ModuleCommand.Callback] = []
        self.parent:Module = parent
        self.isIndex = isIndex
        self.nodePort = None
        #self.fullCommand:str = self.getFullCommand()
        pass

    class Callback:
        def __init__(self, callback:Callable[[any], None], guiCallback:Any, parent:ModuleCommand, force=False):
            self.callback:Callable[[any], None] = callback
            self.guiCallback:Any = guiCallback
            self.force:bool = force
            self.parent = parent

    def addCallback(self, callback:Callable[[any], None], guiCallback=None, force:bool=False):
        for myCallback in self.callbacks:
            if myCallback.callback == callback and myCallback.guiCallback == guiCallback:
                return myCallback
        thisCallback = ModuleCommand.Callback(callback, guiCallback, self, force)
        self.callbacks.append(thisCallback)
        return thisCallback

    def removeCallback(self, callback:Callback):
        #if callback in self.callbacks:
        #    self.callbacks.remove(callback)
        for myCallback in self.callbacks:
            if myCallback == callback:
                self.callbacks.remove(myCallback)
                return

    def setData(self, data:Any):
        newData = False
        if (data != self.arguments):
            if (len(data) > 0) and (data[0] == "[0]"):
                pass
            self.arguments = data
            self.dataChanged = True
            newData = True

        for callback in self.callbacks:
            if newData or callback.force:
                callback.callback(self, callback.guiCallback)

    def getData(self) -> list[str]:
        self.dataChanged = False
        return self.arguments

    def getFullCommand(self) -> str:
        fullCommand = self.parent.getFullCommand()
        if fullCommand != "": fullCommand += "."
        return fullCommand + self.longCommand

class Module:
    def __init__(self, parent:ModuleGroup | ModuleHandler, commandSet, commandItem:Derivedcommanditem=None, itemCommandSet=None, helpModule:HelpModule = None):
        self.longName = ""
        self.shortName = ""
        self.moduleType = ""
        #self.indexingChild = None
        #self.index = 0
        self.parent:ModuleGroup | ModuleHandler = parent
        self.commands:dict[str, ModuleCommand] = {}
        self.commandSet = commandSet
        self.helpModule:HelpModule = helpModule
        self.nodes = []
        self.variablePorts = []

        #if (commandItem is not None):
        #    if (len(commandItem.hierarchy[commandItem.hierarchyIndex].selection) > 0):
        #        self.index = int(commandItem.hierarchy[commandItem.hierarchyIndex].selection[0])
        #else:
        #    pass
        if (itemCommandSet is not None):
            # commandItem: CommandSet = commandItem
            self.longName = itemCommandSet.longName
            self.shortName = itemCommandSet.shortName
            #if (itemCommandSet.indexingChild is not None):
                #self.indexingChild = itemCommandSet.indexingChild
        elif (commandItem is not None):
            self.longName = commandItem.argument[0].strip()
            self.shortName = commandItem.argument[1].strip()
            if hasattr(self, "moduleType"):
                self.moduleType = commandItem.argument[3].strip()
        elif (helpModule is not None):
            self.longName = helpModule.longName
            self.shortName = helpModule.shortName
        else:
            pass
        if not isinstance(self, ModuleGroup):
            self.addHelp()

    def getIndex(self) -> int:
        if isinstance(self.parent, ModuleGroup):
            for i in range(0, len(self.parent.children)):
                if (self.parent.children[i] is self):
                    return i
            return -1
        else:
            return 0

    def getFullCommand(self) -> str:
        if (self.parent is not None) and (self.parent is not self.commandSet):
            fullCommand = self.parent.getFullCommand()
            if (fullCommand != ""): fullCommand += "."
            return fullCommand + self.longName + "[" + str(self.getIndex()) + "]"
        else:
            return ""

    def setCommandData(self, command: str, data, force=False):
        if (not command in self.commands):
            # self.commands[command] = CommandSetModular.CommandData(command, data, force)
            pass
        elif (self.commands[command] != data):
            self.commands[command].setData(data)

    def getCommandData(self, command: str, resetDataChange=False):
        if (command in self.commands):
            return self.commands[command]
        else:
            return None

    def addCommandCallback(self, command:str, callback):
        if (command in self.commands):
            self.commands[command].addCallback(callback)
        else:
            pass

    def removeCallBack(self, command:str, callback):
        if (command in self.commands):
            self.commands[command].removeCallback(callback)
        else:
            pass

    def addHelp(self):
        if self.helpModule is None:
            if self.parent is self.commandSet:
                self.helpModule = self.commandSet.helpModule
            else:
                if isinstance(self.parent, ModuleHandler):
                    pass
                for help in self.parent.helpModule.modules:
                    if (self.longName == help.longName) or (self.shortName == help.shortName):
                        self.helpModule = help
                        break
            if self.helpModule is None:
                return
        for command in self.helpModule.commands:
            self.addCommandFromHelp(command)

    def addCommandFromHelp(self, helpCommand:HelpCommand):
        if helpCommand is None: return
        if not helpCommand.longCommand in self.commands:
            self.commands[helpCommand.longCommand] = ModuleCommand(helpCommand, None, self)

    def requestAllData(self, commands:list[ModuleCommand]) -> ModuleCommand:
        for command in self.commands.values():
            if (commandHasStorableDataCmd(command)):
                commands.append(command)

class ModuleGroup(Module):
    def __init__(self, parent:ModuleHandler, commandSet, commandItem:Derivedcommanditem=None, itemCommandSet=None, helpModule = None):
        self.children:list[ModuleHandler] = []
        super().__init__(parent, commandSet, commandItem, itemCommandSet, helpModule)
        self.empty = False
        self.dataChanged = True
        if (commandItem is not None) or (itemCommandSet is not None):
            pass
        else:
            self.helpCommand = HelpCommand(helpModule.longName, helpModule.shortName, 0, "", False, helpModule.description,"")
            self.selectedIndex:ModuleCommand = ModuleCommand(self.helpCommand, None, self, isIndex = True)
#            self.selectedIndex.oldSetData = self.selectedIndex.setData
#            self.selectedIndex.setData = self.selectedIndexSetData

#    def selectedIndexSetData(self, data:Any):
#        self.selectedIndex.oldSetData(data)
#        pass

    def addModuleHandler(self, commandItem:Derivedcommanditem = None) -> ModuleHandler:
        if len(self.children) != commandItem.hierarchy[commandItem.hierarchyIndex].selection[0]:
            return self.children[commandItem.hierarchy[commandItem.hierarchyIndex].selection[0]]
        child = ModuleHandler(self, self.commandSet, helpModule = self.helpModule)
        self.children.append(child)
        self.dataChanged = True
        return self.children[-1]

    def remove(self, index):
        self.dataChanged = True
        pass

    def requestAllData(self, commands:list[ModuleCommand]) -> ModuleCommand:
        commands.append(self.selectedIndex)
        for child in self.children:
            child.requestAllData(commands)

    def getFullCommand(self) -> str:
        if (self.parent is not None) and (self.parent is not self.commandSet):
            fullCommand = self.parent.getFullCommand()
            return fullCommand
        else:
            return ""

class ModuleHandler(Module):
    def __init__(self, parent, commandSet, commandItem:Derivedcommanditem = None, itemCommandSet = None, helpModule = None):
        super().__init__(parent, commandSet, commandItem, itemCommandSet, helpModule)
        #self.children = []
        self.groups:list[ModuleGroup] = []
        self.instances = 0
        self.isEmpty = False
        self.dataChanged = True

        #self.selectedIndex = -1
        self.callbacks:list[ModuleCommand.Callback] = []
        #self.fullCommand = self.getFullCommand()
    '''
    def setSelectedIndex(self, index):
        newData = False
        if (index != self.selectedIndex):
            self.selectedIndex = index
            self.dataChanged = True
            newData = True
        for callback in self.callbacks:
            if newData or callback.force:
                callback.callback(self, callback.data)

    def getSelectedIndex(self) -> int:
        self.dataChanged = False
        if self.selectedIndex != -1: return self.selectedIndex
        return 0
    '''
    def addCallback(self, callback, guiCallback=None, force=False):
        for callb in self.callbacks:
            if callb.callback == callback:
                return
        self.callbacks.append(ModuleCommand.Callback(callback, guiCallback, force))

    def removeCallback(self, callback):
        self.callbacks.remove(callback)

    def getHelpModule(self, commandItem:Derivedcommanditem) -> HelpModule:
        helpModule = None
        for helpModule in self.helpModule.modules:
            if (helpModule.longName == commandItem.hierarchy[commandItem.hierarchyIndex].name):
                break
        return helpModule

    def getModuleGroup(self, commandItem:Derivedcommanditem) -> ModuleGroup:
        helpModule = self.getHelpModule(commandItem)
        if helpModule is None:
            return None
        for group in self.groups:
            if (group.helpModule == helpModule):
                return group
        return None

    def addModuleGroup(self, commandItem:Derivedcommanditem) -> ModuleGroup:
        group = self.getModuleGroup(commandItem)
        if group is not None:
            return group
        helpModule = self.getHelpModule(commandItem)
        if helpModule is None:
            return
        group = ModuleGroup(self, self.commandSet, helpModule = helpModule)
        self.groups.append(group)
        return group

    def addModuleFromDirReturn(self, commandItem:Derivedcommanditem):
        # If this is the actual 'ls'-command convert it so that we get the hierarchy
        if commandItem.command == "ls":
            newCommandItem = Derivedcommanditem(commandItem.argument[0])
        else:
            newCommandItem = commandItem
        # Skip any entries denoting the selection function as it is implied
        if newCommandItem.command[len(newCommandItem.command) - len("[selection]"):] == "[selection]":
            return
        newCommandItem.argument = commandItem.argument
        moduleGroup = self.addModuleGroup(newCommandItem)
        # If this is the last index in the hierarchy and the 'ls'-command indicates zero children, do not add the actual child
        if (int(newCommandItem.argument[2]) == 0) and (newCommandItem.hierarchyIndex >= len(newCommandItem.hierarchy) - 1):
            moduleHandler = None
        else:
            moduleHandler = moduleGroup.addModuleHandler(newCommandItem)

        if (newCommandItem.hierarchyIndex < len(newCommandItem.hierarchy) - 1 and moduleHandler is not None):
            newCommandItem.hierarchyIndex += 1
            moduleHandler.addModuleFromDirReturn(newCommandItem)
            newCommandItem.hierarchyIndex -= 1

    def requestAllData(self, commands:list[ModuleCommand]) -> ModuleCommand:
        super().requestAllData(commands)
        for group in self.groups:
                group.requestAllData(commands)

    def setCommandData(self, commandItem: Derivedcommanditem) -> bool:
        command, module = self.getCommandAndModule(commandItem)
        if (command is None) or (module is None):
            return False
        if isinstance(module, ModuleGroup):
            data = []
            data.append(str(commandItem.hierarchy[len(commandItem.hierarchy) - 1].selection[0]))
        else:
            data = commandItem.argument
        command.setData(data)

        '''
        # If this is the last item in the hierarchy, it's either a command or a index selection
        if commandItem.hierarchyIndex == len(commandItem.hierarchy) - 1:
            # Check if it's a command
            for command in self.commands.values():
                if commandItem.hierarchy[commandItem.hierarchyIndex].name == command.longCommand or \
                    commandItem.hierarchy[commandItem.hierarchyIndex].name == command.shortCommand:

                    command.setData(commandItem.argument)
                    return True
            # If not, check if it's an index
            for group in self.groups:
                if commandItem.hierarchy[commandItem.hierarchyIndex].name == group.longName or \
                    commandItem.hierarchy[commandItem.hierarchyIndex].name == group.shortName:
                    data = []
                    data.append("[" + str(commandItem.hierarchy[commandItem.hierarchyIndex].selection[0]) + "]")
                    group.selectedIndex.setData(data)
                    return True
            # If neither, it's an error
            return False
        else:
            # If this is not the last item in the hierarchy, search for the right group and then get the selected child (if possible)
            index = commandItem.hierarchy[commandItem.hierarchyIndex].selection[0]
            for group in self.groups:
                if commandItem.hierarchy[commandItem.hierarchyIndex].name == group.longName or \
                    commandItem.hierarchy[commandItem.hierarchyIndex].name == group.shortName:
                    # If the selection is larger than the current amount of children, we have an error
                    if index > len(group.children) - 1:
                        return False
                    commandItem.hierarchyIndex += 1
                    response = group.children[index].setCommandData(commandItem)
                    commandItem.hierarchyIndex -= 1
                    return response
            return False
        '''

    def addModule(self, commandItem: Derivedcommanditem | str) -> ModuleHandler:
        if isinstance(commandItem, str):
            commandItem = Derivedcommanditem(commandItem)
        moduleGroup = self.getModuleGroup(commandItem)
        if (moduleGroup is None):
            return None
        if commandItem.command[len(commandItem.command) - len("[selection]"):] == "[selection]":
            return None

        if (commandItem.hierarchy[commandItem.hierarchyIndex].selection is None) or \
            (len(commandItem.hierarchy[commandItem.hierarchyIndex].selection) == 0):
            return None
        index = int(commandItem.hierarchy[commandItem.hierarchyIndex].selection[0])

        if (len(moduleGroup.children) > index):
            return moduleGroup.children[index]

        # If this is the last index in the hierarchy and the 'ls'-command indicates zero children, do not add the actual child
        return moduleGroup.addModuleHandler(commandItem)

    def removeModule(self, moduleName:Module, moduleIndex):
        for group in self.groups:
            for i in range(0,len(group.children)):
                if (group.children[i].longName == moduleName or group.children[i].shortName == moduleName) and i == int(moduleIndex):
                    group.children.remove(group.children[i])
                    return

    def getCommandAndModule(self, commandItem:Derivedcommanditem | str) -> (ModuleCommand, Module):
        if isinstance(commandItem, str):
            commandItem = Derivedcommanditem(commandItem)
        # If this is the last item in the hierarchy, it's either a command or a index selection
        if commandItem.hierarchyIndex == len(commandItem.hierarchy) - 1:
            # Check if it's a command
            for command in self.commands.values():
                if commandItem.hierarchy[commandItem.hierarchyIndex].name == command.longCommand or \
                    commandItem.hierarchy[commandItem.hierarchyIndex].name == command.shortCommand:

                    return command, self
            # If not, check if it's an index
            for group in self.groups:
                if commandItem.hierarchy[commandItem.hierarchyIndex].name == group.longName or \
                    commandItem.hierarchy[commandItem.hierarchyIndex].name == group.shortName:
                    return group.selectedIndex, group
            # If neither, it's an error
            return None, self
        else:
            # If this is not the last item in the hierarchy, search for the right group and then get the selected child (if possible)

            for group in self.groups:
                if commandItem.hierarchyIndex >= len(commandItem.hierarchy):
                    pass
                if commandItem.hierarchy[commandItem.hierarchyIndex].name == group.longName or \
                    commandItem.hierarchy[commandItem.hierarchyIndex].name == group.shortName:
                    # If the selection is larger than the current amount of children, we have an error

                    # If there's no selection, get the currently selected item from the object
                    if (commandItem.hierarchy is None):
                        pass
                    if len(commandItem.hierarchy[commandItem.hierarchyIndex].selection) == 0:
                        if (group.selectedIndex is None) or (group.selectedIndex.arguments is None) or len(group.selectedIndex.arguments) == 0:
                            index = 0
                        else:
                            index = int(group.selectedIndex.arguments[0])
                    else:
                        index = commandItem.hierarchy[commandItem.hierarchyIndex].selection[0]

                    if index > len(group.children) - 1:
                        return None, None
                    commandItem.hierarchyIndex += 1
                    responseC, responseM = group.children[index].getCommandAndModule(commandItem)
                    commandItem.hierarchyIndex -= 1
                    return responseC, responseM
            return None, None

    def getModule(self, commandItem:Derivedcommanditem | str) -> ModuleHandler:
        if isinstance(commandItem, str):
            commandItem = Derivedcommanditem(commandItem)
        if len(commandItem.hierarchy[commandItem.hierarchyIndex].selection) == 0:
            index = 0
        else:
            index = commandItem.hierarchy[commandItem.hierarchyIndex].selection[0]
        for group in self.groups:
            if commandItem.hierarchy[commandItem.hierarchyIndex].name == group.longName or \
                commandItem.hierarchy[commandItem.hierarchyIndex].name == group.shortName:
                # If the selection is larger than the current amount of children, we have an error
                if index > len(group.children) - 1:
                    return None
                if commandItem.hierarchyIndex == len(commandItem.hierarchy) - 1:
                    return group.children[index]
                else:
                    commandItem.hierarchyIndex += 1
                    module = group.children[index].getModule(commandItem)
                    commandItem.hierarchyIndex -= 1
                    return module
        return None

    '''
    def remove(self, item:Module):
        if (isinstance(item, int)):
            index = item
            item = self.children[index]
        else:
            index = self.children.index(item)
        self.children.remove(item)
        for i in range(index, len(self.children)):
            self.children[i].index -= 1
        self.dataChanged = True

    def getGroups(self, name:str) -> ModuleHandler:
        toReturn = []
        for child in self.children:
            if ((child.longName == name) or (child.shortName == name)):
                toReturn.append(child)
            else:
                subChildren = child.getGroups(name)
                for subChild in subChildren: toReturn.append(subChild)
        return toReturn

    def getGroupParsed(self, newItem:Derivedcommanditem, rootGroup=None, addGroups=False, isEmpty=False) -> ModuleHandler:
        try:
            groupName = newItem.hierarchy[newItem.hierarchyIndex].name
        except:
            # raise("Group not found")
            return None
        thisItem = 0
        for group in rootGroup:
            if ((str(group.longName) == str(groupName)) or (str(group.shortName) == str(groupName))):
                if (len(newItem.hierarchy) == 0 or (newItem.hierarchyIndex >= (len(newItem.hierarchy) - 1))):
                    if (len(newItem.hierarchy[newItem.hierarchyIndex].selection) == 0):
                        # if group.index == 0: return group
                        if group.index == group.parent.getSelectedIndex():
                            return group
                        else:
                            # selection not found is an error
                            pass
                    else:
                        if (int(newItem.hierarchy[newItem.hierarchyIndex].selection[0]) == group.index):
                            return group
                else:
                    newItem.hierarchyIndex += 1
                    if (newItem.hierarchyIndex >= len(newItem.hierarchy)):
                        break
                    else:
                        return group.getGroupParsed(newItem, group.children, addGroups, isEmpty)
        if (addGroups):
            child = self.addGroupFromHierarchy(newItem, isEmpty)
            if (len(rootGroup) != 0):
                group = rootGroup[-1]
                if (newItem.hierarchyIndex < (len(newItem.hierarchy))):
                    group.getGroupParsed(newItem, group.children, True)
                return child
            else:
                pass

    def getGroup(self, commandItem:Derivedcommanditem) -> ModuleHandler:
        return self.getGroupParsed(commandItem, self.children)

    def getCommandDataS(self, commandString: str):
        derivedItem = Derivedcommanditem(commandString)
        if derivedItem is None: return
        return self.getCommandData(derivedItem)

    def getCommandData(self, commandItem: Derivedcommanditem) -> Module | ModuleCommand:
        command, module = self.commandSet.getCommandAndModule(commandItem)
        if module is None: return None
        if command is None:
            command = commandItem.hierarchy[len(commandItem.hierarchy) - 1]
            for module2 in module.children:
                if (command.name == module2.longName or command.name == module2.shortName) and ("[index]" in module2.commands):
                    return module
            return None
        return command

    def getGroupAndAddIfNone(self, commandItem:Derivedcommanditem, isEmpty=False) -> ModuleHandler:
        return self.getGroupParsed(commandItem, self.children, True, isEmpty)

    def addGroup(self, commandItem:Derivedcommanditem, commandGroup, isEmpty=False) -> ModuleHandler:
        child = ModuleHandler(self, self.commandSet, commandItem, commandGroup)
        # child.parent = self
        # child.addHelp()
        child.isEmpty = isEmpty
        self.children.append(child)
        self.dataChanged = True
        return self.children[-1]

    def addGroupFromHierarchy(self, commandItem:Derivedcommanditem, isEmpty=False):
        commandGroup = None
        # Trying to get rid of all the pre-defined modules

        for item in self.commandSet.commands:
            if (item.longName == commandItem.hierarchy[commandItem.hierarchyIndex].name or
                    item.shortName == commandItem.hierarchy[commandItem.hierarchyIndex].name):
                commandGroup = item
                break
        if (self.helpModule is not None):
            helpModule = None
            for item in self.helpModule.modules:
                if (item.longName == commandItem.hierarchy[commandItem.hierarchyIndex].name or
                        item.shortName == commandItem.hierarchy[commandItem.hierarchyIndex].name):
                    helpModule = item
                    break
            if (helpModule is None):
                for item in self.helpModule.commands:
                    if (item.longCommand == commandItem.hierarchy[commandItem.hierarchyIndex].name or
                            item.shortCommand == commandItem.hierarchy[commandItem.hierarchyIndex].name):
                        self.addCommandFromHelp(item)
                        break
            else:
                pass

        if (commandGroup == None):
            pass
        else:
            self.addGroup(commandItem, commandGroup, isEmpty)
            self.dataChanged = True
            commandItem.hierarchyIndex += 1
        if (len(self.children) == 0):
            return None
        return self.children[-1]

    def addModule(self, commandItem: Derivedcommanditem, isEmpty=False) -> ModuleHandler:
        self.dataChanged = True
        return self.getGroupAndAddIfNone(commandItem, isEmpty)

    def removeModule(self, moduleName:Module, moduleIndex):
        for child in self.children:
            if child.longName == moduleName and child.index == int(moduleIndex):
                self.children.remove(child)
                return
    '''


class HelpCommand:
    def __init__(self, longCommand="", shortCommand="", type=0, arguments="", hidden=False,
                 description="", variables= []):
        if longCommand == "" or shortCommand == "":
            longCommand = "[index]"
            shortCommand = "[i]"
        self.longCommand: str = longCommand
        self.shortCommand: str = shortCommand
        self.arguments: str = arguments
        self.description: str = description
        self.hidden: bool = bool(int(hidden))
        # self.save:bool = False
        self.type = int(type)
        self.variables = variables
        self.commandTypeData:HelpCommand.CommandType_data = HelpCommand.CommandType_data(self.type & 0b1111)
        self.commandTypeDataOptions = HelpCommand.CommandType_dataOptions((self.type >> 4) & 0b1)
        self.commandTypeAccess = HelpCommand.CommandType_access((self.type >> 5) & 0b11)
        self.commandTypeFunction = HelpCommand.CommandType_function((self.type >> 7) & 0b1111)
        self.commandTypeSystem = bool(((self.type  >> 11) & HelpCommand.CommandType_flags.ectSystem.value))
        self.commandTypeLogic = bool(((self.type >> 11) & HelpCommand.CommandType_flags.ectLogic.value) > 1)
        self.commandTypeVolatile = bool(((self.type >> 11) & HelpCommand.CommandType_flags.ectVolatileSetting.value) > 2)
        pass

    class CommandType_data(IntEnum):
        ectNone = 0
        ectSimpleString = 1
        ectSimpleBool = 2
        ectSimpleFloat = 3
        ectSimpleUInt8 = 4
        ectSimpleInt16 = 5
        ectSimpleUInt16 = 6
        ectCommands = 7
        ectData = 8
        ectMilliseconds = 9
        ectMicroseconds = 10
        ectHertz = 11
        ectOutputAssignment = 12
        ectSimpleInt8 = 13
        ectConditional = 14

    class CommandType_dataOptions(IntEnum):
        ectStatic = 0
        ectExpression = 1

    class CommandType_access(IntEnum):
        ectSetRequest = 0
        ectRequest = 1
        ectSelfInvoked = 2
        ectInvokeOnly = 3

    class CommandType_function(IntEnum):
        ectUndefined = 0
        #ectParameter = 1
        ectCalibration = 1
        ectAddModule = 2
        ectRemoveModule = 3
        ectCountModules = 4
        ectName = 5
        ectIndex = 6
        ectAssignment = 7
        #ectInvokeAction = 8
        ectAdminAction = 8
        ectLiveParameter = 9
        ectLiveAction = 10
        ectAdminSetting = 11
        ectLiveStatistics = 12
        ectInternalStatistics = 13

    class CommandType_flags(IntEnum):
        ectNone = 0
        ectSystem = 1
        ectLogic = 2
        ectVolatileSetting = 4

class ModuleTypes(Enum):
    software = auto()
    hardware = auto()
    external = auto()

class HelpModule:
    def __init__(self, commandSet, hierarchyIndex=0, longName="", shortName="", description=""):
        self.longName: str = longName
        self.shortName: str = shortName
        self.description: str = description
        self.modules:list[HelpModule] = []
        self.commands:list[HelpCommand] = []
        self.commandSet = commandSet
        self.hierarchyIndex = hierarchyIndex

    def addEntry(self, commandItem: Derivedcommanditem):
        if commandItem.hierarchyIndex < (len(commandItem.hierarchy) - 1):
            for module in self.modules:
                if module.longName == commandItem.hierarchy[commandItem.hierarchyIndex].name:
                    commandItem.hierarchyIndex += 1
                    module.addEntry(commandItem)
                    commandItem.hierarchyIndex -= 1
                    return
        else:
            shortNameH = Derivedcommanditem(commandItem.argument[0])
            shortName = shortNameH.hierarchy[len(shortNameH.hierarchy) - 1].name
            if len(commandItem.argument) >= 5:
                variables = ""
                if len(commandItem.argument) >= 6:
                    #variables = commandItem.argument[5]
                    variables = commandItem.argument[5].split(",")
                self.commands.append(HelpCommand(commandItem.hierarchy[commandItem.hierarchyIndex].name,
                                                 shortName, commandItem.argument[1],
                                                 commandItem.argument[2], commandItem.argument[3], commandItem.argument[4], variables))
            if len(commandItem.argument) == 2:
                self.modules.append(HelpModule(self.commandSet, self.hierarchyIndex + 1,
                                               commandItem.hierarchy[commandItem.hierarchyIndex].name,
                                               shortName, commandItem.argument[1]))
