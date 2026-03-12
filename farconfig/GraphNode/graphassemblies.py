from pathlib import Path

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QEasingCurve

# import example nodes from the "nodes" sub-package
#from nodes import basic_nodes, custom_ports_node, group_node, widget_nodes

from NodeGraphQt import Port
from .customnode import CustomBaseNode, Equation
import GraphNode.customnode as FARNodes
from .customgroupnode import CustomGroupNode, CustomNodeGraph
from Custom_Widgets import QCustomCheckBox

from NodeGraphQt import NodeGraph, NodesPaletteWidget, NodesTreeWidget, PropertiesBinWidget, BaseNode, BackdropNode, constants
from commanddefinitions import CommandID

#ass_node_color = "#000000"
#ass_node_background = (210,210,210)
#wrap_background = (30,30,30)

def connectNodes(outputNode : BaseNode, outputName : str, inputNode : BaseNode, inputName : str):
    outputName = outputName.lower()
    outPort = outputNode.get_output(outputName)
    inputName = inputName.lower()
    inPort = inputNode.get_input(inputName)
    if ((outPort is None) or (inPort is None)):
        pass
    outPort.connect_to(inPort)

class graphAssembly():
    def __init__(self, graph:NodeGraph, name, posx, index = 0, hierarchy = None):
        self.nodes:list[FARNodes.CustomBaseNode] = []

        self.graph = graph
        self.x = posx
        self.name = name
        self.index = index
        self.hierarchy = hierarchy

    def insertNode(self, inNode, pos):
        self.graph.add_node(inNode, pos)
        self.nodes.append(inNode)

    def addNode(self, nodeName, posy, name = "", command = None, locked = True, argumentMatch = None):
        node = self.graph.create_node(nodeName, pos=[self.x, posy], name=name)
        if (locked):
            #node.set_property('locked', True)
            node.locked = True
        if (command is not None):
            node.command = command
        node.argumentMatch = argumentMatch
        self.nodes.append(node)
        return node

#    def wrapAll(self, name):
#        self.backdrop  = self.graph.create_node('Backdrop', name=name)
#        self.backdrop.set_color(wrap_background[0],wrap_background[1],wrap_background[2])
#        self.backdrop.wrap_nodes(self.nodes)

    def getNode(self, nodeName):
        for node in self.nodes:
            if (node.NODE_NAME == nodeName):
                return node
        return None

