import photo_processing
import video_processing
from telebot import types

from config import bot
import work_with_db
import commands_handle
from data_structures import *


work_with_db.create_table()


@bot.message_handler(commands=['start'])
def start_handler(message):
    commands_handle.start_handler(message)


@bot.message_handler(commands=['help'])
def help_handler(message):
    commands_handle.help_handler(message)


@bot.message_handler(commands=['limits'])
def limits_handler(message):
    commands_handle.limits_handler(message)


@bot.message_handler(commands=['ideas'])
def ideas_handler(message):
    commands_handle.ideas_handler(message)


@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    user_id = message.from_user.id

    user_first_time = work_with_db.is_user_first_time(user_id)
    user_data = UserData(first_time=user_first_time)

    photo_processing.get_photo(message, user_data)


@bot.message_handler(content_types=['video'])
def video_handler(message):
    user_id = message.from_user.id

    user_first_time = work_with_db.is_user_first_time(user_id)
    if not user_first_time:
        user_data = UserData(first_time=user_first_time)
        video_processing.get_video(message, user_data)
    else:
        bot.send_message(message.chat.id, 'Отправь фото пожалуйста', reply_markup=types.ReplyKeyboardRemove())


bot.polling(none_stop=True)
