import logging
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CommandProcessor:
    async def handle(self, message: types.Message):
        if message.text == "/help":
            await message.reply(text="this bot is going to manage cpop.tw. "
                                     "Help info will be available later",
                                reply=False)

        if message.text == "/start":
            sticker = open('static/hello_animated_sticker.tgs', 'rb')
            await message.reply_sticker(sticker)

        else:
            logger.debug("USER TYPED UNKNOWN COMMAND " + message.text)
