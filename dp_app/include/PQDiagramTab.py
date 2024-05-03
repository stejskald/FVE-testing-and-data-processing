from include.UIs.PQDiagramTab_ui import Ui_PQDiagramTab
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QWidget
import pyqtgraph as pg
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

        # Connect control signals
        self.dblSpinBoxCosPhi.valueChanged.connect(self.updateCosPhiLines)
        self.hSliderCosPhi.valueChanged.connect(self.updateCosPhiLines)

        # Set initial values
        self.cosPhi = self.dblSpinBoxCosPhi.value()
        self.labelCosPhiValue.setText(f"{self.cosPhi:.2f}")  # type: ignore

        self.fallRisePen = pg.mkPen(color="#d6604d", width=2, style=Qt.PenStyle.DashLine)

        # Create an InfiniteLine (init as vertical)
        self.fallInfLine = pg.InfiniteLine(pos=0, angle=90, pen=self.fallRisePen)  # , name="cos(φ)")
        self.pqPlot.addItem(self.fallInfLine)  # type: ignore

        self.riseInfLine = pg.InfiniteLine(pos=0, angle=90, pen=self.fallRisePen)
        self.pqPlot.addItem(self.riseInfLine)  # type: ignore

        # # Add crosshair lines
        # self.crosshair_v = pg.InfiniteLine(angle=90)
        # self.crosshair_h = pg.InfiniteLine(angle=0)
        # self.PQGraph.addItem(self.crosshair_v, ignoreBounds=True)  # type: ignore
        # self.PQGraph.addItem(self.crosshair_h, ignoreBounds=True)  # type: ignore

        # # Setup a SignalProxy and connect it to a updateCrosshair method
        # # Whenever the mouse is moved over the plot, the updateCrosshair is called with an event as an argument
        # self.proxy = pg.SignalProxy(self.PQGraph.scene().sigMouseMoved, rateLimit=60, slot=self.updateCrosshair)

        # # Hide the cursor over the plot
        # cursor = Qt.CursorShape.BlankCursor
        # self.PQGraph.setCursor(cursor)

        # self.vb = self.pqPlot.vb  # type: ignore
        # self.pqPlot.scene().sigMouseClicked.connect(self.onClick)  # type: ignore

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
        self.realPower3phNominal = float(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.pq_diagram",
                "real_power_3ph_nominal",
            )
        )

    def loadData(self, dataFrame):
        self.df = dataFrame.copy()

        # Get name of the first column with "Time"
        self.timeColName = [col for col in dataFrame.columns if "Time" in col][0]

        # series to list
        self.dataX = self.df[self.reactivePower3ph].tolist()
        self.dataY = self.df[self.realPower3ph].tolist()

        # Use the nominal power value to display the P/Q ratio
        self.dataY = [(item / self.realPower3phNominal) for item in self.dataY]
        self.dataX = [(item / self.realPower3phNominal) for item in self.dataX]

        # Check if the csvDataRef exists (if Import CSV is called multiple times)
        if hasattr(self, "csvDataRef"):
            self.pqPlot.removeItem(self.csvDataRef)  # type: ignore
        # Plot the loaded data
        self.csvDataRef = self.PQGraph.plot(
            self.dataX, self.dataY, pen=self.mainPen, name=f"{self.realPower3ph} vs {self.reactivePower3ph}"
        )

        # Y-Axis
        yLabelStyles = {"color": "#4393c3", "font": "Times", "font-size": "12pt"}
        self.pqPlot.setLabel("left", f"{self.realPower3ph} / Pn", **yLabelStyles)  # type: ignore

        # X-Axis
        xLabelStyles = {"color": "#4393c3", "font": "Times", "font-size": "12pt"}
        self.pqPlot.setLabel("bottom", f"{self.reactivePower3ph} / Pn", **xLabelStyles)  # type: ignore

        # Calculate the slopes for the Cos Phi Fall & Rise lines
        self.calcInfLinesAngles()

        self.fallInfLine.setAngle(self.fallSlope)  # Set the angle to -45 degrees
        self.riseInfLine.setAngle(self.riseSlope)  # Set the angle to 45 degrees

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

    # def updateCrosshair(self, event):
    #     # event[0] holds a positional argument
    #     pos = event[0]
    #     if self.PQGraph.sceneBoundingRect().contains(pos):
    #         mousePoint = self.PQGraph.getPlotItem().vb.mapSceneToView(pos)  # type: ignore
    #         self.crosshair_v.setPos(mousePoint.x())
    #         self.crosshair_h.setPos(mousePoint.y())

    # def onClick(self, event):
    #     # items = self.pqPlot.scene().items(event.scenePos())
    #     mousePoint = self.vb.mapSceneToView(event._scenePos)  # type: ignore
    #     print(mousePoint.x(), mousePoint.y())
    #     if self.pqPlot.sceneBoundingRect().contains(event._scenePos):  # type: ignore
    #         mousePoint = self.vb.mapSceneToView(event._scenePos)  # type: ignore
    #         # # Convert obtained float value to datetime with time zone info
    #         # xVal2DateTime = pd.to_datetime(mousePoint.x(), unit="s")
    #         # myTimeZone = pytz.timezone("Europe/Prague")
    #         # dateTimeWithTimeZone = myTimeZone.localize(xVal2DateTime)

    #         self.labelDataClick1.setText(f"t={mousePoint.x()}, y={mousePoint.y():.3f}")

    def setMeasurementDate(self, measDate):
        self.labelMeasDateValue.setText(measDate)
