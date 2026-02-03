from PySide6.QtWidgets import (QWidget, QLineEdit,
                               QComboBox, QSlider, QVBoxLayout, QCheckBox, QSizePolicy, QLabel, QSpacerItem)
from PySide6.QtCore import Qt

from commandparser import getCommandIndex
from general_helpers import deleteItemsOfLayout, deleteLayout, inputBox

from ui_plugin_ahdsr import Ui_Form_AHDSR as plugin_ahdsr
from ui_plugin_numbermap import Ui_Form_NumberMap as plugin_numbermap
from ui_plugin_lfo import Ui_Form_LFO as plugin_lfo
from ui_plugin_mult import Ui_Form_Mult as plugin_mult

from commanddefinitions import CommandID
import CommandSets

class Plugin_Widget(QWidget):
    def __init__(self, plugin, index, pluginHandler, parent=None):
        super().__init__(parent)

        self.ui = plugin()
        self.ui.setupUi(self)
        self.index = index
        self.updatingFromModule = False
        self.pluginHandler = pluginHandler

        # Wrap the groupbox in a layout
        if hasattr(self.ui, 'mainLayout'):
            layout = self.ui.mainLayout
        else:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.ui.mainGroupBox)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def updateValueAndLabel(self, commandID, valueWidget, label = None, log = False, logMax = 65535):
        value = self.pluginHandler.simpleFARHandler.stringModules[0].getCommandValue(commandID, self.index)
        if isinstance(valueWidget, QLineEdit):
            valueWidget.setText(str(value))
        elif isinstance(valueWidget, QCheckBox):
            if (value):
                valueWidget.setChecked(True)
            else:
                valueWidget.setChecked(False)
        else:
            if (log):
                valueWidget.setValue(self.pluginHandler.mainWidget.logModuleToGUI(value, logMax))
            else:
                valueWidget.setValue(value)

        if (label is not None):
            label.setText(str(value))

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        if (getCommandIndex(commandItem) != self.index): return
        pass

