PUTATIVE_PREDICTORS = []  # the first set of putative predictors
VARIABLES_TO_MODIFY = ["damage_property", "month_name", "short_event", "damage_property_lg", "climate_region",
                       "damage_crops"]
RESPONSE_VARIABLES = ["damage_property_lg", "injuries_direct", "injuries_indirect", "deaths_direct", "deaths_indirect",
                      "damage_crops"]
NON_BINARY_CATEGORICAL_PREDICTORS = ["month_name", "climate_region"]


# the functions are written in case if the variables name will be needed to modify somehow

def retrieve_predictors():
    return PUTATIVE_PREDICTORS[:]


def retrieve_non_binary_cat_predictors():
    return NON_BINARY_CATEGORICAL_PREDICTORS[:]


def retrieve_variables_to_modify():
    return VARIABLES_TO_MODIFY[:]


def retrieve_response_variables():
    return RESPONSE_VARIABLES[:]


regions = {'Central': ['Illinois',
                       'Indiana',
                       'Kentucky',
                       'Missouri',
                       'Ohio',
                       'Tennessee',
                       'West Virginia'],
           'Upper_Midwest/East North Central': ['Iowa', 'Michigan', 'Minnesota', 'Wisconsin', 'Alaska'],
           'Northeast': ['Connecticut',
                         'Delaware',
                         'Maine',
                         'Maryland',
                         'Massachusetts',
                         'New Hampshire',
                         'New Jersey',
                         'New York',
                         'Pennsylvania',
                         'Rhode Island',
                         'Vermont'],
           'Northwest': ['Idaho', 'Oregon', 'Washington'],
           'South': ['South',
                     'Arkansas',
                     'Kansas',
                     'Louisiana',
                     'Mississippi',
                     'Oklahoma',
                     'Texas'],
           'Southeast': ['Alabama',
                         'Florida',
                         'Georgia',
                         'North_Carolina',
                         'South_Carolina',
                         'Virginia'],
           'Southwest': ['Arizona', 'Colorado', 'New Mexico', 'Utah'],
           'West': ["California", "Nevada"],
           'Northern Rockies and Plains/West_North_Central': ['Montana', 'Nebraska', 'North Dakota', 'South Dakota',
                                                              'Wyoming'],
           'Other': []}
