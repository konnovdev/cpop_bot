import logging
from aiogram import Bot, Dispatcher, executor, types

import config
from command_handler import CommandHandler
from new_members_handler import NewMembersHandler
from text_handler import TextHandler

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


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def process_new_member(message: types.Message):
    await newMembersHandler.handle(bot, message)


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
        await commandHandler.handle(message)
    else:
        await textHandler.handle(message)


def main():
    executor.start_polling(
        dispatcher=dp,
    )


if __name__ == '__main__':
    main()
