import pandas as pd
from datetime import datetime
import glob
import re
from pandas.errors import EmptyDataError

reclassification_dir = {"Theft": ["theft", "burglary", "larceny"],
                        "Property Crime": ["property crime", "vandalism"],
                        "Assault": ["assault"],
                        "Robbery": ["robbery"],
                        "Homicide": ["homicide", "murder"],
                        "Sexual Offense": ["sexual assault", "rape"],
                        "Other Violent Offense": ["shooting", "shots fired", "car jacking",
                                                  "carjacking", "kidnapping"]
                        }


def protect_read_csv(f):
	try:
		return pd.read_csv(f)
	except EmptyDataError as e:
		print("Data file {} is empty.".format(f))

def reclassify_incidents(df, prop_list=None, violent_list=None):
	'''
	Many times incidents will be miscategorized into the wrong parentIncidentType.
	This tries to fix them up.
	'''
	if prop_list == None:
		prop_list = ["Breaking & Entering", "Property Crime", "Theft of Vehicle",
                                    "Theft from Vehicle", "Theft"]
	if violent_list == None:
		violent_list = ["Assault", "Robbery", "Sexual Offense", "Homicide",
                                       "Rape", "Other Violent Offense"]
	unaccounted_parents = set(
		df["parentIncidentType"]) - set(prop_list) - set(violent_list)
	for parent, words in reclassification_dir.items():
		for word in words:
			df.loc[df["parentIncidentType"].isin(unaccounted_parents) &
			       df["incidentType"].str.contains(word, case=False), "parentIncidentType"] = parent
	return df

		
def cityprotect(target_dir, end_date=datetime(year=2023, month=1, day=1), reclassify=True, prop_list=None, violent_list=None):
	filelist = glob.glob("{}/*_report.csv".format(target_dir))
	print("Loading from {} files.".format(len(filelist)))
	df = pd.concat([protect_read_csv(f) for f in filelist], ignore_index=True)
	# Header rows are sometimes copied throughout the file.
	df = df[df.ne(df.columns).any(1)]
	# Format the dates to datetimes
	df["date"] = pd.to_datetime(df["date"].str.upper(), format="%m/%d/%Y, %I:%M:%S %p")
	df["updateDate"] = pd.to_datetime(df["updateDate"].str.upper(), format="%m/%d/%Y, %I:%M:%S %p")
	# Los Altos has a bunch of weird stuff at the beginning of each incident
	df["incidentType"] = df["incidentType"].replace(regex=r".CAD\]", value="").str.strip()
	df["parentIncidentType"] = df["parentIncidentType"].str.strip()

	df = df[df["date"] < end_date]
	df.sort_values(by=['date'], inplace=True)

	if reclassify:
		df = reclassify_incidents(df, prop_list=prop_list, violent_list=violent_list)


	return df
	

