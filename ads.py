from telebot import types
from telebot.types import InputMediaPhoto, InputMediaVideo
import work_with_db

from config import bot


class AdsBearer:
    media_between_ads_count = 1

    def __init__(self, ads_group=None):
        self.ads_group = ads_group

    def show_ad(self, message):
        if self.ads_group is None:
            return
        user_id = message.from_user.id
        user_media_between_ads_count = work_with_db.get_user_column_value(user_id, work_with_db.BdTableColumns.media_between_ads_count) + 1
        if user_media_between_ads_count < self.media_between_ads_count:
            work_with_db.set_user_column_value(user_id, work_with_db.BdTableColumns.media_between_ads_count, user_media_between_ads_count)
            return
        work_with_db.set_user_column_value(user_id, work_with_db.BdTableColumns.media_between_ads_count, 0)
        last_showed_ad_index = work_with_db.get_user_column_value(user_id, work_with_db.BdTableColumns.last_showed_ad_index)
        ad_index = (last_showed_ad_index + 1) % len(self.ads_group)
        ad = self.ads_group[ad_index]
        ad.show(message)
        work_with_db.set_user_column_value(user_id, work_with_db.BdTableColumns.last_showed_ad_index, ad_index)


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
        for path in self.images_paths:
            photo = open(path, 'rb')
            open_files.append(photo)
            if self.url is not None:
                media_group.append(InputMediaPhoto(media=photo))
            else:
                media_group.append(InputMediaPhoto(media=photo, caption=self.caption))
        for path in self.videos_paths:
            video = open(path, 'rb')
            open_files.append(video)
            if self.url is not None:
                media_group.append(InputMediaVideo(media=video))
            else:
                media_group.append(InputMediaVideo(media=video, caption=self.caption))

        if self.url is not None and self.url_caption is not None:
            bot.send_media_group(message.chat.id, media_group)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(self.url_caption, url=self.url))
            bot.send_message(message.chat.id, self.caption, reply_markup=markup)
        else:
            bot.send_media_group(message.chat.id, media_group)

        for file in open_files:
            file.close()
