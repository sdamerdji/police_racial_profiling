import pandas as pd

canonical_race_list = ['White', 'Hispanic/Latino(a)', 'Asian', 'Middle Eastern or South Asian',
                       'Black/African American', 'Pacific Islander', 'Native American', 'Multiple', "Other"]


def get_population(city):
    if city == "Los Altos":
        # from https://worldpopulationreview.com/us-cities/los-altos-ca-population
        # White	17,735	58.14%
        # Asian	9,586	31.43%
        # Two or More Races	1,567	5.14%
        # Black or African American	145	0.48%
        # Some Other Race	100	0.33%
        # American Indian and Alaska Native	24	0.08%
        world_pop = [17735, 1347, 9586, 0, 145, 0, 24, 1567, 100]

        # For different numbers, see: https://data.census.gov/cedsci/table?q=DP05&g=1600000US0643280&tid=ACSDP5Y2020.DP05
        # White 19, 074
        # Black or African American        210
        # Native American    43.5
        # Asian        7, 749
        # Indian        2, 919
        # Other        445
        # In that I assigned multiple to the various races, in proportion. Arguably this should all go in the race
        # of whatever is not white, because that's how most people (and police) would categorize them.
        # Also, there's no Hispanic in here, because that's not a race, and it's impossible to tease out how many
        # people in each of the other categories should count.
        census_pop = [19074, 0, 7749, 2919, 210, 0, 43.5, 0, 445]

        # Hybrid.
        # Let's take the world-pop numbers, and split "Asian" into "Asian" and "South Asian" in the proportion of
        # the census numbers. So, 9586*(7749/(7749+2919))
        hybrid_pop = [17735, 1357, 9586 * (7749 / (7749 + 2919)), 9586 * (2919 / (7749 + 2919)), 145, 0, 24, 1567, 100]

        return pd.Series(hybrid_pop, index=canonical_race_list)
    elif city == "Mountain View":
        # from https://worldpopulationreview.com/us-cities/mountain-view-ca-population, 10/27/23
        # Non-Hispanic:
        # White	33,923	41.16%
        # Asian	27,397	33.25%
        # Two or more races	3,923	4.76%
        # Other race	313	0.38%
        # Black or African American	1,922	2.33%
        # Native American	105	0.13%
        # Native Hawaiian or Pacific Islander		0%

        # Hispanic:
        # White	5,987	7.26%
        # Asian	86	0.1%
        # Two or more races	3,963	4.81%
        # Other race	4,455	5.41%
        # Black or African American	75	0.09%
        # Native American	248	0.3%
        # Native Hawaiian or Pacific Islander	12	0.01%

        # Let's combine all the Hispanic options into Hispanic/Latino(a).
        world_pop = [33923, 14826, 27397, 0, 1922, 0, 105, 3923, 313]

        # Again we'll use the census data to split Asian into "Asian" and "South Asian"
        # Here's the breakdown by ancestry: https://statisticalatlas.com/place/California/Mountain-View/Ancestry
        # Chinese       8578
        # Indian        6230
        # Filipino      1904
        # Japanese      1351
        # Korean        1223
        # Vietnamese    734
        # Taiwanese     638
        # Mixed         504
        # Thai          331
        # Pakistani     150
        # Indonesian    143
        # Cambodian     122
        # None of these definitions are tight, but let's call Indian and Pakistani "South Asian", and the rest "Asian"
        # South Asian:  6380        29.1%
        # Asian:        15528       70.9%
        hybrid_pop = world_pop
        hybrid_pop[2] = 0.709 * world_pop[2]
        hybrid_pop[3] = 0.291 * world_pop[2]
        return pd.Series(hybrid_pop, index=canonical_race_list)
    elif city == "Cupertino":
        return pd.Series([55326], index=["total"])
    elif city == "Los Altos Hills":
        return pd.Series([7879], index=["total"])
    else:
        print("City {} not available.".format(city))
        return None

def get_households(city):
    if city == "Los Altos":
        # from https://worldpopulationreview.com/us-cities/los-altos-ca-population, retrieved 8/31/23
        return 10805
    elif city == "Union City":
        return 20800
    elif city == "Saratoga":
        return 11039
    elif city == "Los Altos Hills":
        return 3125
    elif city == "Cupertino":
        return 20963
    else:
        print("City {} not available.".format(city))
        return None
        