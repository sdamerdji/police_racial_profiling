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
				 "Alum Rock",
				"Campbell",
				"Coyote",
				"Cupertino",
				"Gilroy",
				"Holy City",
				"Hollister",
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
				"Rucker",
				"San Jose",
				"San Martin",
				"Santa Clara",
				"Saratoga",
				"Stanford",
				"Sunnyvale",
				"Willow Glen"
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
	# before calling this, you'll need to do something like this
	#         nom = Nominatim(user_agent="policedata", scheme='http')
	# Then pass in 'nom' as the first argument.

	place = re.sub("BLOCK", "", blocksizedAddr.upper()) + ", SANTA CLARA COUNTY, CA"
	try:
		location = nom.geocode(place)
	except:
		print("Nom: failed")
		return None
	if location:
		display_name = [s.strip() for s in location.raw["display_name"].split(",")]                         
		try:
			county_idx = display_name.index("Santa Clara County")
		except ValueError:
			print("Nom: SCC key not found: {}".format(display_name))
			return None
		print("Nom: {}".format(location.raw["display_name"]))
		city = display_name[county_idx-1]
		postcode = display_name[-2]
		if city in cities_in_scc:
			return city, postcode
		else:
			print("Nom: {} not a city in Santa Clara County".format(city))
			return None	
	else:
		print("Nom returned None.")
		return None

        
def attempt_goog(goog, blocksizedAddr):
	# before calling this, you'll need to do something like this, with your own API key
	#        goog = GoogleV3(api_key=api_key)
	# Then pass 'goog' as the first argument.

	place = re.sub("BLOCK", "", blocksizedAddr.upper()) + ", SANTA CLARA COUNTY, CA"
	try:
		location = goog.geocode(place)
	except:
		print("Google failed.")
		return None
	city = location.address.split(",")[1].strip()
	postcode = re.sub("[A-Z]*", "", location.address.split(",")[2]).strip()
	if city in cities_in_scc:
		return city, postcode
	else:
		print("Goog: {} not a city in Santa Clara County".format(city))
		return None
    

def infer_cities(df, nom, goog):
    # Infer the cities from the block addresses
    # For nom and goog see attempt_nom and attempt_goog

    googcount = 0
	# Some blocksizedAddress fields are NaNs, which is Not Helpful
    df.loc[df["blocksizedAddress"].apply(lambda x: type(x) == float), "inferredCity"] = "blank"

	# We will iterate over unique addresses, not records.
    unique_addresses = df[df["inferredCity"] == "unknown"]["blocksizedAddress"].unique()

    for idx, addr in enumerate(unique_addresses):
        print("{}: {}: {} instances".format(idx, addr, len(df[df["blocksizedAddress"] == addr])))
        result = attempt_nom(nom, addr)
        if not result:
            result = attempt_goog(goog, addr)
            googcount += 1

        if result:  # fix all the records at once
            df.loc[df["blocksizedAddress"] == addr, "inferredCity"] = result[0]
            df.loc[df["blocksizedAddress"] == addr, "postcode"] = result[1]
        else:
            print("Failed to identify {}".format(addr))   

        if idx%200 == 0:
            print("Saving...")
            print("Google API count: {}".format(googcount))
            df.to_pickle("SCCSheriff.pkl") 

    print("Made {} calls to the Google API.")
    return df                                       