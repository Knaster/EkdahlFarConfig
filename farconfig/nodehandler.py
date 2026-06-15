import re
import sys
import NodeGraphQt
from sympy.physics.quantum.qasm import stripquotes

from GraphNode.customnode import CustomBaseNode
import GraphNode.graphassemblies as graphassemblies
from NodeGraphQt.base import port
import sympy as sp
import dynamicnodes
from commanddefinitions import CommandID
from commandparser import derivedCommandItem
from general_helpers import stripLeadingQuotes

## The NodeHandler class creates a \a node diagram of the current set of \a modules by using the
# \ref "farconfig.nodehandler.NodeHandler.addDynamicNodeSet" "addDynamicNodeSet" function which is merely a caller for the
# \ref "farconfig.dynamicnodes.dynamicNodeSet" "dynamicNodeSet" class.
# Connections in between the various \a nodes are created by the \ref "farconfig.nodehandler.NodeHandler.parseCommand" "parseCommand" function by parsing
# \a command \a responses received, it also adds the \a glue \a logic \a nodes in between \a nodes in order to simplify the visual aspects of equations and
# functions used.\n\n
# \a Glue \a logic \a nodes are then optimized & combined through the use of the \ref "farconfig.nodehandler.NodeHandler.postBuildUpdate" "postBuildUpdate" function
# which also uses the \ref "nodeorganizer.NodeOrganizer" "NodeOrganizer" class to visually organize the \a nodes.

class NodeHandler:
    def __init__(self, container, commandSet = None):
        self.container = container
        self.ga = graphassemblies.graphAssemblies(container)
        self.commandSet = commandSet
        self.ga.addVariablesAssembly(-1000,-1000)
        self.ga.update()

        self.xSpread = 100
        self.xOffset = 1200

        self.maxDepth = 0

        self.hideImplicits = True
        self.hideAdvanced = True
        self.dynamicNodeSet = dynamicnodes.dynamicNodeSet(self.ga)

        self.iterationLevel = 0
        self.nodesAdded = []

    def clearNodes(self):
        self.ga.graph.clear_session()
        for assembly in self.ga.assemblies:
            assembly.nodes = None
        self.ga.assemblies.clear()
        self.iterationLevel = 0
        self.nodesAdded.clear()
        self.maxDepth = 0
        self.ga.graph.nodeOrganizer.clearData()
        self.ga.addVariablesAssembly(-1000,-1000)

    ## Add a node set dynamically from the given module information using the \ref "farconfig.dynamicnodes.dynamicNodeSet" "dynamicNodeSet" class
    def addDynamicNodeSet(self, inModule):
        self.dynamicNodeSet.commandSet = self.commandSet
        self.ga.commandSet = self.commandSet
        self.dynamicNodeSet.buildNodesFromModules(inModule)

    ## Adds text from a 'name' command to the nodes label
    def appendNameToNode(self, node : CustomBaseNode, command : derivedCommandItem):
        bracketIndex = node.NODE_NAME.find("]")
        name = node.NODE_NAME[:bracketIndex + 1]
        if (len(command.argument) == 0):
            return
        name += " - " + command.argument[0]
        if (bracketIndex + 1 < len(node.NODE_NAME)):
            name += " - " + node.NODE_NAME[bracketIndex + 1:]
        print("Setting node " + node.NODE_NAME + "'s name to " + name)
        node._view.name = name
        node.updateNames()

    def findCommandMatchAndProcess(self, command):
        if (self.commandSet is None):
            return False
        #try:
        commandID = self.commandSet.getCommandID(command)
        #print("command id: " + str(commandID))
        #if (commandID == commandID.pluginAHDSRName):
        #    pass
        #moduleIndex = self.commandSet.get
        if commandID == None:
            return False
        result = False
        for assembly in self.ga.assemblies:
            for node in assembly.nodes:
                node:CustomBaseNode = node
                if (commandID in node.command):
                    allFound = True

                    if (len(command.hierarchy) > 2):
                        commandParentIndex = command.hierarchy[len(command.hierarchy) - 2].selection[0]
                        if (commandParentIndex != node.moduleIndex):
                            allFound = False

                    if (allFound):
                        if (node.argumentMatch is not None):
                            for i in range(0, len(node.argumentMatch)):
                                if command.argument[i] != node.argumentMatch[i]: allFound = False
                        else:
                            pass

                    if (allFound):
