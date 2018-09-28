import numpy
import pandas
from variables import *
from datetime import datetime, timedelta
from math import log


def damage_property(row,
                    variable="damage_property"):  # creating the variable damage in int format to avoid 10K 12M 2B etc
    element = row[variable]
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
                return None
    else:
        # if the value is not str, it means that damage was not evaluated properly and cannot be considered
        return None


def damage_crops(row):
    return damage_property(row, "damage_crops")


def damage_property_lg(row):
    element = float(row["damage_property"])
    if element == 0:
        return 0
    elif element == numpy.nan or element is None:
        return None
    else:
        return log(element, 10)


def damage_property_cat(row):
    median = 3.69
    element = float(row["damage_property_lg"])
    return 1 if element >= median else 0


def short_event(row):
    begin = datetime.strptime(row["begin_date_time"], "%d%b%y:%H:%M:%S")
    end = datetime.strptime(row["end_date_time"], "%d%b%y:%H:%M:%S")
    return (end - begin) < timedelta(1)


def month_name(row):
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
    return month_dict.get(element, '') + '_' + element


def climate_region(row):
    # based on https://www.ncdc.noaa.gov/monitoring-references/maps/us-climate-regions.php
    element = row["state"]
    state_to_regions = {'Alabama': 'Southeast',
                        'Alaska': 'Upper_Midwest',
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


def month_name_num(row):
    element = row['month_name']
    month_dict = {
        "April": 4,
        "August": 8,
        "December": 12,
        "February": 2,
        "January": 1,
        "July": 7,
        "June": 6,
        "March": 3,
        "May": 5,
        "November": 11,
        "October": 10,
        "September": 9
    }
    return month_dict.get(element, 0)


def modify_data_set(data_set, variables_to_modify):
    for variable in variables_to_modify:
        # modify the variables
        data_set[variable] = data_set.apply(eval(variable), axis=1)
    return data_set


def primary_data_management(putative_predictors, response_variables):
    try:
        # taking the data from the file
        data_set = pandas.read_csv('data_related/storm_event_data.csv', low_memory=False)
    except FileNotFoundError:
        # there is two probable locations of the file, so doesn't make sense to write too many lines about it
        data_set = pandas.read_csv('../data_related/storm_event_data.csv', low_memory=False)
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.max_rows', None)
    data_set.columns = map(str.lower, data_set.columns)
    modifiable_variables = retrieve_variables_to_modify()

    data_set = modify_data_set(data_set, modifiable_variables)  # performing necessary modifications of the data set

    # making a subset where we consider only weather events for which damage is evaluated and bigger than zero

    # low_border, high_border = restrictions_to_sample(data_set, "damage_property")
    # data_with_damage = data_set[
    #     (data_set['damage_property'] >= low_border) & (data_set["damage_property"] <= high_border)].copy()
    # return data_with_damage[list(set(modifiable_variables+putative_predictors))]
    return data_set[putative_predictors + response_variables]


if __name__ == "__main__":
    response = retrieve_response_variables()
    explanatory = retrieve_predictors() + retrieve_non_binary_cat_predictors()
    data = primary_data_management(explanatory, response)
    print(data.head(5))
