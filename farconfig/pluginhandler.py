from PySide6.QtWidgets import (QWidget, QComboBox, QSlider, QVBoxLayout, QSizePolicy, QLabel, QSpacerItem)
from PySide6.QtCore import Qt

from commandparser import getCommandIndex
from general_helpers import deleteItemsOfLayout, deleteLayout, inputBox, logModuleToGUI, expGUIToModule

from ModuleSystem import ModuleCommand

from GUICallbackSystem import GUICallbackSystem, GUICallback

from ui_plugin_ahdsr import Ui_Form_AHDSR as plugin_ahdsr
from ui_plugin_numbermap import Ui_Form_NumberMap as plugin_numbermap
from ui_plugin_lfo import Ui_Form_LFO as plugin_lfo
from ui_plugin_mult import Ui_Form_Mult as plugin_mult

from deprecated.commanddefinitions import CommandID
import CommandSets

class Plugin_Widget(QWidget):
    def __init__(self, plugin, index, pluginHandler, parent=None):
        super().__init__(parent)

        self.ui = plugin()
        self.ui.setupUi(self)
        self.index = index
        self.updatingFromModule = False
        self.pluginHandler = pluginHandler
        self.pluginTitle = ""

        self.guiCallbacks:list[GUICallback] = list()

        # Wrap the groupbox in a layout
        if hasattr(self.ui, 'mainLayout'):
            layout = self.ui.mainLayout
        else:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.ui.mainGroupBox)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def updateWidget(self):
        self.pluginHandler.guiCallbackSystem.setGUIObjectValueFromCallbacks(self.guiCallbacks)

    def updateName(self, command):
        name = command.arguments[0] if len(command.arguments) > 0 else None
        title = self.pluginTitle + " [" + str(self.index) + "]"
        if (name is not None): title += " - " + name
        self.ui.mainGroupBox.setTitle(title)

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        return

