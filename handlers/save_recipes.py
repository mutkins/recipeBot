from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from classes import RecipesDB
import keyboards
import tools


async def get_saved_recipes(message: types.Message, state: FSMContext):
    saved_recipes_list = RecipesDB.get_saved_recipes_list_by_user_id(message.from_user.id)
    for saved_recipe in saved_recipes_list:
        recipe = RecipesDB.get_recipe_by_id(saved_recipe.recipe_id)
        ingredients_list = RecipesDB.get_ingredients_by_recipe(recipe)
        answ = tools.convert_recipe_and_ingr_obj_to_message(recipe, ingredients_list)
        await message.answer_photo(**answ, reply_markup=keyboards.saved_recipes_actions()


async def delete_all_recipes(message: types.Message, state: FSMContext):
ДОДЕЛАТЬ УДАЛЕНИЕ ОДНОГО И ВСЕХ ТОЖЕ


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(get_saved_recipes, state=None, commands='мои_рецепты')
    dp.register_message_handler(delete_all_recipes, state=None, commands='мои_рецепты')