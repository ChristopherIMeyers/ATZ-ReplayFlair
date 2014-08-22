import re
from bs4 import BeautifulSoup
from datetime import datetime
import httplib

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
