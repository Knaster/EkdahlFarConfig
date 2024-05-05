from PySide6.QtCore import QThread, Signal
import mido

class MidiHandler(QThread):

    def __init__(self, dataSignaler):
        self.midiInDevice = None
        #self.receiver = receiver
        self.deviceName = ""
        self.dataSignaler = dataSignaler
        pass

    def updateMIDIInDevices(self, qtList):
        for port in mido.get_input_names():
            #mainWidget.ui.comboBoxMIDILearnDevice.addItem(port)
            qtList.addItem(port)

    def midoInCallback(self, msg):
        #print(msg.control)
        self.dataSignaler.emit(self.deviceName, str(msg))
        #self.receiver()

    def connecToMIDIIn(self, deviceName):
        if self.midiInDevice != None:
            self.midiInDevice.close()
        self.deviceName = deviceName
        self.midiInDevice = mido.open_input(self.deviceName, False, self.midoInCallback)
