from variables import *
from data_menegement import primary_data_management
import seaborn
import matplotlib.pyplot as plt


def output_distribution(data_set, categorical):  # showing the distribution of the data set by used variables
    sample_volume = len(data_set)
    print('The sample volume is %i' % sample_volume)  # printing the sample volume
    print('')
    for variable in categorical:
        print("")
        print(f"The {variable} distribution of the damage cost")
        c = data_set.groupby(variable).size()
        print(c)
        pt = c * 100 / sample_volume
        print(f"The percentage {variable} distribution of the damage cost")
        print(pt)


def histogram(variables, data_set):
    for variable in variables:
        seaborn.set()
        seaborn.countplot(y=variable, data=data_set)
        plt.xlabel(f"The {variable} x label")
        plt.ylabel("The number of weather events")
        plt.title(f"The {variable} title")
        plt.show()


def quantitative_plot(variables, data_set):
    for variable in variables:
        seaborn.distplot(data_set[variable].dropna(), kde=False)
        plt.title(f"The {variable} title")  # adding a title
        plt.show()


def description(variables, data_set):
    # also it is possible to use .mode(), .mean() etc instead of .describe
    for variable in variables:
        print(f"Describe {variable}")
        print(data_set[variable].describe())


def univariate_analysis(data_with_damage, categorical, quantitative, response_variables):
    putative_predictors = categorical + quantitative
    output_distribution(data_with_damage, categorical)  # showing the distribution in textual format
    # histogram(putative_predictors, data_with_damage)
    description(categorical + quantitative+response_variables, data_with_damage)
    for variable in response_variables+quantitative:
        plt.boxplot(x=data_with_damage[variable])
        plt.title(f"The {variable} box plot")
        plt.show()
        plt.hist(x=data_with_damage[variable])
        plt.title(f"The {variable} histogram")
        plt.show()


if __name__ == "__main__":
    q_predictors = retrieve_quantitative_predictors()
    cat_predictors = retrieve_non_binary_cat_predictors()
    response = retrieve_cat_response_variables()
    data = primary_data_management(q_predictors+cat_predictors, response)
    response_var = retrieve_cat_response_variables()
    univariate_analysis(data, cat_predictors, q_predictors, response_var)