class Plugin_NumberMap(Plugin_Widget):
    def __init__(self, index, pluginHandler = None):
        super().__init__(plugin_numbermap, index, pluginHandler)
        self.ui.mainGroupBox.setTitle("Number map [" + str(index) + "]")
        self.range = 2
        self.oldRange = 2
        self.maps = {}
        self.ranges = [11, 127, 65535]
        self.steps = [1, 10, 1000]
        self.ui.sliderRange.valueChanged.connect(self.rangeChanged)
        self.pluginHandler.assignValueChanged(self.ui.sliderScale, CommandID.pluginMapScale, [index])
        self.pluginHandler.assignValueChanged(self.ui.textEditTarget, CommandID.pluginMapTarget, [index])
        self.ui.pushButtonAdd.pressed.connect(self.addMap)
        self.ui.pushButtonRemove.pressed.connect(self.removeMap)

        self.requestData = [CommandID.pluginMapData, CommandID.pluginMapName, CommandID.pluginMapScale,
                            CommandID.pluginMapTarget]

    def updateWidget(self, simpleFARHandler):
        self.updatingFromModule = True
        self.updateValueAndLabel(CommandID.pluginMapScale, self.ui.sliderScale, None)
        self.ui.sliderRange = self.range
        name = simpleFARHandler.stringModules[0].getCommandValue(CommandID.pluginMapName)
        if (name != -1):
            self.ui.mainGroupBox.setTitle("Number map [" + str(self.index) + "] - " + name)
        self.updatingFromModule = False

    def addMap(self):
        number = str(inputBox("Map number", "Map number", self))
        mapDa = self.pluginHandler.commandSet.getQualifiedShortCommand(CommandID.pluginMapData, [self.index])[0]
        self.pluginHandler.serialHandler.write(mapDa + ":" + number + ":" + str(self.ranges[self.range]))

    def removeMap(self):
        number = str(inputBox("Map number", "Map number", self))
        key = self.maps.pop(int(number), None)
        if (key is None): return
        deleteLayout(self.ui.layoutSliders.parentWidget(), QVBoxLayout, "number" + str(number), self.ui.layoutSliders)
        mapRm = self.pluginHandler.commandSet.getQualifiedShortCommand(CommandID.pluginMapRemove, [self.index])[0]
        self.pluginHandler.serialHandler.write(mapRm + ":" + number)
        mapDa = self.pluginHandler.commandSet.getQualifiedShortCommand(CommandID.pluginMapData, [self.index])[0]
        self.pluginHandler.serialHandler.write("rqi:" + mapDa)

    def rangeChanged(self, value):
        self.range = value
        out = self.pluginHandler.commandSet.getQualifiedShortCommand(CommandID.pluginMapData, [self.index])[0]
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
                #newValue = (float(self.maps[k]) * int(self.ranges[self.range] + 1)) / int((self.ranges[self.oldRange] + 1))
                update = True
                self.maps[k] = newValue
                slider.setValue(newValue)
                self.updateLabel(int(k), str(round(newValue,0)))
                out += ":" + str(k) + ":" + str(round(newValue,0))

        #if (len(self.maps) > 0): self.pluginHandler.serialHandler.write(out);
        if (update): self.pluginHandler.serialHandler.write(out);
        self.oldRange = self.range

    class customSlider(QSlider):
        def __init__(self, plugin):
            super().__init__()
            self.number = 0
            self.plugin = plugin

        def mouseReleaseEvent(self, ev, /):
            mapDa = self.plugin.pluginHandler.commandSet.getQualifiedShortCommand(CommandID.pluginMapData, [self.plugin.index])[0]
            self.plugin.pluginHandler.serialHandler.write(mapDa + ":" + str(self.number) + ":" + str(self.value()))
            super().mouseReleaseEvent(ev)

    def sliderMouseRelease(self, event):
        mapDa = self.pluginHandler.commandSet.getQualifiedShortCommand(CommandID.pluginMapData, [self.index])[0]
        self.pluginHandler.serialHandler.write(mapDa + ":" + str(self.sender().number) + ":" + str(self.sender().value()))
        self.oldReleaseMouse(event)

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
        if (slider is None): return
        slider.setValue(self.maps[number])

    def renderSliders(self, sliderCountChanged):
        if (sliderCountChanged):
            for i in reversed(range(self.ui.layoutSliders.count())):
                if (not isinstance(self.ui.layoutSliders.itemAt(i), QSpacerItem)):
                    if ((self.ui.layoutSliders.itemAt(i).layout().objectName() != "layoutScale") and
                            (self.ui.layoutSliders.itemAt(i).layout().objectName() != "layoutRange")):
                        self.ui.layoutSliders.removeItem(self.ui.layoutSliders.itemAt(i))
                        #self.ui.layoutSliders.takeAt(i)
                else:
                    #self.ui.layoutSliders.takeAt(i)
                    self.ui.layoutSliders.removeItem(self.ui.layoutSliders.itemAt(i))

            for item in sorted(self.maps.keys()):
                self.addSlider(item, self.maps[item])
            self.rangeChanged(self.range)
        else:
            for item in sorted(self.maps.keys()):
                self.updateSlider(item)

        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.ui.layoutSliders.addItem(spacer)

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        if (getCommandIndex(commandItem) != self.index): return
        id = self.pluginHandler.commandSet.getCommandID(commandItem)
        match(id):
            case CommandID.pluginMapData:
                ogCount = len(self.maps)
                i = 0
                while(i + 1 < len(commandItem.argument)):
                    key = int(commandItem.argument[i].strip('\"').strip('\''))
                    value = int(round(float(commandItem.argument[i + 1].strip('\"').strip('\'')), 0))
                    self.maps[key] = value
                    i += 2
                sliderCountChanged = False
                if (ogCount != len(self.maps)): sliderCountChanged = True
                self.renderSliders(sliderCountChanged)
            case CommandID.pluginMapName:
                if len(commandItem.argument) > 0:
                 self.ui.mainGroupBox.setTitle("Number map [" + str(self.index) + "] - " + commandItem.argument[0])
            case CommandID.pluginMapTarget:
                if (len(commandItem.argument) > 0):
                    self.ui.textEditTarget.setText(commandItem.argument[0])
        pass

