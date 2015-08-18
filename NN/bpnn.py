# Back-Prop Neural Network

import math
import random 
import string 
import numpy as np
import pandas as pd

# seed the random num generator
random.seed(0)

# calculate a random number in [a, b]
def rand(a, b):
	return (b-a)*random.random() + a

# sigmoid function
def sigmoid(x):
	return math.tanh(x)

# derivative of sigmoid
def dsig(y):
	return (math.cosh(y) ** (-2))
	# return 1.0 - y**2

class BPNN:
	def __init__(self, struct):
		self.arch = struct

		# add 1 node to input layer for bias
		self.arch[0] += 1

		# activation matrix
		self.a = [np.ones([x]) for x in self.arch]
		for a in self.a: 
			print a

		# weight matrix 
		self.w = [np.ones([self.arch[i-1], self.arch[i]]) for i in range(1, len(self.arch))]

		print "Initializing weights"
		for m in self.w: 
			for r in range(len(m)): 
				for c in range(len(m[r])): 
					m[r][c] = rand(-.5, .5)
			print m	
		# momentum matrix 
		self.p = [np.zeros([self.arch[i-1], self.arch[i]]) for i in range(1, len(self.arch))]

	# FORWARD PROPOGATION STEP
	# input must be np.array
	def predict(self, inputs):
		# confirm that input size is correct
		if len(inputs) != self.arch[0]-1:
			print "Error: incorrect input vector size"
			print "Actual: %d, Expected: %d\n" % (len(inputs), self.arch[0]-1)
			return
		# propogate through the network
		for l in range(len(self.a)):
			# input activation
			if l == 0: 
				self.a[l] = np.append(inputs, 1.0)
			# hidden and output activation
			else: 
				act = np.matrix(self.a[l-1]).dot(self.w[l-1])
				act = act.flatten().tolist()[0]
				self.a[l] = np.array([sigmoid(x) for x in act])

		return self.a[len(self.a)-1]

	# BACKWARDS PROPOGATION AND WEIGHT UPDATES
	# input includes the label vector, learning rate, and momentum rate. 
	def backprop(self, label, L, G):
		if len(label) != self.arch[len(self.a)-1]:
			print "Error: incorrect label vector size"
			print "Actual: %d, Expected: %d\n" % (len(label), self.arch[0]-1)

		error = self.computeError(label)
		self.updateWeights(error, L, G)

		errorV = label - self.a[len(self.a)-1]
		E = 0.0
		for e in errorV: 
			E += .5 * (e**2)
		return E

	def computeError(self, label):
		error = []
		# Compute error
		for idx in range(len(self.a)-1):
			i = len(self.a)-(idx+1)
			# output error
			if idx == 0:
				dif = label - self.a[i]
				error.append(np.matrix([dsig(self.a[i][k]) * dif[k] for k in range(len(dif))]))

			# back propogate error through network 
			else: 
				dif = self.w[i].dot(np.matrix(error[-1]).T).T
				dif = dif.tolist()[0]
				error.append(np.matrix([dsig(self.a[i][k]) * dif[k] for k in range(len(dif))]))

		
		# print error
		return error

	def updateWeights(self, error, L, G):
		# update weights
		for idx in range(len(self.a)-1):
			i = len(self.a)-(idx+1)
			delta = (np.matrix(self.a[i-1]).T).dot(np.matrix(error[idx]))
			self.w[i-1] = self.w[i-1] + L * delta + G * self.p[i-1]
			self.p[i-1] = delta


	def train(self, data, iterations=1000, L=.5, G=.1):
		# L is the learning rate
		# G is the momentum factor
		for i in range(iterations):
			error = 0.0
			for v in data: 
				# print v
				vector = np.array(v[0])
				label = v[1]
				self.predict(vector)
				error += self.backprop(label, L, G)
			print "Iteration: %d, Error: %f"  % (i, error)

