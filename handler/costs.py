from aiogram import types, Dispatcher
from database.bd import Balance, Database_pred, History
from keyboard import keyboard
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create import bot

my_money = Balance('database.db')
db_pred = Database_pred('database.db')
history = History('database.db')


class FSM(StatesGroup):
    bal = State()
    new_bal = State()


currency = {1: "EUR 🇪🇺", 2: "USD 🇺🇸", 3: "RUB 🇷🇺", 4: "UAH 🇺🇦", 5: "KZT 🇰🇿", 6: "PLN 🇵🇱"}


async def costs_main(callback: types.CallbackQuery):
    if callback.data == 'costs_add':
        await FSM.new_bal.set()
        await callback.message.edit_text("<i>Введіть суму яку ви витратили 📉</i>", reply_markup=keyboard.back(), parse_mode='HTML')
    elif callback.data == 'costs_history':
        user_id = callback.from_user.id
        history_file = history.create_history_file(user_id)
        if history_file:
            with open(history_file, 'rb') as file:
                await callback.message.delete()
                await bot.send_document(chat_id=user_id, document=file)
                await callback.message.answer("<i>⬆️ в файлі вище зібрана вся історія ваших витрачень</i>",
                                              reply_markup=keyboard.all_logg(), parse_mode='HTML')
        else:
            await callback.message.edit_text("<i>Ви ще нічого не витратили ‼️\nЗробіть витрату щоб відкрити можливість переглядати меню</i>", reply_markup=keyboard.costs_back(), parse_mode='HTML')
    elif callback.data == 'costs_back':
        if history.get_subtract_history_by_id(callback.from_user.id) == None:
            await callback.message.edit_text(
                    "<i>📊 в цьому розділі ви маєте можливість вводити витрати, щоб потім зручно "
                        "відстежувати їх та формувати статистику на основі здійснених витрат</i>", reply_markup=keyboard.costs_menu(), parse_mode='HTML')
        else:
            message_delete = callback.message.message_id - 1
            message_delete_2 = callback.message.message_id
            await bot.delete_message(callback.message.chat.id, message_delete)
            await bot.delete_message(callback.message.chat.id, message_delete_2)
            await callback.message.answer(
                "<i>📊 в цьому розділі ви маєте можливість вводити витрати, щоб потім зручно "
                "відстежувати їх та формувати статистику на основі здійснених витрат</i>",
                reply_markup=keyboard.costs_menu(), parse_mode='HTML')


async def cost(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if int(my_money.check_money(message.from_user.id)) - int(message.text) < 0:
            da = my_money.check_money(message.from_user.id)
            await message.answer(
                f"<i>❌ нажаль ви не можете зробити таку витрату оскілкьи у вас немає стілкьи коштів</i>\n\n<i>Ваш баланс складає</i> <b>{da} {currency.get(db_pred.get_default_pred_value())}</b>", parse_mode='HTML')
        else:
            async with state.proxy() as data:
                data['new_bal'] = message.text
                my_money.minuse_money(message.from_user.id, int(message.text))
                history.subtract_money(message.from_user.id, int(message.text))
                message_delete = message.message_id - 1
                message_delete_2 = message.message_id
                await bot.delete_message(message.chat.id, message_delete)
                await bot.delete_message(message.chat.id, message_delete_2)
                await message.answer(
                    f"<i>Ви витратили</i> <b>{message.text}"
                    f" {currency.get(db_pred.get_default_pred_value())}</b>\n<i>Тепер ваш баланс нараховує</i>"
                    f" <b>{my_money.check_money(message.from_user.id)} {currency.get(db_pred.get_default_pred_value())}</b>",
                    reply_markup=keyboard.back_in_main(), parse_mode='HTML')
            await state.finish()
    else:
        await message.answer("<b>Потрібно вводити тільки цифри</b>")


async def back_with_fsm_rules(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    da = my_money.check_money(callback.from_user.id)
    await callback.message.edit_text(
        f"<i>Ваш баланс складає</i> <b>{da} {currency.get(db_pred.get_default_pred_value())}</b>",
        reply_markup=keyboard.balance(), parse_mode='HTML')


def register_cost(dp: Dispatcher):
    dp.register_callback_query_handler(costs_main, lambda callback_query: callback_query.data.startswith('costs'))
    dp.register_message_handler(cost, state=FSM.new_bal)
    dp.register_callback_query_handler(back_with_fsm_rules, state="*", text='fsm_back')
