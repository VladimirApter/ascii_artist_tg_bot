from config import bot
import ads_config
import users_db_statistic


def register_commands():
    from main import breakdown_handler

    @bot.message_handler(commands=['admin_command_update_ads_config'])
    @breakdown_handler
    def update_ads_config(message):
        update_ads_config_handler(message)

    @bot.message_handler(commands=['admin_command_get_users_count'])
    @breakdown_handler
    def get_users_count(message):
        get_users_count_handler(message)

    @bot.message_handler(commands=['admin_command_get_top_active_users'])
    @breakdown_handler
    def get_top_active_users(message):
        get_top_active_users_handler(message)

    @bot.message_handler(commands=['admin_command_get_average_counts'])
    @breakdown_handler
    def get_average_counts(message):
        get_average_counts_handler(message)

    @bot.message_handler(commands=['admin_command_get_first_20_users'])
    @breakdown_handler
    def get_first_20_users(message):
        get_first_20_users_handler(message)

    @bot.message_handler(commands=['admin_command_get_user_by_name'])
    @breakdown_handler
    def get_user_by_name(message):
        get_user_by_name_handler(message)


def update_ads_config_handler(message):
    ads_config.update_ads_group()
    bot.send_message(message.chat.id, 'ads config updated')


def get_users_count_handler(message):
    users_count = users_db_statistic.get_users_count()
    bot.send_message(message.chat.id, f'users count: {users_count}')


def get_top_active_users_handler(message):
    users_data = users_db_statistic.get_top_active_users()
    text = ''
    for index, (name, media_count) in enumerate(users_data):
        text += f'top {index + 1} active user - name: {name}, media count: {media_count}\n'
    if text == '':
        text = 'no data to send'
    bot.send_message(message.chat.id, text)


def get_average_counts_handler(message):
    average_photo_count, average_video_count = users_db_statistic.get_average_counts()
    bot.send_message(message.chat.id, f'average photo count: {average_photo_count}\naverage video count: {average_video_count}')


def get_first_20_users_handler(message):
    users_data = users_db_statistic.get_first_20_users()
    text = ''
    for user_data in users_data:
        for item in user_data:
            text += str(item) + ' '
        text += '\n'
    if text == '':
        text = 'no data to send'
    bot.send_message(message.chat.id, text)


def get_user_by_name_handler(message):
    try:
        user_name = message.text.split()[1]
    except IndexError:
        bot.send_message(message.chat.id, 'table has no user with this username')
        return
    id, photo_count, video_count = users_db_statistic.get_user_by_name(user_name)
    bot.send_message(message.chat.id, f'{user_name} data - id: {id}, photo count: {photo_count}, video count: {video_count}')
