from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def main_menu():
    buttons = [
        [KeyboardButton(text="/help"), KeyboardButton(text="/orders_all")],
        [KeyboardButton(text="/orders"), KeyboardButton(text="/link")],
        [KeyboardButton(text="/analytics"), KeyboardButton(text="/info")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


def confirm_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("Подтвердить", callback_data="confirm"),
        InlineKeyboardButton("Отмена", callback_data="cancel"),
    ]
    keyboard.add(*buttons)
    return keyboard


def order_info_menu(order_id):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        f"Подробнее о заказе #{order_id}", callback_data=f"info_{order_id}"
    )
    keyboard.add(button)
    return keyboard
