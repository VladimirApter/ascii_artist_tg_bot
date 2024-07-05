import telebot
import os
import ascii_artist.main

bot = telebot.TeleBot("7146497668:AAG5wBIrMEoho64W2F9MnSzYPyDPLrnqMto")
CURRENT_DIR = os.getcwd()
IMAGES_DIR_PATH = ''
VIDEOS_DIR_PATH = ''
FILE_ID = ''
FILE_PATH = ''


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Готов работать, отправь изображение или видео")


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    global FILE_PATH, IMAGES_DIR_PATH, FILE_ID

    FILE_ID = message.photo[-1].file_id
    file_info = bot.get_file(FILE_ID)
    downloaded_file = bot.download_file(file_info.file_path)

    IMAGES_DIR_PATH = os.path.join(CURRENT_DIR, 'ascii_artist', 'images')
    file_name = f"user{message.from_user.id}_file{FILE_ID}.jpg"
    FILE_PATH = os.path.join(IMAGES_DIR_PATH, file_name)

    with open(FILE_PATH, 'wb') as f:
        f.write(downloaded_file)

    bot.reply_to(message, "Принял фото, теперь укажи какое количество символов хочешь по вертикали")
    bot.register_next_step_handler(message, process_photo)


def process_photo(message):
    height = int(message.text.strip())

    ascii_artist.main.main(FILE_PATH, height)
    result_path = os.path.join(CURRENT_DIR, 'ascii_artist', 'images', f'user{message.from_user.id}_file{FILE_ID}_ascii_art.jpg')

    with open(result_path, 'rb') as result_photo:
        bot.send_photo(message.chat.id, result_photo)



@bot.message_handler(content_types=['video'])
def process_video(message):
    bot.reply_to(message, "Принял видео")


bot.polling(none_stop=True)
