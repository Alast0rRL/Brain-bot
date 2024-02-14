@bot.message_handler(commands=['F','f'])
def start_om(message):
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
        start_f(message)
    else:
        # Если пользователь ввел что-то другое, завершаем работу
        global F
        F=0
        bot.reply_to(message, 'GigaBrain завершил свою работу')
