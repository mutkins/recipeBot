from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,\
    InlineKeyboardButton
import classes


def get_dish_types_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    dish_types = classes.RecipesDB.get_available_dish_types()
    for dish_type in dish_types:
        button = KeyboardButton(dish_type)
        kb.add(button)
    button = KeyboardButton('/отмена')
    kb.add(button)
    return kb


def get_another_one_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('/еще_вариант')
    kb.add(button)
    button = KeyboardButton('/ок')
    kb.add(button)
    button = KeyboardButton('/отмена')
    kb.add(button)
    button = KeyboardButton('/сохранить_рецепт')
    kb.add(button)
    return kb


def get_welcome_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('/каталог')
    kb.add(button)
    button = KeyboardButton('/мои_рецепты')
    kb.add(button)
    return kb


def saved_recipes_actions():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('/удалить_всё')
    kb.add(button)
    button = KeyboardButton('/удалить_один')
    kb.add(button)
    return kb
