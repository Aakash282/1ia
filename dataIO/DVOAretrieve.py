import wget 
import re
import os
import time

# Might have to get cookies again if the cookie has expired.
home = os.getcwd()
for y in range(2001, 2015):
    for w in range(1, 18): 
        print "Year: %d, Week: %d" % (y, w)
        #os.makedirs(os.getcwd() + ("/%d/%d/" % (y, w)))
        #os.chdir(os.getcwd() + ("/%d/%d/" % (y, w)))
        datadir = os.path.expanduser('~') + "/FSA/data/DVOApages/"
        url = 'http://www.footballoutsiders.com/premium/weekTeamSeasonDvoa.php?od=O&year=%d&team=ARI&week=%d' %(y, w)        
        os.system("wget --load-cookies=cookies.txt -O %syear%dweek%d.html '%s'" %(datadir,y,w,url) )


