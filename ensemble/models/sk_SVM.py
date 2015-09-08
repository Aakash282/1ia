# sk_SVM.py 

from Model import Model
from sklearn.svm import SVR

class sk_SVM(Model):
	'''inherits Model class and implements sklearns SVM class'''
	def __init__(self, ID, params):
		Model.__init__(self, ID, params)
		self.model = SVR(kernel='rbf', verbose=True)

	def train(self, x, y):
		self.model.fit(x, y)

	def predict(self, x, train):
		return self.model.predict(x)
