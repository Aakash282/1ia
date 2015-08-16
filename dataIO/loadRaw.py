# loadRaw.py

import numpy as np 
import pandas as pd 
import os 

def parse():
    cwd = os.getcwd()
    FSA = cwd.strip("1ia")
    datadir = FSA + "data/"

    data = []
    for y in range(2001, 2015):
        data.append(pd.DataFrame.from_csv(datadir + "features/features%d" % y, sep=";"))

    data = pd.concat(data)
    data = data.reset_index(drop=True)
    data.to_csv(datadir + "NFL0114_TeamStats_raw.csv")

def getDataset():
    cwd = os.getcwd()
    FSA = cwd.strip("1ia")
    datadir = FSA + "data/"

    return pd.DataFrame.from_csv(datadir + "NFL0114_TeamStats_raw.csv")