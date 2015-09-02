import features
from dataIO import loadData as ld 
from matplotlib import pyplot as plt

features.feature_set(2012,2013)
# years = range(2001, 2002)
# for y in years: 
# 	season = ld.loadYear(y)
# 	for team in season: 
# 		for idx, w in team.iterrows():
# 			week_year = "%d %d" % (w['week year'], y)
# 			ht = w['team']
# 			at = w['opp_team']
# 			if not w['home_field?']:
# 				at = ht
# 				ht = w['opp_team']
# 			g = game(ht, at, week_year)
# 			print week_year, ht, at
# 			features = g.get_features(3)
# 			if features['home']['pass'] is not None:
# 				if features['home']['score'] > features['away']['score']:
# 					plt.scatter(features['home']['conv 3d'], features['home']['score'], c='g')
# 					plt.scatter(features['away']['conv 3d'], features['away']['score'], c='r')
# 				else:
# 					plt.scatter(features['home']['conv 3d'], features['home']['score'], c='r')
# 					plt.scatter(features['away']['conv 3d'], features['away']['score'], c='g')

# plt.title('Score vs 3rd Downs')
# plt.xlabel("Moving Average of Converted 3rd Downs")
# plt.ylabel('Final Score')
# plt.show()

