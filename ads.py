import os
from telebot.types import InputMediaPhoto, InputMediaVideo
import work_with_db

from config import bot, CURRENT_DIR
ads_media_dir = os.path.join(CURRENT_DIR, 'ads_media')


class AdsBearer:
    media_between_ads_count = 2

    def __init__(self, ads_group):
        self.ads_group = ads_group

    def show_ad(self, message):
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
    def __init__(self, caption: str, images: [str] = None, videos: [str] = None):
        self.caption = caption
        self.images_paths = []
        if images is not None:
            self.images_paths = [os.path.join(ads_media_dir, img) for img in images]
        self.videos_paths = []
        if videos is not None:
            self.videos_paths = [os.path.join(ads_media_dir, vid) for vid in videos]

    def show(self, message):
        media_group = []
        open_files = []
        for path in self.images_paths:
            photo = open(path, 'rb')
            open_files.append(photo)
            media_group.append(InputMediaPhoto(media=photo, caption=self.caption))
        for path in self.videos_paths:
            video = open(path, 'rb')
            open_files.append(video)
            media_group.append(InputMediaVideo(media=video))

        bot.send_media_group(message.chat.id, media_group)

        for file in open_files:
            file.close()