class Plugin_AHDSR(Plugin_Widget):
    def __init__(self, index, pluginHandler = None):
        super().__init__(plugin_ahdsr, index, pluginHandler)
        self.ui.mainGroupBox.setTitle("AHDSR [" + str(index) + "]")

        self.pluginHandler.assignValueChanged(self.ui.dialAmplitude, CommandID.pluginAHDSRAmpltiude, [index])
        self.pluginHandler.assignValueChanged(self.ui.dialAttack, CommandID.pluginAHDSRAttack, [index], True, 65535)
        self.pluginHandler.assignValueChanged(self.ui.dialHold, CommandID.pluginAHDSRHold, [index], True, 65535)
        self.pluginHandler.assignValueChanged(self.ui.dialDecay, CommandID.pluginAHDSRDecay, [index], True, 65535)
        self.pluginHandler.assignValueChanged(self.ui.dialSustain, CommandID.pluginAHDSRSustain, [index])
        self.pluginHandler.assignValueChanged(self.ui.dialRelease, CommandID.pluginAHDSRRelease, [index], True, 65535)
        self.pluginHandler.assignValueChanged(self.ui.checkBoxEnabled, CommandID.pluginAHDSREnable, [index])
        self.pluginHandler.assignValueChanged(self.ui.checkBoxInverted, CommandID.pluginAHDSRInvert, [index])
        self.pluginHandler.assignValueChanged(self.ui.textEditTarget, CommandID.pluginAHDSRTarget, [index])
        self.pluginHandler.assignValueChanged(self.ui.textEditReleaseTarget, CommandID.pluginAHDSRReleaseTarget, [index])

        self.requestData = [CommandID.pluginAHDSRAmpltiude, CommandID.pluginAHDSRAttack,
                            CommandID.pluginAHDSRHold, CommandID.pluginAHDSRDecay,
                            CommandID.pluginAHDSRSustain, CommandID.pluginAHDSRRelease,
                            CommandID.pluginAHDSREnable, CommandID.pluginAHDSRInvert,
                            CommandID.pluginAHDSRTarget, CommandID.pluginAHDSRReleaseTarget]

    def updateWidget(self, simpleFARHandler):
        self.updatingFromModule = True

        self.updateValueAndLabel(CommandID.pluginAHDSRAmpltiude, self.ui.dialAmplitude, None)
        self.updateValueAndLabel(CommandID.pluginAHDSRAttack, self.ui.dialAttack, None, True, 65535)
        self.updateValueAndLabel(CommandID.pluginAHDSRHold, self.ui.dialHold, None, True, 65535)
        self.updateValueAndLabel(CommandID.pluginAHDSRDecay, self.ui.dialDecay, None, True, 65535)
        self.updateValueAndLabel(CommandID.pluginAHDSRSustain, self.ui.dialSustain, None)
        self.updateValueAndLabel(CommandID.pluginAHDSRRelease, self.ui.dialRelease, None, True, 65535)
        self.updateValueAndLabel(CommandID.pluginAHDSREnable, self.ui.checkBoxEnabled, None)
        self.updateValueAndLabel(CommandID.pluginAHDSRInvert, self.ui.checkBoxInverted, None)
        self.updateValueAndLabel(CommandID.pluginAHDSRTarget, self.ui.textEditTarget, None)
        self.updateValueAndLabel(CommandID.pluginAHDSRReleaseTarget, self.ui.textEditReleaseTarget, None)
        name = simpleFARHandler.stringModules[0].getCommandValue(CommandID.pluginAHDSRName)
        if (name != -1):
            self.ui.mainGroupBox.setTitle("AHDSR [" + str(self.index) + "] - " + name)

        self.updatingFromModule = False

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        if (getCommandIndex(commandItem) != self.index): return
        id = self.pluginHandler.commandSet.getCommandID(commandItem)
        match(id):
            case CommandID.pluginAHDSRName:
                if len(commandItem.argument) > 0:
                    self.ui.mainGroupBox.setTitle("AHDSR [" + str(self.index) + "] - " + commandItem.argument[0])

