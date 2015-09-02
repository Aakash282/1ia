import os
import h2o
import pandas as pd

h2o.init()
datadir = os.path.expanduser('~') +'/FSA/data/'
trainingFile = datadir + 'trainBlendPrep.csv'
train = h2o.import_frame(path=trainingFile)
testFile = datadir + 'testBlendPrep.csv'
test = h2o.import_frame(path=testFile)


# dl = h2o.deeplearning(x = train.drop('score diff'),
# 					  y = train['score diff'],
# 					  validation_x = train.drop('score diff'),
# 					  validation_y = train['score diff'],
# 					  nfolds=3,
# 					  epochs=150,
# 					  hidden=[10, 10])

dl = h2o.random_forest(x = train.drop('score diff'),
						y = train['score diff'],
						validation_x = train.drop('score diff'),
						validation_y = train['score diff'],
						ntrees=500, 
						max_depth=40,
						nfolds=2)

# dl = h2o.glm(x = train.drop('score diff'),
# 			  y = train['score diff'],
# 			  validation_x = train.drop('score diff'),
# 			  validation_y = train['score diff'],
# 			  nfolds=4)

dl.show()

dl_preds = dl.predict(test).as_data_frame(use_pandas=True)
dl_preds.to_csv(datadir + "testBlend.csv", index=False)
dl_preds = dl.predict(train).as_data_frame(use_pandas=True)
dl_preds.to_csv(datadir + "trainBlend.csv", index=False)