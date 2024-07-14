import re
from telebot import types

from config import bot
from work_with_result import send_result


colors_dict = {'⚫️': [0, 0, 0], '⚪️': [255, 255, 255], '🔴': [255, 0, 0],
               '🟠': [255, 165, 0], '🟡': [255, 255, 0], '🟢': [0, 255, 0],
               '🔵': [0, 0, 255], '🟣': [139, 0, 255]}

colors_buttons_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
colors_buttons = []
for color in colors_dict.keys():
    colors_buttons.append(types.KeyboardButton(color))
colors_buttons_markup.row(*colors_buttons)


def start_survey(message, user_data):
    _get_height(message, user_data)


def _get_height(message, user_data):
    height = int(message.text.strip())
    user_data['height'] = height

    bot.send_message(message.chat.id, 'Выбери цвет фона или напиши свой в формате rgb, например: 200 150 255', reply_markup=colors_buttons_markup)
    bot.register_next_step_handler(message, _get_bg_color, user_data)


def _get_bg_color(message, user_data):
    user_data['bg_color'] = _get_color(message)

    bot.send_message(message.chat.id, 'Теперь так же укажи цвет шрифта', reply_markup=colors_buttons_markup)
    bot.register_next_step_handler(message, _get_font_color, user_data)


def _get_font_color(message, user_data):
    user_data['font_color'] = _get_color(message)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    standard_btn = types.KeyboardButton('стандартный набор')
    markup.add(standard_btn)

    bot.send_message(message.chat.id, 'Можешь написать символы из которых будет создаваться арт или использовать стандартный набор', reply_markup=markup)
    bot.register_next_step_handler(message, _get_symbols, user_data)


def _get_color(message):
    text = message.text.strip()
    if text in colors_dict:
        return colors_dict[text]
    return list(map(int, filter(None, re.split(r'\W+', message.text))))


def _get_symbols(message, user_data):
    symbols = message.text.strip() + ' '
    if message.text == 'стандартный набор':
        symbols = None
    user_data['symbols'] = symbols

    bot.send_message(message.chat.id, 'Настройки сохранены', reply_markup=types.ReplyKeyboardRemove())
    finish_survey(message, user_data)


def finish_survey(message, user_data):
    send_result(message, user_data)
