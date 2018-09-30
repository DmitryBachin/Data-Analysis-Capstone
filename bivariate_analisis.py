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
import operator


def bar_chart(e_var, r_var, data_set):
    # creates bar chart with confidence intervals
    seaborn.catplot(x=r_var, y=e_var, orient='h', data=data_set, kind="bar")
    plt.xlabel(r_var)
    plt.ylabel(e_var)
    plt.show()


def scatter_plot(e_var, r_var, data_set):
    # creates scatterplot
    seaborn.regplot(x=e_var, y=r_var, data=data_set)
    plt.xlabel(e_var)
    plt.ylabel(r_var)
    plt.show()


def chi_square(e_var, r_var, data_set):
    # performs chi-square test
    tab = pd.crosstab(data_set[r_var], data_set[e_var])
    test_result = scipy.stats.chi2_contingency(tab)
    return test_result


def analysis_of_variance(e_var, r_var, data_set):
    # performs ANOVA
    model = smf.ols(formula="%s~C(%s)" % (r_var, e_var), data=data_set)
    return model.fit()


def post_hoc_tukey(data_set, e_var, r_var):
    # performs tukey post hos test
    m_comparison = multi.MultiComparison(data_set[r_var], data_set[e_var])
    return m_comparison.tukeyhsd()


def comparison_dict_to_table(comparison_dict, e_var='', r_var='', method=''):
    # the result of post hoc test is presented as a dict with tuple of 2 categories and some value if they are
    # statistically different

    # retrieving all existing categories
    categories = set([i for i, _ in comparison_dict] + [j for _, j in comparison_dict])
    categories = sorted(categories)

    # counter will show which categories are more different from other ones
    counter = {key: len(categories) - 1 for key in categories}
    counter["MAXIMUM NUMBER OF DIFFERENCES"] = len(categories) - 1

    table = [['*'] + list(categories)] # creating the header line of the future table
    for i in categories:
        table.append([i])  # adding the first element
        for j in categories:
            if (i, j) in comparison_dict:
                value = comparison_dict[i, j]  # adding p-value or mean difference (depending of the test)
            elif (j, i) in comparison_dict:
                value = comparison_dict[j, i]  # adding p-value or mean difference (depending of the test)
            elif i == j:
                value = '*'  # marking the same categories
            else:
                value = '_'  # marking pairs who are no proofed to be different
                counter[i] -= 1  # subtract one if the categoy is in the pair
            table[-1].append(value)

    csv = ',\n'.join([','.join(line) for line in table])  # creating text for csv file

    if not os.path.exists("results"):  # creating the directory if it doesn't exist
        os.makedirs("results")

    with open(f"results/{method}_response_{r_var}__explanatory_{e_var}.csv", 'w') as f:
        f.write(csv) # writing csv into a file

    # creating the result tables to show in the console
    text_table = tabulate(table[1:], headers=table[0]) if len(table) > 0 else ''
    counter = tabulate(sorted(counter.items(), key=operator.itemgetter(1), reverse=True))
    return text_table, counter


def post_hoc_chi(data_set, e_var, r_var):
    # performing post hoc test with Bonferroni adjustment
    # works only if the response variable has two categories
    e_values = data_set[e_var].unique()  # retrieving all explanatory categories
    pairs = [i for i in combinations(e_values, 2)]  # create the list of combinations between two categories
    comparison_dict = {}
    for e_pair in pairs:
        # leaving only two categories
        df = data_set[(data_set[e_var] == e_pair[0]) | (data_set[e_var] == e_pair[1])].copy()
        # performing chi_square again
        pair_result = chi_square(e_var, r_var, df)
        if pair_result[1] < CRITICAL_VALUE / len(pairs):
            # if we reject null hypothesis, add it to comparison dict with p_value
            comparison_dict[e_pair] = str(pair_result[1])

    return comparison_dict


def post_hoc_anova_to_dict(df):
    # transforming the dataframe with the result of post hoc tukey to comparison dictionary
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
    # performs bivariate analysis
    for r_var in r_q_variables:  # dealing with quantitative response variables
        for e_var in e_cat_variables:  # dealing with categorical explanatory variables
            print("===================================================================================================")
            print(f"The response variable is {r_var}. The explanatory variable is {e_var}. ANOVA")
            bar_chart(e_var, r_var, data_set)  # showing result as a bar chart
            model_fit = analysis_of_variance(e_var, r_var, data_set)  # testing the model
            summary = model_fit.summary()  # printing the summary
            print(summary)
            if model_fit.f_pvalue < CRITICAL_VALUE and len(data_set[e_var].unique()) > 2:
                # if we reject null hypothesis and have than 2 categories
                # we need post host hoc test
                post_hoc_test = post_hoc_tukey(data_set, e_var, r_var)
                post_hoc_rejected = post_hoc_true(post_hoc_test)  # taking only the pairs where we reject H0
                text_table, counter = comparison_dict_to_table(post_hoc_rejected, e_var, r_var, "ANOVA")
                print(text_table)  # printing the post hoc test result the mean difference in response var shown if
                # the result between the pair is confident
                print(counter)  # printing the post hoc test result

        for e_var in e_q_variables:  # dealing with quantitative explanatory variables
            print("===================================================================================================")
            print(f"The response variable is {r_var}. The explanatory variable is {e_var}. Pearson correlation")
            scatter_plot(e_var, r_var, data_set)  # printing the scatterplot
            print("R, p-value")
            print(scipy.stats.pearsonr(data_set[e_var], data_set[r_var])) # performing Person correlation

    if r_cat_variables and e_q_variables:  # if response is categorical and explanatory is quantitative
        # we need to transform explanatory variables to categorical
        # will be added later if needed
        pass

    for r_var in r_cat_variables:  # dealing with categorical response variables
        for e_var in e_cat_variables:  # dealing with categorical explanatory variables
            print("===================================================================================================")
            print(f"The response variable is {r_var}. The explanatory variable is {e_var}. Chi-square")
            bar_chart(e_var, r_var, data_set)  # showing result as a bar chart
            result = chi_square(e_var, r_var, data_set)  # making chi-square test
            print("chi-square value, p-value")
            print(result[:2])
            if len(result) >= 2 and result[1] < CRITICAL_VALUE:  # if p-value lower than critical value...
                post_hoc_test = post_hoc_chi(data_set, e_var, r_var)  # performing the post hoc test
                text_table, counter = comparison_dict_to_table(post_hoc_test, e_var, r_var, 'Chi-Square')
                print(text_table)  # printing the post hoc test result p-value are shown in they are
                # lower than p-value after Bonferroni adjustment
                print(counter)  # printing the post hoc test result


if __name__ == "__main__":
    # retrieving all variables for the research
    categorical_explanatory_variables = retrieve_cat_explanatory_vars()
    categorical_response_variables = retrieve_cat_response_variables()
    quantitative_explanatory_variables = retrieve_quantitative_explanatory_vars()
    quantitative_response_variables = retrieve_q_response_variables()

    # preforming primary data management, adding new variables (more details in variables.py or in the report.pdf)
    data = primary_data_management(categorical_explanatory_variables, categorical_response_variables)
    bivariate_analysis(data, [], categorical_explanatory_variables, [], categorical_response_variables)

    # performing univariate analysis with data where property is damage and evaluated clear
    data = primary_data_management(categorical_explanatory_variables + quantitative_explanatory_variables,
                                   quantitative_response_variables, """(data_set["damage_property"] > 0)""")
    bivariate_analysis(data, quantitative_explanatory_variables, categorical_explanatory_variables,
                       quantitative_response_variables, [])
