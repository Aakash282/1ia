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