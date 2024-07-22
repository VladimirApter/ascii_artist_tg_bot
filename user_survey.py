import re
from telebot import types

from config import bot
from work_with_result import make_result
import tutorial
from data_structures import *


colors_dict = {'⚫️': [0, 0, 0], '⚪️': [255, 255, 255], '🔴': [255, 0, 0],
               '🟠': [255, 165, 0], '🟡': [255, 255, 0], '🟢': [0, 255, 0],
               '🔵': [0, 0, 255], '🟣': [139, 0, 255]}

colors_buttons_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
colors_buttons = []
for color in colors_dict.keys():
    colors_buttons.append(types.KeyboardButton(color))
colors_buttons_markup.row(*colors_buttons)


def restart_possibility(handler):
    def inner(message, user_data: UserData):
        if message.photo:
            from photo_processing import get_photo  # to solve circular import problem
            get_photo(message, user_data)
            return
        elif message.video:
            from video_processing import get_video  # to solve circular import problem
            get_video(message, user_data)

        handler(message, user_data)

    return inner


def start_survey(message, user_data: UserData):
    bot.send_message(message.chat.id, 'Теперь напиши сколько символов хочешь по вертикали')
    bot.register_next_step_handler(message, get_height, user_data)


@restart_possibility
def get_height(message, user_data: UserData):
    file_type = user_data.file_type

    valid = False
    height = 0
    try:
        height = int(message.text.strip(' ,!.символ(ов/а)symbols'))
    except (ValueError, AttributeError):
        pass
    else:
        if file_type == FileType.photo and 1 <= height <= 1000:
            valid = True
        elif file_type == FileType.video and 1 <= height <= 200:
            valid = True

    if not valid:
        if file_type == FileType.photo:
            bot.send_message(message.chat.id, 'Количество символов для фото - число от 1 до 1000, попробуй еще раз')
        elif file_type == FileType.video:
            bot.send_message(message.chat.id, 'Количество символов для видео - число от 1 до 200, попробуй еще раз')
        bot.register_next_step_handler(message, get_height, user_data)
        return

    user_data.height = height

    if not user_data.first_time:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        regular_btn = types.KeyboardButton('обычный')
        true_color_btn = types.KeyboardButton('true color')
        markup.row(regular_btn, true_color_btn)
        bot.send_message(message.chat.id, 'Теперь нужно выбрать режим обработки', reply_markup=markup)
        bot.register_next_step_handler(message, get_mode, user_data)
    else:
        tutorial.show_bg_color_example(message, user_data)


@restart_possibility
def get_mode(message, user_data: UserData):
    if message.text == 'обычный':
        user_data.mode = Mode.regular

        bot.send_message(message.chat.id, 'Выбери цвет фона или напиши свой в формате rgb (например: 200 150 255)', reply_markup=colors_buttons_markup)
        bot.register_next_step_handler(message, get_bg_color, user_data)
    elif message.text == 'true color':
        user_data.mode = Mode.true_color

        if not user_data.first_time:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            standard_btn = types.KeyboardButton('стандартный набор')
            markup.add(standard_btn)

            bot.send_message(message.chat.id, 'Можешь написать символы из которых будет создаваться арт или использовать стандартный набор', reply_markup=markup)
            bot.register_next_step_handler(message, get_symbols, user_data)
        else:
            tutorial.finish_second_phase(message, user_data)
    else:
        bot.send_message(message.chat.id, 'Чтобы выбрать режим нажми на одну из кнопок ниже')
        bot.register_next_step_handler(message, get_mode, user_data)


@restart_possibility
def get_bg_color(message, user_data: UserData):
    bg_color = get_color(message)
    if bg_color is None:
        bot.send_message(message.chat.id, 'Неверный формат, свой цвет можно задать в формате rgb: r g b (r, g, b - любые числа от 0 до 255), попробуй еще раз')
        bot.register_next_step_handler(message, get_bg_color, user_data)
        return
    user_data.bg_color = bg_color

    bot.send_message(message.chat.id, 'Теперь укажи цвет шрифта', reply_markup=colors_buttons_markup)
    bot.register_next_step_handler(message, get_font_color, user_data)


@restart_possibility
def get_font_color(message, user_data: UserData):
    font_color = get_color(message)
    if font_color is None:
        bot.send_message(message.chat.id, 'Неверный формат, свой цвет можно задать в формате rgb: r g b (r, g, b - любые числа от 0 до 255), попробуй еще раз')
        bot.register_next_step_handler(message, get_font_color, user_data)
        return
    user_data.font_color = font_color

    if not user_data.first_time:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        standard_btn = types.KeyboardButton('стандартный набор')
        markup.add(standard_btn)

        bot.send_message(message.chat.id, 'Можешь написать символы из которых будет создаваться арт или использовать стандартный набор', reply_markup=markup)
        bot.register_next_step_handler(message, get_symbols, user_data)
    else:
        tutorial.show_symbols_example(message, user_data)


def get_color(message):
    try:
        text = message.text.strip()
    except AttributeError:
        return None
    if text in colors_dict:
        return colors_dict[text]

    try:
        color_list = list(map(int, filter(None, re.split(r'[^\d-]', message.text))))
        if len(color_list) != 3 or not all(0 <= color_channel <= 255 for color_channel in color_list):
            return None
        return color_list
    except ValueError:
        return None


@restart_possibility
def get_symbols(message, user_data: UserData):
    try:
        symbols = message.text.strip() + ' '
    except AttributeError:
        bot.send_message('Отправь текстовые символы из которых будет создаваться арт, либо нажми "стандартный набор", чтобы использовать символы по умолчанию')
        bot.register_next_step_handler(message, get_symbols, user_data)
        return
    if message.text == 'стандартный набор':
        symbols = None
    user_data.symbols = symbols

    if not user_data.first_time:
        bot.send_message(message.chat.id, 'Настройки сохранены', reply_markup=types.ReplyKeyboardRemove())
        finish_survey(message, user_data)
    else:
        tutorial.finish_first_phase(message, user_data)


def finish_survey(message, user_data: UserData):
    make_result(message, user_data)
