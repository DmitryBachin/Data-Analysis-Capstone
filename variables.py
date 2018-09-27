# PUTATIVE_PREDICTORS = ["event_type", "month_name_num", "state"]  # the first set of putative predictors
PUTATIVE_PREDICTORS = ["cz_type_num"]  # the first set of putative predictors
VARIABLES_TO_MODIFY = ["damage_property", "month_name_num", "short_event", "damage_property_lg", "cz_type_num"]
RESPONSE_VARIABLES = ["damage_property_lg"]
NON_BINARY_CATEGORICAL_PREDICTORS = ["month_name_num", "state_fips"]


# the functions are written in case if the variables name will be needed to modify somehow

def retrieve_predictors():
    return PUTATIVE_PREDICTORS[:]


def retrieve_non_binary_cat_predictors():
    return NON_BINARY_CATEGORICAL_PREDICTORS[:]


def retrieve_variables_to_modify():
    return VARIABLES_TO_MODIFY[:]


def retrieve_response_variables():
    return RESPONSE_VARIABLES[:]
