"""
This is the code written for the final project by Dmitry Bachin (dmitrybachin.com)
The course is organized by Wesleyan University (USA) through Courseta.org
"""
from data_menegement import primary_data_management,variable_names_to_uppercase


def output_distribution(data_set, used_variables):  # showing the distribution of the data set by used variables
    print('The sample volume is %i' % len(data_set))  # printing the sample volume
    print('')
    for variable in used_variables:
        c = data_set.groupby(variable).size()
        print(c)
        pt = c * 100 / len(data_set)
        print(pt)


if __name__ == "__main__":
    putative_predictors = ['event_type', 'month_num', 'state'] # the list of used variables in upper case
    putative_predictors = variable_names_to_uppercase(putative_predictors)
    data_with_damage = primary_data_management(putative_predictors)
    output_distribution(data_with_damage, putative_predictors)  # showing the distribution in textual format
    # TODO: counting mean and start deviation for damage property,

    # TODO: break on functions,

    # TODO: make a plan,

    # checking percantege and graph for explanatory variables (all of them are categorical
