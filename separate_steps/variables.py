PUTATIVE_PREDICTORS = ['event_type', 'month_name', 'state']  # the first set of putative predictors
VARIABLES_TO_MODIFY = ["damage_property", "month_name"]


# the functions are written in case if the variables name will be needed to modify somehow

def retrieve_putative_predictors():
    return PUTATIVE_PREDICTORS[:]


def retrieve_variables_to_modify():
    return VARIABLES_TO_MODIFY[:]
