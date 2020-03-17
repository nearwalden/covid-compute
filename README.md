# COVID Data Analysis

This repo contains some routines that assist in analyzing COVID-19 data.  It works with the Johns Hopkins data and organizes it into pandas dataframes that are useful to work with. 

## Prerequisites

This code was written for Python 3.  The following packages are required:

- pandas
- matplotlib

## Data Sources

[This page](DATA.md) describes the sources for the data used here.

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


