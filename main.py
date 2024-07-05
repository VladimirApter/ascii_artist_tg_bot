import telebot

bot = telebot.TeleBot("7146497668:AAG5wBIrMEoho64W2F9MnSzYPyDPLrnqMto")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Готов работать, отправь изображение или видео")

@bot.message_handler(content_types=['photo'])
def process_photo(message):
    bot.reply_to(message, "Принял фото")

@bot.message_handler(content_types=['video'])
def process_video(message):
    bot.reply_to(message, "Принял видео")

bot.polling(none_stop=True)
