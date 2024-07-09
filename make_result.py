import os

from config import bot
import ascii_artist.main


def make_result(user_data):
    file_id = user_data['file_id']
    height = user_data['height']
    file_path = user_data['file_path']

    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)

    ascii_artist.main.main(file_path, height)

    os.unlink(file_path)
