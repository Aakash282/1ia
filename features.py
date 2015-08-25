import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dataIO import tableFns as TFns

class game:
    '''The idea behind this class is to be able to make a prediction for a 
    possible game that may occur in the future'''
    def __init__(self, home_team, away_team, week_year, field):
        
        self.home = home_team
        self.away = away_team
        self.field = field
        if len(week_year) > 2:
            self.week = int(week_year.split(' ')[0])
            self.year = int(week_year.split(' ')[1])
        else:
            print 'improper time field format!'
    
    def get_stats(self, n):
        home_path = os.getcwd()[:-3] + 'data/teamdatabyyear/teamdata%d/%s.csv' \
            %(self.year, self.home) 
        home_table = pd.DataFrame.from_csv(home_path)
        home_stats = TFns.get_previous_stats(home_table, self.week, n)
        away_path = os.getcwd()[:-3] + 'data/teamdatabyyear/teamdata%d/%s.csv' \
            %(self.year, self.away) 
        away_table = pd.DataFrame.from_csv(away_path)        
        away_stats = TFns.get_previous_stats(away_table, self.week, n)
        return {'home stats': home_stats, 'away stats': away_stats}

    def get_features(self, n):
        stats = get_stats(self, n)
        home_stats = stats['home stats']
        away_stats = stats['away stats']
        #compute features here.  This is currently just an example
        #would probably want a dictionary of different features
        
def rush_feature(team):
    i = 2001
    path = os.getcwd()[:-3] + 'data/NFLstatsbyyear/NFL0114_TeamStats_raw%d.csv' %i
    table = pd.DataFrame.from_csv(path)
    team_path = os.getcwd()[:-3] + 'data/teamdatabyyear/teamdata%d/%s.csv' %(i,team) 
    team_table = pd.DataFrame.from_csv(team_path)
    total_rush = np.append(np.array(table['ht_rush_yards']), \
                           np.array(table['at_rush_yards']))
    team_rush = np.array(team_table['rush_yards'])
    return (team_rush - total_rush.mean()) / total_rush.std()     

def total_yds_feature(team):
    i = 2001
    path = os.getcwd()[:-3] + 'data/NFLstatsbyyear/NFL0114_TeamStats_raw%d.csv' %i
    table = pd.DataFrame.from_csv(path)
    team_path = os.getcwd()[:-3] + 'data/teamdatabyyear/teamdata%d/%s.csv' %(i,team) 
    team_table = pd.DataFrame.from_csv(team_path)
    total = np.append(np.array(table['ht_total_yards']), \
                           np.array(table['at_total_yards']))
    team_total = np.array(team_table['total_yards'])
    return (team_total - total.mean()) / total.std()
    