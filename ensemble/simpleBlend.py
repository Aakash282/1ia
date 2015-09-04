# simpleBlend
# just does a simple mean of all models handed over. 
# this blender needs to be built out properly. 

import numpy as np 
import random as rand

eps = 0.0
amp = 1.3
global results
def blend(preds):
    # l is the number of predictions in each prediction set
    l = len(preds[0])
    for m in preds: 
	if len(m) != l: 
	    print 'error: inconsistent number of predictions'

    results = []
    for i in range(l):
	# take the average of all predictions
	results.append(pdfFit(np.mean([p[i] for p in preds])))
	#results.append(np.mean([pdfFit(p[i]) for p in preds]))
    
    return results


# this is a dummy function that can be used to try to fit our results
# to an emperical distribution of score differences
def pdfFit(val):
    common_scores = [-21, -14, -10, -7, -3, 3, 7, 10, 14, 21]
    dist = np.array([val - x for x in common_scores])
    dist_abs = np.array([abs(x) for x in dist])
    min_dist_score = np.argmin(dist_abs)
    error = dist[min_dist_score]
    return common_scores[min_dist_score] + error/1.2

'''
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import pandas as pd 
import os

xs = np.linspace(-20, 20, 400)
a = [pdfFit(x) for x in xs]
density = gaussian_kde(a)
density.covariance_factor = lambda : .1
density._compute_covariance()
plt.plot(xs,density(xs))
'''