import os
import sys
import numpy as np
import pandas as pd
sys.path.append(os.path.expanduser('~') + '/FSA/1ia/dataIO/' )
sys.path.append(os.path.expanduser('~') + '/FSA/1ia/lib/' )
import tableFns as TFns
import loadData as load
import game
import team
import multiprocessing 
from joblib import Parallel, delayed
import time


datadir = os.path.expanduser('~') + "/FSA/data/teamdatabyyear/"
with open('teamHeaders.csv', 'r') as f: 
	headers = f.readlines()
	headers = [h.strip() for h in headers]
	print headers

# iterate over the years
for year in range(2001, 2015):
	season = load.loadYear(year)
	yearDataPath = datadir + "teamdata%d/" % year
	print year
	# iterate over the teams
	for t in season: 
		gen = team.team(season[t][headers])
		features = gen.computeFeatures(3)

		features = features.tolist()
		# print features

		with open(yearDataPath + t + 'features.csv', 'w') as g: 
			g.write(','.join(headers) + '\n')
			for game in features: 
				g.write(','.join([str(x) for x in game]) + '\n')


