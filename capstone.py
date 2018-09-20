"""
This is the code written for the final project by Dmitry Bachin (dmitrybachin.com)
The course is organized by Wesleyan University (USA) through Courseta.org
"""
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


def damage_property_int(row):  # creating the variable damage in int format to avoid 10K 12M 2B etc
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


def modify_data_set(data_set):
    data_set['damage_int'] = data_set.apply(damage_property_int, axis=1)  # adding damage property column in int format
    return data_set


def output_distribution(data_set, used_variables):  # showing the distribution of the data set by used variables
    print('The sample volume is %i' % len(data_with_damage))  # printing the sample volume
    print('')
    for variable in used_variables:
        c = data_set.groupby(variable).size()
        print(c)
        pt = c * 100 / len(data_set)
        print(pt)


if __name__ == "__main__":
    variables = ['event_type', 'month_name', 'state']  # the list of used variables
    variables = variable_names_to_uppercase(variables)  # transform all variables to upper case
    data = pandas.read_csv('data_related/storm_event_data.csv', low_memory=False)  # taking data from the file
    data = modify_data_set(data)  # performing necessary modifications for the data set

    # making a subset where we consider only wheather events for which damage is evaluated and bigger than zero
    data_with_damage = data[data['damage_int'] > 0]

    output_distribution(data_with_damage, variables)  # showing the distribution in textual format
    # TODO: counting mean and start deviation for damage property,

    # TODO: break on functions,

    # TODO: make a plan,

    # checking percantege and graph for explanatory variables (all of them are categorical
