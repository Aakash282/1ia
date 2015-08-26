import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import loadRaw as load


def loadYear(year):
    ospath = load.getPath()
    datadir = ospath + "/data/teamdatabyyear/"
    y = year
    yearDataPath = datadir + "teamdata%d/" % y
    teamFiles = os.listdir(yearDataPath)

    teams = [open(yearDataPath + team, 'r') for team in teamFiles]
    teamData = [pd.DataFrame.from_csv(t) for t in  teams]
    season = [team.sort(['week year'], ascending=[1]).reset_index(drop=True) for team in teamData]
    return season

def getTeamData(year, team):
    ospath = load.getPath()
    path = ospath + '/data/teamdatabyyear/teamdata%d/%s.csv' %(year,team)
    return pd.DataFrame.from_csv(path)

def getYearData(year):
    ospath = load.getPath()
    path = ospath + '/data/NFLstatsbyyear/NFL0114_TeamStats_raw%d.csv' %year
    return pd.DataFrame.from_csv(path)