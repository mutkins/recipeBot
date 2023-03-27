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

import RecipesDB
import UserRecipeRequest
import keyboards
import tools
from create_bot import dp, bot


class AskFSM(StatesGroup):
    dish_type = State()
    second = State()
    third = State()
    fourth = State()


async def ask_recipe(message: types.Message):
    print(f"async def ask_recipe {message.text}")

    await message.answer("Выберите тип блюда", reply_markup=keyboards.get_dish_types_kb())
    await AskFSM.dish_type.set()


async def dish_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dish_type'] = message.text
        new_urr = UserRecipeRequest.get_user_recipe_request(user_id=message.from_user.id, dish_type=data['dish_type'])
        res = RecipesDB.get_recipes(urr=new_urr)
    await message.answer(f"Вот что я могу предложить:\n {res}")
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(ask_recipe, commands=['ask_recipe'], state=None)
    dp.register_message_handler(dish_type, state=AskFSM.dish_type)