class graphAssemblies():
    BASE_PATH = Path(__file__).parent.resolve()

    def __init__(self, container = None):
        self.assemblies:list[graphAssembly] = []

        # create graph controller.
        #CustomNodeGraph
        self.graph = CustomNodeGraph()

        # set up context menu for the node graph.
        hotkey_path = Path(self.BASE_PATH, 'hotkeys', 'hotkeys.json')
        self.graph.set_context_menu_from_file(hotkey_path, 'graph')

        '''
        basic_nodes.BasicNodeA,
        basic_nodes.BasicNodeB,
        basic_nodes.CircleNode,
        basic_nodes.SVGNode,
        custom_ports_node.CustomPortsNode,
        group_node.MyGroupNode,
        widget_nodes.DropdownMenuNode,
        widget_nodes.TextInputNode,
        widget_nodes.CheckboxNode,
        '''

        # registered example nodes.
        self.graph.register_nodes([

            FARNodes.NoteOn,
            FARNodes.NoteOff,
            FARNodes.Pitchbend,
            FARNodes.ChannelAftertouch,
            FARNodes.PolyAftertouch,
            FARNodes.ProgramChange,
            FARNodes.ControlChange,

            FARNodes.Variables,

            #FARNodes.Solenoid,
            #FARNodes.BowControl,
            #FARNodes.HarmonicSeriesHandler,
            #FARNodes.BowMotor,
            #FARNodes.BowPressure,
            #FARNodes.BowPID,
            #FARNodes.Mute,

            FARNodes.Equation,
            FARNodes.Equation1,
            FARNodes.Equation2,
            FARNodes.Equation3,
            FARNodes.Midi14Bit_to_FAR16Bit,
            FARNodes.Midi7Bit_to_FAR16Bit,
            FARNodes.StaticValue,
            FARNodes.TriggerVariable,
            FARNodes.TriggerBool,

            #FARNodes.ControlBox,

            FARNodes.ControlBoxOutput,

            FARNodes.Bool,
            FARNodes.Deadband,
            FARNodes.Map,
            FARNodes.Multiplexer,

            CustomGroupNode
        ])

        self.graph.set_grid_mode(0)
        self.graph.set_background_color(255,255,255)

        # show the node graph widget.
        if container is None:
            self.graph_widget = self.graph.widget
            self.graph_widget.resize(1900, 1040)
            self.graph_widget.setWindowTitle("NodeGraphQt Example")
            self.graph_widget.showMaximized()
        else:
            self.graph_widget = self.graph.widget

            container.addWidget(self.graph.widget)

        # create a node properties bin widget.
        self.properties_bin = PropertiesBinWidget(node_graph=self.graph, parent=self.graph_widget)
        self.properties_bin.setWindowFlags(QtCore.Qt.Tool)

        # example show the node properties bin widget when a node is double-clicked.
        def display_properties_bin(node):
            if not self.properties_bin.isVisible():
                self.properties_bin.show()

        # wire function to "node_double_clicked" signal.
        self.graph.node_double_clicked.connect(display_properties_bin)

        # create a nodes tree widget.
        self.nodes_tree = NodesTreeWidget(node_graph=self.graph)
        self.nodes_tree.set_category_label('nodeGraphQt.nodes', 'Builtin Nodes')
        self.nodes_tree.set_category_label('nodes.custom.ports', 'Custom Port Nodes')
        self.nodes_tree.set_category_label('nodes.widget', 'Widget Nodes')
        self.nodes_tree.set_category_label('nodes.basic', 'Basic Nodes')
        self.nodes_tree.set_category_label('nodes.group', 'Group Nodes')
        #    nodes_tree.show()

        # create a node palette widget.
        self.nodes_palette = NodesPaletteWidget(node_graph=self.graph)
        self.nodes_palette.set_category_label('nodeGraphQt.nodes', 'Builtin Nodes')
        self.nodes_palette.set_category_label('nodes.custom.ports', 'Custom Port Nodes')
        self.nodes_palette.set_category_label('nodes.widget', 'Widget Nodes')
        self.nodes_palette.set_category_label('nodes.basic', 'Basic Nodes')
        self.nodes_palette.set_category_label('nodes.group', 'Group Nodes')
        #    nodes_palette.show()

        pass

    def findInputPortFromCommand(self, command:str):
        for assembly in self.assemblies:
            for node in assembly.nodes:
                for port in node.input_ports():
                    try:
                        if port.command.lower() == command.lower():
                            return port
                    except:
                        pass
        return None

    def findNodeWithConnectionAndValue(self, outPort:Port, object, value):
        for connection in outPort.connected_ports():
            node = connection.model.node
            if isinstance(node, object):

                try:
                    if node.get_value() == value:
                        return node
                except:
                    pass
        return None

    def getPortForVariable(self, node, variableName):
        outPort = node.get_output(variableName)
        if (outPort is not None):
            return outPort
        ports = node.outputs()
        for port in ports:
            try:
                if (port.variable == variableName):
                    return port
            except:
                print (str(port) + " doesn't have a 'variable' attribute")
                return None

    def findLocalOrVariableOutput(self, node, portName):
