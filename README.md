# Mediatool 

I made this to make torrenting media for my jellyfin server easier and i decided i would upload it here so anyone can use it.

## Requirements
Python 3.9+ recommended

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

## Notes / Warnings
- Keep config.ini private (do NOT commit it to GitHub).
- Do not hardcode API keys in the code.
- If you publish this repo, add config.ini to .gitignore.

## Troubleshooting
### "FIRST_LAUNCH KeyError"
Your config.ini is missing [CONFIG] or FIRST_LAUNCH.
Delete config.ini and rerun to regenerate it.

### "Permission denied" creating folders
Make sure your MEDIA_PATH exists and you have write permissions.
