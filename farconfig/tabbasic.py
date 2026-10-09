from PySide6.QtCore import QObject
import math

import tableTest
from ModuleSystem import ModuleCommand
from CommandSets import CommandSetModular
from commandparser import Derivedcommanditem

from general_helpers import messageBox, inputBox, find_item, remove_item
from GUICallbackSystem import GUICallbackSystem, GUICallback

class TabBasic(QObject):
    def __init__(self, mainWidget, serialHandler, commandSet:CommandSetModular, guiCallbackSystem:GUICallbackSystem):
        super().__init__()
        self.mainWidget = mainWidget
        self.serialHandler = serialHandler
        self.commandSet:CommandSetModular = commandSet
        self.ui = mainWidget.ui

        self.populateComboBoxBaseNote()
        self.populateHarmonicPresets()

        self.scaleDataChangedCallback = None
        self.currentHarmonicData = []

        self.tableViewScale = tableTest.customTableView
        self.customTableModel = tableTest.CustomTableModel
        self.delegate = tableTest.noneDelegate

        self.guiCallbackSystem = guiCallbackSystem
        self.guiCallbacks: list[GUICallback] = list()
        self.guiCallbacksHarmonicConfig: list[GUICallback] = list()
        self.guiCallbacksHarmonicConfigNames: list[GUICallback] = list()

        self.guiCallbacksAdded = False

    def addGUICallbacks(self):
        if (self.guiCallbacksAdded): return
        self.guiCallbacksAdded = True

        self.guiCallbacks = [GUICallback(self.ui.doubleSpinBoxFundamentalFrequency, "bw.hsh.fu"),
                             GUICallback(self.ui.pushButtonCalibrateAll, "ca"),
                             GUICallback(self.ui.pushButtonCalibratePressure, "cbp"),
                             GUICallback(self.ui.pushButtonCalibrateMute, "cmu"),
                             #GUICallback(self.ui.pushButtonCalibrateHammer, "chm"),
                             GUICallback(None, "bw.hsh.count", dataCallbackFunction = self.dataChangedHarmonicSeriesCount, force = True),
                             GUICallback(self.ui.comboBoxHarmonicList, "bw.hsh.hs", force = True,
                                       dataCallbackFunction = self.dataChangedHarmonicListIndex, guiCallbackFunction = self.guiChangedHarmonicListIndex),
                             GUICallback(self.ui.comboBoxBaseNote, "bw.hsh.bn", dataCallbackFunction = self.dataChangedBaseNote,
                                         guiCallbackFunction = self.guiChangedBaseNote),
                             GUICallback(None, "bw.hsh.a", dataCallbackFunction = self.dataChangedHarmonicListAdded),
                             GUICallback(None, "bw.hsh.rm", dataCallbackFunction = self.dataChangedHarmonicListRemoved),
                             GUICallback(None, "psf", dataCallbackFunction = self.dataChangedStringFrequency)]

        self.guiCallbackSystem.addGUICallbacks(self.guiCallbacks)

        self.guiCallbacksHarmonicConfig = [GUICallback(None, "bw.hsh.hs.na", dataCallbackFunction = self.dataChangedHarmonicSeriesName,
                                                       force = True),
                                           GUICallback(None, "bw.hsh.hs.da", dataCallbackFunction=self.dataChangedScaleData, force = True),
                                           GUICallback(None, "bw.hsh.hs.r", dataCallbackFunction = self.dataChangedScaleRatio)]

        #self.ui.comboBoxBaseNote.currentIndexChanged.connect(self.comboBoxBaseNotePressed)
        self.ui.comboBoxFundamentalFrequency.currentIndexChanged.connect(self.comboBoxFundamentalFrequencyIndexChanged)

        self.mainWidget.connectSignalToModalDialog(self.ui.pushButtonCalibrateAll, "ca", "ca")

        self.ui.pushButtonPickupAnalyse.pressed.connect(self.pushButtonPickupAnalysePressed)
        self.ui.pushButtonAddHarmonic.pressed.connect(self.pushButtonAddHarmonicPressed)
        self.ui.pushButtonRemoveHarmonic.pressed.connect(self.pushButtonRemoveHarmonicPressed)
        self.ui.pushButtonLoadHarmonicPreset.pressed.connect(self.pushButtonLoadHarmonicPresetPressed)
        self.ui.pushButtonRenameHarmonicList.pressed.connect(self.pushButtonRenameHarmonicListPressed)
        self.ui.pushButtonAddHarmonicList.pressed.connect(self.pushButtonAddHarmonicListPressed)
        self.ui.pushButtonAddHarmonicListFile.pressed.connect(self.pushButtonAddHarmonicListFilePressed)
        self.ui.pushButtonRemoveHarmonicList.pressed.connect(self.pushButtonRemoveHarmonicListPressed)

        self.tableViewScale = tableTest.customTableView(self.ui.groupBox_3)
        self.tableViewScale.horizontalHeader().setDefaultSectionSize(70)
        self.tableViewScale.horizontalHeader().setMinimumSectionSize(18)
        self.tableViewScale.verticalHeader().setDefaultSectionSize(30)
        self.tableViewScale.verticalHeader().setMinimumSectionSize(22)
        self.ui.layoutHarmonicTable.replaceWidget(self.ui.xtableViewScale, self.tableViewScale)
        self.customTableModel = tableTest.CustomTableModel()
        self.tableViewScale.setModel(self.customTableModel)

        self.delegate = tableTest.noneDelegate()
        self.tableViewScale.setItemDelegateForRow(0, self.delegate)
        self.tableViewScale.model().dataChanged.connect(self.guiChangedScaleData)

    def updateWidget(self):
        self.guiCallbackSystem.setGUIObjectValueFromCallbacks(self.guiCallbacks)
        self.updateScaleData()
        pass

    def comboBoxFundamentalFrequencyIndexChanged(self):
        text = self.ui.comboBoxFundamentalFrequency.currentText()
        if text == "":
            return
        self.ui.doubleSpinBoxFundamentalFrequency.setValue(float(self.ui.comboBoxFundamentalFrequency.currentText()[3:len(text)]))

    def pushButtonPickupAnalysePressed(self):
        saveState = self.ui.checkBoxContinuousSMData.checkState()
        self.ui.checkBoxContinuousSMData.setChecked(True)
        self.serialHandler.write("so.sfm:1,so.en:65535")
        self.mainWidget.showModalWait("", "", 2500, "Analysing", True)
        self.ui.checkBoxContinuousSMData.setCheckState(saveState)
        pass

    def pushButtonLoadHarmonicPresetPressed(self):
        b = self.ui.comboBoxHarmonicPresets.currentIndex()
        if (b < 0) or (b > len(self.harmonicPresets)):
            print("Error!")
            return
        self.setHarmonicSeriesData(self.ui.comboBoxHarmonicList.currentText(), self.harmonicPresets[b][1:len(self.harmonicPresets[b])])

    def guiChangedBaseNote(self, commandData:ModuleCommand):
        index = self.ui.comboBoxBaseNote.currentIndex()
        self.serialHandler.write("bw.hsh.bn:" + str(self.ui.comboBoxBaseNote.itemData(index)))

    def dataChangedBaseNote(self, moduleCommand:ModuleCommand):
        if (moduleCommand is not None) and (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) > 0):
            self.ui.comboBoxBaseNote.setCurrentIndex(int(moduleCommand.arguments[0]) - 48)

    def dataChangedHarmonicSeriesCount(self, moduleCommand:ModuleCommand):
        if (moduleCommand is not None) and (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) > 0):
            self.ui.comboBoxHarmonicList.clear()
            for i in range(0, int(moduleCommand.arguments[0])):
                self.guiCallbackSystem.findCallbackWithIndexAndAdd(i, "bw.hsh.hs", "na", self.dataChangedHarmonicSeriesName,
                                                                   self.guiCallbacksHarmonicConfigNames)

    #            self.guiCallbackSystem.addGUICallback(None, "bw.hsh.hs[" + str(i) + "].na", dataCallbackFunction = self.dataChangedHarmonicSeriesName, force = True)
    #            self.guiCallbackSystem.addGUICallback(None, "bw.hsh.hs[" + str(i) + "].da", dataCallbackFunction=self.dataChangedScaleData, force = True)

                #command = self.commandSet.getCommandDataS("bw.hsh.hs[" + str(i) + "].na")
                command, module = self.commandSet.getCommandAndModule("bw.hsh.hs[" + str(i) + "].na")
                if (command is not None) and (command.arguments is not None) and (len(command.arguments) > 0):
                    self.ui.comboBoxHarmonicList.addItem(command.arguments[0])
                else:
                    self.ui.comboBoxHarmonicList.addItem("--_--")
                    self.serialHandler.write("rqi:bw.hsh.hs[" + str(i) + "].na")
            command, module = self.commandSet.getCommandAndModule("bw.hsh.hs")
            self.ui.comboBoxHarmonicList.setCurrentIndex(int(command.arguments[0]))

    def dataChangedHarmonicListAdded(self, command:ModuleCommand):
        if (command.arguments is not None) and (len(command.arguments) > 1):
            index = int(command.arguments[1])
            if (index == -1): return
            self.guiCallbackSystem.findCallbackWithIndexAndAdd(index, "bw.hsh.hs", "na", self.dataChangedHarmonicSeriesName,
                                                               self.guiCallbacksHarmonicConfigNames)

    def dataChangedHarmonicListRemoved(self, command:ModuleCommand):
        if (command.arguments is not None) and (len(command.arguments) > 1):
            index = int(command.arguments[1])
            if (index == -1): return
            self.guiCallbackSystem.findCallbackWithIndexAndRemove(index, self.guiCallbacksHarmonicConfigNames)

    def dataChangedHarmonicSeriesName(self, moduleCommand:ModuleCommand):
        if moduleCommand.arguments is not None:
            if len(moduleCommand.arguments) > 0:
                name = moduleCommand.arguments[0]
            else:
                name = "[none]"
            index = moduleCommand.parent.getIndex()
            self.ui.comboBoxHarmonicList.setItemText(int(index), name)
            command, module = self.commandSet.getCommandAndModule("bw.hsh.hs")
            self.ui.comboBoxHarmonicList.setCurrentIndex(int(command.arguments[0]))

    def guiChangedScaleData(self, topLeft, bottomRight, role):
        self.serialHandler.write("bw.hsh.hs.r:" + str(topLeft.column()) + ":" + str(topLeft.guiCallback())) #+ ", rqi:bw.hsh.hs.da"

    def dataChangedScaleRatio(self, commandData):
        self.serialHandler.write("rqi:bw.hsh.hs.da")

    def dataChangedScaleData(self, commandData):
        self.updateScaleData()

    def updateScaleData(self):
        #command = self.commandSet.getCommandDataS("bw.hsh.hs.da")
        if self.customTableModel is None or self.tableViewScale is None or (not hasattr(self.customTableModel, "dataset")):
            return

        index = self.tableViewScale.currentIndex()
        cellFocus = False
        if (index.isValid()):
            cellFocus = True
            row = index.row()
            col = index.column()

        command, module = self.commandSet.getCommandAndModule("bw.hsh.hs.da")
        if (command is None): return
        if (not hasattr(command, "arguments")):
            return
        if (command.arguments is None):
            return
        if (len(command.arguments) < 2):
            return

        self.currentHarmonicData.clear()
        for i in range(1, len(command.arguments)):
            self.currentHarmonicData.append(command.arguments[i])

        self.tableViewScale.setModel(tableTest.CustomTableModel(self.currentHarmonicData))
        self.tableViewScale.model().dataChanged.connect(self.guiChangedScaleData)
        if cellFocus:
            self.tableViewScale.setCurrentIndex(self.tableViewScale.model().index(row, col))
            self.tableViewScale.setFocus()


    def dataChangedHarmonicListIndex(self, command):
        newIndex = int(command.arguments[0])
        self.ui.comboBoxHarmonicList.setCurrentIndex(newIndex)
        self.guiCallbackSystem.removeGUICallbacks(self.guiCallbacksHarmonicConfig)
        self.guiCallbackSystem.addGUICallbacks(self.guiCallbacksHarmonicConfig, regenerateModuleCommand=True)
        self.updateScaleData()

    def guiChangedHarmonicListIndex(self, index):
        if self.guiCallbackSystem.updatingFromModule > 0: return
        self.serialHandler.write("bw.hsh.hs[" + str(self.ui.comboBoxHarmonicList.currentIndex()) + "]")

    def pushButtonAddHarmonicPressed(self):
        #command = self.commandSet.getCommandDataS("bw.hsh.hs.da")
        command, module = self.commandSet.getCommandAndModule("bw.hsh.hs.da")
        if (command is None): return
        ratioIndex = len(command.arguments) - 1
        self.serialHandler.write("bw.hsh.hs.r:" + str(ratioIndex) + ":1, rqi:bw.hsh.hs.da")

    def pushButtonRemoveHarmonicPressed(self):
        selected = int(self.tableViewScale.currentIndex().column())
        if (selected < 0):
            messageBox("Error", "Incorrect selection");
            return
        self.serialHandler.write("bw.hsh.hs.rm:"+ str(selected) + ", rqi:bw.hsh.hs.da")

    def pushButtonAddHarmonicListPressed(self):
        listID = inputBox("List name", "List name")
        if listID is None:
            return
        self.serialHandler.write("bw.hsh.a:'" + listID + "', rqi:bw.hsh.count")

    def pushButtonRenameHarmonicListPressed(self):
        listName = inputBox("List name", "List name")
        if listName is None:
            return
        self.serialHandler.write("bw.hsh.hs.na:'" + listName + "'")

    def pushButtonRemoveHarmonicListPressed(self):
        harmonicList = self.ui.comboBoxHarmonicList.currentIndex()
        self.serialHandler.write("bw.hsh.rm:" + str(harmonicList)) # + ", rqi:bw.hsh.count")

    def pushButtonAddHarmonicListFilePressed(self):
        pass

    midiKeys = ["C-", "C#", "D-", "D#", "E-", "F-", "F#", "G-", "G#", "A-", "A#", "B-"]

    def populateComboBoxBaseNote(self):
        for octave in range(0,3):
            for key in range(0,12):
                self.ui.comboBoxBaseNote.addItem(self.midiKeys[key] + str(octave + 4), (octave + 4) * 12 + key)

    harmonicPresets = [["Just", 1, 1.06667, 1.125, 1.2, 1.25, 1.3333, 1.40625, 1.5, 1.6, 1.66667, 1.8, 1.875],
        ["Equal", 1, 1.059463094, 1.122462048, 1.189207115, 1.25992105, 1.334839854, 1.414213562, 1.498307077, 1.587401052, 1.681792831, 1.781797436, 1.887748625]]

    def populateHarmonicPresets(self):
        for a in self.harmonicPresets:
            self.ui.comboBoxHarmonicPresets.addItem(a[0])

    def setHarmonicSeriesData(self,name, data):
        comm = "bw.hsh.hs.da" + ":'" + name + "'"
        for d in data: comm += ":" + str(d)
        self.serialHandler.write(comm) # + ", rqi:bw.hsh.hs[]")

    def getBaseNoteFromFrequency(self, frequency, noteDataArray):
        oct0f = noteDataArray[0] / 32
        octave = 5
        while math.trunc(frequency / (oct0f * 2 ** octave)) < 2:
            octave -= 1
        octave += 1
        measBaseline = oct0f * 2 ** (octave)
        for note in range(0, len(noteDataArray[1])):
            if measBaseline * noteDataArray[1][note] > frequency: break

        # if we're still under we're just at the break of the next octave
        if measBaseline * noteDataArray[1][note] <= frequency:
            note = 11

        note -= 1
        cents = math.log2(frequency / (measBaseline * noteDataArray[1][note])) * 1200
        #  if we are over 60 we should convert to negative by recalculating towards the next note
        if (cents > 60):
            # print ("Cent calculation from frequency failed")
            note += 1
            cents = math.log2(frequency / (measBaseline * noteDataArray[1][note])) * 1200
            #  if we're still over we're at the break of an octave
            if (cents > 60):
                octave += 1
                measBaseline = oct0f * 2 ** (octave)
                note = 0
                cents = math.log2(frequency / (measBaseline * noteDataArray[1][note])) * 1200

        noteName = noteDataArray[2][note]
        return octave, note, cents, noteName

    def dataChangedStringFrequency(self, moduleCommand:ModuleCommand):
        if (moduleCommand.arguments is not None) and (len(moduleCommand.arguments) > 0):
            freq = float(moduleCommand.arguments[0])
            if not freq is None:
                if (freq > 0):
                    if (self.mainWidget.preferences.ui.listWidgetTuningscheme.currentItem() != None):
                        if ((self.mainWidget.preferences.ui.listWidgetTuningscheme.currentItem().text()) == "Equal temperament"):
                            ret = self.getBaseNoteFromFrequency(freq, self.mainWidget.scaleDataEqual)
                        else:
                            ret = self.getBaseNoteFromFrequency(freq, self.mainWidget.scaleDataJust)
                    else:
                        ret = self.getBaseNoteFromFrequency(freq, self.mainWidget.scaleDataJust)

                    self.ui.labelAnalyzeNote.setText(ret[3] + str(ret[0]))
                    self.ui.labelAnalyzeCents.setText(str(round(ret[2])))
                    self.ui.labelAnalyzeFreq.setText(str(round(freq,1)))
