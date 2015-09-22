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

		record_vs_spread = np.array(computeRecordVsSpread(season, n))
		avg_closing_ability = np.array(computeClosingAbilityStats(season, n))
		comeback_record = np.array(computeComebackRecord(season, n))
		avg_plays_per_turnover = np.array(computePlaysPerTurnover(season, n))
		
		complexFeatures = np.vstack((record_vs_spread, avg_closing_ability))
		complexFeatures = np.vstack((complexFeatures, comeback_record))
		complexFeatures = np.vstack((complexFeatures, avg_plays_per_turnover))

		return complexFeatures

# This function computes the average number of plays between turnovers
def computePlaysPerTurnover(season, n):
	plays_and_turnovers = np.empty(len(season)).tolist()
	avg_plays_per_turnover = np.empty(season.shape[0]-(n-1))

	# Bonus term for turnoverless game
	no_turnover_bonus = 4.0 / 3.0

	# Create list of tuples (plays, turnovers)
	for i,game in enumerate(season.tolist()):
		plays = float(game[6])
		turnovers = float(game[7])
		plays_and_turnovers[i] = (plays, turnovers)

	# Compute moving average
	for i in range(season.shape[0]-(n-1)):
		window = plays_and_turnovers[i:i+n]

		# Compute moving sum
		sum_total_plays = sum([pair[0] for pair in window])
		sum_turnovers = sum([pair[1] for pair in window])

		# If there were turnovers, compute average
		if sum_turnovers > 0:
			avg_plays_per_turnover[i] = sum_total_plays / sum_turnovers

		# If there were no turnovers over the 3 game span, multiply by bonus
		else:
			avg_plays_per_turnover[i] = sum_total_plays * no_turnover_bonus

	return avg_plays_per_turnover


# This function computes a team's ability to close out a game
def computeClosingAbilityStats(season, n):
	closing_ability_stats = np.empty(len(season))
	avg_closing_ability = np.empty(season.shape[0]-(n-1))

	for i,game in enumerate(season.tolist()):
		score = float(game[1])
		opp_score = float(game[2])
		final_score_diff = score - opp_score
		startof_fourth_score_diff = (score - float(game[4])) - (opp_score - float(game[5]))
		closing_ability_stats[i] = final_score_diff - startof_fourth_score_diff

	# Compute moving average
	for i in range(season.shape[0]-(n-1)):
		window = closing_ability_stats[i:i+n]
		window = window.mean(0)
		avg_closing_ability[i] = window

	return avg_closing_ability


# This function computes a team's comeback record
def computeComebackRecord(season, n):
	successful_comebacks = np.empty(len(season))
	comeback_opportunities = np.empty(len(season))
	comeback_record = np.empty(len(season))

	for i,game in enumerate(season.tolist()):
		score = float(game[1])
		opp_score = float(game[2])
		score_diff = score - opp_score
		score_startof_fourth = score - float(game[4])
		opp_score_startof_fourth = opp_score - float(game[5])

		# If there was an opportunity for a comeback
		if score_startof_fourth < opp_score_startof_fourth:
			comeback_opportunities[i] = 1

			# If a comeback occurred
			if score_diff > 0:
				successful_comebacks[i] = 1

			# If a comeback attempt failed
			else:
				successful_comebacks[i] = 0

		# If there was no opportunity for a comeback
		else:
			comeback_opportunities[i] = 0
			successful_comebacks[i] = 0

	# Compute sum of comeback opportunities per game
	sum_comeback_opp = [sum(comeback_opportunities[:i]) for i in range(len(comeback_opportunities))][n:]
	sum_comeback_opp.append(sum(comeback_opportunities))

	# Compute sum of successful comebacks per game
	sum_successful_comebacks = [sum(successful_comebacks[:i]) for i in range(len(successful_comebacks))][n:]
	sum_successful_comebacks.append(sum(successful_comebacks))

	comeback_stats = np.empty(len(season))

	for i in range(len(sum_comeback_opp)):
		# If the team has had opportunites to come back
		if sum_comeback_opp[i] > 0:
			comeback_stats[i] = sum_successful_comebacks[i] / sum_comeback_opp[i]

		# If the team has never been losing at the start of the 4th quarter
		else:
			comeback_stats[i] = 1

	# Resize and assign correct values
	comeback_record = comeback_stats[:-(n-1)]
	for i in range(len(comeback_record)):
		comeback_record[i] = comeback_stats[i]

	return comeback_record

# This function computes a team's record vs the spread as a fraction
def computeRecordVsSpread(season, n):
		record_vs_spread = np.empty(len(season))
		buf = np.empty(len(season))
	
		for i,game in enumerate(season.tolist()):
			team = game[0]
			score_diff = float(game[1]) - float(game[2])
			spread = game[3].split()
			record_vs_spread[i] = resultVsSpread(team, score_diff, spread)

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
def resultVsSpread(team, score_diff, spread):
	'''compute the result vs spread for a given team, score_diff, and spread'''
	if spread != ['Pick']:
		spread_team = ''.join(spread[:-1])
		spread = float(spread[-1])

		# If spread uses this team
		if spread_team == team.replace(' ', ''):
			# If team beat the spread
			if score_diff + spread > 0:
				return 1
			else:
				return 0
			
		# If spread uses opp_team
		else:
			# If team beat the spread
			if score_diff - spread > 0:
				return 1
			else:
				return 0

	# If spread is Pick
	else:
		# team beat the spread
		if score_diff > 0:
			return 1
		else:
			return 0