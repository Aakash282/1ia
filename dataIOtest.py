from dataIO import loadRaw as load
from dataIO import datavalidation as val

data = load.getDataset()

print data
if val.validate()!= None:
    print 'invalid data!'

