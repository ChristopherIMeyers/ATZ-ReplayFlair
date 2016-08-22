ATZ-ReplayFlair [![Build Status](https://travis-ci.org/ChristopherIMeyers/ATZ-ReplayFlair.svg?branch=master)](https://travis-ci.org/ChristopherIMeyers/ATZ-ReplayFlair)
===============
* replay flair system running on /r/allthingszerg
* parses replays to figure out battle.net account and reddit account names
* supports AM/EU/KR
* drop.sc and ggtracker.com support

Update Server
---
```bash
sudo pip install --upgrade pip
sudo pip install mpyq
```

Update Script on Server
---
```bash
cp replayflair/settings.py settings.py
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
```
