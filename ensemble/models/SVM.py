# SVM.py
# this file is a handle for support vector regressors

from sklearn import ensemble
from sklearn import dummy as dum
import sklearn.tree as sk
from sklearn import metrics
from sklearn.svm import SVR
import sklearn

def trainModel(x, y):
    m = SVR(kernel='rbf')
    m.fit(x, y.values.T.tolist()[0])
    return m