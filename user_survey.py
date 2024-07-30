import re
from telebot import types

from config import bot
from work_with_result import make_result
import tutorial
from data_structures import *
from ascii_artist.symbols_packs import SymbolsPacks


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
            return
        elif message.text is not None:
            import commands_handle
            if message.text == '/start':
                restart_commands.start_handler(message)
                return
            elif message.text == '/help':
                restart_commands.help_handler(message)
                return
            elif message.text == '/limits':
                restart_commands.limits_handler(message)
                return
            elif message.text == '/ideas':
                restart_commands.ideas_handler(message)
                return

        handler(message, user_data)

    return inner


def start_survey(message, user_data: UserData):
    bot.send_message(message.chat.id, 'Теперь напиши сколько символов хочешь по вертикали')
    bot.register_next_step_handler(message, get_height, user_data)


@restart_possibility
def get_height(message, user_data: UserData):

    valid = False
    height = 0
    max_height = user_data.media.max_height
    try:
        height = int(message.text.strip(' ,!.символ(ов/а)symbols'))
    except (ValueError, AttributeError):
        pass
    else:
        if 1 <= height <= max_height:
            valid = True

    if not valid:
        bot.send_message(message.chat.id, 'Количество символов для '
                         f'{user_data.russian_orientation} '
                         f'{user_data.russian_file_type} '
                         f'- число от 1 до {max_height}, '
                         f'попробуй еще раз')
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


def get_symbols_markup(user_data: UserData):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    standard_btn = types.KeyboardButton('стандартный набор')
    markup.add(standard_btn)

    others_btn = types.KeyboardButton('посмотреть все наборы')
    markup.add(others_btn)

    return markup


@restart_possibility
def get_mode(message, user_data: UserData):
    if message.text == 'обычный':
        user_data.mode = Mode.regular

        bot.send_message(message.chat.id, 'Выбери цвет фона или напиши свой в формате rgb (например: 200 150 255)', reply_markup=colors_buttons_markup)
        bot.register_next_step_handler(message, get_bg_color, user_data)
    elif message.text == 'true color':
        user_data.mode = Mode.true_color

        if not user_data.first_time:
            markup = get_symbols_markup(user_data)

            bot.send_message(message.chat.id, 'Можешь написать символы из которых будет создаваться арт или использовать готовый набор', reply_markup=markup)
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
        markup = get_symbols_markup(user_data)

        bot.send_message(message.chat.id, 'Можешь написать символы из которых будет создаваться арт или использовать готовый набор', reply_markup=markup)
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
        bot.send_message(message.chat.id, 'Отправь текстовые символы из которых будет создаваться арт, либо выбери готовый набор')
        bot.register_next_step_handler(message, get_symbols, user_data)
        return
    if message.text == 'стандартный набор':
        symbols = None
    elif message.text == 'посмотреть все наборы':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        standard_btn = types.KeyboardButton('стандартный')
        russian_btn = types.KeyboardButton('русский')
        greek_btn = types.KeyboardButton('греческий')
        japanese_btn = types.KeyboardButton('японский')
        arabian_btn = types.KeyboardButton('арабский')
        angles_btn = types.KeyboardButton('уголки')
        braille_btn = types.KeyboardButton('Брайля')

        markup.add(standard_btn)
        markup.row(russian_btn, greek_btn)
        markup.row(japanese_btn, arabian_btn)
        markup.row(angles_btn, braille_btn)

        bot.send_message(message.chat.id, 'Вот все готовые наборы', reply_markup=markup)
        bot.register_next_step_handler(message, get_symbols, user_data)
        return
    elif message.text == 'стандартный':
        symbols = None
    elif message.text == 'русский':
        symbols = SymbolsPacks.russian
    elif message.text == 'греческий':
        symbols = SymbolsPacks.greek
    elif message.text == 'японский':
        symbols = SymbolsPacks.japanese
    elif message.text == 'арабский':
        symbols = SymbolsPacks.arabian
    elif message.text == 'уголки':
        symbols = SymbolsPacks.angles
    elif message.text == 'Брайля':
        symbols = SymbolsPacks.braille

    user_data.symbols = symbols

    if not user_data.first_time:
        bot.send_message(message.chat.id, 'Настройки сохранены', reply_markup=types.ReplyKeyboardRemove())
        finish_survey(message, user_data)
    else:
        tutorial.finish_first_phase(message, user_data)


def finish_survey(message, user_data: UserData):
    make_result(message, user_data)
