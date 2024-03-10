from math import sqrt
from config import bot
from config import whitelist
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
