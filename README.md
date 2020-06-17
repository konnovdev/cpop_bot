## Bot to manage telegram chat cpop.tw

Features:

* downloads youtube video when you send the link
* makes every new member go through captcha

### Set up

Create config.py to specify your Telegram Bot token

```
ACCESS_TOKEN = "bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
WHITELIST_CHAT_ID = ['2011545269', '8557378983', '-1001853277651']
```

Setup virtualenv and install dependencies

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Apply patches

```
$ for patch in patch/*.patch; do patch -d venv/lib/python3.*/site-packages -p1 <$patch; done
$ ## Or manually apply each patch like this
$ ## patch -d venv/lib/python3.*/site-packages -p1 <patch/pytube3.patch
```

Run the bot

`$ python3 main.py`
