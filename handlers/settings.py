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


# @dp.message_handler(commands=['setings'], state='*')
async def settings_command(message: types.Message):
    urs_object = database.get_user_recipe_settings_by_user_id(message.from_user.id)
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


# @dp.message_handler(commands=['ingr'], state=SettingsFSM.main_menu)
async def ingr_command(message: types.Message, state: FSMContext):
    await message.answer("Введите количество ингридиентов\n/cancel - отменить всё")
    await SettingsFSM.ingr_input.set()


# @dp.message_handler(state=SettingsFSM.ingr_input)
async def ingr_input(message: types.Message, state: FSMContext):
    urs_object = database.get_user_recipe_settings_by_user_id(message.from_user.id)
    async with state.proxy() as data:
        data['ingr'] = message.text
    await settings_command(message)


# @dp.message_handler(commands=['diet'], state=SettingsFSM.main_menu)
async def diet_command(message: types.Message, state: FSMContext):
    await message.answer("Введите тип диеты\n/cancel - отменить всё")
    await SettingsFSM.diet_input.set()


# @dp.message_handler(state=SettingsFSM.diet_input)
async def diet_input(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['diet'] = message.text
    await settings_command(message)


# @dp.message_handler(commands=['health'], state=SettingsFSM.main_menu)
async def health_command(message: types.Message, state: FSMContext):
    await message.answer("Введите тип здоровости еды\n/cancel - отменить всё")
    await SettingsFSM.health_input.set()


# @dp.message_handler(state=SettingsFSM.health_input)
async def health_input(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['health'] = message.text
    await settings_command(message)



def register_handlers(dp: Dispatcher):
    dp.register_message_handler(settings_command, commands=['setings'], state='*')
    dp.register_message_handler(ingr_command, commands=['ingr'], state=SettingsFSM.main_menu)
    dp.register_message_handler(ingr_input, state=SettingsFSM.ingr_input)
    dp.register_message_handler(diet_command, commands=['diet'], state=SettingsFSM.main_menu)
    dp.register_message_handler(diet_input, state=SettingsFSM.diet_input)
    dp.register_message_handler(health_command, commands=['health'], state=SettingsFSM.main_menu)
    dp.register_message_handler(health_input, state=SettingsFSM.health_input)
