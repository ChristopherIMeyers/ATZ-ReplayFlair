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

def handleMessage(message):
  print "handleMessage from " + message.author.name

  savedReplayName = "tmp/working.SC2Replay"

  replayLink = funcs.isMessageBodyValidLink(message)

  if not replayLink:
    funcs.messageReply(message, "replay link not found in message")
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
  events = protocol.decode_replay_message_events(archive.read_file('replay.message.events'))
  return handleReplayDetails(details, message, events)


def handleReplayDetails(details, message, events):
  if (len(details['m_playerList']) != 1):
    funcs.messageReply(message, "Wrong number of players in replay, please host the game by yourself")
    return False
  realm = details['m_playerList'][0]['m_toon']['m_realm']
  regionInt = details['m_playerList'][0]['m_toon']['m_region']
  playerInt = details['m_playerList'][0]['m_toon']['m_id']
  playerName = details['m_playerList'][0]['m_name']

  playerName = funcs.stripOutClan(playerName)

  redditname = funcs.FindRedditName(events)
  if not (redditname):
    funcs.messageReply(message, "Reddit name not found in replay. Be sure to type out your reddit name in the exact format specified.")
    return False
  if redditname.lower() != message.author.name.lower():
    funcs.messageReply(message, "The reddit name in the replay is not the same reddit name you sent this message as. Be sure to type out your reddit name exactly" )
    return False

  regionName = funcs.RegionNameFromId(regionInt)
  if regionName == None:
    funcs.messageReply(message, "Your region is not supported. Go yell at the programmer responsible")
    return False

  playerBnetUrl = '{0}/{1}/{2}/'.format(playerInt, realm, playerName)
  print "getLeague(" + settings.regions[regionName][0] + ", " + playerBnetUrl + ")"
  leagueData = funcs.getLeague(settings.regions[regionName], playerBnetUrl)
  if not (leagueData):
    funcs.messageReply(message, "Error: {DD6B39E6-857C-11E3-9693-7A7328D43830}")
    return False

  f = open("accounts.txt","a")
  f.write('{0},{1},{2},\n'.format(playerBnetUrl, redditname, regionName))
  f.close()
  subreddit.flair.set('bboe', playerName, leagueData[0].title() + " "+regionName+" " + leagueData[1] + "-" + leagueData[2] + "-" + leagueData[3])
  funcs.messageReply(message, "Your flair has been set. Account link is a success!")
  return True



r = funcs.GetPraw()
subreddit = r.subreddit("AllThingsZerg")

inbox = r.inbox.unread()

filteredmessages = filter(funcs.isflairbotmessage,inbox)

map(handleMessage,filteredmessages)
