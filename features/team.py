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
	def __init__(self, season, DVOA):
		DVOA = DVOA.reset_index()
		season = season.reset_index()
		DVOA = DVOA.reset_index()
		self.season = pd.concat([season,DVOA],axis=1)
		self.cols = season.columns + DVOA.columns[3:]
		self.season = self.season.drop(['index', 'level_0'], axis=1)

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

	def computeRecordVsSpread(self, n, year, this_team, season):
		'''compute all raw features for this team's season'''
		
		num_weeks = len(season[this_team]['week year'])
		record_vs_spread = np.empty(num_weeks)

		for w in range(num_weeks):
			score_diff = season[this_team]['score'][w] - season[this_team]['opp_score'][w]
			spread = season[this_team]['spread'][w].split()
			if spread != ['Pick']:
				spread_team = ' '.join(spread[:-1])
				spread = float(spread[-1])
			
				# If spread uses this team
				if spread_team == this_team:

					# If this_team beat the spread
					if score_diff + spread > 0:
						if w == 0:
							record_vs_spread[w] = 1
						else:
							record_vs_spread[w] = (record_vs_spread[w - 1] * (w - 1) + 1) / float(season[this_team]['week year'][w])

					# If this_team lost against the spread
					else:
						if w == 0:
							record_vs_spread[w] = 0
						else:
							record_vs_spread[w] = record_vs_spread[w - 1] * (w - 1) / float(season[this_team]['week year'][w])

				# If spread uses opp_team
				else:

					# If this_team beat the spread
					if score_diff - spread > 0:
						if w == 0:
							record_vs_spread[w] = 1
						else:
							record_vs_spread[w] = (record_vs_spread[w - 1] * (w - 1) + 1) / float(season[this_team]['week year'][w])
					
					# If this_team lost against the spread
					else:
						if w == 0:
							record_vs_spread[w] = 0
						else:
							record_vs_spread[w] = record_vs_spread[w - 1] * (w - 1) / float(season[this_team]['week year'][w])
			
			# If spread is Pick
			else:

				# this_team beat the spread
				if score_diff > 0:
					if w == 0:
						record_vs_spread[w] = 1
					else:
						record_vs_spread[w] = (record_vs_spread[w - 1] * (w - 1) + 1) / float(season[this_team]['week year'][w])

				# this_tem lost against the spread
				else:
					if w == 0:
						record_vs_spread[w] = 0
					else:
						record_vs_spread[w] = record_vs_spread[w - 1] * (w - 1) / float(season[this_team]['week year'][w])
			
			print year, w, season[this_team]['week year'][w], season[this_team]['team'][w], season[this_team]['opp_team'][w], season[this_team]['home_field?'][w], season[this_team]['score'][w], season[this_team]['opp_score'][w], season[this_team]['spread'][w]

		print record_vs_spread

		season = np.matrix(self.season.values)[:-1]
		features = np.empty_like(season[0:season.shape[0]-(n-1)])
		
		for i in range(season.shape[0]-(n-1)):
			features[i] = season[i]	

		return features








