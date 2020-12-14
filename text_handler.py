import os
import logging
import asyncio
from aiogram import types, Bot
from aiogram.types import ParseMode
import music_grabber
import config
from constants import ERROR_REPORT, ERROR_DELETE

telegram_audio_limit = 52428800
music_sites = ("youtu.be/", "youtube.com/watch?v=", "soundcloud.com/")
WHITELIST_CHAT_ID = config.WHITELIST_CHAT_ID
AVAILABILITY_HTML = config.AVAILABILITY_HTML
GROUP_CHAT_ID = config.GROUP_CHAT_ID
DOWNLOAD_DIR = config.DOWNLOAD_DIR
DEV_ID = config.DEV_ID

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
            text = "This won't be downloaded because its audio file size " + \
                "greater than 50M"
            inform = await message.reply(text, disable_notification=True)
            await self.__delete_message(60, inform)
        except music_grabber.WrongCategoryError as e:
            logger.error(str(e))
        except Exception as e:
            markup = self.__make_inline_keyboard()
            error_html = "<b>URL</b>: " + message.text + \
                "\n<b>Error</b>: <code>" + str(e) + "</code>"
            await message.reply(error_html, parse_mode=ParseMode.HTML,
                                disable_web_page_preview=True,
                                disable_notification=True, reply_markup=markup)

    def __make_inline_keyboard(self):
        markup = types.InlineKeyboardMarkup(reasize_keyboard=True)
        item1 = types.InlineKeyboardButton("Report Error",
                                           callback_data=ERROR_REPORT)
        item2 = types.InlineKeyboardButton("Delete Only",
                                           callback_data=ERROR_DELETE)
        markup.add(item1, item2)
        return markup

    async def callback_error_message(self, callback: types.CallbackQuery):
        from_chat_id = callback.message.chat.id
        message_id = callback.message.message_id
        callback_data = callback.data
        if callback_data == ERROR_REPORT:
            answer_text = "Successfully forward the error message to dev!"
            await self.bot.forward_message(chat_id=DEV_ID,
                                           from_chat_id=from_chat_id,
                                           message_id=message_id)
            await self.bot.answer_callback_query(callback.id, text=answer_text,
                                                 show_alert=False)
            await self.__delete_message(3, callback.message)
        elif callback.data == ERROR_DELETE:
            await callback.message.delete()

    async def __delete_message(self, delay, message):
        await asyncio.sleep(delay)
        await message.delete()
