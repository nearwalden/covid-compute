# Tools for processing Johns Hopkins University COVID-19 data
# Data repo:  https://github.com/CSSEGISandData/COVID-19

import pandas as p
import matplotlib.pyplot as plt
import states

# this should be set to the location where you have cloned the repo above
COVID_19_REPO_PATH = "/Users/dd/gitcode/COVID-19/csse_covid_19_data/csse_covid_19_time_series/"

# confirmed file
COVID_19_CONFIRMED = "time_series_19-covid-Confirmed.csv"

# confirmed file
COVID_19_DEATHS = "time_series_19-covid-Deaths.csv"

class covid_data:
  def __init__(self):
    self.confirmed = p.read_csv(COVID_19_REPO_PATH + COVID_19_CONFIRMED)
    self.deaths = p.read_csv(COVID_19_REPO_PATH + COVID_19_DEATHS)

def summarize_country (df_in):
    df_simpler = df_in.drop(['Province/State', 'Lat', 'Long'], axis=1)
    df_simpler_g = df_simpler.groupby('Country/Region')
    df = df_simpler_g.sum().copy()
    return df.T

def summarize_us (df_in):
    df_states = df_in [df_in['Country/Region'] == 'US'].copy()
    df_states['State'] = df_states['Province/State'].map(states.NAME_MAP)
    df_states = df_states.drop(['Country/Region', 'Lat', 'Long', 'Province/State'], axis=1)
    df_states_gb = df_states.groupby('State').sum()
    df_us = df_states_gb.T
    df_us['US'] = df_us.sum(axis=1)
    return df_us

def plot (df, params, title):
    fig, ax = plt.subplots()
    for param in params:
            ax.plot(df.index, df[param])
    ax.set_title (title)
    plt.show()



    

