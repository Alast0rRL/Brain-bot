from g4f.client import Client
from config import bot
from config import whitelist
@bot.message_handler(commands=['GPT4','Gpt4','gpt4'])
def start_gpt(message):
    if message.from_user.id not in whitelist:
        bot.reply_to(message, "Бота купи сначало, халявы он захотел")
    else:
        msg = bot.reply_to(message, "Введите сообщение")
        bot.register_next_step_handler(msg, process_gpt_step)

def process_gpt_step(message):
    input_message = message.text
    client = Client()
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Вы общаетесь с AI, обученным OpenAI."},
        {"role": "user", "content": input_message},
    ]
    )
    msg = bot.reply_to(message, response.choices[0].message.content)
    bot.register_next_step_handler(msg, check_gpt_restart)

def check_gpt_restart(message):
    if message.text == 'Назад':
        bot.reply_to(message, 'Giga GPT завершил свою работу')
        
    if message.text == '-':
        bot.reply_to(message, 'Giga GPT завершил свою работу')
    else:
        process_gpt_step(message)