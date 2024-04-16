# import pandas as pd
# from random import uniform
import numpy as np
import pyqtgraph as pg
import pandas as pd
import time
from include.UIs.XYGraphTab_ui import Ui_XYGraphTab
from dp_app.include.pgTimeAxis import DateAxisItem
from PyQt6.QtCore import Qt, pyqtSlot  # , QTimer
from PyQt6.QtGui import QFont, QPalette
from PyQt6.QtWidgets import QWidget


# pyuic6 dp-qtdesktopapp/include/UIs/XYGraphTab.ui -o dp-qtdesktopapp/include/UIs/XYGraphTab_ui.py
class XYGraphTab(QWidget, Ui_XYGraphTab):
    def __init__(self):
        super(XYGraphTab, self).__init__()
        self.setupUi(self)

        # Set background colour - default window color background
        xyGraphBGcolor = self.palette().color(QPalette.ColorRole.Base)
        self.XYGraph.setBackground(xyGraphBGcolor)
        self.XYGraph.setTitle("Title", color="k", size="16pt")
        # self.XYGraph.addLegend(offset=20)
        self.XYGraph.showGrid(x=True, y=True)

        self.xyPlot = self.XYGraph.getPlotItem()
        self.pen = pg.mkPen(color="b", width=2, style=Qt.PenStyle.SolidLine)

    def loadData(self, dataFrame):
        self.df = dataFrame.copy()

        # Get name of the first column with "Time"
        self.timeColName = [col for col in dataFrame.columns if "Time" in col][0]

        self.processData()

        # series to list
        self.dataX = self.df[self.comboBoxXData.currentText()].tolist()
        self.dataY = self.df[self.comboBoxYData.currentText()].tolist()

        self.lineDataRef = self.XYGraph.plot(self.dataX, self.dataY, pen=self.pen)
        # Y-Axis
        self.xyPlot.setLabel("left", self.comboBoxYData.currentText())  # , units="???")  # type: ignore
        self.xyPlot.getAxis("left").label.setFont(QFont("Times", 12))  # type: ignore

        # X-Axis (DateTime)
        # Remove the old item to not get message from QGridLayoutEngine: Cell (3, 1) already taken
        old_item = self.xyPlot.layout.itemAt(3, 1)  # type: ignore
        self.xyPlot.layout.removeItem(old_item)  # type: ignore

        # Add the Date-time axis
        xAxis = DateAxisItem(orientation="bottom")
        xAxis.attachToPlotItem(self.xyPlot)

        # TODO Remove units??? Showing "G" at the beginning
        self.xyPlot.setLabel("bottom", self.comboBoxXData.currentText(), units="s")  # type: ignore
        self.xyPlot.getAxis("bottom").label.setFont(QFont("Times", 12))  # type: ignore
        self.xyPlot.setTitle(  # type: ignore
            f"{self.comboBoxYData.currentText()} vs {self.comboBoxXData.currentText()}"
        )

        self.comboBoxXData.currentTextChanged.connect(self.updatePlotData)
        self.comboBoxYData.currentTextChanged.connect(self.updatePlotData)

        # REVIEW Plot some random data with timestamps in the last hour
        # now = time.time()
        # timestamps = np.linspace(now - 3600, now, 100)
        # self.XYGraph.plot(x=timestamps, y=np.random.rand(100), symbol="o")

    def processData(self):
        # Convert datetime to timestamp
        self.df[self.timeColName] = self.df[self.timeColName].apply(pd.Timestamp.timestamp)

        # Ph2PhAvgVoltages = self.df[["Avg.U12[V]", "Avg.U23[V]", "Avg.U31[V]"]]
        # print(Ph2PhAvgVoltages)

        # Average for each row
        # Ph2PhVoltagesMean = np.array(Ph2PhAvgVoltages).mean(axis=1)
        # print(Ph2PhVoltagesMean)
        pass

    @pyqtSlot()
    def updatePlotData(self):
        sender = self.sender()  # .text()  # .objectName()  # type: ignore

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

    # # TODO: finish
    # def saveMeasuredData(self):
    #     x = np.linspace(0, 1, 201)
    #     y = np.random.random(201)

    #     np.savetxt("testData.dat", [x, y])


# Reimplements \c pyqtgraph.AxisItem to display time series.
# \code
# from caxistime import CAxisTime
# \# class definition here...
# self.__axisTime=CAxisTime(orientation='bottom')
# self.__plot=self.__glyPlot.addPlot(axisItems={'bottom': self.__axisTime}) # __plot : PlotItem
# \endcode
class CAxisTime(pg.AxisItem):
    # Formats axis label to human readable time.
    # @param[in] values List of \c time_t.
    # @param[in] scale Not used.
    # @param[in] spacing Not used.
    def tickStrings(self, values, scale, spacing):
        strns = []
        for x in values:
            try:
                strns.append(time.strftime("%H:%M:%S", time.gmtime(x)))  # time_t --> time.struct_time
            except ValueError:  # Windows can't handle dates before 1970
                strns.append("")
        return strns
