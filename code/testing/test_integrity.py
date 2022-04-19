import pandas as pd
import numpy as np


# helper functions
def create_list(core_list, core_freq, series_len):
    '''
    To create a test dataframe, you want to fill out each column with something reasonable. This function
    creates the data for a column.
    Given a list of possible values, and a list of integers of their frequencies,
    repeat the values with the frequencies into one long list.
    For example, if core list is ["A", "B", "C"] and core_freq is [3, 2, 1], and series_len=11 you will get
    ["A", "A", "A", "B", "B", "C", "A", "A", "A", "B", "B"]
    If your series len is long compared to your repeat cycle, and your different lists for different columns are
    incommensurate, then this will give you a good mix but one which is not stochastic -- good for testing.
    :param core_list: List of unique values
    :param core_freq: List of integers, one for each value, of how many times that one will be repeated
    :param series_len: Size of the data frame you are trying to fill out
    :return: list suitable for being popped into the dataframe
    '''
    elements = []
    for idx in range(len(core_freq)):
        elements.extend([core_list[idx] for x in range(core_freq[idx])])
    reps = int(np.ceil(series_len / len(core_list)))
    result = [elem for sub_list in (elements for x in range(reps)) for elem in sub_list]
    result = result[0:series_len]

    return result


def create_compliant_df(start_date, end_date):
    drange = pd.date_range(start_date, end_date, freq="17min")
    stop_id = [x for x in range(len(drange))]
    mydict = {"date_time": drange, "stop_id": stop_id}
    df = pd.DataFrame(mydict)
    races = ['White', 'Hispanic/Latino/a', 'Asian', 'Middle Eastern or South Asian',
             'Black/African American', 'Pacific Islander', 'Native American']
    races_freq = [593, 330, 241, 177, 56, 23, 5]
    mydict["race"] = create_list(races, races_freq, len(df))
    mydict["age"] = create_list(17 + np.arange(60), np.ones(60, dtype=int), len(df))
    mydict["gender"] = create_list(["male", "female", "nonbinary", "decline"], [5, 5, 2, 1], len(df))
    action_list = ['No Action', 'Curbside detention', 'Handcuffed or flex cuffed',
                   'Asked for consent to search property',
                   'Person removed from vehicle by order', 'Field sobriety test conducted',
                   'Search of person was conducted', 'Asked for consent to search person',
                   'Property was seized', 'Patrol car detention']
    action_values = [1330, 28, 25, 17, 17, 3, 2, 1, 1, 1]
    mydict["actions_taken"] = create_list(action_list, action_values, len(df))
    search_list = ['No Search',
                   'Condition of parole / probation/ PRCS / mandatory supervision',
                   'Incident to arrest', 'Consent given',
                   'Officer Safety/safety of others', 'Evidence of crime',
                   'Odor of contraband']
    search_values = [1353, 26, 19, 13, 11, 2, 1]
    mydict["basis_for_search"] = create_list(search_list, search_values, len(df))
    mydict["call_for_service"] = create_list(['No', 'YES'], [467, 8], len(df))
    disabilities_list = ['None', 'Speech impairment or limited use of language',
                         'Mental health condition', 'Deafness or difficulty hearing',
                         'Other disability']
    disabilities_values = [459, 11, 3, 1, 1]
    mydict["disabilities"] = create_list(disabilities_list, disabilities_values, len(df))
    duration_list = [5, 8, 10, 3, 7, 4, 15, 12, 9, 2, 6, 11, 20,
                     13, 25, 30, 1, 14, 16, 45, 18, 60, 35, 40, 17, 180,
                     50, 26, 32, 24, 37, 70, 189, 19, 140, 134, 120, 90, 67,
                     38, 65, 22, 56, 28, 41, 380]
    duration_values = [329, 245, 238, 79, 64, 60, 58, 57, 54, 43, 40, 21, 19,
                       12, 11, 10, 10, 9, 8, 7, 6, 6, 6, 4, 3, 2,
                       2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 1]
    mydict["duration"] = create_list(duration_list, duration_values, len(df))
    evidence_list = ['None', 'Drug Paraphernalia', 'Suspected Stolen property',
                     'Other Contraband or evidence', 'Alcohol',
                     'Weapon(s) other than a firearm', 'Drugs/narcotics',
                     'Cell phone(s) or electronic device(s)']
    evidence_values = [1396, 12, 4, 4, 4, 3, 1, 1]
    mydict["evidence_found"] = create_list(evidence_list, evidence_values, len(df))
    mydict["lgbt"] = create_list(["No", "Yes"], [471, 4], len(df))
    mydict["limited_english"] = create_list(["No", "Yes"], [1316, 109], len(df))
    # location is a mess due to being a free field. Make up a prime number of locations
    location_list = ["Main St", "Oak St", "Truman", "Foothill", "Edith", "Second St", "Fremont",
                     "Roosevelt", "Toyon", "Black Mtn", "Magdalena"]
    location_values = [4, 3, 7, 2, 9, 5, 6, 5, 9, 1, 3]
    mydict["location"] = create_list(location_list, location_values, len(df))
    # property_seized is not in the los altos data
    property_list = ["None", "Firearms", "Drugs", "Vehicle", "Other"]
    property_values = [93, 2, 5, 1, 7]
    mydict["property_seized"] = create_list(property_list, property_values, len(df))
    reason_list = ['Traffic Violation', 'Reasonable Suspicion',
                   'Consensual Encounter resulting in a search',
                   'Investigation to determine whether the person was truant',
                   'Known to be on Parole / Probation / PRCS / Mandatory Supervision',
                   'Knowledge of outstanding arrest warrant/wanted person']
    reason_values = [1354, 50, 8, 8, 3, 2]
    mydict["reason_for_stop"] = create_list(reason_list, reason_values, len(df))
    result_list = ['Warning (verbal or written)', 'Citation for infraction', 'No Action',
                   'In-field cite and release', 'Custodial Arrest without warrant',
                   'Field interview card completed',
                   'Custodial Arrest pursuant to outstanding warrant', 'Psychiatric hold',
                   'Contacted parent/legal guardian or other person responsible for the minor',
                   'Noncriminal transport or caretaking transport']
    result_values = [662, 611, 80, 28, 19, 7, 6, 5, 4, 3]
    mydict["result"] = create_list(result_list, result_values, len(df))

    df = pd.DataFrame(mydict)
    return df
