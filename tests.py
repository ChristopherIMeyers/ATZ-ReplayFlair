import unittest
import praw
import funcs

class Struct:
  def __init__(self, **entries): self.__dict__.update(entries)

class Tests(unittest.TestCase):
  def test_praw(self):
    r = praw.Reddit(user_agent = 'r/allthingszerg replay flair bot')
    frontpage = r.get_front_page()
    self.assertEqual(sum(1 for _ in frontpage), 25)

  def test_isMessageBodyValidLink(self):
    inValid = Struct(body = "blahblahblah")
    validSimple = Struct(body = "drop.sc/1234")
    validSimpleWithD = Struct(body = "drop.sc/1234/d")
    validNested = Struct(body = " wee drop.sc/1234 wee")
    validNestedWithPass = Struct(body = " wee drop.sc/1234?pass=abcdef-789 wee")
    validNestedWithD = Struct(body = " wee drop.sc/1234/d wee")
    validNestedWithDAndPass = Struct(body = " wee drop.sc/1234/d?pass=abcdef-789 wee")
    self.assertEqual(funcs.isMessageBodyValidLink(inValid), False)
    self.assertEqual(funcs.isMessageBodyValidLink(validSimple), "http://drop.sc/1234/d")
    self.assertEqual(funcs.isMessageBodyValidLink(validSimpleWithD), "http://drop.sc/1234/d")
    self.assertEqual(funcs.isMessageBodyValidLink(validNested), "http://drop.sc/1234/d")
    self.assertEqual(funcs.isMessageBodyValidLink(validNestedWithPass), "http://drop.sc/1234/d?pass=abcdef-789")
    self.assertEqual(funcs.isMessageBodyValidLink(validNestedWithD), "http://drop.sc/1234/d")
    self.assertEqual(funcs.isMessageBodyValidLink(validNestedWithDAndPass), "http://drop.sc/1234/d?pass=abcdef-789")

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

  def test_stripOutClan(self):
    self.assertEqual(funcs.stripOutClan("nomatch"), "nomatch")
    self.assertEqual(funcs.stripOutClan("<fakeclan><sp/>withclan"), "withclan")
    self.assertEqual(funcs.stripOutClan("<fakeclan>nomatch"), "<fakeclan>nomatch")
    self.assertEqual(funcs.stripOutClan("[fakeclan]<sp/>withclan"), "withclan")
    self.assertEqual(funcs.stripOutClan("[fakeclan]nomatch"), "[fakeclan]nomatch")

if __name__ == '__main__':
  unittest.main()
