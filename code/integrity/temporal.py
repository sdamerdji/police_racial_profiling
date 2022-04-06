# Checks that the temporal information in the df makes sense

import pandas as pd
import numpy as np

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'plotting'))
from plot_utils import PlotParams


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
