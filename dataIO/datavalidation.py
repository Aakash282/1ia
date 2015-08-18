import os
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import loadRaw as load
# May want to make table a global variable?


def parse_data():
    '''processes the data.  Change the file location'''
    header = "week	home team	away team	spread	time of day (ET)	ht wins toss?	Roof	Surface	attendance	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ht score	ht first downs	ht rush attempts	ht rush yards	ht rush TDs	ht pass comp	ht pass attempt	ht pass yards	ht pass TDs	ht INT	ht sacks	ht sack yards lost	ht net pass yards	ht total yards	ht fumbles	ht fumbles lost	ht turnovers	ht penalties	ht penalty yards	ht 3rd down converted	ht 3rd down attempts	ht 4th down converted	ht 4th down attempts	ht total plays	ht TOP	at score	at first downs	at rush attempts	at rush yards	at rush TDs	at pass comp	at pass attempt	at pass yards	at pass TDs	at INT	at sacks	at sack yards lost	at net pass yards	at total yards	at fumbles	at fumbles lost	at turnovers	at penalties	at penalty yards	at 3rd down converted	at 3rd down attempts	at 4th down converted	at 4th down attempts	at total plays	at TOP	Year"
    header = header.split("\t")
    table = []
    table.append(header)
    
    for i in range(2001, 2009):
        f = open( os.getcwd()[:-10] + "data/features" + str(i))
        line = f.readline()
        print i, "\n"
        while line != "":
            line = line.split(";")
            line.append(str(i))
            line = [x.strip() for x in line]
            if len(line) == len(header):
                table.append(line)
            line = f.readline()
        f.close()
    return(table, header)

    
def validate():
    '''basic sanity checks on the numerical parts of the data'''
    table = load.getDataset()
    # These are inequalities
    for team in ['ht_', 'at_']:
        for elem in [('rush_attempts', 'rush_TDs'), ('pass_attempt', 'pass_comp'), 
                     ('pass_comp', 'pass_TDs'), ('fumbles', 'fumbles_lost'), 
                     ('3rd_down_attempts', '3rd_down_converted'),
                     ('4th_down_attempts', '4th_down_converted')]:
            test = table[team + elem[0]] >= table[team + elem[1]]
            assert(len(set(test)) == 1)
        # These are equalities
        for elem in [('net_pass_yards', 'rush_yards', 'total_yards'),
                     ('fumbles_lost', 'INT', 'turnovers')]:
            test = table[team + elem[0]] + table[team + elem[1]] - \
                table[team + elem[2]]
        assert(len(set(test)) == 1)
    home_TOP = np.array([int(x.split(':')[0])*60 + \
                         int(x.split(':')[1]) for x in table['ht_TOP']])
    away_TOP = np.array([int(x.split(':')[0])*60 + \
                         int(x.split(':')[1]) for x in table['at_TOP']])
    assert(len(set(home_TOP + away_TOP >= 3595)) == 1 )


def home_away_differences():
    ''' Finds the differences between teams and their opponents based on
    location.  Returns a dictionary of numpy arrays.  Ex. use:
    
    a = home_away_differences()
    plt.hist(a['Dallas Cowboys home score'], 20)
    
    which would plot a hist of how many more points the Cowboys have vs their
    opponent when the Cowboys are playing at home.  
    a['Dallas Cowboys away score'] would be their stats when they are away

    Might delete.  Too specific of a function
    '''
    table =load.getDataset()
    all_teams = get_teams(table)
    team_keys = get_team_keys()
    columns = list(table.keys())
    # ghetto, hardcoded filtering method :(
    columns = [x[3:] for x in columns if ('at' in x)]    
    columns.remove('endance')
    columns.remove('TOP')
    stat_diff = {}
    for team in team_keys:
        for stat in columns:
            for location in [(' home', 'ht_', 'at_'), (' away', 'at_', 'ht_')]:
                stat_diff[team + location[0] + ' ' + stat] = \
                    np.array(all_teams[team + location[0]][location[1] + stat]) - \
                    np.array(all_teams[team + location[0]][location[2] + stat])
    return stat_diff


    
    
    
    
    
    