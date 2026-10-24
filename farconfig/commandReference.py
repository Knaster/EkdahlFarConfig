from PySide6.QtWidgets import QWidget, QListWidgetItem, QTableView, QHeaderView, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from ui_reference import Ui_Form as commandReferenceWidget
from ModuleSystem import HelpModule, HelpCommand, ModuleHandler

class commandReference(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = commandReferenceWidget()
        self.ui.setupUi(self)
        self.ui.listWidgetCommands.setSortingEnabled(True)
        self.ui.listWidgetCommands.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.ui.listWidgetCommands.currentItemChanged.connect(self.listWidgetCommandsCurrentItemChanged)
    '''
    def addCommand(self, command, description):
        #commandItemHelp = QListWidgetItem()
        #commandItemHelp.setText(command)
        #commandItemHelp.description = description
        #self.ui.listWidgetCommands.addItem(commandItemHelp)
        cmd = QTreeWidgetItem(self.ui.listWidgetCommands)
        cmd.setText(0, command)
        cmd.setData(0, Qt.ItemDataRole.UserRole, description)


    def addCommandB(self, command, parent, shortHand, description):
        def addit():
            cmd.setText(0, command)
            cmd.setText(1, shortHand)
            cmd.setData(0, Qt.ItemDataRole.UserRole, description)

        if parent == "":
            if (self.ui.listWidgetCommands.findItems(command, Qt.MatchFlag.MatchExactly)):
                return
            cmd = QTreeWidgetItem(self.ui.listWidgetCommands)
        else:
            parentItem = self.ui.listWidgetCommands.findItems(parent, Qt.MatchFlag.MatchExactly or Qt.MatchFlag.MatchRecursive)
            if (len(parentItem) > 0):
                if (len(parentItem) > 1):
                    pass
                for parent in parentItem:
                    cmd = QTreeWidgetItem(parent)
                    addit()
            else:
                if (parent == "[base]"):
                    self.base = QTreeWidgetItem(self.ui.listWidgetCommands)
                    self.base.setText(0, "[base]")
                    cmd = QTreeWidgetItem(self.base)
                else:
                    cmd = QTreeWidgetItem(self.ui.listWidgetCommands)
        addit()
    '''

    def processHelpModule(self, helpModule:HelpModule, parent):
        for helpCommand in helpModule.commands:
            command = QTreeWidgetItem(parent)
            command.setText(0, helpCommand.longCommand)
            command.setData(0, Qt.ItemDataRole.UserRole, helpCommand)

        for helpModuleChild in helpModule.modules:
            module = QTreeWidgetItem(parent)
            module.setText(0, helpModuleChild.longName)
            module.setData(0, Qt.ItemDataRole.UserRole, helpModuleChild)
            self.processHelpModule(helpModuleChild, module)

    def buildReferenceFromHelpSystem(self, baseModule:ModuleHandler):
        self.processHelpModule(baseModule.helpModule, self.ui.listWidgetCommands)

    def listWidgetCommandsCurrentItemChanged(self, current, previous):
        self.ui.plainTextEditCMVDescription.clear()
        if current is not None:
            helpItem = current.data(0, Qt.ItemDataRole.UserRole)
            out2 = ""
            if isinstance(helpItem, HelpModule):
                longName = helpItem.longName
                shortName = helpItem.shortName
            elif isinstance(helpItem, HelpCommand):
                longName = helpItem.longCommand
                shortName = helpItem.shortCommand
                out2 = "<b>Arguments:</b> " + helpItem.arguments + "<br/><br/>"
                if len(helpItem.variables) > 0:
                    out2 += "<b>Variables:</b> "
                    for i in range(0, len(helpItem.variables)):
                        if i != 0: out2 += ", "
                        out2 += helpItem.variables[i]
                    out2 += "<br/><br/>"
                if helpItem.commandTypeVolatile:
                    out2 = "<font color='darkred'><b>!WARNING!</b> This item is marked as volatile, meaning that changing it could break the instrument if you don't know what you are doing!</font><br/>"

            out = "<b>Long name:</b> " + longName + "<br/>"
            out += "<b>Short name:</b> " + shortName + "<br/><br/>"
            out += "<b>Description:</b> " + helpItem.description + "<br/><br/>"
            out += out2
            self.ui.plainTextEditCMVDescription.setHtml(out)

    def clear(self):
        self.ui.listWidgetCommands.clear()