from variables import *
from data_menegement import primary_data_management
import seaborn
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi
import pandas as pd
import scipy.stats
from itertools import combinations
from tabulate import tabulate
import os
import numpy as np


def bar_chart(e_var, r_var, data_set):
    seaborn.catplot(x=r_var, y=e_var, orient='h', data=data_set, kind="bar")
    plt.xlabel(r_var)
    plt.ylabel(e_var)
    plt.show()


def scatter_plot(e_var, r_var, data_set):
    seaborn.regplot(x=e_var, y=r_var, data=data_set)
    plt.xlabel(e_var)
    plt.ylabel(r_var)
    plt.show()


def chi_square(e_var, r_var, data_set):
    tab = pd.crosstab(data_set[r_var], data_set[e_var])
    col_sum = tab.sum(axis=0)
    col_pct = tab / col_sum
    test_result = scipy.stats.chi2_contingency(tab)
    return test_result


def analysis_of_variance(e_var, r_var, data_set):
    model = smf.ols(formula="%s~C(%s)" % (r_var, e_var), data=data_set)
    return model.fit()


def post_hoc_tukey(data_set, e_var, r_var):
    m_comparison = multi.MultiComparison(data_set[r_var], data_set[e_var])
    return m_comparison.tukeyhsd()


def comparison_dict_to_table(comparison_dict, e_var, r_var, method=''):
    categories = set([i for i, _ in comparison_dict] + [j for _, j in comparison_dict])
    categories = sorted(categories)
    table = [['*'] + list(categories)]
    for i in categories:
        table.append([i])
        for j in categories:
            if (i, j) in comparison_dict:
                value = comparison_dict[i, j]
            elif (j, i) in comparison_dict:
                value = comparison_dict[j, i]
            elif i == j:
                value = '*'
            else:
                value = '_'
            table[-1].append(value)
    csv = ',\n'.join([','.join(line) for line in table])
    if not os.path.exists("results"):
        os.makedirs("results")
    with open(f"results/{method}_response_{r_var}__explanatory_{e_var}.csv", 'w') as f:
        f.write(csv)
    return tabulate(table[1:], headers=table[0]) if len(table) > 0 else ''


def post_hoc_chi(data_set, e_var, r_var):
    e_values = data_set[e_var].unique()
    pairs = [i for i in combinations(e_values, 2)]
    comparison_dict = {}
    for e_pair in pairs:
        df = data_set[(data_set[e_var] == e_pair[0]) | (data_set[e_var] == e_pair[1])]
        pair_result = chi_square(e_var, r_var, df)
        if pair_result[1] < 0.05 / len(pairs):
            comparison_dict[e_pair] = str(pair_result[1])

    return comparison_dict


def post_hoc_anova_to_dict(df):
    comparison_dict = {}
    for _, row in df.iterrows():
        comparison_dict[row["group1"], row["group2"]] = str(row["meandiff"])
    return comparison_dict


def post_hoc_true(tukey_result):
    # creating a data frame with the data of post hoc test where the null hypothesis is rejected
    df = pd.DataFrame(data=tukey_result._results_table.data[1:],  # creating a data frame with the results
                      columns=tukey_result._results_table.data[0])
    results = df[df["reject"] == True]  # throwing away the results which are not successful
    return post_hoc_anova_to_dict(results[["group1", "group2", "meandiff"]])


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
                print(comparison_dict_to_table(post_hoc_rejected, e_var, r_var, "ANOVA"))

        for e_var in e_q_variables:
            print("===================================================================================================")
            print(f"The response variable is {r_var}. The explanatory variable is {e_var}. Pearson correlation")
            scatter_plot(e_var, r_var, data_set)
            print(scipy.stats.pearsonr(data_set[e_var], data_set[r_var]))

    if r_cat_variables and e_q_variables:  # if response is categorical and explanatory is quantitative
        # we need to transform explanatory variables to categorical
        pass

    for r_var in r_cat_variables:
        for e_var in e_cat_variables:
            print("===================================================================================================")
            print(f"The response variable is {r_var}. The explanatory variable is {e_var}. Chi-square")
            bar_chart(e_var, r_var, data_set)
            result = chi_square(e_var, r_var, data_set)
            print("chi-square value, p-value")
            print(result[:2])
            if len(result) >= 2 and result[1] < 0.05:
                post_hoc_test = post_hoc_chi(data_set, e_var, r_var)
                print(comparison_dict_to_table(post_hoc_test, e_var, r_var, 'Chi-Square'))


if __name__ == "__main__":
    cat_predictors = retrieve_non_binary_cat_predictors()
    cat_response_var = retrieve_cat_response_variables()
    q_predictors = retrieve_quantitative_predictors()
    q_response = retrieve_q_response_variables()
    # data = primary_data_management(cat_predictors, cat_response_var)
    # bivariate_analysis(data, [], cat_predictors, [], cat_response_var)
    data = primary_data_management(cat_predictors+q_predictors, q_response, """(data_set["damage_property"] > 0)""")
    bivariate_analysis(data, q_predictors, cat_predictors, q_response, [])
