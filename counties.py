# Analyze the largest US counties

import pandas as p
import covid

# returns a dataframe with per-county analysis:
#   confirmed cases
#   confirmed cases/million
#   cases/mile^2
#   deaths  
#   deaths/million
#   change in confirmed case increase (%), 2-day v. prev 2-day

def analyze ():
    cd = covid.CovidData ()
    out = []
    # iterate over counties
    for county in cd.biggest_counties_list():
        county_data = cd.biggest_counties[county]
        item = {'county': county}
        pop = cd.biggest_counties_data.loc[county]['population']
        area = cd.biggest_counties_data.loc[county]['land_area_mi2']        
        item['confirmed'] = int(county_data.iloc[-1]['confirmed'])
        item['confirmed/1M'] = item['confirmed'] * 1000000 / pop
        item['confirmed/sqmi'] = item['confirmed'] / area
        item['deaths'] = int(county_data.iloc[-1]['deaths'])
        item['deaths/1M'] = item['deaths'] * 1000000 / pop
        county_data['pct_change'] = county_data['confirmed'].pct_change()
        county_data['new_cases'] = county_data['confirmed'].diff()
        # 2-day and 3-day window
        if county_data.iloc[-1]['confirmed'] == county_data.iloc[-2]['confirmed']:
            # item['pct_change_3day'] = county_data.iloc[-4:-1]['pct_change'].mean()
            # item['pct_change_3day_prev'] = county_data.iloc[-7:-4]['pct_change'].mean()
            item['pct_change_2day'] = county_data.iloc[-3:-1]['pct_change'].mean()
            item['pct_change_2day_prev'] = county_data.iloc[-5:-3]['pct_change'].mean()
        else:
            # item['pct_change_3day'] = county_data.iloc[-3:]['pct_change'].mean()
            # item['pct_change_3day_prev'] = county_data.iloc[-6:-3]['pct_change'].mean()
            item['pct_change_2day'] = county_data.iloc[-2:]['pct_change'].mean()
            item['pct_change_2day_prev'] = county_data.iloc[-4:-2]['pct_change'].mean()
        # delta = county_data.iloc[-6:-3]['pct_change'].mean() - county_data.iloc[-3:]['pct_change'].mean()
        item['last_peak_pct'] = last_peak(county_data['pct_change'])
        item['last_peak_value'] = last_peak(county_data['new_cases'])
        item['days_since_peak'] = len(county_data) - county_data.reset_index()['new_cases'].idxmax() - 1
        item['new_cases/1M'] = county_data['new_cases'][-2:-1].mean() *1000000 / pop
        out.append(item)
    return p.DataFrame(out).set_index('county')     

# finds entries to first peak since end of series
def last_peak (s):
    i = 0
    j = 0
    while i < len(s)-1:
        if s[-1 - i] > s[-2 - i]:
            return (i - j)
        if s[-1 - i] == 0:
            j += 1
        i += 1
    return 0

        