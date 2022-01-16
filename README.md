# tgbot

A Telegram bot made with [Pyrogram Smart Plugins](https://docs.pyrogram.org/topics/smart-plugins)

## Features
- Get audio from a YouTube video - just send the video link, the bot will convert the music automatically.
- Get current weather with **OpenWeatherApi** - use `/weather city`
- Get a **wolframalpha** answer for the question - use `/wf your query`
- Look up a word in **cedict** (Chinese/English dictionary) - use `/dic word`

## Requirements

- Python 3.6 or higher
- A [Telegram API key](//docs.pyrogram.org/intro/setup#api-keys)
- A [Telegram bot token](//t.me/botfather)

## Run with venv

1. `virtualenv venv` to create a virtual environment
2. install `python3-devel zlib-devel libjpeg-turbo-devel libwebp-devel`,
   clear cache of pip (`~/.cache/pip` on linux distro)
   for building wheel for Pillow. with apt:
   `apt install -y python3-dev zlib1g-dev libjpeg-turbo8-dev libwebp-dev`
3. `venv/bin/pip install -U -r requirements.txt` to install the requirements
4. Create a new `config.ini` file, copy-paste the following and replace with your own
   values:
```
   [pyrogram]
   api_id = 1234567
   api_hash = 0123456789abcdef0123456789abcdef
   bot_token = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

   [plugins]
   root = plugins
```
   Create `config.py` and add constants that are specified in config_example.py
5. Run with `venv/bin/python tgbot.py`
6. Stop with <kbd>CTRL+C</kbd>

## Run with docker

1. Install docker and docker-compose
2. Open the project directory in terminal and run `docker-compose up -d`
3. You can stop the bot by executing `docker-compose down` (you must be in the project directory) 

## License

AGPL-3.0-or-later
