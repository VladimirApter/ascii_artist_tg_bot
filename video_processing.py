import os

from config import bot, CURRENT_DIR
from user_survey import start_survey


VIDEOS_DIR_PATH = os.path.join(CURRENT_DIR, 'ascii_artist', 'videos')


def get_video(message, user_data):
    file_id = message.video.file_id
    user_data['file_id'] = file_id

    file_name = f"user{message.from_user.id}_file{file_id}.mp4"
    file_path = os.path.join(VIDEOS_DIR_PATH, file_name)
    user_data['file_path'] = file_path

    result_file_name = f'user{message.from_user.id}_file{file_id}_ascii_art.mp4'
    result_path = os.path.join(VIDEOS_DIR_PATH, result_file_name)
    user_data['result_path'] = result_path

    bot.reply_to(message, "Принял видео")
    start_survey(message, user_data)
