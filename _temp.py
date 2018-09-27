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




pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

data = pd.read_csv('data_related/_test.csv', low_memory=False)

new_data, new_cat_var = recode_categoricals(data, ["MONTH"])
print(new_cat_var)
print(new_data)