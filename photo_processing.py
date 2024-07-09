import os

from config import bot, CURRENT_DIR
from make_result import make_result

IMAGES_DIR_PATH = os.path.join(CURRENT_DIR, 'ascii_artist', 'images')


def get_photo(message, user_data):
    file_id = message.photo[-1].file_id
    user_data['file_id'] = file_id
    user_data['height'] = 50

    file_name = f"user{message.from_user.id}_file{file_id}.jpg"
    file_path = os.path.join(IMAGES_DIR_PATH, file_name)
    user_data['file_path'] = file_path

    result_file_name = f'user{message.from_user.id}_file{file_id}_ascii_art.jpg'
    result_path = os.path.join(IMAGES_DIR_PATH, result_file_name)
    user_data['result_path'] = result_path

    bot.reply_to(message, "Принял фото, 50 символов хочешь по вертикали")
    send_result(message, user_data)


def send_result(message, user_data):
    result_path = user_data['result_path']

    make_result(user_data)

    with open(result_path, 'rb') as result_photo:
        bot.send_photo(message.chat.id, result_photo)

    os.unlink(result_path)

    bot.send_message(message.chat.id, "Готово! Можешь присылать следующий файл")
