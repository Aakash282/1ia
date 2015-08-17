# Back-Prop Neural Network

import math
import random 
import string 
import numpy as np
import pandas as pd

# seed the random num generator
# random.seed(0)

# calculate a random number in [a, b]
def rand(a, b):
	return (b-a)*random.random() + a

# sigmoid function
def sigmoid(x):
	return math.tanh(x)

# derivative of sigmoid
def dsig(y):
	# return (math.cosh(y) ** (-2))
	return 1.0 - y**2



class BPNN:
	def __init__(self, struct):
		
		self.arch = struct

		# add 1 node to input layer for bias
		self.arch[0] += 1

		# activation matrix
		self.a = [np.ones([x]) for x in self.arch]
		# weight matrix 
		self.w = [np.ones([self.arch[i-1], self.arch[i]]) for i in range(1, len(self.arch))]

		print "Initializing weights"
		for m in self.w: 
			for r in range(len(m)): 
				for c in range(len(m[r])): 
					m[r][c] = rand(-.2, .2)
		
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
				# matrix mult and sigmoid function
				act = (self.w[l-1].T).dot(self.a[l-1]) 
				self.a[l] = np.array([sigmoid(x) for x in act])

		return self.a[len(self.a)-1]

	# BACKWARDS PROPOGATION AND WEIGHT UPDATES
	# input includes the label vector, learning rate, and momentum rate. 

	def backprop(self, label, L, G):
		if len(label) != self.arch[len(self.a)-1]:
			print "Error: incorrect label vector size"
			print "Actual: %d, Expected: %d\n" % (len(label), self.arch[0]-1)

		# backwards indexing
		idx = range(len(self.w))
		idx.reverse()
		D = [np.zeros([self.arch[x+1]]) for x in idx]
		
		
		# print "UP %d" % len(D)
		# compute error propogation
		for i in range(len(D)):
			if i == 0:
				error = label - self.a[len(self.a)-1]
				# delta for output layer
				for j in range(len(D[i])):
					D[i][j] = dsig(self.a[len(self.a)-1][j]) * error[j]
				# update weight vector
				delta = np.empty_like(self.w[len(self.w)-(i+1)])
				# print delta
				for k in range(len(D[i])):
					nodeDelta = D[i][k] * self.a[len(self.a)-2]
					# print "----------------------"
					# print nodeDelta, len(nodeDelta), len(delta)
					for d in range(len(nodeDelta)):
						# print d, nodeDelta[d]
						delta[d][k] = nodeDelta[d]
					self.w[len(self.w)-(i+1)] += L * np.matrix(delta)
			else: 
				# delta for intermediate layers
				error = (self.w[len(self.w)-i]).dot(np.matrix(D[i-1]).T)
				error = np.sum(error)
				for j in range(len(D[i])):
					D[i][j] = dsig(self.a[len(self.a)-(i+1)][j]) * error
				delta = np.empty_like(self.w[len(self.w)-(i+1)])
				# update weight vector
				# print len(D[i])
				for k in range(len(D[i])):
					# print k 
					# print self.a[len(self.a)-(i+2)]
					# print "----------------------"
					# print nodeDelta, len(nodeDelta), len(delta)
					nodeDelta = D[i][k] * self.a[len(self.a)-(i+2)]
					for d in range(len(nodeDelta)):
						# print nodeDelta[d]
						# print d
						# print k
						delta[d][k] = nodeDelta[d]
				# print self.w[len(self.w)-(i+1)]
				self.w[len(self.w)-(i+1)] += L * np.matrix(delta)

		# print self.w
		# print self.a
		# print D

		errorV = label - self.a[len(self.a)-1]
		error = 0.0
		for e in errorV: 
			error += .5 * (e**2)
		return error
		
	def train(self, data, iterations=100, L=.5, G=.1):
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

