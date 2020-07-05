# import urllib.request
import matplotlib.pyplot as plt
import pandas as p

STATES = ['ca', 'fl', 'tx', 'az', 'co']

URL_START = "https://covidtracking.com/api/v1/states/"
URL_END = "/daily.csv"

DAYS = 30

def plot ():
    # fetch the data
    pct_pos = p.DataFrame()
    deaths = p.DataFrame()
    first = True
    pops = p.read_csv ('data/state-populations.csv').set_index('state')
    for state in STATES:
        pop = pops.loc[state.upper()]['population']
        # print (pop)
        url = URL_START + state + URL_END
        df = p.read_csv (url)
        if first:
            pct_pos['date'] = p.to_datetime(df['date'], format='%Y%m%d')
            deaths['date'] = pct_pos['date']
            first = False
        pct_pos[state] = df['positiveIncrease']/df['totalTestResultsIncrease']
        deaths[state] = df['deathIncrease']*1000000/pop
    pct_pos.set_index('date', inplace=True)
    # plot
    pct_pos.iloc[0:DAYS].plot(legend=True, title="Percent Positive (day)")
    deaths.set_index('date', inplace=True)
    # plot
    deaths.iloc[0:DAYS].plot(legend=True, title="Deaths/1M (day)")
   