class Plugin_NumberMap(Plugin_Widget):
    def __init__(self, index, pluginHandler = None):
        super().__init__(plugin_numbermap, index, pluginHandler)
        self.ui.mainGroupBox.setTitle("Number map [" + str(index) + "]")
        self.range = 2
        self.oldRange = 2
        self.maps = {}
        self.ranges = [11, 127, 65535]
        self.steps = [1, 10, 1000]
        self.pluginTitle = "Number map"

        self.ui.sliderRange.valueChanged.connect(self.rangeChanged)
        self.guiCallbacks = [GUICallback(self.ui.sliderScale, "ph.nm[" + str(self.index) + "].sc"),
                             GUICallback(self.ui.textEditTarget, "ph.nm[" + str(self.index) + "].tg", dataIsCommandString = True),
                             GUICallback(None, "ph.nm[" + str(self.index) + "].na", dataCallbackFunction = self.updateName),
                             GUICallback(None, "ph.nm[" + str(self.index) + "].da", dataCallbackFunction = self.dataChangedMap),
                             GUICallback(self.ui.pushButtonAdd, "", guiCallbackFunction = self.addMap),
                             GUICallback(self.ui.pushButtonRemove, "", guiCallbackFunction = self.removeMap)]

        self.pluginHandler.guiCallbackSystem.addGUICallbacks(self.guiCallbacks)

    def addMap(self, anything = None):
        number = str(inputBox("Map number", "Map number", self))
        self.pluginHandler.serialHandler.write("ph.nm[" + str(self.index) + "].da:" + number + ":" + str(self.ranges[self.range]))

    def removeMap(self, anything = None):
        number = str(inputBox("Map number", "Map number", self))
        key = self.maps.pop(int(number), None)
        if (key is None): return
        deleteLayout(self.ui.layoutSliders.parentWidget(), QVBoxLayout, "number" + str(number), self.ui.layoutSliders)
        self.pluginHandler.serialHandler.write("ph.nm[" + str(self.index) + "].rm:" + number)

    def rangeChanged(self, value):
        self.range = value
        out = "ph.nm[" + str(self.index) + "].da"
        update = False
        for k in self.maps.keys():
            slider = self.ui.layoutSliders.parentWidget().findChild(QSlider, name="sliderValue" + str(k),
                                                                    options=Qt.FindChildOption.FindChildrenRecursively)
            slider.setMaximum(self.ranges[self.range])
            slider.setPageStep(self.steps[self.range])
            label = self.ui.layoutSliders.parentWidget().findChild(QLabel, name="labelValue" + str(k), options=Qt.FindChildOption.FindChildrenRecursively)
            label.setVisible((not (self.range == 2)))

            oldRange = int((self.ranges[self.oldRange] + 1))
            newRange = int(self.ranges[self.range] + 1)
            value = float(self.maps[k])
            value *= newRange
            value /= oldRange
            newValue = value
            if (self.range != self.oldRange):
                update = True
                self.maps[k] = newValue
                slider.setValue(newValue)
                self.updateLabel(int(k), str(round(newValue,0)))
                out += ":" + str(k) + ":" + str(round(newValue,0))

        if (update): self.pluginHandler.serialHandler.write(out);
        self.oldRange = self.range

    class customSlider(QSlider):
        def __init__(self, plugin):
            super().__init__()
            self.number = 0
            self.plugin = plugin

        def mouseReleaseEvent(self, ev, /):
            #mapDa = self.plugin.pluginHandler.commandSet.getQualifiedShortCommand(CommandID.pluginMapData, [self.plugin.index])[0]
            mapDa = "ph.nm[" + str(self.plugin.index) + "].da"
            self.plugin.pluginHandler.serialHandler.write(mapDa + ":" + str(self.number) + ":" + str(self.value()))
            super().mouseReleaseEvent(ev)

    def sliderValueChanged(self, value):
        self.updateLabel(self.sender().number, str(value))

    def addSlider(self, number, value):
        layout = QVBoxLayout()
        layout.setObjectName("number" + str(number))
        layout.number = number

        topLabel = QLabel(str(number))
        topLabel.setObjectName("labelNumber")
        topLabel.setAlignment(Qt.AlignCenter)
        topLabel.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        topLabel.setMaximumWidth(71)
        topLabel.setMinimumWidth(20)
        topLabel.setFixedHeight(17)

        slider = self.customSlider(self)
        slider.setObjectName("sliderValue" + str(number))
        slider.setMaximum(self.ranges[self.range])
        slider.setValue(int(value))
        slider.number = number
        slider.valueChanged.connect(self.sliderValueChanged)
        slider.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        slider.setMaximumWidth(71)
        slider.setMinimumWidth(20)
        slider.setMaximumHeight(95)
        slider.setFixedWidth(71)

        valueLabel = QLabel()
        valueLabel.setObjectName("labelValue" + str(number))
        valueLabel.setText(str(value))
        valueLabel.setAlignment(Qt.AlignCenter)
        valueLabel.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        valueLabel.setMaximumWidth(71)
        valueLabel.setMinimumWidth(20)
        valueLabel.setFixedHeight(17)
        if (self.range == 2): valueLabel.setVisible(False)

        layout.addWidget(topLabel)
        layout.addWidget(slider)
        layout.addWidget(valueLabel)

        self.ui.layoutSliders.addLayout(layout)

    def updateLabel(self, number, value = None):
        label = self.ui.layoutSliders.parentWidget().findChild(QLabel, name="labelValue" + str(number), options=Qt.FindChildOption.FindChildrenRecursively)
        if (label is None): return
        if (value is None): value = str(self.maps[number])
        label.setText(str(value))

    def updateSlider(self, number):
        slider = self.ui.layoutSliders.parentWidget().findChild(QSlider, name="sliderValue" + str(number), options=Qt.FindChildOption.FindChildrenRecursively)
        if (slider is None):
            return
        slider.setValue(self.maps[number])

    def renderSliders(self, sliderCountChanged):
        if (sliderCountChanged):
            for i in reversed(range(self.ui.layoutSliders.count())):
                if (not isinstance(self.ui.layoutSliders.itemAt(i), QSpacerItem)):
                    if ((self.ui.layoutSliders.itemAt(i).layout().objectName() != "layoutScale") and
                            (self.ui.layoutSliders.itemAt(i).layout().objectName() != "layoutRange")):
                        self.ui.layoutSliders.removeItem(self.ui.layoutSliders.itemAt(i))
                else:
                    self.ui.layoutSliders.removeItem(self.ui.layoutSliders.itemAt(i))

            for item in sorted(self.maps.keys()):
                self.addSlider(item, self.maps[item])
            self.rangeChanged(self.range)
        else:
            for item in sorted(self.maps.keys()):
                self.updateSlider(item)

        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.ui.layoutSliders.addItem(spacer)

    def dataChangedMap(self, command):
        ogCount = len(self.maps)
        i = 0
        while (i + 1 < len(command.arguments)):
            key = int(command.arguments[i].strip('\"').strip('\''))
            value = int(round(float(command.arguments[i + 1].strip('\"').strip('\'')), 0))
            self.maps[key] = value
            i += 2
        sliderCountChanged = False
        if (ogCount != len(self.maps)): sliderCountChanged = True
        self.renderSliders(sliderCountChanged)

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        return

