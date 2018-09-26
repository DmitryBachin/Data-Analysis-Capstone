from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import sklearn.metrics as sklm
from variables import *
from data_menegement import primary_data_management
from sklearn.model_selection import train_test_split
import sklearn

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



def machine_learning_general(data_sub_set, targets, predictors):
    data_sub_set = retrieve_clean_data(data_sub_set, targets+predictors)
    for target in targets:
        pred_train, pred_test, tar_train, tar_test = train_test_split(data_sub_set[predictors],
                                                                               data_sub_set[target],
                                                                               test_size=.3)
        print(f"The size of the training set is: {pred_train.shape[0]}")
        print(f"The size of the test set is: {pred_test.shape[0]}")

        decision_tree(pred_train, pred_test, tar_train, tar_test)


if __name__ == "__main__":
    response = retrieve_response_variables()
    explanatory = retrieve_putative_predictors()
    data_set = primary_data_management(explanatory, response)
    machine_learning_general(data_set, response, explanatory)