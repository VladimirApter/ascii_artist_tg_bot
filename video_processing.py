import os
from telebot import types

from config import bot, CURRENT_DIR
from data_structures import *


VIDEOS_DIR_PATH = os.path.join(CURRENT_DIR, 'ascii_artist', 'videos')


def get_video(message, user_data: UserData):
    from user_survey import start_survey  # to solve circular import problem

    video = message.video
    file_id = video.file_id

    file_name = f"user{message.from_user.id}_file{file_id}.mp4"
    file_path = os.path.join(VIDEOS_DIR_PATH, file_name)

    result_file_name = f'user{message.from_user.id}_file{file_id}_ascii_art.mp4'
    result_path = os.path.join(VIDEOS_DIR_PATH, result_file_name)

    user_data.media = VideoData(file_id, file_path, result_path, Orientation.horizontal)
    if video.height > video.width:
        user_data.media.orientation = Orientation.vertical

    bot.reply_to(message, "Принял видео", reply_markup=types.ReplyKeyboardRemove())
    start_survey(message, user_data)

