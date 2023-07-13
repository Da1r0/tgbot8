import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from callback.callback import GenderCallbackData
from config import config
from keyboards.inline import gender_inline_keyboard
from keyboards.menu import main_menu_command
from states.form import FormStatesGroup

API_TOKEN = config.token

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

users_data = {}


@dp.message(Command('start'))
async def process_start_command(message: Message):
    await message.answer(text='Этот бот демонстрирует работу FSM\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform')


@dp.message(Command('fillform'))
async def handle_fillform(message: Message, state: FSMContext):
    await message.answer('Вы начали заполнение анкеты. Для начала введите имя')
    await state.set_state(FormStatesGroup.fill_name)


@dp.message(StateFilter(FormStatesGroup.fill_name))
async def handle_get_name(message: Message, state: FSMContext):
    name_from_message = message.text
    await state.update_data(name=name_from_message)
    await message.answer('Хорошо. А теперь напишите ваш возраст')
    await state.set_state(FormStatesGroup.fill_age)


@dp.message(StateFilter(FormStatesGroup.fill_age))
async def handle_get_age(message: Message, state: FSMContext):
    age_from_message = message.text
    if age_from_message.isdigit() and 1 <= int(age_from_message) <= 120:
        await state.update_data(age=age_from_message)
        await message.answer('А теперь укажите пол', reply_markup=gender_inline_keyboard)
        await state.set_state(FormStatesGroup.fill_gender)


@dp.callback_query(StateFilter(FormStatesGroup.fill_gender), GenderCallbackData.filter())
async def handle_get_gender(query: CallbackQuery, callback_data: GenderCallbackData, state: FSMContext):
    is_male = callback_data.is_male
    await state.update_data(is_male=is_male)
    await query.message.answer('Укажите ваше описание')
    await state.set_state(FormStatesGroup.fill_description)


@dp.message(StateFilter(FormStatesGroup.fill_description))
async def handle_get_description(message: Message, state: FSMContext):
    description_from_message = message.text
    await state.update_data(description=description_from_message)
    await message.answer('Отправьте фотографию')
    await state.set_state(FormStatesGroup.upload_photo)


@dp.message(StateFilter(FormStatesGroup.upload_photo), F.photo)
async def handle_photo_upload(message: Message, state: FSMContext):
    photo_id = message.photo[0].file_id
    state_data = await state.get_data()
    name = state_data['name']
    age = int(state_data['age'])
    is_male = state_data['is_male']
    description = state_data['description']

    users_data[message.from_user.id] = {
        'name': name,
        'age': age,
        'is_male': is_male,
        'description': description,
        'photo': photo_id,
    }

    await message.answer_photo(photo_id, caption=f'{name}\n{age}\nПол:{is_male}\n{description}')
    await state.clear()


@dp.message(Command('show'))
async def handle_show(message: Message):
    current_user = users_data[message.from_user.id]
    if current_user['is_male']:
        gender = 'Мужской'
    else:
        gender = 'Женский'
    name = current_user['name']
    user_age = current_user['age']
    description = current_user['description']
    photo = current_user['photo']

async def main():
    try:
        print('Bot Started')
        await bot.set_my_commands(main_menu_command)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')