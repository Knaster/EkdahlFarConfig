from ModuleSystem import ModuleCommand, ModuleHandler, Module, commandHasStorableDataCmd
from CommandSets import CommandSetModular

from PySide6.QtWidgets import (QWidget, QDoubleSpinBox, QLineEdit, QSpinBox, QComboBox, QSlider, QCheckBox, QDial, QPushButton, QListWidget, QLabel,
                               QPlainTextEdit)

from PySide6.QtCore import QObject

class GUICallback:
    SKIP_CALLBACK = 1

    def __init__(self, widget:QWidget, commandString:str, type = "", moduleCommand = None, dataCallbackFunction = None, guiCallbackFunction = None,
                 force = False, isIndex = False, moduleObject = None, dataIsCommandString = False):
        self.widget:QWidget = widget
        self.commandString:str = commandString
        self.moduleCommand:ModuleCommand = moduleCommand
        self.type = type
        self.dataCallbackFunction = dataCallbackFunction
        self.guiCallbackFunction = guiCallbackFunction
        self.force:bool = force
        self.isIndex:bool = isIndex
        self.module:Module | ModuleHandler = moduleObject
        self.moduleCallback:ModuleCommand.Callback = None
        self.dataIsCommandString = dataIsCommandString
        self.widgetConnected = False

    def __eq__(self, other):
        if not isinstance(other, GUICallback):
            return NotImplemented
        return (self.widget is other.widget and
                self.commandString == other.commandString and
                self.dataCallbackFunction is other.dataCallbackFunction and
                self.guiCallbackFunction is other.guiCallbackFunction)

    def __hash__(self):
        return hash((id(self.widget), self.commandString,
                     id(self.dataCallbackFunction), id(self.guiCallbackFunction)))

class GUICallbackSystem(QObject):

    def __init__(self, parent, commandSet, serialHandler):
        super().__init__(parent)
        self.parent = parent
        self.commandSet:CommandSetModular = commandSet
        self.serialHandler = serialHandler
        self.updatingFromGUI:int = 0    # Stack-based indicator of whether things are being updated from the GUI or not, any value above 0 means TRUE
        self.updatingFromModule:int = 0 # Stack-based indicator of whether things are being updated from the module data or not, any value above 0 means TRUE
        self.guiCallBacks = list()

    def dataChangedGUIcallback(self, moduleCommand:ModuleCommand, callback:ModuleCommand.Callback):
        if (self.updatingFromGUI > 0): return
        self.updatingFromModule += 1

        if (moduleCommand is None):
            self.updatingFromModule -= 1
            return

        if callback.dataCallbackFunction is None:
            if (moduleCommand.arguments is None) or len(moduleCommand.arguments) == 0:
                self.updatingFromModule -= 1
                return
            data = moduleCommand.arguments[0]

            match callback.type:
                case "fvalue":
                    callback.widget.setValue(float(data))
                case "ivalue":
                    callback.widget.setValue(round(float(data)))
                case "text":
                    callback.widget.setText(data)
                case "checkbox":
                    callback.widget.setChecked(bool(int(data)))
                case "selection":
                    callback.widget.setCurrentIndex(int(data))
                case _:
                    pass
        elif callback.dataCallbackFunction == GUICallback.SKIP_CALLBACK:
            pass
        else:
            callback.dataCallbackFunction(moduleCommand)

        self.updatingFromModule -= 1

    def setGUIObjectValueFromCallback(self, callback:GUICallback):
        if (self.commandSet is None): return
        if (callback.type == "pressed"): return
        self.updatingFromModule += 1
        #command = self.commandSet.baseModule.getCommandDataS(callback.command)
        #if (command is None): return

        '''
        if isinstance(command, ModuleCommand):
            if (command.arguments is None):
                return
            if (len(command.arguments) < 1): return
            data = command.arguments[0]
        elif isinstance(command, ModuleHandler):
            data = command.selectedIndex
        else:
            pass
        '''
        #data = command.arguments[0]
        if (callback.moduleCommand is None) or (callback.moduleCommand.arguments is None) or (len(callback.moduleCommand.arguments) == 0):
            self.updatingFromModule -= 1
            return
        data = callback.moduleCommand.arguments[0]

        if (callback.dataCallbackFunction is None):
            match callback.type:
                case "fvalue":
                    callback.widget.setValue(float(data))
                case "ivalue":
                    callback.widget.setValue(round(float(data)))
                case "text":
                    callback.widget.setText(data)
                case "checkbox":
                    callback.widget.setChecked(bool(int(data)))
                case "selection":
                    callback.widget.setCurrentIndex(int(data))
                case _:
                    pass
        elif (callback.dataCallbackFunction == GUICallback.SKIP_CALLBACK):
            pass
        else:
            callback.dataCallbackFunction(callback.moduleCommand)
        self.updatingFromModule -= 1

    def guiChangedCallback0(self):
        self.guiChangedCallback(None)

    def guiChangedCallback(self, anything = None):
        if self.updatingFromModule > 0: return
        self.updatingFromGUI += 1

        sendOnly = False
        sender = self.sender()
        if sender.guiCallbackFunction is None:
            match (sender.callbackCallback.type):
                case "fvalue" | "ivalue":
                    value = sender.callbackCallback.widget.value()
                case "text":
                    value = sender.callbackCallback.widget.text()
                case "checkbox":
                    value = int(sender.callbackCallback.widget.isChecked())
                case "selection":
                    value = sender.callbackCallback.widget.currentIndex()
                case "pressed":
                    value = ""
                    sendOnly = True
                case _:
                    pass
            if (not sendOnly) and (not sender.callbackCallback.isIndex):
                out = sender.callbackCommand.getFullCommand()
            else:
                out = sender.callbackCommand
            if sender.callbackCallback.isIndex:
                out += "[" + str(value) + "]"
            else:
                if (str(value) != ""):
                    if (sender.callbackCallback.dataIsCommandString):
                        value = "'" + value + "'"
                    out += ":" + str(value)
            self.serialHandler.write(out)
