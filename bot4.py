import os
import telebot
from dotenv import load_dotenv
from weather_parse.weather_parse import weather


env = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env):
    load_dotenv(env)
    TOKEN = os.getenv("TOKEN")
    ADMIN_ID = os.getenv("ADMIN_ID")
else:
    raise Exception('Файл ".env" отсутствует.')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет")


@bot.message_handler(commands=["weather"])
def get_wather(message):
    data = weather()
    bot.send_message(message.chat.id, data[1])


bot.infinity_polling()
