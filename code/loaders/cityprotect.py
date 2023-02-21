import pandas as pd
from datetime import datetime
import glob
import re
from pandas.errors import EmptyDataError


def protect_read_csv(f):
	try:
		return pd.read_csv(f)
	except EmptyDataError as e:
		print("Data file {} is empty.".format(f))
	
		
def cityprotect(target_dir, end_date=datetime(year=2023, month=1, day=1)):
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

	return df
	

