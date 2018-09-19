"""
This is the code written for the final project by Dmitry Bachin (dmitrybachin.com)
The course is organized by Wesleyan University (USA) through Courseta.org
"""
import numpy
import pandas

""" FUNCTIONS FOR TESTING """


def all_kind_of_value(data_set, variable):
    kinds = []
    for i in data_set[variable]:
        if i not in kinds:
            kinds.append(i)
    return kinds


def damage_property_int(row):  # creating the variable damage in int format to avoid 10K 12M 2B etc
    element = row['DAMAGE_PROPERTY']
    multiplier = {
        'K': 10 ** 3,
        'M': 10 ** 6,
        'B': 10 ** 9
    }
    if type(element) is str:
        if element[-1] in multiplier:
            return int(float(element[:-1]) * multiplier[element[-1]])
        else:
            try:
                return int(element[:])
            except ValueError:
                print(f'The value {element} was not transformed properly')
                return None
    else:
        return None


def modify_data_set(data_set):
    data_set['damage_int'] = data_set.apply(lambda row: damage_property_int(row), axis=1)
    return data_set


def output_distribution(data_set, used_variables):
    print('The sample volume is %i' % len(data_with_damage))
    print('')
    for variable in used_variables:
        c = data_set.groupby(variable).size()
        print(c)
        pt = c * 100 / len(data_set)
        print(pt)


if __name__ == "__main__":
    # the variables in the code book are written in lowercase, but actually they are in uppper
    # so need a little conversion
    variables = ['event_type', 'month_name', 'state']
    variables = list(map(str.upper, variables))

    data = pandas.read_csv('data_related/storm_event_data.csv', low_memory=False)
    data = modify_data_set(data)

    # making a subset where we consider only wheather events for which damage is evalueted and bigger than zero

    data_with_damage = data[data['damage_int'] > 0]

    output_distribution(data_with_damage, variables)
    # TODO: counting mean and start deviation for damage property,

    # TODO: break on functions,

    # TODO: make a plan,

    # checking percantege and graph for explanatory variables (all of them are categorical
