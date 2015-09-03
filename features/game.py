import os
import sys
import numpy as np
import pandas as pd
sys.path.append(os.path.expanduser('~') + '/FSA/1ia/dataIO/' )
sys.path.append(os.path.expanduser('~') + '/FSA/1ia/lib/' )
import tableFns as TFns
import loadData as load

class game:
    '''The idea behind this class is to be able to make a prediction for a 
    possible game that may occur in the future'''
    def __init__(self, home_team, away_team, season, week_year, roof, time):
        self.home = home_team.strip()
        self.away = away_team.strip()
        if len(week_year) > 2:
            self.week = int(week_year.split(' ')[0])
            self.year = int(week_year.split(' ')[1])
        else:
            print 'improper time field format!'

        self.roof = roof
        self.time = time
        self.season = season

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
        feature_list = list(self.season[self.home].keys())
        #remove_list = feature_list[0:7] + ['attendance', 'home_field?', 'Surface']
        remove_list = []
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

        team = self.season[givenTeam]
        prev = []
        for idx, w in team.iterrows():
            if np.mean(w['week year']) < self.week:
                if 'TOP' in feature:
                    prev.append(self.timeOfPossession(feature, w))
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
        team = self.season[givenTeam]
        for idx, w in team.iterrows():
                    if np.mean(w['week year']) == self.week:
                        return w['score']

    def spread(self):
        givenTeam = self.home
        team = self.season[givenTeam]

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

    def timeOfPossession(self, feature, w):
        top = w['TOP']
        minutes, seconds = top.split(':')
        top = float(minutes) + float(seconds) / 60.0
        oppTop = w['opp_TOP']
        minutes, seconds = oppTop.split(':')
        oppTop = float(minutes) + float(seconds) / 60.0
        if 'opp' in feature:
            return oppTop / (top + oppTop)
        return top / (top + oppTop)
    
    def winLoss(self, home):
        '''Returns the current record of a team for a given game.  W/L vals
        are normalized to 1, so 1-0 has the same record as 2-0.  This should
        be changed in the future to better reflect a team's performance'''
        if home:
            team = self.home
        else:
            team = self.away
            
        home_table = self.season[team]
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
        ''' converts time of the game to minutes after midnight''' 
        if 'pm' in self.time:
            time = 12 * 60
        elif 'am' in self.time:
            time = 0
        timeStr = self.time[0:len(self.time) - 2]
        time += int(timeStr.split(':')[0]) * 60 + int(timeStr.split(':')[1])
        return time
