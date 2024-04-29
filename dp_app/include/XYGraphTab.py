from include.UIs.XYGraphTab_ui import Ui_XYGraphTab
from dp_app.include.pgTimeAxis import DateAxisItem
from PyQt6.QtCore import Qt, pyqtSlot, QStringListModel
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QWidget
import pyqtgraph as pg
import dp_app.include.fileTools as ft
import pandas as pd
from os import path

appBaseDir = path.abspath(path.join(__file__, "../.."))


# pyuic6 dp-qtdesktopapp/include/UIs/XYGraphTab.ui -o dp-qtdesktopapp/include/UIs/XYGraphTab_ui.py
class XYGraphTab(QWidget, Ui_XYGraphTab):
    def __init__(self):
        super(XYGraphTab, self).__init__()
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
        self.xyPlot.scene().sigMouseClicked.connect(self.onGraphClick)  # type: ignore

        self.checkBox.stateChanged.connect(self.secondViewEnabled)

        self.dblSpinBoxSetpoint.setValue(self.setpoint)
        self.dblSpinBoxSetpoint.valueChanged.connect(self.updateSetpointError)

        self.btnAutoRephase.clicked.connect(self.processTest)
        self.btnGradient.clicked.connect(self.processTest)
        self.btnRiseTime.clicked.connect(self.processTest)
        self.btnProcessVarMaxVal.clicked.connect(self.processTest)
        self.testActivated = False
        self.clickCount = 0
        self.clickDataX = []
        self.clickDataY = []
        self.processVarMaxVal = 0

    def readConfig(self):
        # Read the setpoint from the INI config file
        self.setpoint = float(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.xy_graph",
                "setpoint",
            )
        )

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
    @pyqtSlot()
    def updateViews(self):
        # View has resized; update auxiliary views to match
        self.viewBoxY2.setGeometry(self.xyPlot.getViewBox().sceneBoundingRect())  # type: ignore

        # Need to re-update linked axes since this was called incorrectly while views had different shapes
        # (probably this should be handled in ViewBox.resizeEvent)
        self.viewBoxY2.linkedViewChanged(self.xyPlot.getViewBox(), self.viewBoxY2.XAxis)  # type: ignore

    def secondViewEnabled(self, state):
        if not state:
            self.cBoxY2Data.setDisabled(True)
            self.viewBoxY2.removeItem(self.y2LineRef)  # type: ignore
            self.xyPlot.legend.removeItem(self.y2LineRef)  # type: ignore
        else:
            if hasattr(self, "y2LineRef"):
                # self.viewBoxY2.removeItem(self.y2LineRef)  # type: ignore
                self.xyPlot.legend.removeItem(self.y2LineRef)  # type: ignore
            self.cBoxY2Data.setEnabled(True)
            self.y2LineRef = pg.PlotCurveItem(pen=self.penY2, name=self.cBoxY2Data.currentText())
            self.viewBoxY2.addItem(self.y2LineRef)
            self.y2LineRef.setData(self.dataX, self.dataY2)
            self.changeLegendLabel(self.xyPlot, self.y2LineRef, self.cBoxY2Data.currentText())

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

    def onGraphClick(self, event):
        # items = self.xyPlot.scene().items(event.scenePos())
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
                if self.mySender is self.btnAutoRephase:
                    if self.clickCount < 3:
                        self.labelTest1Info.setText(
                            f"{self.mySender.text()}: {3-self.clickCount} clicks to graph remaining..."  # type: ignore
                        )
                    else:
                        self.clickCount = 0
                        self.testActivated = False
                        self.labelTest1Info.setText(f"{self.mySender.text()}: Test completed")  # type: ignore

                        # Process Data
                        self.labelSystemDelayVal.setText(f"{self.getSystemDelay(self.clickDataX):.3f} s")
                        self.labelGradientVal.setText(
                            f"{self.getGradient(self.clickDataX, self.clickDataY):.3f} (kW/kvar)/s"
                        )
                        self.labelRiseTimeVal.setText(
                            # TODO implement searching of 10% and 90% in Y values
                            f"{self.getRiseTime(self.clickDataX, self.clickDataY):.3f} s"
                        )

                        self.findProcessVarMaxVal(self.clickDataY[2])
                        self.updateSetpointError()

                        # Clean arrays
                        self.clickDataX = []
                        self.clickDataY = []

                elif self.mySender is self.btnGradient:
                    if self.clickCount < 2:
                        self.labelTest2Info.setText(
                            f"{self.mySender.text()}: {2-self.clickCount} clicks to graph remaining..."  # type: ignore
                        )
                    else:
                        self.clickCount = 0
                        self.testActivated = False
                        self.labelTest2Info.setText(f"{self.mySender.text()}: Test completed")  # type: ignore

                        # Process Data
                        self.labelGradientVal.setText(
                            f"{self.getGradient(self.clickDataX, self.clickDataY):.3f} (kW/kvar)/s"
                        )

                        # Clean arrays
                        self.clickDataX = []
                        self.clickDataY = []

                elif self.mySender is self.btnRiseTime:
                    if self.clickCount < 2:
                        self.labelTest3Info.setText(
                            f"{self.mySender.text()}: {2-self.clickCount} clicks to graph remaining..."  # type: ignore
                        )
                    else:
                        self.clickCount = 0
                        self.testActivated = False
                        self.labelTest3Info.setText(f"{self.mySender.text()}: Test completed")  # type: ignore

                        # Process Data
                        self.labelRiseTimeVal.setText(f"{self.getRiseTime(self.clickDataX, self.clickDataY):.3f} s")

                        # Clean arrays
                        self.clickDataX = []
                        self.clickDataY = []

                elif self.mySender is self.btnProcessVarMaxVal:
                    if self.clickCount < 1:
                        self.labelTest4Info.setText(
                            f"{self.mySender.text()}: {1-self.clickCount} clicks to graph remaining..."  # type: ignore
                        )
                    else:
                        self.clickCount = 0
                        self.testActivated = False
                        self.labelTest4Info.setText(f"{self.mySender.text()}: Test completed")  # type: ignore

                        # Process Data
                        self.findProcessVarMaxVal(self.clickDataY[0])
                        self.updateSetpointError()

                        # Clean arrays
                        self.clickDataX = []
                        self.clickDataY = []

    def processTest(self):
        if not self.testActivated:
            self.testActivated = True
            self.clickCount = 0

            self.mySender = self.sender()  # type: ignore
            if self.mySender is self.btnAutoRephase:
                self.labelTest1Info.setText(f"{self.mySender.text()}: 3 clicks to graph remaining...")  # type: ignore

            elif self.mySender is self.btnGradient:
                self.labelTest2Info.setText(f"{self.mySender.text()}: 2 clicks to graph remaining...")  # type: ignore

            elif self.mySender is self.btnRiseTime:
                self.labelTest3Info.setText(f"{self.mySender.text()}: 2 clicks to graph remaining...")  # type: ignore

            elif self.mySender is self.btnProcessVarMaxVal:
                self.labelTest4Info.setText(f"{self.mySender.text()}: 1 click to graph remaining...")  # type: ignore

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

    def findProcessVarMaxVal(self, clickDataY):
        # Get maximum in small interval of column selected with cBoxY1Data
        column = self.cBoxY1Data.currentText()

        # Find closest index of clicked value
        columnValues = self.df[column].tolist()
        closestVal = min(columnValues, key=lambda x: abs(x - clickDataY))
        idx = columnValues.index(closestVal)

        # Create small interval around the found index and get max value (it handles click inaccuracy)
        indexes = range(idx - 10, idx + 10 + 1)
        colSmallInterval = [columnValues[x] for x in indexes]
        self.processVarMaxVal = max(colSmallInterval)

    def updateSetpointError(self):
        self.setpoint = self.dblSpinBoxSetpoint.value()
        self.labelSetpointErrVal.setText(f"{self.setpoint - self.processVarMaxVal:.3f} (kW/kvar)")

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
