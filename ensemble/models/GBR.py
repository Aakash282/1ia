# GBR.py
# this file is a handle for gradient boosted regressors

from sklearn import ensemble
from sklearn import dummy as dum
import sklearn.tree as sk
from sklearn import metrics
from sklearn.svm import SVR
import sklearn

# n is number of estimators, l is learning rate
def trainModel(n, l, x, y):
    m = ensemble.GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
    m.fit(x, y.values.T.tolist()[0])
    return m