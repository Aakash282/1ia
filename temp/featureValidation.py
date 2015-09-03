import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
sys.path.append(os.path.expanduser('~') + '/FSA/1ia/dataIO/' )
sys.path.append(os.path.expanduser('~') + '/FSA/1ia/lib/' )
import tableFns as TFns
import loadData as load
import multiprocessing 
from joblib import Parallel, delayed
import time
import loadData as load

for year in range(2001, 2015):
    features = load.getFeatures(year)
    for location in ['away ', 'home ', 'away opp_', 'home opp_']:
        for stat in [('3rd_down_attempts', '3rd_down_converted'), \
                     ('4th_down_attempts', '4th_down_converted'), \
                     ('fumbles', 'fumbles_lost'), \
                     ('rush_attempts', 'rush_TDs'), \
                     ('pass_attempt', 'pass_TDs'), \
                     ('pass_attempt', 'pass_comp')]:
            temp = features['%s%s'%(location, stat[0])] >= features['%s%s' %(location, stat[1])]
            if len(set(temp)) != 1:
                print len(set(temp))

    temp = features['home score'] - features['away score'] == features['score diff']    
    if len(set(temp)) != 1:
        print len(set(temp))

'''        
attempted > converted
1st > 3rd
fumbles > fumbles_lost
'''



