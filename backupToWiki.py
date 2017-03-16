import praw
import re

import settings as settings
import funcs

allAccountMaps = funcs.readAccountsFile('accounts.txt')

r = funcs.GetPraw()
subreddit = r.subreddit('AllThingsZerg')

def accountRowToWiki(accountRow):
  return '    ' + accountRow['bnet'] + ',' + accountRow['redditName'] + ',' + accountRow['region']

wikiContent = '\n'.join(map(accountRowToWiki, allAccountMaps))

subreddit.wiki['flairlist'].edit(wikiContent, 'beep boop - backing up account data')

