import pandas as pd

def time_bin_cityprotect_incident_types(df, freq="M"):
    '''
    Given a dataframe of the cityprotect variety, return a df of incident counts with 
    columns as parentIncidentTypes, and rows for frequency (default months)
    '''

    parentIncident_types = set([a.strip() for b in df['parentIncidentType'].str.split(';').values
                                for a in b])
    monthly = {k: df[df["parentIncidentType"] == k].groupby(
        pd.Grouper(key="date", freq=freq)) for k in parentIncident_types}
    monthly_df = pd.DataFrame(
        {k: monthly[k].count()["ccn"] for k in parentIncident_types}).fillna(0)

    return monthly_df

def time_bin_df(df, group_col, time_col, freq="M"):
    group_set = {k for k in df[group_col]}
    generators = {k: df[df[group_col] == k].groupby(
        pd.Grouper(key=time_col, freq=freq)) for k in group_set}
    binned_df = pd.DataFrame({k: generators[k].count()[group_col] for k in group_set}).fillna(0)

    return binned_df

def simplify_race(race):
    if race.lower() in ["white", "asian", "black", "hispanic", "other"]:
        return race
    elif "black" in race.lower():
        return "Black"
    elif "hispanic" in race.lower():
        return "Hispanic"
    elif "asian" in race.lower():
        return "Asian"
    else:
        return "Other"

def simplify_outcome(outcome):
    if outcome == "No Action":
        return "No Action"
    elif "warning" in outcome.lower():
        return "Warning"
    elif ("citation" in outcome.lower()) or ("cite" in outcome.lower()):
        return "Citation"
    elif "arrest" in outcome.lower():
        return "Arrest"
    else:
        return "Other"

def simplify_reason(reason):
    if reason == "Traffic Violation":
        return reason
    elif ("suspicion" in reason.lower()) or "warrant" in reason.lower() or "parole" in reason.lower():
        return "Possible Crime"
    else:
        return "Other" 


def simplify_age(age):
    if age < 18:
        return "Under 18"
    elif age < 30:
        return "18-29"
    elif age < 50:
        return "30-49"
    elif age < 70:
        return "50-69"
    else:
        return "70+"