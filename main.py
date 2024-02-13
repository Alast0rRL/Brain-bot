# Импортируем необходимые библиотеки
import telebot
import cmath
from telebot import types
from math import sqrt

# Создаем экземпляр бота
bot = telebot.TeleBot("6855751951:AAHALEUqgT7puSUEZ0FwubhaMdWadjoVQVs")

# Инициализируем переменную для хранения сопротивления
R = 0




# Обработчик командs /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Отправляем сообщение с описанием команд
    bot.reply_to(message, "/Om-Калькулятор сопротивлений\n/Disk-Решить квадратное уравнение")
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Сопротивление")
    btn2 = types.KeyboardButton("Дискриминант")
    markup.add(btn1, btn2)
    # Отправляем клавиатуру пользователю
    bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)

# Обработчик команды /om
@bot.message_handler(commands=['Om','om'])
def start_om(message):
    # Запрашиваем у пользователя данные и регистрируем следующий шаг
    msg = bot.reply_to(message, "Введите сопротивление в формате:\n1 10 15 20\n1-Последовательное соединение. 2 - Паралельное\nВсе последующие числа это номинал резисторов")
    bot.register_next_step_handler(msg, process_soprotiv1_step)
# Обработчик команды /disk
@bot.message_handler(commands=['Disk','disk'])
def start_disk(message):
    # Запрашиваем у пользователя данные и регистрируем следующий шаг
    msg = bot.reply_to(message, "Введите уровнение в формате 2 5 -2")
    bot.register_next_step_handler(msg, procces_disk_step)

# Обработчик команды /gl_form
@bot.message_handler(commands=['Gl_form','gl_form'])
def start_gl_form(message):
    # Запрашиваем у пользователя данные и регистрируем следующий шаг
    msg = bot.reply_to(message, "Введите данные в формате\nI Pn U cosFi KPD")
    bot.register_next_step_handler(msg, procces_gl_form_step)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def button(message):
    # Если пользователь выбрал "Сопротивление", начинаем расчет
    if(message.text == "Сопротивление"):
        start_om(message)
    elif(message.text == "Дискриминант"):
       start_disk(message)




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
# Функция для решения квадратного
def procces_disk_step(message):
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











# Запускаем бота
bot.polling()
