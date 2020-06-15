import io
import logging
import os
from aiogram import types
from aiogram.types import ParseMode
from pytube import YouTube

logger = logging.getLogger(__name__)


class TextHandler:

    async def handle(self, message: types.Message):
        text = message.text
        if text and ('youtu.be' in text or 'youtube.com' in text):
            await self.__handleYoutubeDownload(message)
        elif text == 'ping':
            await message.reply('pong', reply=False)

    async def __handleYoutubeDownload(self, message: types.Message):
        try:
            yt = YouTube(message.text)
            author = yt.author
            length = yt.length
            title = yt.title
            stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('bitrate').desc().first()
            filesize = stream.filesize
            telegram_audio_limit = 52428800
            if (filesize < telegram_audio_limit and length < 600):
                output_filename = stream.download("downloads")
                with open(output_filename, "rb") as f:
                    await message.reply_audio(f, duration=length, performer=author, title=title)
                os.remove(output_filename)
            else:
                await message.reply("<code>No downloads for 10min+ audio or file size greater than 50M</code>",
                                    parse_mode=ParseMode.HTML)
        except Exception as e:
            await message.reply("I've tried downloading this video but caught the "
                                "following error: " + str(e) + ".\n\n<b>Please report it to @konnov</b>",
                                parse_mode=ParseMode.HTML)
