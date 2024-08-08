from telebot import types
from telebot.types import InputMediaPhoto, InputMediaVideo
import os

from config import bot, CURRENT_DIR
import users_db_work
import ads_db_work
from big_messages import *


def register_commands():
    from main import breakdown_handler

    @bot.message_handler(commands=['start'])
    @breakdown_handler
    def start_command(message):
        start_handler(message)

    @bot.message_handler(commands=['help'])
    @breakdown_handler
    def help_command(message):
        help_handler(message)

    @bot.message_handler(commands=['limits'])
    @breakdown_handler
    def limits_command(message):
        limits_handler(message)

    @bot.message_handler(commands=['ideas'])
    @breakdown_handler
    def ideas_command(message):
        ideas_handler(message)


def start_handler(message):
    user_id = message.from_user.id
    user_name = f'@{message.from_user.username}'

    users_db_work.register_user(user_id, user_name)
    ads_db_work.register_user(user_id)

    is_first_time = users_db_work.get_user_column_value(user_id, users_db_work.BdTableColumns.first_time)
    if not is_first_time:
        bot.send_message(message.chat.id, 'Готов работать, отправь изображение или видео', reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, 'Привет! Пришли мне картинку и я сделаю из нее ascii арт')


def help_handler(message):
    bot.send_message(message.chat.id, help_message, reply_markup=types.ReplyKeyboardRemove())


def limits_handler(message):
    bot.send_message(message.chat.id, limits_message, reply_markup=types.ReplyKeyboardRemove())


def ideas_handler(message):
    files_dir = os.path.join(CURRENT_DIR, 'idea_files')

    images_names = ['trump', 'earth', 'flower', 'messi', 'dunk', 'led']

    media_group = []
    open_files = []
    for image_name in images_names:
        photo_path = os.path.join(files_dir, f'{image_name}.jpg')
        photo = open(photo_path, 'rb')
        open_files.append(photo)
        media_group.append(InputMediaPhoto(media=photo))

    bot.send_chat_action(message.chat.id, 'upload_photo')
    bot.send_media_group(message.chat.id, media_group, timeout=50)
    bot.send_message(message.chat.id, 'Я готов работать, можешь отправить изображение или видео', reply_markup=types.ReplyKeyboardRemove())

    for file in open_files:
        file.close()
