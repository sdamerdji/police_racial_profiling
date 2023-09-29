import pandas as pd

canonical_race_list = ['White', 'Hispanic/Latino/a', 'Asian', 'Middle Eastern or South Asian',
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
    elif city == "Union City":
        return pd.Series([67039], index=["total"])
    elif city == "Saratoga":
        return pd.Series([28437], index=["total"])
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
        