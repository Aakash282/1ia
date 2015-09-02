# loadRaw.py

import numpy as np 
import pandas as pd 
import os 

def getPath():
    # Returns path to base directory
    base_dir = os.getcwd().split('/')
    base_dir = '/' + base_dir[1] + '/' + base_dir[2] + '/' + base_dir[3]
    return base_dir

def parse():
    # Reads in yearly raw data and generates aggregate NFL0114_TeamStats_raw.csv
    base_dir = getPath()
    data_dir = base_dir + '/data/'

    aggregate_data = pd.read_csv(data_dir + "headers.csv", sep = ";")
    for year in range(2001, 2015):
        print year
        year_data = pd.read_csv(data_dir + "rawdata/rawdata%d" % year, sep=";")
        for line in range(len(year_data['week'])):
            year_data['week'][line] = str(year_data['week'][line]) + " %d" %year
          
        aggregate_data = pd.merge(aggregate_data, year_data, how = 'outer')
    columns = list(aggregate_data.keys())
    columns[0] = 'week year'
    aggregate_data.columns = columns
    aggregate_data.to_csv(data_dir + "NFL0114_TeamStats_raw.csv")

def parseYear():
    # Reads in yearly raw data and generates csv for each year
    base_dir = getPath()
    data_dir = base_dir + '/data/'

    for year in range(2001, 2015):
        print year
        aggregate_data = pd.read_csv(data_dir + "headers.csv", sep = ";")
        year_data = pd.read_csv(data_dir + "rawdata/rawdata%d" % year, sep=";")
        aggregate_data = pd.merge(aggregate_data, year_data, how = 'outer')
        columns = list(aggregate_data.keys())
        columns[0] = 'week year'
        aggregate_data.columns = columns
        aggregate_data.to_csv(data_dir + "NFL0114_TeamStats_raw%d.csv" %year)
        
def getDataset():
    base_dir = getPath()
    return pd.DataFrame.from_csv(base_dir + "/data/NFL0114_TeamStats_raw.csv")

def getTeamData(year, team):
    base_dir = getPath()
    path = base_dir + '/data/teamdatabyyear/teamdata%d/%s.csv' %(year,team)
    return pd.DataFrame.from_csv(path)

def getYearData(year):
    base_dir = getPath()
    path = base_dir + '/data/NFLstatsbyyear/NFL0114_TeamStats_raw%d.csv' %year
    return pd.DataFrame.from_csv(path)