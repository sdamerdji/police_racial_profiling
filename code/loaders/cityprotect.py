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

zipcode_lookup = {95035: 'Milpitas', 95123: 'San Jose', 95020: 'Gilroy', 95014: 'Cupertino', 95051: 'Santa Clara', 95111: 'San Jose', 94087: 'Sunnyvale', 95112: 'San Jose', 95125: 'San Jose', 95122: 'San Jose', 95116: 'San Jose', 95124: 'San Jose', 95136: 'San Jose', 94086: 'Sunnyvale', 95148: 'San Jose', 95008: 'Campbell', 94303: 'Palo Alto', 95050: 'Santa Clara', 95132: 'San Jose', 95120: 'San Jose', 95129: 'San Jose', 94040: 'Mountain View', 95121: 'San Jose', 95126: 'San Jose', 95118: 'San Jose', 95131: 'San Jose', 95070: 'Saratoga', 94043: 'Mountain View', 95134: 'San Jose', 95117: 'San Jose', 95133: 'San Jose', 94306: 'Palo Alto', 94089: 'Sunnyvale', 95054: 'Santa Clara', 94085: 'Sunnyvale', 94024: 'Los Altos', 95135: 'San Jose', 95110: 'San Jose', 94022: 'Los Altos', 94301: 'Palo Alto', 94041: 'Mountain View', 95030: 'Los Gatos', 95130: 'Campbell', 95119: 'San Jose', 95139: 'San Jose', 95046: 'San Martin', 95113: 'San Jose', 94308: 'Santa Clara', 95053: 'Santa Clara', 95002: 'San Jose', 95015: 'Santa Clara', 95031: 'San Jose', 95038: 'Morgan Hill', 95159: 'Santa Clara', 95192: 'San Jose', 95056: 'Santa Clara', 95109: 'Santa Clara', 95150: 'Santa Clara', 94039: 'Mountain View'}

communities_dict = {
  "Redwood Estates": 'Los Gatos', 
  "Loyola Corners": 'Los Altos',
  "Stanford": 'Palo Alto'
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

def get_city(address_dict):
	for i in ["town", "village", "city", "hamlet"]:
		if i in address_dict.keys():
			return address_dict[i]
	return None

def attempt_nom(nom, blocksizedAddr):
	# before calling this, you'll need to do something like this
	#         nom = Nominatim(user_agent="policedata", scheme='http')
	# Then pass in 'nom' as the first argument.

	place = re.sub(" BLOCK", "", blocksizedAddr.upper()) # take out "BLOCK" if present
	# specify Santa Clara County if it's not already there
	if "SANTA CLARA COUNTY" not in place:
		place = place + ", SANTA CLARA COUNTY"
	place = place.replace("  ", " ") # remove double spaces
	place = place.replace("  ", " ") # remove triple spaces

	# locate address details
	try:
		location = nom.geocode(place, addressdetails=True)
	except:
		print("Nom: failed, {}".format(place))
		return None
	
	# find city and postcode
	if location:
		address = location.raw['address']                       
		if "postcode" in address.keys():
			city = get_city(address) # search address dict for town/city/village
			if city is None and address["postcode"] in zipcode_lookup.keys():
				city = zipcode_lookup[int(address["postcode"])] # if no city listed, check if city can be found from zipcode dict
			if city and city in cities_in_scc:
				return city, address["postcode"]
			elif city and city in communities_dict.keys():
				return communities_dict[city], address['postcode']
			else:
				print("Nom: could not locate city or not in Santa Clara County of: {}".format(place))
		else:
			print("Couldn't find postcode.")
			# if there is no house number, add one and check again
			if not any(chr.isdigit() for chr in place):
				print("Nom: adding house number")
				place = "1000 " + place
				return (attempt_nom(nom, place))
	else:
		print("Nom could not find postcode/city of: {}".format(place))
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