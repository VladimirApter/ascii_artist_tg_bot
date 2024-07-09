from config import bot
from work_with_result import send_result


def get_height(message, user_data):
    height = int(message.text.strip())
    user_data['height'] = height

    send_result(message, user_data)
