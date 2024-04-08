import os.path as path
import dp_app.include.fileTools as ft


if __name__ == "__main__":
    appBaseDir = path.dirname(__file__)

    # Read the data_separator from the INI config file
    data_separator = ft.iniReadSectionKey(
        path.join(appBaseDir, "appConfig.ini"),
        "app.csv_data",
        "data_separator",
    )

    # Read the filtered_columns from the INI config file
    filtered_columns = ft.iniReadSectionKey(
        path.join(appBaseDir, "appConfig.ini"),
        "app.csv_data",
        "filtered_columns",
    )

    data = ft.readCSVdata(path.join(appBaseDir, "data", "data.csv"), data_separator, filtered_columns)
    print(data)
