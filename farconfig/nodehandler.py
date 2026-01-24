import sys

import NodeGraphQt

from commandparser import CommandList, CommandItem

sys.path.append('../../GraphNoteQT/')
import graphassemblies
import commandparser
import customnode as FARNodes
import equationParsingHelpers
from enum import Enum
import sympy as sp

from NodeGraphQt.base import port

class NodeHandler:
    def __init__(self, container):
        self.container = container

        self.ga = graphassemblies.graphAssemblies(container)
        self.ga.addBasicControlHandling(-1000, -500)
        self.ga.addCompleteStringAssembly(1000, -570)
        self.ga.update()

        self.xSpread = 100
        self.xOffset = 1200

        self.maxDepth = 0

        self.hideImplicits = True
        self.hideAdvanced = True

    def findCommandMatch(self, command:CommandItem):
        try:
            for assembly in self.ga.assemblies:
                for node in assembly.nodes:
                    if node.command:
                        cl = CommandItem(node.command)
                        if (cl.command == command.command):
                            breakAway = False
                            if len(command.argument) < len(cl.argument) : breakAway = True
                            if (not breakAway):
                                for arg in range(0, len(cl.argument)):
                                    if cl.argument[arg] != command.argument[arg]: breakAway = True
                            #self.parseConnectionsMapped(node, command)
                                if (not breakAway): return node
                    for port in node.input_ports():
                        CommandList.addCommands(port.command)
                    pass
        except Exception as e:
            pass

    def parseCommand(self, command:CommandItem):
        result = self.findCommandMatch(command)
        if result is None:
            print("NodeHandler: Command not found: " + command.command)
            return
        if isinstance(result, FARNodes.CustomBaseNode):
            print (str(result) + " is not an instance of FARNodes.CustomBaseNode")

        self.parseConnectionsMapped(result, command)


    def postBuildUpdate(self):
        self.optimizeObjects()
        for node in self.ga.graph.all_nodes():
            if ("modifier" in node.type_):
                node.updateNames()
        #self.buildHorizontalTree()
        self.ga.graph.nodeOrganizer.buildHorizontalTree()

    def parseConnectionsMapped(self, node:FARNodes.CustomBaseNode, command:commandparser.CommandItem):
        cl:CommandList = None
        if command.command == "mev":
            cl = CommandList(command.argument[1])
        elif command.command == "acm":
            cl = CommandList(command.argument[1])
        else:
            return
        self.deleteAllAssociatedNodes(node)
        for command in cl.commands:
            for arg in command.argument:
                self.process(node, command.command + ":" + command.argument[0])

    iterationLevel = 0
    nodesAdded = []

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
        match (function):
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
            case _:
                raise("Function not recognized!")
                return
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
            self.process(mainNode, argument, defaultOutput, False, functionNode.get_input(functionPortNo))
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

        return equation

    def process(self, mainNode:FARNodes.CustomBaseNode, equation:str, inConnectToOutput = None, skipInput = False, inConnectToInput = None):
        self.iterationLevel += 1

        connectToOutput = []
        connectToInput = inConnectToInput

        if ((":" in equation) and (not skipInput)):
            inputCommand = equation[:equation.index(":")]
            connectToInput = self.ga.findInputPortFromCommand(inputCommand)
            equation = equation[equation.index(":") + 1:]

        self.getChildren(sp.sympify(equation), False)

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
                if ((port.model.node is mainNode) and (connectToOutput[0].default)):
                    connectToOutput[0].port = port
                    connectToOutput[0].default = False
                else:
                    connectToOutput.append(self.processOutput(False, port))

        if ((connectToInput is None) and (not skipInput)):
            return

        self.getChildren(sp.sympify(equation), True)
        if (len(self.localNumbers) + len(self.localFunctions) + len(self.localSymbols) > 1):
            createInputs = len(self.localFunctions) + len(self.localSymbols)

            equationNode = None
            noAdd = False

            match (createInputs):
                case 0:
                    print("Cannot make an equation with zero inputs, for equation " + equation)
                case 1:
                    equationNode = self.ga.addModifierEquation1(self.xOffset - self.iterationLevel * self.xSpread, mainNode.y_pos())
                case 2:
                    equationNode = self.ga.addModifierEquation2(self.xOffset - self.iterationLevel * self.xSpread, mainNode.y_pos())
                case 3:
                    equationNode = self.ga.addModifierEquation3(self.xOffset - self.iterationLevel * self.xSpread, mainNode.y_pos())
                case _:
                    noAdd = True

            if (not noAdd):
                equationNode.command = mainNode.command
                self.nodesAdded.append(equationNode)

                inputNumber = 0
                for symbol in self.localSymbols:
                    portName = "in" + str(inputNumber)
                    #equation = equation.replace(symbol, portName)
                    inPort = equationNode.get_input(portName)
                    outPort = self.ga.findLocalOrVariableOutput(mainNode, str(symbol))
                    outPort.connect_to(inPort)
                    inputNumber += 1

                for function in self.localFunctions:
                    equation = self.connectFunctionArguments(function, equation, mainNode, connectToOutput[0], inputNumber, equationNode)

                equationNode.set_value(equation)
                outPort = equationNode.get_output("out")
                outPort.connect_to(connectToInput)

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
            if ((equation == "1") or (equation == "0") and (connectToInput.valueType == "bool")):
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
            if (connectToOutput[0].port.name != "_trigger"):
                triggerPort = connectToOutput[0].port.model.node.get_output("_trigger")
                if (triggerPort is not None):
                    connectToOutput[0].port = triggerPort
            staticTriggerPort.connect_to(connectToOutput[0].port)
            staticOutPort.connect_to(connectToInput)
        elif (len(self.localFunctions) == 1):
            self.connectFunctionArguments(str(self.localFunctions[0]), equation, mainNode, connectToOutput[0], 0, None, connectToInput)
        else:
            print("This should never happen")
        self.iterationLevel -= 1

    def optimizeObjects(self):
        self.removeDuplicateObjects()
        self.optimizeDeadbands()

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

    def optimizeBools(self):
        while (self.optimizeBoolsIter()):
            pass

    def optimizeBoolsIter(self):
        boolList = []
        for node in self.ga.graph.all_nodes():
            if ("Trigger bool" in node.NODE_NAME):
                boolList.append(node)

        if (len(boolList) < 2): return True
        return False

    def optimizeDeadbands(self):
        modifierList = []
        for node in self.ga.graph.all_nodes():
            if ("Deadband" in node.NODE_NAME):
                modifierList.append(node)

        for node in modifierList:
            inputConnections = node.get_input("threshold").connected_ports()
            if (len(inputConnections) == 1):
                if (inputConnections[0].model.node.NODE_NAME == "Static value"):
                    value = inputConnections[0].model.node.get_value()
                    node.set_value(value)
                    self.ga.graph.remove_node(inputConnections[0].model.node)

