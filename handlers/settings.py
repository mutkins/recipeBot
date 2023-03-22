import configparser
import logging
import os
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv
from create_bot import dp, bot
import database


class SettingsFSM (StatesGroup):
    main_menu = State()
    ingr_input = State()
    diet_input = State()
    health_input = State()
    cuisineType_input = State()
    dishType_input = State()
    time_input = State()
    excluded_input = State()


async def settings_command(message: types.Message):
    urs_object, session = database.get_user_recipe_settings_by_user_id(message.from_user.id)
    await message.answer(f"Текущие настройки:\n"
                         f"Количество ингридиентов в рецептах (/ingr): {urs_object.ingr}\n"
                         f"Тип диеты (/diet): {urs_object.diet}\n"
                         f"Тонкая настройка диеты (/health): {urs_object.health}\n"
                         f"Кухня (/cuisineType): {urs_object.cuisineType}\n"
                         f"Тип блюда (/dishType): {urs_object.dishType}\n"
                         f"Время приготовления (/time): {urs_object.time}\n"
                         f"Исключить продукты (/excluded): {urs_object.excluded}\n"
                         f"/cancel - отменить всё")
    await SettingsFSM.main_menu.set()


async def ingr_command(message: types.Message, state: FSMContext):
    await message.answer("Введите количество ингридиентов\n/cancel - отменить всё")
    await SettingsFSM.ingr_input.set()


async def ingr_input(message: types.Message, state: FSMContext):
    urs_object, session = database.get_user_recipe_settings_by_user_id(message.from_user.id)
    urs_object.ingr = message.text
    database.update_user_recipe_settings(session)
    await settings_command(message)


async def diet_command(message: types.Message, state: FSMContext):
    await message.answer("Введите тип диеты\n/cancel - отменить всё")
    await SettingsFSM.diet_input.set()


async def diet_input(message: types.Message, state: FSMContext):
    urs_object, session = database.get_user_recipe_settings_by_user_id(message.from_user.id)
    urs_object.diet = message.text
    database.update_user_recipe_settings(session)
    await settings_command(message)


async def health_command(message: types.Message, state: FSMContext):
    await message.answer("Введите тип здоровости еды\n/cancel - отменить всё")
    await SettingsFSM.health_input.set()


async def health_input(message: types.Message, state: FSMContext):
    urs_object, session = database.get_user_recipe_settings_by_user_id(message.from_user.id)
    urs_object.health = message.text
    database.update_user_recipe_settings(session)
    await settings_command(message)


async def cuisineType_command(message: types.Message, state: FSMContext):
    await message.answer("Введите тип здоровости еды\n/cancel - отменить всё")
    await SettingsFSM.cuisineType_input.set()


async def cuisineType_input(message: types.Message, state: FSMContext):
    urs_object, session = database.get_user_recipe_settings_by_user_id(message.from_user.id)
    urs_object.cuisineType = message.text
    database.update_user_recipe_settings(session)
    await settings_command(message)


async def dishType_command(message: types.Message, state: FSMContext):
    await message.answer("Введите тип здоровости еды\n/cancel - отменить всё")
    await SettingsFSM.dishType_input.set()


async def dishType_input(message: types.Message, state: FSMContext):
    urs_object, session = database.get_user_recipe_settings_by_user_id(message.from_user.id)
    urs_object.dishType = message.text
    database.update_user_recipe_settings(session)
    await settings_command(message)


async def time_command(message: types.Message, state: FSMContext):
    await message.answer("Введите тип здоровости еды\n/cancel - отменить всё")
    await SettingsFSM.time_input.set()


async def time_input(message: types.Message, state: FSMContext):
    urs_object, session = database.get_user_recipe_settings_by_user_id(message.from_user.id)
    urs_object.time = message.text
    database.update_user_recipe_settings(session)
    await settings_command(message)


async def excluded_command(message: types.Message, state: FSMContext):
    await message.answer("Введите тип здоровости еды\n/cancel - отменить всё")
    await SettingsFSM.excluded_input.set()


async def excluded_input(message: types.Message, state: FSMContext):
    urs_object, session = database.get_user_recipe_settings_by_user_id(message.from_user.id)
    urs_object.excluded = message.text
    database.update_user_recipe_settings(session)
    await settings_command(message)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(settings_command, commands=['setings'], state='*')
    dp.register_message_handler(ingr_command, commands=['ingr'], state=SettingsFSM.main_menu)
    dp.register_message_handler(ingr_input, state=SettingsFSM.ingr_input)
    dp.register_message_handler(diet_command, commands=['diet'], state=SettingsFSM.main_menu)
    dp.register_message_handler(diet_input, state=SettingsFSM.diet_input)
    dp.register_message_handler(health_command, commands=['health'], state=SettingsFSM.main_menu)
    dp.register_message_handler(health_input, state=SettingsFSM.health_input)
    dp.register_message_handler(cuisineType_command, commands=['cuisineType'], state=SettingsFSM.main_menu)
    dp.register_message_handler(cuisineType_input, state=SettingsFSM.cuisineType_input)
    dp.register_message_handler(dishType_command, commands=['dishType'], state=SettingsFSM.main_menu)
    dp.register_message_handler(dishType_input, state=SettingsFSM.dishType_input)
    dp.register_message_handler(time_command, commands=['time'], state=SettingsFSM.main_menu)
    dp.register_message_handler(time_input, state=SettingsFSM.time_input)
    dp.register_message_handler(excluded_command, commands=['excluded'], state=SettingsFSM.main_menu)
    dp.register_message_handler(excluded_input, state=SettingsFSM.excluded_input)