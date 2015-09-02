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
import sklearn
eps = 0
amp = 1.0
def compare(l1, l2, l3):
    if len(l1) != len(l2) and len(l2) != len(l3):
        print 'prediction list wrong size'
        exit()
    else: 
        err_count = 0
        total = 0
        for i in range(len(l1)):
            if abs(l1[i] - l3[i]) < eps: continue
            # if abs(l1[i]) < 1.0: continue
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
                # if abs(l1[i]) < 1.0: continue
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
                # if abs(l1[i]) < 1.0: continue
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
            # if abs(l1[i]) < 1.0: continue
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

def fit(val):
    # val += 18
    if val < 1 and val > 0:
        return 1.1
    if val < 0 and val > -1:
        return -1.1
    if val < 3 and val > 1.5:
        return 3.1
    if val < -1.5 and val > -3: 
        return -3.1
    if val < 8 and val > 6:
        return 7.1
    if val < -6 and val > -8: 
        return -7.1

    return round(amp*val)

if __name__ == "__main__":
    datadir = os.path.expanduser('~') + '/FSA/data/NNinput/'
    df_train = pd.DataFrame.from_csv(datadir + "training_set.csv")
    df_test = pd.DataFrame.from_csv(datadir + "testing_set.csv")
    holdout = ['score diff', 'home score', 'away score']# , 'spread']
    feature_cols = [col for col in df_train.columns if col not in holdout]
    test_cols = [col for col in df_train.columns if col in ['score diff']]
    x_train = df_train[feature_cols]
    y_train = df_train[test_cols]
    train_spread = df_train[['spread']]
    x_test = df_test[feature_cols]
    y_test = df_test[test_cols]
    test_spread = df_test[['spread']]
    y_pred = []

    # model5 = ensemble.RandomForestRegressor(n_estimators=10) #, max_depth=70)
    model1 = ensemble.GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
    model2 = ensemble.GradientBoostingRegressor(n_estimators=100, learning_rate=0.05)
    model3 = ensemble.GradientBoostingRegressor(n_estimators=150, learning_rate=0.2)
    model4 = sklearn.linear_model.Ridge()
    model5 = sklearn.linear_model.LinearRegression()
    model6 = ensemble.RandomForestRegressor(n_estimators=10)
    print x_train.shape, y_train.shape
    model1.fit(x_train, y_train.values.T.tolist()[0])
    model2.fit(x_train, y_train.values.T.tolist()[0])
    model3.fit(x_train, y_train.values.T.tolist()[0])
    model4.fit(x_train, y_train.values.T.tolist()[0])
    model5.fit(x_train, y_train.values.T.tolist()[0])
    model6.fit(x_train, y_train.values.T.tolist()[0])
    y1 = model1.predict(x_train)
    y2 = model2.predict(x_train)
    y3 = model3.predict(x_train)
    y4 = model4.predict(x_train)
    y5 = model5.predict(x_train)
    y6 = model6.predict(x_train)
    y_pred = [fit(np.mean([y1[i], y2[i], y3[i], y4[i], y5[i], y6[i]])) for i in range(len(y1))]
    print min(y_pred), max(y_pred), np.mean(y_pred)
    # y_pred = model.predict(x_train)
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
    y1 = model1.predict(x_test)
    y2 = model2.predict(x_test)
    y3 = model3.predict(x_test)
    y4 = model4.predict(x_test)
    y5 = model5.predict(x_test)
    y6 = model6.predict(x_test)
    y_pred = [fit(np.mean([y1[i], y2[i], y3[i], y4[i], y5[i], y6[i]])) for i in range(len(y1))]
    # y_pred = model.predict(x_test)
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

    print min(y_pred), max(y_pred), np.mean(y_pred)
    print min(y_test), max(y_test), np.mean(y_test)
    print x_train.values[y_pred.index(min(y_pred))]