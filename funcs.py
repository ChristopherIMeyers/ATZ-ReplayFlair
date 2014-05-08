import re

def isflairbotmessage(message):
  return message.subject == "account link replay"

def isMessageBodyValidLink(message):
  matches = re.search("(drop.sc/[0-9]+)(/d|)",message.body)
  if matches == None:
    return False
  return 'http://'+matches.group(1)+'/d'
