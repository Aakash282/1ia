# model.py
# this file is a general model class. Actual models should 
# inherit and implement this class. 

class Model:
	'''This is a general model class. Actual models should inherit and
	implement this class.'''
	def __init__(self, ID, params):
		print "initiated model: %d" % ID
		self.model = None
		self.params = params
		self.name = "%d" % ID

	def printParams(self): 
		print self.params