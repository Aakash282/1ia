import os
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
import pandas

def parse_data():
    '''processes the data.  Change the file location'''
    header = "week	home team	away team	spread	time of day (ET)	ht wins toss?	Roof	Surface	attendance	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ref	ht score	ht first downs	ht rush attempts	ht rush yards	ht rush TDs	ht pass comp	ht pass attempt	ht pass yards	ht pass TDs	ht INT	ht sacks	ht sack yards lost	ht net pass yards	ht total yards	ht fumbles	ht fumbles lost	ht turnovers	ht penalties	ht penalty yards	ht 3rd down converted	ht 3rd down attempts	ht 4th down converted	ht 4th down attempts	ht total plays	ht TOP	at score	at first downs	at rush attempts	at rush yards	at rush TDs	at pass comp	at pass attempt	at pass yards	at pass TDs	at INT	at sacks	at sack yards lost	at net pass yards	at total yards	at fumbles	at fumbles lost	at turnovers	at penalties	at penalty yards	at 3rd down converted	at 3rd down attempts	at 4th down converted	at 4th down attempts	at total plays	at TOP	Year"
    header = header.split("\t")
    table = []
    table.append(header)
    
    for i in range(2001, 2009):
        f = open("/home/jamal/1ia/data/features" + str(i))
        line = f.readline()
        print i, "\n"
        while line != "":
            line = line.split(";")
            line.append(str(i))
            line = [x.strip() for x in line]
            if len(line) == 74:
                table.append(line)
            line = f.readline()
        f.close()
    return(table, header)
    #print(tabulate(table))

def get_column(column_name, table, header):
    ''' get all vals for a specific column'''
    index = header.index(column_name)
    column = []
    for row in table:
        column.append(row[index])
    column.remove(column_name)
    return column

def get_teams(table, header):
    '''get all rows for a team'''
    team_dict = {}
    home_ind = header.index('home team')
    away_ind = header.index('away team')
    for row in table:
        for ind in [home_ind, away_ind]:
            if row[ind] not in team_dict.keys():
                team_dict[row[ind]]= []
            team_dict[row[ind]].append(row)
    return team_dict

def plot_score(table, header):
    '''example of difference btwn home/away field scores.  will do 
    actual processing later'''
    ht_score = [float(x) for x in get_column('ht score', table, header)]
    at_score = get_column('at score', table, header)    
    at_score[at_score.index('24:29')] = '0'
    at_score = [float(x) for x in at_score]
    plt.hist( np.array(ht_score) - np.array(at_score) )

def validate():
    table, header = parse_data()
    column_data = {}
    for i in range(len(header)):
        column_data[header[i]] = get_column(header[i], table, header)
    for team in ['ht ', 'at ']:
        for elem in [('rush attempts', 'rush TDs'), ('pass attempt', 'pass comp'), 
                     ('pass comp', 'pass TDs'), ('fumbles', 'fumbles lost')]:
            test1 = np.array(column_data[team + elem[0]]) >= \
                    np.array(column_data[team + elem[1]])
            if len(set(test1)) != 1:
                print elem
    
    
    
'''
rush attempts >= rush TDs
pass attempt >= pass comp >= pass TDs
pass attempt-pass comp >= INT
net pass yards + rush yards = total yards
fumbles <= fumbles lost
turnovers = fumbles lost + INT
3rd down converted < 3rd down attempts (4th)
sum TOP < 60






'''