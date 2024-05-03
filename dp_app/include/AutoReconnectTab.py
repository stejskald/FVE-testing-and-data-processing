from include.UIs.AutoReconnectTab_ui import Ui_AutoReconnectTab
from dp_app.include.pgTimeAxis import DateAxisItem
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QWidget
import pyqtgraph as pg
import dp_app.include.fileTools as ft
import pandas as pd
import numpy as np
from datetime import datetime
from os import path

appBaseDir = path.abspath(path.join(__file__, "../.."))


class AutoReconnectTab(QWidget, Ui_AutoReconnectTab):
    def __init__(self):
        super(AutoReconnectTab, self).__init__()
        self.setupUi(self)

        # Read settings from configuration file
        self.readConfig()

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
        self.xAxis = pg.DateAxisItem(orientation="bottom")
        self.xyPlot.setAxisItems({"bottom": self.xAxis})  # type: ignore
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
        self.xyPlot.scene().sigMouseClicked.connect(self.onGraphClick)  # type: ignore

        # self.xyPlot.sigRangeChanged.connect(self.update_time_axis_range)

        self.btnAutoReconnect.clicked.connect(self.testButtonPressed)
        self.testActivated = False
        self.clickCount = 0
        self.clickDataX = []
        self.clickDataY = []

    def readConfig(self):
        # Read the mean_interval_length from the INI config file
        self.meanIntervalLength = int(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.xy_graph",
                "mean_interval_length",
            )
        )

        # Read the real_power_3ph from the INI config file
        self.realPower3ph = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.pq_diagram",
            "real_power_3ph",
        )

        # Read the right_axis_digital_signal from the INI config file
        self.axisY2Signal = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.auto_connect",
            "right_axis_digital_signal",
        )

    def loadData(self, dataFrame):
        # Get name of the first column with "Time"
        self.timeColName = [col for col in dataFrame.columns if "Time" in col][0]

        # Make a reference to the dataFrame and copy only the timeColName column (will be processed subsequently)
        self.df = dataFrame.loc[:, dataFrame.columns != self.timeColName]
        self.df[self.timeColName] = dataFrame[self.timeColName].copy()

        self.processData()

        # series to list
        self.dataX = self.df[self.timeColName].tolist()
        self.dataY1 = self.df[self.realPower3ph].tolist()
        self.dataY2 = self.df[self.axisY2Signal].tolist()

        self.xyPlot.setTitle(f"{self.realPower3ph} & {self.axisY2Signal} vs {self.timeColName}")  # type: ignore

        # Y1-Axis
        self.xyPlot.setLabel("left", self.realPower3ph, **self.y1LabelStyles)  # type: ignore

        # Check if the y1LineRef exists (if Import CSV is called multiple times)
        if hasattr(self, "y1LineRef"):
            self.xyPlot.removeItem(self.y1LineRef)  # type: ignore
        self.y1LineRef = self.XYGraph.plot(self.dataX, self.dataY1, pen=self.penY1, name=self.realPower3ph)

        # Y2-Axis
        self.xyPlot.setLabel("right", self.axisY2Signal, **self.y2LabelStyles)  # type: ignore
        if hasattr(self, "y2LineRef"):
            self.viewBoxY2.removeItem(self.y2LineRef)  # type: ignore
            self.xyPlot.legend.removeItem(self.y2LineRef)  # type: ignore
        self.y2LineRef = pg.PlotCurveItem(pen=self.penY2, name=self.axisY2Signal)
        self.viewBoxY2.addItem(self.y2LineRef)
        self.y2LineRef.setData(self.dataX, self.dataY2)
        self.changeLegendLabel(self.xyPlot, self.y2LineRef, self.axisY2Signal)

        # X-Axis (DateTime)
        self.xyPlot.setLabel("bottom", self.timeColName, **self.xLabelStyles)  # type: ignore
        self.xyPlot.getAxis("bottom").enableAutoSIPrefix(False)  # type: ignore

        self.xyPlot.getViewBox().sigResized.connect(self.updateViews)  # type: ignore

        self.updateViews()

    def processData(self):
        # Convert datetime to timestamp
        self.df[self.timeColName] = self.df[self.timeColName].apply(pd.Timestamp.timestamp)

    # Handle view resizing
    @pyqtSlot()
    def updateViews(self):
        # View has resized; update auxiliary views to match
        self.viewBoxY2.setGeometry(self.xyPlot.getViewBox().sceneBoundingRect())  # type: ignore

        # Need to re-update linked axes since this was called incorrectly while views had different shapes
        # (probably this should be handled in ViewBox.resizeEvent)
        self.viewBoxY2.linkedViewChanged(self.xyPlot.getViewBox(), self.viewBoxY2.XAxis)  # type: ignore

    def updateCrosshair(self, event):
        # event[0] holds a positional argument
        pos = event[0]
        if self.XYGraph.sceneBoundingRect().contains(pos):
            mousePoint = self.XYGraph.getPlotItem().vb.mapSceneToView(pos)  # type: ignore
            self.crosshair_v.setPos(mousePoint.x())
            self.crosshair_h.setPos(mousePoint.y())

    def onGraphClick(self, event):
        # items = self.xyPlot.scene().items(event.scenePos())  # type: ignore
        # print(items)  # All clicked items
        mousePoint = self.viewBoxY1.mapSceneToView(event._scenePos)  # type: ignore
        # print(mousePoint.x(), mousePoint.y())
        if self.xyPlot.sceneBoundingRect().contains(event._scenePos):  # type: ignore
            mousePoint = self.viewBoxY1.mapSceneToView(event._scenePos)  # type: ignore
            # # Convert obtained float value to datetime with time zone info
            # xVal2DateTime = pd.to_datetime(mousePoint.x(), unit="s")
            # myTimeZone = pytz.timezone("Europe/Prague")
            # dateTimeWithTimeZone = myTimeZone.localize(xVal2DateTime)

            if self.testActivated:
                self.clickDataX += [mousePoint.x()]
                self.clickDataY += [mousePoint.y()]
                self.clickCount += 1
                if self.clickCount < 3:
                    self.textTestInfo.setPlainText(f"{3-self.clickCount} clicks to graph remaining...")
                else:
                    self.clickCount = 0
                    self.btnAutoReconnect.setChecked(False)
                    self.testActivated = False
                    self.textTestInfo.setPlainText("Test completed")

                    # Process Data
                    self.labelSystemDelayVal.setText(f"{self.getSystemDelay(self.clickDataX):.3f} s")
                    self.labelGradientVal.setText(f"{self.getGradient(self.clickDataX, self.clickDataY):.3f} kW/s")
                    self.labelRiseTimeVal.setText(f"{self.getRiseTime(self.clickDataX, self.clickDataY):.3f} s")

                    # Save lists to 2D array and clean lists
                    self.autoReconnectTestResults = np.array(
                        [
                            [datetime.fromtimestamp(item).strftime("%H:%M:%S.%f") for item in self.clickDataX],
                            self.clickDataY,
                        ]
                    )
                    print(f"{self.autoReconnectTestResults}")

    @pyqtSlot(bool)
    def testButtonPressed(self, btnState):
        self.testActivated = btnState
        self.clickCount = 0
        self.clickDataX = []
        self.clickDataY = []
        if btnState:
            self.textTestInfo.setPlainText("3 clicks to graph remaining...")
        else:
            self.textTestInfo.clear()

    def update_time_axis_range(self):
        # time_axis = self.xyPlot.getAxis("bottom")
        # # x_range = time_axis.range if x_range[1] - x_range[0] > 10: new_range = (x_range[1] - 10, x_range[1])
        # time_axis.setXRange(self.dataX[0], self.dataX[-1] / 4)
        pass

    def changeLegendLabel(self, plot, plotItem, name):
        # Change the label of given PlotDataItem in the plot's legend
        plot.legend.removeItem(plotItem)
        plot.legend.addItem(plotItem, name)

    def setMeasurementDate(self, measDate):
        self.labelMeasDateValue.setText(measDate)

    def getSystemDelay(self, dataX):
        return dataX[1] - dataX[0]

    def getGradient(self, dataX, dataY):
        return (dataY[-1] - dataY[-2]) / (dataX[-1] - dataX[-2])  # in (kW/kvar) / sec

    # TODO Implement finding the rise point and taking only interval 10% -> 90%
    def getRiseTime(self, dataX, dataY):
        return dataX[-1] - dataX[-2]

    # # TODO: Finish saving the data
    def saveMeasuredData(self):
        # dataToSave = [
        #     self.labelSystemDelayVal.text(),
        #     self.labelGradientVal.text(),
        #     self.labelRiseTimeVal.text(),
        #     self.labelSetpointErrVal.text(),
        # ]

        # x = np.linspace(0, 1, 201)
        # y = np.random.random(201)

        # np.savetxt("testData.dat", [x, y])
        pass
