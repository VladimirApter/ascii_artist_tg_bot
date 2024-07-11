import re

from config import bot
from work_with_result import send_result


def survey_start(message, user_data):
    _get_height(message, user_data)


def _get_height(message, user_data):
    height = int(message.text.strip())
    user_data['height'] = height

    bot.send_message(message.chat.id, 'Окей, теперь укажи цвет фона в формате rgb, например: 200 150 255')
    bot.register_next_step_handler(message, _get_bg_color, user_data)


def _get_bg_color(message, user_data):
    bg_color = list(map(int, filter(None, re.split(r'\W+', message.text))))
    user_data['bg_color'] = bg_color

    bot.send_message(message.chat.id, 'Теперь так же укажи цвет шрифта')
    bot.register_next_step_handler(message, _get_font_color, user_data)


def _get_font_color(message, user_data):
    font_color = list(map(int, filter(None, re.split(r'\W+', message.text))))
    user_data['font_color'] = font_color

    survey_finish(message, user_data)


def survey_finish(message, user_data):
    send_result(message, user_data)
