from aiogram.fsm.state import StatesGroup, State

class FormStateGroup(StatesGroup):
    fill_name = State()
    fill_age = State()
    upload_photo = State()
