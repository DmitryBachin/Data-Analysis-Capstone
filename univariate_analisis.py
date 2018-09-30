from variables import *
from data_menegement import primary_data_management
import seaborn
import matplotlib.pyplot as plt


def output_distribution(data_set, categorical):  # showing the distribution of the data set by used variables
    sample_volume = len(data_set)
    print('The sample volume is %i' % sample_volume)  # printing the sample volume
    print('')
    for variable in categorical:
        print("======================================================================================================")
        print(f"The {variable} variable distribution")
        c = data_set.groupby(variable).size()
        print(c)
        pt = c * 100 / sample_volume
        print(f"The percentage {variable} variable distribution")
        print(pt)


def histogram(variable, data_set):
    seaborn.set()
    seaborn.countplot(y=variable, data=data_set)
    plt.ylabel(f"The {variable}")
    plt.title(f"The number of weather events by {variable}")
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


def univariate_analysis(data_with_damage, cat_explanatory, q_explanaroty, cat_response, q_response):
    # performs univariate analysis of in
    all_variables = cat_explanatory[:] + q_explanaroty[:] + cat_response[:] + q_response[:]
    output_distribution(data_with_damage, cat_explanatory + cat_response)  # showing the distribution in textual format
    description(all_variables, data_with_damage)
    for variable in all_variables:
        print("=====================================================================================================")
        if variable in q_response or variable in q_explanaroty:
            plt.boxplot(x=data_with_damage[variable])
            plt.title(f"The {variable} box plot")
            plt.show()
            plt.hist(x=data_with_damage[variable])
            plt.title(f"The {variable} histogram")
            plt.show()
        else:
            histogram(variable, data_with_damage)


if __name__ == "__main__":
    # retrieving all variables for the research
    categorical_explanatory_variable = retrieve_non_binary_cat_explanatory_vars()
    categorical_response_variables = retrieve_cat_response_variables()
    quantitative_independent_variables = retrieve_quantitative_explanatory_vars()
    quantitative_response_variables = retrieve_q_response_variables()

    # preforming primary data management, adding new variables (more details in variables.py or in the report.pdf)
    data = primary_data_management(categorical_explanatory_variable[:] + quantitative_independent_variables[:],
                                   categorical_response_variables[:])

    # performing univariate analysis for  all data where damage_property is not nan
    univariate_analysis(data, categorical_explanatory_variable[:], quantitative_independent_variables[:],
                        categorical_response_variables[:], [])

    # performing the data management to work only with data where property is damage and evaluated clear
    data = primary_data_management(categorical_explanatory_variable[:] + quantitative_independent_variables[:],
                                   quantitative_response_variables[:],
                                   """(data_set["damage_property"] > 0)""")

    # performing univariate analysis with data where property is damage and evaluated clear
    univariate_analysis(data, categorical_explanatory_variable[:], quantitative_independent_variables[:], [],
                        quantitative_response_variables[:])
