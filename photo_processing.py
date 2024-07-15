import os

from config import bot, CURRENT_DIR
from user_survey import start_survey


IMAGES_DIR_PATH = os.path.join(CURRENT_DIR, 'ascii_artist', 'images')


def get_photo(message, user_data):
    file_id = message.photo[-1].file_id
    user_data['file_id'] = file_id

    file_name = f"user{message.from_user.id}_file{file_id}.jpg"
    file_path = os.path.join(IMAGES_DIR_PATH, file_name)
    user_data['file_path'] = file_path

    result_file_name = f'user{message.from_user.id}_file{file_id}_ascii_art.jpg'
    result_path = os.path.join(IMAGES_DIR_PATH, result_file_name)
    user_data['result_path'] = result_path

    bot.reply_to(message, "Принял фото")
    start_survey(message, user_data)

