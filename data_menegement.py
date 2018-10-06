import numpy as np
import pandas
from variables import *
from datetime import datetime, timedelta
from math import log


def damage_property(row):
    # creating the variable damage in int format to avoid 10K 12M 2B etc
    element = row["damage_property"]
    multiplier = {
        'K': 10 ** 3,  # for the format like 3.6K
        'M': 10 ** 6,  # for the format like 15M
        'B': 10 ** 9  # for the format like 2B
    }
    if type(element) is str:
        if element[-1] in multiplier:
            return int(float(element[:-1]) * multiplier[element[-1]])
        else:
            try:
                # in case if there are some values less than 1000$ (should not be)
                return int(element[:])
            except ValueError:
                # to check if there are some other format of damage property price is missed
                print(f'The value {element} was not transformed properly')
                return np.nan
    else:
        # if the value is not str, it means that damage was not evaluated properly and cannot be considered
        return np.nan


def log_count(element):  # logarithm with base 10 and excluding nan
    if element in (0, np.nan):
        return np.nan  # nan and zero are excluded
    else:
        return log(element, 10)


def damage_property_lg(row):  # decrease positive skew
    return log_count(float(row["damage_property"]))


def event_duration_lg(row):  # decrease positive skew
    return log_count(float(row["event_duration"]))


def property_damaged(row):  # turning damage_property to categorical: whether property was damaged(1) or not (0)
    element = row["damage_property"]
    if element != np.nan:
        return 1 if element > 0 else 0
    else:
        return np.nan


def event_duration(row):  #
    begin = datetime.strptime(row["begin_date_time"], "%d%b%y:%H:%M:%S")
    end = datetime.strptime(row["end_date_time"], "%d%b%y:%H:%M:%S")
    t = (end - begin).total_seconds() / 3600
    return t


def month_name(row):  # adding numerical prefix to month names
    element = row['month_name']
    month_dict = {
        "April": "04",
        "August": "08",
        "December": "12",
        "February": "02",
        "January": "01",
        "July": "07",
        "June": "06",
        "March": "03",
        "May": "05",
        "November": "11",
        "October": "10",
        "September": "09"
    }
    return month_dict.get(element, '') + '.' + element


def climate_region(row):
    # dividing states to climate region
    # based on https://www.ncdc.noaa.gov/monitoring-references/maps/us-climate-regions.php
    # Alaska is separate from other categories; District of Columbia added to Northeast
    # As a consequence "Other" is related to events happened near islands or in seas or oceans
    element = row["state"]
    state_to_regions = {'Alabama': 'Southeast',
                        'Alaska': 'Alaska',
                        'Arizona': 'Southwest',
                        'Arkansas': 'South',
                        'California': 'West',
                        'Colorado': 'Southwest',
                        'Connecticut': 'Northeast',
                        'Delaware': 'Northeast',
                        'Florida': 'Southeast',
                        'Georgia': 'Southeast',
                        'Idaho': 'Northwest',
                        'Illinois': 'Central',
                        'Indiana': 'Central',
                        'Iowa': 'Upper_Midwest',
                        'Kansas': 'South',
                        'Kentucky': 'Central',
                        'Louisiana': 'South',
                        'Maine': 'Northeast',
                        'Maryland': 'Northeast',
                        'Massachusetts': 'Northeast',
                        'Michigan': 'Upper_Midwest',
                        'Minnesota': 'Upper_Midwest',
                        'Mississippi': 'South',
                        'Missouri': 'Central',
                        'Montana': 'West_North_Central',
                        'Nebraska': 'West_North_Central',
                        'Nevada': 'West',
                        'New Hampshire': 'Northeast',
                        'New Jersey': 'Northeast',
                        'New Mexico': 'Southwest',
                        'New York': 'Northeast',
                        'North Dakota': 'West_North_Central',
                        'North Carolina': 'Southeast',
                        'Ohio': 'Central',
                        'Oklahoma': 'South',
                        'Oregon': 'Northwest',
                        'Pennsylvania': 'Northeast',
                        'Rhode Island': 'Northeast',
                        'South': 'South',
                        'South Dakota': 'West_North_Central',
                        'South Carolina': 'Southeast',
                        'Tennessee': 'Central',
                        'Texas': 'South',
                        'Utah': 'Southwest',
                        'Vermont': 'Northeast',
                        'Virginia': 'Southeast',
                        'Washington': 'Northwest',
                        'West Virginia': 'Central',
                        'Wisconsin': 'Upper_Midwest',
                        'Wyoming': 'West_North_Central',
                        'District Of Columbia': "Northeast"}
    return state_to_regions.get(element.title(), "Other")


def modify_data_set(data_set, variables_to_modify):
    # takes the variables which should be created or modified
    # calls the function with the same name as the variable
    for variable in variables_to_modify:
        # modify the variables
        data_set[variable] = data_set.apply(eval(variable), axis=1)
    return data_set


def primary_data_management(explanatory_variables, response_variables,
                            condition="""(data_set["damage_property"] >= 0)"""):
    # extracts the data set from csv file
    # modifies
    try:
        # taking the data from the file
        data_set = pandas.read_csv('data_related/storm_event_data.csv', low_memory=False)
    except FileNotFoundError:
        # there is two probable locations of the file, so doesn't make sense to write too many lines about it
        data_set = pandas.read_csv('../data_related/storm_event_data.csv', low_memory=False)

    # in case if I need to display the content, I want to see all columns and rows
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.max_rows', None)

    # the variables are written in uppercase in the data set, but written in lowercase in the codebook
    # to be sure I tend to copy variable names from the codebook to the program
    data_set.columns = map(str.lower, data_set.columns)

    modifiable_variables = retrieve_variables_to_modify()
    data_set = modify_data_set(data_set, modifiable_variables)  # performing necessary modifications of the data set

    # making a subset where we consider only weather events for which damage is evaluated and bigger than or equal zero
    # the condition can be changed to come other to change the sample
    data_with_damage = data_set[(data_set["damage_property"] >= 0) & eval(condition)]
    # because the dataset is huge, to save time, I am leaving only variables with which I work with
    return data_with_damage[list(explanatory_variables) + list(response_variables)]


if __name__ == "__main__":
    pass
