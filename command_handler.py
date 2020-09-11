import logging
from aiogram import types
from aiogram.types import ParseMode

logger = logging.getLogger(__name__)


class CommandHandler:
    async def handle(self, message: types.Message):
        if message.text == "/help" or message.text == "/help@cpop_bot":
            await self.__handleHelp(message)
        if message.text == "/start":
            await self.__handleStart(message)
        else:
            logger.debug("USER TYPED UNKNOWN COMMAND " + message.text)

    async def __handleHelp(self, message):
        await message.reply(text="This bot is going to manage cpop\.tw\.\n"
                                 "For now it downloads music from YouTube "
                                 "whenever you send the link and makes new "
                                 "members go through captcha\.\n\n"
                                 "*Notice:* the YouTube audio feature is "
                                 "*only* available for the chats that are in "
                                 "the bot\'s whitelist\. To download audio "
                                 "from YouTube, you need to send a message "
                                 "which contains the YouTube link only\.\n\n"
                                 "_This bot is open source, the source code "
                                 "is available at_ cpop\.tw\n\n"
                                 "Regarding any issues with the bot feel free "
                                 "to contact @konnov", parse_mode=ParseMode.MARKDOWN_V2)

    async def __handleStart(self, message):
        sticker = open('static/hello_animated_sticker.tgs', 'rb')
        await message.reply_sticker(sticker)
