# COVID Data Analysis

This repo contains some routines that assist in analyzing COVID-19 data.  It works with the Johns Hopkins data and organizes it into pandas dataframes that are more reasonable to work with.  

Note 1:   this is currently only creating a US dataset with data for each state and each county.  Countries will be added back in shortly (they changed a bunch of names and I just need to fix them).

Note 2:   when I switched to the daily reports from Hopkins you now have to run a script to ingest them.  See `Updating the data` below.  

## Prerequisites

This code was written for Python 3.  The following packages are required:

- pandas
- matplotlib

## Data sources

[This page](DATA-SOURCES.md) describes the sources for the data used here.  The data set used here is built up from the daily reports in `COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/`.  The new daily reports come out once per day at 8pm ET.  

## Usage

To get started:

1.  Install the prerequisites if needed
2.  Clone the data repo somewhere on your system
3.  Clone this repo somewhere else

Note that once you've cloned the data repo, you can just do `git pull origin master` to get the new data each day.

Next, create a `CovidData` object that cleans up all of the data and makes a bunch of pandas dataframes.  It takes one argument, which is the path to the data repo, including the trailing `/`:

```python
import covid
cd = covid.CovidData('/home/dd/git/')  # assumes data is in /home/dd/git/COVID-19...
```

## Data files

The extracted data files are stored in `/data` in this git repo.  The four key files right now are:

- `state_confirmed.csv` - from 1/22/20
- `state_deaths.csv` - from 1/22/20
- `county_confirmed.csv` - from 3/22/20
- `county_deaths.csv` - from 3/22/20

These are loaded into dataframes the `covid.CovidData` object and a number of other dataframes are created from them.

## Updating the data

If the two data files above are out of date, then you can do the following:

```python
import datetime
import covid
day = datetime.date(2020,4,14)  # put in the right date
# example for pathname below:  if repo is in ~/repos/COVID-19, this should be ~/repos/
covid.add_day('path_to_covid_data_repo', day  
```

Should just work, let me know if it doesn't!  

## Dataframes

A `CovidData` object contains  two types of data structures.  Ones that dataframes that include a single data items for all states or counties, and ones that contain many data structures, each with multiple data items for one state or country.  In all data structures each row is a day in the time series.  State names use the two character abbreviation, and counties use the format `Name, STATE` with the county name and state abbreviation respectively. 

- confirmed_us:  confirmed cases for each state
- confirmed_counties:  confirmed casee for each county
- deaths_us:  deaths for each state
- deaths_counties:  deaths for each country
- states:  a dict where the keys are state names, and the dataframe has confirmed cases and deaths.
- country_populations:  populations of all countries, indexed by name
- state_populations:  populations of states and US, indexed by 2-character abbreviation.

## methods

The `CovidData` object has a couple of basic plotting methods so far:

`plot_states(states, conf_or_death)`
- *states* - an array of state names (2-character abbreviations)
- *conf_or_death* - set to 'confirmed' or 'deaths'

`plot_countries(countries, conf_or_death)` *currently not working*
- *countries* - an array of country names 
- *conf_or_death* - set to 'confirmed' or 'deaths'
  
The following return the countries or states in the dataset, useful for iterating.

`states_list()`

## Other code

In `states.py` the function `analyze()` creates a dataframe with a bunch of interesting state-level data.  