class Plugin_AHDSR(Plugin_Widget):
    def __init__(self, index, pluginHandler = None):
        super().__init__(plugin_ahdsr, index, pluginHandler)
        self.ui.mainGroupBox.setTitle("AHDSR [" + str(index) + "]")
        self.pluginTitle = "AHDSR"

        self.guiCallbacks = [GUICallback(self.ui.dialAmplitude, "ph.ahdsr[" + str(self.index) + "].amp"),
                            GUICallback(self.ui.dialAttack, "ph.ahdsr[" + str(self.index) + "].at", dataCallbackFunction=self.dataChangedLog,
                                        guiCallbackFunction=self.guiChangedLog),
                            GUICallback(self.ui.dialHold, "ph.ahdsr[" + str(self.index)  + "].hd"),
                            GUICallback(self.ui.dialDecay, "ph.ahdsr[" + str(self.index) + "].dc", dataCallbackFunction=self.dataChangedLog,
                                        guiCallbackFunction=self.guiChangedLog),
                            GUICallback(self.ui.dialSustain, "ph.ahdsr[" + str(self.index) + "].su"),
                            GUICallback(self.ui.dialRelease, "ph.ahdsr[" + str(self.index) + "].re", dataCallbackFunction=self.dataChangedLog,
                                        guiCallbackFunction=self.guiChangedLog),
                            GUICallback(self.ui.checkBoxEnabled, "ph.ahdsr[" + str(self.index) + "].en"),
                            GUICallback(self.ui.checkBoxInverted, "ph.ahdsr[" + str(self.index) + "].inv"),
                            GUICallback(self.ui.textEditTarget, "ph.ahdsr[" + str(self.index) + "].tg", dataIsCommandString = True),
                            GUICallback(self.ui.textEditReleaseTarget, "ph.ahdsr[" + str(self.index) + "].rt", dataIsCommandString = True),
                            GUICallback(None, "ph.ahdsr[ " + str(self.index) + "].na", self.updateName)]

        self.pluginHandler.guiCallbackSystem.addGUICallbacks(self.guiCallbacks)

        self.updatingFromModule = True
        self.pluginHandler.mainWidget.updatingFromModule = True#

        self.pluginHandler.mainWidget.updatingFromModule = False
        self.updatingFromModule = False

        self.logUpdateList = { "attack" : self.ui.dialAttack, "decay" : self.ui.dialDecay, "release" : self.ui.dialRelease }

    def dataChangedLog(self, moduleCommand:ModuleCommand):
        if not moduleCommand.longCommand in self.logUpdateList: return
        value = logModuleToGUI(float(moduleCommand.arguments[0]), 65535)
        self.logUpdateList[moduleCommand.longCommand].setValue(value)

    def guiChangedLog(self, moduleCommand:ModuleCommand):
        if not moduleCommand.longCommand in self.logUpdateList: return
        value = expGUIToModule(float(self.logUpdateList[moduleCommand.longCommand].value()), 65535)
        self.pluginHandler.serialHandler.write(moduleCommand.getFullCommand() + ":" + str(value))

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        return

