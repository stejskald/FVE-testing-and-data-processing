# FVE-testing-and-data-processing

The Python application (using a PyQt6 framework) for analysing FVE (photovoltaic power plant) test data

# TODOs
- Create a default Tab class from which all other testing tabs (GradientTab, TimeDelayTab, SetpointErrorTab) will inherit common methods. Each tab will have its own variables.
- In the MainWindow class there is a method adjustCosPhiColumnData() parsing the cosPhi data from string to float value. It contains a few commented lines solving the inconsistency in the column's data, where capacitive values are in a format "C -0.17" or "C 0.17"... Uncomment these lines and adjust the UI files to contain two graphs for visualizing the cosPhi (if delta from value of 1 is needed).
- In particular tab classes there is a method with commented lines, which are processing the cosPhi data to represent a delta from value of 1 - but it is not completely finished...
- ...
- ...
