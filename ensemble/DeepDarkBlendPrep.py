# DeepDarkBlend.py
import pandas as pd
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

preds = [[] for i in range(trainL)]

for filename in training: 
	with open(datadir + filename, 'r') as f: 
		data = f.readlines()
		for i in range(len(data[1:])): 
			pred = float(data[i+1].strip())
			preds[i].append(pred)

df_train = pd.DataFrame.from_csv(datadir + "/NNinput/training_set.csv")
df_test = pd.DataFrame.from_csv(datadir + "/NNinput/testing_set.csv")

train_score = df_train[['score diff']].values.T.tolist()[0]
test_score = df_test[['score diff']].values.T.tolist()[0]

# for i in range(len(preds)):
# 	preds[i].append(train_score[i])

print len(preds)
with open(datadir + 'trainBlendPrep.csv', 'w') as f: 
	f.write("RF,DL,LM,DT,score diff\n")
	for i in range(len(preds)):
		s = ""
		for j in range(len(preds[i])):
			s += "%f," % preds[i][j]
		s += "%f\n" % train_score[i]
		f.write(s)

preds = [[] for i in range(testL)]

for filename in testing: 
	with open(datadir + filename, 'r') as f: 
		data = f.readlines()
		for i in range(len(data[1:])): 
			pred = float(data[i+1].strip())
			preds[i].append(pred)
print len(preds)

# for i in range(len(preds)):
# 	preds[i].append(test_score[i])

print len(preds)
with open(datadir + 'testBlendPrep.csv', 'w') as f: 
	f.write("RF,DL,LM,DT,score diff\n")
	for i in range(len(preds)):
		s = ""
		for j in range(len(preds[i])):
			s += "%f," % preds[i][j]
		s += "%f\n" % test_score[i]
		f.write(s)