# coding=utf-8

import unittest
import praw
import funcs
import os

class Struct:
  def __init__(self, **entries): self.__dict__.update(entries)

class Tests(unittest.TestCase):
  if os.path.exists('settings.py'):
    def test_praw(self):
      r = funcs.GetPraw()
      frontpage = r.front.hot()
      self.assertEqual(sum(1 for _ in frontpage), 100)

    def test_flairInstructionsAreUpToDate(self):
      r = funcs.GetPraw()
      subreddit = r.subreddit('allthingszerg')
      wikipage = subreddit.wiki['flair']
      liveContent = wikipage.content_md
      srcContent = open('flairinstructions.md', 'r').read()
      cleanedLiveContent = liveContent.replace('\r', '')
      cleanedLiveContent = cleanedLiveContent.replace('&lt;', '<')
      cleanedLiveContent = cleanedLiveContent.replace('&gt;', '>')
      cleanedLiveContent = cleanedLiveContent.replace('&amp;', '&')

      self.assertEqual(cleanedLiveContent, srcContent)

  def test_isDropScMessageBodyValidLink(self):
    inValid = Struct(body = "blahblahblah")
    validSimple = Struct(body = "drop.sc/replay/1234")
    validSimpleWithHttp = Struct(body = "http://drop.sc/replay/1234")
    validSimpleWithHttps = Struct(body = "https://drop.sc/replay/1234")
    validNested = Struct(body = " wee drop.sc/replay/1234 wee")
    validNestedWithHttp = Struct(body = " wee http://drop.sc/replay/1234 wee")
    self.assertEqual(funcs.isMessageBodyValidLink(inValid), False)
    self.assertEqual(funcs.isMessageBodyValidLink(validSimple), "http://sc2replaystats.com/download/1234")
    self.assertEqual(funcs.isMessageBodyValidLink(validSimpleWithHttp), "http://sc2replaystats.com/download/1234")
    self.assertEqual(funcs.isMessageBodyValidLink(validSimpleWithHttps), "http://sc2replaystats.com/download/1234")
    self.assertEqual(funcs.isMessageBodyValidLink(validNested), "http://sc2replaystats.com/download/1234")
    self.assertEqual(funcs.isMessageBodyValidLink(validNestedWithHttp), "http://sc2replaystats.com/download/1234")

  def test_isGGTrackerMessageBodyValidLink(self):
    inValid = Struct(body = "blahblahblah")
    validSimple = Struct(body = "ggtracker.com/matches/1234")
    validSimpleWithD = Struct(body = "ggtracker.com/matches/1234/replay")
    validNested = Struct(body = " wee ggtracker.com/matches/1234 wee")
    validNestedWithD = Struct(body = " wee ggtracker.com/matches/1234/replay wee")
    self.assertEqual(funcs.isMessageBodyValidLink(inValid), False)
    self.assertEqual(funcs.isMessageBodyValidLink(validSimple), "http://ggtracker.com/matches/1234/replay")
    self.assertEqual(funcs.isMessageBodyValidLink(validSimpleWithD), "http://ggtracker.com/matches/1234/replay")
    self.assertEqual(funcs.isMessageBodyValidLink(validNested), "http://ggtracker.com/matches/1234/replay")
    self.assertEqual(funcs.isMessageBodyValidLink(validNestedWithD), "http://ggtracker.com/matches/1234/replay")

  def test_accountFileLoads(self):
    actualAccountMaps = funcs.readAccountsFile("accounts_mock.txt")
    expectedAccountMaps = [
      {'bnet': '1234567/1/FirstTester/', 'region': 'EU', 'redditName': 'redditguy1'},
      {'bnet': '2345678/1/SecondTester/', 'region': 'AM', 'redditName': 'redditguy2'}
    ]
    self.assertEqual(actualAccountMaps, expectedAccountMaps)

  def test_getLeagueFromSource(self):
    pageSource = open("testdata/rank1gm.html", "r").read()
    self.assertEqual(funcs.getLeagueFromSource(pageSource), "grandmaster")
    pageSource = open("testdata/missing.html", "r").read()
    self.assertEqual(funcs.getLeagueFromSource(pageSource), "banned")
    pageSource = open("testdata/none.used.to.be.gm.html", "r").read()
    self.assertEqual(funcs.getLeagueFromSource(pageSource), "none")
    pageSource = open("testdata/diamond.html", "r").read()
    self.assertEqual(funcs.getLeagueFromSource(pageSource), "diamond")
    with self.assertRaises(IndexError):
      funcs.getLeagueFromSource("invalid junk")
    self.assertEqual(open("last.failure.txt", "r").read(), "invalid junk")
    os.remove("last.failure.txt")

  def test_stripOutClan(self):
    self.assertEqual(funcs.stripOutClan("nomatch"), "nomatch")
    self.assertEqual(funcs.stripOutClan("<fakeclan><sp/>withclan"), "withclan")
    self.assertEqual(funcs.stripOutClan("<fakeclan>nomatch"), "<fakeclan>nomatch")
    self.assertEqual(funcs.stripOutClan("[fakeclan]<sp/>withclan"), "withclan")
    self.assertEqual(funcs.stripOutClan("[fakeclan]nomatch"), "[fakeclan]nomatch")
    self.assertEqual(funcs.stripOutClan("<fakeclanǂ><sp/>withclan"), "withclan")
    self.assertEqual(funcs.stripOutClan("[[fakeclan]]nomatch"), "[[fakeclan]]nomatch")
    self.assertEqual(funcs.stripOutClan("<<fakeclan>>nomatch"), "<<fakeclan>>nomatch")
    self.assertEqual(funcs.stripOutClan("&lt;fakeclanǂ&gt;<sp/>withclan"), "withclan")


if __name__ == '__main__':
  unittest.main()
