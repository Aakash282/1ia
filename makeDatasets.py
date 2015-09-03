import pandas as pd
import os
from features import features
from dataIO import loadData as ld
from matplotlib import pyplot as plt

# features.get_feature_set(2001, 2014)

# Load in the data
dir_prefix = os.path.expanduser('~') + "/FSA/data/NNinput/"

training_set = []
train_years = range(2001, 2014)
train_years.remove(2006)
train_years.remove(2007)
train_years.remove(2008)
for i in train_years:
	training_set.append(pd.DataFrame.from_csv(dir_prefix + "features%d.csv" % i))

training_set = pd.concat(training_set)
training_set.to_csv(dir_prefix + "training_set.csv")

testing_set = []
for i in range(2014, 2015):
	testing_set.append(pd.DataFrame.from_csv(dir_prefix + "features%d.csv" % i))

testing_set = pd.concat(testing_set)
testing_set.to_csv(dir_prefix + "testing_set.csv")