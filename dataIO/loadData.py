import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import loadRaw as load


def loadYear(year):
    # Creates and returns a season DataFrame for a given year
    base_dir = load.getPath()
    data_dir = base_dir + "/data/teamdatabyyear/"
    yearDataPath = data_dir + "teamdata%d/" % year
    teamFiles = os.listdir(yearDataPath)

    teams = [open(yearDataPath + team, 'r') for team in teamFiles]
    teamData = [pd.DataFrame.from_csv(t) for t in  teams]
    season = [team.sort(['week year'], ascending=[1]).reset_index(drop=True) for team in teamData]
    return season

def getTeamData(year, team):
    base_dir = load.getPath()
    path = base_dir + '/data/teamdatabyyear/teamdata%d/%s.csv' %(year,team)
    return pd.DataFrame.from_csv(path)

def getYearData(year):
    base_dir = load.getPath()
    path = base_dir + '/data/NFLstatsbyyear/NFL0114_TeamStats_raw%d.csv' %year
    return pd.DataFrame.from_csv(path)