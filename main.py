import photo_processing
import video_processing
from telebot import types

from config import bot
import work_with_db

work_with_db.create_table()
work_with_db.print_users_table()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    work_with_db.register_user(user_id, user_name)

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
