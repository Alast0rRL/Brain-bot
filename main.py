# Импортируем необходимые библиотеки
import telebot
import cmath
from telebot import types

# Создаем экземпляр бота
bot = telebot.TeleBot("6855751951:AAHALEUqgT7puSUEZ0FwubhaMdWadjoVQVs")

# Инициализируем переменную для хранения сопротивления
R = 0

# Обработчик команд '/start' и '/help'
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

# Обработчик команд '/Om' и '/om'
@bot.message_handler(commands=['Om','om'])
def start_om(message):
    # Запрашиваем у пользователя данные и регистрируем следующий шаг
    msg = bot.reply_to(message, "Введите сопротивление в формате:\n1 10 15 20\n1-Последовательное соединение. 2 - Паралельное\nВсе последующие числа это номинал резисторов")
    bot.register_next_step_handler(msg, process_soprotiv1_step)

@bot.message_handler(commands=['Disk','disk'])
def start_disk(message):
    # Запрашиваем у пользователя данные и регистрируем следующий шаг
    msg = bot.reply_to(message, "Введите уровнение в формате 2 5 -2")
    bot.register_next_step_handler(msg, procces_disk_step)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def func(message):
    # Если пользователь выбрал "Сопротивление", начинаем расчет
    if(message.text == "Сопротивление"):
        start_om(message)
    elif(message.text == "Дискриминант"):
       start_disk(message)
# Функция для расчета сопротивления
def process_soprotiv1_step(message):
    try:
        global R
        # Преобразуем введенные данные в список чисел
        info = list(map(int, message.text.split()))
        # Если первое число 1, считаем сумму сопротивлений
        if int(info[0]) == 1:
            r = sum(el for el in info[1:] if isinstance(el, (int, float)))
            R += int(r)
        # Если первое число 2, считаем обратную сумму сопротивлений
        elif int(info[0]) == 2:
            i = 1
            for el in info[1:]:
                r = info[i]
                i += 1    
                R += (1/r)
        # Если R - целое число, преобразуем его в int
        if R == int(R):
            R = int(R)
        # Отправляем результат пользователю
        bot.send_message(message.chat.id, R)
        # Запрашиваем у пользователя подтверждение для продолжения
        msg = bot.reply_to(message, "Для продолжения введите: +")
        bot.register_next_step_handler(msg, check_for_restart)
    except Exception as e:
        # Если возникла ошибка, отправляем сообщение об ошибке
        bot.reply_to(message, 'Ошибка! Введите числовое значение.')

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

def procces_disk_step(message):
# Запрашиваем коэффициенты у пользователя
    urav = message.text
    urav_split = urav.split(" ")
# Вычисляем дискриминант
    D = float(urav_split[1])**2 - 4*float(urav_split[0])*float(urav_split[2])
    msg = bot.reply_to(message,D)

# Вычисляем корни
    root1 = (-float(urav_split[1]) - cmath.sqrt(D)) / (2 * float(urav_split[0]))
    root2 = (-float(urav_split[1]) + cmath.sqrt(D)) / (2 * float(urav_split[0]))

    msg = bot.reply_to(message, root1)
    msg = bot.reply_to(message, root2)











# Запускаем бота
bot.polling()
