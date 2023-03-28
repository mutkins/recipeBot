from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import tools
from classes import UserRecipeRequest, RecipesDB
import keyboards


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
        r = tools.convert_recipe_obj_to_message(res)
    await message.answer_photo(**r)
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(ask_recipe, commands=['ask_recipe'], state=None)
    dp.register_message_handler(dish_type, state=AskFSM.dish_type)
