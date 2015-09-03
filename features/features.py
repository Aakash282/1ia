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
    start_time = time.clock()
    # the -1 is because I like to use my computer while running things
    num_cores = min((stop - start) + 1, multiprocessing.cpu_count() - 1)
    # to ensure that at least one core is being used
    num_cores = max(num_cores, 1)
    Parallel(n_jobs = num_cores)(delayed(feature_set)(x, x) for x in range(start, stop + 1))
    print 'Ellapsed time', time.clock() - start_time, 'Using %i core(s)' %num_cores
    
def feature_set(start, stop):
    season_table = {}
    DVOA = load.getDVOA()
    for i in range(start, stop+1):
        season_table[i] = load.loadYear(i)
        df = pd.DataFrame()
        league_data = load.getYearData(i)
        for idx, row in league_data.iterrows():
            DVOA_table = TFns.filter_table(DVOA, 'year', i)
            temp_game = game.game(row['home_team'], row['away_team'], season_table[i],\
                             DVOA_table, str(row['week year']) + ' ' + str(i), \
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
            #print output.values
        df.to_csv(os.path.expanduser('~') + '/FSA/data/NNinput/features%d.csv' % i, index = False)
        