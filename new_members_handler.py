import logging

from aiogram import types, Bot

from constants import CAPTCHA_SUCCESS

logger = logging.getLogger(__name__)


class NewMembersHandler:
    async def handle(self, bot: Bot, message: types.Message):
        if await self.__isBotAdmin(bot, message.chat.id):
            await self.__giveCaptcha(bot, message)

    async def __isBotAdmin(self, bot: Bot, chat_id):
        bot_user: types.User = await bot.get_me()
        bot_id = bot_user.id
        bot_chat_member = await bot.get_chat_member(chat_id, bot_id)
        return bot_chat_member.can_restrict_members

    async def __giveCaptcha(self, bot: Bot, message: types.Message):
        bot_user: types.User = await bot.get_me()
        if message.new_chat_members[0] == bot_user:
            return

        await bot.restrict_chat_member(message.chat.id,
                                       message.from_user.id,
                                       can_send_messages=False,
                                       can_send_media_messages=False,
                                       can_send_other_messages=False)
        markup = types.InlineKeyboardMarkup(resize_keyboard=True)
        item1 = types.InlineKeyboardButton("human", callback_data=CAPTCHA_SUCCESS)
        item2 = types.InlineKeyboardButton("I am clearly a spam bot", callback_data=CAPTCHA_SUCCESS)
        markup.add(item1, item2)
        await message.reply("Welcome, {0.first_name},\nAre you a spam bot or a human?"
                            .format(message.from_user), reply_markup=markup)
