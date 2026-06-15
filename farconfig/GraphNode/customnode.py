import PySide6.QtWidgets
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QGraphicsTextItem

from NodeGraphQt import BaseNode
from NodeGraphQt.qgraphics.node_base import NodeItem, PortItem
from NodeGraphQt.constants import (ICON_NODE_BASE, ITEM_CACHE_MODE, Z_VAL_NODE,
                                   LayoutDirectionEnum, NodeEnum, PortEnum,
                                   PortTypeEnum, NodePropWidgetEnum)
from NodeGraphQt.widgets.node_widgets import NodeLineEdit

from customnodewidgets import NodeSlider, ToggleSwitch, LineEdit, SpinBoxArray, TableView
from nodetemplates.custom_ports_node import draw_triangle_port

from commanddefinitions import CommandID

colorNodeSelect = QtGui.QColor(180,200,50)
colorNodeDeselect = QtGui.QColor(255,255,255)

class CustomNodeItem(NodeItem):
    def __init__(self, name='node', parent=None):
        super().__init__(name, parent)
        self.widgetHeights = 0
        self.midSpacing = 20
        self.widgetNameBackground = QtGui.QColor(240,240,240)
        self.widgetBackground = QtGui.QColor(200,200,200) #QtGui.QColor(*self.color)

    def paint(self, painter, option, widget):
        painter.save()
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)

        # base background.
        margin = 1.0
        rect = self.boundingRect()
        rect = QtCore.QRectF(rect.left() + margin,
                             rect.top() + margin,
                             rect.width() - (margin * 2),
                             rect.height() - (margin * 2))
        radius = 4.0
        painter.setBrush(self.widgetBackground)
        painter.drawRoundedRect(rect, radius, radius)

        painter.setBrush(self.widgetNameBackground)
        painter.drawRect(rect.left() + margin, rect.top() + margin, rect.width() - (margin * 2), self.widgetHeights + 25)

        # light overlay on background when selected.
        if self.selected:
            painter.setBrush(QtGui.Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(rect, radius, radius)

        # node name background.
        padding = 3.0, 2.0
        text_rect = self._text_item.boundingRect()
        text_rect = QtCore.QRectF(text_rect.x() + padding[0],
                                  rect.y() + padding[1],
                                  rect.width() - padding[0] - margin,
                                  text_rect.height() - (padding[1] * 2))
        painter.setBrush(QtGui.QColor(0, 0, 0, 80))
        painter.drawRoundedRect(text_rect, 3.0, 3.0)

        # node border
        if self.selected:
            border_width = 1.2
            border_color = colorNodeSelect
        else:
            border_width = 0.8
            border_color = colorNodeDeselect

        border_rect = QtCore.QRectF(rect.left(), rect.top(),
                                    rect.width(), rect.height())

        pen = QtGui.QPen(border_color, border_width)
        if (self.viewer() is not None):
            pen.setCosmetic(self.viewer().get_zoom() < 0.0)
        path = QtGui.QPainterPath()
        path.addRoundedRect(border_rect, radius, radius)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.setPen(pen)
        painter.drawPath(path)

        painter.restore()

    def _calc_size_horizontal(self):
        # width, height from node name text.
        text_w = self._text_item.boundingRect().width()
        text_h = self._text_item.boundingRect().height()

        # width, height from node ports.
        port_width = 0.0
        p_input_text_width = 0.0
        p_output_text_width = 0.0
        p_input_height = 0.0
        p_output_height = 0.0
        for port, text in self._input_items.items():
            if not port.isVisible():
                continue
            if not port_width:
                port_width = port.boundingRect().width()
            t_width = text.boundingRect().width()
            if text.isVisible() and t_width > p_input_text_width:
                p_input_text_width = text.boundingRect().width()
            #p_input_height += port.boundingRect().height()
            p_input_height += text.boundingRect().height()

        for port, text in self._output_items.items():
            if not port.isVisible():
                continue
            if not port_width:
                port_width = port.boundingRect().width()
            t_width = text.boundingRect().width()
            if text.isVisible() and t_width > p_output_text_width:
                p_output_text_width = text.boundingRect().width()
            #p_output_height += port.boundingRect().height()
            p_output_height += text.boundingRect().height()

        port_text_width = p_input_text_width + p_output_text_width

        # width, height from node embedded widgets.
        widget_width = 0.0
        widget_height = 0.0
        for widget in self._widgets.values():
            if not widget.isVisible():
                continue
            w_width = widget.boundingRect().width()
            w_height = widget.boundingRect().height()
            if w_width > widget_width:
                widget_width = w_width
            widget_height += w_height

        self.widgetHeights = widget_height

        side_padding = 0.0
        if all([widget_width, p_input_text_width, p_output_text_width]):
            port_text_width = max([p_input_text_width, p_output_text_width])
            port_text_width *= 2
        elif widget_width:
            side_padding = 10

        width = max([text_w, p_input_text_width + p_output_text_width + self.midSpacing, widget_width]) + side_padding
        height = max([text_h, p_input_height, p_output_height, widget_height + max([p_input_height, p_output_height])])
        if widget_height:
            # add bottom margin for node widget.
            height += 4.0
        height *= 1.05
        return width, height

    def _align_widgets_horizontal(self, v_offset):
        if not self._widgets:
            return
        rect = self.boundingRect()
        y = rect.y() + v_offset
        inputs = [p for p in self.inputs if p.isVisible()]
        outputs = [p for p in self.outputs if p.isVisible()]
        for widget in self._widgets.values():
            if not widget.isVisible():
                continue
            widget_rect = widget.boundingRect()

            x = self._width / 2 + rect.x() - (widget_rect.width() / 2)
            widget.widget().setTitleAlign('center')

            widget.setPos(x, y)
            y += widget_rect.height()

    ## Rearrange the y-position of the given ports depending on the nodes connected to it in order to avoid as many connection crossings as possible
    def sortByConnections(self, ports):
        sorted = []
        for port in ports:
            if (len(port.connected_ports) == 1):
                py = port.connected_ports[0].node.pos().y() + port.connected_ports[0].pos().y()
            elif (len(port.connected_ports) > 1):
                yavg = 0; yiters = 0;
                for conn in port.connected_ports:
                    yiters += 1
                    yavg += conn.node.pos().y() + conn.pos().y()
                py = int(yavg / yiters)
                pass
            else: py = -9999
            insertPos = 0
            if (len(sorted) == 0) or (py == -9999): insertPos = 0
            else:
                for s in sorted:
                    if (py < s[0]): break
                    insertPos += 1
            sorted.insert(insertPos, [py, port])

        i = 0
        for port in sorted:
            ports[i] = port[1]
            i += 1

        if (len(sorted) > 2):
            pass

        return ports

    def _align_ports_horizontal(self, v_offset):
        sortedInputs = self.sortByConnections(self.inputs)
        sortedOutputs = self.sortByConnections(self.outputs)

        width = self._width
        txt_offset = PortEnum.CLICK_FALLOFF.value - 2
        spacing = 1

        # adjust input position
        #inputs = [p for p in self.inputs if p.isVisible()]
        inputs = [p for p in sortedInputs if p.isVisible()]
        if inputs:
            port_width = inputs[0].boundingRect().width()
            port_height = inputs[0].boundingRect().height()
            port_x = (port_width / 2) * -1
            port_y = v_offset
            for port in inputs:
                port.setPos(port_x, port_y)
                port_y += port_height + spacing
        # adjust input text position
        for port, text in self._input_items.items():
            if port.isVisible():
                txt_x = port.boundingRect().width() / 2 - txt_offset
                text.setPos(txt_x, port.y() - 1.5)

        # adjust output position
        #outputs = [p for p in self.outputs if p.isVisible()]
        outputs = [p for p in sortedOutputs if p.isVisible()]
        if outputs:
            port_width = outputs[0].boundingRect().width()
            port_height = outputs[0].boundingRect().height()
            port_x = width - (port_width / 2)
            port_y = v_offset
            for port in outputs:
                port.setPos(port_x, port_y)
                port_y += port_height + spacing
        # adjust output text position
        for port, text in self._output_items.items():
            if port.isVisible():
                txt_width = text.boundingRect().width() - txt_offset
                txt_x = port.x() - txt_width
                text.setPos(txt_x, port.y() - 1.5)


    def draw_node(self):
        height = self._text_item.boundingRect().height() + 4.0

        # update port text items in visibility.
        for port, text in self._input_items.items():
            if port.isVisible():
                text.setVisible(port.display_name)
        for port, text in self._output_items.items():
            if port.isVisible():
                text.setVisible(port.display_name)

        # setup initial base size.
        self._set_base_size(add_h=height)
        # set text color when node is initialized.
        self._set_text_color(self.text_color)
        # set the tooltip
        self._tooltip_disable(self.disabled)

        # --- set the initial node layout ---
        # (do all the graphic item layout offsets here)

        # align label text
        self.align_label()
        # align icon
        self.align_icon(h_offset=2.0, v_offset=1.0)
        # arrange input and output ports.
        #self.align_ports(v_offset=height + self.widgetHeights + 5)
        self._align_ports_horizontal(v_offset=height + self.widgetHeights + 5)
        # arrange node widgets
        self.align_widgets(v_offset=height - 5)

        self.update()

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        for port in self.outputs:
            for conn in port.connected_ports:
                conn.node.draw_node()
        for port in self.inputs:
            for conn in port.connected_ports:
                conn.node.draw_node()

        #self.draw_node()
        #self.viewer().update()
        #self.update_model()
        #self._view.draw_node()

        pass

class CustomBaseNode(BaseNode):
    def __init__(self, qgraphics_item=None):
        self.NODE_NAME_SHORT = ""
        super(CustomBaseNode, self).__init__(qgraphics_item or CustomNodeItem)
        # Commands associated with node
        self.command = []
        # Name commands associated with node
        self.nameCommand = None
        # Index of associated module
        self.moduleIndex = 0
        self.widgetStyle = "color: #000000; background-color: #f0f0f0; width:250px; max-width:400px;"
        self.equationWidth = 250
        self.locked = False
        self.argumentMatch = None

        if (qgraphics_item is None):
            #self.customView = CustomNodeItem()
            #self.customView.name = self.view.name
            #self.customView.type_ = self.view.type_
            #self._view = self.customView
            pass
        else:
            pass

        self.simpleNodeName = False
        self.concatenatePortName = False

        self.depthLevel = 0
        self.depthChildren = 0
        self.verticalLevel = 0
        self.verticalChildren = 0
        self.maxChildren = 0
#        self.sourceObjects = []

        self.implicit = False
        self.allImplicitChildren = False
        self.source = False

    def hide(self):
        self._view.hide()

    def show(self):
        self._view.show()

    def get_input(self, port):
        if isinstance(port, str):
            for inPort in self.input_ports():
                if (inPort.callsign == port.lower()):
                    return inPort
        return super().get_input(port)

    def get_output(self, port):
        if isinstance(port, str):
            for outPort in self.output_ports():
                if (outPort.callsign == port.lower()):
                    return outPort
        return super().get_output(port)

    def output_ports(self):
        return super().output_ports()

    def input_ports(self):
        return super().input_ports()

    def getPlainTextItem(self, node, direction, port) -> QGraphicsTextItem:
        portText = None
        try:
            if (direction == "in"):
                portText = node.view.get_input_text_item(port.view)
            else:
                portText = node.view.get_output_text_item(port.view)
        except:
            pass
        return portText

    def on_input_connected(self, in_port, out_port):
        #if self.updateNames():
        pass

    def on_input_disconnected(self, in_port, out_port):
        #if self.updateNames():
        pass

    def createMultilineName(self, name, direction):
        if (direction == "in"):
            if ("->" in name):
                if (name.rfind("->") == (len(name) + 2)):
                    name = name[:name.rfind("->")-1]
                pass
        else:
            if ("->" in name):
                name = name[name.find("->")+3:]
                pass
        name = name.replace(" -> ", " ->\n")
        return name

    def buildPortNameFullHierarchy(self, portText, fromNode, fromPort, toPort, direction):
        nodeName = fromNode.name()
        toPortName = toPort.name().lower()
        name = ""
        if ("Static value" in nodeName):
            name = toPortName + "=" + str(fromNode.get_value())
        elif ("Equation" in nodeName):
            name = str(fromNode.get_value())
            if ("Equation1" in nodeName):
                try:
                    fromNode = fromPort.model.node
                    inPort = fromNode.get_input("in0")
                    controlNode = inPort.connected_ports()[0].model.node
                    name = name.replace("value", "[" + controlNode.name() + "]")
                except:
                    pass
        elif ("Deadband" in nodeName):
            try:
                name = nodeName

                fromNode = fromPort.model.node
                inPort = fromNode.get_input("in0")
                controlNode = inPort.connected_ports()[0].model.node
                name = name.replace("value", "[" + controlNode.name() + "]")
            except:
                pass
        elif ("boolean" in nodeName):
            try:
                toNodeName = toPort.model.node.name()
                name = toNodeName + ":" + toPortName
            except:
                pass
        else:
            name = nodeName
            fromPortName = fromPort.name().lower()

            if ((fromPortName != "value") and (fromPortName != "_trigger")):
                name += ":" + fromPortName

        if (direction == "in"):
            name += " ->"
            if ((toPort.variable == "False") or (toPort.variable == "True")):
                name += " [" + toPort.variable + "]"
        else:
            name = "-> " + name
        return name

    def setPortNamesToFullHierarchy(self):
        updated = False

        for inPort in self.input_ports():
            connectedPorts = inPort.connected_ports()
            if ((len(connectedPorts) == 0) and ("modifier" in self.type_)):
                portText = self.getPlainTextItem(self, "in", inPort)
                oldName = portText.toPlainText()
                if (oldName != inPort.name()): updated = True
                portText.setPlainText(inPort.name())
                inPort.model.node.update()
            else:
                if len(connectedPorts) > 1:
                    pass
                for outPort in connectedPorts:
                    if ("modifier" in self.type_):
                        #outPort = connectedPorts[0]
                        portText = self.getPlainTextItem(self, "in", inPort)
                        oldName = portText.toPlainText()
                        name = self.buildPortNameFullHierarchy(portText, outPort.model.node, outPort, inPort, "in")
                        if ((self.concatenatePortName) and ("->" in name)):
                            name = name[:name.find("->") + 2]
                        else:
                            name = self.createMultilineName(name, "in")
                        if (oldName != name): updated = True
                        portText.setPlainText(name)
                        inPort.model.node.update()

                    if ("modifier" in outPort.model.node.type_):
                        portText = self.getPlainTextItem(outPort.model.node, "out", outPort)
                        oldName = portText.toPlainText()
                        name = self.buildPortNameFullHierarchy(portText, inPort.model.node, inPort, outPort, "out")
                        if ((self.concatenatePortName) and ("->" in name)):
                            name = name[name.rfind("->"):]
                        else:
                            name = self.createMultilineName(name, "out")
                        if (oldName != name): updated = True
                        portText.setPlainText(name)
                        #name = name.replace("->", "-")
                        #name = name.replace("\n", "</br>")
                        #portText.setHtml("<div style='text-align:right; text-color:red;'>" + name + "</div>")
                        outPort.model.node.update()

                    if (updated):
                        #outPort.model.node.updateNames()
                        pass
        return updated

    def findIfRootOrEnd(self, direction:str):
        updated = False
        breakAll = False
        connects = []

        if (direction == "in"):
            portList = self.connected_input_nodes()
        else:
            portList = self.connected_output_nodes()

        for port in portList:
            thisItem = None
            for connection in port.connected_ports():
                if ("modifier" not in connection.model.node.type_):
                    if (thisItem is None):
                        thisItem = []
                        thisItem.append(port)
                        connects.append(thisItem)
                    thisItem.append(connection)
            if (breakAll): break

        if (len(connects) > 0):
            for portList in connects:
                newName = ""
                rootPort = portList[0]
                for i in range(1, len(portList)):
                    if (i > 1):
                        newName += ", \n"
                    newName += portList[i].name()

                if (("Trigger bool" in self.NODE_NAME) and (direction == "in")):
                    if ("True" in rootPort.name()):
                        newName += " [True]"
                    else:
                        newName += " [False]"
                portText = self.getPlainTextItem(self, direction, rootPort)
                if (portText is not None):
                    oldName = portText.toPlainText()
                    if (oldName != newName): updated = True
                    portText.setPlainText(newName)

        return updated

    def setPortNamesToRootAndEnd(self):
        updated = self.findIfRootOrEnd("in")
        updated = updated or self.findIfRootOrEnd("out")
        return updated

    def setNodeNamesToRootAndEnd(self):
        if ("modifier" not in self.type_): return False
        changed = False
        roots = []
        ends = []
        roots = self.findRootPort()
        ends = self.findEndPort()
        if (len(roots) > 0) and (len(ends) > 0):
            if isinstance(roots[0][0],  CustomBaseNode):
                newName = roots[0][0].name() + " > "
            else:
                newName = roots[0][1].name() + " > "
            if isinstance(ends[0][0], CustomBaseNode):
                newName += ends[0][0].name()
            else:
                newName += ends[0][1].name()
            if (self._view.name != newName): changed = True
            self._view.name = newName
        return changed

    def setSimpleNodeName(self):
        oldName = self._view.name
        self._view.name = self.name()
        if (oldName != self.name()):
            return True
        else:
            return False

    def buildNodeName(self, rootFromPort = "in0", endFromPort = "out", spacer = ""):
        changed = False
        if (not "modifier" in self.type_):
            return
        roots = []
        ends = []
        roots = self.findRootPort(rootFromPort)
        ends = self.findEndPort(endFromPort)
        if (len(roots) > 0) and (len(ends) > 0):
            newName = roots[0][1].name() + ":" + roots[0][0].name() + " -> "
            if (spacer != ""):
                newName += spacer + " -> "
            newName += ends[0][0].name() + ":" + ends[0][1].name()
            if (self._view.name != newName): changed = True
            self._view.name = newName

        return changed

    def updateNames(self):
        #updated = self.buildPortName()
        updated = self.setPortNamesToRootAndEnd()

        #if (not self.simpleNodeName):
        #    updated = updated or self.buildNodeName()
        #else:
        #updated = updated or self.setSimpleNodeName()

        #updated = updated or self.setNodeNamesToRootAndEnd()

        if updated:
            self.update_model()
            self._view.draw_node()
        return updated

    def add_input(self, name, command=None, valueType="number", variable=None, multi_input=True, display_name=True, color=None, locked=False,
                  painter_func=None, hidden=False, callsign=None, argumentMatch = None):
        #name = name.lower()
        name = name
        port = super().add_input(name, multi_input=multi_input, display_name=display_name, color=color, locked=locked, painter_func=painter_func)
        port.command = command
        port.argumentMatch = argumentMatch
        port.valueType = valueType
        #port.value = None
        port.variable = variable
        if (callsign is not None):
            port.callsign = callsign.lower()
        else:
            port.callsign = name.lower()

        plainText = self.getPlainTextItem(self, "in", port)
        if (plainText is not None):
            plainText.node = self._view

        return port

    def add_output(self, name, command=None, valueType="number", variable=None, multi_output=True, display_name=True, color=None, locked=False,
                   painter_func=None, hidden=False, callsign = None, argumentMatch = None):
        #name = name.lower()
        name= name
        port = super().add_output(name,multi_output=multi_output, display_name=display_name, color=color, locked=locked, painter_func=painter_func)
        port.command = command
        port.argumentMatch = argumentMatch
        port.valueType = valueType
        #port.value = None
        port.variable = variable
        if (callsign is not None):
            port.callsign = callsign.lower()
        else:
            port.callsign = name.lower()

        plainText = self.getPlainTextItem(self, "out", port)
        if (plainText is not None):
            plainText.node = self._view

        return port

    def add_text_input(self, name, label='', text='', placeholder_text='',
                       tooltip=None, tab=None, width=None):
        self.create_property(
            name,
            value=text,
            widget_type=NodePropWidgetEnum.QLINE_EDIT.value,
            widget_tooltip=tooltip,
            tab=tab
        )
        widget = NodeLineEdit(self.view, name, label, text, placeholder_text)
        widget.setToolTip(tooltip or '')
        widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        styleSheetString = "QLineEdit { " + self.widgetStyle + " }"
        widget.widget().setStyleSheet(styleSheetString)
        if (width):
            widget.widget().setFixedWidth(width)

        self.view.add_widget(widget)
        self.view.draw_node()

    def setWidgetColors(self, widgetName, widgeTypeString, widgetType, styleString):
        widget = self.get_widget(widgetName)
        #widget.setMaximumWidth(400)
        if hasattr(widget, 'widget'):
            nodeGroupBox = widget.widget()
            children = nodeGroupBox.children()
            subChild = None
            for child in children:
                if isinstance(child, widgetType):
                    subChild = child
            if (subChild is None):
                print("Child not found in setWidgetColors")
                return
            styleSheetString = widgeTypeString + " { " + styleString + " }"
            subChild.setStyleSheet(styleSheetString)

    def findRootPort(self, portName = "in0"):
        if (portName == None):
            return
        port = self.get_input(portName)
        roots = []
        if (port is None):
            return roots
        for connected in port.connected_ports():
            if (not "modifier" in connected.model.node.type_):
                roots.append(list({connected.model.node, connected}))
            else:
                rootsIter = connected.model.node.findRootPort()
                if (len(rootsIter) > 0):
                    roots = roots + rootsIter
        return roots

    def findEndPort(self, portName = "out"):
        if (portName == None):
            return
        port = self.get_output(portName)
        ends = []
        if (port is None):
            return ends
        for connected in port.connected_ports():
            if (not "modifier" in connected.model.node.type_):
                ends.append(list({connected.model.node, connected}))
            else:
                endsIter = connected.model.node.findEndPort()
                if (len(endsIter) > 0):
                    ends = ends + endsIter
        return ends

mevBackground = QtGui.QColor(146, 216, 159)
acmBackground = QtGui.QColor(83, 166, 98)
variableBackground = QtGui.QColor(246, 235, 126)
controlBackground = QtGui.QColor(126, 148, 246)

# MIDI messages
class NoteOn(CustomBaseNode):
    __identifier__ = "nodes.midi"

    NODE_NAME = 'Note On'

    def __init__(self):
        super(NoteOn, self).__init__()
        self.view.widgetBackground = mevBackground
        #self.command = "mev:noteon"
        self.command = [CommandID.midiConfigurationData]
        self.argumentMatch = ["noteon"]
        self.source = True

        self.add_output('Channel', command = self.command, variable = "channel")
        self.add_output('Note', command = self.command, variable = "note")
        self.add_output('Velocity', command = self.command, variable = "velocity")
        self.add_output('_trigger', command = self.command, variable = "_trig", painter_func = draw_triangle_port, valueType="trig")
        pass

class NoteOff(CustomBaseNode):
    __identifier__ = "nodes.midi"

    NODE_NAME = 'Note Off'

    def __init__(self):
        super(NoteOff, self).__init__()
        self.view.widgetBackground = mevBackground
        #self.command = "mev:noteoff"
        self.command = [CommandID.midiConfigurationData]
        self.argumentMatch = ["noteoff"]
        self.source = True

        self.add_output('Channel', command = self.command, variable = "channel")
        self.add_output('Note', command = self.command, variable = "note")
        self.add_output('Velocity', command = self.command, variable = "velocity")
        self.add_output('_trigger', command = self.command, variable = "_trig", painter_func=draw_triangle_port, valueType="trig")
        pass


class Pitchbend(CustomBaseNode):
    __identifier__ = "nodes.midi"

    NODE_NAME = 'Pitch bend'

    def __init__(self):
        super(Pitchbend, self).__init__()
        self.view.widgetBackground = mevBackground
        #self.command = "mev:pb"
        self.command = [CommandID.midiConfigurationData]
        self.argumentMatch = ["pb"]
        self.source = True

        self.add_output('Channel', command = self.command, variable = "channel")
        self.add_output('Pitch', command = self.command, variable = "pitch")
        self.add_output('_trigger', command = self.command, variable = "_trig", painter_func=draw_triangle_port, valueType="trig")

class PolyAftertouch(CustomBaseNode):
    __identifier__ = "nodes.midi"

    NODE_NAME = 'Poly aftertouch'

    def __init__(self):
        super(PolyAftertouch, self).__init__()
        self.view.widgetBackground = mevBackground
        #self.command = "mev:pat"
        self.command = [CommandID.midiConfigurationData]
        self.argumentMatch = ["pat"]
        self.source = True

        self.add_output('Channel', command = self.command, variable = "channel")
        self.add_output('Note', command = self.command, variable = "note")
        self.add_output('Pressure', command = self.command, variable = "pressure")
        self.add_output('_trigger', command = self.command, variable = "_trig", painter_func=draw_triangle_port, valueType="trig")

class ChannelAftertouch(CustomBaseNode):
    __identifier__ = "nodes.midi"

    NODE_NAME = 'Channel aftertouch'

    def __init__(self):
        super(ChannelAftertouch, self).__init__()
        self.view.widgetBackground = mevBackground
        #self.command = "mev:cat"
        self.command = [CommandID.midiConfigurationData]
        self.argumentMatch = ["cat"]
        self.source = True

        self.add_output('Channel', command = self.command, variable = "channel")
        self.add_output('Pressure', command = self.command, variable = "pressure")
        self.add_output('_trigger', command = self.command, variable = "_trig", painter_func=draw_triangle_port, valueType="trig")

class ControlChange(CustomBaseNode):
    __identifier__ = "nodes.midi"

    NODE_NAME = 'Control change'

    def __init__(self):
        super(ControlChange, self).__init__()
        self.view.widgetBackground = mevBackground
        #self.command = "mev:cc"
        self.command = [CommandID.midiConfigurationData]
        self.argumentMatch = ["cc"]
        self.source = True

        self.add_output('Channel', command = self.command, variable = "channel")
        self.add_output('Value', command = self.command, variable = "value")
        self.add_output('_trigger', command = self.command, variable = "_trig", painter_func=draw_triangle_port, valueType="trig")
        self.node_text = self.add_text_input(name='Control', text='64', width=50)

        self.setWidgetColors('Control', 'QLineEdit', PySide6.QtWidgets.QLineEdit, self.widgetStyle)

    def set_value(self, value):
        self.node_text.set_value(value)

    def get_value(self):
        return self.node_text.get_value()

class ProgramChange(CustomBaseNode):
    __identifier__ = "nodes.midi"

    NODE_NAME = 'Program change'

    def __init__(self):
        super(ProgramChange, self).__init__()
        self.view.widgetBackground = mevBackground
        #self.command = "mev:pc"
        self.command = [CommandID.midiConfigurationData]
        self.argumentMatch = "pc"
        self.source = True

        self.add_output('Channel', command = self.command, variable = "channel")
        self.add_output('Program', command = self.command, variable = "program")
        self.add_output('_trigger', command = self.command, variable = "_trig", painter_func=draw_triangle_port, valueType="trig")

# Virtual Modifiers

class Midi7Bit_to_FAR16Bit(CustomBaseNode):
    __identifier__ = "nodes.virtualmodifiers"

    NODE_NAME = "7-bit to 16-bit"

    def __init__(self):
        super(Midi7Bit_to_FAR16Bit, self).__init__()

        self.add_input("In", variable="in0")
        self.add_output("Out", variable="out")

        self.node_slider = NodeSlider(self.view)
        self.add_custom_widget(self.node_slider)

        self.setWidgetColors('value', 'QLineEdit', PySide6.QtWidgets.QLineEdit, self.widgetStyle)

    def set_value(self, value):
        self.node_slider.set_value(value)

    def get_value(self):
        return self.node_slider.get_value()


class Midi14Bit_to_FAR16Bit(CustomBaseNode):
    __identifier__ = "nodes.virtualmodifiers"

    NODE_NAME = "14-bit to 16-bit"

    def __init__(self):
        super(Midi14Bit_to_FAR16Bit, self).__init__()
        self.add_input("In", variable="in0")
        self.add_output("Out", variable="out")

        self.node_slider = NodeSlider(self.view)
        self.add_custom_widget(self.node_slider)

        self.setWidgetColors('value', 'QLineEdit', PySide6.QtWidgets.QLineEdit, self.widgetStyle)

    def set_value(self, value):
        self.node_slider.set_value(value)

    def get_value(self):
        return self.node_slider.get_value()

class Equation(CustomBaseNode):
    __identifier__ = "nodes.virtualmodifiers"

    NODE_NAME = "Equation"

    def __init__(self):
        super(Equation, self).__init__()
        self.add_input("in0", variable="in0")
        self.add_output("out", variable="out")
        self.add_text_input('Equation',placeholder_text='in0 * 5', width=self.equationWidth)
        self.setWidgetColors('Equation', 'QLineEdit', PySide6.QtWidgets.QLineEdit, self.widgetStyle)
        self.inputsSet = False

    def setInputs(self, inputs):
        if self.inputsSet: return
        for i in range(1,inputs):
            self.add_input("in"+str(i), variable="in"+str(i))
        self.inputsSet = True

    def set_value(self, value):
        self.get_widget('Equation').set_value(value)

    def get_value(self):
        return self.get_widget('Equation').get_value()

#    def buildNodeName(self, rootFromPort = "in0", endFromPort = "out"):
#        if ((len(self.get_input("in0").connected_ports()) > 0) and  (len(self.get_output("out").connected_ports()) > 0)):
#            pass
#        return super().buildNodeName(rootFromPort, endFromPort)

    def setSimpleNodeName(self):
        self._view.name = "Dynamic parameter equation"
        return False

class Equation1(CustomBaseNode):
    __identifier__ = "nodes.virtualmodifiers"

    NODE_NAME = "Equation1"

    def __init__(self):
        super(Equation1, self).__init__()
        self.add_input("in0", variable="in0")
        self.add_output("out", variable="out")
        self.add_text_input('Equation1',placeholder_text='in0 * 5', width=self.equationWidth)
        self.setWidgetColors('Equation1', 'QLineEdit', PySide6.QtWidgets.QLineEdit, self.widgetStyle)

    def set_value(self, value):
        self.get_widget('Equation1').set_value(value)

    def get_value(self):
        return self.get_widget('Equation1').get_value()

    def buildNodeName(self, rootFromPort = "in0", endFromPort = "out"):
        if ((len(self.get_input("in0").connected_ports()) > 0) and  (len(self.get_output("out").connected_ports()) > 0)):
            pass
        return super().buildNodeName(rootFromPort, endFromPort)

    def setSimpleNodeName(self):
        self._view.name = "Single parameter equation"
        return False

class Equation2(CustomBaseNode):
    __identifier__ = "nodes.virtualmodifiers"

    NODE_NAME = "Equation2"

    def __init__(self):
        super(Equation2, self).__init__()
        self.add_input("in0", variable="in0")
        self.add_input("in1", variable="in1")
        self.add_output("out", variable="out")
        self.add_text_input('Equation2',placeholder_text='in0 * (in1 + 1)', width=self.equationWidth)
        self.setWidgetColors('Equation2', 'QLineEdit', PySide6.QtWidgets.QLineEdit, self.widgetStyle)

    def set_value(self, value):
        self.get_widget('Equation2').set_value(value)

    def get_value(self):
        return self.get_widget('Equation2').get_value()

    def findRootPort(self, portName = "in0"):
        first = []
        second = []
        first = super().findRootPort("in0")
        second = super().findRootPort("in1")
        return (first + second)

    def setSimpleNodeName(self):
        self._view.name = "Dual parameter equation"
        return False

class Equation3(CustomBaseNode):
    __identifier__ = "nodes.virtualmodifiers"

    NODE_NAME = "Equation3"

    def __init__(self):
        super(Equation3, self).__init__()
        self.add_input("in0", variable="in0")
        self.add_input("in1", variable="in1")
        self.add_input("in2", variable="in2")
        self.add_output("out", variable="out")
        self.add_text_input('Equation3',placeholder_text='in0 * (in1 + in2)', width=self.equationWidth)
        self.setWidgetColors('Equation3', 'QLineEdit', PySide6.QtWidgets.QLineEdit, self.widgetStyle)

    def set_value(self, value):
        self.get_widget('Equation3').set_value(value)

    def get_value(self):
        return self.get_widget('Equation3').get_value()

    def setSimpleNodeName(self):
        self._view.name = "Three parameter equation"
        return False

class StaticValue(CustomBaseNode):
    __identifier__ = "nodes.virtualmodifiers"

    NODE_NAME = "Static value"

    def __init__(self):
        super(StaticValue, self).__init__()
        self.add_input("_trigger", painter_func=draw_triangle_port, variable="_trigger", valueType="trig")
        self.add_output("out", variable="out")
        self.add_text_input('value',placeholder_text='1', width=50)
        self.setWidgetColors('value', 'QLineEdit', PySide6.QtWidgets.QLineEdit, self.widgetStyle)
        text = self.get_widget('value')

    def set_value(self, value):
        self.value = value
        localWidget = self.get_widget('value')
        if (localWidget is not None): localWidget.set_value(value)

    def get_value(self):
        return self.value

    def buildNodeName(self, rootFromPort = "_trigger", endFromPort = "out", spacer = ""):
        return super().buildNodeName(rootFromPort, endFromPort)

    def findRootPort(self, portName = "_trigger"):
        return super().findRootPort(portName)

    def setSimpleNodeName(self):
        self._view.name = "Trigger static value"
        return False

class TriggerVariable(CustomBaseNode):
    __identifier__ = "nodes.virtualmodifiers"

    NODE_NAME = "Trigger variable"

    def __init__(self):
        super(TriggerVariable, self).__init__()
        self.add_input("Trigger", variable="_trigger", painter_func=draw_triangle_port)
        self.add_input("Variable", variable="variable")
        self.add_output("Out", variable="out")

class TriggerBool(CustomBaseNode):
    __identifier__ = "nodes.virtualmodifiers"

    NODE_NAME = "Trigger bool"

    def __init__(self):
        super(TriggerBool, self).__init__()
        self.add_input("Trigger False", variable="False", painter_func=draw_triangle_port, callsign="False")
        self.add_input("Trigger True", variable="True", painter_func=draw_triangle_port, callsign="True")
        self.add_output("Out", variable="out")
        self.toggleSwitch = ToggleSwitch(self.view)
        #self.toggleSwitch.customWidget.switch.setEnabled(False)
        self.value = False
        self.toggleSwitch.disable()
        self.add_custom_widget(self.toggleSwitch)

    def setTrigger(self):
        try:
            found = False
            in0 = list(self.get_input(0).model.connected_ports.items())
            for tup in in0:
                if (len(tup[1]) > 0):
                    found = True
                    break
            if (not found): in0 = None

            found = False
            in1 = list(self.get_input(1).model.connected_ports.items())
            for tup in in1:
                if (len(tup[1]) > 0):
                    found = True
                    break
            if (not found): in1 = None

            if ((in0 is not None) and (in1 is not None)):
                self.toggleSwitch.customWidget.switch.setEnabled(False)
                self.toggleSwitch.disable()
                pass
            else:
                self.toggleSwitch.customWidget.switch.setEnabled(False)
                self.toggleSwitch.enable()
                if ((in0 is not None)):
                    self.toggleSwitch.customWidget.switch.setChecked(False)
                    self.value = False
                elif ((in1 is not None)):
                    self.value = True
                    self.toggleSwitch.customWidget.switch.setChecked(True)
                else:
                    self.toggleSwitch.customWidget.switch.setEnabled(True)
            pass
        except:
            pass

    def findRootPort(self, portName = "Trigger False"):
        roots = super().findRootPort("Trigger False")
        roots += super().findRootPort("Trigger True")
        return roots

    def update(self):
        super().update()
        self.setTrigger()

    def set_value(self, value):
        self.value = value
        self.toggleSwitch.customWidget.switch.setChecked(value)

    def get_value(self):
        return self.value
# Modifiers

class Bool(CustomBaseNode):
    __identifier__ = "nodes.modifiers"

    NODE_NAME = "Make boolean"

    def __init__(self):
        super(Bool, self).__init__()
        self.add_input("in", variable="in0")
        self.add_input("_trigger", variable="_trigger", painter_func=draw_triangle_port, valueType="trig")
        self.add_output("out", variable="out")
        self.add_checkbox('Invert', text='Invert')
        self.setWidgetColors('Invert', 'QCheckBox', PySide6.QtWidgets.QCheckBox, self.widgetStyle)

    def set_value(self, value):
        self.value = value
        localWidget = self.get_widget('Invert')
        if (localWidget is not None): localWidget.set_value(value)

    def get_value(self):
        return self.value

    def buildNodeName(self, rootFromPort = "in", endFromPort = "out", spacer = ""):
        attempt = super().buildNodeName(rootFromPort, endFromPort)
        if (not attempt):
            attempt = super().buildNodeName("_trigger", endFromPort)
        return attempt

    def findRootPort(self, portName = "in"):
        return super().findRootPort(portName)

    def setSimpleNodeName(self):
        self._view.name = "Create bool from value"
        return False

class Deadband(CustomBaseNode):
    __identifier__ = "nodes.modifiers"

    NODE_NAME = "Deadband"

    def __init__(self):
        super(Deadband, self).__init__()
        self.add_input("value", variable="value")
        self.add_input("threshold", variable="threshold")
        self.add_output("out", variable="out")
        #self.add_text_input(name = "Threshold", width=50)
        self.thresholdWidget = LineEdit(self.view, label="Threshold", name="threshold")
        self.add_custom_widget(self.thresholdWidget)
        self.thresholdWidget.set_value("0")

    def buildNodeName(self, rootFromPort = "value", endFromPort = "out"):
        return super().buildNodeName(rootFromPort, endFromPort, "Deadband")

    def findRootPort(self, portName = "value"):
        return super().findRootPort(portName)

    def setSimpleNodeName(self):
        self._view.name = "Deadband with threshold"
        return False

    def set_value(self, value):
        self.value = value
        self.thresholdWidget.set_value(value)

    def get_value(self):
        return self.value

class Multiplexer(CustomBaseNode):
    __identifier__ = "nodes.modifiers"

    NODE_NAME = "Multiplexer"

    def __init__(self, outputs = 4):
        super(Multiplexer, self).__init__()
        self.add_input("select", variable="select")
        for outs in range(0, outputs):
            self.add_output("out" + str(outs), variable="out" + str(outs))

    def buildNodeName(self, rootFromPort = "select", endFromPort = "out0"):
        return super().buildNodeName(rootFromPort, endFromPort, "Multiplexer")

    def findRootPort(self, portName = "select"):
        return super().findRootPort(portName)

    def setSimpleNodeName(self):
        self._view.name = "Multiplexer"
        return False

class Map(CustomBaseNode):
    __identifier__ = "nodes.modifiers"

    NODE_NAME = "Map"

    def __init__(self, spinBoxes = 3):
        super(Map, self).__init__()
        self.add_input("in", variable="in")
        self.add_output("out", variable="out")
        #self.spinBoxArray = SpinBoxArray(12, self.view, label="Threshold", name="threshold")
        #self.add_custom_widget(self.spinBoxArray)
        self.tableView = TableView(12, self.view)
        self.add_custom_widget(self.tableView)

    def buildNodeName(self, rootFromPort = "in", endFromPort = "out"):
        return super().buildNodeName(rootFromPort, endFromPort, "Map")

    def findRootPort(self, portName = "in"):
        return super().findRootPort(portName)

    def setSimpleNodeName(self):
        self._view.name = "Map"
        return False

'''
# Hardware
class Solenoid(CustomBaseNode):
    __identifier__ = "nodes.hardware"

    NODE_NAME = "Solenoid"

    def __init__(self):
        super(Solenoid, self).__init__()
        self.view.widgetBackground = controlBackground
        self.add_input("Select", "s", "select", variable="select")
        self.add_input("Engage", "se", "bool", variable="engage")
        self.add_input("Duration", "sed", "uint16", variable="in0")
        self.add_input("Disengage", "sd", "bool")
        self.add_input("Multiplier", "sfm", "ratio")

class BowControl(CustomBaseNode):
    __identifier__ = "nodes.hardware"

    NODE_NAME = "Bow control"

    def __init__(self):
        super(BowControl, self).__init__()
        self.view.widgetBackground = controlBackground
        self.add_input("Select", "b", "select")
        self.add_input("Speed mode", "bcsm", "number")
        self.add_input("Timeout", "bmt", "uint16")
        self.add_input("PID On", "bpid", "bool")

        self.add_output("Motor fault", "bmfc", "commands")
        self.add_output("Bow over power", "bmopc", "commands")

        self.implicit = True

class HarmonicSeriesHandler(CustomBaseNode):
    __identifier__ = "nodes.hardware"

    NODE_NAME = "Harmonic series handler"

    def __init__(self):
        super(HarmonicSeriesHandler, self).__init__()
        self.view.widgetBackground = controlBackground
        self.add_input("Harmonic", "bch", "uint16")
        self.add_input("Harmonic add", "bcha", "uint16")
        self.add_input("Harmonic base", "bchb", "uint16")
        self.add_input("Harmonic shift", "bchsh", "uint16")
        self.add_input("Harmonic shift 5", "bchs5", "uint16")
        self.add_input("Base note", "bchbn", "uint16")
        self.add_input("Shift range", "bchsr", "uint16")

        self.add_output("Frequency", "", "float")

class BowMotor(CustomBaseNode):
    __identifier__ = "nodes.hardware"

    NODE_NAME = "Bow motor"

    def __init__(self):
        super(BowMotor, self).__init__()
        self.view.widgetBackground = controlBackground
        self.add_input("Run", "bmr", "bool")
        self.add_input("Direct PWM", "bmdp", "uint16")
        self.add_input("Voltage", "bmv", "float")

        self.add_input("Emergency stop", "bmes", "bool")

        self.implicit = True

class BowPID(CustomBaseNode):
    __identifier__ = "nodes.hardware"

    NODE_NAME = "Bow PID"

    def __init__(self):
        super(BowPID, self).__init__()
        self.view.widgetBackground = controlBackground
        self.add_input("kP", "bpkp", "float")
        self.add_input("kI", "bpki", "float")
        self.add_input("kD", "bpkd", "float")
        self.add_input("Integrator error", "bpie", "float")
        self.add_input("Max error", "bpme", "float")
        self.add_input("Reset", "bpir", "bool")
        self.add_input("Frequency", "bptf", "float")

        self.add_output("Direct PWM", "uint16")
        self.add_output("Peak error", "bpperr")

        self.implicit = True

class BowPressure(CustomBaseNode):
    __identifier__ = "nodes.hardware"

    NODE_NAME = "Bow pressure"

    def __init__(self):
        super(BowPressure, self).__init__()
        self.view.widgetBackground = controlBackground
        self.add_input("Baseline", "bpb", "uint16")
        self.add_input("Modifier", "bpm", "sint16")
        self.add_input("Engage", "bpe", "bool")
        self.add_input("Rest", "bpr", "bool")
        self.add_input("Hold", "bph", "bool")

class Mute(CustomBaseNode):
    __identifier__ = "nodes.hardware"

    NODE_NAME = "Mute"

    def __init__(self):
        super(Mute, self).__init__()
        self.view.widgetBackground = controlBackground
        self.add_input("Select", "m", "select")
        self.add_input("Position", "msp", "uint16")
        self.add_input("Full mute", "mfm", "bool")
        self.add_input("Half mute", "mhm", "bool")
        self.add_input("Rest", "mr", "bool")
        self.add_input("Sustain", "ms", "bool")
'''
class ControlBoxOutput(CustomBaseNode):
    __identifier__ = "nodes.hardware"

    NODE_NAME = "Control box output"

    def __init__(self):
        super(ControlBoxOutput, self).__init__()
        self.command = [CommandID.midiConfigurationData]
        self.argumentMatch = ["noteon"]
        self.view.widgetBackground = acmBackground
        self.source = True

        self.add_output("value")
        self.add_output("_trigger", painter_func=draw_triangle_port, valueType="trig")

# Misc

class Variables(CustomBaseNode):
    __identifier__ = "nodes.far"

    NODE_NAME = "Variables"

    def __init__(self):
        super(Variables, self).__init__()
        self.view.widgetBackground = variableBackground

        self.add_input("uv0", multi_input=True)
        self.add_output("uv0")
        self.add_input("uv1", multi_input=True)
        self.add_output("uv1")
        self.add_input("uv2", multi_input=True)
        self.add_output("uv2")
        self.add_input("uv3", multi_input=True)
        self.add_output("uv3")

        self.add_output("notecount")

        self.source = False


