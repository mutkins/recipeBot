from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
import tools
from classes import RecipesDB
import keyboards
from handlers import common

# Configure logging
logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


class AskFSM(StatesGroup):
    waiting_dish_type = State()
    query = State()
    dish_type = State()
    dish_type_query = State()


async def get_dish_types_list(message: types.Message):
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
        answ = get_recipe_and_ingredients(data)
    await message.answer_photo(**answ, reply_markup=keyboards.get_another_one_kb())
    await AskFSM.dish_type.set()


async def send_recipe_by_dish_type_by_query(message: types.Message, state: FSMContext):
    log.debug(f"DEF send_recipe_by_dish_type_by_query, message {message.text}")
    async with state.proxy() as data:
        # Try if it's another_one status - use existing data, else - create new from the message
        if not ('query' in data):
            data['query'] = message.text
        answ = get_recipe_and_ingredients(data)
    await message.answer_photo(**answ, reply_markup=keyboards.get_another_one_kb())
    await AskFSM.dish_type_query.set()


async def send_recipe_by_query(message: types.Message, state: FSMContext):
    log.debug(f"DEF send_recipe_by_query, message {message.text}")
    async with state.proxy() as data:
        # Try if it's another_one status - use existing data, else - create new from the message
        if not ('query' in data):
            data['query'] = message.text
        answ = get_recipe_and_ingredients(data)
    await message.answer_photo(**answ, reply_markup=keyboards.get_another_one_kb())
    await AskFSM.query.set()


async def finish(message: types.Message, state: FSMContext):
    log.debug(f"DEF finish, message {message.text}")
    await message.answer(text="Удачной готовки!")
    await state.finish()
    await common.send_welcome(message)


def register_handlers(dp: Dispatcher):
    # A2 user sends /каталог to get dish_types list
    dp.register_message_handler(get_dish_types_list, commands=['каталог'], state=None)
    # A3 user sends dish_type to get a recipe with the dish_type
    dp.register_message_handler(send_recipe_by_dish_type, state=AskFSM.waiting_dish_type)
    # A4 user got a recipe, but sends /еще_вариант to get another recipe with the same dish_type
    dp.register_message_handler(send_recipe_by_dish_type, state=AskFSM.dish_type, commands=['еще_вариант'])
    # A5 user got a recipe by dish_type and sends /ok and finishes the dialog
    dp.register_message_handler(finish, state=AskFSM.dish_type, commands=['ок'])
    # A6 user got a recipe by dish_type but sends search query to get a more specify recipe
    dp.register_message_handler(send_recipe_by_dish_type_by_query, state=AskFSM.dish_type)
    # A7 user got a recipe by dish_type and query, but sends /еще_вариант to get another recipe with the same dish_type
    dp.register_message_handler(send_recipe_by_dish_type_by_query, state=AskFSM.dish_type_query, commands=['еще_вариант'])
    # A8 user got a recipe by dish_type and query and sends /ok and finishes the dialog
    dp.register_message_handler(finish, state=AskFSM.dish_type_query, commands=['ок'])
    # A9 user sends search query to get recipe matches the query
    dp.register_message_handler(send_recipe_by_query, states=None)
    # A10 user got a recipe, but sends /еще_вариант to get another recipe with the same query
    dp.register_message_handler(send_recipe_by_query, state=AskFSM.query, commands=['еще_вариант'])
    # A11 user got a recipe by query and sends /ok and finishes the dialog
    dp.register_message_handler(finish, state=AskFSM.query, commands=['ок'])


def get_recipe_and_ingredients1(data):
    # fend a recipe
    recipe = RecipesDB.get_recipe(query=data.get('query'), dish_type=data.get('dish_type'))
    # if there is id this recipe in state proxy data - we get another recipe, until we get a unique
    while recipe.id in data:
        recipe = RecipesDB.get_recipe(query=data.get('query'), dish_type=data.get('dish_type'))
    # if we get unique recipe, save it's id to state proxy data
    data[recipe.id] = 1
    ingredients_list = RecipesDB.get_ingredients_by_recipe(recipe)
    return tools.convert_recipe_and_ingr_obj_to_message(recipe, ingredients_list)


def get_recipe_and_ingredients(data):
    # get a recipe list
    recipe_list = RecipesDB.get_recipe_list(query=data.get('query'), dish_type=data.get('dish_type'))

    # Delete from the list recipes, existing in proxy data list
    if data.get('sent_recipes'):
        for sent_recipe_id in data.get('sent_recipes'):
            for i in range(recipe_list.__len()__)):
                if sent_recipe_id == recipe.id:
                    recipe_list.pop(i)
    else:
        data['sent_recipes'] = []
    recipe = tools.get_random_item_from_list(recipe_list)
    data['sent_recipes'].append(recipe.id)
    deb = data['sent_recipes']
    ingredients_list = RecipesDB.get_ingredients_by_recipe(recipe)
    return tools.convert_recipe_and_ingr_obj_to_message(recipe, ingredients_list)