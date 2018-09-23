from variables import *
from data_menegement import primary_data_management
import seaborn
import matplotlib.pyplot as plt


def bar_chart(explanatory_variables, response_variables, data_set):
    for r_var in response_variables:
        for e_var in explanatory_variables:
            seaborn.factorplot(x=e_var, y=r_var, data=data_set, kind="bar", ci=None)
            plt.xlabel(e_var)
            plt.ylabel(r_var)
            plt.show()


def scatter_plot(explanatory_variables, response_variables, data_set):
    for r_var in response_variables:
        for e_var in explanatory_variables:
            seaborn.regplot(x=e_var, y=r_var, data=data_set)
            plt.xlabel(e_var)
            plt.ylabel(r_var)
            plt.show()


def bivariate_analysis(data_set, explanatory_variables, response_variables):
    pass


if __name__ == "__main__":
    predictors = retrieve_putative_predictors()
    data = primary_data_management(predictors)
    response_var = retrieve_response_variables()
    bivariate_analysis(data, predictors, response_var)