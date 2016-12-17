ATZ-ReplayFlair [![Build Status](https://travis-ci.org/ChristopherIMeyers/ATZ-ReplayFlair.svg?branch=master)](https://travis-ci.org/ChristopherIMeyers/ATZ-ReplayFlair)
===============
* replay flair system running on /r/allthingszerg
* parses replays to figure out battle.net account and reddit account names
* supports AM/EU/KR
* drop.sc and ggtracker.com support

Update Server
---
```bash
sudo python -m pip install --upgrade pip
sudo python -m pip install mpyq
sudo python -m pip install BeautifulSoup4
sudo python -m pip install praw
```

Update Script on Server
---
```bash
cp replayflair/accounts.txt accounts.txt
cp replayflair/settings.py settings.py
cp replayflair/current.iteration.txt current.iteration.txt
rm -r replayflair
wget https://github.com/ChristopherIMeyers/ATZ-ReplayFlair/archive/master.zip
unzip master.zip
rm master.zip
mv ATZ-ReplayFlair-master replayflair
wget https://github.com/Blizzard/s2protocol/archive/master.zip
unzip master.zip
rm master.zip
mv s2protocol-master replayflair/s2protocol
mv settings.py replayflair/settings.py
mv accounts.txt replayflair/accounts.txt
mv current.iteration.txt replayflair/current.iteration.txt
mkdir replayflair/tmp
```
