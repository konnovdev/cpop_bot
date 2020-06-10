import logging
from aiogram import Bot, Dispatcher, executor, types

import config
from command_handler import CommandHandler
from new_members_handler import NewMembersHandler
from text_handler import TextHandler
from callback_handler import CallbackHandler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot = Bot(
    token=config.ACCESS_TOKEN,
)
dp = Dispatcher(
    bot=bot,
)
textHandler = TextHandler()
commandHandler = CommandHandler()
newMembersHandler = NewMembersHandler()
callbackHandler = CallbackHandler()


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def process_new_member(message: types.Message):
    await newMembersHandler.handle(bot, message)


@dp.callback_query_handler(lambda callback: True)
async def process_callback(callback: types.CallbackQuery):
    if callback.message:
        await callbackHandler.handle(bot, callback)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_text_message(message: types.Message):
    if message.is_command():
        await commandHandler.handle(message)
    else:
        await textHandler.handle(message)


def main():
    executor.start_polling(
        dispatcher=dp,
    )


if __name__ == '__main__':
    main()
