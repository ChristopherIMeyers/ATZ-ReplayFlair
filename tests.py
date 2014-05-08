import unittest
import praw
import funcs

class Struct:
  def __init__(self, **entries): self.__dict__.update(entries)

class Tests(unittest.TestCase):
  def test_praw(self):
    r = praw.Reddit(user_agent='r/allthingszerg replay flair bot')
    frontpage = r.get_front_page()
    self.assertEqual(sum(1 for _ in frontpage), 25)

  def test_isMessageBodyValidLink(self):
    inValid = Struct(body="blahblahblah")
    validSimple = Struct(body="drop.sc/1234")
    validSimpleWithD = Struct(body="drop.sc/1234/d")
    validNested = Struct(body=" wee drop.sc/1234 wee")
    validNestedWithD = Struct(body=" wee drop.sc/1234/d wee")
    self.assertEqual(funcs.isMessageBodyValidLink(inValid), False)
    self.assertEqual(funcs.isMessageBodyValidLink(validSimple), "http://drop.sc/1234/d")
    self.assertEqual(funcs.isMessageBodyValidLink(validSimpleWithD), "http://drop.sc/1234/d")
    self.assertEqual(funcs.isMessageBodyValidLink(validNested), "http://drop.sc/1234/d")
    self.assertEqual(funcs.isMessageBodyValidLink(validNestedWithD), "http://drop.sc/1234/d")


if __name__ == '__main__':
  unittest.main()
