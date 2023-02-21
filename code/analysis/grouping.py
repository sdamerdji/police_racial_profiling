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


