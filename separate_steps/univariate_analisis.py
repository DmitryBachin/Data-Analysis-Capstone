from variables import retrieve_putative_predictors
from data_menegement import primary_data_management
import seaborn
import matplotlib.pyplot as plt


def output_distribution(data_set, used_variables):  # showing the distribution of the data set by used variables
    sample_volume = len(data_set)
    print('The sample volume is %i' % sample_volume)  # printing the sample volume
    print('')
    for variable in used_variables:
        print("")
        print(f"The {variable} distribution of the damage cost")
        c = data_set.groupby(variable).size()
        print(c)
        pt = c * 100 / sample_volume
        print(f"The percentage {variable} distribution of the damage cost")
        print(pt)


def univariate_analysis(data_with_damage, putative_predictors):
    # output_distribution(data_with_damage, putative_predictors)  # showing the distribution in textual format
    for variable in putative_predictors:
        seaborn.set(style="darkgrid")
        seaborn.countplot(x=variable, data=data_with_damage)
        plt.xlabel(f"The {variable} x label")
        plt.title(f"The {variable} title")
        plt.show()

if __name__ == "__main__":
    predictors = retrieve_putative_predictors()
    data = primary_data_management(predictors)
    univariate_analysis(data, predictors)
