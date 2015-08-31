import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dataIO import tableFns as TFns
from dataIO import loadData as load
from movingMedian import RunningMedian
from dataIO import loadRaw as ld

global season_table
season_table = {}

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

class game:
    '''The idea behind this class is to be able to make a prediction for a 
    possible game that may occur in the future'''
    def __init__(self, home_team, away_team, week_year, roof, time):
        self.home = home_team.strip()
        self.away = away_team.strip()
        if len(week_year) > 2:
            self.week = int(week_year.split(' ')[0])
            self.year = int(week_year.split(' ')[1])
        else:
            print 'improper time field format!'

        self.roof = roof
        self.time = time
        if 'season_table[self.year]' not in globals():
            season_table[self.year] = load.loadYear(self.year) 
        self.season = season_table[self.year]

    
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
        features_game = self.compute_game_features(n)
        return {'home': features_home, 'away': features_away, 'game': features_game}
        
        
    def compute_features(self, home, n):
        '''input is a boolean for whether computing feature for home team. This 
        function simply makes calls to other feature computing functions'''
        features = {}
        feature_list = list(self.season[0].keys())
        remove_list = feature_list[0:7] + ['attendance', 'home_field?', 'Surface']
        for elem in feature_list:
            if 'ref' in elem or 'score' in elem:
                remove_list.append(elem)
        for elem in remove_list:
            feature_list.remove(elem)
        for elem in feature_list:
            elem = elem.strip()
            features[elem] = self.get_feature(elem, home, n)

        features['score'] = self.score(home)
        win_loss = self.winLoss(home)
        features['wins'], features['losses']  = win_loss['wins'], win_loss['losses']
        features['streak'] = win_loss['streak']
        return features

    def compute_game_features(self, n):
        features = {}
        features['spread'] = self.spread()
        features['roof'] = self.getRoof()
        features['time'] = self.getTime()
        return features
    
    def get_feature(self, feature, home, n):
        '''compute the normalized moving-average of a feature for given team'''
        weeks = pd.concat(self.season).groupby('week year')
        
        if home: 
            givenTeam = self.home
        else: 
            givenTeam = self.away

        for team in self.season:
            if list(set(team['team']))[0].strip() == givenTeam:
                prev = []
                for idx, w in team.iterrows():
                    if np.mean(w['week year']) < self.week:
                        if 'TOP' in feature:
                            prev.append(self.timeOfPossession(w))
                        else:
                            prev.append(w[feature])
                    else: 
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

    def spread(self):
        givenTeam = self.home
        for team in self.season:
            if list(set(team['team']))[0].strip() == givenTeam:
                for idx, w in team.iterrows():
                    if np.mean(w['week year']) == self.week:
                        spread = w['spread']
                        if spread == 'Pick':
                            return 0.0
                        else:
                            favorite,points = spread.split("-")
                            favorite = favorite.strip(" ")
                            if favorite == givenTeam:
                                return float(points)
                            else:
                                return (float(points) * -1.0)

    def timeOfPossession(self, w):
        top = w['TOP']
        minutes, seconds = top.split(':')
        top = float(minutes) + float(seconds) / 60.0
        oppTop = w['opp_TOP']
        minutes, seconds = oppTop.split(':')
        oppTop = float(minutes) + float(seconds) / 60.0
        return top / (top + oppTop)
    
    def winLoss(self, home):
        table = pd.DataFrame()
        for team in self.season:
            table = pd.DataFrame.append(table, team)
        if home:
            team = self.home
        else:
            team = self.away
            
        home_table = TFns.filter_table(table, 'team', team + ' ')
        home_table = TFns.get_previous_stats(home_table, self.week, 17)
        if type(home_table) == type(None):
            return {'wins': 0.0, 'losses': 0.0, 'streak': 0.0}
        home_counts = pd.Series.value_counts(home_table['score'] > home_table['opp_score'])
        home_counts = home_counts.to_dict()
        if len( home_counts.keys() ) == 1:
            if home_counts.keys()[0]:
                home_wins = 1
                home_losses = 0
            elif not home_counts.keys()[0]:
                home_losses = 1
                home_wins = 0
        else:
            home_wins = home_counts[True]
            home_losses = home_counts[False]
        normalize = float(home_wins + home_losses)
        streak = self.getStreak(home_table)
        return {'wins': home_wins / normalize, 'losses': home_losses / normalize, 'streak': streak }

    def getStreak(self, table):
        streak = 0
        results = table['score'] > table['opp_score']
        length = len(results)
        last = results[length-1]
        for i in range(length):
            if results[length-1-i] == last and last:
                streak += 1
            elif results[length-1-i] == last and not last:
                streak -= 1
            else:
                break
        return float(streak)

    def getRoof(self):
        if self.roof == 'outdoors':
            return 1
        return 0
    
    def getTime(self):
        if 'pm' in self.time:
            time = 12 * 60
        elif 'am' in self.time:
            time = 0
        timeStr = self.time[0:len(self.time) - 2]
        time += int(timeStr.split(':')[0]) * 60 + int(timeStr.split(':')[1])
        return time

def feature_set(start, stop):
    for i in range(start, stop+1):
        df = pd.DataFrame()
        league_data = load.getYearData(i)
        for idx, row in league_data.iterrows():
            temp_game = game(row['home_team'], row['away_team'], str(row['week year']) + ' ' + str(i), \
                             row['Roof'], row['time_of_day_(ET)'])
            # Adjust this to change the length of the moving average #FuckMagicNumbers #GlenGeorgeRuinedMe
            movingAvgLength = 3
            temp_features = temp_game.get_features(movingAvgLength)
            if None in temp_features['away'].values() or \
               None in temp_features['home'].values():
                continue
            away = pd.DataFrame.from_dict(data = temp_features['away'], orient = 'index')
            home = pd.DataFrame.from_dict(data = temp_features['home'], orient = 'index')
            score_diff = {'score diff': temp_features['home']['score'] - temp_features['away']['score']}
            game_features = pd.DataFrame.from_dict(data = temp_features['game'], orient = 'index')
            score_diff = pd.DataFrame.from_dict(data = score_diff, orient = 'index')
            output = pd.DataFrame.append(away, home, ignore_index = True)
            output = pd.DataFrame.append(output, score_diff, ignore_index = True)
            output = pd.DataFrame.append(output, game_features, ignore_index = True).transpose()
            columns = ['away ' + x for x in temp_features['away']] + \
                ['home ' + x for x in temp_features['away']] + ['score diff', 'spread', 'roof', 'timeofgame']
            output.columns = columns
            df = pd.DataFrame.append(df, output)
            print output.values
        df.to_csv(ld.getPath() + '/data/NNinput/features%d.csv' % i, index = False)
        