import numpy
import pandas


def variable_names_to_uppercase(used_variables):
    # the variables in the code book are written in lowercase, but actually they are in uppper
    # so need a little conversion
    return list(map(str.upper, used_variables))


def all_kind_of_value(data_set, variable):
    kinds = []
    for i in data_set[variable]:
        if i not in kinds:
            kinds.append(i)
    return kinds


def damage_int(row):  # creating the variable damage in int format to avoid 10K 12M 2B etc
    element = row['DAMAGE_PROPERTY']
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


def month_num(row):
    element = row['MONTH_NAME']
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


def modify_data_set(data_set, added_variables):
    for added_variable in added_variables:
        data_set[added_variable] = data_set.apply(eval(added_variable.lower()),
                                                  axis=1)  # adding damage property column in int format
    return data_set


def primary_data_management(putative_predictors):
    data = pandas.read_csv('data_related/storm_event_data.csv', low_memory=False)  # taking data from the file

    new_variables = ("damage_int", "month_num".upper())

    data = modify_data_set(data, new_variables)  # performing necessary modifications for the data set

    # making a subset where we consider only wheather events for which damage is evaluated and bigger than zero
    data_with_damage = data[data['damage_int'] > 0]
    return data_with_damage


if __name__ == "__main__":
    pass
