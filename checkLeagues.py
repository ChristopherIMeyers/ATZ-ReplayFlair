import praw
import re

import settings as settings
import funcs

accountMaps = funcs.readAccountsFile("accounts.txt")

r = praw.Reddit(user_agent='ATZ flair bot!  Pipe Battle.Net data to Reddit')
r.login(settings.reddituser, settings.redditpass)
subreddit = r.get_subreddit("AllThingsZerg")

def getCurrentLeagueForAccountMap(accountMap):
  def getLeagueForRedditUser(redditName):
    return r.get_flair(subreddit, redditName)
  return getLeagueForRedditUser(accountMap['redditName'])

currentLeagues = map(getCurrentLeagueForAccountMap, accountMaps)


def getNewLeagueForAccountMap(accountMap):
  league = funcs.getLeague(settings.regions[accountMap['region']], accountMap['bnet'])
  return (accountMap['redditName'], league)

newLeagues = map(getNewLeagueForAccountMap, accountMaps)
zipped = zip(currentLeagues, newLeagues)

print 'zipped'
print zipped

def isLeagueDifferent(zippedUser):
  oldLeague = zippedUser[0]['flair_css_class']
  newLeague = zippedUser[1][1][0].lower()
  oldLeagueParsed = re.search("([A-z]+) ", oldLeague).group(1).lower()
  return newLeague != oldLeagueParsed

print 'changes'
changes = filter(isLeagueDifferent, zipped)
print changes