#                       cl = self.commandSet.CommandList(stripLeadingQuotes(command.argument[len(node.argumentMatch) - 2:][0]))
                        if (node.argumentMatch is not None):
                            cl = self.commandSet.CommandList(stripLeadingQuotes(command.argument[len(node.argumentMatch):][0]))
                        else:
                            if (len(command.argument) > 0):
                                cl = self.commandSet.CommandList(stripLeadingQuotes(command.argument[0]))
                            else:
                                cl = self.commandSet.CommandList()
                                pass
                        if commandID == CommandID.midiConfigurationData:
                            pass
                        for comm in cl.commands:
                            if (len(comm.argument) == 0):
                                pass
                            connectFrom = None
                            for port in (node.input_ports() + node.output_ports()):
                                if (port.command == commandID):
                                    connectFrom = port
                                    break
                            result = True
                            self.process(node, comm.command, comm.argument, self.processOutput(False, connectFrom))
                            #return True
                elif commandID == node.nameCommand:
                    commandParentIndex = command.hierarchy[len(command.hierarchy) - 2].selection[0]
                    if (commandParentIndex == node.moduleIndex):
                        self.appendNameToNode(node, command)
                else:
                    pass
        return result

    def parseCommand(self, command):
        return self.findCommandMatchAndProcess(command)

    def postBuildUpdate(self):
        self.optimizeObjects()
        for node in self.ga.graph.all_nodes():
            if ("modifier" in node.type_):
                node.updateNames()
        self.ga.graph.nodeOrganizer.buildHorizontalTree()

    def redraw(self):
        for node in self.ga.graph.all_nodes():
            node.view.draw_node()
            node.view.update()

    localNumbers = []
    localSymbols = []
    localFunctions = []

    def getChildren(self, equation, rootOnly = True):
        self.localNumbers.clear()
        self.localSymbols.clear()
        self.localFunctions.clear()
        self.getChildrenIter(equation, rootOnly)

    def getChildrenIter(self, equation, rootOnly):
        if (equation.is_Number): self.localNumbers.append(str(equation))
        elif (equation.is_Symbol): self.localSymbols.append(str(equation))
        elif (equation.is_Function): self.localFunctions.append(str(equation.func))

        if ((not equation.is_Function) or (equation.is_Function and (not rootOnly))):
            for argument in equation.args:
                if ((not argument.is_Function) or (argument.is_Function and (not rootOnly))):
                    self.getChildrenIter(argument, rootOnly)
                elif (argument.is_Function):    #We're not to go in and parse individual functions if rootOnly, but we still have to add it to the total
                    self.localFunctions.append(argument.func)

    class processOutput:
        default = True
        port = None

        def __init__(self, inDefault = True, inPort = None):
            self.default = inDefault
            self.port = inPort
            pass

    def addFunction(self, function, mainNode):
        match (str(function).lower()):
            case "ibool":
                functionNode = self.ga.addModifierBool(self.xOffset - self.iterationLevel * self.xSpread, mainNode.y_pos())
                functionNode.set_value(True)
                # inPort = functionNode.get_input("in")
            case "bool":
                functionNode = self.ga.addModifierBool(self.xOffset - self.iterationLevel * self.xSpread, mainNode.y_pos())
                functionNode.set_value(False)
                # inPort = functionNode.get_input("in")
            case "deadband":
                functionNode = self.ga.addModifierDeadband(self.xOffset - self.iterationLevel * self.xSpread, mainNode.y_pos())
            case "map":
                functionNode = self.ga.addModifierMap(self.xOffset - self.iterationLevel * self.xSpread, mainNode.y_pos())
            case "mod" | "sin" | "cos":
                functionNode = self.ga.addModifierEquation2(self.xOffset - self.iterationLevel * self.xSpread, mainNode.y_pos())
            case _:
                return None
        functionNode.command = mainNode.command # mainNode.command
        self.nodesAdded.append(functionNode)
        return functionNode

    def getFunctionArguments(self, equation):
        if ("(" in equation):
            index1 = equation.index(")")
            index2 = equation.index("(") + 1
            equation = equation[index2:index1]
        arguments = []
        while ("," in equation):
            separationIndex = equation.index(",")
            arguments.append(equation[:separationIndex].strip())
            equation = equation[separationIndex + 1:].strip()

        arguments.append(equation.strip())
        return arguments

    def getPreferredConnection(self, inputs, output):
        # we can do this with a rating system later instead
        for input in inputs:
            if (input.port.valueType == output.valueType):
                return input.port, output
        print("None preferred, passing the first")
        return inputs[0].port, output

    def connectFunctionArguments(self, function, equation, mainNode, defaultOutput, startFromInput, inputNode, overrideInPort = None):
        eqSy = sp.sympify(equation)
        functionString = ""
        if (eqSy.is_Function):
            functionString = str(eqSy)
        else:
            for argument in eqSy.args:
                if (str(function) in (str(argument))):
                    functionString = str(argument)
        if (functionString == ""):
            pass
        arguments = self.getFunctionArguments(functionString)

        functionNode = self.addFunction(str(function), mainNode)

        functionPortNo = 0
        for argument in arguments:
            self.process(mainNode, "", [argument], defaultOutput, False, functionNode.get_input(functionPortNo))
            functionPortNo += 1

        inputNumber = startFromInput
        portName = "in" + str(inputNumber)
        equation = equation.replace(" ", "")
        functionString = functionString.replace(" ", "")
        equation = equation.replace(functionString, portName)
        if (overrideInPort is not None):
            inPort = overrideInPort
        else:
            inPort = inputNode.get_input(portName) #equationNode.get_input(portName)
        outPort = functionNode.get_output("out")
        outPort.connect_to(inPort)
        inputNumber += 1

        trigger = functionNode.get_input("_trigger")
        if (trigger is not None):
            if (len(trigger.connected_ports()) == 0):
                trigger.connect_to(defaultOutput.port)
                pass

        return equation

    def findInputPortFromCommand(self, inCommand, arguments = None):
        if (arguments is None): arguments = []
        command, module, index = self.commandSet.getCommandModuleAndCommand(inCommand)
        command = self.commandSet.getCommandID(command, module)
        module = module + "[" + str(index) + "]"
        for assembly in self.ga.assemblies:
            for node in assembly.nodes:
                node:CustomBaseNode = node
                if ((node.NODE_NAME == module) or (node.NODE_NAME_SHORT == module)):
                    match(node.hierarchy[len(node.hierarchy) - 1][0]):  #[0]
                        case "multiple":
                            match(arguments[0]):
                                case "ratio":
                                    return node.inputs()["Input ratio"], [arguments[2]]
                                case "adder":
                                    return node.inputs()["Input adder"], [arguments[2]]
                        case _:
                            for port in node.input_ports():
                                if (port.command == command):
                                    return port, arguments
        return [], []

    def createEquation(self, mainNode, equation, connectToInput, connectToOutput):
        createInputs = len(self.localFunctions) + len(self.localSymbols)
        # noAdd = False
        equationNode = self.ga.addModifierEquation(createInputs, self.xOffset - self.iterationLevel * self.xSpread, mainNode.y_pos())

        # if (not noAdd):
        equationNode.command = mainNode.command
        self.nodesAdded.append(equationNode)

        inputNumber = 0
        for symbol in self.localSymbols:
            portName = "in" + str(inputNumber)
            inPort = equationNode.get_input(portName)
            outPort = self.ga.findLocalOrVariableOutput(mainNode, str(symbol))
            outPort.connect_to(inPort)
            inputNumber += 1

        for function in self.localFunctions:
            equation = self.connectFunctionArguments(function, equation, mainNode, connectToOutput[0], inputNumber, equationNode)

        equationNode.set_value(equation)
        outPort = equationNode.get_output("out")
        outPort.connect_to(connectToInput)
        return equationNode

    class skipFunction:
        def __init__(self, inName:str, inAlt:str, inUseBrackets:bool):
            self.name:str = inName
            self.alt:str = inAlt
            self.useBrackets:bool = inUseBrackets

    skipFunctions = [skipFunction('mod', '%', True),
                     skipFunction('sin', '', False),
                     skipFunction('cos', '', False),
                     skipFunction('tan', '', False)]

    #Override simple built-in functions
    def overrideFunction(self, overrideWith:skipFunction, mainNode, equation, connectToInput, connectToOutput):
        if overrideWith.alt != "":
            findAndReplace = overrideWith.alt
        else:
            findAndReplace = overrideWith.name

        #replace function with '+' in order to trick sympy into thinking it's a straight equation
        equation = equation.replace(findAndReplace, "+")
        self.getChildren(sp.sympify(equation), False)

        equationNode = self.createEquation(mainNode, equation, connectToInput, connectToOutput)
        #restore the original dingdong
        equation = equation.replace("(", "")
        if overrideWith.useBrackets:
            equation = equation.replace("+", findAndReplace + "(")
        else:
            equation = equation.replace("+", findAndReplace)
            equation = equation.replace(")", "")
        equationNode.set_value(equation)

    def process(self, mainNode:CustomBaseNode, command, argument = None, inConnectToOutput = None, skipInput = False, inConnectToInput = None):
        self.iterationLevel += 1
        if (argument is None): argument = []