#        outPort = node.get_output(portName)
        outPort = self.getPortForVariable(node, portName)
        if outPort is None:
            assembly = self.getAssembly("Variables")
            if assembly is None: return None
            assemblyNode = assembly.getNode("Variables")
            if assemblyNode is None: return None
            #outPort = assemblyNode.get_output(portName)
            outPort =  self.getPortForVariable(assemblyNode, portName)
        return outPort

    def addAssembly(self, name, posx):
        new = graphAssembly(self.graph, name, posx)
        self.assemblies.append(new)
        return new

    def insertAssembly(self, assembly:graphAssembly) -> graphAssembly:
        for existing in self.assemblies:
            if (existing.name == assembly.name) and (existing.index == assembly.index) and (existing.hierarchy == assembly.hierarchy):
                return existing
        self.assemblies.append(assembly)
        return assembly

    def getAssembly(self, name):
        for assembly in self.assemblies:
            if (assembly.name == name):
                return assembly
        return None

    def addMIDIAssembly(self, posx, posy):
        assembly = self.addAssembly('MIDI events', posx)

        assembly.addNode('nodes.midi.NoteOn', posy, name = "MIDI Note On", command=[CommandID.midiConfigurationData], argumentMatch=["noteon"])
        assembly.addNode('nodes.midi.NoteOff', posy + 135, name = "MIDI Note Off", command=[CommandID.midiConfigurationData], argumentMatch=["noteoff"])
        assembly.addNode('nodes.midi.Pitchbend', posy + 270, name = "MIDI Pitchbend", command=[CommandID.midiConfigurationData], argumentMatch=["pb"])
        assembly.addNode('nodes.midi.ChannelAftertouch', posy + 385, name = "MIDI Ch Aftertouch", command=[CommandID.midiConfigurationData], argumentMatch=["cat"])
        assembly.addNode('nodes.midi.PolyAftertouch', posy + 500, name = "MIDI Poly Aftertouch", command=[CommandID.midiConfigurationData], argumentMatch=["pat"])
        assembly.addNode('nodes.midi.ProgramChange', posy + 635, name = "MIDI Program change", command=[CommandID.midiConfigurationData], argumentMatch=["pc"])
        assembly.addNode('nodes.midi.ControlChange', posy + 745, name = 'MIDI CC 64 (sustain)', command=[CommandID.midiConfigurationData], argumentMatch=["cc", "64"])
        assembly.addNode('nodes.midi.ControlChange', posy + 865, name = 'MIDI CC 123 (all notes off)', command=[CommandID.midiConfigurationData], argumentMatch=["cc", "64"])
#        assembly.wrapAll('MIDI events')
        return assembly

    def addControlboxAssembly(self, posx, posy):
        assembly = self.addAssembly('Control box', posx)
        #assembly.addNode('nodes.hardware.ControlBox', posy)
        posyStep = 100
        assembly.addNode('nodes.hardware.ControlBoxOutput', posy, "CB Harmonic", [CommandID.controlBoxControlData], argumentMatch=["0"])
        assembly.addNode('nodes.hardware.ControlBoxOutput', posy + posyStep * 1, "CB Harmonic shift mod", [CommandID.controlBoxControlData], argumentMatch=["1"])
        assembly.addNode('nodes.hardware.ControlBoxOutput', posy + posyStep * 2, "CB Harmonic shift", [CommandID.controlBoxControlData], argumentMatch=["2"])
        assembly.addNode('nodes.hardware.ControlBoxOutput', posy + posyStep * 3, "CB Pressure", [CommandID.controlBoxControlData], argumentMatch=["3"])
        assembly.addNode('nodes.hardware.ControlBoxOutput', posy + posyStep * 4, "CB Hammer", [CommandID.controlBoxControlData], argumentMatch=["4"])
        assembly.addNode('nodes.hardware.ControlBoxOutput', posy + posyStep * 5, "CB Engage", [CommandID.controlBoxControlData], argumentMatch=["5"])
        assembly.addNode('nodes.hardware.ControlBoxOutput', posy + posyStep * 6, "CB Hammer ratio", [CommandID.controlBoxControlData], argumentMatch=["6"])
        assembly.addNode('nodes.hardware.ControlBoxOutput', posy + posyStep * 7, "CB Mute", [CommandID.controlBoxControlData], argumentMatch=["7"])
