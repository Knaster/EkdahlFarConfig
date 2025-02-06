#
#  This file is part of The Ekdahl FAR firmware.
#
#  The Ekdahl FAR firmware is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  The Ekdahl FAR firmware is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with The Ekdahl FAR firmware. If not, see <https://www.gnu.org/licenses/>.
#
# Copyright (C) 2024 Karl Ekdahl
#

# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import QColor, QKeyEvent
from PySide6.QtWidgets import QDoubleSpinBox, QStyledItemDelegate, QTableView, QLineEdit, QApplication

class customTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Up:
            index = self.selectionModel().currentIndex()
            self.model().setData(index, float(index.data()) + 0.0001)
        elif event.key() == Qt.Key.Key_Down:
            index = self.selectionModel().currentIndex()
            self.model().setData(index, float(index.data()) - 0.0001)
        elif event.key() == Qt.Key.Key_PageUp:
            index = self.selectionModel().currentIndex()
            self.model().setData(index, float(index.data()) + 0.001)
        elif event.key() == Qt.Key.Key_PageDown:
            index = self.selectionModel().currentIndex()
            self.model().setData(index, float(index.data()) - 0.001)
        elif event.modifiers() in [Qt.ControlModifier, Qt.MetaModifier]:
            if event.key() == Qt.Key.Key_C:
                self.copy()
            elif event.key() == Qt.Key.Key_V:
                self.paste()
        else:
        # Call the parent class to handle normal key press events
            super().keyPressEvent(event)

    def copy(self):
        # Get selected indexes
        selected_indexes = self.selectedIndexes()
        if not selected_indexes:
            return

        # Create a list to store the copied data
        copied_data = []
        for index in selected_indexes:
            if index.isValid():
                copied_data.append(self.model().data(index, Qt.DisplayRole))

        # Convert the copied data into a format suitable for the clipboard (CSV-like)
        clipboard_content = '\n'.join([','.join(copied_data[i:i + self.model().columnCount()])
                                      for i in range(0, len(copied_data), self.model().columnCount())])

        # Copy to the clipboard
        clipboard = QApplication.clipboard()
        #clipboard.setText(clipboard_content)
        clipboard.setText(self.selectionModel().currentIndex().data())

    def paste(self):
        # Get the clipboard content
        clipboard = QApplication.clipboard()
        clipboard_content = clipboard.text()

        self.model().setData(self.selectionModel().currentIndex(), float(clipboard_content))
        return

        # Split the clipboard content by lines and cells
        rows = clipboard_content.split('\n')
        for row_idx, row in enumerate(rows):
            cells = row.split(',')
            for col_idx, cell in enumerate(cells):
                index = self.model().index(row_idx, col_idx)
                if index.isValid():
                    self.model().setData(index, cell.strip(), Qt.EditRole)


class CustomTableModel(QAbstractTableModel):
#    dataChanged = Signal(str)

    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        if data == None:
            return
        self.load_data(data)

    def load_data(self, data):
        self.dataset = data
        self.column_count = len(self.dataset)
        self.row_count = 1 #len(self.dataset)

    def rowCount(self, parent=QModelIndex()):
        try:
            return self.row_count
        except:
            return 0

    def columnCount(self, parent=QModelIndex()):
        try:
            return self.column_count
        except:
            return 0

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            header = []
            for i in range(1, len(self.dataset) + 1):
                header.append("" + str(i - 1))
            return (header)[section]
        else:
            return
        #"{}".format(section)

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()

        if role == Qt.DisplayRole:
            return self.dataset[column]
        elif role == Qt.EditRole:
            return self.dataset[column]
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None

    def setData (self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self.dataset[index.column()] = value
            print("Index " + str(self.index(0,index.column()).column()) + " data " + str(self.index(0,index.column()).data()))
            self.dataChanged.emit(self.index(0,index.column()), self.index(0,index.column()), role)
        return True

    def setDataNR(self, column, value):
        self.dataset[column] = value
        self.dataChanged.emit(self.index(0,column), self.index(0,column), Qt.EditRole)
        return

    def flags (self, index):
        return Qt.ItemIsEditable | QAbstractTableModel.flags(self, index)

class SpinBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.index = None

    def createEditor(self, parent, option, index):
        editor = QDoubleSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(1)
        editor.setMaximum(2)
        editor.setSingleStep(0.001)
        editor.setAccelerated(True)
        editor.setDecimals(4)
        editor.valueChanged.connect(self.delValueChanged)
        self.index = index
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        self.index = index
        editor.setValue(float(value))

    def setModelData(self, editor, model, index):
        editor.interpretText()
        value = editor.value()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def delValueChanged(self, value):
        print(str(self.index) + ":" + str(value))
        self.index.model().setData(self.index, value, Qt.EditRole)
        pass

class noneDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        # Always use a QLineEdit for editing, regardless of the cell content type
        editor = QLineEdit(parent)
        editor.setAlignment(Qt.AlignRight)  # Align text to the right for numeric-like input
        return editor

    def setEditorData(self, editor, index):
        # Set the text data when the editor is created (this will be the current cell value)
        if editor:
            value = index.model().data(index, Qt.DisplayRole)
            editor.setText(str(value))

    def setModelData(self, editor, model, index):
        # Update the model with the new value from the editor (text input)
        if editor:
            value = editor.text()
            model.setData(index, value, Qt.EditRole)
