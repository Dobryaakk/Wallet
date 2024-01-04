from aiogram import types, Dispatcher

from create import currency_db, bot
from keyboard import keyboard


currency = {1: "EUR 🇪🇺", 2: "USD 🇺🇸", 3: "RUB 🇷🇺", 4: "UAH 🇺🇦", 5: "KZT 🇰🇿", 6: "PLN 🇵🇱"}


async def start(message: types.Message):
    await message.answer(
        "<b>Привіт 👋🏼</b>\n\nЯ бот, створений для обліку твоїх фінансів та утворення статистики, "
        "щоб зробити управління грошима більш зручним. \n\n"
        "<i>Змінити валюту можна за допомогою команди <b>/change</b>.</i>\n",
        reply_markup=keyboard.main_keyboard(), parse_mode='HTML')


async def change(message: types.Message):
    message_delete = message.message_id - 1
    message_delete_2 = message.message_id
    await bot.delete_message(message.chat.id, message_delete)
    await bot.delete_message(message.chat.id, message_delete_2)
    await message.answer(f"<i>Виберіть валюту для подальшого використання 💶\n\nВибрано:</i> "
                         f"<b>{currency.get(currency_db.get_default_pred_value())}</b>",
                         reply_markup=keyboard.currency(currency_db.get_default_pred_value()), parse_mode="HTML")


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(change, commands=['change'])
