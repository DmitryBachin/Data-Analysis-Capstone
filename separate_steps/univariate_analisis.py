from variables import retrieve_putative_predictors
from data_menegement import primary_data_management


def output_distribution(data_set, used_variables):  # showing the distribution of the data set by used variables
    print('The sample volume is %i' % len(data_set))  # printing the sample volume
    print('')
    for variable in used_variables:
        c = data_set.groupby(variable).size()
        print(c)
        pt = c * 100 / len(data_set)
        print(pt)


def univariate_analysis(data_with_damage, putative_predictors):
    output_distribution(data_with_damage, putative_predictors)  # showing the distribution in textual format


if __name__ == "__main__":
    putative_predictors = retrieve_putative_predictors()
    data = primary_data_management(putative_predictors)
    univariate_analysis(data, putative_predictors)
