import os
import pandas as pd
import re

def loadYear(year):
    # Creates and returns a season DataFrame for a given year
    datadir = os.path.expanduser('~') + "/FSA/data/teamdatabyyear/"
    yearDataPath = datadir + "teamdata%d/" % year
    teamFiles = os.listdir(yearDataPath)
    teams = [open(yearDataPath + team, 'r') for team in teamFiles]
    season = {}
    for t in teams:
        a = re.search('/.*.csv', str(t))
        #holy shit this line is bad. halp pls.  
        team_name = a.group(0).split('/')[-1][:-4]
        temp_stor = pd.DataFrame.from_csv(t)
        season[team_name] = temp_stor.sort(['week year'], ascending=[1]).reset_index(drop=True)
    return season

def getTeamData(year, team):
    path = os.path.expanduser('~') + '/FSA/data/teamdatabyyear/teamdata%d/%s.csv' %(year,team)
    return pd.DataFrame.from_csv(path)

def getYearData(year):
    path = os.path.expanduser('~') + '/FSA/data/NFLstatsbyyear/NFL0114_TeamStats_raw%d.csv' %year
    return pd.DataFrame.from_csv(path)