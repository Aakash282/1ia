import os
import h2o
import pandas as pd
h2o.init()
datadir = os.path.expanduser('~') +'/FSA/data/'
# Load in the data
dir_prefix = datadir + "NNinput/"
trainingFile = dir_prefix + 'training_set.csv'
trainData = h2o.import_frame(path=trainingFile)
testFile = dir_prefix + 'testing_set.csv'
testData = h2o.import_frame(path=testFile)



train = trainData.drop('away score').drop('home score').drop('spread')
test = testData.drop('away score').drop('home score').drop('spread')

drf = h2o.random_forest(x = train.drop('score diff'),
						y = train['score diff'],
						validation_x = train.drop('score diff'),
						validation_y = train['score diff'],
						ntrees=100, 
						max_depth=5,
						nfolds=7)
drf.show()


drf_preds = drf.predict(test).as_data_frame(use_pandas=True)
drf_preds.to_csv(datadir + "testRF.csv", index=False)
drf_preds = drf.predict(train).as_data_frame(use_pandas=True)
drf_preds.to_csv(datadir + "trainRF.csv", index=False)


dl = h2o.deeplearning(x = train.drop('score diff'),
					  y = train['score diff'],
					  validation_x = train.drop('score diff'),
					  validation_y = train['score diff'],
					  nfolds=7,
					  epochs=150,
					  hidden=[10, 5])
dl.show()

dl_preds = dl.predict(test).as_data_frame(use_pandas=True)
dl_preds.to_csv(datadir + "testDL.csv", index=False)
dl_preds = dl.predict(train).as_data_frame(use_pandas=True)
dl_preds.to_csv(datadir + "trainDL.csv", index=False)

glm = h2o.glm(x = train.drop('score diff'),
			  y = train['score diff'],
			  validation_x = train.drop('score diff'),
			  validation_y = train['score diff'],
			  nfolds=4)
glm.show()

glm_preds = glm.predict(test).as_data_frame(use_pandas=True)
glm_preds.to_csv(datadir + "testLM.csv", index=False)
glm_preds = glm.predict(train).as_data_frame(use_pandas=True)
glm_preds.to_csv(datadir + "trainLM.csv", index=False)

gm = h2o.gbm(x = train.drop('score diff'),
			  y = train['score diff'],
			  validation_x = train.drop('score diff'),
			  validation_y = train['score diff'])
gm.show()

gm_preds = glm.predict(test).as_data_frame(use_pandas=True)
gm_preds.to_csv(datadir + "testDT.csv", index=False)
gm_preds = glm.predict(train).as_data_frame(use_pandas=True)
gm_preds.to_csv(datadir + "trainDT.csv", index=False)