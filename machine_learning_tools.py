from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from variables import *
from data_menegement import primary_data_management
from sklearn.model_selection import train_test_split
import sklearn
from sklearn import tree
from io import StringIO
from IPython.display import Image
import pydotplus
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model import LassoLarsCV
import os
import pprint
from common_functions import *

os.environ["PATH"] += os.pathsep + 'C:\\Program Files (x86)\\Graphviz2.38\\bin'


def recode_categorical_variables(data_set, variables):
    data_to_modify = data_set[variables].copy()
    vectors = [one_hot_encoding(data_to_modify, variable) for variable in data_to_modify.columns.values]
    modified_data = pd.concat(vectors, axis=1)
    return modified_data


def retrieve_clean_data(uncleaned_data, variables=None):
    if variables:
        for variable in variables:
            uncleaned_data.dropna(subset=[variable], inplace=True)
        return uncleaned_data
    else:
        return uncleaned_data.dropna()


def decision_tree(pred_train, pred_test, tar_train, tar_test, random_forest=False):
    classifier = DecisionTreeClassifier() if not random_forest else RandomForestClassifier(n_estimators=25)
    classifier = classifier.fit(pred_train, tar_train)
    predictions = classifier.predict(pred_test)
    result = sklearn.metrics.confusion_matrix(tar_test, predictions)
    print("The confusion matrix of the tree")
    print(result)
    accuracy = sklearn.metrics.accuracy_score(tar_test, predictions)
    print(f"The accuracy score is {accuracy}")
    report = sklearn.metrics.classification_report(tar_test, predictions)
    print(report)
    if not random_forest:
        dot_data = tree.export_graphviz(classifier, out_file=None)
        graph = pydotplus.graph_from_dot_data(dot_data)
        Image(graph.create_png())
        graph.write_png("result.png")
    else:
        model = ExtraTreesClassifier()
        model.fit(pred_train, tar_train)
        print(model.feature_importances_)

        trees = range(25)
        accuracy = np.zeros(25)
        for i in trees:
            classifier = RandomForestClassifier(n_estimators=i + 1)
            classifier = classifier.fit(pred_train, tar_train)
            predictions = classifier.predict(pred_test)
            accuracy[i] = sklearn.metrics.accuracy_score(tar_test, predictions)
        plt.cla()
        plt.plot(trees, accuracy)
        plt.show()


def lasso_regression(pred_train, pred_test, tar_train, tar_test, predictors):
    model = LassoLarsCV(cv=10, precompute=False).fit(pred_train, tar_train)
    result = dict(zip(predictors, model.coef_))
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result)
    # TODO: make the regression plot work normally


def machine_learning_general(data_sub_set, targets, predictors, categorical):
    print("=============Machine Learning tools==============================================")
    data_sub_set = retrieve_clean_data(data_sub_set, targets + predictors + categorical)  # dropping values
    cat_predictors = recode_categorical_variables(data_sub_set, categorical)
    for target in targets:
        pred_train, pred_test, tar_train, tar_test = train_test_split(cat_predictors,
                                                                      data_sub_set[target],
                                                                      test_size=.3)
        print(f"The size of the training set is {pred_train.shape[0]}")
        print(f"The size of the test set is {pred_test.shape[0]}")
        # decision_tree(pred_train, pred_test, tar_train, tar_test, random_forest=True)
        lasso_regression(pred_train, pred_test, tar_train, tar_test, cat_predictors)


if __name__ == "__main__":
    # taking variables which are appropriate for machine learning
    target_variables = retrieve_cat_response_variables()
    quantitative_predictors = retrieve_quantitative_explanatory_vars()
    categorical_predictors = retrieve_cat_explanatory_vars()

    # for machine learning tools we work only with the "property_damaged" variable because it is binary
    data = primary_data_management(quantitative_predictors + categorical_predictors, target_variables)

    # performing the machine learning
    machine_learning_general(data, target_variables, quantitative_predictors, categorical_predictors)
