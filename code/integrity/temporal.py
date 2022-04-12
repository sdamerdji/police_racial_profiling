# Checks that the temporal information in the df makes sense

import pandas as pd
import numpy as np

import sys, os
from colorama import Fore, Style

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'plotting'))
from plot_utils import PlotParams
import lare_matplot as lmp


# TODO:
# look for gaps
# look for bunching
# look for day-of-month trends
def quiet_checks(df):
    success = time_range(df)
    success = success and time_gaps(df)
    success = success and stops_by_day(df)
    success = success and weekday_trends(df)

    return success


def verbose_checks(df):
    success = True
    check, first_last = time_range(df)
    print("Sufficient time duration: {}".format(pretty_bool(check)))
    print("First stop: {}".format(first_last[0]))
    print("Last stop:  {}".format(first_last[1]))
    print("Duration of data set: {}".format(first_last[1] - first_last[0]))

    check, gaps = time_gaps(df)
    print("Check for unexpected data gaps: {}".format(pretty_bool(check)))
    if not check:
        print("Index:   Duration:")
        for idx in gaps.index:
            print("{}:  {},   {} to {}".format(idx, gaps[idx], df.shift(1).loc[idx].date_time, df.loc[idx].date_time))
        print()

    check, pparam, bad_days = stops_by_day(df)
    print("Check for excessive stop days: {}".format(pretty_bool(check)))
    if not check:
        lmp.basic_plot(pparam)
        print("{} days with excessive stops.".format(len(bad_days)))
        print(bad_days)
        print()

    check, pparam, bad_days = weekday_trends(df)
    print("Check for excessive weekday: {}".format(pretty_bool(check)))
    if not check:
        lmp.basic_plot(pparam)
        print("Weekdays with excessive stops: {}".format(bad_days))
        print()


def pretty_bool(check):
    if check:
        result = Fore.GREEN + Style.BRIGHT + "PASS" + Style.RESET_ALL
    else:
        result = Fore.RED + Style.BRIGHT + "FAIL" + Style.RESET_ALL
    return result


def time_range(df, threshold=pd.Timedelta('180 days')):
    first = min(df["date_time"])
    last = max(df["date_time"])
    success = (last - first) > threshold
    return success, [first, last]


def time_gaps(df, threshold=pd.Timedelta('24 hours')):
    gaps = df["date_time"].diff()
    long_gaps = gaps[gaps > threshold]
    if (len(long_gaps) > 0):
        success = False
    else:
        success = True
    return success, long_gaps


def weekday_trends(df, threshold=3):
    success = True
    bad_days = []
    weekdays = df["date_time"].apply(lambda x: x.day_name()).value_counts()
    avg = np.mean(weekdays)
    zscores = (weekdays - avg) / np.sqrt(avg)
    if any(np.abs(zscores) > threshold):
        # Anyone more than "threshold" sigma from the mean
        success = False
        bad_days = zscores.where(np.abs(zscores) > threshold).dropna().keys()
    plotparams = PlotParams()
    # make sure they are in the order we want
    plotparams.type = "bar"
    plotparams.xax = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plotparams.yax = [weekdays[d] for d in plotparams.xax]
    plotparams.title = "Stops by Day of Week"
    plotparams.xlabel = None
    plotparams.ylabel = "Stops"

    return success, plotparams, bad_days


def stops_by_day(df, threshold=3):
    success = True
    bad_days = []
    counts = df["date_time"].dt.floor("d").value_counts()
    avg = np.mean(counts)
    zscores = (counts - avg) / np.sqrt(avg)
    if any(np.abs(zscores) > threshold):
        # Anyone more than "threshold" sigma from the mean
        success = False
        bad_days_index = zscores.where(np.abs(zscores) > threshold).dropna().keys()
        bad_days = counts[bad_days_index]
    plotparams = PlotParams()
    # make sure they are in the order we want
    plotparams.type = "scatter"
    plotparams.yax = counts.tolist()
    plotparams.xax = counts.index.tolist()
    plotparams.title = "Stops by Day"
    plotparams.xlabel = None
    plotparams.ylabel = "Stops"

    return success, plotparams, bad_days
