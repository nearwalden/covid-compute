# Analyze the state of US states

import pandas as p
import covid2

# returns a dataframe with per-state analysis:
#   confirmed cases
#   confirmed cases/million
#   deaths  
#   deaths/million
#   average dailly confirmed increase (%), 3-day avg
#   change in confirmed case increase (%), 3-day v. prev 3-day

def analyze ():
    cd = covid2.CovidData ()
    out = []
    # iterate over states
    for state in cd.states_list():
        state_data = cd.states[state]
        item = {'state': state}
        pop = cd.state_populations.loc[state]['population']
        item['confirmed'] = int(state_data.iloc[-1]['confirmed'])
        item['confirmed/1M'] = item['confirmed'] * 1000000 / pop
        item['deaths'] = int(state_data.iloc[-1]['deaths'])
        item['deaths/1M'] = item['deaths'] * 1000000 / pop
        state_data['pct_change'] = state_data['confirmed'].pct_change()
        state_data['new_cases'] = state_data['confirmed'].diff()
        # 2-day and 3-day window
        if state_data.iloc[-1]['confirmed'] == state_data.iloc[-2]['confirmed']:
            item['pct_change_3day'] = state_data.iloc[-4:-1]['pct_change'].mean()
            item['pct_change_3day_prev'] = state_data.iloc[-7:-4]['pct_change'].mean()
            item['pct_change_2day'] = state_data.iloc[-3:-1]['pct_change'].mean()
            item['pct_change_2day_prev'] = state_data.iloc[-5:-3]['pct_change'].mean()
        else:
            item['pct_change_3day'] = state_data.iloc[-3:]['pct_change'].mean()
            item['pct_change_3day_prev'] = state_data.iloc[-6:-3]['pct_change'].mean()
            item['pct_change_2day'] = state_data.iloc[-2:]['pct_change'].mean()
            item['pct_change_2day_prev'] = state_data.iloc[-4:-2]['pct_change'].mean()
        # delta = state_data.iloc[-6:-3]['pct_change'].mean() - state_data.iloc[-3:]['pct_change'].mean()
        item['last_peak_pct'] = last_peak(state_data['pct_change'])
        item['last_peak_value'] = last_peak(state_data['new_cases'])        
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


        