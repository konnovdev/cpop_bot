import io
import logging
import os
from aiogram import types
from aiogram.types import ParseMode
from pytube import YouTube
from urllib.request import urlopen
from PIL import Image
import config

logger = logging.getLogger(__name__)


# TODO move youtube logic into a separate class
class TextHandler:

    async def handle(self, message: types.Message):
        text = message.text
        if text and ('youtu.be' in text or 'youtube.com' in text):
            await self.__handleYoutubeDownload(message)
        elif text == 'ping':
            await message.reply('pong', reply=False)

    async def __handleYoutubeDownload(self, message: types.Message):
        if not str(message.chat.id) in config.WHITELIST_CHAT_ID:
            return
        try:
            yt = YouTube(message.text)
            author = yt.author
            length = yt.length
            title = yt.title
            stream = (yt.streams
                      .filter(only_audio=True, file_extension='mp4')
                      .order_by('bitrate').desc().first())
            filesize = stream.filesize
            telegram_audio_limit = 52428800

            if (filesize < telegram_audio_limit and length < 600):
                output_audiofile = stream.download("downloads")
                output_thumbnail = "downloads/square_thumbnail.jpg"
                self.__make_squarethumb(yt.thumbnail_url, output_thumbnail)
                with open(output_audiofile, "rb") as audio, \
                     open(output_thumbnail, "rb") as thumb:
                    await message.reply_audio(audio,
                                              duration=length,
                                              performer=author,
                                              title=title,
                                              thumb=thumb)
                os.remove(output_audiofile)
                os.remove(output_thumbnail)
            else:
                await message.reply("<code>No downloads for 10min+ audio" +
                                    "or file size greater than 50M</code>",
                                    parse_mode=ParseMode.HTML)
        except Exception as e:
            await message.reply("I've tried downloading this video but" +
                                "caught the following error: <code>" +
                                str(e) + "</code>.\n\n" +
                                "<b>Please report it to @konnov</b>",
                                parse_mode=ParseMode.HTML)

    # https://stackoverflow.com/a/52177551
    def __make_squarethumb(self, img_url, output):
        original_thumb = Image.open(urlopen(img_url))
        squarethumb = self.__crop_to_square(original_thumb)
        squarethumb.thumbnail((320,320), Image.ANTIALIAS)
        squarethumb.save(output)

    def __crop_to_square(self, img):
        width, height = img.size
        length = min(width, height)
        left = (width - length)/2
        top = (height - length)/2
        right = (width + length)/2
        bottom = (height + length)/2
        return img.crop((left, top, right, bottom))
