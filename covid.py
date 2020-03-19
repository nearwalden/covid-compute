# Tools for processing Johns Hopkins University COVID-19 data
# Data repo:  https://github.com/CSSEGISandData/COVID-19

import pandas as p
import matplotlib.pyplot as plt
import state_fixes

# this should be set to the location where you have cloned the repo above
COVID_19_REPO_PATH = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/"

# confirmed file
COVID_19_CONFIRMED = "time_series_19-covid-Confirmed.csv"

# confirmed file
COVID_19_DEATHS = "time_series_19-covid-Deaths.csv"

class CovidData:
    def __init__(self, base_path):
        self.confirmed = p.read_csv(base_path + COVID_19_REPO_PATH + COVID_19_CONFIRMED)
        self.deaths = p.read_csv(base_path + COVID_19_REPO_PATH + COVID_19_DEATHS)
        self.confirmed_us = self.summarize_us (self.confirmed)
        self.confirmed_countries = self.summarize_countries (self.confirmed)
        self.deaths_us = self.summarize_us (self.deaths)        
        self.deaths_countries = self.summarize_countries (self.deaths)
        self.states = self.make_indiv_tables (self.confirmed_us, self.deaths_us)
        self.countries = self.make_indiv_tables (self.confirmed_countries, self.deaths_countries)
        self.state_populations = p.read_csv ('data/state-populations.csv').set_index('state')
        self.country_populations = p.read_csv ('data/country-populations.csv').set_index('country')        

    def summarize_us (self, df_in):
        df_states = df_in [df_in['Country/Region'] == 'US'].copy()
        df_states['State'] = df_states['Province/State'].map(state_fixes.NAME_MAP)
        df_states = df_states.drop(['Country/Region', 'Lat', 'Long', 'Province/State'], axis=1)
        df_states_gb = df_states.groupby('State').sum()
        df_us = df_states_gb.T
        df_us['US'] = df_us.sum(axis=1)
        return df_us

    def summarize_countries (self, df_in):
        df_simpler = df_in.drop(['Province/State', 'Lat', 'Long'], axis=1)
        df_simpler_g = df_simpler.groupby('Country/Region')
        df = df_simpler_g.sum().copy()
        return df.T

    def make_indiv_tables (self, confirmed, deaths):
        tables = {}
        for name in confirmed.columns:
            new_df = p.DataFrame()
            new_df['confirmed'] = confirmed[name]
            new_df['deaths'] = deaths[name]
            tables[name] = new_df
        return tables

    def states_list (self):
        return (list (self.confirmed_us.columns))

    def countries_list (self):
        return (list (self.confirmed_countries.columns))        

    def plot_states (self, states, conf_or_death):
        if conf_or_death == 'confirmed':
            df = self.confirmed_us
        else:
            df = self.deaths_us
        fig, ax = plt.subplots()
        for state in states:
            ax.plot(df.index, df[state], marker='o')
        ax.legend()
        ax.set_title ('State cases (' + conf_or_death + ')')
        plt.show()

    def plot_countries (self, countries, conf_or_death):
        if conf_or_death == 'confirmed':
            df = self.confirmed_countries
        else:
            df = self.deaths_countries
        fig, ax = plt.subplots()
        for country in countries:
            ax.plot(df.index, df[country], marker='o')
        ax.legend()
        ax.set_title ('Country cases (' + conf_or_death + ')')
        plt.show()



    

