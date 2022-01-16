from pyrogram import Client, filters
from pyrogram.types import Message

from tools.utils import command_args_to_str
from tools.weather import get_weather, InvalidApiKeyError
from tools.wolfram import get_wolfram_result

COMMANDS_TEXT_HELP = (
    "This bot only serves cpop.tw and "
    "its members in private chat"
    "\n\n<b>Usage</b>:\n"
    "- To download a song send a message "
    "that only contains a YouTube/SoundCloud/Mixcloud link\n"
    "- <code>/wf question</code> - ask wolframalpha.com a question\n"
    "- <code>/weather city</code> - get current weather for the city\n"
    "- <code>/dic word</code> - look up a word in cedict\n\n"
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
        city_name = command_args_to_str(message.command)
        if city_name:
            weather_response = get_weather(city_name)
            await message.reply(weather_response)
        else:
            await message.reply("Usage:\n<code>/weather city</code>"
                                "\n\nFor example:"
                                "\n<code>/weather San Paulo</code>")
    except InvalidApiKeyError:
        pass


@Client.on_message(filters.command(["wolfram", "wf"])
                   & filters.incoming
                   & ~filters.edited)
async def command_wolfram(_, message: Message):
    """/wf question - get answer from wolframalpha.com"""
    try:
        question = command_args_to_str(message.command)
        if question:
            wolfram_response = get_wolfram_result(question)
            await message.reply(wolfram_response)
        else:
            await message.reply("Usage: \n<code>/wolfram your query</code>"
                                "\n\nFor example:"
                                "\n<code>/wolfram capital of Japan</code>"
                                "\n\nYou can also use <code>/wf</code> "
                                "instead of <code>/wolfram</code>")
    except Exception:
        pass
