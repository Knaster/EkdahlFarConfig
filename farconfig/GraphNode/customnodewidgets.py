from Qt import QtCore, QtWidgets
from PySide6.QtCore import Qt
from Qt import QtCore, QtWidgets

from NodeGraphQt.widgets.node_widgets import NodeBaseWidget
from NodeGraphQt.widgets.viewer_nav import NodeNavigationWidget
from NodeGraphQt.widgets.node_graph import SubGraphWidget
from Custom_Widgets import QCustomCheckBox

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QStandardItemModel, QStandardItem

class NodeSliderW(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NodeSliderW, self).__init__(parent)
        self.slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)

        self.slider.setMaximum(512)
        self.slider.setMinimum(0)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.slider)

class NodeSlider(NodeBaseWidget):
    def __init__(self, parent=None, name='', label='', text='', state=False):
        super(NodeSlider, self).__init__(parent, name, label)

        self.set_name('Slider')
        self.set_label('Ratio')

        self.set_custom_widget(NodeSliderW())

    @property
    def type_(self):
        return 'SliderNodeWidget'

    def wire_signals(self):
        print("wire signal")

    def on_btn_go_clicked(self):
        print('Clicked on node: "{}"'.format(self.node.name()))

    def get_value(self):
        return self.get_custom_widget().slider.value()

    def set_value(self, value):
        if type(value) is not int:
            return
        self.get_custom_widget().slider.setValue(value)

class ToggleSwitchW(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ToggleSwitchW, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.offText = QtWidgets.QLabel(self)
        self.offText.setText("False")
        layout.addWidget(self.offText)

        self.switch = QCustomCheckBox.QCustomCheckBox()
        self.switch.setFixedWidth(34)
        layout.addWidget(self.switch)

        self.onText = QtWidgets.QLabel(self)
        self.onText.setText("True")
        layout.addWidget(self.onText)

class ToggleSwitch(NodeBaseWidget):
    def __init__(self, parent=None, name='', label='', text='', state=False):
        super(ToggleSwitch, self).__init__(parent, name, label)

        self.set_name('Toggle switch')
        #self.set_label('Label')

        self.customWidget = ToggleSwitchW()
        self.set_custom_widget(self.customWidget)

        self.colorEnabledCircle = "#606060"
        self.colorEnabledBackgroundOff = "#ffd0d0"
        self.colorEnabledBackgroundOn = "#d0ffd0"
        self.colorEnabledTristate = "#c3c3c3"

        self.colorDisabledCircle = "#a3a3a3"
        self.colorDisabledBackgroundOff = "#a3a3a3"
        self.colorDisabledBackgroundOn = "#a3a3a3"

    def enable(self):
        self.customWidget.switch.customizeQCustomCheckBox(bgColor = self.colorEnabledBackgroundOff,
                                                          circleColor = self.colorEnabledCircle, activeColor = self.colorEnabledBackgroundOn)

    def disable(self):
        self.customWidget.switch.customizeQCustomCheckBox(bgColor = self.colorDisabledBackgroundOff,
                                                          circleColor = self.colorDisabledCircle, activeColor = self.colorDisabledBackgroundOn)

    @property
    def type_(self):
        return 'ToggleSwitchWidget'

    def wire_signals(self):
        print("wire signal")

    def on_btn_go_clicked(self):
        print('Clicked on node: "{}"'.format(self.node.name()))

    def get_value(self):
        return self.customWidget.switch.isChecked()

    def set_value(self, value):
        if (value == True):
            self.customWidget.switch.setChecked(True)
        else:
            self.customWidget.switch.setChecked(False)

    def get_name(self):
        return "ToggleSwitch"

class LineEditW(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LineEditW, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self.labelText = QtWidgets.QLabel(self)
        self.labelText.setText("Label")
        layout.addWidget(self.labelText)

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setFixedWidth(50)
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight)
        #self.lineEdit.setStyleSheet("QLineEdit { background-color: red; text-align: right; }")
        layout.addWidget(self.lineEdit)

class LineEdit(NodeBaseWidget):
    def __init__(self, parent=None, name='', label='', value="0"):
        super(LineEdit, self).__init__(parent, name, label)

        self.set_name('Custom Line Edit')
        self.customWidget = LineEditW()
        self.set_custom_widget(self.customWidget)

        self.customWidget.labelText.setText(label)
        if (label == ""):
            self.customWidget.labelText.hide()
        self.set_value(value)

    @property
    def type_(self):
        return 'CustomLineEditWidget'

    def get_value(self):
        return self.value

    def set_value(self, value):
        if (self.node is not None):
            self.node.properties()["custom"]["CustomLineEdit"] = value
            #a = self.node.properties()
            #b = a["custom"]
            #b["CustomLineEdit"] = value

        self.value = value
        self.customWidget.lineEdit.setText(value)
        if (value == ""):
            self.customWidget.labelText.hide()
        else:
            self.customWidget.labelText.show()

    def get_name(self):
        return "CustomLineEdit"

class SpinBoxArrayW(QtWidgets.QWidget):
    def __init__(self, spinBoxes = 12, parent = None):
        super(SpinBoxArrayW, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 20)

        self.label = []
        self.spinBox = []

        for box in range(0, spinBoxes):
            hLayout = QtWidgets.QVBoxLayout(self)

            label = QtWidgets.QLabel(self)
            label.setText(str(box))
            label.setAlignment(QtCore.Qt.AlignCenter)
            spinBox = QtWidgets.QSpinBox(self)

            hLayout.addWidget(label)
            hLayout.addWidget(spinBox)

            layout.addLayout(hLayout)

            self.label.append(label)
            self.spinBox.append(spinBox)

class SpinBoxArray(NodeBaseWidget):
    def __init__(self, spinBoxes = 12, parent = None, name = '', label = '', value = "0"):
        super(SpinBoxArray, self).__init__(parent, name, label)

        self.set_name('Spin box array')

        self.customWidget = SpinBoxArrayW(spinBoxes)
        self.set_custom_widget(self.customWidget)

        self.set_value(0)

    @property
    def type_(self):
        return 'SpinBoxArray'

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

class TableViewW(QtWidgets.QWidget):
    def __init__(self, dataPoints = 12, parent = None):
        super(TableViewW, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 20)

        self.tableView = QtWidgets.QTableView()
        self.tableView.setAutoScroll(False)

        model = QStandardItemModel()
        model.setRowCount(1)
        model.setColumnCount(dataPoints)

        for data in range(0, dataPoints):
            item = QStandardItem(0)
            model.setItem(0, 1, item)

        self.tableView.setModel(model)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.model = model

        layout.addWidget(self.tableView)

class TableView(NodeBaseWidget):
    def __init__(self, dataPoints = 12, parent = None, name = '', label = '', value = "0"):
        super(TableView, self).__init__(parent, name, label)

        self.set_name('Table view')

        self.customWidget = TableViewW(dataPoints)
        self.set_custom_widget(self.customWidget)

        self.set_value(0)

    @property
    def type_(self):
        return 'TableView'

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
