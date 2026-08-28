from NodeGraphQt.nodes.group_node import GroupNode, GroupNodeItem
from NodeGraphQt import SubGraph, NodeGraph, Port
from NodeGraphQt.nodes.port_node import PortInputNode, PortOutputNode, PortInputNodeItem, PortOutputNodeItem
from GraphNode.nodeorganizer import NodeOrganizer

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QGraphicsTextItem

import copy

from .customnode import CustomBaseNode, CustomNodeItem

groupBackground = QtGui.QColor(255,200,200)

class CustomGroupNodeItem(CustomNodeItem):
    """
    Group Node item.

    Args:
        name (str): name displayed on the node.
        parent (QtWidgets.QGraphicsItem): parent item.
    """

    def __init__(self, name='group', parent=None):
        super(CustomGroupNodeItem, self).__init__(name, parent)


    def mouseDoubleClickEvent(self, event):
        if (self.node is not None):
            self.node.expand()

    def add_input(self, name='input', multi_port=False, display_name=True,
                  locked=False, painter_func=None):
        item = super().add_input(name, multi_port, display_name, locked, painter_func)

        portText:QGraphicsTextItem = self.get_input_text_item(item)
        portText.setHtml("<div style='text-align:left; color:black;'>" + name + "</div>")
        return item

    def add_output(self, name='input', multi_port=False, display_name=True,
                  locked=False, painter_func=None):
        item = super().add_output(name, multi_port, display_name, locked, painter_func)

        portText:QGraphicsTextItem = self.get_output_text_item(item)
        portText.setHtml("<div style='text-align:right; color:black;'>" + name + "</div>")
        return item


class CustomGroupNode(GroupNode, CustomBaseNode):
    """
    example test group node with a in port and out port.
    """

    # set a unique node identifier.
    __identifier__ = 'nodes.group'

    # set the initial default node name.
    NODE_NAME = 'custom group node'

    def __init__(self, qgraphics_item=None):
        #Custom
        super(CustomGroupNode, self).__init__(qgraphics_item or CustomGroupNodeItem)
        self.view.widgetBackground = groupBackground
        self.view.node = self

        self._input_port_nodes = {}
        self._output_port_nodes = {}

    def migrate_objects(self):
        sub_graph:CustomSubGraph = self.get_sub_graph()
        if (sub_graph is None):
            sub_graph = self.graph.createSubGraph(self)

        copyThis = []
        for node in self.graph.all_nodes():
            if (not "group" in node.type_):
                copyThis.append(node)
            else:
                pass
        self.graph.copy_nodes(copyThis)
        sub_graph.paste_nodes()

        for node in sub_graph.all_nodes():
            try:
                if (node.source == True) or (node.NODE_NAME == "Map"):
                    for port in node.connected_output_nodes():
                        if (len(port.connected_ports()) > 0):
                            newInputName = node.NODE_NAME + ":" + port.name()
                            groupPort = self.add_input(newInputName, True)

                            subNode = sub_graph.get_node_by_name(newInputName)
                            subPort:Port = subNode.get_output(0)

                            originalSource:CustomBaseNode = self.graph.get_node_by_name(node.name())

                            for connection in port.connected_ports():
                                subPort.connect_to(connection)
                                sourcePort = originalSource.get_output(port.name())
                                groupPort.connect_to(sourcePort)

                    sub_graph.remove_node(node)
            except Exception as e:
                pass
        for node in copyThis:
            try:
                if (node.source == False) and (node.NODE_NAME != "Map"):
                    self.graph.remove_node(node)
            except Exception as e:
                pass

        self.get_sub_graph().nodeOrganizer.buildHorizontalTree()

colorPortNodeSelect = QtGui.QColor(180,200,50)
colorPortNodeDeselect = QtGui.QColor(255,255,255)

