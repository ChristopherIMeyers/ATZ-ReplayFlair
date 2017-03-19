import re
from bs4 import BeautifulSoup
from datetime import datetime
import httplib
import praw
import os

if os.path.exists('settings.py'):
  import settings
  def GetPraw():
    return praw.Reddit(client_id = settings.client_id,
                       client_secret = settings.client_secret,
                       username = settings.reddituser,
                       password = settings.redditpass,
                       user_agent = 'r/allthingszerg replay flair script')

def FindRedditName(events):
  for event in events:
    if (event['_event'] == 'NNet.Game.SChatMessage'):
      matches = re.search('reddit *name[ :]*([A-z0-9]+)',event['m_string'].lower())
      if matches != None:
        return matches.group(1)
  return False

def RegionNameFromId(regionId):
  if regionId == 1:
    return "AM"
  if regionId == 2:
    return "EU"
  if regionId == 3:
    return "KR"
  if regionId == 6:
    return "SEA"
  return None

def isflairbotmessage(message):
  return message.subject == "account link replay"

def isMessageBodyValidLink(message):
  matches = re.search("drop.sc/replay/([0-9]+)", message.body)
  if matches != None:
    return 'http://sc2replaystats.com/download/' + matches.group(1)
  matches = re.search("(ggtracker.com/matches/[0-9]+)(/replay|)", message.body)
  if matches != None:
    return 'http://' + matches.group(1) + '/replay'
  return False

def bnetGet(region, url):
  conn = httplib.HTTPConnection(region + '.battle.net')
  conn.connect()
  request = conn.putrequest('GET', url)
  conn.endheaders()
  conn.send('')
  resp = conn.getresponse()
  return resp.read()

def getLeagueFromSource(source):
  soup = BeautifulSoup(source, "html.parser")
  if (len(soup.select(".error-header")) > 0):
    return u'banned'
  try:
    return soup.select(".badge-item")[0].select("span.badge")[0]['class'][1][6:]
  except: 
    open("last.failure.txt", "w").write(source)
    raise

def getLeague(region, url):
  source = bnetGet(region[0], "/sc2/"+region[1]+"/profile/"+url)
  leaguename = getLeagueFromSource(source)
  return (leaguename, str(datetime.now().year), str(datetime.now().month), str(datetime.now().day))

def readAccountsFile(fileName):
  def readAccountsFileLine(line):
    matches = re.search("([^,]+),([^,]+),([^,]+),", line)
    return {
      'bnet': matches.group(1),
      'redditName': matches.group(2),
      'region': matches.group(3)
    }
  lines = open(fileName, "r").readlines()
  return map(readAccountsFileLine, lines)

def messageReply(message, text):
  print "sending message:" + text
  message.reply(text)
  message.mark_read()

def stripOutClan(text):
  return re.search("(" +
                     "(?:\[|<|&lt;)" +
                     "[^\[\]<>]+" +
                     "(?:\]|>|&gt;)" +
                     "<sp/>" +
                   ")?" +
                   "(.+)", text).group(2)

def updateUserFlair(subReddit, redditName, bNetName, regionName, leagueData):
  newFlairText = leagueData[0].title() + " " + regionName + " " + leagueData[1] + "-" + leagueData[2] + "-" + leagueData[3]
  subReddit.flair.set(redditName, bNetName, newFlairText)
