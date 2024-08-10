from telebot import TeleBot
import os

token = os.environ["BOT_TOKEN"]
bot = TeleBot(token)

owner_chat_id = os.environ["OWNER_ID"]

CURRENT_DIR = os.getcwd()

