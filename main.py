import photo_processing
import video_processing
from telebot import types

from config import bot
import work_with_db
import commands_handle
from data_structures import *


bot_is_broken = False

work_with_db.create_table()


def breakdown_handler(handler):
    def inner(message):
        if bot_is_broken:
            bot.send_message(message.chat.id, 'Бот временно не работает, попробуй написать позже.')
        else:
            handler(message)

    return inner


@bot.message_handler(commands=['start'])
@breakdown_handler
def start_handler(message):
    commands_handle.start_handler(message)


@bot.message_handler(commands=['help'])
@breakdown_handler
def help_handler(message):
    commands_handle.help_handler(message)


@bot.message_handler(commands=['limits'])
@breakdown_handler
def limits_handler(message):
    commands_handle.limits_handler(message)


@bot.message_handler(commands=['ideas'])
@breakdown_handler
def ideas_handler(message):
    commands_handle.ideas_handler(message)


@bot.message_handler(content_types=['photo'])
@breakdown_handler
def photo_handler(message):
    user_id = message.from_user.id

    user_first_time = work_with_db.get_user_column_value(user_id, work_with_db.BdTableColumns.first_time)
    user_data = UserData(first_time=user_first_time)

    photo_processing.get_photo(message, user_data)


@bot.message_handler(content_types=['video'])
@breakdown_handler
def video_handler(message):
    user_id = message.from_user.id

    user_first_time = work_with_db.get_user_column_value(user_id, work_with_db.BdTableColumns.first_time)
    if not user_first_time:
        user_data = UserData(first_time=user_first_time)
        video_processing.get_video(message, user_data)
    else:
        bot.send_message(message.chat.id, 'Отправь фото пожалуйста', reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text', 'sticker', 'audio', 'document', 'voice', 'location', 'contact'])
@breakdown_handler
def incorrect_input(message):
    user_id = message.from_user.id

    user_first_time = work_with_db.get_user_column_value(user_id, work_with_db.BdTableColumns.first_time)
    if not user_first_time:
        if message.content_type == 'document':
            bot.send_message(message.chat.id, 'Ты отправил документ, для обработки мне нужно именно фото/видео\nЕсли ты с компьютера поставь галочку "Сжать изображение"')
            return
        bot.send_message(message.chat.id, 'Отправь фото или видео, которое хочешь обработать.\nЕсли нужна помощь воспользуйся /help')
    else:
        if message.content_type == 'document':
            bot.send_message(message.chat.id, 'Ты отправил документ, для обработки мне нужно именно фото\nЕсли ты с компьютера поставь галочку "Сжать изображение"')
            return
        bot.send_message(message.chat.id, 'Отправь фото пожалуйста', reply_markup=types.ReplyKeyboardRemove())


bot.polling(none_stop=True)
try:
    bot.polling(none_stop=True)
except Exception as e:
    print('EXCEPTION:', e)
    bot_is_broken = True
    bot.polling(none_stop=True)
