import re

def isflairbotmessage(message):
  return message.subject == "account link replay"

def isMessageBodyValidLink(message):
  matches = re.search("(drop.sc/[0-9]+)(/d|)",message.body)
  if matches != None:
    return 'http://'+matches.group(1)+'/d'
  matches = re.search("(ggtracker.com/matches/[0-9]+)(/replay|)",message.body)
  if matches != None:
    return 'http://'+matches.group(1)+'/replay'
  return False