class Plugin_LFO(Plugin_Widget):
    def __init__(self, index, pluginHandler = None):
        super().__init__(plugin_lfo, index, pluginHandler)
        self.ui.mainGroupBox.setTitle("LFO [" + str(index) + "]")
        self.wave = { "saw" : 0, "triangle" : 1, "sine" : 2, "square" : 3, "random" : 4, 0 : "saw", 1 : "triangle", 2 : "sine", 3 : "square", 4 : "random"}

        self.pluginHandler.assignValueChanged(self.ui.dialDelay, CommandID.pluginLFODelay, [index], True, 65535)
        self.pluginHandler.assignValueChanged(self.ui.dialAmplitude, CommandID.pluginLFOAmpltiude, [index], True, 65535)
        self.pluginHandler.assignValueChanged(self.ui.dialFrequency, CommandID.pluginLFOFrequency, [index], True, 20)
        self.pluginHandler.assignValueChanged(self.ui.textEditTarget, CommandID.pluginLFOTarget, [index])
        self.pluginHandler.assignValueChanged(self.ui.checkBoxBipolar, CommandID.pluginLFOBipolar, [index])
        self.pluginHandler.assignValueChanged(self.ui.checkBoxEnabled, CommandID.pluginLFOEnable, [index])

        self.ui.sliderWaveform.valueChanged.connect(self.waveformSliderChange)

        self.requestData = [CommandID.pluginLFODelay, CommandID.pluginLFOAmpltiude, CommandID.pluginLFOFrequency,
                            CommandID.pluginLFOWaveform, CommandID.pluginLFOTarget]

    def waveformSliderChange(self, value):
        outMsg = self.pluginHandler.commandSet.getQualifiedShortCommand(CommandID.pluginLFOWaveform, [self.index])[0]
        self.pluginHandler.serialHandler.write(outMsg + ":" + self.wave[value])

    def updateWidget(self, simpleFARHandler):
        self.updatingFromModule = True

        self.updateValueAndLabel(CommandID.pluginLFODelay, self.ui.dialDelay, self.ui.labelDelayValue, True, 65535)
        self.updateValueAndLabel(CommandID.pluginLFOAmpltiude, self.ui.dialAmplitude, self.ui.labelAmplitudeValue, True, 65535)
        self.updateValueAndLabel(CommandID.pluginLFOFrequency, self.ui.dialFrequency, self.ui.labelFrequencyValue, True, 20)
        self.updateValueAndLabel(CommandID.pluginLFOTarget, self.ui.textEditTarget, None)

        a = simpleFARHandler.stringModules[0].getCommandValue(CommandID.pluginLFOWaveform, self.index)
        if (a != -1): self.ui.sliderWaveform.setValue(self.wave[a])

        name = simpleFARHandler.stringModules[0].getCommandValue(CommandID.pluginLFOName)
        if (name != -1):
            self.ui.mainGroupBox.setTitle("LFO [" + str(self.index) + "] - " + name)

        self.updatingFromModule = False

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        if (getCommandIndex(commandItem) != self.index): return
        id = self.pluginHandler.commandSet.getCommandID(commandItem)
        match(id):
            case CommandID.pluginLFOName:
                if len(commandItem.argument) > 0:
                    self.ui.mainGroupBox.setTitle("LFO [" + str(self.index) + "] - " + commandItem.argument[0])

class Plugin_Multiple(Plugin_Widget):
    def __init__(self, index, pluginHandler = None):
        super().__init__(plugin_mult, index, pluginHandler)
        self.ui.mainGroupBox.setTitle("Multiple input mixer [" + str(index) + "]")

        self.pluginHandler.assignValueChanged(self.ui.textEditTarget, CommandID.pluginMultTarget, [index])
        self.ui.pushButtonRemoveAdder.pressed.connect(self.removeAdder)
        self.ui.pushButtonRemoveRatio.pressed.connect(self.removeRatio)
        self.requestData = [CommandID.pluginMultTarget, CommandID.pluginMultData,
                            CommandID.pluginMultName]

    def updateWidget(self, simpleFARHandler):
        self.updatingFromModule = True
        self.updateValueAndLabel(CommandID.pluginMultTarget, self.ui.textEditTarget, None)
        self.updatingFromModule = False

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
        rmCmd = self.pluginHandler.commandSet.getQualifiedShortCommand(CommandID.pluginMultRemove, [self.index])[0]
        for item in items:
            self.pluginHandler.serialHandler.write(rmCmd + ":" + type + ":" + item.text())
            qlist.takeItem(qlist.row(item))

    def updateLists(self, type, id, value):
        match(type):
            case "adder":
                qlist = self.ui.listAdders
            case "ratio":
                qlist = self.ui.listRatios
            case _:
                return
        item = qlist.findItems(id, Qt.MatchFlag.MatchExactly)
        if (len(item) == 0): qlist.addItem(id)

    def processMessages(self, commandItem, commandSets, simpleFARHandler, mainWidget, serialHandler):
        if (getCommandIndex(commandItem) != self.index): return
        id = self.pluginHandler.commandSet.getCommandID(commandItem)
        match(id):
            case CommandID.pluginMultName:
                if len(commandItem.argument) > 0:
                    self.ui.mainGroupBox.setTitle("Multiple input mixer [" + str(self.index) + "] - " + commandItem.argument[0])

            case CommandID.pluginMultData:
                self.updateLists(commandItem.argument[0], commandItem.argument[1], commandItem.argument[2])

            case CommandID.pluginMultRemove:
                pass

