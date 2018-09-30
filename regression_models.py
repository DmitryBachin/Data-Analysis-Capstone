from variables import *
from data_menegement import primary_data_management
from common_functions import *

def regression_modeling(q_explanatory, cat_explanatory, response, data_set):



if __name__ == "__main__":
    # retrieve variables for regression
    quatitative_explanatory_variables = retrieve_quantitative_explanatory_vars()
    categorcal_explanatory_variables = retrieve_cat_explanatory_vars()
    quantitative_response_variables = retrieve_q_response_variables()

    # performing data management with data where property is damaged and evaluated clear
    data = primary_data_management(categorcal_explanatory_variables[:] + categorcal_explanatory_variables[:],
                                   quantitative_response_variables,
                                   """data_set["damage_property"] > 0""")

    # performing regression analysis
    regression_modeling(quatitative_explanatory_variables, categorcal_explanatory_variables,
                        quantitative_response_variables, data)
