import wget 
import re
import os
import time
from bs4 import BeautifulSoup, SoupStrainer


datadir = os.path.expanduser('~') + '/FSA/data/'
pages = datadir + 'DVOApages/'
f = open(datadir + 'DVOA', 'w')
header = 'year;week;team;total_dvoa;off_dvoa;def_dvoa;st_dvoa\n'
f.write(header)
for y in range(2001, 2015):
    for w in range(1, 18): 
        with open(pages+'year%dweek%d.html' %(y,w), 'r') as g:
            only_tables = SoupStrainer('table')
            soup = BeautifulSoup(g,parse_only=only_tables)
            data = soup.find_all('td')
            numTeams = len(data) / 6
            for i in range(numTeams):
                teamData = [str(y)] + [str(w)] + [data[x].text.strip('%') for x in range(i*6, i*6+5)]
                line = ';'.join(teamData)
                f.write(line + '\n')




f.close()