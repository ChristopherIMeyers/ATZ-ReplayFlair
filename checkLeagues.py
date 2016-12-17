import praw
import re
import os

import settings as settings
import funcs

allAccountMaps = funcs.readAccountsFile("accounts.txt")

r = praw.Reddit(user_agent='ATZ flair script! Pipe Battle.Net data to Reddit')
r.login(settings.reddituser, settings.redditpass, disable_warning=True)
subreddit = r.get_subreddit("AllThingsZerg")

def runBatch(accountMaps):
  def getCurrentLeagueForAccountMap(accountMap):
    def getLeagueForRedditUser(redditName):
      return r.get_flair(subreddit, redditName)
    return getLeagueForRedditUser(accountMap['redditName'])

  currentLeagues = map(getCurrentLeagueForAccountMap, accountMaps)

  print '\ncurrentLeagues'
  print currentLeagues

  def getNewLeagueForAccountMap(accountMap):
    league = funcs.getLeague(settings.regions[accountMap['region']], accountMap['bnet'])
    return (accountMap['redditName'], league)

  newLeagues = map(getNewLeagueForAccountMap, accountMaps)
  zipped = zip(accountMaps, currentLeagues, newLeagues)

  print '\nzipped'
  print zipped

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

  print '\nchanges'
  changes = filter(isLeagueDifferent, zipped)
  print changes

  def updateChange(zippedUser):
    funcs.updateUserFlair(subreddit, zippedUser[1]['user'], zippedUser[1]['flair_text'], zippedUser[0]['region'], zippedUser[2][1])

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
