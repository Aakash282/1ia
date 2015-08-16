import os
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

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
    assert(len(set(home_TOP + away_TOP >= 3595) == 1))
    
def get_teams():
    table = import_table()
    #table.describe()
    teams = {}
    team_keys = list(table['home team'].values) + list(table['away team'].values)
    for name in team_keys:        
        teams[name] = table[table['home team'] == name]
        teams[name].append(table[table['away team'] == name])
    return teams
    
    
    
    
    
    
    
    