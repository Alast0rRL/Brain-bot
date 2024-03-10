import cmath
from config import bot
from config import whitelist
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