class Plugin_LFO(Plugin_Widget):
    def __init__(self, index, pluginHandler = None):
        super().__init__(plugin_lfo, index, pluginHandler)
        self.pluginTitle = "LFO"
        self.ui.mainGroupBox.setTitle("LFO [" + str(index) + "]")
        self.wave = { "saw" : 0, "triangle" : 1, "sine" : 2, "square" : 3, "random" : 4, 0 : "saw", 1 : "triangle", 2 : "sine", 3 : "square", 4 : "random"}

        self.guiCallbacks = [GUICallback(self.ui.dialDelay, "ph.lfo[" + str(self.index) + "].dl"),
                             GUICallback(self.ui.dialAmplitude, "ph.lfo[" + str(self.index) + "].amp"),
                             GUICallback(self.ui.dialFrequency, "ph.lfo[" + str(self.index) + "].fq", dataCallbackFunction = self.dataChangedLFOFrequency,
                                         guiCallbackFunction = self.guiChangedLFOFrequency),
                             GUICallback(self.ui.textEditTarget, "ph.lfo[" + str(self.index) + "].tg", dataIsCommandString = True),
                             GUICallback(self.ui.checkBoxBipolar, "ph.lfo[" + str(self.index) + "].bp"),
                             GUICallback(self.ui.checkBoxEnabled, "ph.lfo[" + str(self.index) + "].en"),
                             GUICallback(self.ui.labelDelayValue, "ph.lfo[" + str(self.index) + "].dl"),
                             GUICallback(self.ui.labelAmplitudeValue, "ph.lfo[" + str(self.index) + "].amp"),
                             GUICallback(self.ui.labelFrequencyValue, "ph.lfo[" + str(self.index) + "].fq", dataCallbackFunction = self.dataChangedLFOFrequency),
                             GUICallback(self.ui.sliderWaveform, "ph.lfo[" + str(self.index) + "].wf", dataCallbackFunction = self.dataChangedWaveformSlider,
                                         guiCallbackFunction = self.guiChangedWaveformSlider),
                             GUICallback(None, "ph.lfo[ " + str(self.index) + "].na", self.updateName)]

        self.pluginHandler.guiCallbackSystem.addGUICallbacks(self.guiCallbacks)

    def dataChangedLFOFrequency(self, command):
        value = logModuleToGUI(float(command.arguments[0]), 20)
        self.ui.dialFrequency.setValue(value)
        self.ui.labelFrequencyValue.setText(command.arguments[0])

    def guiChangedLFOFrequency(self, command):
        value = expGUIToModule(float(self.ui.dialFrequency.value()), 20)
        self.pluginHandler.serialHandler.write(command.getFullCommand() + ":" + str(value))

    def dataChangedWaveformSlider(self, command):
        self.ui.sliderWaveform.setValue(self.wave[command.arguments[0]])

    def guiChangedWaveformSlider(self, command):
        self.pluginHandler.serialHandler.write(command.getFullCommand() + ":" + self.wave[self.ui.sliderWaveform.value()])

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        return

