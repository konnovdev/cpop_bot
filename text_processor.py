import io
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.base import InputFile
from pytube import YouTube

logger = logging.getLogger(__name__)


class TextProcessor:

    async def handle(self, message: types.Message):
        text = message.text
        if text and ('youtu.be' in text or 'youtube.com' in text):
            await self.__handle_youtube_download(message)
        elif text == 'ping':
            await message.reply('pong', reply=False)

    async def __handle_youtube_download(self, message: types.Message):
        try:
            yt = YouTube(message.text)
            stream = yt.streams.filter(only_audio=True).first()
            output_filename = stream.download("downloads")
            base, ext = os.path.splitext(output_filename)
            new_filename = base + ".mp3"
            os.rename(output_filename, new_filename)
            file = open(new_filename, "rb")
            telegram_audio_limit = 52428800
            file_size = os.path.getsize(new_filename)
            if file_size < telegram_audio_limit:
                await message.reply_audio(io.BytesIO(file.read()),
                                          performer="unknown",
                                          title=new_filename.split("downloads/")[1])
            else:
                await message.reply("The linked video has been successfully downloaded, however, its "
                                    "audio file has the size of " + str(file_size) + " bytes. " +
                                    "Bots can currently send files of any type of only up to 50 MB " +
                                    "in size (52428800 bytes)")
            os.remove(new_filename)
        except Exception as e:
            logger.error(str(e) + ", failed to download: " + message.text)
