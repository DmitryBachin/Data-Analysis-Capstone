RESPONSE_VARIABLES_CAT = ["property_damaged"]
RESPONSE_VARIABLES_Q = ["damage_property_lg"]

VARIABLES_TO_MODIFY = ["damage_property", "month_name", "event_duration", "damage_property_lg", "climate_region",
                       "property_damaged"]

QUANTATIVE_PREDICTORS = ["event_duration_lg"]  # the first set of putative predictors
MACHINE_LEARNING_TARGETS = []
BINARY_CATEGORICAL_PREDICTORS = []
NON_BINARY_CATEGORICAL_PREDICTORS = ["month_name", "climate_region", "cz_type", "event_type"]


# the functions are written in case if the variables name will be needed to modify somehow

def retrieve_quantitative_predictors():
    return QUANTATIVE_PREDICTORS[:]


def retrieve_non_binary_cat_predictors():
    return NON_BINARY_CATEGORICAL_PREDICTORS[:]


def retrieve_binary_cat_predictors():
    return BINARY_CATEGORICAL_PREDICTORS[:]


def retrieve_variables_to_modify():
    return VARIABLES_TO_MODIFY[:]


def retrieve_cat_response_variables():
    return RESPONSE_VARIABLES_CAT[:]


def retrieve_q_response_variables():
    return RESPONSE_VARIABLES_Q[:]


def retrieve_machine_targets():
    return MACHINE_LEARNING_TARGETS[:]
