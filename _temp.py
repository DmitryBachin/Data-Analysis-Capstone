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
from itertools import combinations, permutations
from tabulate import tabulate
import seaborn

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
data = pd.read_csv('data_related/_test.csv', low_memory=False)

from sklearn import tree
from sklearn.datasets import load_iris
import os
import pprint

os.environ["PATH"] += os.pathsep + 'C:\\Program Files (x86)\\Graphviz2.38\\bin'

def post_hoc_anova_to_dict(df):
    comparison_dict = {}
    for i in range(len(df)):
        print(df["group1"][i])
        print(df["group2"][i])
        print(df["meandiff"][i])
        comparison_dict[df["group1"][i], df["group2"][i]] = df["meandiff"][i]
    return comparison_dict


p = pprint.PrettyPrinter(indent=4).pprint
p(post_hoc_anova_to_dict(data))
