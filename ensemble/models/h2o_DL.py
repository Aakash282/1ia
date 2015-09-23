# h2o_DL.py
# this file is a handle for
import os
import h2o
import pandas as pd
from pandas.util.testing import assert_frame_equal

from Model import Model

class h2o_DL(Model):
	'''inherits Model class and implements h2o distributed RF class'''
	def __init__(self, ID, params):
		Model.__init__(self, ID, params)
		h2o.init()

		datadir = os.path.expanduser('~') +'/FSA/data/'
		trainingFile = datadir + params[1][0]
		valFile = datadir + params[1][1]
		testingFile = datadir + params[1][2]


		self.trainData = h2o.import_file(path=trainingFile)
		self.valData = h2o.import_file(path=valFile)
		#self.valData = self.trainData
		self.testData = h2o.import_file(path=testingFile)

		# print self.trainData.col_names()
		# drop the invalid columns
		self.trainData = self.trainData.drop("away_score").drop("home_score")
		self.valData = self.valData.drop("away_score").drop("home_score")
		self.testData = self.testData.drop("away_score").drop("home_score")

		self.params = params

		if self.params[0] == False:
			self.trainData = self.trainData.drop('spread')
			# self.valData   = self.valData.drop('spread')
			self.testData  = self.testData.drop('spread')

		# for h2o, creating the model is the same as training the model so
		# need to hold of here
		self.model = None

	def train(self, x, y):
		self.model = h2o.deeplearning(x = self.trainData.drop('score diff'),
			                           y = self.trainData['score diff'],
			                           validation_x = self.valData.drop('score diff'),
			                           validation_y = self.valData['score diff'],
			                           hidden=self.params[2],
			                           epochs=self.params[3],
			                           nfolds=self.params[4])

	def predict(self, x, train):
		# check if the input data is training or testing
		if train:
			return self.model.predict(self.trainData).as_data_frame(use_pandas=True).values.T.tolist()[0]
		else:
			return self.model.predict(self.testData).as_data_frame(use_pandas=True).values.T.tolist()[0]