class PluginHandler():
    def __init__(self, mainWidget, serialHandler, simpleFARHandler, commandSet = None):
        self.mainWidget = mainWidget
        self.commandSet: CommandSets.CommandSetModular = commandSet
        self.assignValueChanged = self.mainWidget.assignValueChanged
        self.serialHandler = serialHandler
        self.simpleFARHandler = simpleFARHandler
        self.plugins = []

        mainWidget.ui.pushButtonPluginsAdd.pressed.connect(self.addPlugin)
        mainWidget.ui.pushButtonPluginsRemove.pressed.connect(self.removePlugin)
        mainWidget.ui.pushButtonPluginsName.pressed.connect(self.renamePlugin)

        mainWidget.ui.scrollPlugins.setWidgetResizable(True)
        mainWidget.ui.scrollAreaContentsPlugins.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mainWidget.ui.verticalLayoutPlugins.setAlignment(Qt.AlignmentFlag.AlignTop)
        mainWidget.ui.verticalLayoutPlugins.addStretch()

        if mainWidget.ui.scrollAreaContentsPlugins.layout() is None:
            mainWidget.ui.scrollAreaContentsPlugins.setLayout(QVBoxLayout())
            mainWidget.ui.scrollAreaContentsPlugins.layout().setContentsMargins(0, 0, 0, 0)

        self.pluginNameCommand = { "lfo" : CommandID.pluginLFOName, "ahdsr" : CommandID.pluginAHDSRName,
                                   "multiple" : CommandID.pluginMultName, "numbermap" : CommandID.pluginMapName }

        self.pluginClasses = { "lfo" : Plugin_LFO, "ahdsr" : Plugin_AHDSR, "multiple" : Plugin_Multiple, "numbermap" : Plugin_NumberMap }

    def addPluginInternal(self, type, index):
        pluginList = self.mainWidget.ui.comboBoxPlugins
        pluginList.addItem(type + "[" + str(index) + "]")
        plugin = self.pluginClasses[type](index, self)

        if (plugin is not None):
            self.plugins.append(plugin)
            self.mainWidget.ui.scrollAreaContentsPlugins.layout().addWidget(plugin)
            for request in plugin.requestData:
                if (plugin.index != 0):
                    pass
                rq = self.commandSet.getQualifiedShortCommand(request, [plugin.index])
                if (len(rq) != 0):
                    rq = rq[0]
                else:
                    pass
                self.serialHandler.write("rqi:" + rq)

    def buildPluginList(self):
        pluginList = self.mainWidget.ui.comboBoxPlugins
        pluginList.clear()
        ph = self.commandSet.baseModule.getGroups("pluginhandler")[0]
        for pluginGroup in ph.children:
            pluginGroup:CommandSets.CommandSetModular.Group = pluginGroup
            pluginList.addItem(pluginGroup.longName + " - Add new")

        for i in reversed(range(self.mainWidget.ui.scrollAreaContentsPlugins.layout().count())):
            self.mainWidget.ui.scrollAreaContentsPlugins.layout().itemAt(i).widget().setParent(None)

        for pluginGroup in ph.children:
            if (not pluginGroup.isEmpty):
                for i in range(0, len(pluginGroup.children) + 1):
                    self.addPluginInternal(pluginGroup.longName, pluginGroup.index)
                    i += 1
        pass

    def updateWidgets(self, simpleFARHandler):
        for plugin in self.plugins:
            plugin.updateWidget(simpleFARHandler)

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

    def getPluginTypeCount(self, type):
        count = 0
        for plug in self.plugins:
            if isinstance(plug, self.pluginClasses[type]): count += 1
        return count

    def addPlugin(self):
        if (self.isSelectionPluginInstance()): return
        type = self.getPluginType()
        add = self.commandSet.getQualifiedShortCommand(CommandID.pluginHandlerAdd)[0]
        self.serialHandler.write(add + ":" + type)
        pluginGroup = self.commandSet.baseModule.getGroups("pluginhandler")[0]
        pluginGroup.addModule(self.commandSet.CommandItem(type + "[" + str(self.getPluginTypeCount(type)) + "]"))
        self.addPluginInternal(type, self.getPluginTypeCount(type))

    def removePlugin(self):
        if (not self.isSelectionPluginInstance()): return
        type, index = self.getPluginTypeAndIndex()
        pluginGroup = self.commandSet.baseModule.getGroups("pluginhandler")[0]
        pluginGroup.remove(index)
        plugin = self.getPlugin(type, index)
        deleteItemsOfLayout(plugin.layout())
        plugin.parent().children().remove(plugin)
        plugin.setParent(None)
        pluginList:QComboBox = self.mainWidget.ui.comboBoxPlugins
        pluginList.removeItem(pluginList.currentIndex())
        rq = self.commandSet.getQualifiedShortCommand(CommandID.pluginHandlerRemove)[0]
        self.serialHandler.write(rq + ":" + type + ":" + str(index))

    def renamePlugin(self):
        if (not self.isSelectionPluginInstance()): return
        type, index = self.getPluginTypeAndIndex()
        command = self.pluginNameCommand[type]
        rq = self.commandSet.getQualifiedShortCommand(command, [index])[0]
        newName = str(inputBox("New name", "New name", self.mainWidget))
        self.serialHandler.write(rq + ":" + newName)
