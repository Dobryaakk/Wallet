import asyncio
import text
import requests


from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from fake_useragent import UserAgent

from create import history, currency_db, balance
from keyboard import keyboard
from create import bot

ua = UserAgent()

headers = {
      "User-Agent": ua.random
}


currency = {1: "EUR 🇪🇺", 2: "USD 🇺🇸", 3: "RUB 🇷🇺", 4: "UAH 🇺🇦", 5: "KZT 🇰🇿", 6: "PLN 🇵🇱"}
currency_ = ["EUR", "USD", "RUB", "UAH", "KZT", "PLN"]
currency_l = {"EUR": 'євро', "USD": "долар", "RUB": "рубль", "UAH": "гривня", "KZT": "теньге", "PLN": "злотий"}
currency_get = {1: "EUR", 2: "USD", 3: "RUB", 4: "UAH", 5: "KZT", 6: "PLN"}


def get_exchange_rate(currency_code):
    url = f"https://api.exchangerate-api.com/v4/latest/{currency_get.get(currency_db.get_default_pred_value())}"
    response = requests.get(url)
    data = response.json()
    exchange_rate = data["rates"][currency_code]
    return exchange_rate


async def process_conversion(callback: types.CallbackQuery):
    global flag_base
    await callback.message.edit_text("<i>⏳ отримую актуальні данні, секунду...</i>", parse_mode='HTML')
    await asyncio.sleep(0.1)

    base_currency = currency_get.get(currency_db.get_default_pred_value())
    euro_amount = balance.check_money(callback.from_user.id)

    results = []
    for target_currency in currency_:
        if target_currency == base_currency:
            continue

        exchange_rate = get_exchange_rate(target_currency)
        converted_amount = euro_amount * exchange_rate
        flag_base = currency.get(list(currency_get.keys())[list(currency_get.values()).index(base_currency)])
        flag_target = currency.get(list(currency_get.keys())[list(currency_get.values()).index(target_currency)])

        result_line = f'<b>{converted_amount:.2f}</b>  <i>{flag_target} ({currency_l[target_currency]})</i>'
        results.append(result_line)

    unique_results = list(set(results))
    result_text = "\n".join(unique_results)
    await callback.message.edit_text(f'<i>Ваш баланс</i> <b>{euro_amount:.2f} '
                                     f'{flag_base}</b>.\n\n<i>Конвертація у інші валюти:</i>\n\n{result_text}',
                                     reply_markup=keyboard.back_conv(), parse_mode="HTML")


class FSM(StatesGroup):
    bal = State()
    welcome = State()
    pred = State()


async def money(callback: types.CallbackQuery):
    if callback.data == "main_balance":
        da = balance.check_money(callback.from_user.id)
        await callback.message.edit_text(f"<i>Ваш баланс складає</i> <b>{da} {currency.get(currency_db.get_default_pred_value())}</b>",
                                         reply_markup=keyboard.balance(), parse_mode='HTML')
    elif callback.data == "main_costs":
        await callback.message.edit_text(
            "<i>📊 в цьому розділі ви маєте можливість вводити витрати, щоб потім зручно "
            "відстежувати їх та формувати статистику на основі здійснених витрат</i>",
            reply_markup=keyboard.costs_menu(), parse_mode='HTML')
    elif callback.data == 'main_static':
        await callback.message.edit_text('<i>В цьому розділі ви маєте можливість переглядати статистику щодо ваших поповнень та витрат</i>', reply_markup=keyboard.statistick(), parse_mode='HTML')


async def add_money(callback: types.CallbackQuery):
    if callback.data == "add_money":
        await FSM.bal.set()
        await callback.message.edit_text("<i>Щоб поповнити баланс, потрібно ввести суму на яку бажаєте поповнити 💰</i>", reply_markup=keyboard.back(), parse_mode='HTML')
    elif callback.data == 'add_konvert':
        await process_conversion(callback)
    elif callback.data == "add_back":
        await callback.message.edit_text(
            text.start_not, reply_markup=keyboard.main_keyboard(), parse_mode="HTML")
    elif callback.data == 'add_back_b':
        da = balance.check_money(callback.from_user.id)
        await callback.message.edit_text(
            f"<i>Ваш баланс складає</i> <b>{da} {currency.get(currency_db.get_default_pred_value())}</b>",
            reply_markup=keyboard.balance(), parse_mode='HTML')


