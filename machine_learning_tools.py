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
import matplotlib.pyplot as plt

os.environ["PATH"] += os.pathsep + 'C:\\Program Files (x86)\\Graphviz2.38\\bin'


def retrieve_clean_data(uncleaned_data, variables=None):
    # throwing away any missing results
    if variables:
        for variable in variables:
            uncleaned_data.dropna(subset=[variable], inplace=True)
        return uncleaned_data
    else:
        return uncleaned_data.dropna()


def print_dict(non_pretty_dict):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(non_pretty_dict)


def decision_tree(pred_train, pred_test, tar_train, tar_test, random_forest=False):
    # the function which creates regular decision tree or performs random forest
    if not random_forest:
        classifier = DecisionTreeClassifier(criterion="gini", splitter='random', max_leaf_nodes=20, min_samples_leaf=5,
                                            max_depth=5, random_state=123)
    else:
        classifier = RandomForestClassifier(n_estimators=25, random_state=123)
    classifier = classifier.fit(pred_train, tar_train)
    predictions = classifier.predict(pred_test)
    result = sklearn.metrics.confusion_matrix(tar_test, predictions)  # creating and printing the confusion matrix
    print("The confusion matrix of the tree")
    print(result)
    accuracy = sklearn.metrics.accuracy_score(tar_test, predictions)  # retrieving the accuracy score
    print(f"The accuracy score is {accuracy}")
    report = sklearn.metrics.classification_report(tar_test, predictions)  # retrieving the summary of the model
    print(report)
    if not random_forest:
        # creating a graph of the decision tree
        dot_data = tree.export_graphviz(classifier, feature_names=pred_train.columns, filled=True, rounded=True,
                                        out_file=None)
        graph = pydotplus.graph_from_dot_data(dot_data)
        Image(graph.create_png())
        graph.write_png("results/decision_tree.png")
    else:
        # if it is random forest we need some additional tests
        model = ExtraTreesClassifier()
        model.fit(pred_train, tar_train)
        # showing feature score for every variable
        result = dict(zip(pred_train.columns, model.feature_importances_))
        print_dict(dict_to_table(result))
        # check if the model is successful if we try different number of trees
        number_of_trees = 25
        trees = range(number_of_trees + 1)
        accuracy = np.zeros(number_of_trees + 1)
        for i in trees:
            classifier = RandomForestClassifier(n_estimators=i + 1, random_state=123)
            classifier = classifier.fit(pred_train, tar_train)
            predictions = classifier.predict(pred_test)
            accuracy[i] = sklearn.metrics.accuracy_score(tar_test, predictions)
        plt.cla()
        plt.plot(trees, accuracy)  # making the plot with the result
        plt.show()


def machine_learning_general(data_sub_set, targets, predictors, categorical):
    print("=============Machine Learning tools==============================================")
    data_sub_set = retrieve_clean_data(data_sub_set, targets + predictors + categorical)  # dropping values

    # recoding categorical variable by one hot encoding principles
    cat_predictors = recode_categorical_variables(data_sub_set, categorical)

    for target in targets:
        # splitting on test and training
        pred_train, pred_test, tar_train, tar_test = train_test_split(cat_predictors,
                                                                      data_sub_set[target],
                                                                      test_size=.3)
        print(f"The size of the training set is {pred_train.shape[0]}")
        print(f"The size of the test set is {pred_test.shape[0]}")
        decision_tree(pred_train, pred_test, tar_train, tar_test, random_forest=True)
        decision_tree(pred_train, pred_test, tar_train, tar_test)


if __name__ == "__main__":
    # taking variables which are appropriate for machine learning
    target_variables = retrieve_cat_response_variables()
    quantitative_predictors = retrieve_quantitative_explanatory_vars()
    categorical_predictors = retrieve_cat_explanatory_vars()

    # for machine learning tools we work only with the "property_damaged" variable because it is binary
    data = primary_data_management(quantitative_predictors + categorical_predictors, target_variables)

    # performing the machine learning
    machine_learning_general(data, target_variables, quantitative_predictors, categorical_predictors)
