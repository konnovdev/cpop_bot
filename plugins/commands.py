from pyrogram import Client, filters
from pyrogram.types import Message

from tools.weather import get_weather, InvalidApiKeyError

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
    """/start - introduction of the bot"""
    await message.reply_sticker("static/hello_animated_sticker.tgs")


@Client.on_message(filters.command(["help"])
                   & filters.incoming
                   & ~filters.edited)
async def command_help(_, message: Message):
    """/help - usage of the bot"""
    await message.reply(COMMANDS_TEXT_HELP)


@Client.on_message(filters.command(["json"])
                   & filters.incoming
                   & ~filters.edited)
async def command_json(_, message: Message):
    """/json - get user info"""
    await message.reply(f"<code>{message}</code>")


@Client.on_message(filters.command(["id"])
                   & filters.incoming
                   & ~filters.edited)
async def command_id(_, message: Message):
    """/id - get user info"""
    await message.reply(f"<code>{message.from_user}</code>")


@Client.on_message(filters.command(["weather"])
                   & filters.incoming
                   & ~filters.edited)
async def command_weather(_, message: Message):
    """/weather city - get weather"""
    try:
        start_city_name_index = 1
        end_city_name_index = len(message.command)
        city_name = "+".join(
            message.command[start_city_name_index:end_city_name_index]
        )
        if city_name:
            weather_response = get_weather(city_name)
            await message.reply(weather_response)
        else:
            await message.reply("Usage:\n/weather city"
                                "\n\nFor example:\n/weather San Paulo")
    except InvalidApiKeyError:
        pass
