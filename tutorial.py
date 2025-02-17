from time import sleep
import os
from telebot import types

from config import bot, CURRENT_DIR
import work_with_result
import users_db_work
import user_survey
from data_structures import *

TUTORIAL_IMAGES_DIR = os.path.join(CURRENT_DIR, 'turorial_images')


def start_tutorial(message, user_data: UserData):
    user_data.tutorial_phase = TutorialPhase.first
    user_data.mode = Mode.regular

    set_pause_between_messages(message, 0.25)

    bot.send_message(message.chat.id, 'Ты тут первый раз, поэтому я быстренько покажу тебе как делать арты', reply_markup=types.ReplyKeyboardRemove())
    show_height_example(message, user_data)


def show_height_example(message, user_data: UserData):
    set_pause_between_messages(message, 1.5)

    path_to_original = os.path.join(TUTORIAL_IMAGES_DIR, 'original.jpg')
    with open(path_to_original, 'rb') as file:
        bot.send_photo(message.chat.id, file)
    bot.send_message(message.chat.id, 'Эта картинка будет для примера', reply_markup=types.ReplyKeyboardRemove())

    set_pause_between_messages(message, 1)

    path_to_height20 = os.path.join(TUTORIAL_IMAGES_DIR, 'height20.jpg')
    path_to_height50 = os.path.join(TUTORIAL_IMAGES_DIR, 'height50.jpg')
    photo_group = [
        types.InputMediaPhoto(open(path_to_height20, 'rb')),
        types.InputMediaPhoto(open(path_to_height50, 'rb'))
    ]
    bot.send_media_group(message.chat.id, photo_group)

    bot.send_message(message.chat.id, 'Я обработал картинку по разному: на первой картинке количество символов по вертикали 20, на второй - 50')

    set_pause_between_messages(message, 2.25)

    bot.send_message(message.chat.id, 'Теперь количество символов по вертикали нужно выбрать тебе. Напиши число и я использую его при обработке твоей картинки')
    bot.register_next_step_handler(message, user_survey.get_height, user_data)


def show_bg_color_example(message, user_data: UserData):
    path_to_bg1 = os.path.join(TUTORIAL_IMAGES_DIR, 'bg1.jpg')
    path_to_bg2 = os.path.join(TUTORIAL_IMAGES_DIR, 'bg2.jpg')

    photo_group = [
        types.InputMediaPhoto(open(path_to_bg1, 'rb')),
        types.InputMediaPhoto(open(path_to_bg2, 'rb'))
    ]
    bot.send_media_group(message.chat.id, photo_group)
    bot.send_message(message.chat.id, 'Тут я поменял цвет фона на красный и синий', reply_markup=types.ReplyKeyboardRemove())

    set_pause_between_messages(message, 1)

    bot.send_message(message.chat.id,
                     'Выбери цвет фона для твоей картинки нажав кнопку внизу '
                     'или напиши свой в формате rgb (например: 200 150 255)',
                     reply_markup=user_survey.colors_buttons_markup)
    bot.register_next_step_handler(message, user_survey.get_bg_color, user_data)


def show_symbols_example(message, user_data: UserData):
    bot.send_message(message.chat.id, 'Еще можно выбрать символы из которых будет создаваться арт', reply_markup=types.ReplyKeyboardRemove())

    set_pause_between_messages(message, 1.25)

    path_to_symbols = os.path.join(TUTORIAL_IMAGES_DIR, 'symbols.jpg')
    with open(path_to_symbols, 'rb') as file:
        bot.send_photo(message.chat.id, file)

    bot.send_message(message.chat.id, 'Вот например я использовал только символ @')

    set_pause_between_messages(message, 1.75)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    standard_btn = types.KeyboardButton('стандартный набор')
    markup.add(standard_btn)
    bot.send_message(message.chat.id, 'Можешь написать символы из которых будет создаваться твой арт или использовать стандартный набор', reply_markup=markup)

    bot.register_next_step_handler(message, user_survey.get_symbols, user_data)


def finish_first_phase(message, user_data: UserData):
    bot.send_message(message.chat.id, 'Окей, сохранил твои настройки')
    work_with_result.make_result(message, user_data)


def start_second_phase(message, user_data: UserData):
    user_data.tutorial_phase = TutorialPhase.second

    set_pause_between_messages(message, 2.25)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    true_color_btn = types.KeyboardButton('true color')
    markup.add(true_color_btn)

    bot.send_message(message.chat.id, 'Это был обычный режим, еще есть режим true color, нажми на кнопку и я обработаю твою картинку в этом режиме', reply_markup=markup)

    bot.register_next_step_handler(message, user_survey.get_mode, user_data)


def finish_second_phase(message, user_data: UserData):
    bot.send_message(message.chat.id, 'Активирован режим true color', reply_markup=types.ReplyKeyboardRemove())
    work_with_result.make_result(message, user_data)


def finish_tutorial(message, user_data: UserData):
    set_pause_between_messages(message, 2)

    user_id = message.from_user.id
    users_db_work.update_user_data(user_id, 1, 0)

    bot.send_message(message.chat.id, 'Еще я умею обрабатывать видео, там все точно также', reply_markup=types.ReplyKeyboardRemove())
    set_pause_between_messages(message, 0.5)

    bot.send_message(message.chat.id, 'Все, теперь ты знаешь как делать арты, можешь присылать изображение или видео')


def set_pause_between_messages(message, sleep_time):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(sleep_time)
