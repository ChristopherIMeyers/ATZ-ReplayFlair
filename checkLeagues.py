import praw
import re
import os

import settings as settings
import funcs

allAccountMaps = funcs.readAccountsFile("accounts.txt")

r = funcs.GetPraw()
subreddit = r.subreddit("AllThingsZerg")

def getCurrentLeagueForAccountMap(accountMap):
  def getLeagueForRedditUser(redditName):
    for flair in subreddit.flair:
      if flair['user'].name.lower() == redditName.lower():
        return flair
    raise ValueError('user flair could not be found')
  return getLeagueForRedditUser(accountMap['redditName'])

def getNewLeagueForAccountMap(accountMap):
  league = funcs.getLeague(settings.regions[accountMap['region']], accountMap['bnet'])
  return (accountMap['redditName'], league)

def isLeagueDifferent(zippedUser):
  oldLeague = zippedUser[1]['flair_css_class']
  if oldLeague == None:
    return True
  matches = re.search("([A-z]+) ", oldLeague)
  if matches == None:
    return True
  oldLeagueParsed = matches.group(1).lower()
  newLeague = zippedUser[2][1][0].lower()
  return newLeague != oldLeagueParsed

def updateChange(zippedUser):
  funcs.updateUserFlair(subreddit, zippedUser[1]['user'], zippedUser[1]['flair_text'], zippedUser[0]['region'], zippedUser[2][1])

def runBatch(accountMaps):
  currentLeagues = map(getCurrentLeagueForAccountMap, accountMaps)
  newLeagues = map(getNewLeagueForAccountMap, accountMaps)
  zipped = zip(accountMaps, currentLeagues, newLeagues)
  changes = filter(isLeagueDifferent, zipped)
  if len(changes) > 0:
    print '\nchanges'
    print changes
  map(updateChange, changes)

numberOfAccountsToBatch = 1


if os.path.exists('current.iteration.txt'):
  index = int(open('current.iteration.txt', 'r').read())
  if index >= len(allAccountMaps):
    index = 0
else:
  index = 0
currentBatch = allAccountMaps[index:index + numberOfAccountsToBatch]
index += numberOfAccountsToBatch
open('current.iteration.txt', 'w').write(str(index))
runBatch(currentBatch)