#        assembly.wrapAll("Control box")

        return assembly
        #assembly.wrapAll('Control box')

    def addVariablesAssembly(self, posx, posy):
        assembly = self.addAssembly('Variables', posx)
        assembly.addNode('nodes.far.Variables', posy)
        return assembly

        #assembly.wrapAll('Variables')

    def addHammerAssembly(self, posx, posy):
        assembly = self.addAssembly('Hammer', posx)
        assembly.addNode('nodes.hardware.Solenoid', posy)
        return assembly

        #assembly.wrapAll('Hammer')

    def addHarmonicHandlerAssembly(self, posx, posy):
        assembly = self.addAssembly('Harmonic series handler', posx)
        assembly.addNode('nodes.hardware.HarmonicSeriesHandler', posy)
        return assembly

        #assembly.wrapAll('Harmonic Handler')

    def addBowAssembly(self, posx, posy):
        assembly = self.addAssembly('Bow', posx)
        assembly.addNode('nodes.hardware.BowControl', posy)
        assembly.addNode('nodes.hardware.BowMotor', posy + 110)
        assembly.addNode('nodes.hardware.BowPID', posy + 240)
        assembly.addNode('nodes.hardware.BowPressure', posy + 445)
#        assembly.wrapAll('Bow')
        return assembly

    def addMuteAssembly(self, posx, posy):
        assembly = self.addAssembly('Mute', posx)
        assembly.addNode('nodes.hardware.Mute', posy)
        return assembly
        #assembly.wrapAll('Harmonic Handler')

    def update(self):
        # fit nodes to the viewer.
        self.graph.clear_selection()
        self.graph.fit_to_selection()
        pass

    def addCompleteStringAssembly(self, posx, posy):
        hhandlerAss = self.addHarmonicHandlerAssembly(posx, posy)
        bowAss = self.addBowAssembly(posx, posy + 265)
        self.addHammerAssembly(posx, posy + 935)
        self.addMuteAssembly(posx, posy + 1120)

        hhandler:FARNodes.HarmonicSeriesHandler = hhandlerAss.getNode("Harmonic series handler")
        pid:FARNodes.BowPID = bowAss.getNode("Bow PID")
        connectNodes(hhandler, "Frequency", pid, "Frequency")
        motor:FARNodes.BowMotor = bowAss.getNode("Bow motor")
        connectNodes(pid, "Direct PWM", motor, "Direct PWM")

        #hhandler.get_output("frequency").set_locked(True)
        #pid.get_output("direct pwm").set_locked(True)
        pass

    def addBasicControlHandling(self, posx, posy):
        self.addMIDIAssembly(posx, posy)
        self.addControlboxAssembly(posx, posy+1095)
        self.addVariablesAssembly(posx, posy + 1095 + 855)

    def addModifierStaticValue(self, posx, posy):
        node = self.graph.create_node('nodes.virtualmodifiers.StaticValue', pos=[posx, posy])
        #node.set_color(ass_node_background[0], ass_node_background[1], ass_node_background[2])
        return node

    def addModifierEquation(self, inputs, posx, posy):
        node = self.graph.create_node('nodes.virtualmodifiers.Equation', pos=[posx, posy])
        node.setInputs(inputs)
        return node

    def addModifierEquation1(self, posx, posy):
        node = self.graph.create_node('nodes.virtualmodifiers.Equation1', pos=[posx, posy])
        #node.set_color(ass_node_background[0], ass_node_background[1], ass_node_background[2])
        return node

    def addModifierEquation2(self, posx, posy):
        node = self.graph.create_node('nodes.virtualmodifiers.Equation2', pos=[posx, posy])
        #node.set_color(ass_node_background[0], ass_node_background[1], ass_node_background[2])
        return node

    def addModifierEquation3(self, posx, posy):
        node = self.graph.create_node('nodes.virtualmodifiers.Equation3', pos=[posx, posy])
        #node.set_color(ass_node_background[0], ass_node_background[1], ass_node_background[2])
        return node

    def addModifierBool(self, posx, posy):
        node = self.graph.create_node('nodes.modifiers.Bool', pos=[posx, posy])
        #node.set_color(ass_node_background[0], ass_node_background[1], ass_node_background[2])
        return node

    def addModifierDeadband(self, posx, posy):
        node = self.graph.create_node('nodes.modifiers.Deadband', pos=[posx, posy])
        #node.set_color(ass_node_background[0], ass_node_background[1], ass_node_background[2])
        return node

    def addModifierTriggerBool(self, posx, posy):
        node = self.graph.create_node('nodes.virtualmodifiers.TriggerBool', pos=[posx, posy])
        switch:QCustomCheckBox.QCustomCheckBox = node.toggleSwitch.customWidget.switch
        #switch.customizeQCustomCheckBox(bgColor = "#c3c3c3", circleColor = "#ffffff", activeColor = "#17a8e3", animationEasingCurve = QEasingCurve.Linear, animationDuration = 0)
        #switch.setTristate(True)
        #switch.setStyleSheet()
        #node.set_color(ass_node_background[0],ass_node_background[1],ass_node_background[2])
        return node

    def addModifierMap(self, posx, posy):
        node = self.graph.create_node('nodes.modifiers.Map', pos=[posx, posy])
        return node

    def addDefaultFARSingle(self):
        self.addBasicControlHandling(-1000, -500)
        self.addCompleteStringAssembly(1000, -570)

        n_velocityTo16 = self.graph.create_node('nodes.virtualmodifiers.Midi7Bit_to_FAR16Bit', pos=[0, -500])
        n_velocityTo16.set_value(512)
        n_velocityEquation = self.graph.create_node('nodes.virtualmodifiers.Equation2', pos=[500, -500])
        n_velocityEquation.set_value("A * (1 - B)")
        n_pitchbendTo16 = self.graph.create_node('nodes.virtualmodifiers.Midi14Bit_to_FAR16Bit', pos=[500, -166])
        n_pitchbendTo16.set_value(512)
        n_noteOnStatic1 = self.graph.create_node('nodes.virtualmodifiers.StaticValue', pos=[500, 235])
        n_noteOnStatic1.set_value("1")
        n_noteOnStatic0 = self.graph.create_node('nodes.virtualmodifiers.StaticValue', pos=[500, 0])
        n_noteOnStatic0.set_value("0")
        n_noteoffBool = self.graph.create_node('nodes.modifiers.Bool', pos=[500, 350])
        n_noteoffBool.set_value(True)
        n_noteOffTriggerVariable = self.graph.create_node('nodes.virtualmodifiers.TriggerVariable', pos=[250, 350])
        n_channelaftertouchTo16 = self.graph.create_node('nodes.virtualmodifiers.Midi7Bit_to_FAR16Bit', pos=[-500, -115])
        n_channelaftertouchTo16.set_value(512)
        n_sustainBool = self.graph.create_node('nodes.modifiers.Bool', pos=[-500, 245])

        n_noteon = self.getAssembly("MIDI events").getNode("Note On")
        n_noteoff = self.getAssembly("MIDI events").getNode("Note Off")
        n_pitchbend = self.getAssembly("MIDI events").getNode("Pitch bend")
        n_ccsustain = self.getAssembly("MIDI events").getNode("CC 64 (sustain)")
        n_channelaftertouch = self.getAssembly("MIDI events").getNode("Channel aftertouch")

        n_variables  = self.getAssembly("Variables").getNode("Variables")
        n_solenoid = self.getAssembly("Hammer").getNode("Solenoid")
        n_harmonichandler = self.getAssembly("Harmonic series handler").getNode("Harmonic series handler")
        n_bowmotor = self.getAssembly("Bow").getNode("Bow motor")
        n_bowpressure = self.getAssembly("Bow").getNode("Bow pressure")
        n_bowpid = self.getAssembly("Bow").getNode("Bow PID")
        n_bowcontrol = self.getAssembly("Bow").getNode("Bow control")
        n_mute = self.getAssembly("Mute").getNode("Mute")
        n_controlbox = self.getAssembly("Control box").getNode("Control box")

        connectNodes(n_noteon, 'Velocity', n_velocityTo16, 'In')
        connectNodes(n_velocityTo16, 'Out', n_velocityEquation, 'In A')
        connectNodes(n_variables, 'Notecount', n_velocityEquation, 'In B')
        connectNodes(n_velocityEquation, 'Out', n_solenoid, 'Engage')
        connectNodes(n_noteon, 'Note', n_harmonichandler, 'Harmonic base')

        connectNodes(n_noteon, '_trigger', n_noteOnStatic1, 'Trigger')
        connectNodes(n_noteOnStatic1, 'Out', n_bowmotor, 'Run')
        connectNodes(n_noteOnStatic1, 'Out', n_bowpressure, 'Engage')
        connectNodes(n_noteOnStatic1, 'Out', n_bowcontrol, 'PID On')
        connectNodes(n_noteOnStatic1, 'Out', n_mute, 'Rest')

        connectNodes(n_noteon, '_trigger', n_noteOnStatic0, 'Trigger')
        connectNodes(n_noteOnStatic0, 'Out', n_bowcontrol, 'Speed mode')

        connectNodes(n_noteoff, '_trigger', n_noteOffTriggerVariable, "Trigger")
        connectNodes(n_variables, 'Notecount', n_noteOffTriggerVariable, "Variable")
        connectNodes(n_noteOffTriggerVariable, "Out", n_noteoffBool, "In")
        connectNodes(n_noteoffBool, "Out", n_bowpressure, "Rest")

        connectNodes(n_pitchbend, 'Value', n_pitchbendTo16, 'In')
        connectNodes(n_pitchbendTo16, 'Out', n_harmonichandler, 'Harmonic shift')

        connectNodes(n_channelaftertouch, 'Pressure', n_channelaftertouchTo16, 'In')
        connectNodes(n_channelaftertouchTo16, 'Out', n_bowpressure, 'Modifier')

        connectNodes(n_ccsustain, 'Value', n_sustainBool, 'In')
        connectNodes(n_sustainBool, 'Out', n_bowpressure, 'Hold')

        connectNodes(n_harmonichandler, 'Frequency', n_bowpid, 'Frequency')

        n_cbHarmDiv = self.graph.create_node('nodes.virtualmodifiers.Equation1', pos=[-500, 350])
        connectNodes(n_controlbox, 'Harmonic', n_cbHarmDiv, 'In')
        n_cbHarmDiv.set_value('In / 1327.716667 - 20')
        connectNodes(n_cbHarmDiv, 'Out', n_harmonichandler, 'Harmonic add')

        n_cbHarmShCVOffset = self.graph.create_node('nodes.virtualmodifiers.Equation1', pos=[-500, 450])
        n_cbHarmShCVOffset.set_value('In - 32236')
        connectNodes(n_controlbox, 'Harmonic shift modulation', n_cbHarmShCVOffset, 'In')
        n_cbHarmShCVDeadband = self.graph.create_node('nodes.modifiers.Deadband', pos=[-200, 450])
        n_cbHarmShCVDeadband.set_value('20')
        connectNodes(n_cbHarmShCVOffset, 'Out', n_cbHarmShCVDeadband, 'Value')
        n_cbHarmShCVDiv = self.graph.create_node('nodes.virtualmodifiers.Equation1', pos=[100, 450])
        n_cbHarmShCVDiv.set_value('In / 2.425')
        connectNodes(n_cbHarmShCVDeadband, 'Out', n_cbHarmShCVDiv, 'In')
        connectNodes(n_cbHarmShCVDiv, 'Out', n_harmonichandler, 'Harmonic shift 5')

        n_cbHarmShOffset = self.graph.create_node('nodes.virtualmodifiers.Equation1', pos=[-500, 550])
        n_cbHarmShOffset.set_value('(In - 32600) * 0.49064')
        connectNodes(n_controlbox, 'Harmonic shift', n_cbHarmShOffset, 'In')
        n_cbHarmShDeadband = self.graph.create_node('nodes.modifiers.Deadband', pos=[-200, 550])
        n_cbHarmShDeadband.set_value('250')
        connectNodes(n_cbHarmShOffset, 'Out', n_cbHarmShDeadband, 'Value')
        connectNodes(n_cbHarmShDeadband, 'Out', n_harmonichandler, 'Harmonic shift')

        connectNodes(n_controlbox, 'Pressure', n_bowpressure, 'Baseline')
        connectNodes(n_controlbox, 'Hammer', n_solenoid, 'Engage')


    def createControlboxAssembly(self):
        n_controlbox = self.graph.create_node('nodes.hardware.ControlBox', pos=[-1000, 565])
