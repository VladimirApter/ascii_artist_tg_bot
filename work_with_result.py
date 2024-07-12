import os
from telebot.types import InputMedia

from config import bot
import ascii_artist.main


def _make_result(message, user_data):
    bot.send_message(message.chat.id, 'Начал обрабатывать')
    file_id = user_data['file_id']
    file_path = user_data['file_path']
    height = user_data['height']
    bg_color = user_data['bg_color']
    font_color = user_data['font_color']
    symbols = user_data['symbols']

    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)

    ascii_artist.main.main(file_path, height, bg_color, font_color, symbols)

    os.unlink(file_path)


def send_result(message, user_data):
    result_path = user_data['result_path']

    _make_result(message, user_data)

    with open(result_path, 'rb') as result_file:
        file_type = 'video' if result_path.endswith('.mp4') else 'photo'
        media = [InputMedia(type=file_type, media=result_file)]
        bot.send_media_group(message.chat.id, media)

    os.unlink(result_path)

    bot.send_message(message.chat.id, "Готово! Можешь присылать следующий файл")
