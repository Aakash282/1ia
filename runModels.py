# runModels.py 
# This file runs all models and then runs the appropriate 
# functions to blend and validate the predictions. 
# Only run this after running makeDatasets.py

import ensemble.validate as val 
import ensemble.simpleBlend as blender
import pandas as pd 
from matplotlib import pyplot as plt 
import numpy as np 
import os
import ensemble.models.RF as RF
import ensemble.models.GBR as GBR
import ensemble.models.SVM as SVM
from sklearn import ensemble


def importData(training=1):
    datadir = os.getcwd().strip('1ia') + 'data/NNinput/'
    if training: 
        return pd.DataFrame.from_csv(datadir + 'training_set.csv')
    else: 
        return pd.DataFrame.from_csv(datadir + 'testing_set.csv')

if __name__ == "__main__":
    df_train = importData()
    df_test = importData(0)

    ######################
    # TRAIN ON SPREAD????#
    ######################
    spread = True

    holdout = ['score diff', 'home score', 'away score']
    if not spread: 
        print 'hi'
        holdout.append('spread')

    feature_cols = [col for col in df_train.columns if col not in holdout]
    test_cols = [col for col in df_train.columns if col in ['score diff']]
    x_train = df_train[feature_cols]
    y_train = df_train[test_cols]
    train_spread = df_train[['spread']]
    x_test = df_test[feature_cols]
    y_test = df_test[test_cols]
    test_spread = df_test[['spread']]

    models = [RF.trainModel(10, x_train, y_train) for i in range(10)]
    models += [GBR.trainModel(100, .1, x_train, y_train) for i in range(10)]
    models += [SVM.trainModel(x_train, y_train)]

    trainPreds = [m.predict(x_train) for m in models]
    testPreds = [m.predict(x_test) for m in models]


    trainPreds = blender.blend(trainPreds)
    testPreds = blender.blend(testPreds)

    val.trainError(trainPreds, y_train, train_spread)
    val.plotHist(trainPreds, y_train, train_spread)
    print '#################################'
    val.testError(testPreds, y_test, test_spread)
    val.plotHist(testPreds, y_test, test_spread)
    

