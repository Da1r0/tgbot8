from aiogram.fsm.state import StatesGroup, State


class FormStatesGroup(StatesGroup):
    fill_name = State()
    fill_age = State()
    fill_gender = State()
    fill_description = State()
    upload_photo = State()
