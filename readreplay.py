# -*- coding: utf-8 -*-

import sys
import argparse
import pprint

import mpyq
from s2protocol import protocol15405

import httplib
from bs4 import BeautifulSoup
import re

import json
import praw

import urllib

from datetime import datetime

import settings as settings

import funcs

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



def messageReply(message, text):
  print "sending message:" + text
  message.reply(text)
  message.mark_as_read()

def stripOutClan(text):
  return re.search("(\[[A-z0-9]+\]<sp/>)?(.+)",text).group(2)


def handleMessage(message):
  print "handleMessage from " + message.author.name

  savedReplayName = "tmp/working.SC2Replay"

  replayLink = funcs.isMessageBodyValidLink(message)

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
    _temp = __import__('s2protocol', globals(), locals(), ['protocol%s' % (baseBuild,)])
    protocol = getattr(_temp, 'protocol%s' % (baseBuild,))
  except:
    print >> sys.stderr, 'Unsupported base build: %d' % baseBuild
    sys.exit(1)


  contents = archive.read_file('replay.details')
  details = protocol.decode_replay_details(contents)


  if (len(details['m_playerList']) != 1):
    messageReply(message,"Wrong number of players in replay, please host the game by yourself")
    return False
  if (details['m_playerList'][0]['m_toon']['m_realm'] != 1):
    messageReply(message,"Error: {2751ED8A-857C-11E3-A17F-7A7328D43830}")
    return False
  regionInt = details['m_playerList'][0]['m_toon']['m_region']
  playerInt = details['m_playerList'][0]['m_toon']['m_id']
  playerName = details['m_playerList'][0]['m_name']

  playerName = stripOutClan(playerName)

  redditname = FindRedditName(protocol.decode_replay_message_events(archive.read_file('replay.message.events')))
  if not (redditname):
    messageReply(message,"Reddit name not found in replay.  Be sure to type out your reddit name in the exact format specified.")
    return False
  if redditname.lower() != message.author.name.lower():
    messageReply(message,"The reddit name in the replay is not the same reddit name you sent this message as.  Be sure to type out your reddit name exactly" )
    return False

  regionName = RegionNameFromId(regionInt)
  if regionName == None:
    messageReply(message,"Your region is not supported.  Go yell at the programmer responsible")
    return False

  playerBnetUrl = '{0}/1/{1}/'.format(playerInt,playerName)
  leagueData = funcs.getLeague(settings.regions[regionName], playerBnetUrl)
  if not (leagueData):
    messageReply(message,"Error: {DD6B39E6-857C-11E3-9693-7A7328D43830}")
    return False

  f = open("accounts.txt","a")
  f.write('{0},{1},{2},\n'.format(playerBnetUrl, redditname, regionName))
  f.close()
  r.set_flair(subreddit, redditname, playerName, leagueData[0].title() + " "+regionName+" " + leagueData[1] + "-" + leagueData[2] + "-" + leagueData[3])
  messageReply(message,"Your flair has been set.  Account link is a success!")
  return True



r = praw.Reddit(user_agent='ATZ flair bot!  Pipe Battle.Net data to Reddit')
r.login(settings.reddituser, settings.redditpass)
subreddit = r.get_subreddit("AllThingsZerg")

inbox = r.get_unread()

filteredmessages = filter(funcs.isflairbotmessage,inbox)

map(handleMessage,filteredmessages)
