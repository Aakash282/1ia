# h2o_RF.py
# this file is a handle for 
import os
import h2o
import pandas as pd


class h2o_RF(Model):
	'''inherits Model class and implements h2o distributed RF class'''
	def __init__(self, ID, params):
		h2o.init()
		datadir = os.path.expanduser('~') +'/FSA/data/TrainTest/'
		trainingFile = datadir + 'training_set.csv'
		testingFile = datadir + 'testing_set.csv'

		self.trainData = h2o.import_frame(path=trainingFile)
		self.testData = h2o.import_frame(path=testingFile)

		self.model = None

		params
	def train(self, x, y):
		self.model = h2o.random_forest(x = self.trainData.drop('score diff'),
			                           y = self.trainData['score diff'],
			                           ntrees=params[0],
			                           max_depth=params[1],
			                           nfolds=params[2])

	# def predict(self, )