# KijijiReposter

A python3 script that uses Selenium to delete and repost all current Kijiji ads

## Installation

1. Run `pip install requirements.txt`
2. Download the Chrome driver [(link)](https://chromedriver.chromium.org/downloads) and place it in the `bin` directory of your venv environment 

## Setup
Posting an ad requires a root directory containing all ads in its subdirectories.  A config file named 'ad\_config.yaml'
should be present in each subdirectory (see example [ad\_config.yaml](example_ad/ad_config.yaml) file)

### Example Structure of Root Directory
rootdir
  |-ad1
  |--- ad\_config.yaml
  |--- img1.jpg
  |--- img2.jpg
  |-ad2
  |--- ad\_config.yaml
  |--- img1.jpg
  |--- img2.jpg
  |--- img3.jpg

### Cooke File
A cookie file is needed to sign in.  The required cookie is named `ssid`. It can be found after signing in by opening
Chrome Dev Tools and looking under `Application > Cookies > https://www.kijiji.ca/ > ssid`.  Copy its value and paste it into a text file

## Usage
usage: kijiji\_reposter.py [-h] -c COOKIE\_FILE [-r ROOTDIR] [-d] [-p] [-t] [-l LOG\_FILENAME]

Deletes all ads currently listed and reposts

optional arguments:
  -h, --help            show this help message and exit
  -c COOKIE\_FILE, --cookie\_file COOKIE\_FILE
                        Filename of text file containing SSID cookie used for signing in
  -r ROOTDIR, --rootdir ROOTDIR
                        Root directory containing ad config files in subdirectories
  -d, --delete\_all      Flag to delete all currently posted ads
  -p, --post            Flag to post ads
  -t, --track\_stats     Flag for whether to track views/replies when ads are deleted
  -l LOG\_FILENAME, --log\_filename LOG\_FILENAME
                        File to log all events to


### Example
Use `-d` and `-p` flags to separately delete all ads and post all ads respectively, e.g.,

`python kijiji\_reposter.py -r rootdir -c cookie.txt -d`

`python kijiji\_reposter.py -r rootdir -c cookie.txt -p`

## Supported Web Elements
This project uses the Selenium Page Objects design pattern and only a few web elements are currently supported.  These
elements can be configured in the ad\_config.yaml file with the following keys (see example [ad\_config.yaml](example_ad/ad_config.yaml) file)

* adTitle
* cashless
* categoryId
* curbSide
* description
* imgs
* price
* size
