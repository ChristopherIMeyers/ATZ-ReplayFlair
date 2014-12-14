import settings as settings

import funcs

accountMaps = funcs.readAccountsFile("accounts.txt")
def getLeagueForAccountMap(accountMap):
  league = funcs.getLeague(settings.regions[accountMap['region']], accountMap['bnet'])
  return (accountMap['redditName'], league)

newLeagues = map(getLeagueForAccountMap, accountMaps)
print newLeagues
