import logging
from datetime import datetime
from typing import List
from aiogram import types, Bot
from aiogram.types import ParseMode
from constants import CAPTCHA_SUCCESS
from config import USER_CAPTCHA_TIMEOUT_IN_MINUTES

logger = logging.getLogger(__name__)


class PendingUser:
    def __init__(self, user_id, captcha_message: types.Message, timestamp):
        self.user_id = user_id
        self.captcha_message = captcha_message
        self.timestamp = timestamp


class NewMembersHandler:
    pending_users: List[PendingUser] = list()

    def __init__(self, bot: Bot):
        self.bot = bot

    async def handle(self, message: types.Message):
        if await self.__is_bot_admin(message.chat.id):
            await self.__give_captcha(message)

    async def __is_bot_admin(self, chat_id):
        bot_id = (await self.bot.get_me()).id
        bot_chat_member = await self.bot.get_chat_member(chat_id, bot_id)
        return bot_chat_member.can_restrict_members

    async def __give_captcha(self, message: types.Message):
        if len(message.new_chat_members) > 1 \
                or message.new_chat_members[0].is_bot:
            return

        await self.bot.restrict_chat_member(message.chat.id,
                                            message.from_user.id,
                                            can_send_messages=False,
                                            can_send_media_messages=False,
                                            can_send_other_messages=False)
        markup = self.__make_inline_keyboard()
        replied_message = await message.reply(
            "<b>Welcome</b> {0},\nAre you a human or a spam bot?"
            .format(self.__get_mention(message.from_user)),
            reply_markup=markup, parse_mode=ParseMode.HTML, reply=False)
        await message.delete()
        pending_user = PendingUser(message.from_user.id, replied_message,
                                   datetime.now())
        self.pending_users.append(pending_user)
        await self.__purge_old_captchas()

    def __get_mention(self, user):
        first_name = user.first_name
        return user.get_mention(name=first_name, as_html=True)

    def __make_inline_keyboard(self):
        markup = types.InlineKeyboardMarkup(resize_keyboard=True)
        item1 = types.InlineKeyboardButton("Human",
                                           callback_data=CAPTCHA_SUCCESS)
        item2 = types.InlineKeyboardButton("🤖",
                                           callback_data=CAPTCHA_SUCCESS)
        markup.add(item1, item2)
        return markup

    async def __purge_old_captchas(self):
        for pending_user in self.pending_users:
            time_passed = (datetime.now() -
                           pending_user.timestamp).total_seconds() / 60
            if time_passed > USER_CAPTCHA_TIMEOUT_IN_MINUTES:
                self.pending_users.remove(pending_user)
                await pending_user.captcha_message.delete()

    async def handle_captcha_callback(self, callback: types.CallbackQuery):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id
        from_user_id = callback.from_user.id
        pending_user_id = self.__get_pending_user(message_id, chat_id).user_id
        if pending_user_id != from_user_id:
            await self.bot.answer_callback_query(
                callback.id,
                text="We are waiting for {0} to click".format(
                    (await callback.message.chat.get_member(pending_user_id))
                    .user.first_name),
                show_alert=False)
        else:
            await self.bot.edit_message_text(
                chat_id=chat_id, message_id=message_id,
                text="Congrats {0}, captcha passed".format(
                    self.__get_mention(callback.from_user)),
                parse_mode=ParseMode.HTML, reply_markup=None)
            await self.bot.restrict_chat_member(
                chat_id,
                from_user_id,
                types.ChatPermissions(True, True, True, True,
                                      True, True, True, True))

    def __get_pending_user(self, message_id, chat_id):
        for pending_user in self.pending_users:
            if message_id == pending_user.captcha_message.message_id \
                    and chat_id == pending_user.captcha_message.chat.id:
                return pending_user
        return None
