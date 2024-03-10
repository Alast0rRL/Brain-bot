from config import bot
from config import whitelist
# Обработчик команды /om
F = 0
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
