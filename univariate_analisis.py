from variables import *
from data_menegement import primary_data_management
import seaborn
import matplotlib.pyplot as plt


def output_distribution(data_set, variable,
                        sample_volume):  # showing the distribution of the data set by used variables
    # showing the number of events in every category
    print("======================================================================================================")
    print(f"The {variable} variable distribution")
    c = data_set.groupby(variable).size()
    print(c)
    # showing the percentage of events in every category
    pt = c * 100 / sample_volume
    print(f"The percentage {variable} variable distribution")
    print(pt)


def histogram(variable, data_set):
    # histogram for categorical variables, shows the number of event in each category
    seaborn.set()
    seaborn.countplot(y=variable, data=data_set)
    plt.ylabel(f"The {variable}")
    plt.title(f"The number of weather events by {variable}")
    plt.show()


def description(variable, data_set):
    # also it is possible to use .mode(), .mean() etc instead of .describe
    print(f"Describe {variable}")
    print(data_set[variable].describe())
    print(f"The modes are {str(data_set[variable].mode()[1:])}")


def univariate_analysis(data_set, cat_explanatory, q_explanatory, cat_response, q_response):
    print("===========================================================================================================")
    sample_volume = len(data_set)
    print('The sample volume is %i' % sample_volume)  # printing the sample volume
    # performs univariate analysis of all variables
    all_variables = cat_explanatory[:] + q_explanatory[:] + cat_response[:] + q_response[:]

    for variable in all_variables:
        print('=======================================================================================================')
        description(variable, data_set)  # main features of every variable
        if variable in q_response or variable in q_explanatory:
            # showing boxplot and histogram for quantitative variables
            plt.boxplot(x=data_set[variable])
            plt.title(f"The {variable} box plot")
            plt.show()
            plt.hist(x=data_set[variable])
            plt.title(f"The {variable} histogram")
            plt.show()
        else:
            output_distribution(data_set, variable, sample_volume)  # showing the distribution in textual format
            histogram(variable, data_set) # showing histogram for categorical variables



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
