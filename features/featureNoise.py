'''Takes the current feature data and adds noise to each element to create
fake data in attempt to prevent overfitting and adds it to the noise-free
set'''
import os
import sys
import numpy as np
import pandas as pd
sys.path.append(os.path.expanduser('~') + '/FSA/1ia/dataIO/' )
sys.path.append(os.path.expanduser('~') + '/FSA/1ia/lib/' )
import loadData as load
import time
import random as rand


def synth(n):
    fakeSets = n
    features = pd.DataFrame()
    for year in range(2001, 2015):
        print year
        features = load.getFeatures(year)
        combinedOutput = pd.DataFrame()
        for elem in range(fakeSets):
            tempTable = features
            featureList = list(tempTable.keys())
            featureList.remove('spread')
            for key in featureList:
                # The noise is added in here
                tempTable[key] *= 1 + (rand.random() - 0.5) / 5.0
            combinedOutput = pd.DataFrame.append(combinedOutput, tempTable)
        combinedOutput = pd.DataFrame.append(combinedOutput, features)
        combinedOutput.to_csv(os.path.expanduser('~') + \
                '/FSA/data/FeaturesSynth/featuresSynth%d.csv' % year, index = False)