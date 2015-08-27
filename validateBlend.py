import pandas as pd
from sklearn import ensemble
from sklearn import dummy as dum
import sklearn.tree as sk
from sklearn import metrics
import numpy as np
from matplotlib import pyplot as plt
from NN import bpnn

middle = 0

def compare(l1, l2):
    if len(l1) != len(l2):
        print 'prediction list wrong size'
        exit()
    else: 
        err_count = 0
        for i in range(len(l1)):
            if l1[i] < middle: answer = -1
            else: answer = 1
            if l2[i] < middle: actual = -1
            else: actual = 1
            if answer != actual:
                err_count += 1

        return float(err_count) / len(l1)

def falseNegative(l1, l2):
    if len(l1) != len(l2):
        print 'prediction list wrong size'
        exit()
    else: 
        err_count = 0
        total = 0
        for i in range(len(l1)):
            if l2[i] > middle: 
                total += 1 
                if l1[i] < middle: answer = -1
                else: answer = 1
                if l2[i] < middle: actual = -1
                else: actual = 1
                if answer != actual:
                    err_count += 1
        return float(err_count) / total

def falsePositive(l1, l2):
    if len(l1) != len(l2):
        print 'prediction list wrong size'
        exit()
    else: 
        err_count = 0
        total = 0
        for i in range(len(l1)):
            if l2[i] < middle: 
                total += 1
                if l1[i] < middle: answer = -1
                else: answer = 1
                if l2[i] < middle: actual = -1
                else: actual = 1
                if answer != actual:
                    err_count += 1
        return float(err_count) / total

def confusionMatrix(l1, l2):
    if len(l1) != len(l2):
        print 'size mismatch'
        exit()
    else:
        conf = [0,0,0,0]
        for i in range(len(l1)):
            if l1[i] < middle: answer = -1
            else: answer = 1
            if l2[i] < middle: actual = -1
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



if __name__ == "__main__":
    datadir = os.path.expanduser('~') + '/FSA/data/NNinput/'
    df_train = pd.DataFrame.from_csv(datadir + "training_set.csv")
    df_test = pd.DataFrame.from_csv(datadir + "testing_set.csv")
    holdout = []
    feature_cols = [col for col in df_train.columns if col not in holdout]
    test_cols = [col for col in df_train.columns if col in ['score diff']]
    y_train = df_train[test_cols]
    y_test = df_test[test_cols]
    y_pred = []
    with open(datadir[:-8] + 'trainBlend.csv', 'r') as f: 
        data = f.readlines()
        for i in range(len(data)):
            y_pred.append(float(data[i].strip()))

    y_train = y_train.values.T.tolist()[0]
    print "TRAINING SET RESULTS"
    print "training error: ", compare(y_pred, y_train)
    print "false positive: ", falsePositive(y_pred, y_train)
    print "false negative: ", falseNegative(y_pred, y_train)
    print "--------------"
    conf = confusionMatrix(y_pred, y_train)

    print 'confusion matrix: '
    print "actual\t\taway\thome"
    print "predicted away\t%d\t%d" % (conf[0], conf[1])
    print "predicted home\t%d\t%d" % (conf[2], conf[3])
    print "#################################"

    y_pred = []
    with open(datadir[:-8] + 'testBlend.csv', 'r') as f: 
        data = f.readlines()
        for i in range(len(data)):
            y_pred.append(float(data[i].strip()))

    y_test = y_test.values.T.tolist()[0]
    print "TEST SET RESULTS"
    print "predictive error: ", compare(y_pred, y_test)
    print "false positive: ", falsePositive(y_pred, y_test)
    print "false negative: ", falseNegative(y_pred, y_test)
    
    conf = confusionMatrix(y_pred, y_test)
    print "--------------"
    print 'confusion matrix: '
    print "actual\t\taway\thome"
    print "predicted away\t%d\t%d" % (conf[0], conf[1])
    print "predicted home\t%d\t%d" % (conf[2], conf[3])

    plt.title("Blended Regression Predictions")
    plt.xlabel("Prediction")
    plt.ylabel("Prediction Frequency")
    plt.hist(y_pred, 100, normed=True)
    plt.show()