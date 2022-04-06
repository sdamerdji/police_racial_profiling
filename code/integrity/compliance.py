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
    success = success and all_required_exist(df)

    return success


def verbose_checks(df):
    success = True
    check, missing, extra = all_required_exist(df)
    if check:
        result = Fore.GREEN + Style.BRIGHT + "TRUE" + Style.RESET_ALL
    else:
        result = Fore.RED + Style.BRIGHT + "FALSE" + Style.RESET_ALL
    print("All required fields exist: {}".format(result))
    if not check:
        print("   Missing fields: {}".format(missing))
        print("   Extra fields:   {}".format(extra))


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
