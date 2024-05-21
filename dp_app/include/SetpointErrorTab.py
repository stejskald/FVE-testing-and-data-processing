from include.UIs.SetpointErrorTab_ui import Ui_SetpointErrorTab
from include.AbstractDataModels.TestsTableModel import TableModel
from PyQt6.QtCore import Qt, pyqtSlot, QStringListModel
from PyQt6.QtGui import QPalette, QColor, QPainterPath, QFont, QTransform
from PyQt6.QtWidgets import QWidget, QHeaderView
import pyqtgraph as pg
import dp_app.include.fileTools as ft
import pandas as pd
import numpy as np
from datetime import datetime
from os import path
from math import floor
from collections import namedtuple

appBaseDir = path.abspath(path.join(__file__, "../.."))

TextSymbol = namedtuple("TextSymbol", "label symbol scale")


class SetpointErrorTab(QWidget, Ui_SetpointErrorTab):
    def __init__(self):
        super(SetpointErrorTab, self).__init__()
        self.setupUi(self)

        # Read settings from configuration file
        self.readConfig()

        # Create list of plots
        self.plots = [self.plot0, self.plot1, self.plot2]

        # Get ViewBoxes from plots
        self.pViewBoxes = [plot.getViewBox() for plot in self.plots]

        # Define list indicating in which plot the horizontal crosshair is added
        self.hCrosshairAdded = [False for _ in range(len(self.plots))]

        # Format all plots in UI
        self.formatPlots()

        # Get Plot Items from UI
        self.plotItems = [plot.getPlotItem() for plot in self.plots]

        # Setup a SignalProxy and connect it to a mouseMoved slot
        # Whenever the mouse is moved over the plot, the mouseMoved is called with an event as an argument
        self.proxySignals = [pg.SignalProxy(self.plots[0].scene().sigMouseMoved) for _ in range(len(self.plots))]
        for i in range(len(self.plots)):
            self.proxySignals[i] = pg.SignalProxy(
                self.plots[i].scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved
            )

        # Connect sigMouseClicked signals to a onGraphClick slot
        [plot.scene().sigMouseClicked.connect(self.onGraphClick) for plot in self.plots]

        self.dblSpinBoxPwrSetpoint.setValue(self.pwrSetpoint)
        self.dblSpinBoxCosPhiSetpoint.setValue(self.cosSetpoint)
        # self.dblSpinBoxPwrSetpoint.valueChanged.connect(self.updateSetpointErrors)
        # self.dblSpinBoxCosPhiSetpoint.valueChanged.connect(self.updateSetpointErrors)

        # Connect buttons to slots
        self.btnTest.clicked.connect(self.testButtonPressed)
        self.btnCancelLastPt.clicked.connect(self.cancelLastPoint)

        # Init Tab variables
        self.testActivated = False
        self.seqCount = 0
        self.clickCount = 0
        self.clickDataX = []
        self.clickDataY = []
        self.testResults = [[], [], [], []]
        self.ptsPerSeq = 1
        self.processVarMaxVal = 0
        self.powerSetpointErrorVal = 0
        self.cosSetpointErrorVal = 0

    def readConfig(self):
        # Read the real_power_3ph from the INI config file
        self.realPower3ph = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.setpoint_error",
            "real_power_3ph",
        )

        # Read the reactive_power_3ph from the INI config file
        self.reactivePower3ph = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.setpoint_error",
            "reactive_power_3ph",
        )

        # Read the cos_phi from the INI config file
        self.cosPhi = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.setpoint_error",
            "cos_phi",
        )

        # Read the power_setpoint from the INI config file
        self.pwrSetpoint = float(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.setpoint_error",
                "power_setpoint",
            )
        )

        # Read the cos_phi_setpoint from the INI config file
        self.cosSetpoint = float(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.setpoint_error",
                "cos_phi_setpoint",
            )
        )

        # Read the real_power_3ph_nominal from the INI config file
        self.realPower3phNominal = float(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.setpoint_error",
                "real_power_3ph_nominal",
            )
        )

        # Read the mean_interval_length from the INI config file
        self.meanIntervalLength = int(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.setpoint_error",
                "mean_interval_length",
            )
        )

        # Read the moving_avg_window_size from the INI config file
        self.movAvgWinSize = int(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.setpoint_error",
                "moving_avg_window_size",
            )
        )

        # Read the table_headers from the INI config file
        self.tableHeaders = ft.iniReadSectionKeyItems(
            path.join(appBaseDir, "appConfig.ini"),
            "app.setpoint_error",
            "table_headers",
        )

        # Read the points from the INI config file
        self.pointSeqs = ft.iniReadSectionKeyItems(
            path.join(appBaseDir, "appConfig.ini"),
            "app.setpoint_error",
            "points",
        )

        # Read the points_notes from the INI config file
        self.seqsNotes = ft.iniReadSectionKeyItems(
            path.join(appBaseDir, "appConfig.ini"),
            "app.setpoint_error",
            "points_notes",
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
        [plot.setBackground(plotBGcolor) for plot in self.plots]

        # Define plot colors
        self.plotColors = ["#4393C3", "#B2182B", "#CC6CE7", "#5DE2E7", "#BFD641", "#DFC57B"]

        # Define label styles for all axes
        self.xLabelStyle = {"font": "Times", "font-size": "12pt"}
        self.yLabelStyles = [{"color": color, "font": "Times", "font-size": "12pt"} for color in self.plotColors]

        # Hide axes and auto-scale buttons on each plot except the last
        [plot.hideButtons() for plot in self.plots[:-1]]

        # X-Axes - Set as pg.DateAxisItem
        [plot.setAxisItems({"bottom": pg.DateAxisItem(orientation="bottom")}) for plot in self.plots]

        # Link X-Axes of all plots except the last to the last plot
        [plot.setXLink(self.plots[-1]) for plot in self.plots[:-1]]

        # Hide values on X-Axes of all plots except the last
        [plot.getAxis("bottom").setStyle(showValues=False) for plot in self.plots[:-1]]
        # self.xAxisPlot0.showLabel(False)

        # Turn on the grids
        [plot.showGrid(x=True, y=True, alpha=0.6) for plot in self.plots]

        # Define pen style for each plot
        self.yPens = [pg.mkPen(color=color, width=2, style=Qt.PenStyle.SolidLine) for color in self.plotColors]

        # Define, create and add crosshair lines
        self.crosshairColors = ["#648200", "#FFDE59", "#C0FF00"]
        crosshairPen = pg.mkPen(color=self.crosshairColors[0], width=1, style=Qt.PenStyle.SolidLine)

        self.hCrosshair = pg.InfiniteLine(angle=0, pen=crosshairPen)
        # self.hCrosshair2 = pg.InfiniteLine(angle=0, pen=crosshairPen)
        self.vCrosshairs = [pg.InfiniteLine() for _ in range(len(self.plots))]
        for iter in range(len(self.plots)):
            self.vCrosshairs[iter] = pg.InfiniteLine(angle=90, pen=crosshairPen)

        # Add vCrosshair lines to all plots
        [plot.addItem(self.vCrosshairs[i], ignoreBounds=True) for i, plot in enumerate(self.plots)]  # type: ignore

        # Define and add cursor label
        self.cursorLabel = pg.TextItem(anchor=(-0.02, 1))
        self.plots[0].addItem(self.cursorLabel, ignoreBounds=True)  # type: ignore

        # Set cursor over the plots as small cross
        [plot.setCursor(Qt.CursorShape.CrossCursor) for plot in self.plots]
        # Hide cursor over the plots
        # self.plots[0].setCursor(Qt.CursorShape.BlankCursor)

        # Init Scatter Plot Items for symbol and text inserting to plot area
        self.scatterPoints = [pg.ScatterPlotItem() for _ in range(len(self.pViewBoxes))]
        for i, pViewBox in enumerate(self.pViewBoxes):
            self.scatterPoints[i] = pg.ScatterPlotItem(
                symbol=self.clickPtSymbol,
                pen=pg.mkPen(None),
                brush=pg.mkBrush(QColor("black")),
                size=self.clickPtSymbolSize,
                hoverable=True,
            )
            pViewBox.addItem(self.scatterPoints[i])

        self.scatterLabels = [pg.ScatterPlotItem() for _ in range(len(self.pViewBoxes))]
        for i, pViewBox in enumerate(self.pViewBoxes):
            self.scatterLabels[i] = pg.ScatterPlotItem(
                pen=pg.mkPen(None),  # QColor("black"), width=2
                brush=QColor("black"),
                size=self.clickPtLabelSize,
            )
            pViewBox.addItem(self.scatterLabels[i])
        # self.scatterLabels.sigClicked.connect(self.scatterPointsClicked)

    def loadData(self, dataFrame):
        # Get name of the first column with "Time"
        self.timeColName = [col for col in dataFrame.columns if "Time" in col][0]

        # Make a reference to the dataFrame and copy only the timeColName column (will be processed subsequently)
        self.df = dataFrame.loc[:, dataFrame.columns != self.timeColName]
        self.df[self.timeColName] = dataFrame[self.timeColName].copy()

        timeList = ["" for _ in range(len(self.pointSeqs))]
        cosPhiSetListIdx = ["" for _ in range(len(self.pointSeqs))]
        PorQSetListIdx = ["" for _ in range(len(self.pointSeqs))]
        deltaPorQListIdx = ["" for _ in range(len(self.pointSeqs))]
        deltaCosPhiListIdx = ["" for _ in range(len(self.pointSeqs))]
        self.timeListIdx = 0
        self.cosPhiSetListIdx = 2
        self.PorQSetListIdx = 3
        self.deltaPorQListIdx = 4
        self.deltaCosPhiListIdx = 5

        if len(self.pointSeqs) > len(self.seqsNotes):
            for _ in range(len(self.seqsNotes), len(self.pointSeqs)):
                self.seqsNotes.append("")

        self.dfTable = pd.DataFrame(
            list(
                zip(
                    timeList,
                    self.pointSeqs,
                    cosPhiSetListIdx,
                    PorQSetListIdx,
                    deltaPorQListIdx,
                    deltaCosPhiListIdx,
                    self.seqsNotes,
                )
            ),
            columns=self.tableHeaders,
        )
        self.setTableDataModel(self.dfTable)

        self.processData()

        # series to lists with averaging
        sizeCorrection = 0
        if self.movAvgWinSize % 2 != 0:
            sizeCorrection = 1
        halfWin = int(self.movAvgWinSize / 2)

        self.xData = self.df[self.timeColName].tolist()[halfWin + sizeCorrection : -halfWin + 1]
        self.yData = [
            self.movAvgConvolve(self.df[self.realPower3ph].tolist(), self.movAvgWinSize),
            self.movAvgConvolve(self.df[self.reactivePower3ph].tolist(), self.movAvgWinSize),
            self.movAvgConvolve(self.df[self.cosPhi].tolist(), self.movAvgWinSize),
        ]

        # X-Axis
        self.plotItems[-1].setLabel("bottom", self.timeColName, **self.xLabelStyle)  # type: ignore
        # self.plotItem6.getAxis("bottom").enableAutoSIPrefix(False)  # type: ignore

        # Y-Axes
        self.yNames = [
            self.realPower3ph,
            self.reactivePower3ph,
            self.cosPhi,
        ]
        self.yLineRefs = [pg.PlotDataItem() for _ in range(len(self.plots))]
        for i in range(len(self.plots)):
            self.yLineRefs[i] = self.plots[i].plot(self.xData, self.yData[i], pen=self.yPens[i], name=self.yNames[i])

        # Set Y-Axes Labels
        self.yLeftLabels = ["P [kW]", "Q [kvar]", "δcos(φ) []"]  # "δ(cos(φ)-1) []"
        for i, plotItem in enumerate(self.plotItems):
            plotItem.setLabel("left", self.yLeftLabels[i], **self.yLabelStyles[i])  # type: ignore

        self.setComboBoxDataModel(self.yLeftLabels[:-1])

        # Reinit scatters and (re)init needed variables
        [scatter.clear() for scatter in self.scatterPoints]
        [scatter.clear() for scatter in self.scatterLabels]
        self.seqCount = 0

    def setTableDataModel(self, data):
        # Getting the Model
        self.tableModel = TableModel(data)

        # Creating a QTableView
        self.tableView.setModel(self.tableModel)

        # QTableView Headers
        self.horizHeader = self.tableView.horizontalHeader()
        self.vertHeader = self.tableView.verticalHeader()
        self.horizHeader.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)  # type: ignore
        # self.vertHeader.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)  # type: ignore

    def processData(self):
        # Convert datetime to timestamp
        self.df[self.timeColName] = self.df[self.timeColName].apply(pd.Timestamp.timestamp)

        # Adjust cosPhi
        # TODO Separe to 2 graphs?...
        # cosPhiList = self.df[self.cosPhi].tolist()
        # cosPhiTemp1 = [(lambda x: -1 - x)(x) for x in cosPhiList]
        # cosPhiTemp2 = [(lambda x: 1 - x)(x) for x in cosPhiList]
        # cosPhiTemp3 = [cosPhiTemp1[i] if x < 0 else cosPhiTemp2[i] for i, x in enumerate(cosPhiList)]
        # self.df[self.cosPhi] = [cosPhiTemp3[i] if x != 0 else float("nan") for i, x in enumerate(cosPhiList)]

    def movAvgConvolve(self, array, n=10):
        weights = np.ones(n) / n
        return np.convolve(array, weights, mode="valid")

    def setComboBoxDataModel(self, items=[]):
        self.cBoxPlotsDataModel = QStringListModel(items)
        self.cBoxPlots.setModel(self.cBoxPlotsDataModel)
        self.cBoxPlots.setCurrentIndex(0)

    def mouseMoved(self, event):
        # TODO how to know above which plot the cursor is or what plot fired the proxysignal?...
        # sender = self.sender().signal  # type: ignore
        # print(sender)
        # print(self.sender())
        # print(self.proxySignals[0].signal.source) does not work

        # event[0] holds a positional argument
        pos = event[0]

        # Checks if data has been loaded
        if hasattr(self, "xData"):
            # for i, plot in enumerate(self.plots):
            i = self.cBoxPlots.currentIndex()
            if self.plots[i].sceneBoundingRect().contains(pos):
                mousePoint = self.plots[i].getPlotItem().vb.mapSceneToView(pos)  # type: ignore

                # Set hCrosshair and cursorLabel to selected plot
                if self.hCrosshairAdded[i] is False:
                    for j, plot in enumerate(self.plots):
                        if j != i:
                            plot.removeItem(self.hCrosshair)
                            plot.removeItem(self.cursorLabel)
                    self.plots[i].addItem(self.hCrosshair, ignoreBounds=True)  # type: ignore
                    self.plots[i].addItem(self.cursorLabel, ignoreBounds=True)  # type: ignore
                    self.hCrosshairAdded = [False if j != i else True for j in range(len(self.hCrosshairAdded))]
                    print(f"hCrosshair and cursorLabel added to plot{i}")

                # Find closest index of clicked value
                xClosestVal = min(self.xData, key=lambda x: abs(x - mousePoint.x()))
                index = self.xData.index(xClosestVal)
                if 0 < index < len(self.xData):
                    # Update cursorLabel text
                    self.cursorLabel.setText(
                        f"x={datetime.fromtimestamp(self.xData[index]).strftime('%H:%M:%S.%f')}, "
                        + f"y={self.yData[i][index]:0.3f}",
                        color="k",
                    )
                    # self.cursorLabel.setHtml(
                    #     "<span style='font-size: 12pt'>x={}, \
                    #      <span style='color: #B2182B'>y={:0.3f}</span>".format(
                    #         datetime.fromtimestamp(self.dataX[index]).strftime("%H:%M:%S.%f"), self.dataY1[index]
                    #     )
                    # )

                    # Update positions of cursorLabel and all crosshairs
                    self.cursorLabel.setPos(mousePoint.x(), mousePoint.y())
                    self.hCrosshair.setPos(mousePoint.y())
                    [vCrosshair.setPos(mousePoint.x()) for vCrosshair in self.vCrosshairs]

                # break
            else:
                return None

    def onGraphClick(self, event):
        j = self.cBoxPlots.currentIndex()
        if self.plots[j].sceneBoundingRect().contains(event._scenePos):
            mousePoint = self.pViewBoxes[j].mapSceneToView(event._scenePos)
            # # Convert obtained float value to datetime with time zone info
            # xValay2DateTime = pd.to_datetime(mousePoint.x(), unit="s")
            # myTimeZone = pytz.timezone("Europe/Prague")
            # dateTimeWithTimeZone = myTimeZone.localize(xValay2DateTime)

            if hasattr(self, "dfTable"):
                xClosestVal = min(self.xData, key=lambda x: abs(x - mousePoint.x()))
                index = self.xData.index(xClosestVal)

                # Checks if test was activated and data has been loaded
                if self.testActivated and 0 < index < len(self.xData):
                    self.clickDataX += [self.xData[index]]
                    self.clickDataY += [self.yData[j][index]]
                    self.clickCount += 1
                    if self.clickCount < self.ptsPerSeq:
                        self.textTestInfo.setPlainText(f"{self.ptsPerSeq-self.clickCount} clicks to graph remaining...")
                    else:
                        self.clickCount = 0
                        self.btnTest.setChecked(False)
                        self.testActivated = False
                        self.textTestInfo.setPlainText("Test completed")

                        # Process Data
                        self.findProcessVarMaxVal(self.clickDataY[self.ptsPerSeq - 1])
                        self.updateSetpointErrors(index)

                        # Save results to the table
                        # usec value in .2f format
                        self.dfTable.iloc[self.seqCount, self.timeListIdx] = datetime.fromtimestamp(
                            self.clickDataX[self.ptsPerSeq - 1]
                        ).strftime("%H:%M:%S.%f")[:-4]

                        self.dfTable.iloc[self.seqCount, self.cosPhiSetListIdx] = f"{self.cosSetpoint:.2f}"

                        self.dfTable.iloc[self.seqCount, self.PorQSetListIdx] = (
                            f"{self.pwrSetpoint/self.realPower3phNominal:.3f}"
                        )

                        self.dfTable.iloc[self.seqCount, self.deltaPorQListIdx] = f"{self.powerSetpointErrorVal:.2f}"

                        self.dfTable.iloc[self.seqCount, self.deltaCosPhiListIdx] = f"{self.cosSetpointErrorVal:.2f}"

                        # Let the TableView know that the Data Model has changed
                        # Note: it doesn't update only specified row, but the entire table, it seems...
                        self.tableModel.dataChanged.emit(
                            self.tableModel.index(self.seqCount, self.timeListIdx),
                            self.tableModel.index(self.seqCount, self.deltaCosPhiListIdx),
                        )

                        # Update scatterPoints data points
                        actStartIdx = self.seqCount * self.ptsPerSeq + 1
                        self.scatterPoints[j].addPoints(
                            self.clickDataX,
                            self.clickDataY,
                            data=[actStartIdx + i for i in range(len(self.clickDataX))],
                        )

                        # Update scatterLabels data points
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
                        self.scatterLabels[j].addPoints(spots)

                        # Save lists to 2D list -> [[x0, x1, ...], [y0, y1, ...]]
                        [self.testResults[0].append(xVal) for xVal in self.clickDataX]
                        [self.testResults[1].append(yVal) for yVal in self.clickDataY]
                        [self.testResults[2].append(spot) for spot in spots]
                        [self.testResults[3].append(j) for _ in range(len(self.clickDataX))]

                        self.seqCount += 1

                        # # Save lists to 2D array
                        # self.autoReconnectTestResults = np.array(
                        #     [
                        #         [datetime.fromtimestamp(item).strftime("%H:%M:%S.%f") for item in self.clickDataX],
                        #         self.clickDataY,
                        #     ]
                        # )
                        # print(f"{self.autoReconnectTestResults}")

    @pyqtSlot(bool)
    def testButtonPressed(self, btnState):
        self.testActivated = btnState
        self.clickCount = 0
        self.clickDataX = []
        self.clickDataY = []
        if btnState:
            self.textTestInfo.setPlainText(f"{self.ptsPerSeq} clicks to graph remaining...")
        else:
            self.textTestInfo.clear()

    @pyqtSlot()
    def cancelLastPoint(self):
        if hasattr(self, "dfTable") and self.seqCount > 0:
            self.seqCount -= 1
            # Delete results of the last sequence from the table
            self.dfTable.iloc[self.seqCount, self.timeListIdx] = ""
            self.dfTable.iloc[self.seqCount, self.cosPhiSetListIdx] = ""
            self.dfTable.iloc[self.seqCount, self.PorQSetListIdx] = ""
            self.dfTable.iloc[self.seqCount, self.deltaPorQListIdx] = ""
            self.dfTable.iloc[self.seqCount, self.deltaCosPhiListIdx] = ""

            # Let the TableView know that the Data Model has changed
            self.tableModel.dataChanged.emit(
                self.tableModel.index(self.seqCount, self.timeListIdx),
                self.tableModel.index(self.seqCount, self.deltaCosPhiListIdx),
            )

            # Remove last element from both lists
            i = int(self.testResults[3][-1])
            [self.testResults[0].pop() for _ in range(self.ptsPerSeq)]
            [self.testResults[1].pop() for _ in range(self.ptsPerSeq)]
            [self.testResults[2].pop() for _ in range(self.ptsPerSeq)]
            [self.testResults[3].pop() for _ in range(self.ptsPerSeq)]

            # Remove last points from scatterPoints
            actStartIdx = 1
            tempX = [self.testResults[0][j] for j in range(len(self.testResults[0])) if i == self.testResults[3][j]]
            tempY = [self.testResults[1][j] for j in range(len(self.testResults[1])) if i == self.testResults[3][j]]
            self.scatterPoints[i].setData(
                tempX,
                tempY,
                data=[actStartIdx + i for i in range(len(tempX))],
            )

            # Remove last labels from scatterLabels
            self.scatterLabels[i].clear()
            self.scatterLabels[i].addPoints(
                [self.testResults[2][j] for j in range(len(self.testResults[2])) if i == self.testResults[3][j]]
            )

            # for j in range(len(self.scatterLabels)):
            #     for i, plotIdx in enumerate(self.testResults[3]):
            #         if j == plotIdx:
            #             self.scatterLabels[j].addPoints(self.testResults[2][i])

    def setMeasurementDate(self, measDate):
        self.labelMeasDateValue.setText(measDate)

    def findProcessVarMaxVal(self, clickDataY):
        # Get maximum in small interval of selected column
        column = self.yNames[self.cBoxPlots.currentIndex()]

        # Find closest index of clicked value
        columnValues = self.df[column].tolist()
        closestVal = min(columnValues, key=lambda x: abs(x - clickDataY))
        idx = columnValues.index(closestVal)

        # Create small interval around the found index and get mean value (it handles click inaccuracy)
        indexes = range(idx - floor(self.meanIntervalLength / 2), idx + floor(self.meanIntervalLength / 2) + 1)
        colSmallInterval = [columnValues[x] for x in indexes]
        self.processVarMaxVal = np.mean(colSmallInterval)  # ...I would prefer max() func

    def updateSetpointErrors(self, index: int):
        yLabel = self.cBoxPlots.currentText()

        if yLabel in self.yLeftLabels[:2]:
            unit = "kvar" if yLabel.find("kvar") != -1 else "kW"
            self.dblSpinBoxPwrSetpoint.setSuffix(" " + unit)
            self.pwrSetpoint = self.dblSpinBoxPwrSetpoint.value()
            if unit == "kW":
                self.powerSetpointErrorVal = 100 * (self.processVarMaxVal - self.pwrSetpoint) / self.pwrSetpoint
                self.labelPwrSetpointErrVal.setText(f"{self.powerSetpointErrorVal:.2f} %")
            else:
                self.powerSetpointErrorVal = 100 * (self.processVarMaxVal - self.pwrSetpoint) / self.pwrSetpoint
                self.labelPwrSetpointErrVal.setText(f"{self.powerSetpointErrorVal:.2f} %")

        self.cosSetpoint = self.dblSpinBoxCosPhiSetpoint.value()
        self.cosSetpointErrorVal = abs(self.yData[2][index] - self.cosSetpoint)
        self.labelCosPhiSetpointErrVal.setText(f"{self.cosSetpointErrorVal:.2f}")

    def createLabel(self, label, angle):
        symbol = QPainterPath()
        symbol.addText(-0.5, 0.5, QFont("Times", 12), label)
        br = symbol.controlPointRect()  # faster than symbol.boundingRect()
        scale = min(1.0 / br.width(), 1.0 / br.height())
        tr = QTransform()
        tr.scale(scale, scale)
        tr.rotate(angle)
        tr.translate(-br.x() - br.width() / 2.0, -br.y() - br.height() / 2.0)
        return TextSymbol(label, tr.map(symbol), 0.1 / scale)
