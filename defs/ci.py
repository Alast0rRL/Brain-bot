from config import bot
from config import whitelist
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
