from include.UIs.XYGraphTab_ui import Ui_XYGraphTab
from dp_app.include.pgTimeAxis import DateAxisItem
from PyQt6.QtCore import Qt, pyqtSlot, QStringListModel
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QWidget
import pyqtgraph as pg
import pandas as pd

# import numpy as np


# pyuic6 dp-qtdesktopapp/include/UIs/XYGraphTab.ui -o dp-qtdesktopapp/include/UIs/XYGraphTab_ui.py
class XYGraphTab(QWidget, Ui_XYGraphTab):
    def __init__(self):
        super(XYGraphTab, self).__init__()
        self.setupUi(self)

        # Set background colour - default window color background
        xyGraphBGcolor = self.palette().color(QPalette.ColorRole.Base)
        self.XYGraph.setBackground(xyGraphBGcolor)
        self.XYGraph.setTitle("Graph Title", color="k", size="16pt")
        self.XYGraph.addLegend(offset=10)

        self.xyPlot = self.XYGraph.getPlotItem()
        self.xyPlot.setTitle("XY Graph")  # type: ignore

        self.penY1 = pg.mkPen(color="#4393c3", width=2, style=Qt.PenStyle.SolidLine)
        self.penY2 = pg.mkPen(color="#b2182b", width=2, style=Qt.PenStyle.SolidLine)

        self.xLabelStyles = {"font": "Times", "font-size": "12pt"}
        self.y1LabelStyles = {"color": "#4393c3", "font": "Times", "font-size": "12pt"}
        self.y2LabelStyles = {"color": "#b2182b", "font": "Times", "font-size": "12pt"}

        # X-Axis (DateTime)
        # Remove the old item to not get message from QGridLayoutEngine: Cell (3, 1) already taken
        old_item = self.xyPlot.layout.itemAt(3, 1)  # type: ignore
        self.xyPlot.layout.removeItem(old_item)  # type: ignore

        # Add the Date-time axis
        self.xAxis = DateAxisItem(orientation="bottom")
        self.xAxis.attachToPlotItem(self.xyPlot)
        self.xyPlot.showGrid(x=True, y=True, alpha=0.5)  # type: ignore

        # Create a new ViewBox, link the right axis to its coordinate system
        self.viewBoxY2 = pg.ViewBox()
        self.xyPlot.showAxis("right")  # type: ignore
        self.xyPlot.scene().addItem(self.viewBoxY2)  # type: ignore
        self.xyPlot.getAxis("right").linkToView(self.viewBoxY2)  # type: ignore
        self.viewBoxY2.setXLink(self.xyPlot)

        # Add crosshair lines
        crosshairPen = pg.mkPen(color="#648200", width=1, style=Qt.PenStyle.SolidLine)  # #c0ff00
        self.crosshair_v = pg.InfiniteLine(angle=90, pen=crosshairPen)
        self.crosshair_h = pg.InfiniteLine(angle=0, pen=crosshairPen)
        self.XYGraph.addItem(self.crosshair_v, ignoreBounds=True)  # type: ignore
        self.XYGraph.addItem(self.crosshair_h, ignoreBounds=True)  # type: ignore

        # Setup a SignalProxy and connect it to a updateCrosshair method
        # Whenever the mouse is moved over the plot, the updateCrosshair is called with an event as an argument
        self.proxy = pg.SignalProxy(self.XYGraph.scene().sigMouseMoved, rateLimit=60, slot=self.updateCrosshair)

        # Hide the cursor over the plot
        cursor = Qt.CursorShape.BlankCursor
        self.XYGraph.setCursor(cursor)

        self.viewBoxY1 = self.xyPlot.getViewBox()  # type: ignore
        self.xyPlot.scene().sigMouseClicked.connect(self.onClick)  # type: ignore

    def loadData(self, dataFrame):
        # Get name of the first column with "Time"
        self.timeColName = [col for col in dataFrame.columns if "Time" in col][0]

        # Make a reference to the dataFrame and copy only the timeColName column (will be processed subsequently)
        self.df = dataFrame.loc[:, dataFrame.columns != self.timeColName]
        self.df[self.timeColName] = dataFrame[self.timeColName].copy()

        self.processData()

        # series to list
        self.dataX = self.df[self.cBoxXData.currentText()].tolist()
        self.dataY1 = self.df[self.cBoxY1Data.currentText()].tolist()
        self.dataY2 = self.df[self.cBoxY2Data.currentText()].tolist()

        self.xyPlot.setTitle(  # type: ignore
            f"{self.cBoxY1Data.currentText()} & {self.cBoxY2Data.currentText()} vs {self.cBoxXData.currentText()}"
        )

        # Y1-Axis
        self.xyPlot.setLabel("left", self.cBoxY1Data.currentText(), **self.y1LabelStyles)  # type: ignore

        # Check if the y1LineRef exists (if Import CSV is called multiple times)
        if hasattr(self, "y1LineRef"):
            self.xyPlot.removeItem(self.y1LineRef)  # type: ignore
        self.y1LineRef = self.XYGraph.plot(self.dataX, self.dataY1, pen=self.penY1, name=self.cBoxY1Data.currentText())

        # Y2-Axis
        self.xyPlot.setLabel("right", self.cBoxY2Data.currentText(), **self.y2LabelStyles)  # type: ignore
        if hasattr(self, "y2LineRef"):
            self.viewBoxY2.removeItem(self.y2LineRef)  # type: ignore
            self.xyPlot.legend.removeItem(self.y2LineRef)  # type: ignore
        self.y2LineRef = pg.PlotCurveItem(pen=self.penY2, name=self.cBoxY2Data.currentText())
        self.viewBoxY2.addItem(self.y2LineRef)
        self.y2LineRef.setData(self.dataX, self.dataY2)
        self.changeLegendLabel(self.xyPlot, self.y2LineRef, self.cBoxY2Data.currentText())

        # X-Axis (DateTime)
        self.xyPlot.setLabel("bottom", self.cBoxXData.currentText(), **self.xLabelStyles)  # type: ignore
        self.xyPlot.getAxis("bottom").enableAutoSIPrefix(False)  # type: ignore

        self.cBoxXData.currentTextChanged.connect(self.updatePlotData)
        self.cBoxY1Data.currentTextChanged.connect(self.updatePlotData)
        self.cBoxY2Data.currentTextChanged.connect(self.updatePlotData)

        self.xyPlot.getViewBox().sigResized.connect(self.updateViews)  # type: ignore

    def processData(self):
        # Convert datetime to timestamp
        self.df[self.timeColName] = self.df[self.timeColName].apply(pd.Timestamp.timestamp)

    @pyqtSlot()
    def updatePlotData(self):
        sender = self.sender()  # type: ignore

        self.xyPlot.setTitle(  # type: ignore
            f"{self.cBoxY1Data.currentText()} & {self.cBoxY2Data.currentText()} vs {self.cBoxXData.currentText()}"
        )
        if sender is self.cBoxXData:
            self.xyPlot.setLabel("bottom", self.cBoxXData.currentText())  # type: ignore
            self.dataX = self.df[self.cBoxXData.currentText()].tolist()
        elif sender is self.cBoxY1Data:
            self.xyPlot.setLabel("left", self.cBoxY1Data.currentText())  # type: ignore
            self.dataY1 = self.df[self.cBoxY1Data.currentText()].tolist()
        elif sender is self.cBoxY2Data:
            self.xyPlot.setLabel("right", self.cBoxY2Data.currentText())  # type: ignore
            self.dataY2 = self.df[self.cBoxY2Data.currentText()].tolist()

        self.y1LineRef.setData(self.dataX, self.dataY1)  # Update the Y1 line data ref
        self.y2LineRef.setData(self.dataX, self.dataY2)  # Update the Y2 line data ref

        self.changeLegendLabel(self.xyPlot, self.y1LineRef, self.cBoxY1Data.currentText())
        self.changeLegendLabel(self.xyPlot, self.y2LineRef, self.cBoxY2Data.currentText())

        self.updateViews()

    # Handle view resizing
    def updateViews(self):
        # View has resized; update auxiliary views to match
        self.viewBoxY2.setGeometry(self.xyPlot.getViewBox().sceneBoundingRect())  # type: ignore

        # Need to re-update linked axes since this was called incorrectly while views had different shapes
        # (probably this should be handled in ViewBox.resizeEvent)
        self.viewBoxY2.linkedViewChanged(self.xyPlot.getViewBox(), self.viewBoxY2.XAxis)  # type: ignore

    def setComboBoxesDataModel(self, headers=[]):
        self.cBoxXDataModel = QStringListModel([headers[0]])
        self.cBoxXData.setModel(self.cBoxXDataModel)
        self.cBoxXData.setCurrentIndex(0)

        self.cBoxY1DataModel = QStringListModel(headers[1:])  # without Time column
        self.cBoxY1Data.setModel(self.cBoxY1DataModel)
        self.cBoxY1Data.setCurrentIndex(0)

        self.cBoxY2DataModel = QStringListModel(headers[1:])  # without Time column
        self.cBoxY2Data.setModel(self.cBoxY2DataModel)
        self.cBoxY2Data.setCurrentIndex(1)

    def updateCrosshair(self, event):
        # event[0] holds a positional argument
        pos = event[0]
        if self.XYGraph.sceneBoundingRect().contains(pos):
            mousePoint = self.XYGraph.getPlotItem().vb.mapSceneToView(pos)  # type: ignore
            self.crosshair_v.setPos(mousePoint.x())
            self.crosshair_h.setPos(mousePoint.y())

    def onClick(self, event):
        # items = self.xyPlot.scene().items(event.scenePos())
        mousePoint = self.viewBoxY1.mapSceneToView(event._scenePos)  # type: ignore
        print(mousePoint.x(), mousePoint.y())
        if self.xyPlot.sceneBoundingRect().contains(event._scenePos):  # type: ignore
            mousePoint = self.viewBoxY1.mapSceneToView(event._scenePos)  # type: ignore
            # # Convert obtained float value to datetime with time zone info
            # xVal2DateTime = pd.to_datetime(mousePoint.x(), unit="s")
            # myTimeZone = pytz.timezone("Europe/Prague")
            # dateTimeWithTimeZone = myTimeZone.localize(xVal2DateTime)

            self.labelDataClick1.setText(f"X={mousePoint.x()}, Y1={mousePoint.y():.3f}")

    def setMeasurementDate(self, measDate):
        self.labelMeasDateValue.setText(measDate)

    def changeLegendLabel(self, plot, plotItem, name):
        # Change the label of given PlotDataItem in the plot's legend
        plot.legend.removeItem(plotItem)
        plot.legend.addItem(plotItem, name)

    # # TODO: finish
    # def saveMeasuredData(self):
    #     x = np.linspace(0, 1, 201)
    #     y = np.random.random(201)

    #     np.savetxt("testData.dat", [x, y])
