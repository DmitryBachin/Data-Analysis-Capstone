from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from variables import *
from data_menegement import primary_data_management
from sklearn.model_selection import train_test_split
import sklearn
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


def label_encoding(data_set, variable):  # returns the recoding dictionary
    # doesn't return the array to avoid complication
    le = LabelEncoder()
    le.fit(data_set[variable])
    return {str_value: num_value for num_value, str_value in enumerate(le.classes_)}


def one_hot_encoding(data_set, variable):
    value_map = label_encoding(data_set[[variable]], variable)
    x_0 = data_set[[variable]]
    x_0[variable] = x_0[variable].map(value_map)
    enc = OneHotEncoder()
    enc.fit(x_0)
    x_one_hot = enc.transform(x_0).toarray()

    names = ["%s_%s" % (variable, i) for i in value_map]

    df = pd.DataFrame(x_one_hot, columns=names)
    return df


def recode_categoricals(data_set, variables):
    data_to_modify = data_set[variables].copy()
    vectors = [one_hot_encoding(data_to_modify, variable) for variable in data_to_modify.columns.values]
    modified_data = pd.concat(vectors + [data_set.copy()], axis=1)
    return modified_data, modified_data.columns.values


def retrieve_clean_data(uncleaned_data, variables=None):
    if variables:
        for variable in variables:
            uncleaned_data.dropna(subset=[variable], inplace=True)
        return uncleaned_data
    else:
        return uncleaned_data.dropna()


def decision_tree(pred_train, pred_test, tar_train, tar_test):
    classifier = DecisionTreeClassifier()
    classifier = classifier.fit(pred_train, tar_train)
    predictions = classifier.predict(pred_test)
    result = sklearn.metrics.confusion_matrix(tar_test, predictions)
    print(result)


def machine_learning_general(data_sub_set, targets, predictors, categorical):
    data_sub_set = retrieve_clean_data(data_sub_set, targets + predictors + categorical)  # dropping values

    for target in targets:
        pred_train, pred_test, tar_train, tar_test = train_test_split(data_sub_set[predictors + categorical],
                                                                      data_sub_set[target],
                                                                      test_size=.3)


if __name__ == "__main__":
    response = retrieve_response_variables()
    explanatory = retrieve_predictors()
    non_binary_categorical = retrieve_non_binary_cat_predictors()
    data = primary_data_management(explanatory + non_binary_categorical, response)
    machine_learning_general(data, response, explanatory, non_binary_categorical)
