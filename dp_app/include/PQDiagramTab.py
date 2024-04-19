from include.UIs.PQDiagramTab_ui import Ui_PQDiagramTab
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QWidget
import pyqtgraph as pg
from math import sqrt
import pandas as pd

# import numpy as np


# pyuic6 dp-qtdesktopapp/include/UIs/PQDiagramTab.ui -o dp-qtdesktopapp/include/UIs/PQDiagramTab_ui.py
class PQDiagramTab(QWidget, Ui_PQDiagramTab):
    def __init__(self):
        super(PQDiagramTab, self).__init__()
        self.setupUi(self)

        # Set background colour - default window color background
        xyGraphBGcolor = self.palette().color(QPalette.ColorRole.Window)
        self.PQGraph.setBackground(xyGraphBGcolor)
        self.PQGraph.setTitle("Avg.3P[kW] vs Avg.3Q[kvar]", color="k", size="16pt")
        self.PQGraph.addLegend(offset=-1)
        self.PQGraph.showGrid(x=True, y=True)

        self.pqPlot = self.PQGraph.getPlotItem()
        self.mainPen = pg.mkPen(color="#4393c3", width=2, style=Qt.PenStyle.SolidLine)
        self.pqPlot.setTitle("PQ Diagram")  # type: ignore

        # Connect control signals
        self.dblSpinBoxCosPhi.valueChanged.connect(self.updateCosPhiLines)
        self.hSliderCosPhi.valueChanged.connect(self.updateCosPhiLines)

        # Set initial values
        self.cosPhi = self.dblSpinBoxCosPhi.value()
        self.labelCosPhiValue.setText(f"{self.cosPhi:.2f}")  # type: ignore

        self.fallRisePen = pg.mkPen(color="#d6604d", width=2, style=Qt.PenStyle.DashLine)

    def loadData(self, dataFrame):
        self.df = dataFrame.copy()

        # Get name of the first column with "Time"
        self.timeColName = [col for col in dataFrame.columns if "Time" in col][0]

        self.processData()

        # series to list
        self.dataX = self.df["Avg.3Q[kvar]"].tolist()
        self.dataY = self.df["Avg.3P[kW]"].tolist()

        # Check if the csvDataRef exists (if Import CSV is called multiple times)
        if hasattr(self, "csvDataRef"):
            self.pqPlot.removeItem(self.csvDataRef)  # type: ignore
        # Plot the loaded data
        self.csvDataRef = self.PQGraph.plot(self.dataX, self.dataY, pen=self.mainPen, name="Avg.3P[kW] vs Avg.3Q[kvar]")

        # Y-Axis
        yLabelStyles = {"color": "#4393c3", "font": "Times", "font-size": "12pt"}
        self.pqPlot.setLabel("left", "Avg.3P[kW]", **yLabelStyles)  # type: ignore

        # X-Axis
        xLabelStyles = {"color": "#4393c3", "font": "Times", "font-size": "12pt"}
        self.pqPlot.setLabel("bottom", "Avg.3Q[kvar]", **xLabelStyles)  # type: ignore

        # CosPhi Fall & Rise Lines
        # Generate data frame for the lines
        self.cosPhiLinesData = pd.DataFrame()  # ["X-", "X+", "Y-", "Y+"])
        # REVIEW Don't hardcode 1501 and is it needed to make an array of so many elements?
        # TODO Use InfiniteLine???
        # Calculate the slopes for the Cos Phi Fall & Rise lines
        self.calculateFallRiseLines()

        # Plot the lines
        if hasattr(self, "fallLineRef"):
            self.pqPlot.removeItem(self.fallLineRef)  # type: ignore
        self.fallLineRef = self.PQGraph.plot(
            self.cosPhiLinesData["X-"], self.cosPhiLinesData["Y-"], pen=self.fallRisePen, name="cos(φ)"
        )

        if hasattr(self, "riseLineRef"):
            self.pqPlot.removeItem(self.riseLineRef)  # type: ignore
        self.riseLineRef = self.PQGraph.plot(
            self.cosPhiLinesData["X+"], self.cosPhiLinesData["Y+"], pen=self.fallRisePen
        )  # , name="cosPhi/"

    def processData(self):
        pass

    @pyqtSlot()
    def updateCosPhiLines(self):
        sender = self.sender()  # type: ignore
        self.cosPhi = sender.value()  # type: ignore
        if sender is not self.dblSpinBoxCosPhi:
            self.cosPhi /= 100

        self.calculateFallRiseLines()

        self.fallLineRef.setData(self.cosPhiLinesData["X-"], self.cosPhiLinesData["Y-"])  # Update Fall Line data ref
        self.riseLineRef.setData(self.cosPhiLinesData["X+"], self.cosPhiLinesData["Y+"])  # Update Fall Line data ref

        # Update actual cosPhi value on indicator and control
        self.labelCosPhiValue.setText(f"{self.cosPhi:.2f}")  # type: ignore

    def calculateFallRiseLines(self):
        self.fallSlope = sqrt(1 - self.cosPhi**2) * -1
        self.riseSlope = sqrt(1 - self.cosPhi**2)
        self.cosPhiLinesData["X-"] = [(x * self.fallSlope) for x in range(0, 1501, 500)]
        self.cosPhiLinesData["Y-"] = range(0, 1501, 500)
        self.cosPhiLinesData["X+"] = [(x * self.riseSlope) for x in range(0, 1501, 500)]
        self.cosPhiLinesData["Y+"] = range(0, 1501, 500)

    def setMeasurementDate(self, measDate):
        self.labelMeasDateValue.setText(measDate)
