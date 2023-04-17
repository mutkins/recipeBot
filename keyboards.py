from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,\
    InlineKeyboardButton
import classes
import classes.RecipesDB


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
    button = KeyboardButton('/сохранить_рецепт')
    kb.add(button)
    button = KeyboardButton('/ок')
    kb.add(button)
    button = KeyboardButton('/отмена')
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
    button = KeyboardButton('/отмена')
    kb.add(button)
    return kb


def saved_recipes_list(user_id):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    saved_recipes = classes.RecipesDB.get_saved_recipes_list_by_user_id(user_id)
    for saved_recipe in saved_recipes:
        button = KeyboardButton(saved_recipe.recipe_title)
        kb.add(button)
    button = KeyboardButton('/отмена')
    kb.add(button)
    return kb
