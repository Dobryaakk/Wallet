import io
import text
import matplotlib.pyplot as plt

from aiogram import types

from create import history, currency_db, balance, bot
from create import Dispatcher
from keyboard import keyboard


currency_l = {"EUR": 'євро', "USD": "длр", "RUB": "руб", "UAH": "грн", "KZT": "тенге", "PLN": "злоты"}
currency = {1: "EUR 🇪🇺", 2: "USD 🇺🇸", 3: "RUB 🇷🇺", 4: "UAH 🇺🇦", 5: "KZT 🇰🇿", 6: "PLN 🇵🇱"}


async def statistic_m(callback: types.CallbackQuery):
    subtract_history = history.get_subtract_history_by_id(callback.from_user.id)
    amounts = [entry['amount'] for entry in subtract_history]
    dates = [str(entry['timestamp']) for entry in subtract_history]

    formatted_dates = [f"{date[:4]}\n{date[4:6]}-{date[6:]}" for date in dates]
    x_labels = [f"{date[:4]}\n{date[4:6]}-{date[6:]}" for date in dates]

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(formatted_dates)), amounts)
    plt.xlabel('Дата')
    plt.ylabel('Сума')
    plt.title('Графік витрат')

    for i, amount in enumerate(amounts):
        plt.text(i, amount + 0.1, str(amount), ha='center')

    if len(amounts) <= 10:
        step = 2
    elif 10 < len(amounts) <= 30:
        step = 3
    elif 30 < len(amounts) <= 60:
        step = 5
    elif 60 < len(amounts) <= 90:
        step = 5
    elif 90 < len(amounts) <= 120:
        step = 5
    else:
        step = 10

    plt.xticks(range(0, len(formatted_dates), step), [date for i, date in enumerate(x_labels) if i % step == 0])

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    add = 'subtract'
    total = int(balance.check_money(callback.from_user.id))
    de = round(history.get_average(callback.from_user.id, add), 0)
    await callback.message.edit_text("<b>Нижче ви можете ознайомитись зі статистикою</b>", parse_mode='HTML')
    await callback.message.answer_photo(photo=types.InputFile(buf, filename='graph.png'))
    await callback.message.answer('<b>📊 коротко про ваші витрати ⬇️</b>\n\n'
                                  f'<i>Всього витрачено</i> <b>{history.get_sum(callback.from_user.id, add)} '
                                  f'{currency.get(currency_db.get_default_pred_value())}</b>\n\n'
                                  f'<i>В середньому ви витрачаєте</i> '
                                  f'<b>{round(history.get_average(callback.from_user.id, add), 0) if history.get_average(callback.from_user.id, add) != 0 else "лддл"}</b>'
                                  f' {currency.get(currency_db.get_default_pred_value())}</b> <i>в день</i>\n\n'
                                  f'<i>Судячи з даних ваших коштів, вам вистачить приблизно на</i> <b>{total // de}</b>'
                                  f' <i>днів</i>' if de != 0 else '<i>Судячи з даних ваших коштів, неможливо розрахувати</i>'
                                  f' <i>днів</i>', reply_markup=keyboard.stat_back(), parse_mode='HTML')

    buf.close()


async def statistic_a(callback: types.CallbackQuery):
    subtract_history = history.get_add_history_by_id(callback.from_user.id)

    amounts = [entry['amount'] for entry in subtract_history]
    dates = [str(entry['timestamp']) for entry in subtract_history]

    formatted_dates = [f"{date[:4]}\n{date[4:6]}-{date[6:]}" for date in dates]
    x_labels = [f"{date[:4]}\n{date[4:6]}-{date[6:]}" for date in dates]

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(formatted_dates)), amounts)
    plt.xlabel('Дата')
    plt.ylabel('Сума')
    plt.title('Графік поповнень')

    for i, amount in enumerate(amounts):
        plt.text(i, amount + 0.1, str(amount), ha='center')

    if len(amounts) <= 10:
        step = 2
    elif 10 < len(amounts) <= 30:
        step = 3
    elif 30 < len(amounts) <= 60:
        step = 5
    elif 60 < len(amounts) <= 90:
        step = 5
    elif 90 < len(amounts) <= 120:
        step = 5
    else:
        step = 10

    plt.xticks(range(0, len(formatted_dates), step), [date for i, date in enumerate(x_labels) if i % step == 0])

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    add_sum = 'add'
    ku = currency.get(currency_db.get_default_pred_value())
    await callback.message.edit_text("<b>Нижче ви можете ознайомитись зі статистикою</b>",parse_mode='HTML')
    await callback.message.answer_photo(photo=types.InputFile(buf, filename='graph.png'))
    await callback.message.answer('<b>📊 коротко про ваші поповнення ⬇️</b>\n\n'
                                  f'<i>Взагалом ви поповнили</i> <b>{history.get_sum(callback.from_user.id, add_sum)}'
                                  f' {currency.get(currency_db.get_default_pred_value())}</b>\n\n'
                                  f'<i>В середньому ви поповняєте свій баланс на</i> '
                                  f'<b>{round(history.get_average(callback.from_user.id, add_sum), 0)} '
                                  f'{currency.get(currency_db.get_default_pred_value())}</b>',
                                  reply_markup=keyboard.stat_back(), parse_mode='HTML')

    buf.close()


async def stats(calback: types.CallbackQuery):
    if calback.data == 'statistick_back':
        message_1 = calback.message.message_id - 2
        message_2 = calback.message.message_id - 1
        message_3 = calback.message.message_id
        await bot.delete_message(calback.message.chat.id, message_1)
        await bot.delete_message(calback.message.chat.id, message_2)
        await bot.delete_message(calback.message.chat.id, message_3)
        await calback.message.answer(
            text.start_not, reply_markup=keyboard.main_keyboard(), parse_mode="HTML")
    elif calback.data == 'statistick_back_main':
        await calback.message.edit_text(
            text.start_not, reply_markup=keyboard.main_keyboard(), parse_mode="HTML")


def register_cost(dp: Dispatcher):
    dp.register_callback_query_handler(statistic_m, text='statistick_minuse')
    dp.register_callback_query_handler(statistic_a, text='statistick_add')
    dp.register_callback_query_handler(stats, text=['statistick_back', 'statistick_back_main'])
