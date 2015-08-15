import wget 
import re
import os
import time

def findGames(file):
    games = re.findall('/boxscores/[0-9]{9}[a-z]{2,3}\.htm', file)
    return set(games)

years = [x for x in range(2001, 2008)]
weeks = [x+1 for x in range(17)]
home = os.getcwd()
for y in years:
    for w in weeks: 
        print "Year: %d, Week: %d" % (y, w)
        os.makedirs(os.getcwd() + ("/%d/%d/" % (y, w)))
        os.chdir(os.getcwd() + ("/%d/%d/" % (y, w)))
        url = "http://www.pro-football-reference.com/years/%d/week_%d.htm" % (y, w)
        filename = wget.download(url)
        with open(filename, 'r') as f: 
            lines = f.readlines()
            text = ""
            for l in lines: 
                text += l
            games = findGames(text)
            for g in games: 
                print g
                url = "http://www.pro-football-reference.com/"  + g
                wget.download(url)
                time.sleep(2) # rest for 1 second
        os.chdir(home)

