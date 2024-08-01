from telebot import types
from telebot.types import InputMediaPhoto, InputMediaVideo
import os

from config import bot, CURRENT_DIR
import work_with_db
from big_messages import *


def start_handler(message):
    user_id = message.from_user.id
    user_name = f'@{message.from_user.username}'
    work_with_db.register_user(user_id, user_name)

    is_first_time = work_with_db.get_user_column_value(user_id, work_with_db.BdTableColumns.first_time)
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

    images_names = ['anonymous', 'messi', 'earth', 'flower',
                    'trump', 'dunk', 'led', 'taj_mahal']
    videos_names = ['basket', 'weightlifting']

    media_group = []
    open_files = []
    for image_name in images_names:
        photo_path = os.path.join(files_dir, f'{image_name}.jpg')
        photo = open(photo_path, 'rb')
        open_files.append(photo)
        media_group.append(InputMediaPhoto(media=photo))
    for video_name in videos_names:
        video_path = os.path.join(files_dir, f'{video_name}.mp4')
        video = open(video_path, 'rb')
        open_files.append(video)
        media_group.append(InputMediaVideo(media=video))

    bot.send_media_group(message.chat.id, media_group, timeout=50)
    bot.send_message(message.chat.id, 'Я готов работать, можешь отправить изображение или видео', reply_markup=types.ReplyKeyboardRemove())

    for file in open_files:
        file.close()