class CustomPortInputNodeItem: #(PortInputNodeItem):
    def __init__(self, original:PortInputNodeItem): # name='group port', parent=None):
        #super(CustomPortInputNodeItem, self).__init__(name, parent)
        #self.__dict__ = original.__dict__
        self._original = original
        #super(CustomPortInputNodeItem).__init__(original.name, original.parentObject())

    def __getattr__(self, name):
        return getattr(self._original, name)

    def paint(self, painter, option, widget):
        self.auto_switch_mode()

        painter.save()
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)

        margin = 2.0
        rect = self.boundingRect()
        rect = QtCore.QRectF(rect.left() + margin,
                             rect.top() + margin,
                             rect.width() - (margin * 2),
                             rect.height() - (margin * 2))

        text_rect = self._text_item.boundingRect()
        text_rect = QtCore.QRectF(
            rect.center().x() - (text_rect.width() / 2) - 5,
            rect.center().y() - (text_rect.height() / 2),
            text_rect.width() + 10,
            text_rect.height()
        )

        painter.setBrush(QtGui.QColor(255, 0, 0, 20))
        if self.selected:
            painter.setPen(QtGui.QPen(colorPortNodeSelect, 1.3))
        painter.drawRoundedRect(rect, 20, 20)

        painter.setBrush(QtGui.QColor(0, 0, 0, 100))
        painter.drawRoundedRect(text_rect, 3, 3)

        size = int(rect.height() / 4)
        triangle = QtGui.QPolygonF()
        triangle.append(QtCore.QPointF(-size, size))
        triangle.append(QtCore.QPointF(0.0, 0.0))
        triangle.append(QtCore.QPointF(size, size))

        transform = QtGui.QTransform()
        transform.translate(rect.width() - (size / 6), rect.center().y())
        transform.rotate(90)
        poly = transform.map(triangle)

#        if self.selected:
#            pen = QtGui.QPen(colorPortNodeSelect, 1.3)
#            painter.setBrush(colorPortNodeSelect)
#        else:
        pen = QtGui.QPen(colorPortNodeDeselect, 1.2)
        painter.setBrush(QtGui.QColor(0, 0, 0, 50))

        pen.setJoinStyle(QtCore.Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)
        painter.drawPolygon(poly)

        edge_size = 30
        edge_rect = QtCore.QRectF(rect.width() - (size * 1.7),
                                  rect.center().y() - (edge_size / 2),
                                  4, edge_size)
        painter.drawRect(edge_rect)

        painter.restore()

class CustomPortOutputNodeItem: #(PortOutputNodeItem):
    def __init__(self, original): #name='group port', parent=None):
        #super(CustomPortOutputNodeItem, self).__init__(name, parent)
        #self.__dict__ = original.__dict__
        self._original = original
        #super(CustomPortOutputNodeItem).__init__(original.name, original.parentObject())

    def __getattr__(self, name):
        return getattr(self._original, name)

    def paint(self, painter, option, widget):
        self.auto_switch_mode()

        painter.save()
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)

        margin = 2.0
        rect = self.boundingRect()
        rect = QtCore.QRectF(rect.left() + margin,
                             rect.top() + margin,
                             rect.width() - (margin * 2),
                             rect.height() - (margin * 2))

        text_rect = self._text_item.boundingRect()
        text_rect = QtCore.QRectF(
            rect.center().x() - (text_rect.width() / 2) - 5,
            rect.center().y() - (text_rect.height() / 2),
            text_rect.width() + 10,
            text_rect.height()
        )

        painter.setBrush(QtGui.QColor(255, 0, 0, 20))
        if self.selected:
            painter.setPen(QtGui.QPen(colorPortNodeSelect, 1.3))
        painter.drawRoundedRect(rect, 20, 20)

        painter.setBrush(QtGui.QColor(0, 0, 0, 100))
        painter.drawRoundedRect(text_rect, 3, 3)

        size = int(rect.height() / 4)
        triangle = QtGui.QPolygonF()
        triangle.append(QtCore.QPointF(-size, size))
        triangle.append(QtCore.QPointF(0.0, 0.0))
        triangle.append(QtCore.QPointF(size, size))

        transform = QtGui.QTransform()
        transform.translate(rect.x() + (size / 3), rect.center().y())
        transform.rotate(-90)
        poly = transform.map(triangle)

