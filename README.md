# Mediatool 

I made this script to help me manage and organize media for my jellyfin server. Instead of having to juggle multiple tools and websites just to download 1 movie i decided i wanted to make a all in one tool to help me. It combines Real debrid downloads, omdb folder automation and library management into one clean cli. After i thought it was good enough i then decided to upload it here.

## Requirements
```
Python 3.9+ recommended
[Real Debrid Api Key](https://real-debrid.com/) (Its like 3$ for 15 days) 
OMDB Api Key (Its free)
```
## Install
### 1) Clone
git clone https://github.com/kalebdoesthings/mediatool.git
cd mediatool

### 2) Install Python packages
pip install -r requirements.txt

If you do not have a requirements.txt yet, install these:
pip install colorama requests simple-term-menu pyfiglet thefuzz beautifulsoup4

## First Run Setup
On first run, the tool will ask you for:
- Real-Debrid API key
- OMDb API key
- Media path (creates movies/ and tvshow/ folders)

Example media path:
  /home/youruser/media

It will generate a config file:
  config.ini

## config.ini format
The tool reads keys from the [CONFIG] section:

[CONFIG]
FIRST_LAUNCH = 0
REAL_DEBRID_API_KEY =
OMDB_API_KEY =
MEDIA_PATH =

FIRST_LAUNCH:
- 0 = run setup prompts
- 1 = skip setup and use saved config

## Run
python3 mediatool.py

## How to navigate menu

```
[m] Movies
    ├── Manual        | Use magnet links in this section
    └── RARBG Scrape  | Scrapes RARBG to find torrents for you

[t] TV Shows
    ├── Manual        | Use magnet links in this section
    └── RARBG Scrape  | Scrapes RARBG to find torrents for you
[s] Search
    ├── [m] Movies    | Lets you search your media library for similar media file names
    └── [q] Quit  | Goes back to main menu
[e] Edit Config
    ├── Allows you to edit your config
[q] Quit
    ├── Quits the menu
    
    
```.
