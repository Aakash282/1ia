# ensemble.py

from models.sk_RF import sk_RF
from models.sk_GBR import sk_GBR
from models.sk_SVM import sk_SVM

from models.h2o_RF import h2o_RF
from models.h2o_DL import h2o_DL

import simpleBlend as blender
import validate as val
import validateMoneyLine as moneyline

class Ensemble:
    def __init__(self):
        print 'Initiating Ensemble'
        # a list of model instances
        self.models = []

        # a list of predictions from each of the corresponding models above
        self.preds = []
        self.blended_results = []
        self.numModels = 0

    def addSKRF(self, params):
        self.models.append(sk_RF(self.numModels, params))
        self.numModels += 1

    def addSKGBR(self, params):
        self.models.append(sk_GBR(self.numModels, params))
        self.numModels += 1

    def addSKSVM(self, params):
        self.models.append(sk_SVM(self.numModels, params))
        self.numModels += 1

    def addh2oRF(self, params):
        self.models.append(h2o_RF(self.numModels, params))
        self.numModels += 1

    def addh2oDL(self, params):
        self.models.append(h2o_DL(self.numModels, params))
        self.numModels += 1

    def train(self, x, y):
        print "###########################"
        print "Training all models"
        y = y.values.T.tolist()[0]
        for m in self.models:
            m.train(x, y)
            print "Finished training model %s" % m.name
        self.preds = []
        print "###########################"

    def predict(self, x, train=True):
        # clear out the current predictions and predict from each model
        self.preds = [m.predict(x, train) for m in self.models]

    def blend(self):
        # blend all results in self.preds together
        self.blended_results = blender.blend(self.preds)
        return self.blended_results

    def validate(self, actual, spread, test, moneyline):
        if moneyline: 
            if test:
                return moneyline.testError(self.blended_results, actual, spread)
            else:
                moneyline.trainError(self.blended_results, actual, spread)
        else:
            if test:
                return val.testError(self.blended_results, actual, spread)
            else:
                val.trainError(self.blended_results, actual, spread)            

