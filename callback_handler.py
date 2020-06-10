import logging
from aiogram import types

logger = logging.getLogger(__name__)


class CallbackHandler:
    async def handle(self, bot, callback: types.CallbackQuery):
        if callback.data == 'captcha_passed':
            await self.__handleCaptchaPassed(bot, callback)

    async def __handleCaptchaPassed(self, bot, callback: types.CallbackQuery):
        await bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id,
                                    text="Congrats, " + callback.from_user.first_name + ", captcha passed",
                                    reply_markup=None)
