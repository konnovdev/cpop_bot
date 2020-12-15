import logging
from aiogram import types
from aiogram.types import ParseMode
from config import ABOUT_HTML, HELP_HTML

logger = logging.getLogger(__name__)


class CommandHandler:

    async def handle(self, bot_username, message: types.Message):
        if message.text in ("/about", "about@" + bot_username):
            await self.__handle_about(message)
        elif message.text in ("/help", "/help@" + bot_username):
            await self.__handle_help(message)
        elif message.text == "/start":
            await self.__handle_start(message)
        else:
            logger.debug("USER TYPED UNKNOWN COMMAND " + message.text)

    async def __handle_about(self, message):
        await message.reply(text=ABOUT_HTML, parse_mode=ParseMode.HTML)

    async def __handle_help(self, message):
        await message.reply(text=HELP_HTML, parse_mode=ParseMode.HTML)

    async def __handle_start(self, message):
        with open('static/hello_animated_sticker.tgs', 'rb') as sticker:
            await message.reply_sticker(sticker)
