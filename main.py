# Импортируем необходимые библиотеки
import json
import telebot
import cmath
import cv2
import os
from telebot import types
from math import sqrt


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
        # Отправляем сообщение с описанием команд
        bot.reply_to(message, "/Om-Калькулятор сопротивлений\n/Disk-Решить квадратное уравнение\n/gl_form - Главная формула")
        # Создаем клавиатуру
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Сопротивление")
        btn2 = types.KeyboardButton("Ёмкость")
        btn3 = types.KeyboardButton("Дискриминант")
        btn4 = types.KeyboardButton("Главная формула")
        btn5 = types.KeyboardButton("Перевести в СИ")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        # Отправляем клавиатуру пользователю
        bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)

@bot.message_handler(commands=['Id','id'])
def start_id(message):
    bot.reply_to(message, message.from_user.id)

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
    info = message.text.split(" ")
    otvet = result(float(info[0]), info[1], info[2])
    bot.reply_to(message, format(otvet, '.25f'))

    # except Exception as e:
    #     # Если возникла ошибка, отправляем сообщение об ошибке
    #     bot.reply_to(message, 'Ошибка!')

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
    if '/add_id' in message.text and message.from_user.id == admin_id:
        id = int(message.text.split()[-1])
        add_id(id)
        bot.reply_to(message, "id добавлен")
        # тут ответ от бота своего пропиши, я хз что у тебя за библиотека
    elif '/del_id' in message.text and message.from_user.id == admin_id:
        id = int(message.text.split()[-1])
        del_id(id)
        bot.reply_to(message, "id удалён")
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



def add_id(id):
  whitelist.append(id)
  with open(f'{filename}.json', 'w') as file:
    json.dump({"ids": whitelist}, file)

def del_id(id):
  whitelist.remove(id)
  with open(f'{filename}.json', 'w') as file:
    json.dump({"ids": whitelist}, file)








# Запускаем бота
bot.polling()