class Plugin_Multiple(Plugin_Widget):
    def __init__(self, index, pluginHandler = None):
        super().__init__(plugin_mult, index, pluginHandler)
        self.pluginTitle = "Multiple"
        self.ui.mainGroupBox.setTitle("Multiple input mixer [" + str(index) + "]")

        self.guiCallbacks = [GUICallback(self.ui.textEditTarget, "ph.mult[" + str(self.index) + "].tg", dataIsCommandString = True),
                             GUICallback(None, "ph.mult[" + str(self.index) + "].da", dataCallbackFunction = self.updateLists),
                             GUICallback(self.ui.pushButtonRemoveAdder, None, dataCallbackFunction = self.removeAdder),
                             GUICallback(self.ui.pushButtonRemoveRatio, None, dataCallbackFunction = self.removeRatio)]

        self.pluginHandler.guiCallbackSystem.addGUICallbacks(self.guiCallbacks)

    def removeRatio(self):
        self.removeItem("ratio")

    def removeAdder(self):
        self.removeItem("adder")

    def removeItem(self, type):
        match(type):
            case "adder":
                qlist = self.ui.listAdders
            case "ratio":
                qlist = self.ui.listRatios
            case _:
                return
        items = qlist.selectedItems()
        if not items: return
        for item in items:
            self.pluginHandler.serialHandler.write("rm:" + type + ":" + item.text())
            qlist.takeItem(qlist.row(item))

    def updateLists(self, command): #, type, id, value):
        match(command.arguments[0]):
            case "adder":
                qlist = self.ui.listAdders
            case "ratio":
                qlist = self.ui.listRatios
            case _:
                return
        item = qlist.findItems(command.arguments[1], Qt.MatchFlag.MatchExactly)
        if (len(item) == 0): qlist.addItem(id)

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        return

