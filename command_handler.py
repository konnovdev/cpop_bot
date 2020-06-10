import logging
from aiogram import Bot, Dispatcher, executor, types

logger = logging.getLogger(__name__)


class CommandHandler:
    async def handle(self, message: types.Message):
        if message.text == "/help":
            await self.__handleHelp(message)
        if message.text == "/start":
            await self.__handleStart(message)
        else:
            logger.debug("USER TYPED UNKNOWN COMMAND " + message.text)

    async def __handleHelp(self, message):
        await message.reply(text="this bot is going to manage cpop.tw.\n"
                                 "For now it converts a youtube video to mp3 "
                                 "whenever you send a link and makes new members"
                                 "go through captcha",
                            reply=False)

    async def __handleStart(self, message):
        sticker = open('static/hello_animated_sticker.tgs', 'rb')
        await message.reply_sticker(sticker)
