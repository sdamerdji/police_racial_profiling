import pandas as pd
import os


def load_ripa_data(file_list, dir="../../data/clean_data", verbose=False):
    # Load CSVs in the format that MV provided, based on Xuesong Wang's format in LA 9/2023

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
         
        # Make the times into datetime objects
        df["stopTime"] = pd.to_datetime(df["SDate"] + "-" + df["STime"], format="%m/%d/%Y-%H:%M")

        std_cols = {"LEARecordID": "stop_id",
                    "stopTime": "date_time",
                    "SDur": "duration",
                    "Is_ServCall": "call_for_service",
                    "Loc": "location",
                    "Act_CD": "actions_taken",
                    "personSearchConsentGiven": "person_search_consent",
                    "propertySearchConsentGiven": "property_search_consent",
                    "Ethn": "race",
                    "StReas": "reason_for_stop",
                    "StReas_Given": "reason_given_for_stop",
                    "Disb": "disabilities",
                    "Is_LimEng": "limited_english",
                    "Age": "age",
                    "Gend": "gender",
                    "LGBT": "lgbt",
                    "GendNC": "gender_nonconforming",
                    "ResCD": "result",
                    "BasSearch_N": "basis_for_search",
                    "Cb": "evidence_found"
        }
        df.rename(columns=std_cols, inplace="True")

        df_list.append(df)

 
    return df_list
