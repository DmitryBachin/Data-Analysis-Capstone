PUTATIVE_PREDICTORS = ['event_type', 'month_num', 'state']  # the first set of putative predictors


def variable_names_to_uppercase(used_variables):
    # the variables in the code book are written in lowercase, but actually they are in uppper
    # so need a little conversion
    return list(map(str.upper, used_variables))


def retrieve_putative_predictors():
    return variable_names_to_uppercase(PUTATIVE_PREDICTORS[:])