#        elif (sender.guiCallbackFunction == GUICallback.SKIP_CALLBACK):
#            pass
        else:
            sender.guiCallbackFunction(sender.callbackCommand)
        self.updatingFromGUI -= 1

    def setGUIObjectValueFromCallbacks(self, guiCallbacks:list[GUICallback]):
        for guiCallback in guiCallbacks:
            self.setGUIObjectValueFromCallback(guiCallback)

    def addGUICallbacks(self, guiCallbacks: list[GUICallback], regenerateModuleCommand = False):
        for i in range(0, len(guiCallbacks)):
            guiCallback = guiCallbacks[i]
            returnCallback = self.addGUICallback(guiCallback, regenerateModuleCommand=regenerateModuleCommand)
            guiCallbacks[i] = returnCallback

    def addGUICallback(self, guiCallback:GUICallback, regenerateModuleCommand = False) -> GUICallback:
        sendOnly = False
        isIndex = False
        # widget, commandString:str, moduleCommand = None, dataCallbackFunction = None, guiCallbackFunction = None, force = False
        if (guiCallback is None):
            print("ERROR!! Guicallback is None")
            return

        if (guiCallback.moduleCallback is not None):
            if (guiCallback.moduleCommand is not None):
                guiCallback.moduleCommand.removeCallback(guiCallback.moduleCallback)
            guiCallback.moduleCallback = None

        if (regenerateModuleCommand or (guiCallback.moduleCommand is None) or (guiCallback.module is None)) and \
            (guiCallback.commandString is not None and guiCallback.commandString != ""):
            guiCallback.moduleCommand, guiCallback.module = self.commandSet.baseModule.getCommandAndModule(guiCallback.commandString)
            if (guiCallback.moduleCommand is None):
                print("ERROR!! Adding callback for commandstring " + guiCallback.commandString + " failed")

        if isinstance(guiCallback.widget, QPushButton):
            sendOnly = True
        elif (guiCallback.commandString is None) or (guiCallback.commandString == ""):
            guiCallback.module = None
            pass
        else:
            if guiCallback.module is None:
                return None
            if guiCallback.moduleCommand is None:
                return None

        if isinstance(guiCallback.widget, QLineEdit):
            guiCallback.type = "text"
            if not guiCallback.widgetConnected:
                guiCallback.widget.editingFinished.connect(self.guiChangedCallback)
                guiCallback.widgetConnected = True
        elif isinstance(guiCallback.widget, QCheckBox):
            guiCallback.type = "checkbox"
            if not guiCallback.widgetConnected:
                guiCallback.widget.checkStateChanged.connect(self.guiChangedCallback)
                guiCallback.widgetConnected = True
        elif isinstance(guiCallback.widget, QDoubleSpinBox):
            guiCallback.type = "fvalue"
            if not guiCallback.widgetConnected:
                guiCallback.widget.valueChanged.connect(self.guiChangedCallback)
                guiCallback.widgetConnected = True
        elif isinstance(guiCallback.widget, QDial) or isinstance(guiCallback.widget, QSpinBox) or isinstance(guiCallback.widget, QSlider):
            guiCallback.type = "ivalue"
            if not guiCallback.widgetConnected:
                guiCallback.widget.valueChanged.connect(self.guiChangedCallback)
                guiCallback.widgetConnected = True
        elif isinstance(guiCallback.widget, QLabel):
            guiCallback.type = "text"
        elif isinstance(guiCallback.widget, QComboBox):
            guiCallback.type = "selection"
            if not guiCallback.widgetConnected:
                guiCallback.widget.currentIndexChanged.connect(self.guiChangedCallback)
                guiCallback.widgetConnected = True
        elif isinstance(guiCallback.widget, QListWidget):
            guiCallback.type = "selection"
            if not guiCallback.widgetConnected:
                guiCallback.widget.currentItemChanged.connect(self.guiChangedCallback)
                guiCallback.widgetConnected = True
        elif isinstance(guiCallback.widget, QPushButton):
            guiCallback.type = "pressed"
            if not guiCallback.widgetConnected:
                guiCallback.widget.pressed.connect(self.guiChangedCallback0)
                guiCallback.widgetConnected = True
        elif isinstance(guiCallback.widget, QPlainTextEdit):
            guiCallback.type = "text"
            if not guiCallback.widgetConnected:
                guiCallback.widget.returnPressed.connect(self.guiChangedCallback)
                guiCallback.widgetConnected = True
        elif guiCallback.widget is None:
            guiCallback.type = "none"
        else:
            guiCallback.type = "unknown"
            print("ERROR Unknown widget type when adding GUICallback for command " + guiCallback.commandString)

        callbackExists = guiCallback in self.guiCallBacks

        if (not sendOnly):
            if (guiCallback.moduleCommand is not None):
                #if (guiCallback.moduleCallback is not None):
                    #self.removeGUICallback(guiCallback, moduleOnly = True)
                #    guiCallback.moduleCommand.removeCallback(guiCallback.moduleCallback)
                #if callbackExists and guiCallback.moduleCallback is not None:
                #    pass
                #    if guiCallback.commandString == "mcf.mc.ac":
                #        pass
                #else:
                guiCallback.moduleCallback = guiCallback.moduleCommand.addCallback(self.dataChangedGUIcallback, guiCallback, guiCallback.force)

            if guiCallback.widget is not None:
                guiCallback.widget.callbackCommand = guiCallback.moduleCommand
        else:
            if guiCallback.widget is not None:
                guiCallback.widget.callbackCommand = guiCallback.commandString

        if guiCallback.widget is not None:
            guiCallback.widget.guiCallbackFunction = guiCallback.guiCallbackFunction
            guiCallback.widget.callbackCallback = guiCallback

        if not callbackExists:
            self.guiCallBacks.append(guiCallback)

        return guiCallback

    def removeGUICallbacks(self, guiCallbacks:list[GUICallback]):
        for guiCallback in guiCallbacks:
            self.removeGUICallback(guiCallback, False)

    def removeGUICallback(self, guiCallback:GUICallback, moduleOnly = True):
        if guiCallback.moduleCommand is not None and isinstance(guiCallback.moduleCommand, ModuleCommand):
            guiCallback.moduleCommand.removeCallback(guiCallback.moduleCallback)
            if guiCallback in self.guiCallBacks and not moduleOnly:
                self.guiCallBacks.remove(guiCallback)
        else:
            pass

    def refreshAllGUIElements(self):
        for guiCallback in self.guiCallBacks:
            #data = self.commandSet.getCommandDataS(guiCallback.command)
            command = guiCallback.moduleCommand
            if (command is not None) and (commandHasStorableDataCmd(command)):
                self.dataChangedGUIcallback(command, guiCallback)
            pass
        pass

    def findCallbackWithIndexAndRemove(self, index:int, guiCallbacks:list[GUICallback]):
        #index = moduleCommand.parent.getIndex()
        for guiCallback in guiCallbacks:
            if (guiCallback.module.getIndex() == index):
                self.removeGUICallback(guiCallback, moduleOnly = True)
                guiCallbacks.remove(guiCallback)
                return

    def findCallbackWithIndexAndAdd(self, index:int, moduleStr:str, commandStr:str, dataCallbackFunction,
                                    guiCallbacks:list[GUICallback], force = False) -> list[GUICallback]:
        #index = moduleCommand.parent.getIndex()
        found = False
        for guiCallback in guiCallbacks:
            if (guiCallback.module.getIndex() == index):
                found = True
                break
        if not found:
            guiCallback = GUICallback(None, moduleStr + "[" + str(index) + "]." + commandStr, dataCallbackFunction = dataCallbackFunction, force=force)
            guiCallbacks.append(guiCallback)
            self.addGUICallback(guiCallback)
        return guiCallbacks

    def assignButtonPressCommandIssue(self, qtObject, command):
        qtObject.command = command
#        qtObject.refresh = refresh
        qtObject.pressed.connect(self.buttonPressIssueCommand)
    '''
    def convertWidgetCommandToString(self, sender):
        command = ""
        if (isinstance(sender.command, list)):
            i = 0
            while(i < len(sender.command)):
                qualifiedShorts = commandSets.getQualifiedShortCommand(sender.command[i])
                for qualified in qualifiedShorts:
                    if (command != ""): command += ","
                    command += qualified + ":" + sender.command[i + 1]
                i += 2
        elif (isinstance(sender.command, CommandID)):
            qualifiedShorts = commandSets.getQualifiedShortCommand(sender.command)
            for qualified in qualifiedShorts:
                if (command != ""): command += ","
                command += qualified
        else:
            command = sender.command
        return command
    '''
    def buttonPressIssueCommand(self):
        sender = self.sender()
        #command = self.convertWidgetCommandToString(sender)
        command = sender.command
        self.serialHandler.write(command)
        #if sender.refresh:
        #    self.updateUIData()
