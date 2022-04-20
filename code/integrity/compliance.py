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
