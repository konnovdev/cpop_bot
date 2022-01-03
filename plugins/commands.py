from pyrogram import Client, filters
from pyrogram.types import Message

COMMANDS_TEXT_HELP = (
    "This bot only serves cpop.tw and "
    "its members in private chat"
    "\n\n<b>Usage</b>:\n"
    "- Send a message that only contains a YouTube/SoundCloud/Mixcloud link "
    "to download the music\n"
    "- Playlists are not supported\n"
    "- Your message will be deleted in private chat after the music gets "
    "successfully uploaded\n"
    "- You can get YouTube links with inline bot @vid\n\n"
    "Regarding any issues with the bot "
    "feel free to contact @konnov"
)


@Client.on_message(filters.command(["start"])
                   & filters.incoming
                   & ~filters.edited)
async def command_start(_, message: Message):
    """/start introduction of the bot"""
    sticker = open('static/hello_animated_sticker.tgs', 'rb')
    await message.reply_sticker(sticker)


@Client.on_message(filters.command(["help"])
                   & filters.incoming
                   & ~filters.edited)
async def command_help(_, message: Message):
    """/help usage of the bot"""
    await message.reply(COMMANDS_TEXT_HELP)


@Client.on_message(filters.command(["json"])
                   & filters.incoming
                   & ~filters.edited)
async def command_json(_, message: Message):
    """/json get user info"""
    await message.reply(f"<code>{message}</code>")


@Client.on_message(filters.command(["id"])
                   & filters.incoming
                   & ~filters.edited)
async def command_id(_, message: Message):
    """/id get user info"""
    await message.reply(f"<code>{message.from_user}</code>")
