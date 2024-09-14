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
