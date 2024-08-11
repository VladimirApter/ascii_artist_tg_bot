import os
from telebot import types
from telebot.apihelper import ApiTelegramException

from config import bot
import ads_config
import ascii_artist.main
import users_db_work
import tutorial
import big_messages
from data_structures import *


def make_result(message, user_data: UserData):
    file_id = user_data.media.file_id
    file_path = user_data.media.file_path
    height = user_data.height
    symbols = user_data.symbols
    true_color_mode = user_data.mode == Mode.true_color
    bg_color = [0, 0, 0]
    font_color = [255, 255, 255]
    if not true_color_mode:
        bg_color = user_data.bg_color
        font_color = user_data.font_color

    bot.send_message(message.chat.id, 'Загружаю твой файл', reply_markup=types.ReplyKeyboardRemove())
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, 'wb') as f:
        f.write(downloaded_file)

    bot.send_message(message.chat.id, 'Начал обрабатывать')

    try:
        ascii_artist.main.main(file_path, height, bg_color, font_color, symbols, true_color_mode)
        os.unlink(file_path)
    except:
            bot.send_message(message.chat.id, big_messages.big_result_error_message)
    else:
        send_result(message, user_data)


def send_result(message, user_data: UserData):
    height = user_data.height
    result_path = user_data.media.result_path
    media = user_data.media

    str_file_type = 'photo' if isinstance(user_data.media, PhotoData) else 'video'
    bot.send_chat_action(message.chat.id, f'upload_{str_file_type}')

    directory = os.path.dirname(result_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(result_path, 'rb') as result_file:
        try:
            if (height <= 60 and media.orientation == Orientation.horizontal) or \
                    (height <= 100 and media.orientation == Orientation.vertical):
                if isinstance(media, PhotoData):
                    bot.send_photo(message.chat.id, result_file)
                elif isinstance(media, VideoData):
                    bot.send_video(message.chat.id, result_file)
            else:
                bot.send_document(message.chat.id, result_file)
        except ApiTelegramException:
            bot.send_message(message.chat.id, big_messages.big_result_error_message)

    os.unlink(result_path)

    if not user_data.first_time:
        user_id = message.from_user.id
        if isinstance(user_data.media, PhotoData):
            users_db_work.update_user_data(user_id, 1, 0)
        elif isinstance(user_data.media, VideoData):
            users_db_work.update_user_data(user_id, 0, 1)

        bot.send_message(message.chat.id, 'Готово! Можешь присылать следующий файл', reply_markup=types.ReplyKeyboardRemove())

        ads_config.ADS_BEARER.show_ad(message)
    else:
        bot.send_message(message.chat.id, 'Готово!', reply_markup=types.ReplyKeyboardRemove())
        if user_data.tutorial_phase == TutorialPhase.first:
            tutorial.start_second_phase(message, user_data)
        elif user_data.tutorial_phase == TutorialPhase.second:
            tutorial.finish_tutorial(message, user_data)
