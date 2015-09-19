# loadRaw.py

import numpy as np 
import pandas as pd 
import os 

def getPath():
    '''Returns path to base directory'''
    base_dir = os.getcwd().split('/')
    base_dir = '/' + base_dir[1] + '/' + base_dir[2] + '/' + base_dir[3]
    return base_dir

def parse(start,stop):
    '''Reads in yearly raw data and generates aggregate NFL0114_TeamStats_raw.csv'''
    # Note: Not actually sure that this function is ever called
    base_dir = getPath()
    data_dir = base_dir + '/data/'

    # aggregate_data is where every year's data is added
    aggregate_data = pd.read_csv(data_dir + "headers.csv", header=None, sep = ";")
    columns = list(aggregate_data.keys())
    columns[0] = 'week year'
    for year in range(start, stop+1):
        print year
        year_data = pd.read_csv(data_dir + "rawdata/rawdata%d" % year, sep=";", header=None)          
        aggregate_data = pd.merge(aggregate_data, year_data, how = 'outer')
    print columns
    aggregate_data.columns = columns
    aggregate_data.to_csv(data_dir + "NFL0114_TeamStats_raw.csv")

def parseYear(start, stop):
    ''' Reads in yearly raw data and generates csv for each year
        Ideally should be combined with parse() so that either parse calls
        parseYear or parseYear() is eliminated completely'''
    # Note: Not actually sure that this function is ever called either
    base_dir = getPath()
    data_dir = base_dir + '/data/'

    for year in range(start, stop+1):
        print year
        headers = pd.read_csv(data_dir + "headers.csv", sep = ",")
        year_data = pd.read_csv(data_dir + "rawdata/rawdata%d" % year, sep=";", header=None)
        columns = list(headers.keys())
        columns[0] = 'week year'
        year_data.columns = columns
        year_data.to_csv(data_dir + "NFLstatsbyyear/NFL0114_TeamStats_raw%d.csv" %year)
        
def getDataset():
    base_dir = os.path.expanduser('~') + "/FSA/data"
    return pd.DataFrame.from_csv(base_dir + "/NFL0114_TeamStats_raw.csv")

def getTeamData(year, team):
    base_dir = getPath()
    path = base_dir + '/data/teamdatabyyear/teamdata%d/%s.csv' %(year,team)
    return pd.DataFrame.from_csv(path)

def getYearData(year):
    base_dir = getPath()
    path = base_dir + '/data/NFLstatsbyyear/NFL0114_TeamStats_raw%d.csv' %year
    return pd.DataFrame.from_csv(path)