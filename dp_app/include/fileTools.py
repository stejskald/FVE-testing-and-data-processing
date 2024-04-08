import configparser
import pandas as pd


# ------------------------------------- CSV File Tools -------------------------------------
def csvReadOnlyHeaders(fpath, separator):
    # Read only the header row - all columns
    return pd.read_csv(fpath, sep=separator, header=1).columns.tolist()


def readCSVdata(fpath, separator, columns=[]):
    # Load CSV data into a Pandas DataFrame
    df = pd.read_csv(fpath, sep=separator, header=1, na_values="- -")

    # Specific columns filter
    df = df[columns]
    return df


# ------------------------------------------------------------------------------------------


# ------------------------------------- INI File Tools -------------------------------------
config = configparser.ConfigParser()


def iniWriteSectionKeyValue(fpath, section, key, value):
    # Add a section and set a value
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, value)

    # Save the configuration to a file
    with open(fpath, "w", encoding="utf-8") as configFile:
        config.write(configFile)


def iniWriteSectionKeyValues(fpath, section, key, values=[]):
    # Add a section and set a value
    if not config.has_section(section):
        config.add_section(section)

    list_as_str = "\n" + ", \n".join(values)
    config.set(section, key, list_as_str)

    # Save the configuration to a file
    with open(fpath, "w", encoding="utf-8") as configFile:
        config.write(configFile)


def iniReadSectionKey(fpath, section, key):
    # Read the configuration file
    config.read(fpath, encoding="utf-8")

    # # Get the sections
    # configSections = config.sections()

    # # Iterate through keys in a section
    # for key in config[section]:
    #     print(key)

    # Access specific values
    # print(f"Member in {section}: {config[section][key]}")

    myString = config[section][key]
    myString = "".join(char for char in myString if char not in "\n")  # Removes all '\n' signs

    if myString.find(",") == -1:
        return myString
    else:
        return myString.split(",")


# ------------------------------------------------------------------------------------------
