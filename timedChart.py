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

class timedChart(QWidget):
    def __init__(self):
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

    def addData(self, seriesID, value, inSeriesType): #min, max,): #
        if ((inSeriesType == seriesType.frequency) and (value <= 0)):
            return

        sFound = False
        for s in self.seriesArr:
            if (s.name == seriesID):
                sFound = True
#                print("Found series")
                break

        if (not sFound):
#            print("Creating new series")
            s = QLineSeries()
            s.name = seriesID
            s.setName(seriesID)

            s.setPointLabelsColor(QColor("blue"))
            s.setPointLabelsFormat("@yPoint")
            s.setPointLabelsClipping(True)
            #s.setPointLabelsVisible(True)

            #s.setMarkerSize(5)
            #s.setLightMarker(default_light_marker(5))

            self.seriesArr.append(s)
            self.chart.addSeries(s)

            s.attachAxis(self.axisX)
            if (inSeriesType == seriesType.integer):
                s.attachAxis(self.axisYInt)
            elif (inSeriesType == seriesType.frequency):
                s.attachAxis(self.axisYHz)
            else:
                print("ERROR")

        s.append(self.timeStamper.getCurrent(), float(value))

        #self.chart.createDefaultAxes()
        #self.chart.axisX(s).setRange(self.timeStamper.getCurrent() - self.timeStamper.overflow, self.timeStamper.getCurrent())
        self.axisX.setRange(self.timeStamper.getCurrent() - self.timeStamper.overflow, self.timeStamper.getCurrent())

#        points_within_range = [point for point in s.pointsVector() if x_min <= point.x() <= x_max]
        for point in s.pointsVector():
            if point.x() < (self.timeStamper.getCurrent() - self.timeStamper.overflow):
                s.remove(point)
#        self.chart.axisY(s).setRange(min, max)
