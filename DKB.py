import numpy as np
import os
 
training = ['trainRF.csv', 'trainDL.csv', 'trainLM.csv', 'trainDT.csv']
testing = ['testRF.csv', 'testDL.csv', 'testLM.csv', 'testDT.csv']
datadir = os.path.expanduser('~') + '/FSA/data/'
models = 4
trainL = 0
testL = 0
# get len of data
with open(datadir + training[0], 'r') as f: 
	trainL = len(f.readlines())-1
	print trainL

with open(datadir + testing[0], 'r') as f:
	testL = len(f.readlines())-1
	print testL

preds = [0.0 for i in range(trainL)]

for filename in training: 
	with open(datadir + filename, 'r') as f: 
		data = f.readlines()
		for i in range(len(data[1:])): 
			pred = float(data[i+1].strip())
			preds[i] += pred

print len(preds)
with open(datadir + 'trainBlend.csv', 'w') as f: 
	for i in range(len(preds)):
		preds[i] = preds[i] / models
		f.write(str(preds[i]) + '\n')

preds = [0.0 for i in range(testL)]

for filename in testing: 
	with open(datadir + filename, 'r') as f: 
		data = f.readlines()
		for i in range(len(data[1:])): 
			pred = float(data[i+1].strip())
			preds[i] += pred
print len(preds)

with open(datadir + 'testBlend.csv', 'w') as f: 
	for i in range(len(preds)):
		preds[i] = preds[i] / models
		f.write(str(preds[i]) + '\n')