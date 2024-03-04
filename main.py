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
import openai

openai.api_key = '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'





filename = "members"

admin_id = '1753676469'

with open(f'{filename}.json') as file:
  whitelist = json.load(file)['ids']



# Создаем экземпляр бота
bot = telebot.TeleBot("6855751951:AAHALEUqgT7puSUEZ0FwubhaMdWadjoVQVs")
# Инициализируем переменную для хранения сопротивления
F = 0
R = 0
# Обработчик командs /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.from_user.id not in whitelist:
       bot.reply_to(message, "Бота купи сначало, халявы он захотел")
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
    response = openai.Completion.create(
        engine="text-davinci-003",  # Выберите движок, например, "text-davinci-003"
        prompt=input_message,
        max_tokens=150  # Максимальное количество токенов в ответе
    )
    msg = bot.reply_to(message, response.choices[0].text.strip())
    bot.register_next_step_handler(msg, check_gpt3_restart)

def check_gpt3_restart(message):
    if message.text == ' ':
        bot.reply_to(message, 'GPT-3.5 завершил свою работу')
        
    if message.text == '-':
        bot.reply_to(message, 'GPT-3.5 завершил свою работу')
        send_welcome(message)
    else:
        process_gpt3_step(message)


@bot.message_handler(commands=['GPT4','Gpt4','gpt4'])
def start_gpt(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначало, халявы он захотел")
    else:
        msg = bot.reply_to(message, "Введите сообщение")
        bot.register_next_step_handler(msg, process_gpt_step)

def process_gpt_step(message):
    input_message = message.text
    client = Client()
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Вы общаетесь с AI, обученным OpenAI."},
        {"role": "user", "content": input_message},
    ]
    )
    msg = bot.reply_to(message, response.choices[0].message.content)
    bot.register_next_step_handler(msg, check_gpt_restart)

def check_gpt_restart(message):
    if message.text == ' ':
        bot.reply_to(message, 'Giga GPT завершил свою работу')
        
    if message.text == '-':
        bot.reply_to(message, 'Giga GPT завершил свою работу')
        send_welcome(message)
    else:
        process_gpt_step(message)


