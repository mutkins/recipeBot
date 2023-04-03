from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import tools
from classes import RecipesDB
import keyboards


class AskFSM(StatesGroup):
    waiting_dish_type = State()
    another_one = State()
    another_one_query = State()


async def ask_recipe(message: types.Message):
    print(f"async def ask_recipe {message.text}")

    await message.answer("Выберите тип блюда", reply_markup=keyboards.get_dish_types_kb())
    await AskFSM.waiting_dish_type.set()


async def send_recipe_by_dish_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Try if it's another_one status - use existing data, else - create new from the message
        if not ('dish_type' in data):
            data['dish_type'] = message.text
        # Creatr new user recipe request object. It keeps data about

        recipe = RecipesDB.get_recipe(dish_type=data.get('dish_type'))
        ingredients_list = RecipesDB.get_ingredients_by_recipe(recipe)
        r = tools.convert_recipe_and_ingr_obj_to_message(recipe, ingredients_list)
    await message.answer_photo(**r, reply_markup=keyboards.get_another_one_kb())
    await AskFSM.another_one.set()


async def send_recipe_by_query(message: types.Message, state: FSMContext):
    print(f"async def search_by_query {message.text}")
    async with state.proxy() as data:
        # Try if it's another_one status - use existing data, else - create new from the message
        if not ('query' in data):
            data['query'] = message.text
        recipe = RecipesDB.get_recipe(query=data.get('query'), dish_type=data.get('dish_type'))
        ingredients_list = RecipesDB.get_ingredients_by_recipe(recipe)
        r = tools.convert_recipe_and_ingr_obj_to_message(recipe, ingredients_list)
    await message.answer_photo(**r, reply_markup=keyboards.get_another_one_kb())
    await AskFSM.another_one_query.set()


async def finish(message: types.Message, state: FSMContext):
    await message.answer(text="Удачной готовки!")
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(ask_recipe, commands=['тип_блюда'], state=None)
    dp.register_message_handler(send_recipe_by_dish_type, state=AskFSM.waiting_dish_type)
    dp.register_message_handler(send_recipe_by_dish_type, state=AskFSM.another_one, commands=['еще_вариант'])
    dp.register_message_handler(finish, state=AskFSM.another_one, commands=['ок'])
    dp.register_message_handler(finish, state=AskFSM.another_one_query, commands=['ок'])
    dp.register_message_handler(send_recipe_by_query, state=AskFSM.another_one_query, commands=['еще_вариант'])
    dp.register_message_handler(send_recipe_by_query, state=AskFSM.another_one)
    dp.register_message_handler(send_recipe_by_query, states=None)
