import telebot
import json

bot = telebot.TeleBot("6855751951:AAHALEUqgT7puSUEZ0FwubhaMdWadjoVQVs")
filename = "members"
admin_id = '1753676469'
with open(f'{filename}.json') as file:
  whitelist = json.load(file)['ids']