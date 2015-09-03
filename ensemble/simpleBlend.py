# simpleBlend
# just does a simple mean of all models handed over. 
# this blender needs to be built out properly. 

import numpy as np 

eps = 0.0
amp = 1.3

def blend(preds):
	# l is the number of predictions in each prediction set
	l = len(preds[0])
	for m in preds: 
		if len(m) != l: 
			print 'error: inconsistent number of predictions'

	results = []
	for i in range(l):
		# take the average of all predictions
		results.append(np.mean([pdfFit(p[i]) for p in preds]))

	return results


# this is a dummy function that can be used to try to fit our results
# to an emperical distribution of score differences
def pdfFit(val):
    if val < 1 and val > 0:
        return 1.1
    if val < 0 and val > -1:
        return -1.1
    if val < 3 and val > 1.5:
        return 3.1
    if val < -1.5 and val > -3: 
        return -3.1
    if val < 8 and val > 6:
        return 7.1
    if val < -6 and val > -8: 
        return -7.1
    # if val < 6 and val > 3.7:
    # 	return 6
    # if val < -3.7 and val > -6:
    # 	return -6

    return round(amp*val)