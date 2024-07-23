import os
from telebot import types

from config import bot, CURRENT_DIR
from data_structures import *


IMAGES_DIR_PATH = os.path.join(CURRENT_DIR, 'ascii_artist', 'images')


def get_photo(message, user_data: UserData):
    from user_survey import start_survey  # to solve circular import problem
    from tutorial import start_tutorial

    photo = message.photo[-1]
    file_id = photo.file_id

    file_name = f"user{message.from_user.id}_file{file_id}.jpg"
    file_path = os.path.join(IMAGES_DIR_PATH, file_name)

    result_file_name = f'user{message.from_user.id}_file{file_id}_ascii_art.jpg'
    result_path = os.path.join(IMAGES_DIR_PATH, result_file_name)

    user_data.media = PhotoData(file_id, file_path, result_path, Orientation.horizontal)
    if photo.height > photo.width:
        user_data.media.orientation = Orientation.vertical

    bot.reply_to(message, "Принял фото", reply_markup=types.ReplyKeyboardRemove())

    if not user_data.first_time:
        start_survey(message, user_data)
    else:
        start_tutorial(message, user_data)

