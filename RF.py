import pandas as pd
from sklearn import ensemble
from sklearn import dummy as dum
import sklearn.tree as sk
from sklearn import metrics
import numpy as np
from matplotlib import pyplot as plt
from NN import bpnn
import math
import os
from sklearn.svm import SVR

eps = 0

def compare(l1, l2, l3):
    if len(l1) != len(l2) and len(l2) != len(l3):
        print 'prediction list wrong size'
        exit()
    else: 
        err_count = 0
        total = 0
        for i in range(len(l1)):
            if abs(l1[i] - l3[i]) < eps: continue
            if abs(l1[i]) < 1.0: continue
            else: 
                total += 1
            if l1[i] < l3[i]: answer = -1
            else: answer = 1
            if l2[i] < l3[i]: actual = -1
            else: actual = 1
            if answer != actual:
                err_count += 1

        return float(err_count) / total

def falseNegative(l1, l2, l3):
    if len(l1) != len(l2):
        print 'prediction list wrong size'
        exit()
    else: 
        err_count = 0
        total = 0
        for i in range(len(l1)):
            
            if l2[i] > l3[i]: 
                if abs(l1[i] - l3[i]) < eps: continue
                if abs(l1[i]) < 1.0: continue
                total += 1 
                if l1[i] < l3[i]: answer = -1
                else: answer = 1
                if l2[i] < l3[i]: actual = -1
                else: actual = 1
                if answer != actual:
                    err_count += 1
        return float(err_count) / total

def falsePositive(l1, l2, l3):
    if len(l1) != len(l2):
        print 'prediction list wrong size'
        exit()
    else: 
        err_count = 0
        total = 0
        for i in range(len(l1)):
            if l2[i] < l3[i]: 
                if abs(l1[i] - l3[i]) < eps: continue
                if abs(l1[i]) < 1.0: continue
                total += 1
                if l1[i] < l3[i]: answer = -1
                else: answer = 1
                if l2[i] < l3[i]: actual = -1
                else: actual = 1
                if answer != actual:
                    err_count += 1
        return float(err_count) / total

def confusionMatrix(l1, l2, l3):
    if len(l1) != len(l2):
        print 'size mismatch'
        exit()
    else:
        conf = [0,0,0,0]
        for i in range(len(l1)):
            if abs(l1[i] - l3[i]) < eps: continue
            if abs(l1[i]) < 1.0: continue
            if l1[i] < l3[i]: answer = -1
            else: answer = 1
            if l2[i] < l3[i]: actual = -1
            else: actual = 1
            if actual == 1:
                if answer > 0.0:
                    conf[3] += 1
                else:
                    conf[1] += 1
            else: 
                if answer > 0.0:
                    conf[2] += 1
                else: 
                    conf[0] += 1
    return conf

def bets_made(l1, l2, l3):
    if len(l1) != len(l2) and len(l2) != len(l3):
        print 'prediction list wrong size'
        exit()
    else: 
        total = 0
        err_count = 0
        for i in range(len(l1)):
            if abs(l1[i] - l3[i]) < eps:
                # print "%f, %f, %f\n" % (l1[i], l2[i], l3[i])
                continue
            else: 
                total  += 1

    return total

if __name__ == "__main__":
    datadir = os.path.expanduser('~') + '/FSA/data/NNinput/'
    df_train = pd.DataFrame.from_csv(datadir + "training_set.csv")
    df_test = pd.DataFrame.from_csv(datadir + "testing_set.csv")
    holdout = ['score diff', 'home_score', 'away_score', 'spread']
    feature_cols = [col for col in df_train.columns if col not in holdout]
    test_cols = [col for col in df_train.columns if col in ['score diff']]
    x_train = df_train[feature_cols]
    y_train = df_train[test_cols]
    train_spread = df_train[['spread']]
    x_test = df_test[feature_cols]
    y_test = df_test[test_cols]
    test_spread = df_test[['spread']]
    y_pred = []
    with open(datadir[:-8] + 'trainBlend.csv', 'r') as f: 
        data = f.readlines()
        for i in range(1, len(data)):
            y_pred.append(float(data[i].strip()))

    model = ensemble.RandomForestRegressor(n_estimators=50)
    print x_train.shape, y_train.shape
    model.fit(x_train, y_train.values.T.tolist()[0])
    y_pred = model.predict(x_train)
    y_train = y_train.values.T.tolist()[0]
    train_spread = train_spread.values.T.tolist()[0]
    print "TRAINING SET RESULTS"
    print "training error: ", compare(y_pred, y_train, train_spread)
    print "false positive: ", falsePositive(y_pred, y_train, train_spread)
    print "false negative: ", falseNegative(y_pred, y_train, train_spread)
    print "bets made: ", bets_made(y_pred, y_train, train_spread)
    print "--------------"
    conf = confusionMatrix(y_pred, y_train, train_spread)

    print 'confusion matrix: '
    print "actual\t\taway\thome"
    print "predicted away\t%d\t%d" % (conf[0], conf[1])
    print "predicted home\t%d\t%d" % (conf[2], conf[3])
    print "#################################"

    y_pred = []
    with open(datadir[:-8] + 'testBlend.csv', 'r') as f: 
        data = f.readlines()
        for i in range(1, len(data)):
            y_pred.append(float(data[i].strip()))
    y_pred = model.predict(x_test)
    y_test = y_test.values.T.tolist()[0]
    test_spread = test_spread.values.T.tolist()[0]
    print "TEST SET RESULTS"
    print "predictive error: ", compare(y_pred, y_test, test_spread)
    print "false positive: ", falsePositive(y_pred, y_test, test_spread)
    print "false negative: ", falseNegative(y_pred, y_test, test_spread)
    print "bets made: ", bets_made(y_pred, y_test, test_spread)
    
    conf = confusionMatrix(y_pred, y_test, test_spread)
    print "--------------"
    print 'confusion matrix: '
    print "actual\t\taway\thome"
    print "predicted away\t%d\t%d" % (conf[0], conf[1])
    print "predicted home\t%d\t%d" % (conf[2], conf[3])

    plt.title("Blended Regression Predictions")
    plt.xlabel("Prediction")
    plt.ylabel("Prediction Frequency")
    plt.hist(y_pred, 100, normed=True, color='b')
    plt.hist(y_test, 100, normed=True, color='g')
    plt.hist(test_spread, 100, normed=True, color='r')
    plt.show()