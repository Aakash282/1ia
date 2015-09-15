# runModels.py 
# This file runs all models and then runs the appropriate 
# functions to blend and validate the predictions. 
# Only run this after running makeDatasets.py
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from ensemble.Ensemble import Ensemble
import pandas as pd 
import os


def importData(training=1):
    # Change the data dir if pulling from the normal set
    datadir = os.getcwd().strip('1ia') + 'data/TrainTestSynth/'
    if training: 
        return pd.DataFrame.from_csv(datadir + 'training_set.csv')
    else: 
        return pd.DataFrame.from_csv(datadir + 'testing_set.csv')

if __name__ == "__main__":
    df_train = importData()
    df_test = importData(0)

    files = ('TrainTestSynth/training_set.csv', 'TrainTestSynth/val_set.csv', 'TrainTestSynth/testing_set.csv')
    ######################
    # TRAIN ON SPREAD????#
    ######################
    spread = False

    holdout = ['score diff', 'home score', 'away score']
    if not spread: 
        holdout.append('spread')

    # Load the datasets into memory to hand of to the models
    feature_cols = [col for col in df_train.columns if col not in holdout]
    test_cols = [col for col in df_train.columns if col in ['score diff']]
    x_train = df_train[feature_cols]
    y_train = df_train[test_cols]
    train_spread = df_train[['spread']]
    x_test = df_test[feature_cols]
    y_test = df_test[test_cols]
    test_spread = df_test[['spread']]

    # print list(df_train.columns)

    # create an ensemble to start adding models
    ens = Ensemble()

    # add a SK Random Forests
    # ens.addSKRF([50])

    # add a SK Gradient Boosted Machine
    # ens.addSKGBR([150, .07])

    # add a SK SVM 
    # ens.addSKSVM([])

    # add an h2o RF
    ens.addh2oRF([True, files, 100, 150, 2])

    # add an h2o DL Network
    ens.addh2oDL([True, files, [150, 100], 150, 2])

    # train all models
    ens.train(x_train, y_train)

    # find training error
    ens.predict(x_train, train=True)
    a = ens.blend()
    ens.validate(y_train, train_spread, False)

    # predict on test set and compute error report
    ens.predict(x_test, train=False)
    b = ens.blend()
    ens.validate(y_test, test_spread, True)
    
    density = gaussian_kde(a)
    xs = np.linspace(-20, 20, 200)
    density.covariance_factor = lambda : .1
    density._compute_covariance()
    plt.plot(xs,density(xs))
    
    density = gaussian_kde(b)
    xs = np.linspace(-20, 20, 200)
    density.covariance_factor = lambda : .1
    density._compute_covariance()
    plt.plot(xs,density(xs))
    plt.show()    
