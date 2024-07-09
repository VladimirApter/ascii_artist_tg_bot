from telebot import TeleBot
import os

from config import bot
import photo_processing, video_processing


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Готов работать, отправь изображение или видео")


@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    photo_processing.get_photo(message)


@bot.message_handler(content_types=['video'])
def photo_handler(message):
    video_processing.get_video(message)


bot.polling(none_stop=True)
