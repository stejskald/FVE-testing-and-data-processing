import os.path as path
import dp_app.include.fileTools as ft


if __name__ == "__main__":
    appBaseDir = path.dirname(__file__)

    # # # Write Section
    # Write a data_separator to the INI config file
    # ft.iniWriteSectionKeyValue(path.join(appBaseDir, "appConfig.ini"), "app.csv_data", "data_separator", ";")

    # # Write a date_time_format to the INI config file
    # ft.iniWriteSectionKeyValue(
    #     path.join(appBaseDir, "appConfig.ini"), "app.csv_data", "date_time_format", "%%Y-%%m-%%d %%H:%%M:%%S"
    # )

    # # Write a sample_period_s to the INI config file
    # ft.iniWriteSectionKeyValue(path.join(appBaseDir, "appConfig.ini"), "app.csv_data", "sample_period_s", "0.20")

    # # Write a filtered_columns to the INI config file
    # ft.iniWriteSectionKeyValues(
    #     path.join(appBaseDir, "appConfig.ini"),
    #     "app.csv_data",
    #     "filtered_columns",
    #     [
    #         "Record Time[s]",
    #         "Avg.U12[V]",
    #         "Avg.U23[V]",
    #         "Avg.U31[V]",
    #         "Avg.3P[kW]",
    #         "Avg.3Q[kvar]",
    #         "3Cosφ[]",
    #         "Avg.f[Hz]",
    #         "Avg.U4dc[V]",
    #         "DOI1[]",
    #         "DOI4[]",
    #     ],
    # )

    # # Write uncertainties to the INI config file
    # ft.iniWriteSectionKeyValue(path.join(appBaseDir, "appConfig.ini"), "app.uncertainties", "uncertainty_P", "0.002")
    # ft.iniWriteSectionKeyValue(path.join(appBaseDir, "appConfig.ini"), "app.uncertainties", "uncertainty_Q", "0.01")

    # # Read Section
    # Read the data_separator from the INI config file
    data_separator = ft.iniReadSectionKey(
        path.join(appBaseDir, "appConfig.ini"),
        "app.csv_data",
        "data_separator",
    )

    # Read the date_time_format from the INI config file
    date_time_format = ft.iniReadSectionKey(
        path.join(appBaseDir, "appConfig.ini"),
        "app.csv_data",
        "date_time_format",
    )

    # Read the filtered_columns from the INI config file
    filtered_columns = ft.iniReadSectionKey(
        path.join(appBaseDir, "appConfig.ini"),
        "app.csv_data",
        "filtered_columns",
    )

    # Read the uncertainty_P from the INI config file
    uncertainty_P = ft.iniReadSectionKey(
        path.join(appBaseDir, "appConfig2.ini"),
        "app.uncertainties",
        "uncertainty_P",
    )

    # Read the uncertainty_Q from the INI config file
    uncertainty_Q = ft.iniReadSectionKey(
        path.join(appBaseDir, "appConfig2.ini"),
        "app.uncertainties",
        "uncertainty_Q",
    )
