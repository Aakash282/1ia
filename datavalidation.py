import os
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
# May want to make table a global variable?


def parse_data():
    '''processes the data.  Change the file location'''
    header = "week	home team	away team	spread	time of day (ET)	ht wins toss?	Roof	Surface	attendance	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ht score	ht first downs	ht rush attempts	ht rush yards	ht rush TDs	ht pass comp	ht pass attempt	ht pass yards	ht pass TDs	ht INT	ht sacks	ht sack yards lost	ht net pass yards	ht total yards	ht fumbles	ht fumbles lost	ht turnovers	ht penalties	ht penalty yards	ht 3rd down converted	ht 3rd down attempts	ht 4th down converted	ht 4th down attempts	ht total plays	ht TOP	at score	at first downs	at rush attempts	at rush yards	at rush TDs	at pass comp	at pass attempt	at pass yards	at pass TDs	at INT	at sacks	at sack yards lost	at net pass yards	at total yards	at fumbles	at fumbles lost	at turnovers	at penalties	at penalty yards	at 3rd down converted	at 3rd down attempts	at 4th down converted	at 4th down attempts	at total plays	at TOP	Year"
    header = header.split("\t")
    table = []
    table.append(header)
    
    for i in range(2001, 2009):
        f = open("/home/jamal/FSA/data/features" + str(i))
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

def write_csv():
    table, header = parse_data()
    with open('/home/jamal/FSA/dataT/2001-2008data.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, quoting = csv.QUOTE_ALL)
        writer.writerows(table)

def import_table():
    return pd.read_csv('/home/jamal/FSA/data/2001-2008data.csv')
    
def validate():
    '''basic sanity checks on the numerical parts of the data'''
    table = import_table()
    TOP = {}
    # These are inequalities
    for team in ['ht ', 'at ']:
        for elem in [('rush attempts', 'rush TDs'), ('pass attempt', 'pass comp'), 
                     ('pass comp', 'pass TDs'), ('fumbles', 'fumbles lost'), 
                     ('3rd down attempts', '3rd down converted'),
                     ('4th down attempts', '4th down converted')]:
            test = table[team + elem[0]] >= table[team + elem[1]]
            assert(len(set(test)) == 1)
        # These are equalities
        for elem in [('net pass yards', 'rush yards', 'total yards'),
                     ('fumbles lost', 'INT', 'turnovers')]:
            test = table[team + elem[0]] + table[team + elem[1]] - \
                table[team + elem[2]]
        assert(len(set(test)) == 1)
    home_TOP = np.array([int(x.split(':')[0])*60 + \
                         int(x.split(':')[1]) for x in table['ht TOP']])
    away_TOP = np.array([int(x.split(':')[0])*60 + \
                         int(x.split(':')[1]) for x in table['at TOP']])
    assert(len(set(home_TOP + away_TOP >= 3595)) == 1 )
    
def get_teams():
    '''returns a dictionary of teams separated by their location.  Ex:
    get_teams()['Dallas Cowboys home'] would return the cowboys' home game
    information'''
    table = import_table()
    #table.describe() useful to use later
    teams = {}
    team_keys = list(table['home team'].values) + list(table['away team'].values)
    for name in team_keys:        
        for location in ['home', 'away' ]:
            teams[name + " " + location] = table[table[location + ' team'] == name]
    return teams, table

def home_away_differences():
    ''' Finds the differences between teams and their opponents based on
    location.  Returns a dictionary of numpy arrays.  Ex. use:
    
    a = home_away_differences()
    plt.hist(a['Dallas Cowboys home score'], 20)
    
    which would plot a hist of how many more points the Cowboys have vs their
    opponent when the Cowboys are playing at home.  
    a['Dallas Cowboys away score'] would be their stats when they are away
    '''
    all_teams, table = get_teams()
    team_keys = get_team_keys()
    columns = list(table.keys())
    # ghetto, hardcoded filtering method :(
    columns = [x[3:] for x in columns if ('at' in x)]    
    columns.remove('endance')
    columns.remove('TOP')
    stat_diff = {}
    for team in team_keys:
        for stat in columns:
            for location in [(' home', 'ht ', 'at '), (' away', 'at ', 'ht ')]:
                stat_diff[team + location[0] + ' ' + stat] = \
                    np.array(all_teams[team + location[0]][location[1] + stat]) - \
                    np.array(all_teams[team + location[0]][location[2] + stat])
    return stat_diff

def get_team_keys():
    table = import_table()
    teams = list(set(list(table['home team'].values) + list(table['away team'].values)))
    # filters out spurious data.  Should change in the future
    teams = [x for x in teams if len(x) > 4]
    return teams

def combine_home_adv(stat):
    '''Finds the difference between a given stat for all teams for home field
    advantage.  Returns a numpy array.  Ex usage would be
    
    diff = combine_home_adv('score')
    diff.mean() -> the average score difference'''
    
    stat_diffs = home_away_differences()
    team_keys = get_team_keys()
    diff = []
    for team in team_keys:
        if len(stat_diffs[team + ' home ' + stat]) != 0 and \
           len(stat_diffs[team + ' away ' + stat]) != 0:
                diff.append(stat_diffs[team + ' home ' + stat].mean() -\
                            stat_diffs[team + ' away ' + stat].mean())
    # I think I am double counting here.  Not sure, but dividing by two only 
    # fixes the median problems
    return np.array(diff)/2.0
        
    
    
    
    
    
    
    
    
    
    