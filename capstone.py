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


"""THE MAIN PART"""

# the variables in the code book are written in lowercase, but actually they are in uppper
# so need a little conversion
variables = ['event_type', 'month_name', 'state']
variables = list(map(str.upper, variables))

data = pandas.read_csv('data_related/storm_event_data.csv', low_memory=False)


def damage_property_int(row):  # creating the variable damage in int format to avoid 10K 12M 2B etc
    element = row['DAMAGE_PROPERTY']
    multiplier = {
        'K': 1000,
        'M': 1000*1000,
        'B': 1000*1000*1000
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


data['damage_int'] = data.apply(lambda row: damage_property_int(row), axis=1)

# making a subset where we consider only wheather events for which damage is evalueted and bigger than zero

data_with_damage = data[data['damage_int'] > 0]

print('The sample volume is %i' % len(data_with_damage))
print('')
# TODO: counting mean and start deviation for damage property

# checking percantege and graph for explanatory variables (all of them are categorical)
for variable in variables:
    c = data_with_damage.groupby(variable).size()
    print(c)
    pt = c * 100 / len(data_with_damage)
    print(pt)
