from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext

import keyboards
from create_bot import dp, bot


# @dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    await message.answer("<b>Книга рецептов подскажет что приготовить</b>\n"
                         "Для поиска по типу блюда: /тип_блюда\n"
                         "Для управления сохраненными рецептами: /мои_рецепты"
                         "Для свободного поиска - просто напишите свой запрос (можно писать название рецепта,"
                         " часть названия, главный ингредиент, и так далее)"
                         , reply_markup=keyboards.get_welcome_kb(), parse_mode="HTML")



# You can use state '*' if you need to handle all states
# @dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await send_welcome(message)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help', 'хелп'])
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')


