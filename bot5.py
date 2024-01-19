import os
import telebot
from telebot import types
from dotenv import load_dotenv
from currency_converter import CurrencyConverter


env = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env):
    load_dotenv(env)
    TOKEN = os.getenv("TOKEN")
    ADMIN_ID = os.getenv("ADMIN_ID")
else:
    raise Exception('Файл ".env" отсутствует.')

bot = telebot.TeleBot(TOKEN)

currency = CurrencyConverter()


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Введите сумму")
    bot.register_next_step_handler(message, summa)


amount = 0


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат, впишите сумму")
        bot.register_next_step_handler(message, summa)
        return  # Чтобы последующий код не выполнялся в случае перехвата исключения

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("USD/EUR", callback_data="USD/EUR")
        btn2 = types.InlineKeyboardButton("EUR/USD", callback_data="EUR/USD")
        btn3 = types.InlineKeyboardButton("USD/GBP", callback_data="USD/GBP")
        btn4 = types.InlineKeyboardButton("Другое значение", callback_data="else")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Выберите пару валют", reply_markup=markup)
    else:
        bot.send_message(
            message.chat.id, "Число должно быть больше чем 0. Впишите сумму"
        )
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "else":
        bot.send_message(call.message.chat.id, "Введите пару значений через слеш.")
        bot.register_next_step_handler(call.message, my_currency)
    else:
        values = call.data.split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(
            call.message.chat.id,
            f"Получается: {round(res, 2)}. Можете заного ввести число.",
        )
        bot.register_next_step_handler(call.message, summa)


def my_currency(message):
    try:
        values = message.text.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(
            message.chat.id, f"Получается: {round(res, 2)}. Можете заного ввести число."
        )
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(
            message.chat.id,
            "Что-то не так, введите корректные наименования валют через слеш.",
        )
        bot.register_next_step_handler(message, my_currency)


bot.infinity_polling()
