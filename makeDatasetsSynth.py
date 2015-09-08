import pandas as pd
import os
from features import features
# from dataIO import loadData as ld
# from matplotlib import pyplot as plt
from features import featureNoise as noise


# features.get_feature_set(2014, 2015)

# synthesize data
noise.synth(50)

# Load in the data
dir_prefix = os.path.expanduser('~') + "/FSA/data/"
inpath = "FeaturesSynth/"
testInPath = 'FeaturesByYear/'
outpath = "TrainTestSynth/"
train_years = range(2001, 2010)
val_years = range(2010, 2012)
test_years = range(2012, 2015)

# exclude years
'''
train_years.remove(2006)
train_years.remove(2007)
train_years.remove(2008)
'''

# create sets
training_set = []
print "Train Years"
for i in train_years:
	print i
	training_set.append(pd.DataFrame.from_csv(dir_prefix + inpath + "featuresSynth%d.csv" % i))

training_set = pd.concat(training_set)
training_set.to_csv(dir_prefix + outpath + "training_set.csv")

val_set = []
print "Validation Years"
for i in val_years:
	print i
	val_set.append(pd.DataFrame.from_csv(dir_prefix + inpath + "featuresSynth%d.csv" % i))

val_set = pd.concat(val_set)
val_set.to_csv(dir_prefix + outpath + "val_set.csv")

testing_set = []
print "Test Years"
for i in test_years:
	print i
	testing_set.append(pd.DataFrame.from_csv(dir_prefix + testInPath + "features%d.csv" % i))

testing_set = pd.concat(testing_set)
testing_set.to_csv(dir_prefix + outpath + "testing_set.csv")
