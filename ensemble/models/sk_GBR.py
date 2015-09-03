# sk_GBR.py 

from Model import Model
from sklearn import ensemble

class sk_GBR(Model):
	'''inherits Model class and implements sklearns RandomForestRegressor class'''
	def __init__(self, ID, params):
		Model.__init__(self, ID, params)
		self.n_est = params[0]
		self.l = params[1]
		self.model = ensemble.GradientBoostingRegressor(n_estimators=self.n_est, learning_rate=self.l)

	def train(self, x, y):
		self.model.fit(x, y)

	def predict(self, x):
		return self.model.predict(x)
