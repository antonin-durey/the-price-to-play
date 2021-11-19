# The price to play

**Artifact for The Web Conference submission #3001 "The Price to Play: a Privacy Analysis of Free and Paid Games in the Android Ecosystem"**

This repository contains 4 resources:

- `app_ids.csv` contains the list of game IDs we used for our study, and the source we used to collect the game files (either AndroZoo or Google's Play Pass)
- `android-zoo-apk-collector.py` collects the files of the games listed in `app_ids.csv`  with the `android_zoo` source. The downloaded apks will be placed in the `data/androzoo_apks` folder.
This script requires:
  - you put in an environment variable your AndroZoo key (https://androzoo.uni.lu/access),
  - and that you download the list of apps contained in the AndroZoo dataset in a file named `latest.csv` that you place in this directory.
- `google-play-pass-apk-collector.py` monitors a smartphone via the `adb` tool to automatically install a game, download its files and uninstall it.
The downloaded apks will be placed in the `data/play_pass_apks` folder
- `metadata-collector.py` collects the information available on the Play Store page of the game and stores them in a json file. The generated json files are available in the `data/json` folder.