from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QComboBox, QListWidget
import math
from PySide6.QtGui import QColor

def stripLeadingQuotes(inp:str):
    if (len(inp) < 2): return inp
    if ((inp[0] == "'") or (inp[0] == "\"")) and ((inp[len(inp) - 1] == "'") or (inp[len(inp) - 1] == "\"")):
        inp = inp[1:len(inp)-1]
    return inp

def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())

def deleteLayout(widget, layoutType, delLayoutName, parentLayout):
    delLayout = widget.findChild(layoutType, name=delLayoutName, options=Qt.FindChildOption.FindChildrenRecursively)
    deleteItemsOfLayout(delLayout)
    parentLayout.removeItem(delLayout)

def messageBox(title, message):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(message)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(QMessageBox.Ok) # | QMessageBox.Cancel)

    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        pass

def inputBox(title, message, parent = None):
    text, ok = QInputDialog().getText(parent, title, message, QLineEdit.Normal)
    if ok and text:
        return text
    else:
        return None

def find_item(widget, item_text):
    if (isinstance(widget, QComboBox)):
        for index in range(widget.count()):
            if widget.itemText(index) == item_text:
                return index
    elif (isinstance(widget, QListWidget)):
        index = widget.findItems(item_text, Qt.MatchFlag.MatchExactly)
        if (len(index) == 0): return -1
        else:
            return index[0]
    return -1

def find_item_with_data(widget, item_data):
    if (isinstance(widget, QComboBox)):
        for index in range(widget.count()):
            if widget.itemData(index) == item_data:
                return index
    elif (isinstance(widget, QListWidget)):
        for index in range(0, widget.count()):
            item = widget.item(index)
            if (item.data(Qt.ItemDataRole.UserRole) == item_data):
                return index
    return -1

def remove_item(widget, item_text):
    index = widget.findItems(item_text, Qt.MatchFlag.MatchExactly)
    if (len(index) != 0):
        widget.takeItem(widget.row(index[0]))

def expGUIToModule(value, max):
    divisor = 65535 / math.log10(max)
    out = math.pow(10, (value / divisor)) - 0.999
    return out

def logModuleToGUI(value, max):
    value = float(value)
    if (value < 0): return 0
    divisor = 65535 / math.log10(max)
    return math.log10(value + 0.999) * divisor

# Every message contains two parts; the prefix type ("[dbg]" etc) and then the actual message
# The actual message can be of plain text type (for instance many [err] & [dbg] messages) or they can be
# command-type ([cmd] and [irq]) which has a command:result structure
#
# Messages needs to be able to be filtered entirely by prefix type (like ALL [irq] messages for instance),
# by command (all 'bw.paf' values for instance) or by a combination of prefix type and command
# (all [rqi] 'bw.pfa' values)

class dataVisibilitySettings():
    #show = None
    #uiReportFunction = Any
    #dataReportFunction = Any
    #prefixType = None
    #uiObject = None
    #moduleCommand:ModuleCommand = None
    #commandString:str = ""
    #color:QColor = QColor(127, 127, 127)

    def __init__(self, show:int, inIdentifier:str, inUIReportFunction = None, inDataReportFunction = None, inUIObject = None,
                 color:QColor = QColor(100, 100, 255), prefixType = "", moduleCommand = None, commandString:str = ""):
        self.show = show
        self.identifier = inIdentifier
        self.uiReportFunction = inUIReportFunction
        self.dataReportFunction = inDataReportFunction
        self.uiObject = inUIObject
        self.color = color
        self.prefixType:list[str] = []
        if isinstance(prefixType, str):
            self.prefixType += prefixType
        elif isinstance(prefixType, list):
            self.prefixType += prefixType
        self.moduleCommand = moduleCommand
        self.commandString = commandString

    def setShowUI(self, show):
        self.show = show
        if (self.dataReportFunction is not None): self.dataReportFunction(self)

    def setShowData(self, show):
        self.show = show
        if (self.uiReportFunction is not None): self.uiReportFunction(self)
