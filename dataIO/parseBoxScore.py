from bs4 import BeautifulSoup, SoupStrainer
from glob import glob
import os, csv


def parseGame(game, week):
  # Open the game file
  with open(game, 'r') as g:
    only_tables = SoupStrainer('table')
    soup = BeautifulSoup(g,parse_only=only_tables)

    features = [str(week)]
    home = []
    away = []

    # First get the tables we need
    gameInfo = soup.find(id="game_info").find_all('td')
    lineScore = soup.find(id="linescore").find_all('td')
    teamStats = soup.find(id="team_stats").find_all('td')
    officials = soup.find(id="ref_info").find_all('td')
    
    # Teams and Records
    if len(lineScore) > 12:
      features.append(lineScore[7].text.split('(')[0])
      features.append(lineScore[0].text.split('(')[0])
      awayScores = [lineScore[x].text for x in range(1,5)] + [lineScore[6].text]
      homeScores = [lineScore[x].text for x in range(8,12)] + [lineScore[13].text]

    else:
      features.append(lineScore[6].text.split('(')[0])
      features.append(lineScore[0].text.split('(')[0])
      awayScores = [lineScore[x].text for x in range(1,6)]
      homeScores = [lineScore[x].text for x in range(7,12)]

    spread = ""
    time = ""
    toss = ""
    roof = ""
    surface = ""
    attendance = ""

    for i in xrange(0, len(gameInfo),2):
      if gameInfo[i].text == 'Vegas Line':
        spread = gameInfo[i+1].text
      elif gameInfo[i].text == 'Start Time (ET)':
        time = gameInfo[i+1].text
      elif gameInfo[i].text == 'Won Toss':
        toss = gameInfo[i+1].text
      elif gameInfo[i].text == 'Roof':
        roof = gameInfo[i+1].text
      elif gameInfo[i].text == 'Surface':
        surface = gameInfo[i+1].text
      elif gameInfo[i].text == 'Attendance':
        attendance = gameInfo[i+1].text
      else:
        continue

    # Spread
    features.append(spread)
    # Time of day
    features.append(time) 
    # Toss Winner
    features.append(toss)
    # Roof
    features.append(roof)
    # Surface
    features.append(surface)
    # Attendance
    features.append(attendance)

    # Officials
    refs = [officials[x].text for x in range(len(officials))]
    refs += [''] * (14 - len(refs))
    features.extend(refs)

    # Score
    home.extend(homeScores)
    away.extend(awayScores)

    
    # First Downs
    away.append(teamStats[1].text)
    home.append(teamStats[2].text)
    
    # Rushing Stats
    awayRush = teamStats[4].text
    homeRush = teamStats[5].text
    
    away.extend(awayRush.split('-'))
    home.extend(homeRush.split('-'))

    # Passing Stats
    awayPass = teamStats[7].text
    homePass = teamStats[8].text
    away.extend(awayPass.split('-'))
    home.extend(homePass.split('-'))

    # Sacked
    awaySacked = teamStats[10].text
    homeSacked = teamStats[11].text
    away.extend(awaySacked.split('-'))
    home.extend(homeSacked.split('-'))

    # Net Pass Yards
    away.append(teamStats[13].text)
    home.append(teamStats[14].text)

    # Total Yards
    away.append(teamStats[16].text)
    home.append(teamStats[17].text)

    # Fumbles
    away.extend(teamStats[19].text.split('-'))
    home.extend(teamStats[20].text.split('-'))

    # Turnovers
    away.append(teamStats[22].text)
    home.append(teamStats[23].text)
    # Penalties
    away.extend(teamStats[25].text.split('-'))
    home.extend(teamStats[26].text.split('-'))

    # 3rd Down Eff
    away.extend(teamStats[28].text.split('-'))
    home.extend(teamStats[29].text.split('-'))

    # 4th Down Eff
    away.extend(teamStats[31].text.split('-'))
    home.extend(teamStats[32].text.split('-'))

    # Total Plays
    away.append(teamStats[34].text)
    home.append(teamStats[35].text)
    # TOP
    away.append(teamStats[37].text)
    home.append(teamStats[38].text)

    # Finish Up
    features.extend(home)
    features.extend(away)

    return features

home = os.path.expanduser('~') + "/FSA/data/"
years = [x for x in range(2010, 2015)]
weeks = [x+1 for x in range(17)]
for y in years:
  with open(home + "rawdata/rawdata" + str(y), 'w') as f:
    for w in weeks:
      print "Year: %d, Week: %d" % (y, w)
      games = glob(home + 'boxscores' + '/' + str(y) + '/' + str(w) + '/' + '2*.htm')
      for game in games:
        gameData = parseGame(game, w)
        # Write the game data
        data = ';'.join(gameData)
        f.write(data + "\n")

