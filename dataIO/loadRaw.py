# loadRaw.py

import numpy as np 
import pandas as pd 
import os 

def getPath():
    ospath = os.getcwd().split('/')
    ospath = '/' + ospath[1] + '/' + ospath[2] + '/' + ospath[3]
    return ospath

def parse():
    ospath = getPath()
    datadir = ospath + '/data/'

    p = pd.read_csv(datadir + "headers.csv", sep = ";")
    for y in range(2001, 2015):
        print y
        lst_temp = pd.read_csv(datadir + "features/features%d" % y, sep=";")
        for line in range(len(lst_temp['week'])):
            lst_temp['week'][line] = str(lst_temp['week'][line]) + " %d" %y
          
        p = pd.merge(p, lst_temp, how = 'outer')
    columns = list(p.keys())
    columns[0] = 'week year'
    p.columns = columns
    p.to_csv(datadir + "NFL0114_TeamStats_raw.csv")

def parseYear():
    ospath = getPath()
    datadir = ospath + '/data/'

    for y in range(2001, 2015):
        print y
        p = pd.read_csv(datadir + "headers.csv", sep = ";")
        lst_temp = pd.read_csv(datadir + "features/features%d" % y, sep=";")
        p = pd.merge(p, lst_temp, how = 'outer')
        columns = list(p.keys())
        columns[0] = 'week year'
        p.columns = columns
        p.to_csv(datadir + "NFL0114_TeamStats_raw%d.csv" %y)
        
def getDataset():
    ospath = getPath()
    return pd.DataFrame.from_csv(ospath + "/data/NFL0114_TeamStats_raw.csv")

def getTeamData(year, team):
    ospath = getPath()
    path = ospath + '/data/teamdatabyyear/teamdata%d/%s.csv' %(year,team)
    return pd.DataFrame.from_csv(path)

def getYearData(year):
    ospath = getPath()
    path = ospath + '/data/NFLstatsbyyear/NFL0114_TeamStats_raw%d.csv' %year
    return pd.DataFrame.from_csv(path)