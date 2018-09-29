from variables import *
from data_menegement import primary_data_management
import seaborn
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi
import pandas as pd
import scipy.stats


def bar_chart(e_var, r_var, data_set):
    seaborn.factorplot(y=e_var, x=r_var, data=data_set, kind="bar", ci=None)
    plt.xlabel(e_var)
    plt.ylabel(r_var)
    plt.show()


def scatter_plot(e_var, r_var, data_set):
    seaborn.regplot(x=e_var, y=r_var, data=data_set)
    plt.xlabel(e_var)
    plt.ylabel(r_var)
    plt.show()


def chi_square(e_var, r_var, data_set):
    tab = pd.crosstab(data_set[r_var], data_set[e_var])
    print(tab)
    col_sum = tab.sum(axis=0)
    col_pct = tab / col_sum
    print(col_pct)
    test_result = scipy.stats.chi2_contingency(tab)
    print(test_result)
    return test_result


def analysis_of_variance(e_var, r_var, data_set):
    model = smf.ols(formula="%s~C(%s)" % (r_var, e_var), data=data_set)
    return model.fit()


def post_hoc_tukey(data_set, e_var, r_var):
    m_comparison = multi.MultiComparison(data_set[r_var], data_set[e_var])
    return m_comparison.tukeyhsd()


def post_hoc_chi(data_set, e_var, r_var):
    e_values = data_set[e_var].unique()
    for


def post_hoc_true(tukey_result):
    # creating a data frame with the data of post hoc test where the null hypothesis is rejected
    df = pd.DataFrame(data=tukey_result._results_table.data[1:],  # creating a data frame with the results
                      columns=tukey_result._results_table.data[0])
    results = df[df["reject"] == True]  # throwing away the results which are not successful
    return results[["group1", "group2", "meandiff"]]


def bivariate_analysis(data_set, e_q_variables, e_cat_variables, r_q_variables, r_cat_variables):
    for r_var in r_q_variables:
        for e_var in e_cat_variables:
            print("===================================================================================================")
            print(f"The response variable is {r_var}. The explanatory variable is {e_var}. ANOVA")
            bar_chart(e_var, r_var, data_set)
            model_fit = analysis_of_variance(e_var, r_var, data_set)
            summary = model_fit.summary()
            print(summary)
            if model_fit.f_pvalue < 0.05:
                post_hoc_test = post_hoc_tukey(data_set, e_var, r_var)
                post_hoc_rejected = post_hoc_true(post_hoc_test)
                print(post_hoc_rejected)

        for e_q_variables in e_q_variables:
            print("===================================================================================================")
            print(f"The response variable is {r_var}. The explanatory variable is {e_var}. Correlation analysis")

    if r_cat_variables and e_q_variables:  # if response is categorical and explanatory is quantitative
        # we need to transform explanatory variables to categorical
        pass

    for r_var in r_cat_variables:
        for e_var in e_cat_variables:
            print("===================================================================================================")
            print(f"The response variable is {r_var}. The explanatory variable is {e_var}. Chi-square")
            bar_chart(e_var, r_var, data_set)
            result = chi_square(e_var, r_var, data_set)
            if len(result) >= 2 and result[1] < 0.05:
                post_hoc_test = post_hoc_chi(data_set, e_var, r_var)


if __name__ == "__main__":
    cat_predictors = retrieve_non_binary_cat_predictors()
    cat_response_var = retrieve_cat_response_variables()
    data = primary_data_management(cat_predictors, cat_response_var)
    bivariate_analysis(data, [], cat_predictors, [], cat_response_var)
