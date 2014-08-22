import re

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
