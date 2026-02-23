# Mediatool

I created this script to help manage and organize media for my Jellyfin server. Instead of juggling multiple tools and websites just to download a single movie, I wanted an all-in-one CLI utility that streamlined the entire process.

Mediatool combines Real-Debrid downloads, OMDb folder automation, and local library management into a single, clean command-line interface. Once it was stable and working well, I decided to share it here so others can use or improve it.

---

## Requirements

- Python 3.9+ recommended  
- [Real-Debrid API Key](https://real-debrid.com/) (~$3 for 15 days)  
- OMDb API Key (Free)  

---

## Quick Install (One Command)

On Linux (Debian/Ubuntu-based), copy and paste:

```bash
git clone https://github.com/kalebdoesthings/mediatool.git && \
cd mediatool && \
chmod +x setup.sh && \
./setup.sh
```
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
