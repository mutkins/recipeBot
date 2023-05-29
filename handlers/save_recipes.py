from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import handlers.common
from classes import RecipesDB
import keyboards
import tools


class SavedFSM(StatesGroup):
    saved_recipes = State()
    waiting_recipe_to_delete = State()


async def print_saved_recipes(message: types.Message, state: FSMContext):
    # Reset state if it exists (if user is in the process)
    handlers.common.reset_state(message=message, state=state)
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


async def get_recipes_to_delete(message: types.Message, state: FSMContext):
    await message.answer('Выберите рецепт для удаления из сохраненных', reply_markup=keyboards.saved_recipes_list(message.from_user.id))
    await SavedFSM.waiting_recipe_to_delete.set()


async def delete_recipe_by_title(message: types.Message, state: FSMContext):
    RecipesDB.delete_saved_recipes_by_user_id_by_title(user_id=message.from_user.id, title=message.text)
    await message.answer('Рецепт удален', reply_markup=keyboards.saved_recipes_actions())
    await handlers.common.cancel_handler(message, state)


def register_handlers(dp: Dispatcher):
    # B2 User send /мои_рецепты to get list of saved recipes
    dp.register_message_handler(print_saved_recipes, commands=['мои_рецепты', 'saved_recipes'], state='*')
    # B3 User send /удалить_всё to delete all saved recipes
    dp.register_message_handler(delete_all_recipes, state=SavedFSM.saved_recipes, commands='удалить_всё')
    # B4 User send /удалить_один get saved recipes list as a keyboard
    dp.register_message_handler(get_recipes_to_delete, state=SavedFSM.saved_recipes, commands='удалить_один')
    # B5 User send title of recipe to delete it
    dp.register_message_handler(delete_recipe_by_title, state=SavedFSM.waiting_recipe_to_delete)
