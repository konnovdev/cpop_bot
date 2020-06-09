import logging

from aiogram import types

logger = logging.getLogger(__name__)


class NewMembersProcessor:
    async def handle(self, message: types.Message):
        await message.reply("Welcome, " + message.from_user.first_name)
