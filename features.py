import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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
    