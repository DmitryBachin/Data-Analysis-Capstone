from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import pandas as pd
import operator
from tabulate import tabulate


def label_encoding(data_set, variable):  # returns the recoding dictionary
    # doesn't return the array to avoid complication
    le = LabelEncoder()
    le.fit(data_set[variable])
    return {str_value: num_value for num_value, str_value in enumerate(le.classes_)}


def one_hot_encoding(data_set, variable):
    # recode every category as binary variable
    value_map = label_encoding(data_set[[variable]], variable)
    x_0 = data_set[[variable]]
    x_0[variable] = x_0[variable].map(value_map)
    enc = OneHotEncoder()
    enc.fit(x_0)
    x_one_hot = enc.transform(x_0).toarray()

    names = ["%s_%s" % (variable, i) for i in value_map]

    df = pd.DataFrame(x_one_hot, columns=names)
    return df


def recode_categorical_variables(data_set, variables):
    # use one hot encoding to adapt data to machine learning tools
    data_to_modify = data_set[variables].copy()
    vectors = [one_hot_encoding(data_to_modify, variable) for variable in data_to_modify.columns.values]
    modified_data = pd.concat(vectors, axis=1)
    return modified_data


def dict_to_table(result_dict):
    return tabulate(sorted(result_dict.items(), key=operator.itemgetter(1), reverse=True))


def parse_feature_importance_table(table):
    replace_map = [
        ("'", ""),
        ("\n\n ", "\n"),
        ("  ", "*"),
        ("* ", "*"),
        ("event_", "event "),
        ("climate_", "climate "),
        ("West_North_Central", "West North Central"),
        ("Upper_Midwest", "Upper Midwest"),
        ("_lg", " lg"),
        ("_", ": ")
    ]
    for old, new in replace_map:
        table = table.replace(old, new)

    while "**" in table:
        table = table.replace("**", "*")

    return table
