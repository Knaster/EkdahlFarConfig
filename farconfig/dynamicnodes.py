from GraphNode.customnode import CustomBaseNode
from CommandSets import CommandSetModular #, ModuleCommand
#from commanddefinitions import ModuleCommandType_data, ModuleCommandType_access, ModuleCommandType_function, ModuleCommandType_dataOptions, parseModuleCommandType, \
#    ModuleCommandType_data, ModuleCommandType_access, ModuleCommandType_function, ModuleCommandType_dataOptions
from deprecated.commanddefinitions import CommandID
from GraphNode.nodetemplates.custom_ports_node import draw_triangle_port

from ModuleSystem import ModuleHandler, ModuleCommand, HelpCommand, Module

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

    # This function will add an input or output port to newNode if the given moduleCommand requires it
#    def addNodeDataFromModuleCommand(self, newNode:CustomBaseNode, commandID:CommandID, command:ModuleCommand) -> CustomBaseNode:
    def addNodeDataFromModuleCommand(self, newNode: CustomBaseNode, moduleCommand: ModuleCommand) -> CustomBaseNode:
        #lastCmd = str(moduleCommand.shortCommand).rfind(".")
        #if (lastCmd != -1): comstr = moduleCommand.longCommand[moduleCommand.longCommand.rfind(".") + 1:]
        #else: comstr = moduleCommand.longCommand
        comstr = moduleCommand.longCommand

        #data, options, access, func = parseModuleCommandType(int(command.commandType))
        help = moduleCommand.helpCommand
        data = moduleCommand.helpCommand.commandTypeData
        eCMF = HelpCommand.CommandType_function
        eCMD = HelpCommand.CommandType_data
        #if ((func == ModuleCommandType_function.Parameter) or (func == ModuleCommandType_function.Assignment)) and (access == ModuleCommandType_access.Normal):
        port = None
        if ((help.commandTypeFunction == eCMF.ectLiveAction) or (help.commandTypeFunction == eCMF.ectLiveParameter) or
                (help.commandTypeFunction == eCMF.ectAssignment)) and (help.commandTypeAccess == HelpCommand.CommandType_access.ectSetRequest):
            match (data):
                #case ModuleCommandType_data.OutputAssignment:
                case eCMD.ectOutputAssignment:
                    isSource = True
                    port = newNode.add_output(comstr, moduleCommand, valueType="_trigger")
                    newNode.command.append(moduleCommand)

                #case ModuleCommandType_data.Hertz | ModuleCommandType_data.Microseconds | ModuleCommandType_data.Milliseconds | \
                #     ModuleCommandType_data.SimpleUInt16 | ModuleCommandType_data.SimpleUInt8 | ModuleCommandType_data.SimpleFloat | ModuleCommandType_data.SimpleInt16 | \
                #     ModuleCommandType_data.SimpleInt8:
                case eCMD.ectHertz | eCMD.ectMicroseconds | eCMD.ectMilliseconds | eCMD.ectSimpleUInt16 | eCMD.ectSimpleUInt8 | eCMD.ectSimpleFloat | \
                    eCMD.ectSimpleInt16 | eCMD.ectSimpleInt8:
                    port = newNode.add_input(comstr, moduleCommand, valueType="number")
                    newNode.command.append(moduleCommand)

