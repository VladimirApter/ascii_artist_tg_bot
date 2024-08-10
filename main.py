import ads_db_work
import photo_processing
import video_processing
from telebot import types

from config import bot, owner_chat_id
import users_db_work
import commands_handle
import admin_commands_handle
import advertiser_commands_handle
from data_structures import *


bot_is_broken = False

users_db_work.create_table()
ads_db_work.create_table()


def breakdown_handler(handler):
    def inner(message):
        if bot_is_broken:
            bot.send_message(owner_chat_id, 'Бот сломался')
            bot.send_message(message.chat.id, 'Бот временно не работает, попробуй написать позже')
        else:
            handler(message)

    return inner


commands_handle.register_commands()
admin_commands_handle.register_commands()
advertiser_commands_handle.register_commands()


@bot.message_handler(content_types=['photo'])
@breakdown_handler
def photo_handler(message):
    user_id = message.from_user.id

    user_first_time = users_db_work.get_user_column_value(user_id, users_db_work.BdTableColumns.first_time)
    user_data = UserData(first_time=user_first_time)

    photo_processing.get_photo(message, user_data)


@bot.message_handler(content_types=['video'])
@breakdown_handler
def video_handler(message):
    user_id = message.from_user.id

    user_first_time = users_db_work.get_user_column_value(user_id, users_db_work.BdTableColumns.first_time)
    if not user_first_time:
        user_data = UserData(first_time=user_first_time)
        video_processing.get_video(message, user_data)
    else:
        bot.send_message(message.chat.id, 'Отправь фото пожалуйста', reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text', 'sticker', 'audio', 'document', 'voice', 'location', 'contact'])
@breakdown_handler
def incorrect_input(message):
    user_id = message.from_user.id

    user_first_time = users_db_work.get_user_column_value(user_id, users_db_work.BdTableColumns.first_time)
    if message.content_type == 'document':
        available_media = 'фото' if user_first_time else 'фото/видео'
        bot.send_message(message.chat.id, f'Ты отправил документ, для обработки мне нужно именно {available_media}\nЕсли ты с компьютера поставь галочку "Сжать изображение"')
    else:
        message_text = 'Отправь фото пожалуйста' if user_first_time else 'Отправь фото или видео, которое хочешь обработать.\nЕсли нужна помощь воспользуйся /help'
        bot.send_message(message.chat.id, message_text, reply_markup=types.ReplyKeyboardRemove())


bot.polling(none_stop=True)
'''while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        if bot_is_broken:
            continue
        if 'bot was blocked by the user' in str(e):
            pass
        else:
            bot.send_message(owner_chat_id, f'EXCEPTION: {str(e)}')
            bot_is_broken = True'''
