import sys
from random import randint, uniform

import numpy as np
import pyqtgraph as pg
from include.UIs.PQDiagramTab_ui import Ui_PQDiagramTab
from PyQt6.QtCore import QStringListModel, Qt, QTimer
from PyQt6.QtGui import QFont, QPalette
from PyQt6.QtWidgets import QWidget


# pyuic6 dp-qtdesktopapp/include/UIs/PQDiagramTab.ui -o dp-qtdesktopapp/include/UIs/PQDiagramTab_ui.py
class PQDiagramTab(QWidget, Ui_PQDiagramTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        channels = ["CH0", "CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7"]
        comboBoxChnlSelModel = QStringListModel(channels)
        self.comboBoxChannelSelect.setModel(comboBoxChnlSelModel)
        self.comboBoxChannelSelect.currentTextChanged.connect(
            self.adcChannelChanged
        )

        # Set background colour - default window color background
        graphBGcolor = self.palette().color(QPalette.ColorRole.Base)
        self.graphWidget.setBackground(graphBGcolor)
        self.graphWidget.setTitle("Měření", color="k", size="18pt")
        # self.graphWidget.addLegend(offset=20)
        self.graphWidget.showGrid(x=True, y=True)

        # Timer initialization - for plot data updating
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updatePlotData)
        self.timer.timeout.connect(self.updateLineEditsVoltageData)
        self.timer.start()

        self.pen = pg.mkPen(color="b", width=2, style=Qt.PenStyle.SolidLine)
        self.time = list(range(100))  # 100 time points
        self.voltage = [
            uniform(23.75, 24.15) for _ in range(100)
        ]  # 100 data points
        self.lineDataRef = self.graphWidget.plot(
            self.time, self.voltage, pen=self.pen
        )
        self.adcChannelPlot = self.graphWidget.getPlotItem()
        self.adcChannelPlot.setLabel("left", "napětí", units="V")
        self.adcChannelPlot.getAxis("left").label.setFont(QFont("Times", 12))
        self.adcChannelPlot.setLabel("bottom", "čas", units="s")
        self.adcChannelPlot.getAxis("bottom").label.setFont(QFont("Times", 12))
        self.adcChannelPlot.setTitle(
            "ADC {}".format(self.comboBoxChannelSelect.currentText())
        )

    def adcChannelChanged(self):
        self.adcChannelPlot.setTitle(
            "ADC {}".format(self.comboBoxChannelSelect.currentText())
        )

        self.voltage = [uniform(23.75, 24.15) for _ in range(100)]
        self.lineDataRef.setData(
            self.time, self.voltage
        )  # Update the line data ref

    def updatePlotData(self):
        self.time = self.time[1:]  # Remove the 1st element of time vector
        self.time.append(self.time[-1] + 1)

        self.voltage = self.voltage[1:]  # Remove the 1st element of voltage
        self.voltage.append(uniform(23.75, 24.15))  # Add a new random value

        self.lineDataRef.setData(
            self.time, self.voltage
        )  # Update the line data ref

    # TODO: Hardcoded random values - should be obtained from SAM D21
    def updateLineEditsVoltageData(self):
        # Value string must be max 6 chars long
        self.lineEdit_vdd.setText(str(round(uniform(23.75, 24.15), 3)) + " V")
        self.lineEdit_5v.setText(str(round(uniform(4.90, 5.2), 3)) + " V")
        self.lineEdit_4v.setText(str(round(uniform(3.85, 4.100), 3)) + " V")
        self.lineEdit_3v3.setText(str(round(uniform(3.150, 3.45), 3)) + " V")
        self.lineEdit_vcc.setText(str(round(uniform(23.75, 24.15), 3)) + " V")
        self.lineEdit_air.setText(str(round(uniform(23.75, 24.15), 3)) + " V")
        self.lineEdit_do1.setText(str(round(uniform(23.75, 24.15), 3)) + " V")
        self.lineEdit_do0.setText(str(round(uniform(23.75, 24.15), 3)) + " V")

    # TODO: finish
    def saveMeasuredData(self):
        x = np.linspace(0, 1, 201)
        y = np.random.random(201)

        np.savetxt("testData.dat", [x, y])
