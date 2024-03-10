# Импортируем необходимые библиотеки
import cv2
import os
from config import *
from telebot import types
import defs.ci as ci
import defs.qr as qr
import defs.gl as gl
import defs.gpt4 as gpt4
import defs.disk as disk
import defs.farad as farad
import defs.om as om
import defs.rec as rec
# Обработчик командs /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.from_user.id not in whitelist:
       bot.reply_to(message, "Бота купи сначало, халявы он захотел")
    else:
        # Создаем клавиатуру
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Найти")
        btn2 = types.KeyboardButton("Главная формула")
        btn3 = types.KeyboardButton("Перевести в СИ")
        btn4 = types.KeyboardButton("QR Code")
        btn5 = types.KeyboardButton("Распознование текста")
        btn6 = types.KeyboardButton("GPT")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        # Отправляем клавиатуру пользователю
        bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)

@bot.message_handler(commands=['Id','id'])
def start_id(message):  
    bot.reply_to(message, message.from_user.id)

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





# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def button(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначало, халявы он захотел")
    else:
        # Если пользователь выбрал "Сопротивление", начинаем расчет
        
        if(message.text == "GPT"):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("GPT 3.5(fast)")
            btn2 = types.KeyboardButton("GPT 4(slow)")
            btn3 = types.KeyboardButton("Назад")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)
        elif(message.text == "Найти"):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Сопротивление")
            btn2 = types.KeyboardButton("Ёмкость")
            btn3 = types.KeyboardButton("Дискриминант")
            btn4 = types.KeyboardButton("Назад")
            markup.add(btn1, btn2, btn3, btn4)
            # Отправляем клавиатуру пользователю
            bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)
        elif(message.text == "Сопротивление"):
            om.start_om(message)
        elif(message.text == "Дискриминант"):
            disk.start_disk(message)
        elif(message.text == "Ёмкость"):
            farad.start_f(message)            
        elif(message.text == "Главная формула"):
            gl.start_gl_form(message)
        elif(message.text == "Перевести в СИ"):
            ci.start_ci(message)
        elif(message.text == "QR Code"):
            qr.start_qr(message)
        elif(message.text == "Распознование текста"):
            rec.start_rec(message)
        elif(message.text == "Назад"):
            send_welcome(message)
        elif(message.text == "GPT 3.5(fast)"):
            pass
        #start_gpt3(message)
        elif(message.text == "GPT 4(slow)"):
            gpt4.start_gpt(message)







# Запускаем бота
bot.polling()
