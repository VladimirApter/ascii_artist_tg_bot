from telebot import types
from telebot.types import InputMediaPhoto, InputMediaVideo

import users_db_work
import ads_db_work
from config import bot


class AdsBearer:
    media_between_ads_count = 1

    def __init__(self, ads_group=None):
        self.ads_group = ads_group

    def show_ad(self, message):
        if self.ads_group is None:
            return

        user_id = message.from_user.id
        user_media_between_ads_count = users_db_work.get_user_column_value(user_id, users_db_work.BdTableColumns.media_between_ads_count) + 1
        if user_media_between_ads_count < self.media_between_ads_count:
            users_db_work.set_user_column_value(user_id, users_db_work.BdTableColumns.media_between_ads_count, user_media_between_ads_count)
            return

        users_db_work.set_user_column_value(user_id, users_db_work.BdTableColumns.media_between_ads_count, 0)
        last_showed_ad_index = users_db_work.get_user_column_value(user_id, users_db_work.BdTableColumns.last_showed_ad_index)
        ad_index = (last_showed_ad_index + 1) % len(self.ads_group)
        users_db_work.set_user_column_value(user_id, users_db_work.BdTableColumns.last_showed_ad_index, ad_index)

        ad = self.ads_group[ad_index]
        ad.show(message)


class Ad:
    def __init__(self, id: str = None, caption: str = '', images_paths: [str] = None, videos_paths: [str] = None, url: str = None, url_caption: str = None):
        self.id = id
        self.caption = caption

        self.images_paths = []
        if images_paths is not None:
            self.images_paths = images_paths

        self.videos_paths = []
        if videos_paths is not None:
            self.videos_paths = videos_paths

        self.url = url
        self.url_caption = url_caption

    def show(self, message):
        media_group = []
        open_files = []
        is_first_file = True

        media_files = [(self.images_paths, InputMediaPhoto), (self.videos_paths, InputMediaVideo)]

        for paths, media_type in media_files:
            for path in paths:
                media_file = open(path, 'rb')
                open_files.append(media_file)
                if self.url is None and is_first_file:
                    media_group.append(media_type(media=media_file, caption=self.caption))
                else:
                    media_group.append(media_type(media=media_file))
                is_first_file = False

        if len(media_group) == 1:
            is_photo = len(self.images_paths) != 0
            media_file = open_files[0]
            self.show_single_media_ad(message, media_file, is_photo)
        else:
            self.show_default_ad(message, media_group)

        for file in open_files:
            file.close()

        user_id = message.from_user.id
        ads_db_work.increment_user_ad_views(user_id, self.id)

    def show_default_ad(self, message, media_group):
        if self.url is not None and self.url_caption is not None:
            if media_group:
                bot.send_media_group(message.chat.id, media_group)
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton(self.url_caption, url=self.url))
            bot.send_message(message.chat.id, self.caption,
                             reply_markup=markup)
        else:
            if media_group:
                bot.send_media_group(message.chat.id, media_group)
            else:
                bot.send_message(message.chat.id, self.caption)

    def show_single_media_ad(self, message, media_file, is_photo):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(self.url_caption, url=self.url))
        if is_photo:
            bot.send_photo(message.chat.id, media_file, caption=self.caption, reply_markup=markup)
        else:
            bot.send_video(message.chat.id, media_file, caption=self.caption, reply_markup=markup)
