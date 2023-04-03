from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
import tools
from classes import RecipesDB
import keyboards

# Configure logging
logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


class AskFSM(StatesGroup):
    waiting_dish_type = State()
    another_one = State()
    another_one_query = State()


async def ask_recipe(message: types.Message):
    log.debug(f"DEF ask_recipe, message {message.text}")
    await message.answer("Выберите тип блюда. После выбора можно будет уточнить выборку запросом в свободной форме",
                         reply_markup=keyboards.get_dish_types_kb())
    await AskFSM.waiting_dish_type.set()


async def send_recipe_by_dish_type(message: types.Message, state: FSMContext):
    log.debug(f"DEF send_recipe_by_dish_type, message {message.text}")
    async with state.proxy() as data:
        # Try if it's another_one status - use existing data, else - create new from the message
        if not ('dish_type' in data):
            data['dish_type'] = message.text
        recipe = RecipesDB.get_recipe(query=data.get('query'), dish_type=data.get('dish_type'))
        ingredients_list = RecipesDB.get_ingredients_by_recipe(recipe)
        r = tools.convert_recipe_and_ingr_obj_to_message(recipe, ingredients_list)
    await message.answer_photo(**r, reply_markup=keyboards.get_another_one_kb())
    await AskFSM.another_one.set()


async def send_recipe_by_query(message: types.Message, state: FSMContext):
    log.debug(f"DEF send_recipe_by_query, message {message.text}")
    async with state.proxy() as data:
        # Try if it's another_one status - use existing data, else - create new from the message
        if not ('query' in data):
            data['query'] = message.text
        recipe = RecipesDB.get_recipe(query=data.get('query'), dish_type=data.get('dish_type'))
        ingredients_list = RecipesDB.get_ingredients_by_recipe(recipe)
        r = tools.convert_recipe_and_ingr_obj_to_message(recipe, ingredients_list)
    await message.answer_photo(**r, reply_markup=keyboards.get_another_one_kb())
    await AskFSM.another_one_query.set()


async def send_recipe_by_dish_type_by_query(message: types.Message, state: FSMContext):
    log.debug(f"DEF send_recipe_by_dish_type_by_query, message {message.text}")
    async with state.proxy() as data:
        # Try if it's another_one status - use existing data, else - create new from the message
        data['query'] = message.text
        recipe = RecipesDB.get_recipe(query=data.get('query'), dish_type=data.get('dish_type'))
        ingredients_list = RecipesDB.get_ingredients_by_recipe(recipe)
        r = tools.convert_recipe_and_ingr_obj_to_message(recipe, ingredients_list)
    await message.answer_photo(**r, reply_markup=keyboards.get_another_one_kb())
    await AskFSM.another_one.set()


async def finish(message: types.Message, state: FSMContext):
    log.debug(f"DEF finish, message {message.text}")
    await message.answer(text="Удачной готовки!")
    await state.finish()


def register_handlers(dp: Dispatcher):
    # user sends /каталог to get dish_types list
    dp.register_message_handler(ask_recipe, commands=['каталог'], state=None)
    # user sends dish_type to get a recipe with the dish_type
    dp.register_message_handler(send_recipe_by_dish_type, state=AskFSM.waiting_dish_type)
    # user got a recipe, but sends /еще_вариант to get another recipe with the same dish_type
    dp.register_message_handler(send_recipe_by_dish_type, state=AskFSM.another_one, commands=['еще_вариант'])
    # user got a recipe by query and sends /ok and finishes the dialog
    dp.register_message_handler(finish, state=AskFSM.another_one, commands=['ок'])
    # user got a recipe by dish_type but sends search query to get a more specify recipe
    dp.register_message_handler(send_recipe_by_dish_type_by_query, state=AskFSM.another_one)
    # user got a recipe by query and sends /ok and finishes the dialog
    dp.register_message_handler(finish, state=AskFSM.another_one_query, commands=['ок'])
    # user got a recipe, but sends /еще_вариант to get another recipe with the same query
    dp.register_message_handler(send_recipe_by_query, state=AskFSM.another_one_query, commands=['еще_вариант'])
    # user sends search query to get recipe matches the query
    dp.register_message_handler(send_recipe_by_query, states=None)
