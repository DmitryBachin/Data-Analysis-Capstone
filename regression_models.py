from variables import *
from data_menegement import primary_data_management
from common_functions import *
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf


def formula_creation(r_var, e_vars):
    # creating the formula for ols
    return f"{r_var} ~ " + " + ".join(e_vars)


def regression_modeling(q_explanatory, cat_explanatory, response, data_set):
    # centering quantitative variables
    for variable in q_explanatory:
        data_set[variable] = data_set[variable] - data_set[variable].mean()

    for r_var in response:
        formula = formula_creation(r_var, explanatory_variables)
        print(formula)
        regression_model = smf.ols(formula, data=data_set).fit()
        print(regression_model.summary())


if __name__ == "__main__":
    # retrieve variables for regression
    quantitative_explanatory_variables = retrieve_quantitative_explanatory_vars()
    categorical_explanatory_variables = retrieve_cat_explanatory_vars()
    quantitative_response_variables = retrieve_q_response_variables()
    categorical_response_variables = retrieve_cat_response_variables()

    categorical_explanatory_variables.remove("event_type")  # too much categories

    # performing data management with data where property is damaged and evaluated clear
    data = primary_data_management(quantitative_explanatory_variables[:] + categorical_explanatory_variables[:],
                                   quantitative_response_variables[:],
                                   """data_set["damage_property"] > 0""")

    # performing regression analysis
    regression_modeling(quantitative_explanatory_variables[:], categorical_explanatory_variables[:],
                        quantitative_response_variables[:], data)
    #
    # # performing data management with data where property is damaged and evaluated clear
    # data = primary_data_management(quantitative_explanatory_variables[:] + categorical_explanatory_variables[:],
    #                                categorical_response_variables[:])
    #
    # # preforming regression analysis
    # logistic_regression(quantitative_explanatory_variables, categorical_explanatory_variables,
    #                     categorical_response_variables, data)
