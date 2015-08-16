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



class BPNN:
	def __init__(self, struct):
		
		self.arch = struct

		# add 1 node to input layer for bias
		self.arch[0] += 1

		# activation matrix
		self.a = [np.ones([x]) for x in self.arch]
		print self.a
		# weight matrix 
		self.w = [np.ones([self.arch[i-1], self.arch[i]]) for i in range(1, len(self.arch))]

		print "Initializing weights"
		for m in self.w: 
			print m
			for r in range(len(m)): 
				print m[r]
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
				self.a[l] = np.append(inputs, 1.0)# np.array(inputs.append(1.0))
			# hidden and output activation
			else:
				# matrix mult and sigmoid function
				act = (self.w[l-1].T).dot(self.a[l-1]) 
				self.a[l] = np.array([sigmoid(x) for x in act])

		return self.a[len(self.a)-1]

	def backprop(self, label, L, G):
		if len(label) != self.arch[len(self.a)-1]:
			print "Error: incorrect label vector size"
			print "Actual: %d, Expected: %d\n" % (len(label), self.arch[0]-1)

		# backwards indexing
		idx = range(len(self.w))
		idx.reverse()
		D = [np.zeros([self.arch[x+1]]) for x in idx]
		print D

		
		error = label - self.a[len(self.a)-1]
		print "Error"
		for i in range(len(D)):
			if i == 0:
				# delta for output layer
				for j in range(len(D[i])):
					D[i][j] = dsig(self.a[len(self.a)-1][j]) * error[j]
			else: 
				# delta for intermediate layers
				# 
				error = (self.w[len(self.w)-i].T).dot(D[i-1])
				error = np.sum(error)
				for j in range(len(D[i])):
					D[i][j] = dsig(self.a[len(self.a)-(i+1)][j]) * error[j]
		
		# for i in range()
		return
	def train(self, data, iterations=100, L=.5, G=.1):
		# L is the learning rate
		# G is the momentum factor
		print self.a
		for i in range(iterations):
			error = 0.0
			for v in data: 
				vector = np.array(v[0])
				label = v[1]
				self.predict(vector)
				error += self.backprop(label, L, G)

