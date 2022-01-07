"""music.py"""
# Chats where the users can download music from video services
# and additional users that need to use the music downloader
# feature but are not in any chat
MUSIC_CHATS = ["foo_group_username", -100123456789]
# MUSIC_USERS should be list of str ("username") or int (ID)
MUSIC_USERS = [53257673]
# leave it as an empty array
# if you want it to work in all the chats：
# MUSIC_CHATS = []
# MUSIC_USERS = []


"""welcome_captcha.py"""
# Chats where the bot will give a captcha for every new user
WELCOME_CAPTCHA_CHATS = ['1234567', '954534212']
# leave it as an empty array if you want this feature
# to work everywhere where the bot is admin
# WELCOME_CAPTCHA_CHATS = []

"""tools/weather.py"""
# Get API token from https://home.openweathermap.org/
# to get the bot fetch the weather
OPENWEATHER_API = "23141234awe124124"

"""tools/wolfram.py"""
# Get API token from https://developer.wolframalpha.com/
# to get the bot to query wolframalpha.com
WOLFRAMALPHA_API = "23141234awe124124"
