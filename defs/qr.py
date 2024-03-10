import os
import qrcode
from math import sqrt
from config import bot
from config import whitelist

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