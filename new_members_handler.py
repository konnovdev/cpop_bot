import logging
from datetime import datetime
from typing import List

from aiogram import types, Bot

from config import USER_CAPTCHA_TIMEOUT_IN_MINUTES
from constants import CAPTCHA_SUCCESS

logger = logging.getLogger(__name__)


class PendingUser:
    def __init__(self, user_id, captcha_message: types.Message, timestamp):
        self.user_id = user_id
        self.captcha_message = captcha_message
        self.timestamp = timestamp


class NewMembersHandler:
    pendingUsers: List[PendingUser] = list()

    def __init__(self, bot: Bot):
        self.bot = bot

    async def handle(self, message: types.Message):
        if await self.__isBotAdmin(message.chat.id):
            await self.__giveCaptcha(message)

    async def __isBotAdmin(self, chat_id):
        bot_id = (await self.bot.get_me()).id
        bot_chat_member = await self.bot.get_chat_member(chat_id, bot_id)
        return bot_chat_member.can_restrict_members

    async def __giveCaptcha(self, message: types.Message):
        if len(message.new_chat_members) > 1 or message.new_chat_members[0].is_bot:
            return

        await self.bot.restrict_chat_member(message.chat.id,
                                            message.from_user.id,
                                            can_send_messages=False,
                                            can_send_media_messages=False,
                                            can_send_other_messages=False)
        markup = self.__makeInlineKeyboard()
        replied_message = await message.reply("Welcome, {0.first_name},\nAre you a spam bot or a human?"
                                              .format(message.from_user), reply_markup=markup)
        pendingUser = PendingUser(message.from_user.id,
                                  replied_message,
                                  datetime.now())
        self.pendingUsers.append(pendingUser)
        await self.__purge_old_captchas()

    def __makeInlineKeyboard(self):
        markup = types.InlineKeyboardMarkup(resize_keyboard=True)
        item1 = types.InlineKeyboardButton("human", callback_data=CAPTCHA_SUCCESS)
        item2 = types.InlineKeyboardButton("I am clearly a spam bot", callback_data=CAPTCHA_SUCCESS)
        markup.add(item1, item2)
        return markup

    async def __purge_old_captchas(self):
        for pendingUser in self.pendingUsers:
            time_passed = (datetime.now() - pendingUser.timestamp).total_seconds() / 60
            if time_passed > USER_CAPTCHA_TIMEOUT_IN_MINUTES:
                self.pendingUsers.remove(pendingUser)
                await pendingUser.captcha_message.delete()

    async def handleCaptchaCallback(self, callback: types.CallbackQuery):
        pending_user = self.__get_pending_user(callback.message.message_id,
                                               callback.message.chat.id,
                                               callback.from_user.id)
        if pending_user.user_id != callback.from_user.id:
            await self.bot.answer_callback_query(callback.id,
                                                 text="We are waiting for " +
                                                      (await
                                                       callback
                                                       .message
                                                       .chat
                                                       .get_member(
                                                           pending_user.user_id
                                                       )).user.first_name +
                                                      " to click!",
                                                 show_alert=False)
        else:
            await self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                             message_id=callback.message.message_id,
                                             text="Congrats, " + callback.from_user.first_name + ", captcha passed",
                                             reply_markup=None)
            await self.bot.restrict_chat_member(
                callback.message.chat.id,
                callback.from_user.id,
                types.ChatPermissions(True, True, True, True, True, True, True, True))

    def __get_pending_user(self, message_id, chat_id, user_id):
        for pendingUser in self.pendingUsers:
            if message_id == pendingUser.captcha_message.message_id \
                    and chat_id == pendingUser.captcha_message.chat.id:
                return pendingUser
        return None
