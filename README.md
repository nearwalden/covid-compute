# COVID Data Analysis

This repo contains some routines that assist in analyzing COVID-19 data.  It works with the Johns Hopkins data and organizes it into pandas dataframes that are more reasonable to work with. 

## Prerequisites

This code was written for Python 3.  The following packages are required:

- pandas
- matplotlib

## Data Sources

[This page](DATA-SOURCES.md) describes the sources for the data used here.  The main data that's here today is the 

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

## dataframes

A `CovidData` object contains  two types of data structures.  Ones that dataframes that include a single data items for all states or countries, and ones that contain many data structures, each with multiple data items for one state or country.  In all data structures each row is a day in the time series.  Country names are spelled out and states use the two character abbreviation. 

- confirmed_us:  confirmed cases for each state
- confirmed_countries:  confirmed casee for each country
- deaths_us:  deaths for each state
- deaths_countries:  deaths for each country
- states:  a dict where the keys are state names, and the dataframe has confirmed cases and deaths.
- countries:  a dict where the keys are country names, and the dataframe has confirmed cases and deaths.
- country_populations:  populations of all countries, indexed by name
- state_populations:  populations of states and US, indexed by 2-character abbreviation.

## methods

The `CovidData` object has a couple of basic plotting methods so far:

`plot_states(states, conf_or_death)`
- *states* - an array of state names (2-character abbreviations)
- *conf_or_death* - set to 'confirmed' or 'deaths'

`plot_countries(countries, conf_or_death)`
- *countries* - an array of country names 
- *conf_or_death* - set to 'confirmed' or 'deaths'
  
The following return the countries or states in the dataset, useful for iterating.

`countries_list()`

`states_list()`





