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

import keyboards
import tools
from create_bot import dp, bot


class AskFSM(StatesGroup):
    meal_type = State()
    second = State()
    third = State()
    fourth = State()


async def ask_recipe(message: types.Message):
    print(f"async def ask_recipe {message.text}")
    await message.answer("Выберите тип блюда", reply_markup=keyboards.get_dish_types_kb())
    await AskFSM.meal_type.set()


async def meal_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['meal_type'] = message.text
    await message.answer("Вот что я могу предложить", reply_markup=keyboards.get_dish_types_kb())
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(ask_recipe, commands=['ask_recipe'], state=None)
    dp.register_message_handler(meal_type, state=AskFSM.meal_type)
