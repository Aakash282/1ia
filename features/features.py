import os
import sys
import numpy as np
import pandas as pd
import multiprocessing
from joblib import Parallel, delayed
from timeit import default_timer

from dataIO import loadData
from lib import movingMedian
import game


def get_feature_set(start, stop):
    '''parallelized version of feature_set'''
    start_time = default_timer()
    # the -1 is because I like to use my computer while running things
    num_cores = min((stop - start) + 1, multiprocessing.cpu_count() - 1)
    # to ensure that at least one core is being used
    num_cores = max(num_cores, 1)

    Parallel(n_jobs = num_cores)(delayed(feature_set)(x) for x in range(start, stop + 1))
    print 'Ellapsed time', default_timer() - start_time, 'Using %i core(s)' %num_cores

def extractFeatures(team, week, year):
    try:
        year_features = loadData.getTeamFeatures(year, team)
        features = year_features.loc[float(week)].to_dict()
        return features
    except:
        return {'':None}

def feature_set(year):
    DVOA = loadData.getDVOA()
    season_table = loadData.loadYear(year)
    league_data = loadData.getYearData(year)
    outputs = []
    for idx, row in league_data.iterrows():
        week_year = str(row['week year'])
        home_features = extractFeatures(row['home_team'].strip(), week_year, year)
        away_features = extractFeatures(row['away_team'].strip(), week_year, year)


        temp_game = game.game(row['home_team'], row['away_team'], season_table,\
                         home_features, away_features, week_year + ' ' + str(year), \
                         row['Roof'], row['time_of_day_(ET)'])

        # Adjust this to change the length of the moving average #FuckMagicNumbers #GlenGeorgeRuinedMe
        movingAvgLength = 3
        temp_features = temp_game.get_features(movingAvgLength)

        if None in temp_features['away'].values() or None in temp_features['home'].values():
            continue
        score_diff = temp_features['home']['score'] - temp_features['away']['score']
        feature_lst = temp_features['away'].values() + temp_features['home'].values() + \
                      [score_diff] + temp_features['game'].values() + [week_year]
        outputs.append(feature_lst)

    header = ['away ' + x for x in temp_features['away']] + \
             ['home ' + x for x in temp_features['away']] + ['score diff', 'spread', 'roof', 'timeofgame', 'week_year']
    output_file = os.path.expanduser('~') + '/FSA/data/FeaturesByYear/features%d.csv' % year
    np.savetxt(output_file, np.array(outputs), delimiter=',', fmt="%s", header=','.join(header))
