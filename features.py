import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dataIO import tableFns as TFns
from dataIO import loadData as load
from movingMedian import RunningMedian

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

class game:
    '''The idea behind this class is to be able to make a prediction for a 
    possible game that may occur in the future'''
    def __init__(self, home_team, away_team, week_year):
        self.home = home_team.strip()
        self.away = away_team.strip()
        if len(week_year) > 2:
            self.week = int(week_year.split(' ')[0])
            self.year = int(week_year.split(' ')[1])
        else:
            print 'improper time field format!'

        self.season = load.loadYear(self.year)

    
    def get_stats(self, n):
        home_table = load.getTeamData(self.year, self.home)
        away_table = load.getTeamData(self.year, self.away)
        home_stats = TFns.get_previous_stats(home_table, self.week, n)
        away_stats = TFns.get_previous_stats(away_table, self.week, n)
        return {'home stats': home_stats, 'away stats': away_stats}

    def get_features(self, n):
        '''main use of this class... just call this and read the feature dict'''
        features_home = self.compute_features(1, n)
        features_away = self.compute_features(0, n)
        return {'home': features_home, 'away': features_away}
        
        
    def compute_features(self, home, n):
        '''input is a boolean for whether computing feature for home team. This 
        function simply makes calls to other feature computing functions'''
        features = {}
        features['rush'] = self.get_feature('rush_yards', home, n)
        features['pass'] = self.get_feature('pass_yards', home, n)
        features['first_downs'] = self.get_feature('first_downs', home, n)
        features['conv 3d'] = self.get_feature('3rd_down_converted', home, n)
        features['score'] = self.score(home)
        return features
    
    def get_feature(self, feature, home, n):
        '''compute the normalized moving-average of rush yards for given team'''
        avg = []
        weeks = pd.concat(self.season).groupby('week year')
        for idx, w in weeks:
            avg.append(np.mean(w[feature].values))
        
        if home: 
            givenTeam = self.home
        else: 
            givenTeam = self.away

        for team in self.season:
            if list(set(team['team']))[0].strip() == givenTeam:
                prev = []
                for idx, w in team.iterrows():
                    if np.mean(w['week year']) < self.week:
                        prev.append(w[feature])
                if len(prev) > n:
                    return np.mean(prev[-n:])
                else: 
                    return None 


    def score(self, home):
        '''get the score for the given team'''
        if home: 
            givenTeam = self.home
        else: 
            givenTeam = self.away
        for team in self.season:
            if list(set(team['team']))[0].strip() == givenTeam:
                for idx, w in team.iterrows():
                    if np.mean(w['week year']) == self.week:
                        return w['score']