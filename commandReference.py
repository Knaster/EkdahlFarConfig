from PySide6.QtWidgets import QWidget, QListWidgetItem, QTableView, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from ui_reference import Ui_Form as commandReferenceWidget

class commandReference(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = commandReferenceWidget()
        self.ui.setupUi(self)

        self.ui.listWidgetCommands.setSortingEnabled(True)
        self.ui.listWidgetCommands.currentItemChanged.connect(self.listWidgetCommandsCurrentItemChanged)
#        self.model = QStandardItemModel()
#        self.model.setHorizontalHeaderLabels(["Command", "Short", "Scope", "Parameters", "Description"])
#        self.ui.tableViewReference.setModel(self.model)
#        self.ui.tableViewReference.horizontalHeader().setStretchLastSection(True)

#    def add_row(self, row_data):
#        row_items = [QStandardItem(str(data)) for data in row_data]
#        self.model.appendRow(row_items)

    def addCommand(self, command, description):
        commandItemHelp = QListWidgetItem()
        commandItemHelp.setText(command)
        commandItemHelp.description = description
        self.ui.listWidgetCommands.addItem(commandItemHelp)

    def listWidgetCommandsCurrentItemChanged(self, current, previous):
        self.ui.plainTextEditCMVDescription.clear()
        if current is not None:
            self.ui.plainTextEditCMVDescription.insertPlainText(current.description)

    def clear(self):
        self.ui.listWidgetCommands.clear()