#                case ModuleCommandType_data.Immediate | ModuleCommandType_data.Conditional | ModuleCommandType_data.SimpleBool:
                case eCMD.ectConditional | eCMD.ectSimpleBool:
                    port = newNode.add_input(comstr, moduleCommand, valueType="_trigger")
                    newNode.command.append(moduleCommand)

        #elif (func == ModuleCommandType_function.Name):
        elif (help.commandTypeFunction == eCMF.ectName):
            newNode.nameCommand = moduleCommand

        if port is not None:
            moduleCommand.nodePort = port

        if (moduleCommand.helpCommand.variables is not None):
            for variable in moduleCommand.helpCommand.variables:
                port = newNode.add_output(variable, moduleCommand, variable="number", painter_func= draw_triangle_port)
                if (port not in moduleCommand.parent.variablePorts):
                    moduleCommand.parent.variablePorts.append(port)
            #if (len(command.variables) > 0) and (comstr != "target"):
            #    newNode.add_output("_trig", CommandID, variable="trig")

        return newNode

    def treatSpecialModule(self, inModule:ModuleHandler | Module, newNode) -> CustomBaseNode:
        match(inModule.longName):
            case "multiple":
                newNode.add_input("Input ratio", "multiple[" + str(inModule.getIndex()) + "].data:ratio:", variable="inputratio")
                newNode.add_input("Input adder", "multiple[" + str(inModule.getIndex()) + "].data:adder:", variable="inputadder")
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
    def buildNodesFromModules(self, inModule:ModuleHandler):
        separate = 0
        isSource = False

        newNode = CustomBaseNode()
        newNode.command = []
        newNode.module = inModule

        # Check if node has assignment commands as it makes it a source
        # Also see if this module has a name command, if so set the module name using that and also add a callback to that ModuleCommand
        # so that if it changes the node handler will dynamically follow
        nameCommand = None
        for command in inModule.commands.values():
            if (command.helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectAssignment) or \
               (command.helpCommand.commandTypeData == HelpCommand.CommandType_data.ectOutputAssignment)  :
                isSource = True

            # If the module has variables, add a separation to the stack
            if (command.helpCommand.variables is not None):
                if len(command.helpCommand.variables) > 0: separate += 1

            # Check if the current command is a name function, add callback if so
            if (command.helpCommand.commandTypeFunction == HelpCommand.CommandType_function.ectName):
                newNode.nameCommand = command
                nameCommand = command
                command.addCallback(newNode.nameCallback, None)

        # Check if the module has a parent that is the pluginhandler, if so it's not a source, it's a plugin
        isPlugin = False
        if (inModule.parent is not None) and hasattr(inModule.parent, "parent") and (inModule.parent.parent is not None):
            if (hasattr(inModule.parent.parent, "longName")) and (inModule.parent.parent.longName == "pluginhandler"):
                isPlugin = True

        if (separate > 1): separate = True
        else: separate = False

        # Check if this module needs any special treatment
        newNode = self.treatSpecialModule(inModule, newNode)

        # Create a GraphAssembly around this node and insert it into the main GraphAssembly
        # A single assembly can contain one or more nodes depending on whether the various commands are to be separated into different nodes or not
        assembly = graphassemblies.graphAssembly(self.ga.graph, newNode.NODE_NAME, 0,
                                                 inModule.getIndex(), self.commandSet.getModuleHierarchy(inModule))
        assembly.module = inModule
        assembly = self.ga.insertAssembly(assembly)
        #assembly.moduleIndex = inModule.index
        #assembly.hierarchy = self.commandSet.getModuleHierarchy(inModule)

        if (isSource and not isPlugin):
            poslistI = 0
            #color = QtGui.QColor(126, 148, 246)
        elif (isPlugin):
            poslistI = 1
            #color = QtGui.QColor(126, 148, 146)
        else:
            poslistI = 2
                #color = QtGui.QColor(226, 148, 146)

        # Loop through each command of the module
        # if we're to separate the various commands into separate nodes, do that.
        # If not, we add all the inputs and outputs to the first node created per the commands it has
        for command in inModule.commands.values():
            # We set all this data in every loop because of separation
            newNode.source = isSource
            newNode.plugin = isPlugin
            #newNode.view.widgetBackground = color
            newNode.module = inModule
            newNode.nameCallback()
            newNode.moduleIndex = inModule.getIndex()
            newNode.hierarchy = self.commandSet.getModuleHierarchy(inModule)

            #self.treatSpecialCommand(inModule, commandd, newNode)

            #See if the current command adds as a input or output depending on the function & data type
            self.addNodeDataFromModuleCommand(newNode, command) #, inModule.commands[commandd])

            # If we have inputs & outputs, and we are supposed to separate these into different nodes, get at it.
            # Afterwards, create a new newNode
            if (len(newNode.inputs()) + len(newNode.outputs()) > 0) and (separate):
                newNode.nameSuffix = command.longCommand
                newNode.nameCallback()
                assembly.insertNode(newNode, self.posList[poslistI])
                inModule.nodes.append(newNode)
                #self.ga.insertAssembly(assembly)
                newNode = CustomBaseNode()
                newNode.command = []
                newNode.module = inModule
                if (nameCommand is not None):
                    newNode.nameCommand = nameCommand
                    nameCommand.addCallback(newNode.nameCallback, None)
                self.posList[poslistI][1] += self.addY

        # If we have inputs & outputs and we are NOT separating things, the current node should have been the same as from the beginning
        # Add it to the list
        if (len(newNode.inputs()) + len(newNode.outputs()) > 0) and not (separate):
            inModule.nodes.append(newNode)
            assembly.insertNode(newNode, self.posList[poslistI])
            self.posList[poslistI][1] += self.addY

        for group in inModule.groups:
            for child in group.children:
                self.buildNodesFromModules(child)
