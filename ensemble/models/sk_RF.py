# sk_RF.py

from Model import Model
from sklearn import ensemble

class sk_RF(Model):
	'''inherits Model class and implements sklearns RandomForestRegressor class'''
	def __init__(self, ID, params):
		Model.__init__(self, ID, params)
		self.n_est = params[0]
		self.model = ensemble.RandomForestRegressor(n_estimators=self.n_est, verbose=0, n_jobs=3,
                                                    max_depth=10, oob_score=True)

	def train(self, x, y):
		self.model.fit(x, y)

	def predict(self, x, train):
		return self.model.predict(x)
