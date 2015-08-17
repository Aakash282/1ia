import numpy as np 
import pandas as pd 
import os 
import datavalidation as val
import loadRaw as load
import csv

# data is missing week and/or year columns, which are needed to perform a data
# analysis

def separate_teams():
    table = load.getDataset()
    team_dict = val.get_teams(table)
    return team_dict

def write_teams():
    table = load.getDataset()
    teams_table = separate_teams()
    team_keys = teams_table.keys()
    team_keys = list(set([x[:-5] for x in team_keys]))
    yes_ser = pd.Series(np.repeat(np.array(['True']), len(table)))
    no_ser = pd.Series(np.repeat(np.array(['False']), len(table)))
    for team in team_keys:
        home_team = teams_table[team + ' home'] 
        away_team = teams_table[team + ' away'] 
        home_team = format_home(home_team)
        home_team['home_field?'] = yes_ser 
        away_team = format_away(away_team)
        away_team['home_field?'] = no_ser 
        table_out = pd.merge(home_team, away_team, how = 'outer')
        dirpath =  os.getcwd()[:-10] + '/data/teamdata/'
        table_out.to_csv(dirpath + team + '.csv')
        
def format_home(home_team):
    keys = home_team.keys()
    keys_1 = [x[3:] for x in keys if 'ht' == x[0:2]]
    keys_2 = ['opp_' + x[3:] for x in keys if 'at' == x[0:2]]
    keys_3 = ['opp_' + x[5:] for x in keys if 'away' == x[0:4]]
    keys_4 = [x[5:] for x in keys if 'home' == x[0:4]]
    out = keys_4 + keys_3 + list(keys[2:22]) + keys_1 + keys_2
    out.remove('wins_toss')
    out.remove('opp_endance')
    home_team.columns = out
    return home_team

def format_away(away_team):
    keys = away_team.keys()
    keys_1 = ['opp_'+ x[3:] for x in keys if 'ht' == x[0:2]]
    keys_2 = [x[3:] for x in keys if 'at' == x[0:2]]
    keys_3 = [x[5:] for x in keys if 'away' == x[0:4]]
    keys_4 = ['opp_' + x[5:] for x in keys if 'home' == x[0:4]]
    out = keys_4 + keys_3 + list(keys[2:22]) + keys_1 + keys_2
    out.remove('opp_wins_toss')
    out.remove('endance')
    away_team.columns = out
    return away_team
