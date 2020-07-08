# Analyze the state of US states

import pandas as p
import covid
import datetime

# returns a dataframe with per-state analysis:
#   confirmed cases
#   confirmed cases/million
#   deaths  
#   deaths/million
#   average dailly confirmed increase (%), 3-day avg
#   change in confirmed case increase (%), 3-day v. prev 3-day

def analyze ():
    cd = covid.CovidData ()
    out = []
    # iterate over states
    for state in cd.states_list():
        state_data = cd.states[state]
        item = {'state': state}
        pop = cd.state_populations.loc[state]['population']
        item['conf'] = int(state_data.iloc[-1]['confirmed'])
        item['conf/1M'] = item['conf'] * 1000000 / pop
        state_data['new_cases'] = state_data['confirmed'].diff()
        item['day conf'] = state_data['new_cases'].iloc[-1]
        item['day conf/1M'] = state_data['new_cases'].iloc[-1] * 1000000 / pop        
        item['deaths'] = int(state_data.iloc[-1]['deaths'])
        item['deaths/1M'] = item['deaths'] * 1000000 / pop
        state_data['conf_pct_change'] = state_data['confirmed'].pct_change()
        state_data['deaths_pct_change'] = state_data['deaths'].pct_change()
        state_data['new_deaths'] = state_data['deaths'].diff()
        item['day deaths'] = state_data['new_deaths'].iloc[-1]
        item['day deaths/1M'] = state_data['new_deaths'].iloc[-1] * 1000000 / pop        
        # 2-day and 3-day window
        item['conf_pct_chg'] = state_data.iloc[-3:-1]['conf_pct_change'].mean()
        # item['conf_pct_chg_prev'] = state_data.iloc[-5:-3]['conf_pct_change'].mean()
        # delta = state_data.iloc[-6:-3]['pct_change'].mean() - state_data.iloc[-3:]['pct_change'].mean()
        item['deaths_pct_chg'] = state_data.iloc[-2:]['deaths_pct_change'].mean()
        # item['deaths_pct_chg_prev'] = state_data.iloc[-4:-2]['deaths_pct_change'].mean()
        # item['conf_days_peak'] = len(state_data) - state_data.reset_index()['new_cases'].idxmax() - 1
        # item['deaths_days_peak'] = len(state_data) - state_data.reset_index()['new_deaths'].idxmax() - 1        
        out.append(item)
    return p.DataFrame(out).set_index('state')     

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

def pct_change_bins_conf (d):
    cd = covid.CovidData ()
    data = []
    d_str = d.strftime('%m-%d-%Y')
    bins = p.IntervalIndex.from_tuples([(0, 0.06), (0.06, 0.12), (0.12, 0.24), (0.24, 0.35), \
                                        (0.35, 0.7), (0.7, 1.4), (1.4, 20)])
    for state in cd.states_list():
        state_data = cd.states[state]
        item = {'state': state}
        state_data['pct_change'] = state_data['confirmed'].pct_change()
        state_data['pct_change_2day'] = state_data['pct_change'].rolling(2).mean()
        item['pct_change_2day'] = state_data.loc[d_str]['pct_change_2day']
        data.append(item)
    df = p.DataFrame(data)
    return p.cut(df['pct_change_2day'], bins).value_counts()


def pct_change_bins_deaths (d):
    cd = covid.CovidData ()
    data = []
    d_str = d.strftime('%m-%d-%Y')
    bins = p.IntervalIndex.from_tuples([(0, 0.06), (0.06, 0.12), (0.12, 0.24), (0.24, 0.35), \
                                        (0.35, 0.7), (0.7, 1.4), (1.4, 20)])
    for state in cd.states_list():
        state_data = cd.states[state]
        item = {'state': state}
        state_data['pct_change'] = state_data['deaths'].pct_change()
        state_data['pct_change_2day'] = state_data['pct_change'].rolling(2).mean()
        item['pct_change_2day'] = state_data.loc[d_str]['pct_change_2day']
        data.append(item)
    df = p.DataFrame(data)
    return p.cut(df['pct_change_2day'], bins).value_counts()

def cases_1m_bins (d):
    cd = covid.CovidData ()
    data = []
    d_str = d.strftime('%m-%d-%Y')
    bins = p.IntervalIndex.from_tuples([(0,  10), (10, 20), (20, 30), \
                                        (30, 40), (40, 50), (50, 75), (75, 100), (100, 10000)])
    for state in cd.states_list():
        state_data = cd.states[state]
        item = {'state': state}
        pop = cd.state_populations.loc[state]['population']
        state_data['new_cases'] = state_data['confirmed'].diff()
        state_data['new_cases_1m'] = state_data['new_cases'] * 1000000 /pop
        item['new_cases_1m'] = state_data.loc[d_str]['new_cases_1m']
        data.append(item)
    df = p.DataFrame(data)
    return p.cut(df['new_cases_1m'], bins).value_counts()    

def deaths_1m_bins (d):
    cd = covid.CovidData ()
    data = []
    d_str = d.strftime('%m-%d-%Y')
    bins = p.IntervalIndex.from_tuples([(0, 1), (1, 2), (2, 3), (3, 4), \
                                        (4, 6), (6, 8), (8, 10), (10, 500)])
    for state in cd.states_list():
        state_data = cd.states[state]
        item = {'state': state}
        pop = cd.state_populations.loc[state]['population']
        state_data['deaths'] = state_data['deaths'].diff()
        state_data['deaths_1m'] = state_data['deaths'] * 1000000 /pop
        item['deaths_1m'] = state_data.loc[d_str]['deaths_1m']
        data.append(item)
    df = p.DataFrame(data)
    return p.cut(df['deaths_1m'], bins).value_counts()    

def deaths_1m (d, round=False):
    cd = covid.CovidData ()
    data = []
    d_str = d.strftime('%m-%d-%Y')
    for state in cd.states_list():
        state_data = cd.states[state]
        item = {'state': state}
        pop = cd.state_populations.loc[state]['population']
        state_data['deaths'] = state_data['deaths'].diff()
        state_data['deaths3'] = state_data['deaths'].rolling(3).mean()
        state_data['deaths_1m'] = state_data['deaths3'] * 1000000.0 /pop
        if round:
            state_data['deaths_1m'] = state_data['deaths_1m'].round()
        item['deaths_1m'] = state_data.loc[d_str]['deaths_1m']
        data.append(item)
    return p.DataFrame(data)

def deaths_1m_multi (d, weeks):
    newdf = p.DataFrame()
    for week in range(0, weeks):
        d_week = d - datetime.timedelta(days=7) * week
        d_str = d_week.strftime('%m-%d-%Y')
        deaths = deaths_1m (d_week).set_index('state')
        newdf[d_str] = deaths['deaths_1m']
    return newdf.T.sort_index()

TOP_20 = ["CA","TX","FL","NY","PA","IL","OH","GA","NC","MI","NJ","VA","WA", \
            "AZ","MA","TN","IN","MO","MD","WI"]

TOP_10 = ["CA","TX","FL","NY","PA","IL","OH","GA","NC","MI"]

INTEREST = ['CA', 'TX', 'FL', 'NY', 'MA', 'GA', 'AZ']


  

  




        