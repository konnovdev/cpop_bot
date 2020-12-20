# Get the access token from @BotFather
ACCESS_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"

DEV_ID = 2011545269  # errors will be forwarded to this user ID

# Members of these chats can use the bot in private.
# Group chat IDs always start with `-`
PROMOTION_LIST_CHAT_ID = (
    -1001853277651,
    -1001748900794
)

WHITELIST_CHAT_ID = PROMOTION_LIST_CHAT_ID + (
    DEV_ID,
    8557378983
)

# Configure a response to `/help` message
AVAILABILITY_HTML = ("This bot only serves cpop.tw group @mandopop and its "
                     "group members in private chat.")
CONTACTS_HTML = ("Regarding any issues with the bot feel free to contact "
                 "@konnov")
ABOUT_HTML = ("This bot is going to manage cpop.tw.\n"
              "For now it downloads music from YouTube or SoundCloud "
              "whenever you send the link and makes new members go through "
              "captcha." + "\n\n"
                           "<i>Source code available at cpop.tw/code under GPLv3 "
                           "license</i>\n\n" +
              CONTACTS_HTML)
HELP_HTML = (AVAILABILITY_HTML + "\n\n"
                                 "<b>Usage</b>:\n"
                                 "- send a message that only contains a link of a YouTube video "
                                 "or a SoundCloud track.\n"
                                 "- Playlists are not supported, but you can select multiple "
                                 "audio messages and forward them to create playlist instead.\n"
                                 "- Your message will be deleted in private chat after the music "
                                 "gets successfully uploaded.\n"
                                 "- You can get YouTube links with inline bot @vid and use "
                                 "them.\n\n" +
             CONTACTS_HTML)

# Music will be temporary downloaded to this destination
# and then automatically deleted once the bot uploaded it
# to telegram
DOWNLOAD_DIR = "/tmp/cpop_bot/"


"""
 Admin features
"""
# After selected time the captcha message will be deleted
USER_CAPTCHA_TIMEOUT_IN_MINUTES = 5

# If `True` the bot will delete `*** joined the group` type of messages
DELETE_JOIN_MESSAGE = True
