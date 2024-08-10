from telebot import TeleBot
import os

token = os.environ["BOT_TOKEN"]
bot = TeleBot(token)

owner_chat_id = os.environ["OWNER_ID"]

CURRENT_DIR = os.getcwd()
users_db_path = os.path.join('data', 'users_db.sql')
ads_db_path = os.path.join('data', 'ads_db.sql')
