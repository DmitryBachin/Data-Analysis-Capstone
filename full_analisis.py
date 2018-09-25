"""
This is the code written for the final project by Dmitry Bachin (dmitrybachin.com)
The course is organized by Wesleyan University (USA) through Courseta.org
"""
from variables import *
from data_menegement import primary_data_management
from univariate_analisis import univariate_analysis


if __name__ == "__main__":
    putative_predictors = retrieve_putative_predictors()
    response_variables = retrieve_response_variables()
    data_with_damage = primary_data_management(putative_predictors)
    univariate_analysis(data_with_damage, putative_predictors, response_variables)