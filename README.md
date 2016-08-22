ATZ-ReplayFlair [![Build Status](https://travis-ci.org/ChristopherIMeyers/ATZ-ReplayFlair.svg?branch=master)](https://travis-ci.org/ChristopherIMeyers/ATZ-ReplayFlair)
===============
* replay flair system running on /r/allthingszerg
* parses replays to figure out battle.net account and reddit account names
* supports AM/EU/KR
* drop.sc and ggtracker.com support

Update Script on Server
---
```bash
cp replayflair/settings.py settings.py
rm -r replayflair
wget https://github.com/ChristopherIMeyers/ATZ-ReplayFlair/archive/master.zip
unzip master.zip
rm master.zip
mv ATZ-ReplayFlair-master replayflair
mv settings.py replayflair/settings.py
```