class PluginHandler():
    def __init__(self, mainWidget, serialHandler, commandSet, guiCallbackSystem ):
        self.mainWidget = mainWidget
        self.commandSet: CommandSets.CommandSetModular = commandSet
        self.serialHandler = serialHandler
        self.plugins = []

        self.guiCallbackSystem:GUICallbackSystem = guiCallbackSystem

        mainWidget.ui.pushButtonPluginsAdd.pressed.connect(self.addPlugin)
        mainWidget.ui.pushButtonPluginsRemove.pressed.connect(self.removePlugin)
        mainWidget.ui.pushButtonPluginsName.pressed.connect(self.renamePlugin)

        mainWidget.ui.scrollPlugins.setWidgetResizable(True)
        mainWidget.ui.scrollAreaContentsPlugins.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        mainWidget.ui.verticalLayoutPlugins.setObjectName(u"verticalLayoutPlugins")
        mainWidget.ui.verticalLayoutPlugins.setContentsMargins(0, 0, 0, 0)

        mainWidget.ui.verticalLayoutPlugins.setAlignment(Qt.AlignmentFlag.AlignTop)
        mainWidget.ui.verticalLayoutPlugins.addStretch()

        if mainWidget.ui.scrollAreaContentsPlugins.layout() is None:
            mainWidget.ui.scrollAreaContentsPlugins.setLayout(QVBoxLayout())
            mainWidget.ui.scrollAreaContentsPlugins.layout().setContentsMargins(0, 0, 0, 0)

        self.pluginClasses = { "lfo" : Plugin_LFO, "ahdsr" : Plugin_AHDSR, "multiple" : Plugin_Multiple, "numbermap" : Plugin_NumberMap }

    def addGUICallbacks(self):
        self.guiCallbacks = [GUICallback(None, "ph.a", dataCallbackFunction = self.dataChangedAddPlugin),
                             GUICallback(None, "ph.rm", dataCallbackFunction = self.dataChangedRemovePlugin)]
        self.guiCallbackSystem.addGUICallbacks(self.guiCallbacks)

    def addPluginInternal(self, type, index):
        pluginList = self.mainWidget.ui.comboBoxPlugins
        pluginList.addItem(type + "[" + str(index) + "]")
        plugin = self.pluginClasses[type](index, self)

        if (plugin is not None):
            self.plugins.append(plugin)

            #Keep the spacer at the bottom to push widgets up
            position = self.mainWidget.ui.verticalLayoutPlugins.count()
            if (position > 0): position -= 1
            self.mainWidget.ui.verticalLayoutPlugins.insertWidget(position, plugin)

            plugin.updateWidget()
        return plugin

    def buildPluginList(self):
        self.clearAllPlugins()
        pluginList = self.mainWidget.ui.comboBoxPlugins
        ph = self.commandSet.baseModule.getModule("pluginhandler")
        for pluginGroup in ph.groups:
            pluginList.addItem(pluginGroup.longName + " - Add new")

        for group in ph.groups:
            for child in group.children:
                self.addPluginInternal(child.longName, child.getIndex())
        pass

    def clearAllPlugins(self):
        self.mainWidget.ui.comboBoxPlugins.clear()

        #Do not remove the spacer!
        for i in reversed(range(self.mainWidget.ui.verticalLayoutPlugins.count() - 1)):
            if (self.mainWidget.ui.verticalLayoutPlugins.itemAt(i).widget() is not None):
                self.mainWidget.ui.verticalLayoutPlugins.itemAt(i).widget().setParent(None)
            else:
                self.mainWidget.ui.verticalLayoutPlugins.removeItem(self.mainWidget.ui.verticalLayoutPlugins.itemAt(i))

    #[allow(dead_code)]
    def updateWidgets(self):
        for plugin in self.plugins:
            plugin.updateWidget()
        pass

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        for plugin in self.plugins:
            plugin.processMessages(commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler)

    def isSelectionPluginInstance(self):
        combo:QComboBox = self.mainWidget.ui.comboBoxPlugins
        index = combo.currentIndex()
        if (index == -1): return False
        dash = str(combo.currentText()).find("-")
        if dash != -1: return False
        return True

    def getPlugin(self, type, index) -> QWidget:
        for plugin in self.plugins:
            if ((plugin.index == index) and (isinstance(plugin, self.pluginClasses[type]))):
                return plugin
        return None

    def getPluginType(self):
        combo:QComboBox = self.mainWidget.ui.comboBoxPlugins
        index = combo.currentIndex()
        if (index == -1): return False
        dash = str(combo.currentText()).find("-")
        if dash == -1: return ""
        return combo.currentText()[:dash - 1]

    def getPluginTypeAndIndex(self):
        combo:QComboBox = self.mainWidget.ui.comboBoxPlugins
        type = combo.currentText()
        dash = type.find("[")
        index = int(type[dash + 1:len(type) - 1])
        type = type[:dash]
        return type, index

    #[allow(dead_code)]
    def getPluginTypeCount(self, type):
        count = 0
        for plug in self.plugins:
            if isinstance(plug, self.pluginClasses[type]): count += 1
        return count

    def dataChangedAddPlugin(self, command):
        if (command.arguments is None) or  (len(command.arguments) == 0): return
        type = command.arguments[0]
        index = int(command.arguments[1])
        plugin = self.addPluginInternal(type, index)
        if (plugin is None): return

    def addPlugin(self):
        if (self.isSelectionPluginInstance()): return
        type = self.getPluginType()
        self.serialHandler.write("ph.a:" + type)

    def dataChangedRemovePlugin(self, command):
        if (command.arguments is None) or (len(command.arguments) < 2): return
        type, index = self.getPluginTypeAndIndex()
        plugin = self.getPlugin(type, index)
        if (plugin is not None):
            deleteItemsOfLayout(plugin.layout())
            plugin.parent().children().remove(plugin)
            plugin.setParent(None)
        pluginList = self.mainWidget.ui.comboBoxPlugins
        pluginList.removeItem(pluginList.currentIndex())

    def removePlugin(self):
        if (not self.isSelectionPluginInstance()): return
        type, index = self.getPluginTypeAndIndex()
        self.serialHandler.write("ph.rm:" + type + ":" + str(index))

    def renamePlugin(self):
        if (not self.isSelectionPluginInstance()): return
        type, index = self.getPluginTypeAndIndex()
        newName = str(inputBox("New name", "New name", self.mainWidget))
        self.serialHandler.write("ph." + type + "[" + str(index) + "].name:" + newName)
