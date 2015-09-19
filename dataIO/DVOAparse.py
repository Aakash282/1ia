import wget 
import re
import os
import time
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import tableFns as TFns

datadir = os.path.expanduser('~') + '/FSA/data/'
pages = datadir + 'DVOApages/'
f = open(datadir + 'DVOA.csv', 'w')
header = 'year,week,team,total_dvoa,total_dvoa_rank,weighted_dvoa,weighted_dvoa_rank,off_dvoa,off_dvoa_rank,weighted_off_dvoa,weighted_off_dvoa_rank,def_dvoa,def_dvoa_rank,weighted_def_dvoa,weighted_def_dvoa_rank,st_dvoa,st_dvoa_rank,weighted_st_dvoa,weighted_st_dvoa_rank\n'
f.write(header)
for y in range(1997, 2015):
    for w in range(1, 18): 
        with open(pages+'year%dweek%d.html' %(y,w), 'r') as g:
            only_tables = SoupStrainer('table')
            soup = BeautifulSoup(g,parse_only=only_tables)
            data = soup.find_all('td')
            numTeams = len(data) / 18
            for i in range(numTeams):
                teamData = [str(y)] + [str(w)] + [data[i*18].text] + [str(float(data[x].text.strip('%'))) for x in range(i*18+2, i*18+18)]
                line = ','.join(teamData)
                f.write(line + '\n')
f.close()

# this part of the code is used to convert the abbreviated names to their full names
teams = ['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills', 'Carolina Panthers', 'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos', 'Detroit Lions', 'Green Bay Packers', 'Indianapolis Colts', 'Jacksonville Jaguars', 'Kansas City Chiefs', 'Miami Dolphins', 'Minnesota Vikings', 'New England Patriots', 'New Orleans Saints', 'New York Giants', 'New York Jets', 'Oakland Raiders', 'Philadelphia Eagles', 'Pittsburgh Steelers', 'San Diego Chargers', 'San Francisco 49ers', 'Seattle Seahawks', 'St. Louis Rams', 'Tampa Bay Buccaneers', 'Tennessee Titans', 'Washington Redskins']
table = pd.read_csv(datadir + 'DVOA.csv')
team_short = list(set(table['team']))
team_short.sort()
# SEA and SF names need to be switched
temp = (team_short[26], team_short[27])
team_short[26] = temp[1]
team_short[27] = temp[0]
# create conversion dictionary
team_conversion = {}
for i in range(len(team_short)):
    team_conversion[team_short[i]] = teams[i]
    
replace_team = []    
for elem in table.iterrows():
    replace_team.append(team_conversion[elem[1]['team']])
table['team'] = replace_team
table.to_csv(datadir + 'DVOA.csv', index = False)



