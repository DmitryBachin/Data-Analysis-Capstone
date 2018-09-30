from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import pandas as pd

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
