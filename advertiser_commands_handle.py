from config import bot
import ads_config


def register_commands():
    from main import breakdown_handler

    @bot.message_handler(commands=['show_ads_by_owner_id'])
    @breakdown_handler
    def show_ads(message):
        show_ads_handler(message)


def show_ads_handler(message):
    try:
        id = message.text.split()[1]
    except IndexError:
        bot.send_message(message.chat.id, 'Дополните запрос id')
        return
    ad = get_ad_by_id(id)
    if ad is None:
        bot.send_message(message.chat.id, 'Рекламы с соответствующим id нет')
        return
    ad.show(message)


def get_ad_by_id(id):
    ads_bearer = ads_config.ADS_BEARER
    if ads_bearer.ads_group is None:
        return None
    for ad in ads_bearer.ads_group:
        if ad.id == id:
            return ad
    return None
