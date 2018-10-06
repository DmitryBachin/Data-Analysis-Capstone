from variables import *
from data_menegement import primary_data_management
from common_functions import *
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf


def formula_creation(r_var, q_e_vars, cat_e_vars, data_set):
    # creating the formula for ols
    formula = f"{r_var} ~ " + " + ".join(q_e_vars)
    references = {
        "climate_region":"Other",
    }

    for variable in cat_e_vars:
        reference_value = references.get(variable, data_set[variable].unique()[0])
        formula += f" + C({variable}, Treatment(reference='{reference_value}'))"
    return formula


def regression_modeling(q_explanatory, cat_explanatory, response, data_set):
    # centering quantitative variables
    for variable in q_explanatory:
        mean = data_set[variable].mean()
        data_set[variable] = data_set[variable] - mean
        print(f"The variable {variable} was centralized. The value {mean} was substracted from every row.")

    for r_var in response:
        formula = formula_creation(r_var, q_explanatory, cat_explanatory, data_set)
        print(formula)
        regression_model = smf.ols(formula, data=data_set).fit()
        summary = regression_model.summary()
        print(summary)


if __name__ == "__main__":
    # retrieve variables for regression
    quantitative_explanatory_variables = retrieve_quantitative_explanatory_vars()
    categorical_explanatory_variables = retrieve_cat_explanatory_vars()
    quantitative_response_variables = retrieve_q_response_variables()
    categorical_explanatory_variables.pop("cz_type", None)

    # performing data management with data where property is damaged and evaluated clear
    data = primary_data_management({**quantitative_explanatory_variables, **categorical_explanatory_variables},
                                   quantitative_response_variables.copy(),
                                   """data_set["damage_property"] > 0""")

    # performing regression analysis
    regression_modeling(quantitative_explanatory_variables.copy(), categorical_explanatory_variables.copy(),
                        quantitative_response_variables.copy(), data)
