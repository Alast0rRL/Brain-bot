# Импортируем необходимые библиотеки
import json
import telebot
import cmath
import cv2
import os
import qrcode
from telebot import types
from math import sqrt
from g4f.client import Client

# Добавляем ключ API GPT-4
gpt4_api_key = 'ваш_ключ_api_gpt4'

# Создаем экземпляр бота
bot = telebot.TeleBot("ваш_токен_бота")
client = Client(api_key=gpt4_api_key)

filename = "members"
admin_id = '1753676469'

with open(f'{filename}.json') as file:
    whitelist = json.load(file)['ids']

# Инициализируем переменную для хранения сопротивления
R = 0

# Обработчик команд /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначала, халявы он захотел")
    else:
        # Создаем клавиатуру
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Сопротивление")
        btn2 = types.KeyboardButton("Ёмкость")
        btn3 = types.KeyboardButton("Дискриминант")
        btn4 = types.KeyboardButton("Главная формула")
        btn5 = types.KeyboardButton("Перевести в СИ")
        btn6 = types.KeyboardButton("QR Code")
        btn7 = types.KeyboardButton("GPT 3.5(fast)")
        btn8 = types.KeyboardButton("GPT 4(slow)")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
        # Отправляем клавиатуру пользователю
        bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)

@bot.message_handler(commands=['Id','id'])
def start_id(message):
    bot.reply_to(message, message.from_user.id)

@bot.message_handler(commands=['GPT3.5', 'gpt3.5'])
def start_gpt3(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначала, халявы он захотел")
    else:
        msg = bot.reply_to(message, "Введите сообщение для GPT-3.5")
        bot.register_next_step_handler(msg, process_gpt3_step)

def process_gpt3_step(message):
    input_message = message.text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Вы общаетесь с AI, обученным OpenAI."},
            {"role": "user", "content": input_message},
        ]
    )
    bot.reply_to(message, response['choices'][0]['message']['content'])
    # После каждого ответа проверяем, хочет ли пользователь задать еще вопрос
    msg = bot.reply_to(message, "Для нового вопроса введите '+', для выхода '-'")
    bot.register_next_step_handler(msg, check_gpt3_restart)

def check_gpt3_restart(message):
    if message.text == '+':
        start_gpt3(message)
    elif message.text == '-':
        send_welcome(message)

@bot.message_handler(commands=['GPT4','Gpt4','gpt4'])
def start_gpt(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначала, халявы он захотел")
    else:
        msg = bot.reply_to(message, "Введите сообщение")
        bot.register_next_step_handler(msg, process_gpt_step)

def process_gpt_step(message):
    input_message = message.text
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Вы общаетесь с AI, обученным OpenAI."},
            {"role": "user", "content": input_message},
        ]
    )
    bot.reply_to(message, response['choices'][0]['message']['content'])
    # После каждого ответа проверяем, хочет ли пользователь задать еще вопрос
    msg = bot.reply_to(message, "Для нового вопроса введите '+', для выхода '-'")
    bot.register_next_step_handler(msg, check_gpt_restart)

def check_gpt_restart(message):
    if message.text == '+':
        start_gpt(message)
    elif message.text == '-':
        send_welcome(message)

# Далее идет ваш код, не затрагивающий обработку GPT

# ...

# Запускаем бота
bot.polling()