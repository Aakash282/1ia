import numpy as np 
import pandas as pd 
import os 
import tableFns as TFns
import loadRaw as load
import csv	
import multiprocessing
from joblib import Parallel, delayed
from timeit import default_timer


def separate_teams(table):
    team_dict = TFns.get_teams(table)
    return team_dict

def write_teams_year(year):
    '''Writes the feature data for all teams in a given year'''
    table = load.getYearData(year)
    teams_table = separate_teams(table)
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
        dirpath =  os.path.expanduser('~') + '/FSA/data/teamdatabyyear/teamdata%d/' %year
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        table_out = table_out.sort('week year')
        table_out.to_csv(dirpath + team + '.csv')

def write_teams_years(start, stop):
    '''parallelized version of write_teams_year'''
    start_time = default_timer()
    # the -1 is because I like to use my computer while running things
    num_cores = min(14, multiprocessing.cpu_count() - 1)
    Parallel(n_jobs = num_cores)(delayed(write_teams_year)(x) for x in range(start, stop+1))
    print 'Ellapsed time', default_timer() - start_time, 'seconds Using %i core(s)' %num_cores
            
def write_teams():
    table = load.getDataset()
    teams_table = separate_teams(table)
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
    out = [keys[0]] + keys_4 + keys_3 + list(keys[3:23]) + keys_1 + keys_2
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
    out = [keys[0]] + keys_4 + keys_3 + list(keys[3:23]) + keys_1 + keys_2
    out.remove('opp_wins_toss')
    out.remove('endance')
    away_team.columns = out
    return away_team