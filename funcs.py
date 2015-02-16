import re
from bs4 import BeautifulSoup
from datetime import datetime
import httplib

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
  matches = re.search("(drop.sc/[0-9]+)(/d|)(\?pass=[a-z0-9\-]+|)",message.body)
  if matches != None:
    return 'http://'+matches.group(1)+'/d'+matches.group(3)
  matches = re.search("(ggtracker.com/matches/[0-9]+)(/replay|)",message.body)
  if matches != None:
    return 'http://'+matches.group(1)+'/replay'
  return False

def bnetGet(region, url):
  conn = httplib.HTTPConnection(region+'.battle.net')
  conn.connect()
  request = conn.putrequest('GET',url)
  conn.endheaders()
  conn.send('')
  resp = conn.getresponse()
  return resp.read()

def getLeague(region, url):
  print "getLeague(" + region[0] + ", " + url + ")"
  soup = BeautifulSoup(bnetGet(region[0], "/sc2/"+region[1]+"/profile/"+url))
  if (len(soup.select(".error-header")) > 0):
    return (u'banned', str(datetime.now().year), str(datetime.now().month), str(datetime.now().day))
  leaguename = soup.select(".badge-item")[0].select("span.badge")[0]['class'][1][6:]
  return (leaguename, str(datetime.now().year), str(datetime.now().month), str(datetime.now().day))

def readAccountsFile(fileName):
  def readAccountsFileLine(line):
    matches = re.search("([^,]+),([^,]+),([^,]+),", line)
    return {
      'bnet': matches.group(1),
      'redditName': matches.group(2),
      'region': matches.group(3)
    }
  lines = open(fileName,"r").readlines()
  return map(readAccountsFileLine, lines)

def messageReply(message, text):
  print "sending message:" + text
  message.reply(text)
  message.mark_as_read()

def stripOutClan(text):
  return re.search("(\[[A-z0-9]+\]<sp/>)?(.+)",text).group(2)

def updateUserFlair(subReddit, redditName, bNetName, regionName, leagueData):
  r.set_flair(subReddit, redditName, bNetName, leagueData[0].title() + " " + regionName + " " + leagueData[1] + "-" + leagueData[2] + "-" + leagueData[3])
