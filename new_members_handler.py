import logging

from aiogram import types, Bot

from constants import CAPTCHA_SUCCESS

logger = logging.getLogger(__name__)


class NewMembersHandler:
    pendingUsers = dict()

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
        self.pendingUsers[replied_message.message_id] = message.from_user.id

    def __makeInlineKeyboard(self):
        markup = types.InlineKeyboardMarkup(resize_keyboard=True)
        item1 = types.InlineKeyboardButton("human", callback_data=CAPTCHA_SUCCESS)
        item2 = types.InlineKeyboardButton("I am clearly a spam bot", callback_data=CAPTCHA_SUCCESS)
        markup.add(item1, item2)
        return markup

    async def handleCaptchaCallback(self, callback: types.CallbackQuery):
        pending_user_id = self.pendingUsers.get(callback.message.message_id)
        if pending_user_id != callback.from_user.id:
            await self.bot.answer_callback_query(callback.id,
                                                 text="We are waiting for " +
                                                      (await callback.message.chat.get_member(
                                                          pending_user_id)).user.first_name +
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
            self.pendingUsers.pop(callback.message.message_id)
