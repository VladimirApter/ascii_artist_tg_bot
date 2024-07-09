import os

from config import bot, CURRENT_DIR
import ascii_artist.main


VIDEOS_DIR_PATH = os.path.join(CURRENT_DIR, 'ascii_artist', 'videos')


def get_video(message):
    file_id = message.video.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    file_name = f"user{message.from_user.id}_file{file_id}.mp4"
    file_path = os.path.join(VIDEOS_DIR_PATH, file_name)
    result_file_name = f'user{message.from_user.id}_file{file_id}_ascii_art.mp4'
    result_path = os.path.join(VIDEOS_DIR_PATH, result_file_name)

    with open(file_path, 'wb') as f:
        f.write(downloaded_file)

    bot.reply_to(message, "Принял видео, 50 символов хочешь по вертикали")
    bot.register_next_step_handler(message, send_result, file_path, 50, result_path)


def send_result(message, file_path, height, result_path):
    ascii_artist.main.main(file_path, height)

    with open(result_path, 'rb') as result_video:
        bot.send_video(message.chat.id, result_video)

    os.unlink(result_path)
    os.unlink(file_path)

    bot.send_message(message.chat.id, "Готово! Можешь присылать следующий файл")
