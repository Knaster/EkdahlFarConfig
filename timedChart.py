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


class timedChart(QWidget):
    chartMatchArr = {"adcr0": chartMatchData(seriesType.integer, "Harmonic (A0)"),
                     "adcr1": chartMatchData(seriesType.integer, "Harmonic shift (A1)"),
                     "adcr2": chartMatchData(seriesType.integer, "Fine tuning (A2)"),
                     "adcr3": chartMatchData(seriesType.integer, "Pressure (A3)"),
                     "adcr4": chartMatchData(seriesType.integer, "Hammer trig (A4)"),
                     "adcr5": chartMatchData(seriesType.integer, "Gate (A5)"),
                     "adcr6": chartMatchData(seriesType.integer, "Hammer scale (A6)"),
                     "adcr7": chartMatchData(seriesType.integer, "Mute (A7)"),
                     "bcf": chartMatchData(seriesType.frequency, "Set motor frequency"),
                     "bmf": chartMatchData(seriesType.frequency, "Read motor frequency"),
                     "psf": chartMatchData(seriesType.frequency, "Audio frequency"),
                     "pap": chartMatchData(seriesType.integer, "Audio peak"),
                     "par": chartMatchData(seriesType.integer, "Audio RMS"),
                     "bpperr": chartMatchData(seriesType.frequency, "PID Error"),
                     "bmc": chartMatchData(seriesType.integer, "Motor current (x6k)")
                     }

    #for poo in chartMatchArr:
    #    print(chartMatchArr[poo].description)

    def __init__(self):
        ## Array of all the series classes in the chart
        self.seriesArr = []

        self.chart = QChart()
#        self.chart.createDefaultAxes()

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

    lastClean = 0

    def addData(self, seriesID, value, inSeriesType): #min, max,): #
        if ((inSeriesType == seriesType.frequency) and (value <= 0)):
            return

        s = self.getSeries(seriesID)
        if s is None:
            s = self.addSeries(seriesID, inSeriesType)
            s.setUseOpenGL(True)
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
#        s.setVisible(False)
        # s.setPointLabelsVisible(True)

        # s.setMarkerSize(5)
        # s.setLightMarker(default_light_marker(5))

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

    def setSeriesVisibleCommand(self, command, visible):
        try:
            seriesID = self.chartMatchArr[command].description
            s = self.getSeries(seriesID)
        except:
            print("Error in setSeriesVisibleCommand")
            return

        if s is None:
            s = self.addSeries(seriesID, self.chartMatchArr[command].seriesType)
            if s is None:
                return

        s.setVisible(visible)

    def processCommand(self, command):
        key = command.command
        try:
            value = float(command.argument[0])
        except:
            return

        #if command.command == "adcr":
        match command.command:
            case "adcr":
                key += command.argument[0]
                value = float(command.argument[1])
            case "pap" | "par":
                value *= 65535
            case "bmc":
                value *= 60000

        try:
            series = self.chartMatchArr[key]
            #print("Found a chart!")
        except:
            #print("no series for command " + str(key) )
            return

        self.addData(series.description, value, series.seriesType)

# mainWidget.debugTimedChart.setSeriesVisible(chartMatchArr[checkbox.seriesName].description, chartMatchArr[checkbox.seriesName].seriesType, visible)


# Match commands that are going on the chart, these commands may be processed further by processInformationReturn

#        if (not sFound):
##            print("Creating new series")
#            s = QLineSeries()
#            s.name = seriesID
#            s.setName(seriesID)
#
#            s.setPointLabelsColor(QColor("blue"))
#            s.setPointLabelsFormat("@yPoint")
#            s.setPointLabelsClipping(True)
#            #s.setPointLabelsVisible(True)
#
#            #s.setMarkerSize(5)
#            #s.setLightMarker(default_light_marker(5))
#
#            # Add the newly created series class to the local series array seriesArr
#            self.seriesArr.append(s)
#            self.chart.addSeries(s)
#
#            s.attachAxis(self.axisX)
#            if (inSeriesType == seriesType.integer):
#                s.attachAxis(self.axisYInt)
#            elif (inSeriesType == seriesType.frequency):
#                s.attachAxis(self.axisYHz)
#            else:
#                print("ERROR")

#        print(s.isVisible())
        #s.setVisible(True)
