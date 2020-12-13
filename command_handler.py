import logging
from aiogram import types
from aiogram.types import ParseMode
import config

logger = logging.getLogger(__name__)
ABOUT_HTML = config.ABOUT_HTML
HELP_HTML = config.HELP_HTML


class CommandHandler:

    async def handle(self, bot_username, message: types.Message):
        if message.text in ("/about", "about@" + bot_username):
            await self.__handleAbout(message)
        elif message.text in ("/help", "/help@" + bot_username):
            await self.__handleHelp(message)
        elif message.text == "/start":
            await self.__handleStart(message)
        else:
            logger.debug("USER TYPED UNKNOWN COMMAND " + message.text)

    async def __handleAbout(self, message):
        await message.reply(text=ABOUT_HTML, parse_mode=ParseMode.HTML)

    async def __handleHelp(self, message):
        await message.reply(text=HELP_HTML, parse_mode=ParseMode.HTML)

    async def __handleStart(self, message):
        with open('static/hello_animated_sticker.tgs', 'rb') as sticker:
            await message.reply_sticker(sticker)
