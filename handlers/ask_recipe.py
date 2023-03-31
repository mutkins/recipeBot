from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import tools
from classes import UserRecipeRequest, RecipesDB, UserRecipeSettings
import keyboards


class AskFSM(StatesGroup):
    waiting_dish_type = State()
    another_one = State()
    third = State()
    fourth = State()


async def ask_recipe(message: types.Message):
    print(f"async def ask_recipe {message.text}")

    await message.answer("Выберите тип блюда", reply_markup=keyboards.get_dish_types_kb())
    await AskFSM.waiting_dish_type.set()


async def send_recipe(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Try if it's another_one status - use existing data, else - create new from the message
        if not ('dish_type' in data):
            data['dish_type'] = message.text
        # Creatr new user recipe request object. It keeps data about
        new_urr = UserRecipeRequest.get_user_recipe_request(user_id=message.from_user.id, dish_type=data['dish_type'])
        urs = UserRecipeSettings.get_user_recipe_settings_by_user_id(user_id=message.from_user.id)
        recipe = RecipesDB.get_recipes(urr=new_urr, urs=urs)
        ingredients_list = RecipesDB.get_ingredients_by_recipe(recipe)
        r = tools.convert_recipe_and_ingr_obj_to_message(recipe, ingredients_list)
    await message.answer_photo(**r, reply_markup=keyboards.get_another_one_kb())
    await AskFSM.another_one.set()


async def finish(message: types.Message, state: FSMContext):
    await message.answer(text="Удачной готовки!")
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(ask_recipe, commands=['ask_recipe'], state=None)
    dp.register_message_handler(send_recipe, state=AskFSM.waiting_dish_type)
    dp.register_message_handler(send_recipe, state=AskFSM.another_one, commands=['еще'])
    dp.register_message_handler(finish, state=AskFSM.another_one, commands=['ok'])
