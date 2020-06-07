import telebot
import config

bot = telebot.TeleBot(config.ACCESS_TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('static/hello_animated_sticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, "Sup, {0.first_name}\n I am <b>{1.first_name}</b> a cpop fan"
                     .format(message.from_user, bot.get_me()),
                     parse_mode='html')


@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