async def back_all_menu(callback: types.CallbackQuery):
    if callback.data == 'back':
        await callback.message.edit_text(
            text.start_not, reply_markup=keyboard.main_keyboard(), parse_mode="HTML")
    if callback.data == "back_balance":
        da = balance.check_money(callback.from_user.id)
        await callback.message.edit_text(
            f"<i>Ваш баланс складає</i> <b>{da} {currency.get(currency_db.get_default_pred_value())}</b>",
            reply_markup=keyboard.balance(), parse_mode='HTML')


async def pred_settings(callback: types.CallbackQuery):
    pred_options = {
        'pred_one': 'EUR 🇪🇺',
        'pred_two': 'USD 🇺🇸',
        'pred_three': 'RUB 🇷🇺',
        'pred_four': 'UAH 🇺🇦',
        'pred_five': 'KZT 🇰🇿',
        'pred_sex': 'PLN 🇵🇱'
    }

    pred_data = {
        'pred_one': 1,
        'pred_two': 2,
        'pred_three': 3,
        'pred_four': 4,
        'pred_five': 5,
        'pred_sex': 6
    }

    pred_key = callback.data
    if pred_key in pred_options:
        currency_code = pred_options[pred_key]
        pred_value = pred_data[pred_key]
        currency_db.insert_or_update_data(callback.from_user.id, callback.from_user.full_name, pred_value)
        message_text = f"<i>Виберіть валюту для подальшого використання 💶\n\nВибрано:</i> <b>{currency_code}</b>"
        await callback.message.edit_text(message_text, reply_markup=keyboard.currency(currency_db.get_default_pred_value()), parse_mode="HTML")

    elif pred_key == 'pred_agree':
        await callback.message.delete()
        await callback.message.answer(
            text.start_not, reply_markup=keyboard.main_keyboard(), parse_mode="HTML")


async def rules(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['bal'] = message.text
            history.add_money_history(message.from_user.id, message.text)
            balance.add_money(message.from_user.id, message.text)
            message_delete = message.message_id - 1
            message_delete_2 = message.message_id
            await bot.delete_message(message.chat.id, message_delete)
            await bot.delete_message(message.chat.id, message_delete_2)
            await message.answer(
                f"<i>Ваш баланс поповнено на</i> <b>{message.text}</b>"
                f" {currency.get(currency_db.get_default_pred_value())}\n<i>Тепер ваш баланс нараховує</i>"
                f" <b>{balance.check_money(message.from_user.id)} {currency.get(currency_db.get_default_pred_value())}</b>",
                reply_markup=keyboard.back_in_main(), parse_mode='HTML')
            await state.finish()
    else:
        await message.answer("<b>Потрібно вводити тільки цілі числа</b>")


async def back_with_fsm_rules(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    da = balance.check_money(callback.from_user.id)
    await callback.message.edit_text(
        f"<i>Ваш баланс складає</i> <b>{da} {currency.get(currency_db.get_default_pred_value())}</b>",
        reply_markup=keyboard.balance(), parse_mode='HTML')


def register_balance(dp: Dispatcher):
    dp.register_message_handler(get_exchange_rate, commands=['p'])
    dp.register_callback_query_handler(money, lambda callback_query: callback_query.data.startswith('main'))
    dp.register_callback_query_handler(add_money, lambda callback_query: callback_query.data.startswith('add'))
    dp.register_callback_query_handler(back_all_menu, lambda callback_query: callback_query.data.startswith('back'))
    dp.register_callback_query_handler(pred_settings, lambda callback_query: callback_query.data.startswith('pred'))
    dp.register_message_handler(rules, state=FSM.bal)
    dp.register_callback_query_handler(back_with_fsm_rules, state="*", text='fsm_back')
