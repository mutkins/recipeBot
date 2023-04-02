from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,\
    InlineKeyboardButton
import classes


def get_dish_types_kb():
    dish_type_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    dish_types = classes.RecipesDB.get_available_dish_types()
    for dish_type in dish_types:
        button = KeyboardButton(dish_type)
        dish_type_kb.add(button)
    return dish_type_kb


def get_another_one_kb():
    another_one_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('/еще')
    another_one_kb.add(button)
    button = KeyboardButton('/ok')
    another_one_kb.add(button)
    return another_one_kb
