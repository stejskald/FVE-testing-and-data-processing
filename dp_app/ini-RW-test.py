import os.path as path
import dp_app.include.fileTools as ft


if __name__ == "__main__":
    appBaseDir = path.dirname(__file__)

    # Write a data_separator to the INI config file
    ft.iniWriteSectionKeyValue(path.join(appBaseDir, "appConfig.ini"), "app.csv_data", "data_separator", ";")

    # Write a filtered_columns to the INI config file
    ft.iniWriteSectionKeyValues(
        path.join(appBaseDir, "appConfig.ini"),
        "app.csv_data",
        "filtered_columns",
        [
            "Record Time[s]",
            "Avg.U12[V]",
            "Avg.3P[kW]",
            "Avg.3Q[kvar]",
            "3Cosφ[]",
            "Avg.f[Hz]",
            "Avg.U4dc[V]",
            "DOI1[]",
            "DOI4[]",
        ],
    )

    # Read the data_separator from the INI config file
    data_separator = ft.iniReadSectionKey(
        path.join(appBaseDir, "appConfig.ini"),
        "app.csv_data",
        "data_separator",
    )
    print(f"data_separator from app.csv_data: {data_separator}")

    # Read the filtered_columns from the INI config file
    filtered_columns = ft.iniReadSectionKey(
        path.join(appBaseDir, "appConfig.ini"),
        "app.csv_data",
        "filtered_columns",
    )
    print(f"filtered_columns from app.csv_data: {filtered_columns}")
