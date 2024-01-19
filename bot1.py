import os
import webbrowser

import telebot
from dotenv import load_dotenv


env = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env):
    load_dotenv(env)
    TOKEN = os.getenv("TOKEN")
    ADMIN_ID = os.getenv("ADMIN_ID")
else:
    raise Exception('Файл ".env" отсутствует.')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["site"])
def site(message):
    webbrowser.open("https://google.com")


@bot.message_handler(commands=["start", "main", "hello"])
def main(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name} {message.from_user.last_name}",
    )


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(
        message.chat.id,
        "<b>Help</b> <em><u>information</u></em>",
        parse_mode="html",
    )


@bot.message_handler()
def info(message):
    if message.text.lower() == "привет":
        bot.send_message(
            message.chat.id,
            f"Привет, {message.from_user.first_name} {message.from_user.last_name}",
        )
    elif message.text.lower() == "id":
        bot.reply_to(message, f"ID: {message.from_user.id}")


bot.infinity_polling()
