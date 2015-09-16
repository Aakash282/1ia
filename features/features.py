import os
import sys
import numpy as np
import pandas as pd
sys.path.append(os.path.expanduser('~') + '/FSA/1ia/dataIO/' )
sys.path.append(os.path.expanduser('~') + '/FSA/1ia/lib/' )
import tableFns as TFns
import loadData as load
import game
import multiprocessing 
from joblib import Parallel, delayed
import time

def get_feature_set(start, stop):
    '''parallelized version of feature_set'''
    start_time = time.time()
    # the -1 is because I like to use my computer while running things
    num_cores = min((stop - start) + 1, multiprocessing.cpu_count() - 1)
    # to ensure that at least one core is being used
    num_cores = max(num_cores, 1)
    Parallel(n_jobs = num_cores)(delayed(feature_set)(x, x) for x in range(start, stop + 1))
    print 'Ellapsed time', (time.time() - start_time) / 60.0, 'minutes Using %i core(s)' %num_cores

def extractFeatures(team, week, year):
    try:
        year_features = load.getTeamFeatures(year, team)
        features = year_features.loc[float(week)].to_dict()
        return features
    except:
        return {'':None}

def feature_set(start, stop):
    season_table = {}
    DVOA = load.getDVOA()
    for i in range(start, stop+1):
        season_table[i] = load.loadYear(i)
        df = pd.DataFrame()
        league_data = load.getYearData(i)
        for idx, row in league_data.iterrows():
            week_year = str(row['week year'])
            home_features = extractFeatures(row['home_team'].strip(), week_year, i)
            away_features = extractFeatures(row['away_team'].strip(), week_year, i)

            temp_game = game.game(row['home_team'], row['away_team'], season_table[i],\
                             home_features, away_features, week_year + ' ' + str(i), \
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
            # print output.values
        added_columns = [('3rd_down_conv%', '3rd_down_converted', '3rd_down_attempts'), \
                         ('4th_down_conv%', '4th_down_converted', '4th_down_attempts'), 
                         ('yards_play', 'total_yards', 'total_plays'),
                         ('yards_carry', 'rush_yards', 'rush_attempts'),
                         ('yards_throw', 'pass_yards', 'pass_attempt'),
                         ('yards_comp', 'pass_yards', 'pass_comp'),
                         ('pass_comp%', 'pass_comp', 'pass_attempt'),
                         ('rush yards%', 'rush_yards', 'total_yards'),
                         # PassTD/Int might be too noisy?
                         ('PassTD/INT', 'pass_TDs', 'INT')]
        df = add_div_features(df, added_columns)
        df.to_csv(os.path.expanduser('~') + '/FSA/data/FeaturesByYear/features%d.csv' % i, index = False)

def divide_features(table, feature_name, feature_numerator, feature_divisor):
    for elem in ['away ', 'home ', 'away opp_', 'home opp_']:
        table[elem + feature_name] = table[elem + feature_numerator] / table[elem + feature_divisor]
        vals = []
        for item in table[elem + feature_name].values:
            if not np.isfinite(item) or np.isnan(item):
                vals.append(0.5)
            else:
                vals.append(item)
        table[elem + feature_name] = np.array(vals)
    return table
            
def add_div_features(table, div_list):
    # div list is a list of tuples
    for elem in div_list:
        table = divide_features(table, elem[0], elem[1], elem[2])
    return table    
    
    
    