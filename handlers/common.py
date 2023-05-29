from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from classes import RecipesDB
import keyboards
from create_bot import dp, bot
import tools


# @dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    await message.answer("<b>Книга рецептов подскажет что приготовить</b>\n"
                         "Для поиска по типу рецепта: /каталог\n"
                         "Для управления сохраненными рецептами: /мои_рецепты\n"
                         "Для свободного поиска - просто напишите свой запрос (можно писать название рецепта,"
                         " часть названия, главный ингредиент, и так далее)"
                         , reply_markup=keyboards.get_welcome_kb(), parse_mode="HTML")


async def cancel_handler(message: types.Message, state: FSMContext):
    reset_state(state=state)
    # Cancel state and inform user about it
    await send_welcome(message)


async def reset_state(state: FSMContext):
    # Cancel state if it exists
    current_state = await state.get_state()
    if current_state:
        await state.finish()


def register_handlers(dp: Dispatcher):
    # A1 user sends /help or smthg like it
    dp.register_message_handler(send_welcome, commands=['start', 'help', 'хелп'])
    dp.register_message_handler(cancel_handler, state='*', commands=['cancel','отмена')


