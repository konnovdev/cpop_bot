import os
import logging
import asyncio
from aiogram import types, Bot
from aiogram.types import ParseMode
from . import music_grabber
from .constants import ERROR_REPORT, ERROR_DELETE
from config import PROMOTION_LIST_CHAT_ID, DEV_ID, WHITELIST_CHAT_ID
from config import AVAILABILITY_HTML, DOWNLOAD_DIR

TELEGRAM_UPLOAD_LIMIT = 52428800
DELAY_DELETE_IN_SEC_PING = 5
DELAY_DELETE_IN_SEC_SIZE_WARNING = 60
DELAY_DELETE_IN_SEC_REPORT_ERROR = 3
music_sites = ("youtu.be/", "youtube.com/watch?v=", "soundcloud.com/")

logger = logging.getLogger(__name__)
musicDownloader = music_grabber.MusicDownloader()
squarethumbMaker = music_grabber.SquarethumbMaker()


class TextHandler:

    def __init__(self, bot: Bot):
        self.bot = bot

    async def handle(self, message: types.Message):
        if not await self.__should_provide_service(message):
            return
        text = message.text
        if self.__is_url_for_music_download(text):
            await types.ChatActions.typing()
            await self.__handle_music_grabber(message)
        elif text == 'ping':
            pong = await message.reply('pong', reply=False)
            await self.__delete_messages(DELAY_DELETE_IN_SEC_PING,
                                         (pong, message))

    async def __should_provide_service(self, message: types.Message):
        chat_id = message.chat.id
        if chat_id in WHITELIST_CHAT_ID:
            return True
        chat_type = message.chat.type
        if chat_type == "private":
            user_id = chat_id
            for promotion_chat in PROMOTION_LIST_CHAT_ID:
                if (await self.bot.get_chat_member(
                        promotion_chat, user_id)).is_chat_member():
                    return True
                else:
                    await message.reply(AVAILABILITY_HTML,
                                        parse_mode=ParseMode.HTML)
                    return False
        else:
            return False

    async def __handle_music_grabber(self, message: types.Message):
        try:
            info = musicDownloader.download(message.text,
                                            TELEGRAM_UPLOAD_LIMIT)
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
                "is greater than 50M"
            inform = await message.reply(text, disable_notification=True)
            await self.__delete_messages(DELAY_DELETE_IN_SEC_SIZE_WARNING,
                                         (inform, ))
        except music_grabber.WrongCategoryError as e:
            logger.error(str(e))
        except Exception as e:
            markup = self.__make_inline_keyboard()
            error_html = "<b>URL</b>: " + message.text + \
                "\n<b>Error</b>: <code>" + str(e) + "</code>"
            await message.reply(error_html, parse_mode=ParseMode.HTML,
                                disable_web_page_preview=True,
                                disable_notification=True, reply_markup=markup)

    def __is_url_for_music_download(self, text):
        if text and (text.startswith("http")) \
                and (' ' not in text and '\n' not in text) \
                and not ('/sets/' in text and '?in=' not in text) \
                and any(site in text for site in music_sites):
            return True
        else:
            return False

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
            answer_text = "Message forwarded to the developer"
            await self.bot.forward_message(chat_id=DEV_ID,
                                           from_chat_id=from_chat_id,
                                           message_id=message_id)
            await self.bot.answer_callback_query(callback.id, text=answer_text,
                                                 show_alert=False)
            await self.__delete_messages(DELAY_DELETE_IN_SEC_REPORT_ERROR,
                                         (callback.message, ))
        elif callback.data == ERROR_DELETE:
            await callback.message.delete()

    async def __delete_messages(self, delay, messages):
        await asyncio.sleep(delay)
        for msg in messages:
            await msg.delete()
