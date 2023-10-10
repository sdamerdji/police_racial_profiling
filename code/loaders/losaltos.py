import pandas as pd
import os

def load_ripa_data(file_list, dir="../../data/clean_data", verbose=False):
    # Load CSVs in the format that Xuesong Wang used up to at least 8/28/2023
    df_list = read_csv_list(file_list, dir)

    if verbose:
        for df in df_list:
            print("Records: {} Stop IDs: [{}, {}]  Date Range: [{}, {}]".format(len(df), df["stop_id"].min(), df["stop_id"].max(),
                                                                    df["date_time"].min(), df["date_time"].max()))
    final_df = pd.concat(df_list, axis=0)
    final_df = final_df.drop_duplicates(subset="stop_id", keep="last")
    return final_df

def read_csv_list(file_list, dir):
    # Core CSV reader, returning a list of dataframes, one per file
    df_list = []
    for file in file_list:
        df=pd.read_csv(os.path.join(dir, file), 
                                   encoding = 'utf-8-sig',
                                   #encoding = 'unicode_escape', 
                                   engine ='python',
                                   skipinitialspace=True,
                                   encoding_errors="replace")
        # There is a typo in one of the column names we need to fix
        if "reaultOfStop" in df.columns:
            df.rename(columns={"reaultOfStop":"resultOfStop"}, inplace=True)
        
        # Make the times into datetime objects
        df["stopTime"] = pd.to_datetime(df["stopTime"], format="%m/%d/%Y %H:%M")
        df["entryUpdateTime"] = pd.to_datetime(df["stopTime"], format="%m/%d/%Y %H:%M")
        std_cols = {"stopID": "stop_id",
            "stopTime": "date_time",
            "stopDuration": "duration",
            "stopInResponseToCFS": "call_for_service",
           "street": "location",
           "actionTakens": "actions_taken",
           "personSearchConsentGiven": "person_search_consent",
           "propertySearchConsentGiven": "property_search_consent",
           "perceivedRace": "race",
           "reasonForStop": "reason_for_stop",
           "perceivedOrKnownDisability": "disabilities",
            "perceivedLimitedEnglish": "limited_english",
            "perceivedAge": "age",
            "perceivedGender": "gender",
            "perceivedLgbt": "lgbt",
            "genderNonConforming": "gender_nonconforming",
            "resultOfStop": "result",
            "basisForSearch": "basis_for_search",
            "contrabandOrEvidenceDiscovered": "evidence_found"
        }
        df.rename(columns=std_cols, inplace="True")

        df_list.append(df)

 
    return df_list