@bot.message_handler(commands=['ci','Ci','si','Si'])
def start_ci(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначало, халявы он захотел")
    else:
        msg = bot.reply_to(message, "Введите сообщение в формате:\n1 к г\n где 1 к-исходная величина в кило\n г-требуемая величина в гига")
        bot.register_next_step_handler(msg, process_ci_step)
def process_ci_step(message):
    #try:
    UNITS = {
    'p': 1e-12,
    'п': 1e-12,

    'n': 1e-9,
    'н': 1e-9,
    'mk': 1e-6,
    'мк': 1e-6,

    'm': 1e-3,
    'м': 1e-3,

    '0': 1,

    'K': 1e3,
    'К': 1e3,

    'M': 1e6,
    'М': 1e6,

    'G': 1e9,
    'Г': 1e9,

    'T': 1e12,
    'Т': 1e12
}
    def result(value, from_unit,
        to_unit): return UNITS[from_unit] * value / UNITS[to_unit]
    try:
        info = message.text.split(" ")
        otvet = result(float(info[0]), info[1], info[2])
        bot.reply_to(message, format(otvet, '.25f'))

    except Exception as e:
        # Если возникла ошибка, отправляем сообщение об ошибке
        bot.reply_to(message, 'Ошибка!')

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        # Сохраняем фото
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('image.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)




        # Ждем 1 минуту
        # Чтение изображения
        image = cv2.imread("image.jpg")

        # Преобразование изображения в оттенки серого
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Инвертирование изображения
        inverted = 255 - gray_image

        # Размытие инвертированного изображения
        blur = cv2.GaussianBlur(inverted, (21, 21), 0)

        # Инвертирование размытого изображения
        invertedblur = 255 - blur

        # Создание эскиза
        sketch = cv2.divide(gray_image, invertedblur, scale=256.0)

        # Сохранение эскиза
        cv2.imwrite("sketch_image.png", sketch)







        # Отправляем фото обратно пользователю
        img = open('sketch_image.png', 'rb')
        bot.send_photo(chat_id, img)
        img.close()

        # Удаляем фото с компьютера
        os.remove("image.jpg")
        os.remove("sketch_image.png")
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(commands=['Qr','qr'])
def start_qr(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначало, халявы он захотел")
    else:
        # Запрашиваем у пользователя данные и регистрируем следующий шаг
        msg = bot.reply_to(message, "Отправьте текст, который вы хотите сконвертировать в QR-код")
        bot.register_next_step_handler(msg, create_qr_code)
def create_qr_code(message):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(message.text)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save('qr_code.png')
    
    with open('qr_code.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    os.remove("qr_code.png")

@bot.message_handler(commands=['F','f'])
def start_f(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначало, халявы он захотел")
    else:
        # Запрашиваем у пользователя данные и регистрируем следующий шаг
        msg = bot.reply_to(message, "Введите ёмкости в формате:\n1 10 15 20\n1-Последовательное соединение. 2 - Паралельное\nВсе последующие числа это номинал резисторов")
        bot.register_next_step_handler(msg, process_f_step)
# Функция для расчета сопротивления
def process_f_step(message):
    try:
        global F
        # Преобразуем введенные данные в список чисел
        info = list(map(float, message.text.split()))
        # Если первое число 1, считаем сумму сопротивлений
        if float(info[0]) == 2:
            r = sum(el for el in info[1:] if isinstance(el, (int, float)))
            F += int(r)
        # Если первое число 2, считаем обратную сумму сопротивлений
        elif float(info[0]) == 1:
            i = 1
            for el in info[1:]:
                r = info[i]
                i += 1    
                F += (1/r)
        # Если R - целое число, преобразуем его в int
        if F == int(F):
            F = int(F)
        # Отправляем результат пользователю
        bot.send_message(message.chat.id, str(R)+" Фарад")
        # Запрашиваем у пользователя подтверждение для продолжения
        msg = bot.reply_to(message, "Для продолжения введите: +")
        bot.register_next_step_handler(msg, check_for_restart_f)
    except Exception as e:
        # Если возникла ошибка, отправляем сообщение об ошибке
        bot.reply_to(message, 'Ошибка!')
# Функция для проверки, хочет ли пользователь продолжить
def check_for_restart_f(message):
    if message.text == '+':
        # Если пользователь ввел '+', продолжаем расчет
        start_f(message)
    else:
        # Если пользователь ввел что-то другое, завершаем работу
        global F
        F=0
        bot.reply_to(message, 'GigaBrain завершил свою работу')


# Обработчик команды /om
@bot.message_handler(commands=['Om','om'])
def start_om(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначало, халявы он захотел")
    else:
        # Запрашиваем у пользователя данные и регистрируем следующий шаг
        msg = bot.reply_to(message, "Введите сопротивление в формате:\n1 10 15 20\n1-Последовательное соединение. 2 - Паралельное\nВсе последующие числа это номинал резисторов")
        bot.register_next_step_handler(msg, process_soprotiv1_step)
# Функция для расчета сопротивления
def process_soprotiv1_step(message):
    try:
        global R
        # Преобразуем введенные данные в список чисел
        info = list(map(float, message.text.split()))
        # Если первое число 1, считаем сумму сопротивлений
        if float(info[0]) == 1:
            r = sum(el for el in info[1:] if isinstance(el, (int, float)))
            R += int(r)
        # Если первое число 2, считаем обратную сумму сопротивлений
        elif float(info[0]) == 2:
            i = 1
            for el in info[1:]:
                r = info[i]
                i += 1    
                R += (1/r)
        # Если R - целое число, преобразуем его в int
        if R == int(R):
            R = int(R)
        # Отправляем результат пользователю
        bot.send_message(message.chat.id, str(R)+" Ом")
        # Запрашиваем у пользователя подтверждение для продолжения
        msg = bot.reply_to(message, "Для продолжения введите: +")
        bot.register_next_step_handler(msg, check_for_restart)
    except Exception as e:
        # Если возникла ошибка, отправляем сообщение об ошибке
        bot.reply_to(message, 'Ошибка!')
# Функция для проверки, хочет ли пользователь продолжить
def check_for_restart(message):
    if message.text == '+':
        # Если пользователь ввел '+', продолжаем расчет
        start_om(message)
    else:
        # Если пользователь ввел что-то другое, завершаем работу
        global R
        R=0
        bot.reply_to(message, 'GigaBrain завершил свою работу')

# Обработчик команды /disk
@bot.message_handler(commands=['Disk','disk'])
def start_disk(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначало, халявы он захотел")
    else:
        # Запрашиваем у пользователя данные и регистрируем следующий шаг
        msg = bot.reply_to(message, "Введите уровнение в формате 2 5 -2")
        bot.register_next_step_handler(msg, procces_disk_step)
# Функция для решения квадратного
def procces_disk_step(message):
    try:
# Запрашиваем коэффициенты у пользователя
        urav = message.text
        urav_split = urav.split(" ")
# Вычисляем дискриминант
        D = float(urav_split[1])**2 - 4*float(urav_split[0])*float(urav_split[2])
        msg = bot.reply_to(message,"D="+str(D))

# Вычисляем корни
        root1 = (-float(urav_split[1]) - cmath.sqrt(D)) / (2 * float(urav_split[0]))
        root2 = (-float(urav_split[1]) + cmath.sqrt(D)) / (2 * float(urav_split[0]))

        msg = bot.reply_to(message, "x1="+str(root1))
        msg = bot.reply_to(message, "x2="+str(root2))
    except Exception as e:
         # Если возникла ошибка, отправляем сообщение об ошибке
         bot.reply_to(message, 'Ошибка!')

# Обработчик команды /gl_form
@bot.message_handler(commands=['Gl_form','gl_form'])
def start_gl_form(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначало, халявы он захотел")
    else:
        # Запрашиваем у пользователя данные и регистрируем следующий шаг
        msg = bot.reply_to(message, "Введите данные в формате\nI Pn U cosFi KPD")
        bot.register_next_step_handler(msg, procces_gl_form_step)
#главная формула
def procces_gl_form_step(message):
    try:
        info = list((message.text.split()))
        if info[0]== "x":
            formula = "In=Pn/(sqrt(3)*Un*cosFi*KPD"
            result = float(info[1])/(sqrt(3)*float(info[2])*float(info[3])*float(info[4]))
            bot.reply_to(message, formula)
            bot.reply_to(message, 'In='+str(result)+" A")
        elif info[1] == "x":
            formula = "Pn=In*sqrt(3)*Un*cosFi*KPD"
            result = float(info[0])*sqrt(3)*float(info[2])*float(info[3])*float(info[4])
            bot.reply_to(message, formula)
            bot.reply_to(message, 'Pn='+str(result)+" Вт")
        elif info[2] == "x":
            formula = "Un=Pn/(sqrt(3)*In*cosFi*KPD"
            result = float(info[1])/(sqrt(3)*float(info[0])*float(info[3])*float(info[4]))
            bot.reply_to(message, formula)
            bot.reply_to(message, 'Un='+str(result)+" В")
        elif info[3] == "x":
            formula = "cosFi=Pn/(sqrt(3)*In*Un*KPD"
            result = float(info[1])/(sqrt(3)*float(info[0])*float(info[2])*float(info[4]))
            bot.reply_to(message, formula)
            bot.reply_to(message, 'cosFi='+str(result))
        elif info[4] == "x":
            formula = "KPD=Pn/(sqrt(3)*In*Un*cosFi"
            result = float(info[1])/(sqrt(3)*float(info[0])*float(info[2])*float(info[3]))
            bot.reply_to(message, formula)
            bot.reply_to(message, 'KPD='+str(result))
    except Exception as e:
         # Если возникла ошибка, отправляем сообщение об ошибке
         bot.reply_to(message, 'Ошибка!')

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def button(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначало, халявы он захотел")
    else:
        # Если пользователь выбрал "Сопротивление", начинаем расчет
        if(message.text == "Сопротивление"):
            start_om(message)
        elif(message.text == "Дискриминант"):
            start_disk(message)
        elif(message.text == "Ёмкость"):
            start_f(message)            
        elif(message.text == "Главная формула"):
            start_gl_form(message)
        elif(message.text == "Перевести в СИ"):
            start_ci(message)
        elif(message.text == "QR Code"):
            start_qr(message)
        elif(message.text == "GPT 3.5(fast)"):
            start_gpt3(message)
        elif(message.text == "GPT 4(slow)"):
            start_gpt(message)







# Запускаем бота
bot.polling()
