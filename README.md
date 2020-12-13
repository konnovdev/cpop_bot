## Bot to manage telegram chat cpop.tw

Features:

* downloads youtube video when you send the link
* makes every new member go through captcha

### Set up

- create `config.py` (check `config_example.py`)
- install `libwebp-devel`, clear cache of pip (`~/.cache/pip` on linux distro) for building wheel for Pillow
- setup virtualenv and install dependencies

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Run the bot

`$ python3 main.py`
