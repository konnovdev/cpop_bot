import logging

from aiogram import types, Bot

from constants import CAPTCHA_SUCCESS

logger = logging.getLogger(__name__)


class NewMembersHandler:
    async def handle(self, bot: Bot, message: types.Message):
        if self.__isBotAdmin(bot, message.chat.id):
            await self.__giveCaptcha(message)

    async def __isBotAdmin(self, bot: Bot, chat_id):
        bot_user: types.User = await bot.get_me()
        bot_id = bot_user.id
        bot_chat_member = await bot.get_chat_member(chat_id, bot_id)
        return bot_chat_member.is_chat_admin()

    async def __giveCaptcha(self, message: types.Message):
        markup = types.InlineKeyboardMarkup(resize_keyboard=True)
        item1 = types.InlineKeyboardButton("human", callback_data=CAPTCHA_SUCCESS)
        item2 = types.InlineKeyboardButton("I am clearly a spam bot", callback_data=CAPTCHA_SUCCESS)
        markup.add(item1, item2)
        await message.reply("Welcome, {0.first_name},\nAre you a spam bot or a human?"
                            .format(message.from_user), reply_markup=markup)
