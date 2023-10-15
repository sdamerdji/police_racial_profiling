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
cities_in_scc = ["Alviso",
				"Campbell",
				"Coyote",
				"Cupertino",
				"Gilroy",
				"Holy City",
				"Los Altos",
				"Los Altos Hills",
				"Monte Sereno", 
				"Los Gatos",
				"Milpitas",
				"Morgan Hill",
				"Mount Hamilton",
				"Mountain View",
				"Palo Alto",
				"Redwood Estates",
				"San Jose",
				"San Martin",
				"Santa Clara",
				"Saratoga",
				"Stanford",
				"Sunnyvale"
]

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

		
def cityprotect(target_dir, start_date=datetime(year=2017, month=1, day=1),
						end_date=datetime(year=2023, month=1, day=1), 
						reclassify=True, prop_list=None, violent_list=None):
	print("Starting: {}".format(start_date))
	print("Ending:   {}".format(end_date))
	filelist = glob.glob("{}/*_report.csv".format(target_dir))
	print("Loading from {} files.".format(len(filelist)))
	df = pd.concat([protect_read_csv(f) for f in filelist], ignore_index=True)
	# Header rows are sometimes copied throughout the file.
	df = df[df.ne(df.columns).any(axis=1)]
	# Format the dates to datetimes
	df["date"] = pd.to_datetime(df["date"].str.upper(), format="%m/%d/%Y, %I:%M:%S %p")
	df["updateDate"] = pd.to_datetime(df["updateDate"].str.upper(), format="%m/%d/%Y, %I:%M:%S %p")
	# Los Altos has a bunch of weird stuff at the beginning of each incident
	df["incidentType"] = df["incidentType"].replace(regex=r".CAD\]", value="").str.strip()
	df["parentIncidentType"] = df["parentIncidentType"].str.strip()

	df = df[df["date"] < end_date]
	df = df[df["date"] >= start_date]
	df.sort_values(by=['date'], inplace=True)

	if reclassify:
		df = reclassify_incidents(df, prop_list=prop_list, violent_list=violent_list)


	return df
	
def attempt_nom(nom, blocksizedAddr):
    place = re.sub("BLOCK", "", blocksizedAddr.upper()) + ", SANTA CLARA COUNTY, CA"
    try:
        location = nom.geocode(place)
        print("Nom: {}".format(location.raw["display_name"]))
        display_name = [s.strip() for s in location.raw["display_name"].split(",")]                         
        try:
            county_idx = display_name.index("Santa Clara County")
        except ValueError:
            print("SCC not found: {}".format(display_name))
            return None
        city = display_name[county_idx-1]
        postcode = display_name[-2]
        return city, postcode
    except:
        return None
        
def attempt_goog(goog, blocksizedAddr):
    place = re.sub("BLOCK", "", blocksizedAddr.upper()) + ", SANTA CLARA COUNTY, CA"
    try:
        location = goog.geocode(place)
        city = location.address.split(",")[1].strip()
        postcode = re.sub("[A-Z]*", "", location.address.split(",")[2]).strip()
        return city, postcode
    except:
        return None
    
def geocode(row, nom, goog):
	blockaddr = row["blocksizedAddress"]
	loc_tuple = attempt_nom(nom, blockaddr)
	if not loc_tuple or loc_tuple[0] not in cities_in_scc:
		loc_tuple = attempt_goog(goog, blockaddr)
		if loc_tuple:
			print("Google successful on {}".format(blockaddr))
		else:
			return None, None
	else:
		print("Nominatim successful on {}".format(blockaddr))

	if loc_tuple[1]:
		postcode = int(loc_tuple[1])
	else:
		postcode = None

	return loc_tuple[0], postcode

def infer_cities(df, nom, goog, max=300):
	counter = 0
	for index, row in df[df["inferredCity"] == "unknown"].iterrows():
		location_tuple = geocode(row, nom, goog)
			
		counter = counter + 1
		df.at[index, "inferredCity"] = location_tuple[0]
		df.at[index, "postcode"] = location_tuple[1]
		print("\n{}: {} {}- {}, {}".format(counter, df.at[index, "date"], row["blocksizedAddress"], df.at[index,"inferredCity"], df.at[index, "postalCode"]))
		if counter/200 == round(counter/200):
			print("Saving...")
			df.to_pickle("SCCSheriff.pkl")
		if counter > max:
			break

