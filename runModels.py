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
import returns

def importData(training=1):
    # Change the data dir if pulling from the normal set
    datadir = os.getcwd().strip('1ia') + 'data/TrainTest/'
    if training:
        return pd.DataFrame.from_csv(datadir + 'training_set.csv')
    else:
        return pd.DataFrame.from_csv(datadir + 'testing_set.csv')


def create_ensemble():
    # create an ensemble to start adding models
    ens = Ensemble()

    # add a SK Random Forests
    ens.addSKRF([2])

    # add a SK Gradient Boosted Machine
    #ens.addSKGBR([150, .07])

    # add a SK SVM
    #ens.addSKSVM([])

    # add an h2o RF
    #ens.addh2oRF([True, files, 100, 150, 2])

    # add an h2o DL Network
    #ens.addh2oDL([True, files, [150, 100], 150, 2])

    return ens

def train(ens, x_train, y_train):
    # train all models
    ens.train(x_train, y_train)

def test(ens, x_train, y_train, train_spread, x_test, y_test, test_spread):
    # find training error
    plot = False
    # Currently moneyline is set to false.  Not sure how to set to true
    ens.predict(x_train, train=True)
    a = ens.blend()
    ens.validate(y_train, train_spread, False, False)
    
    ens.predict(x_test, train=False)
    b = ens.blend()
    c = ens.validate(y_test, test_spread, True, False)

    if plot:
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
    return c    
    
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

    X_train = df_train[feature_cols]
    Y_train = df_train[test_cols]
    train_spread = df_train[['spread']]
    X_test = df_test[feature_cols]
    Y_test = df_test[test_cols]
    test_spread = df_test[['spread']]

    ens = create_ensemble()
    train(ens, X_train, Y_train),
    results = []
    for week in set(df_train['week_year']):
        print 'week', week
        #plt.figure('week %d' %week)
        #plt.title(week)
        train_idx = X_train['week_year'] == week
        test_idx = X_test['week_year'] == week
        results.append(
            test(ens, X_train[train_idx], Y_train[train_idx], train_spread[train_idx],
                  X_test[test_idx], Y_test[test_idx], test_spread[test_idx]))
        
        #plt.legend(["actual", "predicted"])
    #plt.show()
    wins, losses = 0, 0
    for elem in results:
        print elem  
        wins += elem['wins']
        losses += elem['losses']
    print 'cumulative p', round(wins / float(wins + losses), 2)
    print 'percent return fixed:', \
          round((returns.returnsFromData(results, .4, True) - 1) * 100, 1)
    print 'percent return smartP:', \
          round((returns.returnsFromData(results, .4, False) - 1) * 100, 1)
    returns.pEstGraph(wins, losses)
    
    