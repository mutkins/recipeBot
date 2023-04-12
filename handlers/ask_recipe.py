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


async def finish(message: types.Message, state: FSMContext):
    log.debug(f"DEF finish, message {message.text}")
    await message.answer(text="Удачной готовки!")
    await state.finish()
    await common.send_welcome(message)


async def set_query_and_send_recipe(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['query'] = message.text
    await AskFSM.query.set()
    await send_recipe(message=message, state=state)


async def set_dish_type_and_send_recipe(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dish_type'] = message.text
    await AskFSM.dish_type.set()
    await send_recipe(message=message, state=state)


async def set_dish_type_query_and_send_recipe(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['query'] = message.text
    await AskFSM.dish_type_query.set()
    await send_recipe(message=message, state=state)


async def send_recipe(message: types.Message, state: FSMContext):
    log.debug(f"DEF send_recipe, message {message.text}")
    async with state.proxy() as data:
        try:
            answ = get_recipe_and_ingredients(data)
        except ValueError as e:
            await message.answer(text=e.args[0])
            await common.cancel_handler(message, state)
    await message.answer_photo(**answ, reply_markup=keyboards.get_another_one_kb())


def register_handlers(dp: Dispatcher):
    # A2 user sends /каталог to get dish_types list
    dp.register_message_handler(get_dish_types_list, commands=['каталог'], state=None)
    # A3 user sends dish_type to get a recipe with the dish_type
    dp.register_message_handler(set_dish_type_and_send_recipe, state=AskFSM.waiting_dish_type)
    # A4 user got a recipe, but sends /еще_вариант to get another recipe with the same dish_type
    dp.register_message_handler(send_recipe, state=AskFSM.dish_type, commands=['еще_вариант'])
    # A5 user got a recipe by dish_type and sends /ok and finishes the dialog
    dp.register_message_handler(finish, state=AskFSM.dish_type, commands=['ок'])
    # A6 user got a recipe by dish_type but sends search query to get a more specify recipe
    dp.register_message_handler(set_dish_type_query_and_send_recipe, state=AskFSM.dish_type)
    # A7 user got a recipe by dish_type and query, but sends /еще_вариант to get another recipe with the same dish_type
    dp.register_message_handler(send_recipe, state=AskFSM.dish_type_query, commands=['еще_вариант'])
    # A8 user got a recipe by dish_type and query and sends /ok and finishes the dialog
    dp.register_message_handler(finish, state=AskFSM.dish_type_query, commands=['ок'])
    # A9 user got a recipe by dish_type and query and sends another query to get recipe matches the query (and dish_type)
    dp.register_message_handler(set_dish_type_query_and_send_recipe, state=AskFSM.dish_type_query)
    # A10 user sends search query to get recipe matches the query
    dp.register_message_handler(set_query_and_send_recipe, state=None)
    # A11 user got a recipe, but sends /еще_вариант to get another recipe with the same query
    dp.register_message_handler(send_recipe, state=AskFSM.query, commands=['еще_вариант'])
    # A12 user got a recipe by query and sends /ok and finishes the dialog
    dp.register_message_handler(finish, state=AskFSM.query, commands=['ок'])
    # A13 user got a recipe by query and sends another query to get recipe matches the query
    dp.register_message_handler(set_query_and_send_recipe, state=AskFSM.query)


def get_recipe_and_ingredients(data):
    # get a recipe list
    recipe_list = RecipesDB.get_recipe_list(query=data.get('query'), dish_type=data.get('dish_type'))
    # Cause we don't wanna send one recipe twice, clear recipe list from sent recipes
    recipe_list = subtract_from_recipe_list_sent_recipes(data, recipe_list)
    # if recipe list's not empy after cleaning choose random recipe from it and save it's id to data['sent_recipes']
    if recipe_list:
        recipe = tools.get_random_item_from_list(recipe_list)
        data['sent_recipes'].append(recipe.id)
        ingredients_list = RecipesDB.get_ingredients_by_recipe(recipe)
        return tools.convert_recipe_and_ingr_obj_to_message(recipe, ingredients_list)
    else:
        raise ValueError('Больше рецептов нет')


def subtract_from_recipe_list_sent_recipes(data, recipe_list):
    # data['sent_recipes'] keeps recipe id's which were sent to user in this dialog
    # Delete from the list recipes, existing in data['sent_recipes']
    if data.get('sent_recipes'):
        for sent_recipe_id in data.get('sent_recipes'):
            i = 0
            for recipe in recipe_list:
                if sent_recipe_id == recipe.id:
                    recipe_list.pop(i)
                i += 1
    else:
        data['sent_recipes'] = []
    return recipe_list
