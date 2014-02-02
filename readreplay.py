# -*- coding: utf-8 -*-

import sys
import argparse
import pprint

from mpyq import mpyq
import protocol15405

import httplib
from bs4 import BeautifulSoup
import re

import json
import praw

import urllib


import settings as settings


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
  return None

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
  matches = re.search(u"([0-9]{4}) (Season|시즌) ([0-9]+) -",soup.select("#season-snapshot")[0].select("h3")[0].get_text().strip())
  if matches == None:
    return False
  return (leaguename, matches.group(1), matches.group(3))


def messageReply(message, text):
  print "sending message:" + text
  message.reply(text)
  message.mark_as_read()



def isMessageBodyValidLink(message):
  matches = re.search("(drop.sc/[0-9]+)(/d|)",message.body)
  if matches == None:
    return False
  return 'http://'+matches.group(1)+'/d'

def isflairbotmessage(message):
  return message.subject == "account link replay"

def stripOutClan(text):
  return re.search("(\[[A-z0-9]+\]<sp/>)?(.+)",text).group(2)


def handleMessage(message):
  print "handleMessage from " + message.author.name

  savedReplayName = "tmp/working.SC2Replay"

  replayLink = isMessageBodyValidLink(message)

  if not replayLink:
    messageReply(message,"replay link not found in message")
    return False

  urllib.urlretrieve(replayLink, savedReplayName)

  archive = mpyq.MPQArchive(savedReplayName)
    
  # Read the protocol header, this can be read with any protocol
  contents = archive.header['user_data_header']['content']
  header = protocol15405.decode_replay_header(contents)


  # The header's baseBuild determines which protocol to use
  baseBuild = header['m_version']['m_baseBuild']
  try:
    protocol = __import__('protocol%s' % (baseBuild,))
  except:
    print >> sys.stderr, 'Unsupported base build: %d' % baseBuild
    sys.exit(1)


  contents = archive.read_file('replay.details')
  details = protocol.decode_replay_details(contents)


  if (len(details['m_playerList']) == 1):
    if (details['m_playerList'][0]['m_toon']['m_realm'] == 1):
      regionInt = details['m_playerList'][0]['m_toon']['m_region']
      playerInt = details['m_playerList'][0]['m_toon']['m_id']
      playerName = details['m_playerList'][0]['m_name']

      playerName = stripOutClan(playerName)

      redditname = FindRedditName(protocol.decode_replay_message_events(archive.read_file('replay.message.events')))
      if redditname:
        if redditname.lower() == message.author.name.lower():
          regionName = RegionNameFromId(regionInt)
          if regionName != None:
            playerBnetUrl = '{0}/1/{1}/'.format(playerInt,playerName)
            leagueData = getLeague(settings.regions[regionName], playerBnetUrl)
            if leagueData:
                f = open("accounts.txt","a")
                f.write('{0},{1},{2},\n'.format(playerBnetUrl, redditname, regionName))
                f.close()
                r.set_flair(subreddit, redditname, playerName, leagueData[0].title() + " "+regionName+" S" + leagueData[1] + "-" + leagueData[2])
                messageReply(message,"Your flair has been set.  Account link is a success!")
            else:
              messageReply(message,"Error: {DD6B39E6-857C-11E3-9693-7A7328D43830}. I don't really know what that error message is supposed to mean either.")
          else:
            messageReply(message,"Your region is not supported.  Go yell at the programmer responsible")
        else:
          messageReply(message,"The reddit name in the replay is not the same reddit name you sent this message as.  Be sure to type out your reddit name exactly" )
      else:
        messageReply(message,"Reddit name not found in replay.  Be sure to type out your reddit name in the exact format specified.")
    else:
      messageReply(message,"Error: {2751ED8A-857C-11E3-A17F-7A7328D43830}. I don't really know what that error message is supposed to mean either.")
  else:
    messageReply(message,"Wrong number of players in replay, please host the game by yourself")


r = praw.Reddit(user_agent='ATZ flair bot!  Pipe Battle.Net data to Reddit')
r.login(settings.reddituser, settings.redditpass)
subreddit = r.get_subreddit("AllThingsZerg")

inbox = r.get_unread()

filteredmessages = filter(isflairbotmessage,inbox)

map(handleMessage,filteredmessages)
