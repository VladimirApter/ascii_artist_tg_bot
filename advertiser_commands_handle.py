from config import bot
import ads_config
import ads_db_statistic
import users_db_work


def register_commands():
    from main import breakdown_handler

    @bot.message_handler(commands=['show_ad_by_id'])
    @breakdown_handler
    def show_ad(message):
        show_ad_handler(message)

    @bot.message_handler(commands=['show_ad_statistic_by_id'])
    @breakdown_handler
    def show_ad_statistic(message):
        show_ad_statistic_handler(message)

    @bot.message_handler(commands=['show_ad_for_user_statistic_by_id_and_name'])
    @breakdown_handler
    def show_ad_for_user_statistic(message):
        show_ad_for_user_statistic_handler(message)


def get_id_from_command(message):
    try:
        id = message.text.split()[1]
    except IndexError:
        bot.send_message(message.chat.id, 'Дополните запрос id')
        return None
    return id


def get_ad_by_id(message, id):
    ads_bearer = ads_config.ADS_BEARER
    if ads_bearer.ads_group is None:
        bot.send_message(message.chat.id, 'Рекламы с таким id нет')
        return None
    for ad in ads_bearer.ads_group:
        if ad.id == id:
            return ad
    bot.send_message(message.chat.id, 'Рекламы с таким id нет')
    return None


def get_user_id_by_name_from_command(message):
    try:
        name = message.text.split()[2]
    except IndexError:
        bot.send_message(message.chat.id, 'Дополните запрос именем пользователя')
        return None

    id = users_db_work.get_user_id_by_name(name)
    if id is None:
        bot.send_message(message.chat.id, 'Этот пользователь еще не пользовался ботом')
        return None

    return id


def show_ad_handler(message):
    id = get_id_from_command(message)
    if id is None:
        return

    ad = get_ad_by_id(message, id)
    if ad is None:
        return

    ad.show(message)


def show_ad_statistic_handler(message):
    id = get_id_from_command(message)
    if id is None:
        return

    ad = get_ad_by_id(message, id)
    if ad is None:
        return

    total_views = ads_db_statistic.get_total_ad_views(ad.id)
    average_views = ads_db_statistic.get_average_ad_views(ad.id)

    bot.send_message(message.chat.id, f'Всего реклама просмотрена {total_views} раз\nВ среднем каждый пользователь посмотрел вашу рекламу {average_views} раз')


def show_ad_for_user_statistic_handler(message):
    ad_id = get_id_from_command(message)
    if ad_id is None:
        return

    ad = get_ad_by_id(message, ad_id)
    if ad is None:
        return

    user_id = get_user_id_by_name_from_command(message)

    user_views = ads_db_statistic.get_user_ad_views(user_id, ad_id)
    bot.send_message(message.chat.id, f'Этот пользователь посмотрел вашу рекламу {user_views} раз')
