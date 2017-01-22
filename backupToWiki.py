import praw
import re

import settings as settings
import funcs

allAccountMaps = funcs.readAccountsFile('accounts.txt')

r = praw.Reddit(user_agent='ATZ flair script! Pipe Battle.Net data to Reddit')
r.login(settings.reddituser, settings.redditpass, disable_warning=True)
subreddit = r.get_subreddit('AllThingsZerg')

def accountRowToWiki(accountRow):
  return '    ' + accountRow['bnet'] + ',' + accountRow['redditName'] + ',' + accountRow['region']

wikiContent = '\n'.join(map(accountRowToWiki, allAccountMaps))

r.edit_wiki_page(subreddit, 'flairlist', wikiContent, 'beep boop - backing up account data')

