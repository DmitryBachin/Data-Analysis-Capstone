from variables import *
from data_menegement import primary_data_management
import seaborn
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi
import pandas as pd


def bar_chart(e_var, r_var, data_set):
    seaborn.factorplot(x=e_var, y=r_var, data=data_set, kind="bar", ci=None)
    plt.xlabel(e_var)
    plt.ylabel(r_var)
    plt.show()


def scatter_plot(e_var, r_var, data_set):
    seaborn.regplot(x=e_var, y=r_var, data=data_set)
    plt.xlabel(e_var)
    plt.ylabel(r_var)
    plt.show()


def analysis_of_variance(e_var, r_var, data_set):
    model = smf.ols(formula="%s~C(%s)" % (r_var, e_var), data=data_set)
    return model.fit()


def post_hoc(data_set, e_var, r_var):
    m_comparison = multi.MultiComparison(data_set[r_var], data_set[e_var])
    return m_comparison.tukeyhsd()


def post_hoc_true(tukey_result):
    # creating a data frame with the data of post hoc test where the null hypothesis is rejected
    df = pd.DataFrame(data=tukey_result._results_table.data[1:],  # creating a data frame with the results
                      columns=tukey_result._results_table.data[0])
    results = df[df["reject"] == True]  # throwing away the results which are not successful
    return results[["group1", "group2", "meandiff"]]


def bivariate_analysis(data_set, explanatory_variables, response_variables):
    for r_var in response_variables:
        for e_var in explanatory_variables:
            bar_chart(e_var, r_var, data_set)
            model_fit = analysis_of_variance(e_var, r_var, data_set)
            summary = model_fit.summary()
            print(summary)
            if model_fit.f_pvalue < 0.05:
                post_hoc_test = post_hoc(data_set, e_var, r_var)
                post_hoc_rejected =post_hoc_true(post_hoc_test)
                print(post_hoc_rejected)


if __name__ == "__main__":
    predictors = retrieve_putative_predictors()
    data = primary_data_management(predictors)
    response_var = retrieve_response_variables()
    bivariate_analysis(data, predictors, response_var)
