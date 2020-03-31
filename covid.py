# Tools for processing Johns Hopkins University COVID-19 data
# Data repo:  https://github.com/CSSEGISandData/COVID-19

import pandas as p
import matplotlib.pyplot as plt
import state_fixes
import datetime

# this should be set to the location where you have cloned the repo above
COVID_19_REPO_PATH = "COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/"

STATE_CONF_PATH = "data/state_confirmed.csv"
STATE_DEATHS_PATH = "data/state_deaths.csv"

class CovidData:
    def __init__(self):
        # self.county_data = p.read_csv ('data/biggest_us_counties.csv').set_index('name')       
        us = p.read_csv (STATE_CONF_PATH).set_index('Date')
        self.confirmed_us = us.drop(['Other', 'SHIP', 'Unnamed: 0'], 1) 
        self.confirmed_us['US'] = self.confirmed_us.sum(axis=1)       
        # self.confirmed_countries = self.summarize_countries (self.confirmed)
        # self.confirmed_biggest_counties = self.summarize_counties (self.confirmed)
        us = p.read_csv(STATE_DEATHS_PATH).set_index('Date')   
        self.deaths_us = us.drop(['Other', 'SHIP', 'Unnamed: 0'], 1)                   
        self.deaths_us['US'] = self.deaths_us.sum(axis=1)       
        # self.deaths_countries = self.summarize_countries (self.deaths)
        # self.deaths_biggest_counties = self.summarize_counties (self.deaths)
        self.states = self.make_indiv_tables (self.confirmed_us, self.deaths_us)
        # self.countries = self.make_indiv_tables (self.confirmed_countries, self.deaths_countries)
        # self.biggest_counties = self.make_indiv_tables (self.confirmed_biggest_counties, self.deaths_biggest_counties)
        self.state_populations = p.read_csv ('data/state-populations.csv').set_index('state')
        # self.country_populations = p.read_csv ('data/country-populations.csv').set_index('country')

    # def load_file (self, date):
    #     filename = self.base_path + COVID_19_REPO_PATH + datetime.strftime("%Y-%m-%d") + ".csv"
    #     return p.read_csv(filename)

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

    # def countries_list (self):
    #     return (list (self.confirmed_countries.columns))

    # def counties_list (self):
    #     return (list (self.confirmed_biggest_counties))        

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

    def plot_state_pct_change (self, states):
        df = self.confirmed_us
        fig, ax = plt.subplots()
        for state in states:
            ax.plot(df.index, df[state].pct_change(), marker='o')
        ax.legend()
        ax.set_title ('Daily % incrase in cases')
        plt.show()

    def plot_state_new_cases (self, states):
        df = self.confirmed_us
        fig, ax = plt.subplots()
        for state in states:
            ax.plot(df.index, df[state].diff(), marker='o')
        ax.legend()
        ax.set_title ('Number of new cases')
        plt.show()


    # def plot_countries (self, countries, conf_or_death):
    #     if conf_or_death == 'confirmed':
    #         df = self.confirmed_countries
    #     else:
    #         df = self.deaths_countries
    #     fig, ax = plt.subplots()
    #     for country in countries:
    #         ax.plot(df.index, df[country], marker='o')
    #     ax.legend()
    #     ax.set_title ('Country cases (' + conf_or_death + ')')
    #     plt.show()

# routines to get the pump primed
# initial date is 1/22/2020
# can do country and US state with name fixes through 3/21
# can do country, state and county in format 4 starting 3/22


def load_file (base_path, date):
    filename = base_path + COVID_19_REPO_PATH + date.strftime("%m-%d-%Y") + ".csv"
    return p.read_csv(filename)

# the next two just need to be run once to get the base file setup through 3/21
#    Once you have that you shouldn't need to run these again.

def first_file (base_path):
    d = datetime.date(2020, 1, 22)
    ctry_conf = [] 
    ctry_deaths = []
    state_conf = [] 
    state_deaths = []
    curr_date = ""
    for i in range(60):
        curr_date = d.strftime("%m-%d-%Y")
        path = base_path + COVID_19_REPO_PATH + curr_date + ".csv"
        df = p.read_csv(path)
        df_ctry = df.groupby('Country/Region').sum().T
        df_ctry['Date'] = curr_date
        ctry_conf.append(df_ctry.loc['Confirmed'])
        ctry_deaths.append(df_ctry.loc['Deaths'])
        df_us = df[df['Country/Region'] == 'US']
        df_us['State'] = df_us['Province/State'].apply(lambda x: state_fixes.NAME_MAP[x])
        df_state = df_us.groupby('State').sum().T
        df_state['Date'] = curr_date
        state_conf.append(df_state.loc['Confirmed'])
        state_deaths.append(df_state.loc['Deaths'])
        print ("Processed " + curr_date)        
        d += datetime.timedelta(days=1)
    write_data (ctry_conf, 'data/country_confirmed.csv')
    write_data (ctry_deaths, 'data/country_deaths.csv')
    write_data (state_conf, 'data/state_confirmed.csv')
    write_data (state_deaths, 'data/state_deaths.csv')

def write_data (d, path):
    df = p.DataFrame(d).reset_index()
    df = df.drop('index', 1)
    df.fillna(0).to_csv(path)

# these work with the new format
# need to be run once per day
# d is a datetime object.  datetime.today() works for today.


def add_day (base_path, d):
    df = load_file (base_path, d)
    df_us = df[df['Country_Region'] == 'US'].copy()
    df_us['State'] = df_us['Province_State'].apply(lambda x: state_fixes.STATE_MAP[x])
    df_state = df_us.groupby('State').sum().T
    df_state['Date'] = d.strftime("%m-%d-%Y")
    # return (add_line(df_ctry.loc['Confirmed'], 'data/country_confirmed.csv'))
    add_line (df_state.loc['Confirmed'], STATE_CONF_PATH)
    add_line (df_state.loc['Deaths'], STATE_DEATHS_PATH)    

def add_line (df_line, path):
    df = p.read_csv (path)
    df_new = df.append(df_line, ignore_index=True).fillna(0)
    df_new = df_new.drop('Unnamed: 0', 1)
    df_new.to_csv(path)










    

