import photo_processing
import video_processing
from telebot import types

from config import bot
import work_with_db
from data_structures import *

work_with_db.create_table()


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    work_with_db.register_user(user_id, user_name)

    if not work_with_db.is_user_first_time(user_id):
        bot.send_message(message.chat.id, "Готов работать, отправь изображение или видео", reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, 'Привет! Пришли мне картинку и я сделаю из нее ascii арт')


@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    work_with_db.register_user(user_id, user_name)

    user_first_time = work_with_db.is_user_first_time(user_id)
    user_data = UserData(first_time=user_first_time)

    photo_processing.get_photo(message, user_data)


@bot.message_handler(content_types=['video'])
def video_handler(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    work_with_db.register_user(user_id, user_name)

    user_first_time = work_with_db.is_user_first_time(user_id)
    if not user_first_time:
        user_data = UserData(first_time=user_first_time)
        video_processing.get_video(message, user_data)
    else:
        bot.send_message(message.chat.id, 'Отправь фото пожалуйста')


bot.polling(none_stop=True)
