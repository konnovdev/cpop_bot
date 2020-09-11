import io
import logging
import os
from aiogram import types
from aiogram.types import ParseMode
from pytube import YouTube
from pytube import extract
from urllib.request import urlopen
from PIL import Image
import config

logger = logging.getLogger(__name__)


# TODO move youtube logic into a separate class
class TextHandler:

    async def handle(self, message: types.Message):
        text = message.text
        if text and (' ' not in text and '\n' not in text) \
                and ('youtu.be' in text or 'youtube.com' in text):
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
            video_id = extract.video_id(message.text)
            video_url = "youtu.be/" + video_id
            telegram_audio_limit = 52428800

            if (filesize < telegram_audio_limit and length < 600):
                output_audiofile = stream.download(output_path = "downloads/",
                                                   filename = title +
                                                              " - YouTube - " +
                                                              video_id)
                output_thumbnail = "downloads/square_thumbnail_" + video_id + \
                                   ".jpg"
                self.__make_squarethumb(yt.thumbnail_url, output_thumbnail)
                with open(output_audiofile, "rb") as audio, \
                     open(output_thumbnail, "rb") as thumb:
                    await message.reply_audio(audio,
                                              caption="<a href=\"" + video_url +
                                                      "\">" + title + "</a>",
                                              parse_mode=ParseMode.HTML,
                                              duration=length,
                                              performer=author,
                                              title=title,
                                              thumb=thumb)
                os.remove(output_audiofile)
                os.remove(output_thumbnail)
            else:
                await message.reply("`No downloads for 10min\+ audio " +
                                    "or file size greater than 50M`",
                                    parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            await message.reply("I've tried downloading this video but " +
                                "caught the following error: `" +
                                str(e) + "`\.\n\n" +
                                "*Please report it to @konnov*",
                                parse_mode=ParseMode.MARKDOWN_V2)

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
