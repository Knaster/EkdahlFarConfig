from GraphNode.customnode import CustomBaseNode, CustomNodeItem
from CommandSets import CommandSetModular, ModuleCommand
from commanddefinitions import ModuleCommandType_data, ModuleCommandType_access, ModuleCommandType_function, ModuleCommandType_dataOptions, parseModuleCommandType, \
    ModuleCommandType_data, ModuleCommandType_access, ModuleCommandType_function, ModuleCommandType_dataOptions, CommandID
from GraphNode.nodetemplates.custom_ports_node import draw_triangle_port


import GraphNode.graphassemblies as graphassemblies
from PySide6 import QtGui

## The dynamicNodeSet class creates a set of \a assemblies and \a nodes from the given \ref "farconfig.CommandSets.CommandSetModular.GroupHandler" "CommandSetModular.GroupHandler"
# Each \a module will have its own \a assembly, the \a modules \a commands may all be contained in a single \a node or split into several \a nodes depending
# on their attributes. This \a class does not create any connections in between the different \a nodes

class dynamicNodeSet:
    def __init__(self, ga:graphassemblies.graphAssemblies, commandSet:CommandSetModular = None):
        ## Current \ref graphassemblies.graphAssembly
        self.ga = ga
        ## Associated \ref "farconfig.CommandSets.CommandSetModular" "CommandSets.CommandSetModular"
        self.commandSet = commandSet    #:CommandSetModular
        ## Associated modules
        self.modules = []
        #self.y = -1000

        ## Starting points of sources, modifiers and destination nodes
        self.posList = [[-500, -1000], [0, -1000], [750, -1000]]
        ## Increase in Y position per added item
        self.addY = 300

    def addNodeDataFromModuleCommand(self, newNode:CustomBaseNode, commandID:CommandID, command:ModuleCommand) -> CustomBaseNode:
        lastCmd = str(command.shortCommand).rfind(".")
        if (lastCmd != -1): comstr = command.longCommand[command.longCommand.rfind(".") + 1:]
        else: comstr = command.longCommand

        data, options, access, func = parseModuleCommandType(int(command.commandType))
        if ((func == ModuleCommandType_function.Parameter) or (func == ModuleCommandType_function.Assignment)) and (access == ModuleCommandType_access.Normal):
            match (data):
                case ModuleCommandType_data.OutputAssignment:
                    isSource = True
                    newNode.add_output(comstr, commandID, valueType="_trigger")
                    newNode.command.append(commandID)

                case ModuleCommandType_data.Hertz | ModuleCommandType_data.Microseconds | ModuleCommandType_data.Milliseconds | \
                     ModuleCommandType_data.SimpleUInt16 | ModuleCommandType_data.SimpleUInt8 | ModuleCommandType_data.SimpleFloat | ModuleCommandType_data.SimpleInt16 | \
                     ModuleCommandType_data.SimpleInt8:
                    newNode.add_input(comstr, commandID, valueType="number")
                    newNode.command.append(commandID)

                case ModuleCommandType_data.Immediate | ModuleCommandType_data.Conditional | ModuleCommandType_data.SimpleBool:
                    newNode.add_input(comstr, commandID, valueType="_trigger")
                    newNode.command.append(commandID)

        elif (func == ModuleCommandType_function.Name):
            newNode.nameCommand = commandID

        if (command.variables is not None):
            for variable in command.variables:
                newNode.add_output(variable, CommandID, variable="number", painter_func= draw_triangle_port)
            #if (len(command.variables) > 0) and (comstr != "target"):
            #    newNode.add_output("_trig", CommandID, variable="trig")

        return newNode

    def treatSpecialModule(self, inModule, newNode) -> CustomBaseNode:
        match(inModule.longName):
            case "multiple":
                newNode.add_input("Input ratio", "multiple[" + str(inModule.index) + "].data:ratio:", variable="inputratio")
                newNode.add_input("Input adder", "multiple[" + str(inModule.index) + "].data:adder:", variable="inputadder")
        return newNode

    def treatSpecialCommand(self, inModule, inCommand:CommandID, newNode:CustomBaseNode) -> CustomBaseNode:
        match(inModule.longName):
            case "midiconfiguration":
                match(inCommand):
                    case CommandID.midiConfigurationContinuousController:
                        #newNode.NODE_NAME += " " + str(inModule.)
                        pass

    ## Processes the \ref "farconfig.CommandSets.CommandSetModular.GroupHandler" "CommandSetModular.GroupHandler" object given and does the following;
    # * Loop through each \a command of the \a module and
    #   * Check if the \a command has an \a output \a assignment, if so set the local \a source variable to \a true
    #   * For each \a variable associated with the \a command, increase the local \a separate variable
    # * Check if the \a modules parent object name is \a 'pluginhandler', if so, set the local variable \a isPlugin to \a true
    # * Create a empty \ref "customnode.CustomBaseNode" "CustomBaseNode" for the \a module
    # * See if the \a node type requires any special treatment through the use of \ref "farconfig.dynamicnodes.dynamicNodeSet.treatSpecialModule" "treatSpecialModule"
    # * Create a \ref graphassemblies.graphAssembly for the \a module
    # * Loop through each \a command of the \a module again and
    #   * Set the various \a node data, color is dependent on whether it's a \a source, \a plugin, \a modifier or \a destination
    #   * process \a command through \ref "farconfig.dynamicnodes.dynamincNodeSet.addNodeDataFromModuleCommand" "addNodeDataFromModuleCommand". \n
    #     Depending on the command properties this adds upp two \a inputs or \a outputs in any configuration. See function for more information
    #   * Checks whether to separate this \a command into a separate \a node in the same \a assembly. \n
    #     If the total number of \a inputs + \a outputs > 0 AND the \a module has more than one \a variable associated with it it should be separated. \n
    #     Insert the current \a node into the \a assembly and create a new \a node for the next \a command
    # * Recursively repeat the entire process for all child \a modules
    def buildNodesFromModules(self, inModule:CommandSetModular.GroupHandler):
        if (inModule.shortName == "cc"):
            pass

        name = ""
        separate = 0
        isSource = False
        for commandd in inModule.commands:
            command: ModuleCommand = inModule.commands[commandd]
            data, options, access, func = parseModuleCommandType(int(command.commandType))
            if (data == ModuleCommandType_data.OutputAssignment): isSource = True
            if (command.variables is not None):
                if len(command.variables) > 0: separate += 1

        isPlugin = False
        if (inModule.parent is not None):
            if (inModule.parent.longName == "pluginhandler"):
                isPlugin = True

        prefixLong = inModule.longName + "[" + str(inModule.index) + "]"
        prefixShort = inModule.shortName + "[" + str(inModule.index) + "]"

        if (separate > 1): separate = True
        else: separate = False

        newNode = CustomBaseNode()
        newNode.command = []

        newNode = self.treatSpecialModule(inModule, newNode)

        assembly = graphassemblies.graphAssembly(self.ga.graph, prefixLong, 0, inModule.index, self.commandSet.getModuleHierarchy(inModule))
        assembly = self.ga.insertAssembly(assembly)
        #assembly.moduleIndex = inModule.index
        #assembly.hierarchy = self.commandSet.getModuleHierarchy(inModule)

        if (isSource and not isPlugin):
            poslistI = 0
            color = QtGui.QColor(126, 148, 246)
        elif (isPlugin):
            poslistI = 1
            color = QtGui.QColor(126, 148, 146)
        else:
            poslistI = 2
            color = QtGui.QColor(226, 148, 146)

        for commandd in inModule.commands:
            newNode.source = isSource
            newNode.view.widgetBackground = color
            newNode.NODE_NAME = prefixLong
            newNode.NODE_NAME_SHORT = prefixShort
            newNode.moduleIndex = inModule.index
            newNode.hierarchy = self.commandSet.getModuleHierarchy(inModule)
            newNode.module = inModule

            #self.treatSpecialCommand(inModule, commandd, newNode)
            self.addNodeDataFromModuleCommand(newNode, commandd, inModule.commands[commandd])

            if (len(newNode.inputs()) + len(newNode.outputs()) > 0) and (separate):
                lastCmd = str(inModule.commands[commandd].longCommand).rfind(".")
                if (lastCmd != -1): comstr = inModule.commands[commandd].longCommand[inModule.commands[commandd].longCommand.rfind(".") + 1:]
                else: comstr = inModule.commands[commandd].longCommand
                newNode.NODE_NAME += "\n\r- " + comstr
                assembly.insertNode(newNode, self.posList[poslistI])
                #self.ga.insertAssembly(assembly)
                newNode = CustomBaseNode()
                newNode.command = []
                self.posList[poslistI][1] += self.addY

        if (len(newNode.inputs()) + len(newNode.outputs()) > 0) and not (separate):
            assembly.insertNode(newNode, self.posList[poslistI])
            self.posList[poslistI][1] += self.addY

        for child in inModule.children:
            self.buildNodesFromModules(child)
