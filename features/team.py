import os
import sys
import numpy as np
import pandas as pd
sys.path.append(os.path.expanduser('~') + '/FSA/1ia/dataIO/' )
sys.path.append(os.path.expanduser('~') + '/FSA/1ia/lib/' )
import tableFns as TFns
import loadData as load

class team:
	'''This class is use for computing 1 season of features for a team'''
	def __init__(self, season, DVOA, complex_season):
		DVOA = DVOA.reset_index()
		season = season.reset_index()
		complex_season.reset_index()
		self.season = pd.concat([season,DVOA],axis=1)
		self.cols = season.columns + DVOA.columns[3:]
		self.season = self.season.drop(['index', 'level_0'], axis=1)
		self.complex_season = pd.concat([complex_season],axis=1)

	def computeFeatures(self, n):
		'''compute all features for this team's season'''
		window = np.zeros([n, len(self.cols)])
		season = np.matrix(self.season.values)[:-1]
		features = np.empty_like(season[0:season.shape[0]-(n-1)])
		for i in range(season.shape[0]-(n-1)):
			window = season[i:i+n]
			window = window.mean(0)
			features[i] = window	

		return features

	def computeComplexFeatures(self, n):
		'''compute all complex features for this team's season'''
		season = np.matrix(self.complex_season.values)
		data = np.empty_like(season[0:season.shape[0]-n])

		for i in range(len(data)):
			data[i] = season[i + n]

		complexFeatures = np.empty(len(data))
		record_vs_spread = np.empty(len(data))
	
		for i,game in enumerate(data.tolist()):
			this_team = game[0]
			score_diff = float(game[1]) - float(game[2])
			spread = game[3].split()
			result_vs_spread = resultVsSpread(this_team, score_diff, spread)
			complexFeatures[i] = result_vs_spread

		for w,record in enumerate(complexFeatures):
			record_vs_spread[w] = sum(complexFeatures[:w + 1]) / (w + 1)
		
		return record_vs_spread

def resultVsSpread(this_team, score_diff, spread):
	'''compute the result vs spread for a given team, score_diff, and spread'''
		if spread != ['Pick']:
			spread_team = ''.join(spread[:-1])
			spread = float(spread[-1])

			# If spread uses this team
			if spread_team == this_team.replace(' ', ''):
				# If this_team beat the spread
				if score_diff + spread > 0:
					return 1
				else:
					return 0
				
			# If spread uses opp_team
			else:
				# If this_team beat the spread
				if score_diff - spread > 0:
					return 1
				else:
					return 0

		# If spread is Pick
		else:
			# this_team beat the spread
			if score_diff > 0:
				return 1
			else:
				return 0