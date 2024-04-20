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
        self.XYGraph.showGrid(x=True, y=True)

        self.xyPlot = self.XYGraph.getPlotItem()
        self.pen = pg.mkPen(color="#4393c3", width=2, style=Qt.PenStyle.SolidLine)
        self.xyPlot.setTitle("XY Graph")  # type: ignore

        # Add crosshair lines
        self.crosshair_v = pg.InfiniteLine(angle=90)
        self.crosshair_h = pg.InfiniteLine(angle=0)
        self.XYGraph.addItem(self.crosshair_v, ignoreBounds=True)  # type: ignore
        self.XYGraph.addItem(self.crosshair_h, ignoreBounds=True)  # type: ignore

        # Setup a SignalProxy and connect it to a updateCrosshair method
        # Whenever the mouse is moved over the plot, the updateCrosshair is called with an event as an argument
        self.proxy = pg.SignalProxy(self.XYGraph.scene().sigMouseMoved, rateLimit=60, slot=self.updateCrosshair)

        # Hide the cursor over the plot
        cursor = Qt.CursorShape.BlankCursor
        self.XYGraph.setCursor(cursor)

        self.vb = self.xyPlot.vb  # type: ignore
        self.xyPlot.scene().sigMouseClicked.connect(self.onClick)  # type: ignore

    def loadData(self, dataFrame):
        # Get name of the first column with "Time"
        self.timeColName = [col for col in dataFrame.columns if "Time" in col][0]

        # Make a reference to the dataFrame and copy only the timeColName column (will be processed subsequently)
        self.df = dataFrame.loc[:, dataFrame.columns != self.timeColName]
        self.df[self.timeColName] = dataFrame[self.timeColName].copy()

        self.processData()

        # series to list
        self.dataX = self.df[self.comboBoxXData.currentText()].tolist()
        self.dataY = self.df[self.comboBoxYData.currentText()].tolist()

        # Check if the lineDataRef exists (if Import CSV is called multiple times)
        if hasattr(self, "lineDataRef"):
            self.xyPlot.removeItem(self.lineDataRef)  # type: ignore
        self.lineDataRef = self.XYGraph.plot(
            self.dataX, self.dataY, pen=self.pen, name=self.comboBoxYData.currentText()
        )

        # Y-Axis
        yLabelStyles = {"color": "#4393c3", "font": "Times", "font-size": "12pt"}
        self.xyPlot.setLabel("left", self.comboBoxYData.currentText(), **yLabelStyles)  # type: ignore

        # X-Axis (DateTime)
        # Remove the old item to not get message from QGridLayoutEngine: Cell (3, 1) already taken
        old_item = self.xyPlot.layout.itemAt(3, 1)  # type: ignore
        self.xyPlot.layout.removeItem(old_item)  # type: ignore

        # Add the Date-time axis
        xAxis = DateAxisItem(orientation="bottom")
        xAxis.attachToPlotItem(self.xyPlot)

        xLabelStyles = {"font": "Times", "font-size": "12pt"}
        self.xyPlot.setLabel("bottom", self.comboBoxXData.currentText(), units="s", **xLabelStyles)  # type: ignore
        # self.xyPlot.getAxis("bottom").label.setFont(QFont("Times", 12))  # type: ignore

        self.comboBoxXData.currentTextChanged.connect(self.updatePlotData)
        self.comboBoxYData.currentTextChanged.connect(self.updatePlotData)

    def processData(self):
        # Convert datetime to timestamp
        self.df[self.timeColName] = self.df[self.timeColName].apply(pd.Timestamp.timestamp)
        # print(self.df[self.timeColName])

    @pyqtSlot()
    def updatePlotData(self):
        sender = self.sender()  # type: ignore

        self.xyPlot.setTitle(  # type: ignore
            f"{self.comboBoxYData.currentText()} vs {self.comboBoxXData.currentText()}"
        )
        if sender is self.comboBoxXData:
            self.xyPlot.setLabel("bottom", self.comboBoxXData.currentText())  # type: ignore
            self.dataX = self.df[self.comboBoxXData.currentText()].tolist()
        elif sender is self.comboBoxYData:
            self.xyPlot.setLabel("left", self.comboBoxYData.currentText())  # type: ignore
            self.dataY = self.df[self.comboBoxYData.currentText()].tolist()

        self.lineDataRef.setData(self.dataX, self.dataY)  # Update the line data ref
        self.changeLabel(self.xyPlot, self.lineDataRef, self.comboBoxYData.currentText())

    def setComboBoxesDataModel(self, headers=[]):
        self.comboBoxXDataModel = QStringListModel([headers[0]])
        self.comboBoxXData.setModel(self.comboBoxXDataModel)
        self.comboBoxXData.setCurrentIndex(0)

        self.comboBoxYDataModel = QStringListModel(headers[1:])  # without Time column
        self.comboBoxYData.setModel(self.comboBoxYDataModel)
        self.comboBoxYData.setCurrentIndex(0)

    def updateCrosshair(self, event):
        # event[0] holds a positional argument
        pos = event[0]
        if self.XYGraph.sceneBoundingRect().contains(pos):
            mousePoint = self.XYGraph.getPlotItem().vb.mapSceneToView(pos)  # type: ignore
            self.crosshair_v.setPos(mousePoint.x())
            self.crosshair_h.setPos(mousePoint.y())

    def onClick(self, event):
        # items = self.xyPlot.scene().items(event.scenePos())
        mousePoint = self.vb.mapSceneToView(event._scenePos)  # type: ignore
        print(mousePoint.x(), mousePoint.y())
        if self.xyPlot.sceneBoundingRect().contains(event._scenePos):  # type: ignore
            mousePoint = self.vb.mapSceneToView(event._scenePos)  # type: ignore
            # # Convert obtained float value to datetime with time zone info
            # xVal2DateTime = pd.to_datetime(mousePoint.x(), unit="s")
            # myTimeZone = pytz.timezone("Europe/Prague")
            # dateTimeWithTimeZone = myTimeZone.localize(xVal2DateTime)

            self.labelDataClick1.setText(f"t={mousePoint.x()}, y={mousePoint.y():.3f}")

    def setMeasurementDate(self, measDate):
        self.labelMeasDateValue.setText(measDate)

    def changeLabel(self, plot, plotItem, name):
        # Change the label of given PlotDataItem in the plot's legend
        plot.legend.removeItem(plotItem)
        plot.legend.addItem(plotItem, name)

    # # TODO: finish
    # def saveMeasuredData(self):
    #     x = np.linspace(0, 1, 201)
    #     y = np.random.random(201)

    #     np.savetxt("testData.dat", [x, y])
