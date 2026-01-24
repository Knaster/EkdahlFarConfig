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

import time
from PySide6.QtWidgets import QWidget
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QScatterSeries, QSplineSeries, QValueAxis, QLogValueAxis
from PySide6.QtGui import QPainter

#------------------
from PySide6.QtGui import QImage, QColor
from PySide6.QtCore import Qt
#import rc_markers  # noqa: F401

from dataclasses import dataclass

from CommandSets import CommandID, CommandSets

def rectangle(point_type, image_size):
    image = QImage(image_size, image_size, QImage.Format_RGB32)
    painter = QPainter()
    painter.begin(image)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.fillRect(0, 0, image_size, image_size, point_type[2])
    painter.end()
    return image

def triangle(point_type, image_size):
    return QImage(point_type[3]).scaled(image_size, image_size)

def circle(point_type, image_size):
    image = QImage(image_size, image_size, QImage.Format_ARGB32)
    image.fill(QColor(0, 0, 0, 0))
    painter = QPainter()
    painter.begin(image)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(point_type[2])
    pen = painter.pen()
    pen.setWidth(0)
    painter.setPen(pen)
    painter.drawEllipse(0, 0, image_size * 0.9, image_size * 0.9)
    painter.end()
    return image


_point_types = [("RedRectangle", rectangle, Qt.red),
                ("OrangeCircle", circle, QColor(255, 127, 80))]

def default_light_marker(image_size):
    return circle(_point_types[1], image_size)

#-----------------

class timeStamp:
    def __init__(self):
        self.initValue = -1
        self.overflow = 10

    def getCurrent(self):
        if (self.initValue == -1):
            self.initValue = time.time()

        return (time.time() - self.initValue)

from enum import Enum

class seriesType(Enum):
    frequency = 1
    integer = 2

@dataclass
class chartMatchData:
    seriesType: seriesType
    description: str
    index: int
    commandID:CommandID


class timedChart(QWidget):
    chartMatchArr = [ chartMatchData(seriesType.integer, "Harmonic (A0)", 0, CommandID.controlBoxDataReturn),
                      chartMatchData(seriesType.integer, "Harmonic shift (A1)", 1, CommandID.controlBoxDataReturn),
                      chartMatchData(seriesType.integer, "Fine tuning (A2)", 2, CommandID.controlBoxDataReturn),
                      chartMatchData(seriesType.integer, "Pressure (A3)", 3, CommandID.controlBoxDataReturn),
                      chartMatchData(seriesType.integer, "Hammer trig (A4)", 4, CommandID.controlBoxDataReturn),
                      chartMatchData(seriesType.integer, "Gate (A5)", 5, CommandID.controlBoxDataReturn),
                      chartMatchData(seriesType.integer, "Hammer scale (A6)", 6, CommandID.controlBoxDataReturn),
                      chartMatchData(seriesType.integer, "Mute (A7)", 7, CommandID.controlBoxDataReturn),
                      chartMatchData(seriesType.frequency, "Set motor frequency", -1, CommandID.pidTargetFreq),
                      chartMatchData(seriesType.frequency, "Read motor frequency", -1, CommandID.motorFrequency),
                      chartMatchData(seriesType.frequency, "Audio frequency", -1, CommandID.pickupStringFrequency),
                      chartMatchData(seriesType.integer, "Audio peak", -1, CommandID.pickupAudioPeak),
                      chartMatchData(seriesType.integer, "Audio RMS", -1, CommandID.pickupAudioRMS),
                      chartMatchData(seriesType.frequency, "PID Error", -1, CommandID.pidPeakError),
                      chartMatchData(seriesType.integer, "Motor current (x6k)", -1, CommandID.motorCurrent) ]

    def getChart(self, commandID, index):
        for chart in self.chartMatchArr:
            if (chart.commandID == commandID) and ((chart.index == -1) or (chart.index == index)):
                return chart
        return None

    def __init__(self):
        ## Array of all the series classes in the chart
        self.seriesArr = []

        self.chart = QChart()

        self.axisX = QValueAxis();
        self.axisX.setTitleText("Time (S)")
        self.axisX.setTitleVisible(True)
        self.chart.addAxis(self.axisX, Qt.AlignBottom)

        self.axisYHz = QLogValueAxis();
        self.axisYHz.setBase(2)
        self.axisYHz.setRange(1, 2048)
        self.axisYHz.setTitleText("Frequency (Hz)")
        self.axisYHz.setTitleVisible(True)
        self.chart.addAxis(self.axisYHz, Qt.AlignRight)

        self.axisYInt = QValueAxis();
        self.axisYInt.setRange(0, 65535)
        self.axisYInt.setLabelFormat("%i")
        self.axisYInt.setTitleText("uint16")
        self.axisYInt.setTitleVisible(True)
        self.chart.addAxis(self.axisYInt, Qt.AlignLeft)

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        self.timeStamper = timeStamp()

        self.commandSet = None

    lastClean = 0

    def addData(self, seriesID, value, inSeriesType): #min, max,): #
        if ((inSeriesType == seriesType.frequency) and (value <= 0)):
            return

        s = self.getSeries(seriesID)
        if s is None:
            s = self.addSeries(seriesID, inSeriesType)
            #s.setUseOpenGL(True)
            if s is None:
                return
            sFound = True

        s.append(self.timeStamper.getCurrent(), float(value))

        self.axisX.setRange(self.timeStamper.getCurrent() - self.timeStamper.overflow, self.timeStamper.getCurrent())

