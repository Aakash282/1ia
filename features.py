import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dataIO import tableFns as TFns
from dataIO import loadRaw as load

class game:
    '''The idea behind this class is to be able to make a prediction for a 
    possible game that may occur in the future'''
    def __init__(self, home_team, away_team, week_year, field):
        
        self.home = home_team
        self.away = away_team
        self.field = field
        if len(week_year) > 2:
            self.week = int(week_year.split(' ')[0])
            self.year = int(week_year.split(' ')[1])
        else:
            print 'improper time field format!'
    
    def get_stats(self, n):
        home_table = load.getTeamData(self.year, self.home)
        away_table = load.getTeamData(self.year, self.away)
        home_stats = TFns.get_previous_stats(home_table, self.week, n)
        away_stats = TFns.get_previous_stats(away_table, self.week, n)
        return {'home stats': home_stats, 'away stats': away_stats}

    def get_features(self, n):
        stats = get_stats(self, n)
        home_stats = stats['home stats']
        away_stats = stats['away stats']
        features_home = compute_features({}, home_stats)
        features_away = compute_features({}, away_stats)
        #compute features here.  This is currently just an example
        #would probably want a dictionary of different features
        
        
    def compute_features(self, feature_dict, stats):
        '''to be finished later'''
        feature_dict['rush'] = rush_feature(self, stats)
        return feature_dict
    
    def rush_feature(self, stats):
        league_data = load.getYearData(self.year)
        league_rush = np.append(league_data['ht_rush_yards'] + league_data['at_rush_yards'])
        return (stats['rush_yards'].values - league_rush.mean())/league_rush.std()
    