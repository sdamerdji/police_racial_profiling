# Tests to show compliance with RIPA laws
import pandas as pd
from colorama import Fore, Style

# Required fields from https://www.ripalog.com/ripa/ripa-faq.htm
# and the official regulation: https://oag.ca.gov/sites/all/files/agweb/pdfs/ripa/stop-data-reg-final-text-110717.pdf?

required_fields = {'stop_id',
                   'age', 'race', 'gender',
                   'lgbt', 'disabilities', 'limited_english',
                   'date_time', 'duration', 'location',
                   'reason_for_stop', 'actions_taken', 'call_for_service',
                   'basis_for_search', 'evidence_found', 'property_seized',
                   'result'}


def quiet_checks(df):
    success = True
    check, _, _ = all_required_exist(df)
    success = success and check
    check, _ = unique_stops(df)
    success = success and check

    return success


def pretty_bool(check):
    if check:
        result = Fore.GREEN + Style.BRIGHT + "PASS" + Style.RESET_ALL
    else:
        result = Fore.RED + Style.BRIGHT + "FAIL" + Style.RESET_ALL
    return result


def verbose_checks(df):
    success = True
    check, missing, extra = all_required_exist(df)
    print("All required fields exist: {}".format(pretty_bool(check)))
    if not check:
        print("   Missing fields: {}".format(missing))
        print("   Extra fields:   {}".format(extra))
    success = success and check
    check, dups = unique_stops(df)
    print("All stops unique: {}".format(pretty_bool(check)))
    if not check:
        print("   Total records:   {}".format(len(df)))
        print("   Unique stop_ids: {}".format(len(df.drop_duplicates(subset="stop_id", inplace=False))))
        print("   Unique records:  {}".format(len(df.drop_duplicates(inplace=False))))
        print("   Duplicate stop_ids: {}".format(dups["stop_id"].values))
    success = success and check
    return success


def all_required_exist(df):
    '''
    Verify that all the required fields exist in the dataframe
    :param df: dataframe to check
    :return: success(bool), list of missing fields
    '''

    fields = set(df.keys())
    missing = required_fields.difference(fields)
    extra = fields.difference(required_fields)
    if missing:
        success = False
    else:
        success = True

    return success, missing, extra


def unique_stops(df):
    '''
    Make sure that stops are uniquely identified. This takes two forms:
    1. Are there duplicate rows in the dataframe?
    2. Are there duplicate stop_ids that have different data?

    :param df:
    :return: success(bool), stop_ids that are duplicated somehow
    '''

    dups = df[df.duplicated("stop_id")]
    if dups.empty:
        success = True
    else:
        success = False

    return success, dups


def count_individuals(single_stop_df, verbose=False):
    '''
    Given a dataframe that is a subset where all rows have a single stop_id,
    Estimate the number of individuals involved in the stop.

    First look at differences in demographic variables.
    Finally, use the information about the result. If one row has "No Action" and other rows have some action,
    then the No Action was probably a different person.
    '''
    demog_keys = ["age", "race", "gender", "limited_english", "lgbt", "disabilities"]
    stop_id = set(single_stop_df["stop_id"])
    if len(stop_id) == 1:
        stop_id = list(stop_id)[0]
    else:
        print("ERROR: single stop dataframe contains multiple stop_ids! {}".format(stop_id))
        assert (False)
    # get rid of exact duplicate rows.
    orig_records = len(single_stop_df)
    single_stop_df.drop_duplicates(inplace=True)
    uniq_records = len(single_stop_df)
    if (uniq_records < orig_records) and verbose:
        print("Data Issue: stop_id {} has {} identical records.".format(stop_id, orig_records - uniq_records + 1))
    if uniq_records == 1:
        return 1

    demog = single_stop_df.drop_duplicates(subset=demog_keys, inplace=False)
    demog_counts = demog.nunique()
    individuals = len(demog)
    diffs = demog_counts[demog_counts > 1].keys()
    if individuals > 1:
        if verbose:
            print("stop_id {}: Likely {} different individuals, differing by: {}".format(stop_id, individuals,
                                                                                         [d for d in diffs]))
    else:
        uniq_res = set(single_stop_df["result"].values)
        if len(uniq_res) > 1 and "No Action" in uniq_res:
            individuals = (single_stop_df["result"].value_counts())["No Action"] + 1
            if verbose:
                print("stop_id {}: Possibly {}+ individuals, based on different results".format(stop_id, individuals))
        else:
            if verbose:
                print("stop_id {}: Likely single individual with multiple actions.".format(stop_id))
    return individuals
