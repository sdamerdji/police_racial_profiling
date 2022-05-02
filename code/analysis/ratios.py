import pandas as pd
import numpy as np


def add_races(data, races_to_add, field='result'):
    '''
    Generate value_counts() summed for all the races in the list
    :param data: Full RIPA dataframe. No uniqueness is handled here.
    :param races_to_add: list of races to include, that match format
    :param field: optional; the column of the original DF to count values in.
    :return: Series of value_counts
    '''
    res = pd.Series(0, data[field].value_counts().keys())
    for race in races_to_add:
        res = res.add(data[field][data['race'] == race].value_counts(), fill_value=0)
    return res


def generate_relative_df(baseline, comparison, base_race, comparison_race):
    '''
    Generate a dataframe comparing a set of value_counts against baseline.
    Typically, one would use the "White" counts, or total counts, as baseline, and look for differences.
    The resulting dataframe shows how often the various outcomes would be expected, if they occurred for the
    comparison races at the same frequency as the baseline race.
    :param baseline: Series of value_counts for the baseline race
    :param comparison: Series of value_counts for the comparison race(s). If races are being summed,
    they should be summed using add_races() first.
    :param base_race: String identifying the baseline race
    :param comparison_race: String identifying the comparison race
    :return: A dataframe with the following columns:
    * The actual value counts for the baseline race
    * The actual value counts for the comparison race
    * The expected value counts for the comparison race, if the proportions were the same as baseline
    * The relative rate for that outcome, comparison vs. baseline
    '''
    temp_dict = {base_race: baseline, comparison_race: comparison}
    scaled_baseline = sum(comparison) * (baseline / sum(baseline))
    relative = (comparison / baseline) * (sum(baseline) / sum(comparison))
    temp_dict["Expected {}".format(comparison_race)] = scaled_baseline
    temp_dict["Relative"] = relative
    return pd.DataFrame(temp_dict)
