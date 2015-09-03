# RF.py 
# this file is a handle for random forest regressors

from sklearn import ensemble
from sklearn import dummy as dum
import sklearn.tree as sk
from sklearn import metrics
from sklearn.svm import SVR
import sklearn


def trainModel(n, x, y):
    rf = ensemble.RandomForestRegressor(n_estimators=n)
    rf.fit(x, y.values.T.tolist()[0])
    return rf