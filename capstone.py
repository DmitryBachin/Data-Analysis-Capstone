"""
This is the code written for the final project by Dmitry Bachin (dmitrybachin.com)
The course is organized by Wesleyan University (USA) through Courseta.org
"""

""" FUNCTIONS FOR TESTING """


def AllKindOfValue(dataset, Variable):
    Kinds = []
    for i in dataset[Variable]:
        if i not in Kinds:
            Kinds.append(i)
    return Kinds


"""THE MAIN PART"""

import numpy
import pandas

# the variables in the code book are written in lowercase, but actually they are in uppper
# so need a little conversion
Variables = ['event_type', 'month_name', 'state']
Variables = list(map(str.upper, Variables))

data = pandas.read_csv('data_related/storm_event_data.csv', low_memory=False)


def damage_property_int(row):  # creating the variable damage in int format to avoid 10K 12M 2B etc
    element = row['DAMAGE_PROPERTY']

    if type(element) is str:

        if element[-1] == 'K':
            return int(float(element[:-1]) * 1000)
        elif element[-1] == 'M':
            return int(float(element[:-1]) * 1000000)
        else:
            return int(float(element[:-1]) * 1000000000)
    else:
        return 0  # later I plan to exclude both unknown and zero damage, so in this data management step
        # it is possible to assign 0 to unknown damage


data['damage_int'] = data.apply(lambda row: damage_property_int(row), axis=1)

# making a subset where we consider only wheather events for which damage is evalueted and bigger than zero


data = data[data['damage_int'] > 0]

print('The sample volume is %i' % len(data))
print('')
# counting mean and start deviation for damage property

# checking percantege and graph for explanatory variables (all of them are categorical)
for Variable in Variables:
    c = data.groupby(Variable).size()
    print(c)
    pt = c * 100 / len(data)
    print('')


