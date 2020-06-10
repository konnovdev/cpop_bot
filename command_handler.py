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
        await message.reply(text="this bot is going to manage cpop.tw.\n"
                                 "For now it converts a youtube video to mp3 "
                                 "whenever you send a link and makes new members "
                                 "go through captcha.\n\n<b>Notice</b> if you don't "
                                 "want the video to be downloaded, just make the link "
                                 " follow a command, for example <code>/test "
                                 "youtu.be/somevid</code>. This will <b>not</b> "
                                 "download the video. \n\n<i>This bot is open source, "
                                 "the source code is available at</i> "
                                 "cpop.tw/code", parse_mode=ParseMode.HTML)

    async def __handleStart(self, message):
        sticker = open('static/hello_animated_sticker.tgs', 'rb')
        await message.reply_sticker(sticker)
