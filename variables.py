CRITICAL_VALUE = 0.05

RESPONSE_CATEGORICAL_VARIABLES = [
    "property_damaged"  # whether property was damaged or not
]
RESPONSE_QUATITATIVE_VARIABLES = [
    "damage_property_lg"  # logarithm of the damage property caused by the weather event amount (base 10)
]
VARIABLES_TO_MODIFY = [
    "damage_property",  # the amount of damage property; modified to integers from 30K, 2M, 1B
    "month_name",  # the month when the event took place; modified to the name with numeric prefix ("01_January")
    "event_duration",  # the duration of the event in hours; created from begin and end time of the event
    "damage_property_lg",  # logarithm of the damage property caused by the weather event amount (base 10)
    "climate_region",  # arranging states by climate region; Alaska is separated from others, DC added to Northeast
    "property_damaged",  # categorical; 0 if damage_property is 0, 1 if bigger than 0, nan if nan
    "event_duration_lg"  # logarithm of the event duration with base 10
]

QUANTITATIVE_EXPLANATORY_VARIABLES = [
    "event_duration_lg"  # logarithm of the event duration with base 10
]

CATEGORICAL_EXPLANATORY_VARIABLES = [
    "month_name",
    "climate_region",
    "cz_type",
    "event_type"
]


# the functions are written in case if the variables name will be needed to modify somehow

def retrieve_quantitative_explanatory_vars():
    return QUANTITATIVE_EXPLANATORY_VARIABLES[:]


def retrieve_cat_explanatory_vars():
    return CATEGORICAL_EXPLANATORY_VARIABLES[:]


def retrieve_variables_to_modify():
    return VARIABLES_TO_MODIFY[:]


def retrieve_cat_response_variables():
    return RESPONSE_CATEGORICAL_VARIABLES[:]


def retrieve_q_response_variables():
    return RESPONSE_QUATITATIVE_VARIABLES[:]
