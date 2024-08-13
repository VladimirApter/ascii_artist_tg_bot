from telebot import TeleBot
import os

token = os.environ["BOT_TOKEN"]
bot = TeleBot(token)

owner_chat_ids = [int(id) for id in os.environ["OWNER_IDS"].split('|')]

CURRENT_DIR = os.getcwd()
data_dir_path = os.path.join(CURRENT_DIR, '/data')
users_db_path = os.path.join(data_dir_path, 'users_db.sql')
ads_db_path = os.path.join(data_dir_path, 'ads_db.sql')


def make_ads_data_dir():
    ads_data_path = os.path.join(data_dir_path, 'ads_data')
    if not os.path.exists(ads_data_path):
        os.makedirs(ads_data_path)