#        if self.selected:
#            pen = QtGui.QPen(colorPortNodeSelect, 1.3)
#            painter.setBrush(colorPortNodeSelect)
#        else:
        pen = QtGui.QPen(colorPortNodeDeselect, 1.2)
        painter.setBrush(QtGui.QColor(0, 0, 0, 50))

        pen.setJoinStyle(QtCore.Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)
        painter.drawPolygon(poly)

        edge_size = 30
        edge_rect = QtCore.QRectF(rect.x() + (size * 1.6),
                                  rect.center().y() - (edge_size / 2),
                                  4, edge_size)
        painter.drawRect(edge_rect)

        painter.restore()

class CustomSubGraph(SubGraph):
    def __init__(self, parent=None, node=None, node_factory=None, **kwargs):
        super(CustomSubGraph, self).__init__(parent, node, node_factory, **kwargs)
        self.set_grid_mode(0)
        self.set_background_color(255,255,255)
        self.nodeOrganizer = NodeOrganizer(self)

        #self.navigation_widget.setStyleSheet("QListView { border: 1px solid rgb(200,200,200); background-color:rgb(255,255,255); color: rgb(50,50,50) }"
        #                                     "QListView::Item { background-color: rgb(240,240,240); color: rgb(200, 200, 200); ")

    # This is where the main subgraph nodes that connects to the outer world are added
    def add_node(self, node, pos=None, selected=True, push_undo=True, inherite_graph_style=True):

        if isinstance(node._view, PortInputNodeItem):
            node._view.paint = CustomPortInputNodeItem(node._view).paint
        if isinstance(node._view, PortOutputNodeItem):
            node._view.paint = CustomPortOutputNodeItem(node._view).paint

        super().add_node(node, pos, selected, push_undo, inherite_graph_style)

        pass


class CustomNodeGraph(NodeGraph):
    default_node_color = "#000000"
    default_node_background = (210, 210, 210)
    default_wrap_background = (30, 30, 30)

    def __init__(self):
        super().__init__()
        self.nodeOrganizer = NodeOrganizer(self)
        #overrides any other styles set, may not be great
        self.widget.setStyleSheet("border: none")

    def expand_group_node(self, node):
        if not isinstance(node, CustomGroupNode):return
        if self._widget is None: raise RuntimeError('NodeGraph.widget not initialized!')

        self.viewer().clear_key_state()
        self.viewer().clearFocus()

        if node.id in self._sub_graphs:
            sub_graph = self._sub_graphs[node.id]
            tab_index = self._widget.indexOf(sub_graph.widget)
            self._widget.setCurrentIndex(tab_index)
            return sub_graph

        return self.createSubGraph(node)

    def createSubGraph(self, node):
        # build new sub graph.
        node_factory = copy.deepcopy(self.node_factory)
        layout_direction = self.layout_direction()
        kwargs = { 'layout_direction': self.layout_direction(), 'pipe_style': self.pipe_style(), }
        sub_graph = CustomSubGraph(self, node=node, node_factory=node_factory, **kwargs)

        # populate the sub graph.
        session = node.get_sub_graph_session()
        sub_graph.deserialize_session(session)

        # store reference to expanded.
        self._sub_graphs[node.id] = sub_graph

        # open new tab at root level.
        self._widget.setStyleSheet("QTabBar::tab { background:rgb(255,255,255); border:0px solid black; color:rgb(200,200,200); height: 30px;  width:200px;} "
                                   "QTabBar::tab:selected { color:rgb(0,0,0); background:rgb(200,200,200); border-top:1px solid rgb(100,100,100); } "
                                   "QTabBar::tab:hover { color:rgb(128,128,128); border-top:1px solid rgb(100,100,100); } "
                                   "QSpinBox { color:rgb(226,226,226); background-color:rgb(225,225,225); min-width:30px; padding-right:20px; } "
                                   "QSpinBox QLineEdit { min-width:20px;}")

        sub_graph.widget._layout.removeWidget(sub_graph.widget.navigator)

        self.widget.add_viewer(sub_graph.widget, node.name(), node.id)
        return sub_graph

    def create_node(self, node_type, name=None, selected=True, color=None,
                    text_color=None, pos=None, push_undo=True):

        if (text_color is None): text_color = self.default_node_color
        node = super().create_node(node_type, name, selected, color, text_color, pos, push_undo)
        node.set_color(self.default_node_background[0],self.default_node_background[1],self.default_node_background[2])
        return node

