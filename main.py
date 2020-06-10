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
    await newMembersProcessor.handle(bot, message)


@dp.callback_query_handler(lambda callback: True)
async def process_callback(callback: types.CallbackQuery):
    if callback.message:
        if callback.data == 'captcha_passed':
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  text="Congrats, " + callback.from_user.first_name + ", captcha passed",
                                  reply_markup=None)


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
