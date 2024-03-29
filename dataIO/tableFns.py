import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import loadRaw as load

def get_teams(table):
    '''returns a dictionary of teams separated by their location.  Ex:
    get_teams()['Dallas Cowboys home'] would return the cowboys' home game
    information'''
    teams = {}
    team_keys = list(table['home_team'].values) + list(table['away_team'].values)
    for name in team_keys:        
        for location in ['home', 'away' ]:
            teams[name + location] = table[table[location + '_team'] == name]
    return teams

def get_team_keys():
    '''gets a list of all teams'''
    table = load.getDataset()
    teams = list(set(list(table['home_team'].values) + list(table['away_team'].values)))
    teams = [x.strip() for x in teams]
    return teams
        
def cum_stat(stat):
    '''Gives a rough idea of the dsistribution of a stat for all games at
    a glance.  Input is a string'''
    table = load.getDataset()
    return table.describe()[stat]

def cum_array(stat):
    '''Returns a pd series of a particular stat from the table. Input is 
    a string'''
    return load.getDataset()[stat]
    
def team_array():
    '''Returns a dictionary of pd dataframe objects.  Filters out the data
    to only include a specific team. Ex usage:
    
    df = team_array()
    print df['Dallas Cowboys']
    '''
    table = load.getDataset()
    teams = get_teams(table)
    team_keys = get_team_keys()
    combined = {}
    for team in team_keys:
        combined[team] = pd.merge(teams[team + ' home'], \
                                  teams[team + ' away'], how = 'outer')
    return combined


def team_array_1(team, table):
    '''exactly the same as team_array except for a specific team.  much cleaner
    than the other function; may delete team_array.  ex:
    team_array_1('Dallas Cowboys') == team_array()['Dallas Cowboys']
    '''
    # There is a weird spacing issue?
    team += " "
    return pd.merge(filter_table(table, 'home_team', team), \
             filter_table(table, 'away_team', team), how = 'outer')

def filter_table(table, column, entry):
    '''filters the table to only include certain entries'''
    return table[(table[column]) == entry]
    
def get_values(table, column):
    '''returns all unique values for a given column'''
    return set(table[column].values)

def get_previous_stats(table, week, n):
    ''' Returns the previous n weeks for a given table.  Returns a table'''
    table = table.sort('week year')
    table_lst = [int(x) for x in list(table['week year'])]
    index = 0
    if week in table_lst:
        index = table_lst.index(week)
    else:
        index = table_lst.index(week + 1)
    if index == 0:
        return None
    if index < n:
        return table[0:index]
    return table[index  - n: index]


    