import unittest
import praw

class Tests(unittest.TestCase):
  def test_praw(self):
    r = praw.Reddit(user_agent='r/allthingszerg replay flair bot')
    frontpage = r.get_front_page()
    self.assertEqual(sum(1 for _ in frontpage), 25)

if __name__ == '__main__':
  unittest.main()
