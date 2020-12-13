import os
import logging
import asyncio
from aiogram import types, Bot
from aiogram.types import ParseMode
import music_grabber
import config

telegram_audio_limit = 52428800
music_sites = ("youtu.be/", "youtube.com/watch?v=", "soundcloud.com/")
WHITELIST_CHAT_ID = config.WHITELIST_CHAT_ID
AVAILABILITY_HTML = config.AVAILABILITY_HTML
GROUP_CHAT_ID = config.GROUP_CHAT_ID
DOWNLOAD_DIR = config.DOWNLOAD_DIR

logger = logging.getLogger(__name__)
musicDownloader = music_grabber.MusicDownloader()
squarethumbMaker = music_grabber.SquarethumbMaker()


class TextHandler:

    def __init__(self, bot: Bot):
        self.bot = bot

    async def handle(self, message: types.Message):
        if not await self.__isProvideService(message):
            return
        text = message.text
        if text and (' ' not in text and '\n' not in text) \
                and any(site in text for site in music_sites):
            await self.__handleMusicGrabber(message)
        elif text == 'ping':
            await message.reply('pong', reply=False)

    async def __isProvideService(self, message: types.Message):
        chat_id = message.chat.id
        if chat_id in WHITELIST_CHAT_ID:
            return True
        chat_type = message.chat.type
        if chat_type == "private":
            member = await self.bot.get_chat_member(GROUP_CHAT_ID, chat_id)
            if member.is_chat_member():
                return True
            else:
                await message.reply(AVAILABILITY_HTML,
                                    parse_mode=ParseMode.HTML)
                return False
        else:
            return False

    async def __handleMusicGrabber(self, message: types.Message):
        try:
            info = musicDownloader.download(message.text,
                                            telegram_audio_limit)
            downloads = info['downloads']
            audio_file = downloads['audio']
            thumbnail_file = downloads['thumbnail']
            squarethumb_file = DOWNLOAD_DIR + \
                info['extractor'] + info['id'] + "_squarethumb.jpg"
            squarethumbMaker.make_squarethumb(thumbnail_file,
                                              squarethumb_file)
            with open(audio_file, "rb") as audio, \
                 open(squarethumb_file, "rb") as thumb:
                title = info['title']
                url = info['webpage_url']
                performer = info['uploader']
                duration = int(float(info['duration']))
                caption = "<b><a href=\"" + url + "\">" + title + "</a></b>"
                await types.ChatActions.upload_document()
                if message.chat.type == "private":
                    keep_message = False
                else:
                    keep_message = True
                await message.reply_audio(audio,
                                          caption=caption,
                                          parse_mode=ParseMode.HTML,
                                          duration=duration,
                                          performer=performer,
                                          title=title,
                                          thumb=thumb,
                                          reply=keep_message)
            for f in audio_file, thumbnail_file, squarethumb_file:
                os.remove(f)
            if not keep_message:
                await message.delete()
        except music_grabber.WrongFileSizeError as e:
            logger.error(str(e))
            inform = await message.reply("This won't be downloaded because "
                                         "its audio file size is greater "
                                         "than 50M",
                                         disable_notification=True)
            await self.__deleteMessage(60, inform)
        except music_grabber.WrongCategoryError as e:
            logger.error(str(e))
        except Exception as e:
            await message.reply("<b>Error</b>: <code>" + str(e) +
                                "</code>", parse_mode=ParseMode.HTML,
                                disable_notification=True)

    async def __deleteMessage(self, delay, message):
        await asyncio.sleep(delay)
        await message.delete()
