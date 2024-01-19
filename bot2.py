import os

import telebot
from telebot import types
from dotenv import load_dotenv


env = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env):
    load_dotenv(env)
    TOKEN = os.getenv("TOKEN")
    ADMIN_ID = os.getenv("ADMIN_ID")
else:
    raise Exception('Файл ".env" отсутствует.')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=["photo"])
def get_photo(message):
    # Обработчик фото
    # + с кнопками в ответе
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Перейти на сайт", url="https://google.com")
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Удалить фото", callback_data="delete")
    btn3 = types.InlineKeyboardButton("Изменить текст", callback_data="edit")
    markup.row(btn2, btn3)
    bot.reply_to(message, "Какое красивое фото", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    # Обработчики упомянутых выше кнопок
    if callback.data == "delete":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == "edit":
        bot.edit_message_text(
            "Edit text", callback.message.chat.id, callback.message.message_id
        )


@bot.message_handler(commands=["start"])
def start(message):
    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Перейти на сайт")
    murkup.row(btn1)
    btn2 = types.KeyboardButton("Удалить фото")
    btn3 = types.KeyboardButton("Изменить текст")
    murkup.row(btn2, btn3)
    file = open("./static/7c6effea8b4f0a5c637c2de1c217237e.jpeg", "rb")
    bot.send_photo(message.chat.id, file, reply_markup=murkup)
    # bot.send_message(message.chat.id, 'Привет', reply_markup=murkup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == "Перейти на сайт":
        bot.send_message(message.chat.id, "web site is open")
    elif message.text == "Удалить фото":
        bot.send_message(message.chat.id, "Delete")


bot.polling(non_stop=True)
