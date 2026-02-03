from PySide6.QtWidgets import QWidget, QListWidgetItem, QTableView, QHeaderView, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from ui_reference import Ui_Form as commandReferenceWidget

class commandReference(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = commandReferenceWidget()
        self.ui.setupUi(self)
        self.ui.listWidgetCommands.setSortingEnabled(True)
        self.ui.listWidgetCommands.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.ui.listWidgetCommands.currentItemChanged.connect(self.listWidgetCommandsCurrentItemChanged)

    def addCommand(self, command, description):
        commandItemHelp = QListWidgetItem()
        commandItemHelp.setText(command)
        commandItemHelp.description = description
        self.ui.listWidgetCommands.addItem(commandItemHelp)

    def addCommandB(self, command, parent, shortHand, description):
        if parent == "":
            cmd = QTreeWidgetItem(self.ui.listWidgetCommands)
        else:
            parentItem = self.ui.listWidgetCommands.findItems(parent, Qt.MatchFlag.MatchExactly or Qt.MatchFlag.MatchRecursive)
            if (len(parentItem) == 1):
                cmd = QTreeWidgetItem(parentItem[0])
            elif (len(parentItem) > 1):
                pass
            else:
                if (parent == "[base]"):
                    self.base = QTreeWidgetItem(self.ui.listWidgetCommands)
                    self.base.setText(0, "[base]")
                    cmd = QTreeWidgetItem(self.base)
                else:
                    cmd = QTreeWidgetItem(self.ui.listWidgetCommands)
        cmd.setText(0, command)
        cmd.setText(1, shortHand)
        cmd.setData(0, Qt.ItemDataRole.UserRole, description)

    def listWidgetCommandsCurrentItemChanged(self, current, previous):
        self.ui.plainTextEditCMVDescription.clear()
        if current is not None:
            self.ui.plainTextEditCMVDescription.insertPlainText(current.data(0, Qt.ItemDataRole.UserRole))

    def clear(self):
        self.ui.listWidgetCommands.clear()