# Only clean up every [overflow] so that this doesn't detract
        if (self.timeStamper.getCurrent() - self.lastClean > self.timeStamper.overflow):
            self.lastClean = self.timeStamper.getCurrent()
            for point in s.pointsVector():
                if point.x() < (self.timeStamper.getCurrent() - self.timeStamper.overflow):
                    s.remove(point)

    def getSeries(self, seriesID):
#        for s in self.chart.series():
        for s in self.seriesArr:
            if (s.name == seriesID):
                return s

        return None

    def addSeries(self, seriesID, inSeriesType):
        s = QLineSeries()
        s.name = seriesID
        s.setName(seriesID)

        s.setPointLabelsColor(QColor("blue"))
        s.setPointLabelsFormat("@yPoint")
        s.setPointLabelsClipping(True)

        self.seriesArr.append(s)
        self.chart.addSeries(s)

        s.attachAxis(self.axisX)
        if inSeriesType == seriesType.integer:
            s.attachAxis(self.axisYInt)
        elif inSeriesType == seriesType.frequency:
            s.attachAxis(self.axisYHz)
        else:
            print("ERROR")
            return None
        return s

    def setSeriesVisibleCommand(self, command, index, visible):
        try:
            #seriesID = self.chartMatchArr[command].description
            seriesID = self.getChart(command, index).description
            seriesType = self.getChart(command, index).seriesType
            s = self.getSeries(seriesID)
        except:
            print("Error in setSeriesVisibleCommand")
            return

        if s is None:
            #s = self.addSeries(seriesID, self.chartMatchArr[command].seriesType)
            s = self.addSeries(seriesID, seriesType)
            if s is None:
                return
        s.setVisible(visible)

    def processCommand(self, command):
        if self.commandSet is None: return
        cId = self.commandSet.getCommandID(command)

        try:
            value = float(command.argument[0])
        except:
            return

        match cId:
            case CommandID.controlBoxDataReturn:
                value = float(command.argument[1])
            case CommandID.pickupAudioPeak | CommandID.pickupAudioRMS:
                value *= 65535
            case CommandID.motorCurrent:
                value *= 60000
        try:
            index = -1
            if len(command.argument) > 2: index = int(command.argument[0])
            series = self.getChart(cId, index)
        except:
            return
        if (series is not None):
            self.addData(series.description, value, series.seriesType)
