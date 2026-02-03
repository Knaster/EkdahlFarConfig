from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QComboBox, QListWidget

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

def remove_item(widget, item_text):
    index = widget.findItems(item_text, Qt.MatchFlag.MatchExactly)
    if (len(index) != 0):
        widget.takeItem(widget.row(index[0]))
