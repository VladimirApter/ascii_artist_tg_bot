import photo_processing
import video_processing
from telebot import types

from config import bot


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Готов работать, отправь изображение или видео", reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    user_data = {'file_type': 'photo'}
    photo_processing.get_photo(message, user_data)


@bot.message_handler(content_types=['video'])
def video_handler(message):
    user_data = {'file_type': 'video'}
    video_processing.get_video(message, user_data)


bot.polling(none_stop=True)
