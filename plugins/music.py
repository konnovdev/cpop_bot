"""Download music from YouTube/SoundCloud/Mixcloud, convert thumbnail
to square thumbnail and upload to Telegram

Send a link as a reply to bypass Music category check
"""
import os
import asyncio
from datetime import timedelta
from urllib.parse import urlparse
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant
from youtube_dl import YoutubeDL
from PIL import Image
from config import MUSIC_CHATS, MUSIC_USERS

MUSIC_DELAY_DELETE_INFORM_IN_SECONDS = 10
TG_THUMB_MAX_LENGTH = 320
MUSIC_MAX_LENGTH_IN_SECONDS = 10800
MUSIC_INFORM_AVAILABILITY = (
    "This bot only serves the cpop.tw group and "
    "its members in private chat"
)
SITES_REGEX = (
    r"^((?:https?:)?\/\/)"
    r"?((?:www|m)\.)"
    r"?((?:youtube\.com|youtu\.be|soundcloud\.com|mixcloud\.com))"
    r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$"
)
EXCLUDE_PLAYLISTS = (
    r"\/playlist\?list=|&list=|\/sets\/"
)


@Client.on_message(filters.text
                   & filters.incoming
                   & filters.regex(SITES_REGEX)
                   & ~filters.regex(EXCLUDE_PLAYLISTS)
                   & ~filters.edited)
async def music_downloader(client: Client, message: Message):
    """Add members of specified chats to the list when it's a private
    chat. Or if both music users and music chats are unspecified then just
    allow the user to use the bot
    """
    # print(' '.join([str(u) for u in MUSIC_USERS]))
    if message.chat.type != "private" and \
            message.chat.id not in MUSIC_CHATS and \
            len(MUSIC_CHATS) != 0:
        return
    if message.chat.type == "private":
        user_id = message.from_user.id
        if user_id not in MUSIC_USERS:
            for chat in MUSIC_CHATS:
                try:
                    await client.get_chat_member(chat, user_id)
                    MUSIC_USERS.append(user_id)
                    break
                except UserNotParticipant:
                    pass
        if len(MUSIC_USERS) == 0 and len(MUSIC_CHATS) == 0:
            MUSIC_USERS.append(user_id)
        if user_id not in MUSIC_USERS:
            await message.reply(MUSIC_INFORM_AVAILABILITY)
            return
    await _fetch_and_send_music(message)


async def _fetch_and_send_music(message: Message):
    await message.reply_chat_action("typing")
    try:
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': '%(title)s - %(extractor)s-%(id)s.%(ext)s',
            'writethumbnail': True
        }
        ydl = YoutubeDL(ydl_opts)
        info_dict = ydl.extract_info(message.text, download=False)
        # send a link as a reply to bypass Music category check
        if not message.reply_to_message \
                and _youtube_video_not_music(info_dict):
            inform = ("This won't be downloaded "
                      "because it's not under Music category")
            await _reply_and_delete_later(message, inform,
                                          MUSIC_DELAY_DELETE_INFORM_IN_SECONDS)
            return
        if info_dict['duration'] > MUSIC_MAX_LENGTH_IN_SECONDS:
            readable_max_length = \
                str(timedelta(seconds=MUSIC_MAX_LENGTH_IN_SECONDS))
            inform = ("This won't be downloaded because its audio length is "
                      "longer than the limit `{}` which is set by the bot"
                      .format(readable_max_length))
            await _reply_and_delete_later(message, inform,
                                          MUSIC_DELAY_DELETE_INFORM_IN_SECONDS)
            return
        d_status = await message.reply_text("Downloading...", quote=True,
                                            disable_notification=True)
        ydl.process_info(info_dict)
        audio_file = ydl.prepare_filename(info_dict)
        task = asyncio.create_task(_upload_audio(message, info_dict,
                                                 audio_file))
        await message.reply_chat_action("upload_document")
        await d_status.delete()
        while not task.done():
            await asyncio.sleep(4)
            await message.reply_chat_action("upload_document")
        await message.reply_chat_action("cancel")
        if message.chat.type == "private":
            await message.delete()
    except Exception as e:
        await message.reply_text(repr(e))


def _youtube_video_not_music(info_dict):
    if info_dict['extractor'] == 'youtube' \
            and 'Music' not in info_dict['categories']:
        return True
    return False


async def _reply_and_delete_later(message: Message, text: str, delay: int):
    reply = await message.reply_text(text, quote=True)
    await asyncio.sleep(delay)
    await reply.delete()


async def _upload_audio(message: Message, info_dict, audio_file):
    basename = audio_file.rsplit(".", 1)[-2]
    if info_dict['ext'] == 'webm':
        audio_file_weba = basename + ".weba"
        os.rename(audio_file, audio_file_weba)
        audio_file = audio_file_weba
    thumbnail_url = info_dict['thumbnail']
    if os.path.isfile(basename + ".jpg"):
        thumbnail_file = basename + ".jpg"
    else:
        file_extension = _get_file_extension_from_url(thumbnail_url)
        thumbnail_file = basename + "." + file_extension
    squarethumb_file = basename + "_squarethumb.jpg"
    make_squarethumb(thumbnail_file, squarethumb_file)
    webpage_url = info_dict['webpage_url']
    title = info_dict['title']
    caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
    duration = int(float(info_dict['duration']))
    performer = info_dict['uploader']
    await message.reply_audio(audio_file, caption=caption, duration=duration,
                              performer=performer, title=title,
                              parse_mode='HTML', thumb=squarethumb_file)
    os.remove(audio_file)
    os.remove(thumbnail_file)
    os.remove(squarethumb_file)


def _get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]


def make_squarethumb(thumbnail, output):
    """Convert thumbnail to square thumbnail"""
    # https://stackoverflow.com/a/52177551
    original_thumb = Image.open(thumbnail)
    squarethumb = _crop_to_square(original_thumb)
    squarethumb.thumbnail((TG_THUMB_MAX_LENGTH, TG_THUMB_MAX_LENGTH),
                          Image.ANTIALIAS)
    squarethumb.save(output)


def _crop_to_square(img: Image):
    width, height = img.size
    length = min(width, height)
    left = (width - length) / 2
    top = (height - length) / 2
    right = (width + length) / 2
    bottom = (height + length) / 2
    return img.crop((left, top, right, bottom))
