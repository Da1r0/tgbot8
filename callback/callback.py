from aiogram.filters.callback_data import CallbackData

FormStateGroup = {}


class GenderCallbackData(CallbackData, prefix='gender'):
    is_male: bool
