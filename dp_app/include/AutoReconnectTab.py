from include.UIs.AutoReconnectTab_ui import Ui_AutoReconnectTab
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QPalette, QPainterPath, QFont, QTransform, QColor
from PyQt6.QtWidgets import QWidget
import pyqtgraph as pg
import dp_app.include.fileTools as ft
import pandas as pd
import numpy as np
from datetime import datetime
from os import path
from collections import namedtuple

appBaseDir = path.abspath(path.join(__file__, "../.."))

TextSymbol = namedtuple("TextSymbol", "label symbol scale")


class AutoReconnectTab(QWidget, Ui_AutoReconnectTab):
    def __init__(self):
        super(AutoReconnectTab, self).__init__()
        self.setupUi(self)

        # Read settings from configuration file
        self.readConfig()

        # # Set background color - default window color background
        # xyGraphBGcolor = self.palette().color(QPalette.ColorRole.Base)
        # self.XYGraph.setBackground(xyGraphBGcolor)
        # self.XYGraph.addLegend(offset=10)

        # Get Plot Item from UI
        self.xyPlotItem = self.XYGraph.getPlotItem()
        self.y1ViewBox = self.xyPlotItem.getViewBox()  # type: ignore
        self.xyPlotItem.setTitle("XY Graph")  # type: ignore

        self.formatPlots()

        # Setup a SignalProxy and connect it to a mouseMoved method
        # Whenever the mouse is moved over the plot, the mouseMoved is called with an event as an argument
        self.proxy = pg.SignalProxy(self.XYGraph.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        # Connect sigMouseClicked signal of pItem1 to onGraphClick method
        self.xyPlotItem.scene().sigMouseClicked.connect(self.onGraphClick)  # type: ignore

        # Create a new ViewBox, link the right axis to its coordinate system
        self.y2ViewBox = pg.ViewBox()
        self.xyPlotItem.showAxis("right")  # type: ignore
        self.xyPlotItem.scene().addItem(self.y2ViewBox)  # type: ignore
        self.xyPlotItem.getAxis("right").linkToView(self.y2ViewBox)  # type: ignore
        self.y2ViewBox.setXLink(self.xyPlotItem)

        # Connect btnAutoReconnect button to testButtonPressed method
        self.btnAutoReconnect.clicked.connect(self.testButtonPressed)

        # Init Tab variables
        self.testActivated = False
        self.seqCount = 0
        self.clickCount = 0
        self.clickDataX = []
        self.clickDataY = []
        self.ptsPerSeq = 3

    def readConfig(self):
        # Read the real_power_3ph from the INI config file
        self.realPower3ph = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.pq_diagram",
            "real_power_3ph",
        )

        # Read the right_axis_digital_signal from the INI config file
        self.y2AxisSignal = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.auto_connect",
            "right_axis_digital_signal",
        )

        # Read the real_power_3ph_nominal from the INI config file
        self.realPwr3phNom = float(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.auto_connect",
                "real_power_3ph_nominal",
            )
        )

        # Read the moving_avg_window_size from the INI config file
        self.movAvgWinSize = int(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.auto_connect",
                "moving_avg_window_size",
            )
        )

        # Read the zoom_ratio from the INI config file
        self.zoomRatio = int(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.auto_connect",
                "zoom_ratio",
            )
        )

        # Read the click_point_symbol from the INI config file
        self.clickPtSymbol = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.plots",
            "click_point_symbol",
        )

        # Read the click_point_symbol_size from the INI config file
        self.clickPtSymbolSize = int(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.plots",
                "click_point_symbol_size",
            )
        )

        # Read the click_point_x_offset from the INI config file
        self.clickPtOffsetX = int(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.plots",
                "click_point_x_offset",
            )
        )

        # Read the click_point_y_offset from the INI config file
        self.clickPtOffsetY = int(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.plots",
                "click_point_y_offset",
            )
        )

        # Read the click_point_label_size from the INI config file
        self.clickPtLabelSize = int(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.plots",
                "click_point_label_size",
            )
        )

    def formatPlots(self):
        # Set background color - default window color background
        plotBGcolor = self.palette().color(QPalette.ColorRole.Base)
        self.XYGraph.setBackground(plotBGcolor)
        self.XYGraph.addLegend(offset=10)

        # Define plot colors
        self.plotColors = ["#4393C3", "#B2182B"]

        # Define label styles for all axes
        self.xLabelStyle = {"font": "Times", "font-size": "12pt"}
        self.yLabelStyles = [{"color": color, "font": "Times", "font-size": "12pt"} for color in self.plotColors]

        # X-Axes - Set as pg.DateAxisItem
        self.XYGraph.setAxisItems({"bottom": pg.DateAxisItem(orientation="bottom")})

        # Turn on the grids
        self.XYGraph.showGrid(x=True, y=True, alpha=0.6)  # type: ignore

        # Define pen style for each plot
        self.yPens = [pg.mkPen(color=color, width=2, style=Qt.PenStyle.SolidLine) for color in self.plotColors]

        # Define, create and add crosshair lines
        self.crosshairColors = ["#648200", "#FFDE59", "#C0FF00"]
        crosshairPen = pg.mkPen(color=self.crosshairColors[0], width=1, style=Qt.PenStyle.SolidLine)

        self.hCrosshair = pg.InfiniteLine(angle=0, pen=crosshairPen)
        self.vCrosshair = pg.InfiniteLine(angle=90, pen=crosshairPen)

        self.XYGraph.addItem(self.vCrosshair, ignoreBounds=True)  # type: ignore
        self.XYGraph.addItem(self.hCrosshair, ignoreBounds=True)  # type: ignore

        # Define and add cursor label
        self.cursorLabel = pg.TextItem(anchor=(-0.02, 1))
        self.XYGraph.addItem(self.cursorLabel, ignoreBounds=True)  # type: ignore

        # Set cursor over the plots as small cross
        self.XYGraph.setCursor(Qt.CursorShape.CrossCursor)

        # Init Scatter Plot Items for symbol and text inserting to plot area
        self.scatterPoints = pg.ScatterPlotItem(
            symbol=self.clickPtSymbol,
            pen=pg.mkPen(None),
            brush=pg.mkBrush(QColor("black")),
            size=self.clickPtSymbolSize,
            hoverable=True,
        )
        self.y1ViewBox.addItem(self.scatterPoints)  # type: ignore

        self.scatterLabels = pg.ScatterPlotItem(
            pen=pg.mkPen(None),  # QColor("black"), width=2
            brush=QColor("black"),
            size=self.clickPtLabelSize,
        )
        self.y1ViewBox.addItem(self.scatterLabels)  # type: ignore
        # self.scatterLabels.sigClicked.connect(self.scatterPointsClicked)

    def loadData(self, dataFrame):
        # Get name of the first column with "Time"
        self.timeColName = [col for col in dataFrame.columns if "Time" in col][0]

        # Make a reference to the dataFrame and copy only the timeColName column (will be processed subsequently)
        self.df = dataFrame.loc[:, dataFrame.columns != self.timeColName]
        self.df[self.timeColName] = dataFrame[self.timeColName].copy()

        self.processData()

        # series to lists
        self.xData = self.df[self.timeColName].tolist()[: int(self.df.shape[0] / self.zoomRatio)]
        self.yData = [
            self.df[self.realPower3ph].tolist()[: int(self.df.shape[0] / self.zoomRatio)],
            self.df[self.y2AxisSignal].tolist()[: int(self.df.shape[0] / self.zoomRatio)],
        ]

        # lists averaging
        sizeCorrection = 0
        if self.movAvgWinSize % 2 != 0:
            sizeCorrection = 1
        halfWin = int(self.movAvgWinSize / 2)
        self.xData = self.xData[halfWin + sizeCorrection : -halfWin + 1]
        self.yData[0] = self.movAvgConvolve(self.yData[0], self.movAvgWinSize)
        self.yData[1] = self.yData[1][halfWin + sizeCorrection : -halfWin + 1]

        self.xyPlotItem.setTitle(f"P [kW] & Button [] vs {self.timeColName}")  # type: ignore

        # X-Axis
        self.xyPlotItem.setLabel("bottom", self.timeColName, **self.xLabelStyle)  # type: ignore
        # self.xyPlotItem.getAxis("bottom").enableAutoSIPrefix(False)  # type: ignore

        # Y-Axes
        self.yNames = ["P [kW]", "Button []"]

        self.xyPlotItem.setLabel("left", "P [kW]", **self.yLabelStyles[0])  # type: ignore
        # Check if the y1LineRef exists (if Import CSV is called multiple times)
        if hasattr(self, "y1LineRef"):
            self.xyPlotItem.removeItem(self.y1LineRef)  # type: ignore
        self.y1LineRef = self.XYGraph.plot(self.xData, self.yData[0], pen=self.yPens[0], name="P [kW]")

        self.xyPlotItem.setLabel("right", self.yNames[1], **self.yLabelStyles[1])  # type: ignore
        if hasattr(self, "y2LineRef"):
            self.y2ViewBox.removeItem(self.y2LineRef)  # type: ignore
            self.xyPlotItem.legend.removeItem(self.y2LineRef)  # type: ignore
        self.y2LineRef = pg.PlotCurveItem(pen=self.yPens[1], name=self.yNames[1])
        self.y2ViewBox.addItem(self.y2LineRef)
        self.y2LineRef.setData(self.xData, self.yData[1])
        self.changeLegendLabel(self.xyPlotItem, self.y2LineRef, self.yNames[1])

        # Hide the cursor over the plot
        self.XYGraph.setCursor(Qt.CursorShape.BlankCursor)

        self.xyPlotItem.getViewBox().sigResized.connect(self.updateViews)  # type: ignore

        self.updateViews()

    def processData(self):
        # Convert datetime to timestamp
        self.df[self.timeColName] = self.df[self.timeColName].apply(pd.Timestamp.timestamp)

    def movAvgConvolve(self, array, n=10):
        weights = np.ones(n) / n
        return np.convolve(array, weights, mode="valid")

    # Handle view resizing
    @pyqtSlot()
    def updateViews(self):
        # View has resized; update auxiliary views to match
        self.y2ViewBox.setGeometry(self.xyPlotItem.getViewBox().sceneBoundingRect())  # type: ignore

        # Need to re-update linked axes since this was called incorrectly while views had different shapes
        # (probably this should be handled in ViewBox.resizeEvent)
        self.y2ViewBox.linkedViewChanged(self.xyPlotItem.getViewBox(), self.y2ViewBox.XAxis)  # type: ignore

    def mouseMoved(self, event):
        # event[0] holds a positional argument
        pos = event[0]
        # Checks if data has been loaded
        if hasattr(self, "xData"):
            if self.XYGraph.sceneBoundingRect().contains(pos):
                mousePoint = self.XYGraph.getPlotItem().vb.mapSceneToView(pos)  # type: ignore

                # Find closest index of clicked value
                xClosestVal = min(self.xData, key=lambda x: abs(x - mousePoint.x()))
                index = self.xData.index(xClosestVal)
                if 0 < index < len(self.xData):
                    # Update cursorLabel text
                    self.cursorLabel.setText(
                        f"x={datetime.fromtimestamp(self.xData[index]).strftime('%H:%M:%S.%f')}, "
                        + f"y={self.yData[0][index]:0.3f}",
                        color="k",
                    )
                    self.cursorLabel.setPos(mousePoint.x(), mousePoint.y())
                    self.hCrosshair.setPos(mousePoint.y())
                    self.vCrosshair.setPos(mousePoint.x())

    def onGraphClick(self, event):
        # items = self.xyPlotItem.scene().items(event.scenePos())  # type: ignore
        # print(items)  # All clicked items
        if self.xyPlotItem.sceneBoundingRect().contains(event._scenePos):  # type: ignore
            mousePoint = self.y1ViewBox.mapSceneToView(event._scenePos)  # type: ignore
            # # Convert obtained float value to datetime with time zone info
            # xVal2DateTime = pd.to_datetime(mousePoint.x(), unit="s")
            # myTimeZone = pytz.timezone("Europe/Prague")
            # dateTimeWithTimeZone = myTimeZone.localize(xVal2DateTime)

            if hasattr(self, "xData"):
                xClosestVal = min(self.xData, key=lambda x: abs(x - mousePoint.x()))
                index = self.xData.index(xClosestVal)

                if self.testActivated and 0 < index < len(self.xData):
                    self.clickDataX += [self.xData[index]]
                    self.clickDataY += [self.yData[0][index]]
                    self.clickCount += 1
                    if self.clickCount < self.ptsPerSeq:
                        self.textTestInfo.setPlainText(f"{self.ptsPerSeq-self.clickCount} clicks to graph remaining...")
                    else:
                        self.clickCount = 0
                        self.btnAutoReconnect.setChecked(False)
                        self.testActivated = False
                        self.textTestInfo.setPlainText("Test completed")

                        # Process Data
                        self.labelSystemDelayVal.setText(f"{self.getTimeDelay(self.clickDataX)/60:.3f} min")
                        self.labelGradientVal.setText(
                            f"{self.getGradient(self.clickDataX, self.clickDataY)/self.realPwr3phNom*6000:.2f} %Pn/min"
                        )
                        self.labelRiseTimeVal.setText(f"{self.getRiseTime(self.clickDataX)/60:.3f} min")

                        # Update scatterPoints data points
                        actStartIdx = self.seqCount * self.ptsPerSeq + 1
                        self.scatterPoints.setData(
                            self.clickDataX,
                            self.clickDataY,
                            data=[actStartIdx + i for i in range(len(self.clickDataX))],
                        )

                        # Update scatterLabels data points
                        self.scatterLabels.clear()
                        actStartIdx = self.seqCount * self.ptsPerSeq + 1
                        spots = [
                            {
                                "pos": [
                                    self.clickDataX[i] + self.clickPtOffsetX,
                                    self.clickDataY[i] + self.clickPtOffsetY,
                                ],
                                "symbol": label[1],
                            }
                            for (i, label) in [
                                (i, self.createLabel(str(actStartIdx + i), 0)) for i in range(len(self.clickDataX))
                            ]
                        ]
                        self.scatterLabels.addPoints(spots)

                        self.seqCount += 1

    @pyqtSlot(bool)
    def testButtonPressed(self, btnState):
        self.testActivated = btnState
        self.clickCount = 0
        # Clean lists
        self.clickDataX = []
        self.clickDataY = []

        if btnState:
            self.textTestInfo.setPlainText(f"{self.ptsPerSeq} clicks to graph remaining...")
        else:
            self.textTestInfo.clear()

    def changeLegendLabel(self, plot, plotItem, name):
        # Change the label of given PlotDataItem in the plot's legend
        plot.legend.removeItem(plotItem)
        plot.legend.addItem(plotItem, name)

    def setMeasurementDate(self, measDate):
        self.labelMeasDateValue.setText(measDate)

    def getTimeDelay(self, dataX):
        return dataX[1] - dataX[0]

    def getGradient(self, dataX, dataY):
        return (dataY[-1] - dataY[-2]) / (dataX[-1] - dataX[-2])  # in (kW/kvar) / sec

    def getRiseTime(self, dataX):
        return dataX[-1] - dataX[-2]

    def createLabel(self, label, angle):
        symbol = QPainterPath()
        symbol.addText(-0.5, 0.5, QFont("Times", 12), label)
        br = symbol.boundingRect()
        scale = min(1.0 / br.width(), 1.0 / br.height())
        tr = QTransform()
        tr.scale(scale, scale)
        tr.rotate(angle)
        tr.translate(-br.x() - br.width() / 2.0, -br.y() - br.height() / 2.0)
        return TextSymbol(label, tr.map(symbol), 0.1 / scale)

    # # TODO: Finish saving the data
    # def saveMeasuredData(self):
    #     # dataToSave = [
    #     #     self.labelSystemDelayVal.text(),
    #     #     self.labelGradientVal.text(),
    #     #     self.labelRiseTimeVal.text(),
    #     #     self.labelSetpointErrVal.text(),
    #     # ]

    #     # x = np.linspace(0, 1, 201)
    #     # y = np.random.random(201)

    #     # np.savetxt("testData.dat", [x, y])
    #     pass
