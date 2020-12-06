import logging
from aiogram import types
from aiogram.types import ParseMode
import config

logger = logging.getLogger(__name__)
HELP = config.help_text


class CommandHandler:
    async def handle(self, message: types.Message):
        if message.text == "/help" or message.text == "/help@cpop_bot":
            await self.__handleHelp(message)
        if message.text == "/start":
            await self.__handleStart(message)
        else:
            logger.debug("USER TYPED UNKNOWN COMMAND " + message.text)

    async def __handleHelp(self, message):
        await message.reply(text=HELP, parse_mode=ParseMode.HTML)

    async def __handleStart(self, message):
        sticker = open('static/hello_animated_sticker.tgs', 'rb')
        await message.reply_sticker(sticker)