#        if (inConnectToOutput is None): inConnectToOutput = []
        if (inConnectToInput is None): inConnectToInput = []
        connectToOutput = []
        connectToInput = inConnectToInput

#        if ((":" in equation) and (not skipInput)):
            #inputCommand = equation[:equation.index(":")]
        inputCommand = command
        if (command != ""):
            try:
                connectToInput, argument = self.findInputPortFromCommand(inputCommand, argument)
            except:
                pass
        else:
            pass
            #connectToInput = self.ga.findInputPortFromCommand(inputCommand)
            #equation = equation[equation.index(":") + 1:]
        if (len(argument) > 0):
            equation = str(argument[0])
            equation = equation.replace(" ", "")
            self.getChildren(sp.sympify(equation), False)
        else:
            return
            #equation = ""
            #self.localNumbers.clear()
            #self.localSymbols.clear()
            #self.localFunctions.clear()

        if (inConnectToOutput is None):
            defaultPort = mainNode.get_output("_trigger")
            if (defaultPort is None):
                print("Error, no default port")
                return
            connectToOutput.append(self.processOutput(True, defaultPort))
        else:
            connectToOutput.append(inConnectToOutput)

        if (len(self.localSymbols) > 0):
            self.getChildren(sp.sympify(equation), True)
            for symbol in self.localSymbols:
                port = self.ga.findLocalOrVariableOutput(mainNode, symbol)
                if (port is None):
                    print("Port is none in function process")
                    return
                if ((port.model.node is mainNode) and (connectToOutput[0].default)):
                    connectToOutput[0].port = port
                    connectToOutput[0].default = False
                else:
                    connectToOutput.append(self.processOutput(False, port))

        if ((connectToInput is None) and (not skipInput)):
            return

        self.getChildren(sp.sympify(equation), True)
        if (len(self.localNumbers) + len(self.localFunctions) + len(self.localSymbols) > 1):
            self.createEquation(mainNode, equation, connectToInput, connectToOutput)

        elif (len(self.localSymbols) == 1):
            if (skipInput):
                return connectToOutput
            else:
                if (len(connectToOutput) > 1):
                    input, output = self.getPreferredConnection(connectToOutput, connectToInput)
                    input.connect_to(output)
                    #If not of same node we need trig too
                    if (input.model.node is not mainNode):
                        mainTrig = mainNode.get_output("_trigger")
                        funcTrig = output.model.node.get_input("_trigger")
                        if ((mainTrig and funcTrig) is not None):
                            mainTrig.connect_to(funcTrig)
                else:
                    connectToOutput[0].port.connect_to(connectToInput)
        elif (len(self.localNumbers) == 1):
            isBool = False
            if ((equation == "1") or (equation == "0") and (connectToInput.valueType == "bool" or connectToInput.valueType == "_trigger")):
                staticNode = self.ga.addModifierTriggerBool(self.xOffset - self.iterationLevel * self.xSpread, mainNode.y_pos())
                isBool = True
            else:
                staticNode = self.ga.addModifierStaticValue(self.xOffset - self.iterationLevel * self.xSpread, mainNode.y_pos())

            staticNode.command = mainNode.command
            self.nodesAdded.append(staticNode)

            if isBool:
                if (equation == "1"):
                    staticTriggerPort = staticNode.get_input("True")
                    staticNode.set_value(True)
                else:
                    staticTriggerPort = staticNode.get_input("False")
                    staticNode.set_value(False)
            else:
                staticNode.set_value(equation)
                staticTriggerPort = staticNode.get_input("_trigger")

            staticOutPort = staticNode.get_output("out")
            if not hasattr(connectToOutput[0].port, "name"):
                pass
            if (connectToOutput[0].port.name != "_trigger"):
                triggerPort = connectToOutput[0].port.model.node.get_output("_trigger")
                if (triggerPort is not None):
                    connectToOutput[0].port = triggerPort
            staticTriggerPort.connect_to(connectToOutput[0].port)
            staticOutPort.connect_to(connectToInput)
        elif (len(self.localFunctions) == 1):
            skip = False
            for f in self.skipFunctions:
                if f.name == self.localFunctions[0].lower():
                    skip = True
                    break
            if skip:
                self.overrideFunction(f, mainNode, equation, connectToInput, connectToOutput)
            else:
                self.connectFunctionArguments(str(self.localFunctions[0]), equation, mainNode, connectToOutput[0], 0, None, connectToInput)
        else:
            print("This should never happen")
        self.iterationLevel -= 1

    def optimizeObjects(self):
        self.removeDuplicateObjects()
        self.optimizeDeadbands()
        self.optimizeMakeBools()

    def deleteAllAssociatedNodes(self, mainNode):
        for node in self.ga.graph.all_nodes():
            try:
                if ((node.command == mainNode.command) and (("nodes.modifiers" in str(node.type_)) or ("nodes.virtualmodifiers" in str(node.type_)))):
                    self.ga.graph.remove_node(node)
            except:
                pass
            pass

    def removeDuplicateObjects(self):
        while(self.removeDuplicateObjectsIter()):
            pass
        pass

    def removeDuplicateObjectsIter(self):
        modifiers = []
        for node in self.ga.graph.all_nodes():
            if (("nodes.modifiers" in str(node.type_)) or ("nodes.virtualmodifiers" in str(node.type_))):
                modifiers.append(node)

        for node in modifiers:
            compareNode = node
            for node in modifiers:
                try:
                    # If nodes belong to the same command, have the same type but is not the same instance, continue
                    if ((compareNode.command == node.command) and (compareNode is not node) and (compareNode.type_ == node.type_)):
                        containsSame = True

                        for portNumber in range(0, len(compareNode.inputs())):
                            compareNodePort = compareNode.get_input(portNumber)
                            nodePort = node.get_input(portNumber)
                            compareNodePortConnections = compareNodePort.connected_ports()
                            nodePortConnections = nodePort.connected_ports()

                            #check if all INPUT connections are the same
                            if (len(compareNodePortConnections) == len(nodePortConnections)):
                                for connectionNumber in range(0, len(compareNodePortConnections)):
                                    if (compareNodePortConnections[connectionNumber] != nodePortConnections[connectionNumber]):
                                        containsSame = False
                                        break
                                #if this is a value-based modifier, check if they have the same value
                                if ((containsSame == True) and (("Equation" in node.NODE_NAME) or
                                                                ("Static value" in node.NODE_NAME) or
                                                                ("Make boolean" in node.NODE_NAME) or
                                                                ("Trigger bool" in node.NODE_NAME))):

                                    if (compareNode.get_value() != node.get_value()):
                                        containsSame = False
                                        break
                            else:
                                containsSame = False
                                break
                            pass
                        #if the nodes are indeed COMING FROM the same object, with the same input ports, but GOING TO different things,
                        #add all the OUTPUT connections from the first object to the second object and remove the first object
                        if (containsSame == True):
                            compareOutPorts = compareNode.output_ports()
                            for outPortNumber in range(0, len(compareOutPorts)):
                                outPort = compareOutPorts[outPortNumber]
                                nodeOutPort = node.get_output(outPort.name())
                                for connection in nodeOutPort.connected_ports():
                                    outPort.connect_to(connection)
                            self.ga.graph.remove_node(node)
                            return True
                        pass
                    #If not, check if the objects are of the same type but is not the same object
                    elif ((compareNode is not node) and (compareNode.type_ == node.type_)):
                        containsSame = True

                        for portNumber in range(0, len(compareNode.outputs())):
                            compareNodePort = compareNode.get_output(portNumber)
                            nodePort = node.get_output(portNumber)
                            compareNodePortConnections = compareNodePort.connected_ports()
                            nodePortConnections = nodePort.connected_ports()

                            # check if all OUTPUT connections are the same
                            if (len(compareNodePortConnections) == len(nodePortConnections)):
                                for connectionNumber in range(0, len(compareNodePortConnections)):
                                    if (compareNodePortConnections[connectionNumber] != nodePortConnections[connectionNumber]):
                                        containsSame = False
                                        break
                                # if this is a value-based modifier, check if they have the same value
                                if ((containsSame == True) and (("Equation" in node.NODE_NAME) or
                                                                ("Static value" in node.NODE_NAME) or
                                                                ("Make boolean" in node.NODE_NAME) or
                                                                ("Trigger bool" in node.NODE_NAME))):

                                    if (compareNode.get_value() != node.get_value()):
                                        containsSame = False
                                        break
                            else:
                                containsSame = False
                                break
                            pass
                        # if the nodes are indeed GOING TO the same objects, but COMING FROM different things,
                        # add all the INPUT connections from the first object to the second object and remove the first object
                        if (containsSame == True):
                            compareInPorts = compareNode.input_ports()
                            for inPortNumber in range(0, len(compareInPorts)):
                                inPort = compareInPorts[inPortNumber]
                                nodeInPort = node.get_input(inPort.name())
                                for connection in nodeInPort.connected_ports():
                                    inPort.connect_to(connection)
                            self.ga.graph.remove_node(node)
                            return True
                        pass
                except Exception as e:
                    print("Node has no command attribute")
        return False

    def optimizeMakeBools(self):
        while (self.optimizeMakeBoolsIter()):
            pass

    def optimizeMakeBoolsIter(self):
        for node in self.ga.graph.all_nodes():
            if ("Make boolean" in node.NODE_NAME):
                #Remove trigger connection if it connects to the same root object in order to de-clutter
                inRoots = node.findRootPort("in")
                trigRoots = node.findRootPort("_trigger")

                r = None; t = None; tp = None
                if (len(inRoots) > 0):
                    for i in inRoots[0]:
                        if isinstance(i, CustomBaseNode): r = i; break
                else:
                    pass
                if (len(trigRoots) > 0):
                    for i in trigRoots[0]:
                        if isinstance(i, CustomBaseNode): t = i
                        elif isinstance(i, NodeGraphQt.Port): tp = i
                else:
                    pass

                if (r == t):
                    node.get_input("_trigger").disconnect_from(tp)
        return False

    def optimizeDeadbands(self):
        modifierList = []
        for node in self.ga.graph.all_nodes():
            if ("Deadband" in node.NODE_NAME):
                modifierList.append(node)

        for node in modifierList:
            inputConnections = node.get_input("threshold").connected_ports()
            if (len(inputConnections) == 1):
                if ("Static value" in inputConnections[0].model.node.NODE_NAME):
                    value = inputConnections[0].model.node.get_value()
                    node.set_value(value)
                    self.ga.graph.remove_node(inputConnections[0].model.node)

