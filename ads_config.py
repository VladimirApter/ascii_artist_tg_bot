import os

import ads
import ads_db_work
from config import CURRENT_DIR

ADS_MEDIA_DIR = os.path.join(CURRENT_DIR, 'data', 'ads_data')

ADS_BEARER = ads.AdsBearer()


def get_folders_paths(directory_path):
    folders_paths = []
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            folders_paths.append(item_path)
    return folders_paths


def extract_data(folder_path):
    images_paths = []
    videos_paths = []
    caption = None
    url = None
    url_caption = None
    id = None

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if not os.path.isfile(item_path):
            return

        if item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            images_paths.append(item_path)
        elif item.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            videos_paths.append(item_path)
        elif item == 'caption.txt':
            with open(item_path, 'r', encoding='utf-8') as file:
                caption = file.read()
        elif item == 'url.txt':
            with open(item_path, 'r', encoding='utf-8') as file:
                url = file.read()
        elif item == 'id.txt':
            with open(item_path, 'r', encoding='utf-8') as file:
                id = file.read().strip()
        elif item == 'url_caption.txt':
            with open(item_path, 'r', encoding='utf-8') as file:
                url_caption = file.read()

    return images_paths, videos_paths, caption, url, url_caption, id


def update_ads_group():
    global ADS_BEARER

    ads_group = []

    folders = get_folders_paths(ADS_MEDIA_DIR)
    for folder in folders:
        images_paths, videos_paths, caption, url, url_caption, id = extract_data(folder)
        ad = ads.Ad(id, caption, images_paths, videos_paths, url, url_caption)
        ads_group.append(ad)

    ADS_BEARER.ads_group = ads_group

    ads_db_work.update_ads(ADS_BEARER.ads_group)
