from aiogram import Bot, Dispatcher, executor, types


class TextProcessor:
    async def handle(self, message: types.Message):
        await message.reply(message.text, reply=False)
