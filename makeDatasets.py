import pandas as pd
import os
import sys
from features import features
from features import features
import argparse
from dataIO import separate_teams as sep
from dataIO import loadRaw as lr
sys.path.append(os.path.expanduser('~') + '/FSA/1ia/features/' )

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--all", help="Remake all data sets (requires rawdata).", action='store_true')
parser.add_argument("-f", "--features", help="Remake only the features and then the training and test sets.",action='store_true')
args = parser.parse_args()

if args.all:
    # Run loadRaw
    print "Loading rawdata"
    lr.parseYear()
    # Run separate_teams
    print "Separating teams"
    sep.write_teams_years()
    # Run features
    execfile(os.path.expanduser('~') + "/FSA/1ia/features/computeTeamFeatures.py")
    print "Computing features"
    from features import features
    features.get_feature_set(2001, 2014)

elif args.features:
    # Run features
    execfile(os.path.expanduser('~') + "/FSA/1ia/features/computeTeamFeatures.py")
    print "Computing features"
    from features import features
    features.get_feature_set(2001, 2014)


train_start = input('Enter starting year for training set: ')
train_stop = input('Enter stopping year for training set: ')
test_start = input('Enter starting year for test set: ')
test_stop = input('Enter stopping year for test set: ')

# Load in the data
dir_prefix = os.path.expanduser('~') + "/FSA/data/"
inpath = "FeaturesByYear/"
outpath = "TrainTest/"
training_set = []
train_years = range(train_start, train_stop+1)

for i in train_years:
	training_set.append(pd.DataFrame.from_csv(dir_prefix + inpath + "features%d.csv" % i))

training_set = pd.concat(training_set)
training_set.to_csv(dir_prefix + outpath + "training_set.csv")

testing_set = []
for i in range(test_start, test_stop+1):
	testing_set.append(pd.DataFrame.from_csv(dir_prefix + inpath + "features%d.csv" % i))

testing_set = pd.concat(testing_set)
testing_set.to_csv(dir_prefix + outpath + "testing_set.csv")
