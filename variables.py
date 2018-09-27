PUTATIVE_PREDICTORS = []  # the first set of putative predictors
VARIABLES_TO_MODIFY = ["damage_property", "month_name", "short_event", "damage_property_lg", "damage_property_cat"]
RESPONSE_VARIABLES = ["damage_property_cat"]
NON_BINARY_CATEGORICAL_PREDICTORS = ["month_name", "state"]


# the functions are written in case if the variables name will be needed to modify somehow

def retrieve_predictors():
    return PUTATIVE_PREDICTORS[:]


def retrieve_non_binary_cat_predictors():
    return NON_BINARY_CATEGORICAL_PREDICTORS[:]


def retrieve_variables_to_modify():
    return VARIABLES_TO_MODIFY[:]


def retrieve_response_variables():
    return RESPONSE_VARIABLES[:]
