import pandas as pd
from sklearn import metrics
import numpy as np
from matplotlib import pyplot as plt
import math
import os

eps = 2

########################################################
# FOR ALL OF THE BELOW FUNCTIONS                       #
# l1 is the prediction list                            #
# l2 is the actual score difference                    #
# l3 is the spread                                     #
########################################################

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

def trainError(y_pred, y_train, train_spread):
    y_train = y_train.values.T.tolist()[0]
    train_spread = train_spread.values.T.tolist()[0]
    print "TRAINING SET RESULTS"
    print "training error: ", compare(y_pred, y_train, train_spread)
    print "false positive: ", falsePositive(y_pred, y_train, train_spread)
    print "false negative: ", falseNegative(y_pred, y_train, train_spread)
    print "bets made: ", bets_made(y_pred, y_train, train_spread)
    conf = confusionMatrix(y_pred, y_train, train_spread)
    print "--------------"
    print 'confusion matrix: '
    print "actual\t\taway\thome+"
    print "predicted away\t%d\t%d" % (conf[0], conf[1])
    print "predicted home+\t%d\t%d" % (conf[2], conf[3])
    print "###########################"

def testError(y_pred, y_test, test_spread):
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
    print "###########################"

def plotHist(l1, l2, l3):
    l2 = l2.values.T.tolist()[0]
    l3 = l3.values.T.tolist()[0]

    plt.title("Blended Regression Predictions")
    plt.xlabel("Prediction")
    plt.ylabel("Prediction Frequency")
    plt.hist(l1, 100, normed=True, color='b')
    plt.hist(l2, 200, normed=True, color='g')
    plt.hist(l3, 100, normed=True, color='r')
    plt.show()