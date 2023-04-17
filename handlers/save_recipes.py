from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import handlers.common
from classes import RecipesDB
import keyboards
import tools


class SavedFSM(StatesGroup):
    saved_recipes = State()
    query = State()
    dish_type = State()
    dish_type_query = State()


async def get_saved_recipes(message: types.Message, state: FSMContext):
    saved_recipes_list = RecipesDB.get_saved_recipes_list_by_user_id(message.from_user.id)
    if saved_recipes_list:
        for saved_recipe in saved_recipes_list:
            recipe = RecipesDB.get_recipe_by_id(saved_recipe.recipe_id)
            ingredients_list = RecipesDB.get_ingredients_by_recipe(recipe)
            answ = tools.convert_recipe_and_ingr_obj_to_message(recipe, ingredients_list)
            await message.answer_photo(**answ, reply_markup=keyboards.saved_recipes_actions())
        await SavedFSM.saved_recipes.set()
    else:
        await message.answer("Нет сохраненных рецептов")
        await handlers.common.cancel_handler(message, state)


async def delete_all_recipes(message: types.Message, state: FSMContext):
    RecipesDB.delete_saved_recipes_by_user_id(message.from_user.id)
    await message.answer('Рецепты удалены', reply_markup=keyboards.saved_recipes_actions())
    await handlers.common.cancel_handler(message, state)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(get_saved_recipes, state=None, commands='мои_рецепты')
    dp.register_message_handler(delete_all_recipes, state=SavedFSM.saved_recipes, commands='удалить_всё')