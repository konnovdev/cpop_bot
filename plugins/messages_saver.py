from pyrogram import Client, filters
from pyrogram.types import Message

from plugins.music import SITES_REGEX, EXCLUDE_PLAYLISTS
from tools.cng import save_message


@Client.on_message(filters.text
                   & filters.incoming
                   & ~filters.edited
                   & ~filters.regex(r"^(p|P)ing$")
                   & ~filters.regex(r"^(u|U)ptime$")
                   & ~filters.regex(SITES_REGEX)
                   & ~filters.regex(EXCLUDE_PLAYLISTS))
async def log_message(_, message: Message):
    save_message(message)
