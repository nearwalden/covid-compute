# Tools for processing Johns Hopkins University COVID-19 data
# Data repo:  https://github.com/CSSEGISandData/COVID-19

import pandas as p
import matplotlib.pyplot as plt
import states

# this should be set to the location where you have cloned the repo above
COVID_19_REPO_PATH = "/Users/dd/gitcode/covid-19/csse_covid_19_data/csse_covid_19_time_series/"

# confirmed file
COVID_19_CONFIRMED = "time_series_19-covid-Confirmed.csv"

# confirmed file
COVID_19_DEATHS = "time_series_19-covid-Deaths.csv"


# returns a dataframe of data
def load_data ():
    confirmed = p.read_csv(COVID_19_REPO_PATH + COVID_19_CONFIRMED)
    configmed_us = summarize_us (confirmed)
    confirmed_country = summarize_country (confirmed)
    confirmed_state = summarize_state (confirmed)
    deaths = p.read_csv(COVID_19_REPO_PATH + COVID_19_DEATHS)
    deaths_summary = summarize_country (deaths)
    deaths_state = summarize_state (confirmed)    


def summarize_country (df_in):
    df_simpler = df_in.drop(['Province/State', 'Lat', 'Long'], axis=1)
    df_simpler_g = df_simpler.groupby('Country/Region')
    df = df_simpler_g.sum().copy()
    return df.T

def summarize_us (df_in):
    df_states = df_in [df_in['Country/Region'] == 'US']
    df_states = df_states[df_states['Province/State'].isin(states.US_STATES)]
    df_states = df_states.drop(['Country/Region', 'Lat', 'Long'], axis=1)
    df_states = df_states.set_index('Province/State')
    df_us = df_states.T
    df_us['US'] = 0
    for state in df_us.keys():
        df_us.US += df_us[state]
    return df_us

def plot (df, params, title):
    fig, ax = plt.subplots()
    for param in params:
            ax.plot(df.index, df[param])
    ax.set_title (title)
    plt.show()



    

