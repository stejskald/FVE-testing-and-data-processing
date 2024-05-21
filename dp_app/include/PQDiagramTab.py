from include.UIs.PQDiagramTab_ui import Ui_PQDiagramTab
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QWidget
import pyqtgraph as pg
import numpy as np
from math import acos, degrees
import dp_app.include.fileTools as ft
from os import path

appBaseDir = path.abspath(path.join(__file__, "../.."))


# pyuic6 dp-qtdesktopapp/include/UIs/PQDiagramTab.ui -o dp-qtdesktopapp/include/UIs/PQDiagramTab_ui.py
class PQDiagramTab(QWidget, Ui_PQDiagramTab):
    def __init__(self):
        super(PQDiagramTab, self).__init__()
        self.setupUi(self)

        # Read settings from configuration file
        self.readConfig()

        # Set background colour - default window color background
        xyGraphBGcolor = self.palette().color(QPalette.ColorRole.Base)
        self.PQGraph.setBackground(xyGraphBGcolor)
        self.PQGraph.setTitle(f"{self.realPower3ph} vs {self.reactivePower3ph}", color="k", size="16pt")
        self.PQGraph.addLegend(offset=-1)
        self.PQGraph.showGrid(x=True, y=True)

        self.pqPlot = self.PQGraph.getPlotItem()
        self.mainPen = pg.mkPen(color="#4393c3", width=2, style=Qt.PenStyle.SolidLine)
        self.pqPlot.setTitle("PQ Diagram")  # type: ignore

        # Setup a SignalProxy and connect it to a mouseMoved method
        # Whenever the mouse is moved over the plot, the mouseMoved is called with an event as an argument
        self.proxy = pg.SignalProxy(self.PQGraph.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        # Connect control signals
        self.dblSpinBoxCosPhi.valueChanged.connect(self.updateCosPhiLines)
        self.hSliderCosPhi.valueChanged.connect(self.updateCosPhiLines)

        # Set initial values
        self.cosPhi = self.dblSpinBoxCosPhi.value()
        self.labelCosPhiValue.setText(f"{self.cosPhi:.2f}")  # type: ignore

        # Create an InfiniteLine (init as vertical)
        self.fallRisePen = pg.mkPen(color="#d6604d", width=2, style=Qt.PenStyle.DashLine)
        self.fallInfLine = pg.InfiniteLine(pos=0, angle=90, pen=self.fallRisePen)  # , name="cos(φ)")
        self.pqPlot.addItem(self.fallInfLine)  # type: ignore

        self.riseInfLine = pg.InfiniteLine(pos=0, angle=90, pen=self.fallRisePen)
        self.pqPlot.addItem(self.riseInfLine)  # type: ignore

        # Define and add cursor label
        self.cursorLabel = pg.TextItem(anchor=(-0.02, 1))
        self.PQGraph.addItem(self.cursorLabel, ignoreBounds=True)  # type: ignore

        # Set cursor over the plots as small cross
        self.PQGraph.setCursor(Qt.CursorShape.CrossCursor)

        self.drawBasicRequirementArea()

    def readConfig(self):
        # Read the real_power_3ph from the INI config file
        self.realPower3ph = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.pq_diagram",
            "real_power_3ph",
        )

        # Read the reactive_power_3ph from the INI config file
        self.reactivePower3ph = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.pq_diagram",
            "reactive_power_3ph",
        )

        # Read the real_power_3ph_nominal from the INI config file
        self.realPwr3phNom = float(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.pq_diagram",
                "real_power_3ph_nominal",
            )
        )

        # Read the moving_avg_window_size from the INI config file
        self.movAvgWinSize = int(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.pq_diagram",
                "moving_avg_window_size",
            )
        )

    def loadData(self, dataFrame):
        self.df = dataFrame.copy()

        # Get name of the first column with "Time"
        self.timeColName = [col for col in dataFrame.columns if "Time" in col][0]

        # series to list
        self.xData = self.movAvgConvolve(self.df[self.reactivePower3ph].tolist(), self.movAvgWinSize)
        self.yData = self.movAvgConvolve(self.df[self.realPower3ph].tolist(), self.movAvgWinSize)

        # Use the nominal power value to display the P/Q ratio
        self.yData = [(item / self.realPwr3phNom) for item in self.yData]
        self.xData = [(item / self.realPwr3phNom) for item in self.xData]

        # Check if the csvDataRef exists (if Import CSV is called multiple times)
        if hasattr(self, "csvDataRef"):
            self.pqPlot.removeItem(self.csvDataRef)  # type: ignore
        # Plot the loaded data
        self.csvDataRef = self.PQGraph.plot(self.xData, self.yData, pen=self.mainPen, name="P [kW] vs Q [kvar]")

        # Y-Axis
        yLabelStyles = {"color": "#4393c3", "font": "Times", "font-size": "12pt"}
        self.pqPlot.setLabel("left", "P / Pn [-]", **yLabelStyles)  # type: ignore

        # X-Axis
        xLabelStyles = {"color": "#4393c3", "font": "Times", "font-size": "12pt"}
        self.pqPlot.setLabel("bottom", "Q / Pn [-]", **xLabelStyles)  # type: ignore

        # Calculate the slopes for the Cos Phi Fall & Rise lines
        self.calcInfLinesAngles()

        self.fallInfLine.setAngle(self.fallSlope)  # Set the angle to -45 degrees
        self.riseInfLine.setAngle(self.riseSlope)  # Set the angle to 45 degrees

        # TODO Draw the gray area (see doc in OneDrive) <------------------------------------------------------

    @pyqtSlot()
    def updateCosPhiLines(self):
        # Update self.cosPhi from sender value
        sender = self.sender()  # type: ignore
        self.cosPhi = sender.value()  # type: ignore
        if sender is not self.dblSpinBoxCosPhi:
            self.cosPhi /= 100

        # Update Infinity Lines angle values
        self.calcInfLinesAngles()
        self.fallInfLine.setAngle(self.fallSlope)  # Set the angle to -45 degrees
        self.riseInfLine.setAngle(self.riseSlope)  # Set the angle to 45 degrees

        if sender is not self.dblSpinBoxCosPhi:
            # Update actual cosPhi value on indicator
            self.labelCosPhiValue.setText(f"{self.cosPhi:.2f}")  # type: ignore

    def calcInfLinesAngles(self):
        self.fallSlope = 90 - degrees(acos(self.cosPhi)) * (-1)
        self.riseSlope = 90 - degrees(acos(self.cosPhi))

    def movAvgConvolve(self, array, n=10):
        weights = np.ones(n) / n
        return np.convolve(array, weights, mode="valid")

    def mouseMoved(self, event):
        # event[0] holds a positional argument
        pos = event[0]
        # Checks if data has been loaded
        if hasattr(self, "xData"):
            if self.PQGraph.sceneBoundingRect().contains(pos):
                mousePoint = self.PQGraph.getPlotItem().vb.mapSceneToView(pos)  # type: ignore

                # Find closest index of clicked value
                xClosestVal = min(self.xData, key=lambda x: abs(x - mousePoint.x()))
                index = self.xData.index(xClosestVal)
                if 0 < index < len(self.xData):
                    # Update cursorLabel text
                    self.cursorLabel.setText(
                        f"x={self.xData[index]:0.3f}, y={self.yData[index]:0.3f}",
                        color="k",
                    )
                    self.cursorLabel.setPos(mousePoint.x(), mousePoint.y())

    def drawBasicRequirementArea(self):
        originX = 0.0
        originY = 0.0

        pen = (255, 255, 255)
        curve1 = self.PQGraph.plot(x=[originX, originX - 0.484], y=[originY, originY + 0.2], pen=pen)
        curve2 = self.PQGraph.plot(x=[originX - 0.484, originX - 0.484], y=[originY + 0.2, 1.0], pen=pen)
        curve3 = self.PQGraph.plot(x=[originX - 0.484, originX + 0.484], y=[1.0, 1.0], pen=pen)
        curve4 = self.PQGraph.plot(x=[originX + 0.484, originX + 0.484], y=[1.0, 0.2], pen=pen)
        curve5 = self.PQGraph.plot(x=[originX + 0.484, originX], y=[0.2, originY], pen=pen)

        curve00 = self.PQGraph.plot(x=[originX - 0.484, originX + 0.484], y=[originY, originY], pen=pen)
        curve0 = self.PQGraph.plot(x=[originX - 0.484, originX + 0.484], y=[0.2, 0.2], pen=(211, 211, 211))

        # Create data points for a circle
        radius = 0.1
        theta = np.linspace(0, np.pi, 1000)
        x_circle = radius * np.cos(theta) + originX  # Center at (originX, originY)
        y_circle = radius * np.sin(theta) + originY

        # Plot the circular curve
        halfCirc = self.PQGraph.plot(x_circle, y_circle, pen=pen)  # Set pen color to green

        brush = (211, 211, 211)
        brushCirc = (255, 255, 255)
        fill1 = pg.FillBetweenItem(curve0, curve3, brush)
        fill2 = pg.FillBetweenItem(curve1, curve4, brush)
        fill3 = pg.FillBetweenItem(curve5, curve2, brush)
        fill0 = pg.FillBetweenItem(curve00, halfCirc, brushCirc)

        self.PQGraph.addItem(fill1)
        self.PQGraph.addItem(fill2)
        self.PQGraph.addItem(fill3)
        self.PQGraph.addItem(fill0)

    def setMeasurementDate(self, measDate):
        self.labelMeasDateValue.setText(measDate)
