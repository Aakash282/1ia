# loadRaw.py

import numpy as np 
import pandas as pd 
import os 

def parse():
    cwd = os.getcwd()
    FSA = cwd.strip("1ia/dataIO")
    datadir = '/' + FSA + "/data/"

    p = pd.read_csv(datadir + "headers.csv", sep = ";")
    for y in range(2001, 2015):
        print y
        lst_temp = pd.read_csv(datadir + "features/features%d" % y, sep=";")
        for line in range(len(lst_temp['week'])):
            lst_temp['week'][line] = str(lst_temp['week'][line]) + " %d" %y
          
        p = pd.merge(p, lst_temp, how = 'outer')
    columns = list(p.keys())
    columns[0] = 'week year'
    p.columns = columns
    p.to_csv(datadir + "NFL0114_TeamStats_raw.csv")

def getDataset():
    cwd = os.getcwd()
    FSA = cwd.strip("1ia/dataIO")
    datadir = '/' + FSA + "/data/"
    return pd.DataFrame.from_csv(datadir + "NFL0114_TeamStats_raw.csv")
