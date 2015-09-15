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
		# do not include the last game of the season since we
		# will NEVER know this information until the season is over
		season = np.matrix(self.complex_season.values)[:-1]

		# complexFeatures will contain all computed features where
		# each computed feature is its own row
		complexFeatures = np.empty(len(season)-(n-1))

		# add a computed feature
		complexFeatures = computeRecordVsSpread(season, n)
		return complexFeatures

# This function computes a team's record vs the spread as a fraction
def computeRecordVsSpread(season, n):
		record_vs_spread = np.empty(len(season))
		buf = np.empty(len(season))
	
		for i,game in enumerate(season.tolist()):
			this_team = game[0]
			score_diff = float(game[1]) - float(game[2])
			spread = game[3].split()
			record_vs_spread[i] = resultVsSpread(this_team, score_diff, spread)

		# use buffer to compute sum of records all weeks
		buf = [sum(record_vs_spread[:i]) for i in range(len(record_vs_spread))][n:]
		buf.append(sum(record_vs_spread))
		# now divide by record size (i + n)
		buf = [buf[i] / (i+n) for i in range(len(buf))]
		
		# resize and assign correct values
		record_vs_spread = record_vs_spread[:-(n-1)]
		for i in range(len(record_vs_spread)):
			record_vs_spread[i] = buf[i]

		return record_vs_spread
		
# this function computes how a team did against a spread for a single game
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