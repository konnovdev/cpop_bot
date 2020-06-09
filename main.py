import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot import api

import config
from command_processor import CommandProcessor
from new_members_processor import NewMembersProcessor
from text_processor import TextProcessor

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot = Bot(
    token=config.ACCESS_TOKEN,
)
dp = Dispatcher(
    bot=bot,
)
textProcessor = TextProcessor()
commandProcessor = CommandProcessor()
newMembersProcessor = NewMembersProcessor()


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def process_new_member(message: types.Message):
    await newMembersProcessor.handle(message)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_text_message(message: types.Message):
    if message.is_command():
        await commandProcessor.handle(message)
    else:
        await textProcessor.handle(message)


def main():
    executor.start_polling(
        dispatcher=dp,
    )


if __name__ == '__main__':
    main()
