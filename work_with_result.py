import os
from telebot.types import InputMedia
import time

from config import bot
import ascii_artist.main


def _make_result(message, user_data):
    file_id = user_data['file_id']
    file_path = user_data['file_path']
    height = user_data['height']
    bg_color = user_data['bg_color']
    font_color = user_data['font_color']
    symbols = user_data['symbols']

    bot.send_message(message.chat.id, 'Загружаю твой файл')
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)

    bot.send_message(message.chat.id, 'Начал обрабатывать')
    ascii_artist.main.main(file_path, height, bg_color, font_color, symbols)

    os.unlink(file_path)


def send_result(message, user_data):
    height = user_data['height']
    result_path = user_data['result_path']
    file_type = user_data['file_type']

    _make_result(message, user_data)

    with open(result_path, 'rb') as result_file:
        if file_type == 'photo' and height <= 60:
            bot.send_photo(message.chat.id, result_file)
        elif file_type == 'video' and height <= 60:
            bot.send_video(message.chat.id, result_file)
        else:
            bot.send_document(message.chat.id, result_file)

    os.unlink(result_path)

    bot.send_message(message.chat.id, "Готово! Можешь присылать следующий файл")
