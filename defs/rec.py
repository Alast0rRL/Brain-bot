from config import bot
from config import whitelist
@bot.message_handler(commands=['Rec', 'rec'])
def start_rec(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначало, халявы он захотел")
    else:
        # Запрашиваем у пользователя данные и регистрируем следующий шаг
        msg = bot.reply_to(message, "Отправьте изображение")
        bot.register_next_step_handler(msg, step_rec)

def step_rec(message):
    chat_id = message.chat.id

    # Сохраняем фото
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('image.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)