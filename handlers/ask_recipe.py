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


class AskFSM(StatesGroup):
    meal_type = State()
    second = State()
    third = State()
    fourth = State()




# @dp.message_handler(commands=['ask_recipe'], state=None)
async def ask_recipe(message: types.Message):
    print(f"async def ask_recipe {message.text}")
    await AskFSM.meal_type.set()
    await message.answer("Breakfast, Lunch, Dinner, Snack, Teatime\n/cancel - отменить всё")


# @dp.message_handler(state=AskFSM.meal_type)
async def meal_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['meal_type'] = message.text
    print(f"async def kind_of_meal {message.text}")
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(ask_recipe, commands=['ask_recipe'], state=None)
    dp.register_message_handler(meal_type, state=AskFSM.meal_type)
