import random
import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.ACCESS_TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('static/hello_animated_sticker.tgs', 'rb')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Random number")
    item2 = types.KeyboardButton("Sup")
    markup.add(item1, item2)

    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, "Sup, {0.first_name}\n I am <b>{1.first_name}</b> a cpop fan"
                     .format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def echo(message):
    if message.chat.type == 'private':
        if message.text == "Random number":
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == "Sup":

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("all good", callback_data='good')
            item2 = types.InlineKeyboardButton("not well :/", callback_data='unwell')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, "yeboi, sup??", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, "kek, i'm also p good")
            elif call.data == 'unwell':
                bot.send_message(call.message.chat.id, "L")

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="yeboi, sup??",
                                  reply_markup=None)

            bot.answer_callback_query(callback_query_id=call.id,
                                      show_alert=False,
                                      text="This is a test message")

    except Exception as e:
        pass


bot.polling(none_stop=True)
