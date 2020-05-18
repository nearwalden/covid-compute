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
        item['conf'] = int(county_data.iloc[-1]['confirmed'])
        item['conf/1M'] = item['conf'] * 1000000 / pop
        item['conf/sqmi'] = item['conf'] / area
        county_data['new_cases'] = county_data['confirmed'].diff()
        item['day conf'] = county_data['new_cases'].iloc[-1]
        item['day conf/1M'] = county_data['new_cases'].iloc[-1] * 1000000 / pop        
        item['deaths'] = int(county_data.iloc[-1]['deaths'])
        item['deaths/1M'] = item['deaths'] * 1000000 / pop
        county_data['conf_pct_change'] = county_data['confirmed'].pct_change()
        county_data['deaths_pct_change'] = county_data['deaths'].pct_change()
        county_data['new_deaths'] = county_data['deaths'].diff()        
        item['day deaths'] = county_data['new_deaths'].iloc[-1]
        item['day deaths/1M'] = county_data['new_deaths'].iloc[-1] * 1000000 / pop        
        # 2-day and 3-day window
        item['conf_pct_chg'] = county_data.iloc[-3:-1]['conf_pct_change'].mean()
        item['conf_pct_chg'] = county_data.iloc[-2:]['conf_pct_change'].mean()
        # delta = county_data.iloc[-6:-3]['pct_change'].mean() - county_data.iloc[-3:]['pct_change'].mean()
        item['deaths_pct_chg'] = county_data.iloc[-2:]['deaths_pct_change'].mean()
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

def deaths_1m (d):
    cd = covid.CovidData ()
    data = []
    d_str = d.strftime('%m-%d-%Y')
    for county in cd.biggest_counties_list():
        county_data = cd.biggest_counties[county]
        county_meta = cd.biggest_counties_data.loc[county]
        item = {'county': county, 'state': county_meta['abbrev']}
        pop = cd.biggest_counties_data.loc[county]['population']
        county_data['deaths'] = county_data['deaths'].diff()
        county_data['deaths3'] = county_data['deaths'].rolling(3).mean()
        county_data['deaths_1m'] = county_data['deaths3'] * 1000000 /pop
        county_data['deaths_1m'] = county_data['deaths_1m'].round()
        item['deaths_1m'] = county_data.loc[d_str]['deaths_1m']
        item['population'] = pop
        data.append(item)
    return p.DataFrame(data)       