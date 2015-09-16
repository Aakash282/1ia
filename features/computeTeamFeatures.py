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
with open(os.path.expanduser('~') + '/FSA/1ia/features/teamHeaders.csv', 'r') as f: 
	headers = f.readlines()
	headers = [h.strip() for h in headers]

with open(os.path.expanduser('~') + '/FSA/1ia/features/headersForComputed.csv', 'r') as f: 
	headersForComputed = f.readlines()
	headersForComputed = [h.strip() for h in headersForComputed]

DVOA = load.getDVOA()
DVOAheaders = DVOA.columns[3:].tolist()
print headers + DVOAheaders
# iterate over the years
for year in range(2001, 2015):
	season = load.loadYear(year)
	print year
	yearDVOA = TFns.filter_table(DVOA, 'year', year)
	# iterate over the teams
	for t in season:
		teamDVOA = TFns.filter_table(yearDVOA, 'team', t)
		bye = [x for x in range(1,18) if x not in set(season[t]['week year'])]
		teamDVOA = teamDVOA[teamDVOA.week != bye]
		teamDVOA = teamDVOA.drop(['team','week','year'], axis=1)
		gen = team.team(season[t][headers], teamDVOA, season[t][headersForComputed])
		features = gen.computeFeatures(3)
		features = np.append(np.matrix(season[t]['week year'][3:]).transpose(), features, axis=1)

		computedHeaders = ['record_vs_spread', 'avg_closing_ability', 'comeback_record']
		computedFeatures = gen.computeComplexFeatures(3)

		features = np.concatenate((features, computedFeatures.transpose()), axis=1)
		features = features.tolist()
		
		featuresdir = os.path.expanduser('~') + "/FSA/data/teamfeaturesbyyear/features%d/" % year
		with open(featuresdir + t + '.csv', 'w') as g: 
			g.write(','.join(['week'] + headers + DVOAheaders + computedHeaders) + '\n')
			for game in features: 
				g.write(','.join([str(x) for x in game]) + '\n')

