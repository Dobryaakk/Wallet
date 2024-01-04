from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Баланс", callback_data='main_balance')],
        [InlineKeyboardButton("Виртати", callback_data='main_costs')],
        [InlineKeyboardButton("Статистика", callback_data='main_static')]]
    )
    return markup


def balance() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Поповнити", callback_data='add_money'),
         (InlineKeyboardButton("Конвертувати", callback_data='add_konvert'))],
        [InlineKeyboardButton("Назад", callback_data='add_back')]]
    )
    return markup


def back() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data='fsm_back')]]
    )
    return markup

def back_conv() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data='add_back_b')]]
    )
    return markup

def back_in_main() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("В головне меню", callback_data='back')]]
    )
    return markup


def currency(pred_value):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='EUR' + (' ✅' if pred_value == 1 else ''), callback_data='pred_one'),
         InlineKeyboardButton(text='USD' + (' ✅' if pred_value == 2 else ''), callback_data='pred_two'),
         InlineKeyboardButton(text='RUB' + (' ✅' if pred_value == 3 else ''), callback_data='pred_three')],
        [InlineKeyboardButton(text='UAH' + (' ✅' if pred_value == 4 else ''), callback_data='pred_four'),
         InlineKeyboardButton(text='KZT' + (' ✅' if pred_value == 5 else ''), callback_data='pred_five'),
         InlineKeyboardButton(text="PLN" + (' ✅' if pred_value == 6 else ''), callback_data='pred_sex')],
        [InlineKeyboardButton(text="Підтвердити", callback_data="pred_agree")]
    ])
    return keyboard


def costs_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Добавити", callback_data="costs_add")],
        [InlineKeyboardButton("Історія", callback_data="costs_history")],
        [InlineKeyboardButton("Назад", callback_data='back')]]
    )
    return markup


def costs_back() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data='costs_back')]]
    )
    return markup


def all_logg() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Назад", callback_data='costs_back')]]
    )
    return markup


def statistick() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Витрати", callback_data='statistick_minuse'),
         InlineKeyboardButton("Поповнення", callback_data='statistick_add')],
        [InlineKeyboardButton("назад", callback_data='statistick_back_main')]]
    )
    return markup

def stat_back() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Повернутися назад", callback_data='statistick_back')]]
    )
    return markup
