import numpy
import pandas
from variables import retrieve_variables_to_modify


def all_kind_of_value(data_set, variable):
    kinds = []
    for i in data_set[variable]:
        if i not in kinds:
            kinds.append(i)
    return kinds


def damage_property(row):  # creating the variable damage in int format to avoid 10K 12M 2B etc
    element = row['damage_property']
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


def month_name(row):
    element = row['month_name']
    month_dict = {
        "April": "04.",
        "August": "08.",
        "December": "12.",
        "February": "02.",
        "January": "01.",
        "July": "07.",
        "June": "06.",
        "March": "03.",
        "May": "05.",
        "November": "11.",
        "October": "10.",
        "September": "09."
    }
    return month_dict.get(element, '') + element


def modify_data_set(data_set, variables_to_modify):
    for variable in variables_to_modify:
        # modify the variables
        data_set[variable] = data_set.apply(eval(variable), axis=1)
    return data_set


def primary_data_management(putative_predictors):
    try:
        # taking the data from the file
        data_set = pandas.read_csv('../data_related/storm_event_data.csv', low_memory=False)
    except FileNotFoundError:
        # there is two probable locations of the file, so doesn't make sense to write too many lines about it
        data_set = pandas.read_csv('data_related/storm_event_data.csv', low_memory=False)
    data_set.columns = map(str.lower, data_set.columns)
    modifiable_variables = retrieve_variables_to_modify()

    data_set = modify_data_set(data_set, modifiable_variables)  # performing necessary modifications of the data set

    # making a subset where we consider only weather events for which damage is evaluated and bigger than zero
    data_with_damage = data_set[data_set['damage_property'] > 0].copy()
    return data_with_damage


if __name__ == "__main__":
    pass
