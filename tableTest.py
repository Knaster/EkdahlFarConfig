# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QDoubleSpinBox, QStyledItemDelegate

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
                header.append("Harmonic " + str(i - 1))
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
